CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY NOT NULL,
    name character varying (50) NOT NULL,
    user_name character varying (50) NOT NULL,
    email character varying (50) NOT NULL,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    password character varying (15) NOT NULL
    );

CREATE TABLE IF NOT EXISTS blacklist (
    tokens character varying(200) NOT NULL
    );

CREATE TABLE IF NOT EXISTS questions (
    question_id serial PRIMARY KEY NOT NULL,
    title varchar (50) NOT NULL,
    description varchar (200) NOT NULL,
    user_id numeric NOT NULL,
    created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
    );

CREATE TABLE IF NOT EXISTS answers (
    answer_id serial PRIMARY KEY NOT NULL,
    question_id numeric NOT NULL,
    user_id numeric NOT NULL,
    description varchar (200) NOT NULL,
    up_votes numeric DEFAULT 0,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    user_preferred boolean DEFAULT false
    );
