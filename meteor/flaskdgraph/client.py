
#     1 import pydgraph
#     2 
#     3 class DGraph:
#     4     """
#     5     A wrapper for the pydgraph client to integrate with a Flask application.
#     6     """
#     7     def __init__(self):
#     8         self.client = None
#     9 
#    10     def init_app(self, app):
#    11         """
#    12         Initializes the Dgraph client using configuration from the Flask app.
#    13         """
#    14         host = app.config.get('DGRAPH_HOST')
#    15         port = app.config.get('DGRAPH_PORT')
#    16 
#    17         client_stub = pydgraph.DgraphClientStub(f'{host}:{port}')
#    18         self.client = pydgraph.DgraphClient(client_stub)
#    19 
#    20         app.logger.info(f'Successfully connected to Dgraph at {host}:{port}')
#    21 
#    22     def query(self, query, variables=None):
#    23         """
#    24         A helper method to run a query.
#    25         """
#    26         if not self.client:
#    27             raise Exception("Dgraph client not initialized. Did you call init_app?")
#    28 
#    29         txn = self.client.txn(read_only=True)
#    30         try:
#    31             return txn.query(query, variables=variables)
#    32         finally:
#    33             txn.discard()
