// Set-up database
CREATE OR REPLACE USER neo4jPython SET PASSWORD "python" SET PASSWORD CHANGE NOT REQUIRED;
GRANT ROLE admin to neo4jPython;

CALL apoc.periodic.iterate('MATCH (n) RETURN n', 'DETACH DELETE n', {batchSize:1000})

MATCH (n)-[r]->(m)
RETURN n,r,m

RETURN apoc.version() AS output;

// Create indexes
DROP constraint ON (n:Asset) ASSERT n.uuid is UNIQUE;
DROP constraint ON (n:Agent) ASSERT n.uuid is UNIQUE;
CREATE CONSTRAINT asset_uuid IF NOT EXISTS FOR (n:Asset) REQUIRE n.uuid IS UNIQUE;
CREATE CONSTRAINT agent_uuid IF NOT EXISTS FOR (n:Agent) REQUIRE n.uuid IS UNIQUE;
CREATE INDEX actief  FOR (n:Asset) ON (n.isActief);
CREATE INDEX ean FOR (n:Asset) ON (n.eanNummer);
CREATE INDEX naam FOR (n:Asset) ON (n.naam);
CREATE INDEX naampad FOR (n:Asset) ON (n.naampad);

show indexes