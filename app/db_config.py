def tables():
    """ Contains all tables creation queries"""
    users = """ CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY NOT NULL,
    name character varying (50) NOT NULL,
    user_name character varying (50) NOT NULL,
    email character varying (50) NOT NULL,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    password character varying (15) NOT NULL
    );"""

    blacklist = """ CREATE TABLE IF NOT EXISTS blacklist (
    tokens character varying(200) NOT NULL
    ); """
    return[users, blacklist]


def destroydb():
    """Deletes all tables after tests have been run"""
    users = """DROP TABLE IF EXISTS users CASCADE;"""
    blacklist = """DROP TABLE IF EXISTS blacklist CASCADE;"""
    return[users, blacklist]
