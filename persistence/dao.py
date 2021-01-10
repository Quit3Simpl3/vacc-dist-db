from .dbtools import orm

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
        args = list(dto_fields_dict.values())
        qmarks = ','.join(['?'] * len(dto_fields_dict))
        query = 'INSERT INTO {table_name} ({column_names}) VALUES ({qmarks})'.format(
            table_name=self._table_name,
            column_names=column_names,
            qmarks=qmarks
            )

        self._conn.execute(query, args)

    def get_all(self,order_by="id",ascending =True):
        cursor = self._conn.cursor()
        if ascending:
            order_by += " ASC"
        cursor.execute('SELECT * FROM {table_name} ORDER BY {order_by}'.format(
            table_name=self._table_name,
            order_by=order_by
            ))
        return orm(cursor, self._dto_type)

    def get(self, order_by="id", **keyvals):
        column_names = list(keyvals.keys())
        if order_by not in column_names:
            order_by = "id"

        args = list(keyvals.values())
        if not keyvals:
            raise Exception("no condition have been provided for sql select query")

        query = 'SELECT * FROM {table_name} WHERE {conditions} ORDER BY {order_by} DESC'.format(
            table_name=self._table_name,
            conditions=' AND '.join([col + '=?' for col in column_names]),
            order_by=order_by
        )
        cursor = self._conn.cursor()
        cursor.execute(query, args)
        return orm(cursor, self._dto_type)

    def update(self, set_values, conditions):
        set_column_names = list(set_values.keys())
        set_params = list(set_values.values())
        cond_column_names = list(conditions.keys())
        cond_params = list(conditions.values())
        params = set_params + cond_params
        query = 'UPDATE {table_name} SET {columns} WHERE {conditions}'.format(
            table_name=self._table_name,
            columns=', '.join([set + '=?' for set in set_column_names]),
            conditions=' AND '.join([cond + '=?' for cond in cond_column_names])
            )
        self._conn.execute(query, params)

    def delete(self,**keyvals):
        column_names = list(keyvals.keys())
        params = list(keyvals.values())
        query = 'DELETE FROM {} WHERE {}'.format(self._table_name,
                                                ' AND '.join([col + '=?' for col in column_names]))
        c = self._conn.cursor()
        c.execute(query, params)
