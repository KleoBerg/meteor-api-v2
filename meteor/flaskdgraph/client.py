

from flask import current_app, g
import pydgraph
import logging

class DGraph(object):
    # Class for dgraph database connection

    def __init__(self, app=None):
        self.app = app
        self.client_stub = None
        self.logger = logging.getLogger(__name__)
        
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        if 'dgraph' in app.extensions:
            self.logger.warning("DGraph extension already initialized for this app.")
            return
        
        app.extensions['dgraph'] = self

        self.app = app

        app.config.setdefault('DGRAPH_ENDPOINT', 'localhost:9080')
        app.config.setdefault('DGRAPH_CREDENTIALS', None)
        app.config.setdefault('DGRAPH_OPTIONS', None)
        app.teardown_appcontext(self.teardown)
        
        self.client_stub = pydgraph.DgraphClientStub(app.config['DGRAPH_ENDPOINT'],
                                                     credentials=app.config['DGRAPH_CREDENTIALS'],
                                                     options=app.config['DGRAPH_OPTIONS'])



    # create a/ get the connection
    @property
    def connection(self):
        if not hasattr(g, 'dgraph_client'):
            self.logger.debug(f"Establishing connection to DGraph: {current_app.config['DGRAPH_ENDPOINT']}")

            g.dgraph_client = pydgraph.DgraphClient(self.client_stub)
    
        return g.dgraph_client
    
    # create a/ get the transaction
    @property
    def txn(self):
        if not hasattr(g, 'dgraph_txn'):
            g.dgraph_txn = self.connection.txn()
        
        return g.dgraph_txn
    
    # teardown at the end of each request, commit transaction if no exception, discard if exception -> atomical requests
    def teardown(self, exception):
        txn = g.pop('dgraph_txn', None)
        if txn is not None:
            if exception is None:
                try:
                    txn.commit()
                except Exception as e:
                    self.logger.error(f"Error committing DGraph transaction: {e}")
                    txn.discard()
            else:  
                self.logger.info(f"Discarding transaction due to request exception: {exception}")
                txn.discard()

    # Close the client stub when the app shuts down
    def close(self):
        if self.client_stub is not None:
            self.client_stub.close()
            self.client_stub = None
            self.logger.info("DGraph client stub closed.")
        

    