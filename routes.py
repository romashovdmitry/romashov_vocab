# imports from config
import config_file
from config_file import db, login_manager, app
# import from an other modules
import operations
import variables
import hash
import templates

from telegram import requests_list
from models import users, whole_vocab
from forms import register_form, login_form, word_and_definition
# imports of python packages 
from flask_login import login_user, current_user, logout_user, login_required, UserMixin
from flask import request, jsonify, redirect, url_for, render_template, flash
import json

@app.route('/dope_shit/<ex>', methods=['POST', 'GET'])
def dope_shit(ex):
    '''404 URL, nothing special'''
    return render_template('vocab_table/404_page.html', ex=ex)

@login_manager.user_loader
def load_user(user_id): # foo, that give an User ID
    '''Foo, that five an User ID, we need it for authentication'''
    return(users.query.get(int(user_id)))

@app.route('/<toke>/', methods=['POST', 'GET'])
def get_message():
    '''URL to get data(from request) from Telegram server'''
    try:
        if request.method == 'POST':
            r_json = request.get_json() 
            message = r_json['message']['text']
            chat_id = r_json['message']['chat']['id']
            config_file.logger.info("Пришло сообщение с текстом <{}> от chat_id №{}".format(message, chat_id))
            requests_list(message, chat_id, r_json)
        return ('<h1>Hello, eto bot! </h1>')
    except Exception as ex:
        config_file.ex_catcher(current_user.id, "get_message", ex)

@app.route('/registration', methods=['POST', 'GET'])
def errors():
    '''URL for registrations'''
    try:
        if current_user.is_authenticated:
            return redirect(url_for('render_table'))
        form = register_form()
        return render_template('login/registrate.html',
                            form=form,
                            my_email_error=variables.my_email_error,
                            my_password_error=variables.my_password_error)
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "errors", ex)
        return redirect(url_for('dope_shit', ex=ex))

@app.route('/tg_autentification')
@login_required
def tg_autentification():
    '''URL of page, where site propose got to Telegram Bot'''
    try:
        return render_template('login/tg_autentification.html')
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "tg_autentification", ex)
        return redirect(url_for('dope_shit', ex=ex))

@app.route("/", methods=['POST', 'GET'])
def test():
    '''
    Directly, URL don't open any page. That's intermediate URL for 
    processing data, reveived from HTML-forms
    
    '''
    try:
        variables.my_email_error[0], variables.my_password_error[0] = None, None
        if current_user.is_authenticated:
            return redirect(url_for('render_table'))
        form = register_form()
        if form.validate_on_submit():
            password= hash.hashing(register_form().password.data)
            email=register_form().email.data
            user_info_to_db = users(email=register_form().email.data, user_password=password)
            db.session.add(user_info_to_db)
            db.session.commit()
            email = users.query.filter_by(email=form.email.data).first()
            login_user(email, remember=register_form().remember.data)
            flash(f'accounted created for {register_form().email.data}')
            return redirect(url_for('tg_autentification'))
        # put errors in variables. That's not "musthave", but it's more comfortable in my case for me
        if form.email.errors:
            for error in form.email.errors:
                variables.my_email_error[0] = error
        if form.password.errors:
            for error in form.password.errors:
                variables.my_password_error[0] = error
        # have finished to put
        return redirect(url_for('errors'))
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "test", ex)
        return redirect(url_for('dope_shit', ex=ex))

@app.route('/check_registrate_form', methods=['POST', 'GET'])
@login_required
def go_to_tg():
    '''URL for verification of logging of user'''
    try:
        return render_template('login/tg_autentification.html')
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "go_to_tg", ex)
        return redirect(url_for('dope_shit', ex=ex))

@app.route('/second_login', methods=['POST', 'GET'])
def second_login():
    ''' URL for users, who are not loged in'''
    try:
        if current_user.is_authenticated:
            return redirect(url_for('render_table'))
        form = login_form()
        return render_template('login/login.html',
                            form=form,
                            my_email_error=variables.my_email_error,
                            my_password_error=variables.my_password_error)
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "second_login", ex)
        return redirect(url_for('dope_shit', ex=ex))

@app.route('/login', methods=['POST', 'GET'])
def login():
    '''URL where user is logging in'''
    try:
        variables.my_email_error[0], variables.my_password_error[0] = None, None
        if current_user.is_authenticated:
            return redirect(url_for('render_table'))
        form = login_form()
        if form.validate_on_submit():
            email = users.query.filter_by(email=form.email.data).first()
            if email:
                if email.user_password == hash.hashing(form.password.data):
                    login_user(email, remember=form.remember.data)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('render_table'))
                else:
                    variables.my_password_error[0] = "There's a mistake in password. Please check that."
            else:
                variables.my_email_error[0] = "There's a mistake in email. Please check that."
        return redirect(url_for('second_login'))
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "login", ex)
        return redirect(url_for('dope_shit', ex=ex))

@app.route('/logout')
def logout():
    '''URL for logging out user'''
    try:
        logout_user()
        return redirect(url_for('login'))
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "logout", ex)
        return redirect(url_for('dope_shit', ex=ex))

@app.route('/table', methods=['POST', 'GET'])
@login_required
def render_table():
    '''URL for page with list of words and definitions from vocab'''
    try: 
        if request.method == 'POST':
            word = request.form.get('word')
            definition = request.form.get('definition')       
            new_word = whole_vocab(word_in_whole=word, definition_of_word=definition, user_id=current_user.id)
            db.session.add(new_word)
            db.session.commit()
            flash('Слово {} было добавлено в словарь'.format(word))
            word, definition = None, None
            return redirect(url_for('render_table'))
        try:
            words = db.session.query(whole_vocab).filter_by(user_id=current_user.id).all()
            return render_template('vocab_table/vocab.html', words=words)
        except:
            return render_template('vocab_table/first_word.html')
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "render_table", ex)
        return redirect(url_for('dope_shit', ex=ex))

@app.route('/intermediate/<id>', methods=['POST', 'GET'])
def intermediate(id):
    '''Intermediate level, where words and definition are modificating'''
    try:
        word = request.form.get('word')
        definition = request.form.get('definition') 
        past_word = db.session.query(whole_vocab).filter_by(id_in_whole=id).first().word_in_whole
        db.session.query(whole_vocab).get(id).word_in_whole = word
        db.session.query(whole_vocab).get(id).definition_of_word = definition
        db.session.commit()
        flash('Слово {} было изменено!'.format(past_word))
        word, definition = None, None
        return redirect(url_for('render_table'))
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "remove_from_table", ex)
        return redirect(url_for('dope_shit', ex=ex))

@app.route('/modificate/<word>/<id>/<definition>', methods=['POST', 'GET'])
def modificateWordInTable(word, id, definition):
    '''URL for page, Where user modificate word and/or definition'''
    try:
        return render_template('vocab_table/modificate_form.html', word=word, id=id, definition=definition)
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "remove_from_table", ex)
        return redirect(url_for('dope_shit', ex=ex))

@app.route('/remove/<id>', methods=['POST', 'GET'])
def remove_from_table(id):
    try:
        '''URL for deleting words from vocabulary(table)'''
        removed_word = db.session.query(whole_vocab).filter_by(id_in_whole=id).first().word_in_whole
        db.session.delete(whole_vocab.query.get(id))
        db.session.commit()
        flash('Слово {} было удалено!'.format(removed_word))
        word, definition = None, None
        return redirect(url_for('render_table'))   
    except Exception as ex:     
        config_file.ex_catcher(current_user.id, "remove_from_table", ex)
        return redirect(url_for('dope_shit', ex=ex))