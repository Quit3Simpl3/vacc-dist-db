import inspect

def orm(cursor, dto_type):
    args = inspect.getargspec(dto_type.__init__).args # Constructor args' names
    args = args[1:] # Ignore 'self' - the first arg
    col_names = [column[0] for column in cursor.description]
    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]

def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)