import psycopg2
from tables import tables, destroydb


class DataBaseConnection:
    """ Handles the main connection to the database of the app setting """

    def init_db(self):
        """Create tables and return connection"""
        con = psycopg2.connect("dbname='unstack' host='localhost' port=5432  user='kawalya' password='kawalyaa'")
        cur = con.cursor()
        all_tables = tables()
        for query in all_tables:
            cur.execute(query)
            con.commit()
        return con

    def drop_all_tables(self):
        drop_all = destroydb()
        con = self.init_db()
        cur = con.cursor()
        for query in drop_all:
            cur.execute(query)
            con.commit()
