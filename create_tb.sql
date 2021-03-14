-- SQL commands for creating tables in DB. 

CREATE DATABASE new_vocab_db;

CREATE TABLE users(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    email VARCHAR(50) NOT NULL,
    user_password VARCHAR(300) NOT NULL,
    telegram_id BIGINT NULL, 
    user_level VARCHAR(25) NULL
);

CREATE TABLE whole_vocab(
    id_in_whole BIGSERIAL NOT NULL PRIMARY KEY,
    word_in_whole VARCHAR (200) NOT NULL,
    definition_of_word VARCHAR(2000) NOT NULL DEFAULT 'no definition',
    user_id BIGINT NOT NULL,
    status_of_word_in_whole VARCHAR(10) DEFAULT 'not done'
);


CREATE TABLE dynamic_vocab(
    user_id BIGINT NOT NULL,
    word_in_dynamic VARCHAR(200) NOT NULL,
    definition_in_dynamic VARCHAR(2000),
    id_in_dynamic BIGINT,
    status_of_word_in_dynamic VARCHAR(10) DEFAULT 'not done'
);
