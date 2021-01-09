from dbtools import orm

class Dao():
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type
        self._table_name = "{name}s".format(name=dto_type.__name__.lower())

    def insert_bulk(self, dto_list):
        for dto in dto_list:
            self.insert(dto)

    def insert(self, dto):
        dto_fields_dict = vars(dto)
        column_names = ','.join(dto_fields_dict.keys())
        args = dto_fields_dict.values()
        qmarks = ','.join(['?'] * len(dto_fields_dict))
        query = 'INSERT INTO {table_name} ({column_names}) VALUES ({qmarks})'.format(
            table_name=self._table_name,
            column_names=column_names,
            qmarks=qmarks
            )
        self._conn.execute(query, args)

    def get_all(self):
        cursor = self._conn.cursor()
        cursor.execute('SELECT * FROM {table_name}'.format(table_name=self._table_name))
        return orm(cursor, self._dto_type)

    def get(self, **keyvals):
        column_names = keyvals.keys()
        args = keyvals.values()
        query = 'SELECT * FROM {table_name} WHERE {conditions}'.format(
            table_name=self._table_name,
            conditions=' AND '.join([col + '=?' for col in column_names])
            )
        cursor = self._conn.cursor()
        cursor.execute(query, args)
        return orm(cursor, self._dto_type)

    def update(self, set_values, conditions):
        set_column_names = set_values.keys()
        set_params = set_values.values()
        cond_column_names = conditions.keys()
        cond_params = conditions.values()
        params = set_params + cond_params
        query = 'UPDATE {table_name} SET ({columns}) WHERE ({conditions})'.format(
            table_name=self._table_name,
            columns=', '.join([set + '=?' for set in set_column_names]),
            conditions=' AND '.join([cond + '=?' for cond in cond_column_names])
            )
        self._conn.execute(query, params)