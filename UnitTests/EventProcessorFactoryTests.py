from unittest import TestCase
from unittest.mock import Mock

from EventProcessorFactory import EventProcessorFactory
from EventProcessors.NaamGewijzigdProcessor import NaamGewijzigdProcessor
from EventProcessors.NieuwOnderdeelProcessor import NieuwOnderdeelProcessor


class EventProcessorFactoryTests(TestCase):
    """These tests require a running instance of neo4J, defined in the setUp method"""

    def test_factory_returns_correct_processor(self):
        processor = EventProcessorFactory.CreateEventProcessor(event_type='NIEUW_ONDERDEEL', tx_context=Mock(),
                                                               em_infra_importer=Mock())
        self.assertTrue(isinstance(processor, NieuwOnderdeelProcessor))

        processor = EventProcessorFactory.CreateEventProcessor(event_type='NAAM_GEWIJZIGD', tx_context=Mock(),
                                                               em_infra_importer=Mock())
        self.assertTrue(isinstance(processor, NaamGewijzigdProcessor))

        processor = EventProcessorFactory.CreateEventProcessor(event_type='POSTIT_GEWIJZIGD', tx_context=Mock(),
                                                               em_infra_importer=Mock())
        self.assertIsNone(processor)

        with self.assertRaises(NotImplementedError):
            processor = EventProcessorFactory.CreateEventProcessor(event_type='NOT_IMPLEMENTED', tx_context=Mock(),
                                                                   em_infra_importer=Mock())
