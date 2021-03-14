import config_file
import telegram_api_request
import variables
import operations
import hash

# There are in variable message_text Indentations looks like:
# 'some text' + /
# 'some text'
#
# That's because, if to not use concatenation in Telegram Bot 
# would be just long spaces. That's not good. 

def checking_chat_id(chat_id): 
    '''
    Foo checks is there chat_id in table users or not, i.e. user is authorized 
    or not in Telegram Bot. 
    
    '''
    try:
        if True == (config_file.db_select('SELECT TRUE HAVING {} IN (SELECT telegram_id\
                                        FROM users)'.format(chat_id))[0][0]):
            return True
    except:
        return False

def modificate_level(id_in_db: int, new_level: str):
    '''Foo modificate level of user in DB'''
    config_file.db_update("UPDATE users SET user_level = '{}' WHERE id = {}".
                        format(new_level, id_in_db ))

def requests_list(message, chat_id, r_json):
    '''
    Foo takes message and chat_id from Teleram server and make an answer to user. 
    There are 4 main levels, every level means a certain step in work of Telegram Bot. 

    This foo is more like a distributor of functions, that realy have a weight, do action.  
    Also first lines of foo check authorization of user in Telegram Bot. 

    '''
    try:
        if checking_chat_id(chat_id) == False and "@" in message: 
            try:
                print(chat_id, message)
                print("UPDATE users SET telegram_id='{}', user_level='start password' \
                                    WHERE email='{}'".
                                    format(chat_id, str(message)))
                config_file.db_update("UPDATE users SET telegram_id='{}', user_level='start password' \
                                    WHERE email='{}'".
                                    format(chat_id, str(message)))                
                telegram_api_request.ButtonCreate(message_text='Теперь напиши пароль', 
                                                chat_id=chat_id, 
                                                texts_of_button=['']).return_button()
            except:
                telegram_api_request.ButtonCreate(message_text='Что-то пошло не так. напиши почту, ' + \
                                                'которую ты зарегистрировал на сайте. Именно почту.\n' + \
                                                'Если не зарегистрирован на сайте, то следуте зарегистрироваться сначала. ' + \
                                                'Ссылка на сайт: https://telegrampyvocab.herokuapp.com/registration', 
                                                chat_id=chat_id, 
                                                texts_of_button=['']).\
                                                return_button()
        elif checking_chat_id(chat_id) == False and "@" not in message: 
            telegram_api_request.ButtonCreate(message_text='Напиши почту, на которую зарегистрирован аккаунт на сайте. ' + \
                                            'Пожалуйста, не ошибись при записи :) ', 
                                            chat_id=chat_id, 
                                            texts_of_button=['']).\
                                            return_button()        
        else: 
            pk_of_user_in_db = config_file.db_select("SELECT id from users where telegram_id={}".format(chat_id))[0][0]
            message_list = ['Добавить новое слово',
                            'Удалить слова',
                            'Внести изменения в словарь',
                            'Проверять слова!'
                            ]
            if message in message_list:
                if message=='Добавить новое слово':
                    variables.Variables(message,chat_id,pk_of_user_in_db).add_word()
                elif message=='Удалить слова':
                    variables.Variables(message, chat_id, pk_of_user_in_db).delete_word()
                elif message=='Внести изменения в словарь':
                    variables.Variables(message, chat_id,pk_of_user_in_db).modif_dict()
                elif message=='Проверять слова!':
                    variables.Variables(message, chat_id, pk_of_user_in_db).check_word()
            else:
                level = config_file.db_select("SELECT user_level FROM users \
                                            WHERE telegram_id = {}".format(chat_id))[0][0]
                if level == 'start password':
                    try:
                        tg_password = hash.hashing(str(message))
                        if tg_password == config_file.db_select("SELECT user_password FROM users \
                                                                WHERE telegram_id = {}".format(chat_id))[0][0]:
                            modificate_level(pk_of_user_in_db, 'default')
                            telegram_api_request.ButtonCreate(message_text='Ты авторизован! Теперь добавь первое слово. ' + \
                                                            'Нажми кнопку.', 
                                                            chat_id=chat_id, 
                                                            texts_of_button=['Добавить новое слово']).\
                                                            return_button()
                        else: 
                            modificate_level(pk_of_user_in_db, 'default')
                            telegram_api_request.ButtonCreate(message_text='Пароль не тот :(\nПопробуй еще раз, пожалуйста. ' + \
                                                            'Напиши почту сначала. ', 
                                                            chat_id=chat_id, 
                                                            texts_of_button=['']).\
                                                            return_button()
                    except:
                        telegram_api_request.ButtonCreate(message_text='Что-то пошло не так. Посмотри внимательно свой пароль. ' + \
                                                        'Напиши снова почту', 
                                                        chat_id=chat_id, 
                                                        texts_of_button=['']).\
                                                        return_button()
                elif level == 'adding word':
                    config_file.db_update("INSERT INTO whole_vocab (word_in_whole, user_id, status_of_word_in_whole) \
                                        VALUES('{}', {}, 'doing')".
                                        format(message.rstrip()[::-1].rstrip()[::-1], pk_of_user_in_db))
                    modificate_level(pk_of_user_in_db, 'adding_definition')
                    telegram_api_request.ButtonCreate(message_text='Напиши дефиницию или перевод данного слова.', 
                                                    chat_id=chat_id, 
                                                    texts_of_button=['Добавить новое слово', 'Удалить слова', 
                                                    'Внести изменения в словарь']).\
                                                    return_button()
                elif level == 'adding_definition':
                    config_file.db_update("UPDATE whole_vocab SET definition_of_word = '{}', status_of_word_in_whole = 'not done' \
                                        WHERE user_id = {} AND status_of_word_in_whole='doing' ".
                                        format(message.rstrip()[::-1].rstrip()[::-1], pk_of_user_in_db))
                    modificate_level(pk_of_user_in_db, 'default')
                    telegram_api_request.ButtonCreate(message_text='Новое слово добавлено.', 
                                                    chat_id=chat_id, 
                                                    texts_of_button=['Добавить новое слово', 'Проверять слова!', 
                                                    'Внести изменения в словарь', 'Удалить слова'], )\
                                                    .return_button()
                elif level == 'default':
                    bul, word = operations.checking_word(message, pk_of_user_in_db)
                    if bul == True:
                        telegram_api_request.ButtonCreate(message_text='Правильно. ' + '\n\n' + operations.show_word(pk_of_user_in_db), 
                                                        chat_id=chat_id, 
                                                        texts_of_button=['Добавить новое слово', 'Внести изменения в словарь', 
                                                        'Удалить слова', 'Проверять слова!']).\
                                                        return_button()
                    else:
                        telegram_api_request.ButtonCreate(message_text='Неправильно.\nПравильно так: ' + word + '\n\n' + \
                                                        operations.show_word(pk_of_user_in_db), 
                                                        chat_id=chat_id, 
                                                        texts_of_button=['Добавить новое слово', 'Внести изменения в словарь', 
                                                        'Удалить слова', 'Проверять слова!']).\
                                                        return_button()
                elif level == 'deleting':
                    if len(config_file.db_select("SELECT * FROM whole_vocab WHERE user_id={}".format(pk_of_user_in_db))) > 0: 
                        delete_message = operations.delete_word(numbers=message,pk_of_user_in_db=pk_of_user_in_db)
                        if delete_message == 'Пожалуйста, не используйте буквы, предпочтительно использовать такой формат: \n\n 1, 2, 3':
                                telegram_api_request.ButtonCreate(message_text='Пожалуйста, не используйте буквы, ' + \
                                                                'предпочтительно использовать такой формат: \n\n 1, 2, 3', 
                                                                chat_id=chat_id, 
                                                                texts_of_button=['Добавить новое слово', 'Проверять слова!', 
                                                                'Внести изменения в словарь']).\
                                                                return_button()
                        else:
                            telegram_api_request.ButtonCreate(message_text='Удалено!', 
                                                            chat_id=chat_id, 
                                                            texts_of_button=['Добавить новое слово', 'Проверять слова!', 
                                                            'Внести изменения в словарь', 'Удалить слова']).\
                                                            return_button()
                    else:
                        telegram_api_request.ButtonCreate(message_text='Словарь в данный момент пустой.\n\nНеловко это сообщать, ' + \
                                                        'но сначала следует добавить слова прежде, чем удалять их :) ', 
                                                        chat_id=chat_id, 
                                                        texts_of_button=['Добавить новое слово', 'Проверять слова!', 
                                                        'Внести изменения в словарь', 'Удалить слова']).\
                                                        return_button()
                elif level == 'modificate word':
                    definition = operations.modificate_word(message, pk_of_user_in_db)
                    if definition == 'Что-то пошло не так. Попробуй, пожалуйста, набрать только номер, без других символов. \
                                    Возможно, в этом дело' \
                                    or definition == 'Что-то пошло не так. Попробуй еще разок именно в формате таком: \n 1. Слово. ':
                        telegram_api_request.ButtonCreate(message_text=definition, chat_id=chat_id, texts_of_button=['']).return_button()    
                    else:
                        modificate_level(pk_of_user_in_db, 'modificate definition')
                        telegram_api_request.ButtonCreate(message_text=definition, 
                                                        chat_id=chat_id, 
                                                        texts_of_button=['Добавить новое слово','Удалить слова','Проверять слова!',
                                                        'Внести изменения в словарь']).\
                                                        return_button()
                elif level == 'modificate definition':
                    result_of_operation = operations.modificate_definition(message, pk_of_user_in_db)
                    telegram_api_request.ButtonCreate(message_text=result_of_operation, 
                                                    chat_id=chat_id, 
                                                    texts_of_button=['Добавить новое слово','Удалить слова',
                                                    'Проверять слова!', 'Внести изменения в словарь']).\
                                                    return_button()
    except Exception as ex:
        config_file.db_select("SELECT user_level FROM users WHERE telegram_id={}".format(chat_id))
        telegram_api_request.ButtonCreate(message_text='Что-то пошло не так. Затруднительно сказать на каком именно этапе произошла ошибка. ' + \
                                        '\n\nПередай информаци Диме, сообщив ошибку., ошибка такая{}'.
                                        format(str(ex)), 
                                        chat_id=chat_id, 
                                        texts_of_button=['']).\
                                        return_button()