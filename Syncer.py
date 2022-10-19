import logging
import time
import traceback
from datetime import datetime

import neo4j.exceptions

from AgentSyncer import AgentSyncer
from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.RelatieProcessor import RelatieProcessor
from EventProcessors.RelationNotCreatedError import BetrokkeneRelationNotCreatedError, AssetRelationNotCreatedError
from FeedEventsCollector import FeedEventsCollector
from FeedEventsProcessor import FeedEventsProcessor
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler


class Syncer:
    def __init__(self, connector: Neo4JConnector, request_handler: RequestHandler, eminfra_importer: EMInfraImporter, settings=None):
        self.connector = connector
        self.request_handler = request_handler
        self.eminfra_importer = eminfra_importer
        self.events_collector = FeedEventsCollector(eminfra_importer)
        self.events_processor = FeedEventsProcessor(connector, eminfra_importer)
        self.settings = settings
        self.sync_start = None
        self.sync_end = None
        if 'time' in self.settings:
            self.sync_start = self.settings['time']['start']
            self.sync_end = self.settings['time']['end']

    def start_syncing(self, stop_when_fully_synced=False):
        while True:
            try:
                params = self.connector.get_page_by_get_or_create_params()
                if params['freshstart']:
                    self.perform_fresh_start_sync(params)
                else:
                    self.perform_syncing(stop_when_fully_synced=stop_when_fully_synced)
                    if stop_when_fully_synced:
                        break
            except Exception as ex:
                logging.error('Could not start synchronising. Do you have connection to the internet and the Neo4J database?')
                logging.error(ex)
                logging.info('Retrying in 30 seconds.')
                time.sleep(30)

    def perform_fresh_start_sync(self, params: dict):
        page_size = params['pagesize']
        page = params['page']
        if page == -1:
            tx_context = self.connector.start_transaction()
            self.save_last_feedevent_to_params(page_size, tx_context=tx_context)
            self.connector.commit_transaction(tx_context)

        self.check_apoc()

        while True:
            # main sync loop for getting all assets/agents/relations
            params = self.connector.get_page_by_get_or_create_params()
            otltype = params['otltype']
            cursor = params['cursor']
            page_size = params['pagesize']

            if otltype == -1:
                otltype = 1
            if otltype >= 5:
                break

            tx_context = self.connector.start_transaction()
            self.eminfra_importer.cursor = cursor
            if otltype == 1:
                agents = self.eminfra_importer.import_agents_from_webservice_page_by_page(page_size)
                agentsyncer = AgentSyncer(emInfraImporter=self.eminfra_importer, neo4J_connector=self.connector)
                agentsyncer.tx_context = tx_context
                agentsyncer.update_agents(agents)
            elif otltype == 2:
                assets = self.eminfra_importer.import_assets_from_webservice_page_by_page(page_size)
                asset_processor = NieuwAssetProcessor()
                asset_processor.tx_context = tx_context
                for asset in assets:
                    asset_processor.create_asset_from_jsonLd_dict(asset)
            elif otltype == 3:
                start = time.time()
                assetrelaties = self.eminfra_importer.import_assetrelaties_from_webservice_page_by_page(page_size)
                relatie_processor = RelatieProcessor()
                relatie_processor.tx_context = tx_context
                for assetrelatie in assetrelaties:
                    try:
                        relatie_processor.create_assetrelatie_from_jsonLd_dict(assetrelatie)
                    except AssetRelationNotCreatedError:
                        pass
                        #raise AssetRelationNotCreatedError
                end = time.time()
                logging.info(f'time for 100 relations: {round(end - start, 2)}')
            elif otltype == 4:
                start = time.time()
                betrokkenerelaties = self.eminfra_importer.import_betrokkenerelaties_from_webservice_page_by_page(page_size)
                relatie_processor = RelatieProcessor()
                relatie_processor.tx_context = tx_context
                for betrokkenerelatie in betrokkenerelaties:
                    try:
                        relatie_processor.create_betrokkenerelatie_from_jsonLd_dict(betrokkenerelatie)
                    except BetrokkeneRelationNotCreatedError:
                        pass
                        # raise BetrokkeneRelationNotCreatedError
                end = time.time()
                logging.info(f'time for 100 betrokkenerelations: {round(end - start, 2)}')

            cursor = self.eminfra_importer.cursor
            if cursor == '':
                otltype += 1
            self.connector.save_props_to_params(tx=tx_context, params=
                {'otltype': otltype,
                 'cursor': cursor,
                 'last_update_utc': datetime.utcnow()})
            if otltype >= 5:
                self.connector.save_props_to_params(tx=tx_context, params=
                    {'freshstart': False})
            self.connector.commit_transaction(tx_context)

    def save_last_feedevent_to_params(self, page_size: int, tx_context):
        start_num = 1
        step = 5
        start_num = self.recur_exp_find_start_page(current_num=start_num, step=step, page_size=page_size)
        current_page_num = self.recur_find_last_page(current_num=int(start_num / step), current_step=int(start_num / step),
                                                     step=step, page_size=page_size)

        # doublecheck
        event_page = self.eminfra_importer.get_events_from_page(page_num=current_page_num, page_size=page_size)
        links = event_page['links']
        prev_link = next((l for l in links if l['rel'] == 'previous'), None)
        if prev_link is not None:
            raise RuntimeError('algorithm did not result in the last page')

        # find last event_id
        entries = event_page['entries']
        last_event_id = entries[0]['id']

        self.connector.save_props_to_params(tx=tx_context, params=
            {'event_id': last_event_id,
             'page': current_page_num})

    def recur_exp_find_start_page(self, current_num, step, page_size):
        event_page = self.eminfra_importer.get_events_from_page(page_num=current_num, page_size=page_size)
        if 'message' not in event_page:
            return self.recur_exp_find_start_page(current_num=current_num * step, step=step, page_size=100)
        return current_num

    def recur_find_last_page(self, current_num, current_step, step, page_size):
        new_i = 0
        for i in range(step + 1):
            new_num = current_num + current_step * i
            event_page = self.eminfra_importer.get_events_from_page(page_num=new_num, page_size=page_size)
            if 'message' in event_page:
                new_i = i - 1
                break
        if current_step == 1:
            return current_num + current_step * new_i

        return self.recur_find_last_page(current_num + current_step * new_i,
                                         int(current_step / step), step, page_size)

    def calculate_sync_allowed_by_time(self):
        if self.sync_start is None:
            return True

        start_struct = time.strptime(self.sync_start, "%H:%M:%S")
        end_struct = time.strptime(self.sync_end, "%H:%M:%S")
        now = datetime.utcnow().time()
        start = now.replace(hour=start_struct.tm_hour, minute=start_struct.tm_min, second=start_struct.tm_sec)
        end = now.replace(hour=end_struct.tm_hour, minute=end_struct.tm_min, second=end_struct.tm_sec)
        v = start < now < end
        return v

    def perform_syncing(self, stop_when_fully_synced=False):
        sync_allowed_by_time = self.calculate_sync_allowed_by_time()

        while sync_allowed_by_time:
            params = self.connector.get_page_by_get_or_create_params()
            current_page = params['page']
            completed_event_id = params['event_id']
            page_size = params['pagesize']
            logging.info(f'starting a sync cycle, page: {str(current_page + 1)} event_id: {str(completed_event_id)}')
            start = time.time()

            eventsparams_to_process = self.events_collector.collect_starting_from_page(current_page, completed_event_id,
                                                                                       page_size)

            total_events = sum(len(lists) for lists in eventsparams_to_process.event_dict.values())
            if total_events == 0:
                with self.connector.driver.session(database=self.connector.db) as session:
                    tx = session.begin_transaction()
                    self.connector.save_props_to_params(params={'last_sync_utc': datetime.utcnow()}, tx=tx)
                    tx.commit()
                    tx.close()

                if stop_when_fully_synced:
                    logging.info(f"The database is fully synced.")
                    break
                logging.info(f"The database is fully synced. Continuing keep up to date in 30 seconds")

                time.sleep(30)  # wait 30 seconds to prevent overloading API

                continue

            end = time.time()

            self.log_eventparams(eventsparams_to_process.event_dict, round(end - start, 2))
            try:
                self.events_processor.process_events(eventsparams_to_process)
            except BetrokkeneRelationNotCreatedError:
                # agents syncen of na 24h
                self.events_processor.tx_context.rollback()
                self.sync_all_agents()
            except AssetRelationNotCreatedError:
                self.events_processor.tx_context.rollback()
                self.sync_all_agents()
            except Exception as exc:
                traceback.print_exception(exc)
                self.events_processor.tx_context.rollback()

            sync_allowed_by_time = self.calculate_sync_allowed_by_time()

    @staticmethod
    def log_eventparams(event_dict, time: float):
        total = sum(len(events) for events in event_dict.values())
        logging.info(f'fetched {total} asset events to sync in {time} seconds')
        for k, v in event_dict.items():
            if len(v) > 0:
                logging.info(f'number of events of type {k}: {len(v)}')

    def sync_all_agents(self):
        logging.info(f'sync_all_agents started')
        agentsyncer = AgentSyncer(emInfraImporter=self.eminfra_importer, neo4J_connector=self.connector)
        agentsyncer.sync_agents()
        logging.info(f'sync_all_agents done')

    def check_apoc(self):
        apoc_check_query = 'RETURN apoc.version() AS output;'

        tx_context = self.connector.start_transaction()
        try:
            result = tx_context.run(apoc_check_query)
            version = result.data()[0]['output']
            logging.info(f'The apoc plugin is installed, version {version}')
            tx_context.commit()
        except neo4j.exceptions.ClientError as exc:
            if "Unknown function 'apoc.version'" in exc.message:
                tx_context.rollback()
                logging.error('The apoc plugin is not enabled in this Neo4J database. Please install it first.')
                raise RuntimeError('The apoc plugin is not enabled in this Neo4J database. Please install it first.')

