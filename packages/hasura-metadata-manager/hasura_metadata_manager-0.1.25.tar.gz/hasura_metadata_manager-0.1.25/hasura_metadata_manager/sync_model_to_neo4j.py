import logging
from sqlalchemy.orm import sessionmaker

from hasura_metadata_manager import Supergraph
from hasura_metadata_manager.load import create_engine_config
logger = logging.getLogger(__name__)

def sync_model_to_neo4j():
    """
    Export model RDF with proper transaction management and Neo4j sync
    """

    session = None
    try:
        engine = create_engine_config(os.getenv("DATABASE_URL", ''))
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
        assert session is not None, "Session not initialized."

        # Initialize Neo4j configuration in its own transaction
        with session.begin_nested():
            Supergraph.configure_neo4j()

        # Generate model metadata graph in a separate transaction
        with session.begin_nested():
            graph = Supergraph.generate_model_metadata_graph(session)

            # Verify graph generation succeeded
            assert len(graph) > 0, "Generated model RDF graph is empty"

        # Sync to Neo4j in final transaction
        with session.begin_nested():
            Supergraph.sync_all_to_neo4j(
                session=session,
                source_graph=graph
            )

        # Commit all changes if everything succeeded
        session.commit()

    except Exception as e:
        session.rollback()
        logger.error(f"Model RDF export failed: {str(e)}")
        raise
