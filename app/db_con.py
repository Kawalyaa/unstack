# import os
from flask import current_app
import psycopg2
# from psycopg2.extras import RealDictCursor
# from app.tables import tables


class DataBaseConnection:
    """ Handles the main connection to the database of the app setting """

    # def init_db(self):
    # """Create tables and return connection"""
    # con = psycopg2.connect("dbname='unstack' host='localhost' port=5432  user='kawalya' password='kawalyaa'")
    # with con as con, con.cursor() as cur:
    # with current_app.open_resource('schema.sql', mode='r') as sql:
    # cur.execute(sql.read())
    # con.commit()
    # return con
    def init_db(self):
        db_url = current_app.config['DATABASE_URL']
        con = psycopg2.connect(db_url)
        # con = psycopg2.connect("dbname='unstack' port=5432  user='kawalya' password='kawalyaa'")
        with con as con, con.cursor() as cur:
            with current_app.open_resource('schema.sql', mode='r') as sql:
                cur.execute(sql.read())
        con.commit()
        return con

    # def _init_db(self):
    #    db_url = current_app.config['DATABASE_URL']
    #    con = psycopg2.connect(db_url)
    # con = psycopg2.connect("dbname='unstack_test' port=5432  user='kawalya' password='kawalyaa'")
    #    with con as con, con.cursor(cursor_factory=RealDictCursor) as cur:
    #        with current_app.open_resource('schema.sql', mode='r') as sql:
    #            cur.executcon.commit()
    #    return ce(sql.read())con.commit()
    #    return c
    #    con.commit()
    #    return con

    def destroydb(self):
        """Deletes all tables after tests have been run"""
        # con = psycopg2.connect('')
        con = psycopg2.connect("dbname='unstack' host='127.0.0.1' port=5432  user='kawalya' password='kawalyaa'")
        cur = con.cursor()
        users = """DROP TABLE IF EXISTS users CASCADE;"""
        blacklist = """DROP TABLE IF EXISTS blacklist CASCADE;"""
        questions = """DROP TABLE IF EXISTS questions CASCADE;"""
        answers = """DROP TABLE IF EXISTS answers CASCADE;"""
        queries = [users, blacklist, questions, answers]
        for query in queries:
            cur.execute(query)
        con.commit()

    def drop_all_tables(self):
        drop_all = self.destroydb()
        return drop_all
