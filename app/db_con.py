import os
from flask import current_app
import psycopg2


class DataBaseConnection:
    """ Handles the main connection to the database of the app setting """

    def init_db(self):
        con = os.getenv('DATABASE_URL')
        cur = con.cursor()
        with current_app.open_resource('schema.sql', mode='r') as sql:
            cur.execute(sql.read())
        con.commit()
        return con

    def destroydb(self):
        """Deletes all tables after tests have been run"""
        con = psycopg2.connect("dbname='unstack_test' host='localhost' port='5432'  user='kawalya' password='kawalyaa'")
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
        """destroying all the tables"""
        drop_all = self.destroydb()
        return drop_all
