from collections import OrderedDict

from .bridge import internal_api

import time


# TODO we need to deal here with this metatokens stuff and many rals
# Maintains the resulset and the token after the run_query
class ResultSet:

    def __init__(self, client, metaToken, startTime):
        self.client = client
        self.metaToken = metaToken
        self.startTime = startTime

    # this will call the get_result api
    def get(self):
        temp = internal_api.run_query_get_results(self.client, self.metaToken, self.startTime)

        return temp

    # TODO see Rodriugo proposal for interesting actions/operations here


class SQL(object):

    def __init__(self):
        self.tables = OrderedDict()

    def __del__(self):
        all_table_names = list(self.tables.keys())
        for table_name in all_table_names:
            self.drop_table(table_name)

    # TODO percy
    def create_database(self, database_name):
        pass

    # ds is the DataSource object
    def create_table(self, table_name, datasource):
        self._verify_table_name(table_name)

        # TODO verify cuda ipc ownership or reuse resources here

        self.tables[table_name] = datasource

        # # TODO percy create table result
        # output = OrderedDict()
        # output['name'] = table_name
        # output['datasource'] = datasource

        # return output

    # TODO percy this is to save materialized tables avoid reading from the data source
    def create_view(self, view_name, sql):
        pass

    # TODO percy
    def drop_database(self, database_name):
        pass

    # TODO percy drops should be here but this will be later (see Felipe proposal free)
    def drop_table(self, table_name):
        if table_name in self.tables:
            del self.tables[table_name]

    # TODO percy
    def drop_view(self, view_name):
        pass

    def run_query(self, client, sql):
        startTime = time.time()
        metaToken = internal_api.run_query_get_token(client, sql)
        return ResultSet(client, metaToken, startTime)


    def _verify_table_name(self, table_name):
        # TODO percy throw exception
        if table_name in self.tables:
            # TODO percy improve this one add the fs type so we can raise a nice exeption
            raise Exception('Fail add table_name already exists')

