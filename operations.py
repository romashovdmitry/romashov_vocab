from config_file import db, app
import telegram_api_request
from typing import Tuple

import random as rm
import re
import config_file

# Row in tables can have 3 statuses:
# not_done - nothing is happening with row in table
# doing - for deleting of row in table
# modif - for modification of row in table

def show_word(pk_of_user_in_db: int) -> str: 
    '''
    Foo is using on level "default". Foo returns definition of randomly selected 
    word and assign status "doing" to row.  
    
    '''
    if len(config_file.db_select("SELECT * \
                                FROM dynamic_vocab WHERE user_id={}".
                                format(pk_of_user_in_db))) > 0:
        highest = len(config_file.db_select("SELECT * \
                                            FROM dynamic_vocab \
                                            WHERE user_id={}".
                                            format(pk_of_user_in_db)))
        config_file.db_update("WITH test AS (\
                            SELECT id_in_dynamic, ROW_NUMBER() OVER() \
                            FROM dynamic_vocab WHERE user_id={})\
                            UPDATE dynamic_vocab \
                            SET status_of_word_in_dynamic='doing' \
                            WHERE id_in_dynamic IN  (SELECT id_in_dynamic \
                                                    FROM test \
                                                    WHERE row_number=(SELECT floor(random() \
                                                    * 0 + {})::int))".format(pk_of_user_in_db, highest))
        return(config_file.db_select("SELECT definition_in_dynamic FROM dynamic_vocab \
                                    WHERE status_of_word_in_dynamic='doing'")[0][0])
    return('Словарь закончился!\n\nДобавь новые слова или пройдись еще раз по словарю. ')

def vocab_work(pk_of_user_in_db: int) -> str: 
    '''Foo is using on level "default". Foo fills table dynamic_vocab'''
    config_file.db_update("DELETE FROM dynamic_vocab WHERE user_id={}".format(pk_of_user_in_db))
    config_file.db_update("INSERT INTO dynamic_vocab \
                        (user_id, word_in_dynamic, definition_in_dynamic, id_in_dynamic) \
                        SELECT user_id, word_in_whole, definition_of_word, id_in_whole \
                        FROM whole_vocab WHERE user_id={}".format(pk_of_user_in_db))
    return(show_word(pk_of_user_in_db))

def checking_word(message_word: str, pk_of_user_in_db: int) -> Tuple[bool, str]:    
    '''Foo checks accuracy of written (to bot) word'''
    if message_word.rstrip()[::-1].rstrip()[::-1].lower() == \
        config_file.db_select("SELECT word_in_dynamic \
                            FROM dynamic_vocab \
                            WHERE status_of_word_in_dynamic='doing'") \
                            [0][0].lower():
        config_file.db_update("DELETE FROM dynamic_vocab \
                              WHERE status_of_word_in_dynamic='doing'")
        return (True, None)
    word = config_file.db_select("SELECT word_in_dynamic \
                                FROM dynamic_vocab \
                                WHERE status_of_word_in_dynamic='doing'") \
                                [0][0]
    config_file.db_update ("DELETE FROM dynamic_vocab \
                        WHERE status_of_word_in_dynamic='doing'")
    return (False, word)

def show_all_words_for_deleting(pk_of_user_in_db, chat_id):
    '''
    Foo is using on level "deleting". Foo returns whole list of words in table 
    whole_vocab. Returning is with a frequency of 25 words. 
    
    '''
    config_file.db_update("DELETE FROM dynamic_vocab \
                        WHERE user_id={}".format(pk_of_user_in_db))
    config_file.db_update("INSERT INTO dynamic_vocab \
                        (user_id, word_in_dynamic, id_in_dynamic) \
                        SELECT user_id, word_in_whole, id_in_whole \
                        FROM whole_vocab WHERE user_id={}".
                        format(pk_of_user_in_db))
    list_all_words = config_file.db_select("SELECT word_in_dynamic \
                                            FROM dynamic_vocab \
                                            WHERE user_id={}".
                                            format(pk_of_user_in_db))
    list_all_words = [i[0] for i in list_all_words]
    if len(list_all_words) < 1: 
        telegram_api_request.ButtonCreate(message_text=
                                        'Словарь пустой.\nСначала следует добавить слова.',
                                        chat_id=chat_id, 
                                        texts_of_button=['Добавить новое слово',
                                        'Проверять слова!', 'Внести изменения в словарь']). \
                                        return_button()
    else: 
        i = 1
        while len(list_all_words) != 0:
            s= ''
            for b in list_all_words[0:25]:
                s = s + str(i)  + '. ' + str(b) + '\n'
                i += 1
            list_all_words = list_all_words[25:]
            telegram_api_request.ButtonCreate(message_text=s, 
                                            chat_id=chat_id, 
                                            texts_of_button=['']). \
                                            return_button()
        telegram_api_request.ButtonCreate(message_text='Это список слов.\n\nНапиши номер ' + \
            'слова, которое хочешь удалить.\n\nЕсли их несколько, то напиши через запятую ' + \
            'в таком формате: 1,2,3', 
            chat_id=chat_id, 
            texts_of_button=
            ['Добавить новое слово', 'Проверять слова!', 'Внести изменения в словарь']). \
            return_button()        

def show_all_words_for_modif(pk_of_user_in_db: int, chat_id: int):
    '''
    Foo is using on level "modificate word". Foo returns whole list of words in table 
    whole_vocab. Returning is with a frequency of 25 words. 
    
    '''    
    config_file.db_update("DELETE FROM dynamic_vocab \
                        WHERE user_id={}".
                        format(pk_of_user_in_db))
    config_file.db_update("INSERT INTO dynamic_vocab \
                        (user_id, word_in_dynamic, definition_in_dynamic, id_in_dynamic) \
                        SELECT user_id, word_in_whole, definition_of_word, id_in_whole \
                        FROM whole_vocab WHERE user_id={}".
                        format(pk_of_user_in_db))
    list_all_words = config_file.db_select("SELECT word_in_dynamic \
                                        FROM dynamic_vocab \
                                        WHERE user_id={}".
                                        format(pk_of_user_in_db))
    list_all_words = [i[0] for i in list_all_words]
    if len(list_all_words) < 1: 
        telegram_api_request.ButtonCreate(message_text=
            'Словарь пустой.\nСначала следует добавить слова.', 
            chat_id=chat_id, 
            texts_of_button=
            ['Добавить новое слово', 'Проверять слова!', 'Внести изменения в словарь', 'Удалить слова']). \
            return_button()
    else: 
        i=1
        while len(list_all_words) != 0:
            s= ''
            for b in list_all_words[0:25]:
                s = s + str(i)  + '. ' + str(b) + '\n'
                i += 1
            list_all_words = list_all_words[25:]
            telegram_api_request.ButtonCreate(message_text=s, 
                                            chat_id=chat_id, 
                                            texts_of_button=['']). \
                                            return_button()
        telegram_api_request.ButtonCreate(message_text=
                                        'Это список слов.\nНапиши номер слова, которое хочешь изменить. ' + \
                                        'Если хочешь изменить само слово, не только его дефиницию, ' + \
                                        'то напиши сразу слово. Например так:\n1. Example word', 
                                        chat_id=chat_id, 
                                        texts_of_button=['Добавить новое слово', 'Проверять слова!',
                                        'Внести изменения в словарь', 'Удалить слова']). \
                                        return_button()        

def delete_word(numbers: str, pk_of_user_in_db: int) -> str: 
    '''Foo delete row from table'''
    alpha_checking = (re.search('[^1-9, ]', numbers)) 
    if alpha_checking == None:                        # if there is no letters
        numbers = re.sub('[\s]', '', numbers)         # delete spaces
        list_for_deleting = numbers.rsplit(',')       # create list, comma is separator         
        list_for_deleting = list((int(i) for i in list_for_deleting))
        list_for_deleting.sort()
        if list_for_deleting[0] > list_for_deleting[-1]:
            list_for_deleting.reverse()
        for b in list_for_deleting:
            config_file.db_update("WITH test AS \
                                (SELECT user_id, id_in_dynamic, ROW_NUMBER() OVER() \
                                FROM dynamic_vocab WHERE user_id={}) \
                                DELETE FROM whole_vocab WHERE id_in_whole \
                                IN (SELECT id_in_dynamic \
                                FROM test WHERE row_number ={} AND user_id={})".
                                format(pk_of_user_in_db, b, pk_of_user_in_db))
        return ('Удалено! ')
    else:
        return('Пожалуйста, не используйте буквы, предпочтительно использовать такой \
            формат: \n\n 1, 2, 3')

def modificate_word(message: str, pk_of_user_in_db: int) -> str:   
    '''Foo modificate word and status of word'''
    if (re.search('[a-z]', message)) == None:       # if there is no letters in message       
        message = re.sub('[\s]', '', message)       # remove spaces   
        message = int(re.sub('[.,]', '', message))  # remove dots and commas
        try:
            config_file.db_update("WITH test AS (SELECT id_in_dynamic, ROW_NUMBER() OVER () \
                                FROM dynamic_vocab WHERE user_id={}) \
                                UPDATE dynamic_vocab SET status_of_word_in_dynamic='modif' \
                                WHERE id_in_dynamic \
                                IN (SELECT id_in_dynamic FROM test WHERE row_number={} AND user_id={})".
                                format(pk_of_user_in_db, message, pk_of_user_in_db))
            definition_of_word = 'Дефиниция у слова следующая: {}. \nНапиши теперь верную дефиницию.'. \
                                format(config_file.db_select("SELECT definition_in_dynamic \
                                                            FROM dynamic_vocab \
                                                            WHERE status_of_word_in_dynamic='modif'") \
                                                            [0][0])
            return(definition_of_word) 
        except: 
            return('Что-то пошло не так. Попробуй, пожалуйста, набрать только номер, без других символов. Возможно, в этом дело')
    else: 
        try:
            number_and_word = message.rsplit('.', 1)    # [0] is number, [1] is word
            number_and_word[0] = int(re.sub('[\s]', '', number_and_word[0]))
            config_file.db_update("WITH test AS (SELECT id_in_dynamic, ROW_NUMBER() OVER ()\
                                FROM dynamic_vocab \
                                WHERE user_id={}) \
                                UPDATE whole_vocab SET word_in_whole='{}' \
                                WHERE id_in_whole \
                                IN (SELECT id_in_dynamic \
                                FROM test WHERE row_number={} \
                                AND user_id={})".
                                format(pk_of_user_in_db, str(number_and_word[1]),
                                number_and_word[0], pk_of_user_in_db))
            config_file.db_update("WITH test AS (SELECT id_in_dynamic, ROW_NUMBER() OVER () \
                                FROM dynamic_vocab WHERE user_id={}) \
                                UPDATE dynamic_vocab SET status_of_word_in_dynamic='modif' \
                                WHERE id_in_dynamic IN (SELECT id_in_dynamic FROM test \
                                WHERE row_number={} AND user_id={})".
                                format(pk_of_user_in_db, number_and_word[0], pk_of_user_in_db))
            definition_of_word=config_file.db_select("SELECT definition_in_dynamic \
                                                    FROM dynamic_vocab \
                                                    WHERE status_of_word_in_dynamic='modif'")
            returning_message=str('Слово изменено. Дефиниция у него такая: ' + str(
                config_file.db_select("SELECT definition_in_dynamic FROM dynamic_vocab \
                                    WHERE status_of_word_in_dynamic='modif'")[0][0]) + \
                                    '\nНапиши теперь верную дефиницию для слова. \
                                    Если менять ее не надо, то можешь просто скопировать \
                                    написанную выше, либо вызвать другую команду. ')
            return(returning_message)
        except:
            return('Что-то пошло не так. Попробуй еще разок именно в формате таком: \n 1. \
                                                                                  Слово. ')

def modificate_definition(definition: str, pk_of_user_in_db: int) -> str:
    '''Foo modificate definition in row of table whole_vocab '''
    try:
        number_in_whole = config_file.db_select("WITH test as (SELECT id_in_dynamic \
                                                FROM dynamic_vocab \
                                                WHERE status_of_word_in_dynamic='modif' \
                                                AND user_id={}) \
                                                SELECT id_in_whole FROM whole_vocab \
                                                WHERE id_in_whole IN (SELECT id_in_dynamic\
                                                FROM test);".
                                                format(pk_of_user_in_db))[0][0]
        config_file.db_update("UPDATE whole_vocab SET definition_of_word='{}' \
                            WHERE id_in_whole={}".
                            format(definition, number_in_whole))
        return('Done!')
    except:
        return('Что-то пошло не так :(')