# Python code

Mainly, project consists of 2 parts:

1. Telegram bot.
2. Flask Interface. 

routes.py includes routes of Flask, telegram.py include function requests_list, that processes incoming messages in Telegram bot. Mainly by using "flag" (level) code choose functions from module operations.py and use them to construct answers for user. 

# Heroku

clock.py - for runing on schedule of POST requests to set webhook: https://core.telegram.org/bots/api#setwebhook

requirements.txt, Procfile - files for requirements of Heroku to know packages, modules, them versions, that are using in development.

# Flask Web Interface

For web interface have used simple HTML, little bit of standart CSS and Bootstrap styles: https://getbootstrap.com

## Next steps in project: 

1. To add simple math models for less random output of words. Now output is absolutely random. That's not cool, because to remember some words are more easily than others. And if you have 1000 words, than difficult words just can not to be showed in Telegram bot. 
2. Division any certain amount of words on pages. Like on one page could be maximum 100 words. Because if you have 1000 words, loading of page could be very slow. 
3. To add password recovery by email. 

## Stack of technologies: 
- SQL commands, PostgreSQL
- Telegram API
- JSON, requests
- little bit of regular expressions
- Heroku deployment
- Flask, Flask-packages, Jinja syntax
- formatting strings
- little bit of network knowledge, like WebHook, SSH for testing  
- HTML, Bootstrap, CSS
- Hashing
- OOP
- Logging
