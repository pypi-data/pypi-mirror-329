from contextlib import contextmanager

import pyodbc


@contextmanager
def easy_open_data_connection(constr: str, autocommit: bool = True):
    con = None
    try:
        con = pyodbc.connect(constr, autocommit=autocommit)
        yield con
    finally:
        if con:
            con.close()
