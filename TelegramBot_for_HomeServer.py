#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2025 Mr_Pon4ik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import re
import os
import time

from dotenv import load_dotenv

import programs

# Load environment variables from the .env file (if present)
load_dotenv()

debug = programs.Debug()
nextcloud = programs.Nextcloud()
ssh = programs.SSH()
telegram_bot = programs.TelegramBot()

_log_format = f'%(asctime)s %(levelname)s %(message)s'

# logging.basicConfig(
#                 format=_log_format,
#                 filename='escort.log', filemode='a',
#                 datefmt='%Y-%m-%d %H:%M'
#                 ) #set base logger

with open('config.conf', encoding='utf-8') as f: #Writing parameters to classes
    for line in f:
        string = line.lstrip()
        if len(string) > 0:
            if string[0] != '#':
                for program in programs.programs.list_programs:
                    for k, v in program.get_settings().items():
                        if re.search(k, string):
                            temp_data = string[re.search(k, string).end():].strip()
                            program.get_settings()[k] = os.getenv(f'{temp_data}', temp_data)

#creating custom logger(escort)
escort_logger = debug.creat_custom_logger(log_format=_log_format, name_logger='escort', name_log_file='escort.log')
escort_logger.info("Hello, this is escort ;) \n")

#Start check
possible_launch = False
escort_logger.info('Start check \n')
for program in programs.Get_data.list_programs:
    ckg_settings_temp = program.ckg_settings()
    escort_logger.debug(f'{program.PROGRAM_NAME}: {ckg_settings_temp}')
    if ckg_settings_temp == 'Ok':
        program.working_status = 'checked'
        escort_logger.debug(f'Module "{program.PROGRAM_NAME}" ready to start')
        escort_logger.debug('------------------------------------------------')
        if program.PROGRAM_NAME != 'Logging':
            possible_launch = True

escort_logger.info('')
escort_logger.info('Program start')

if (telegram_bot.check_id_status == False):
    @telegram_bot.bot.message_handler(commands=['start'])
    def welcome(message):
        telegram_bot.bot.send_message(message.chat.id, f'Hello, your chat id: {message.chat.id}'.format(message.from_user, telegram_bot.bot.get_me()))
    telegram_bot.bot.polling(none_stop=True)

telegram_bot.send_message(message= '👾Hello, it is EscortBot for your server. I was just launched ;)')
alarm_count = 0

while(possible_launch):
    if alarm_count > 4:
        possible_launch = False
    #***---------------SSH module-----------------***
    try:
        #raise Exception('Test alarm')
        if ssh.working_status == 'checked':
            ssh.checking_log_file()
        elif ssh.working_status == 'changed':
            message = ssh.prepare_message()
        elif ssh.working_status == 'sending':
            telegram_bot.send_message(message= '‼️‼️‼️ ATTENTION, an attempt was made to connect to the server via ssh.')
            escort_logger.info(ssh.message)
            telegram_bot.send_message(message= ssh.message)
            ssh.working_status = 'checked'
        if ssh.working_status == 'error':
            error = ssh.get_error()
            escort_logger.info(message= error)
            telegram_bot.send_message(message= error)
        
    except Exception as error:
        escort_logger.exception(f'Окак')
        telegram_bot.send_message(message= f'{error}')
        telegram_bot.send_message(message= f'Bot: Окак')
        alarm_count += 1
    
    time.sleep(1)

'''
2025-11-16 19:07 INFO
2025-11-16 19:07 ERROR Окак
Traceback (most recent call last):
  File "/opt/TelegramBotEscortServer/TelegramBot_for_HomeServer.py", line 104, in <module>
    telegram_bot.send_message(message= ssh.message)
  File "/opt/TelegramBotEscortServer/programs.py", line 269, in send_message
    self.bot.send_message(self.settings['chat_id'], message)
  File "/opt/TelegramBotEscortServer/.venv/lib/python3.12/site-packages/telebot/__init__.py", line 1800, in send_message
    apihelper.send_message(
  File "/opt/TelegramBotEscortServer/.venv/lib/python3.12/site-packages/telebot/apihelper.py", line 275, in send_message
    return _make_request(token, method_url, params=payload, method='post')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/TelegramBotEscortServer/.venv/lib/python3.12/site-packages/telebot/apihelper.py", line 168, in _make_request
    json_result = _check_result(method_name, result)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/TelegramBotEscortServer/.venv/lib/python3.12/site-packages/telebot/apihelper.py", line 195, in _check_result
    raise ApiTelegramException(method_name, result, result_json)
telebot.apihelper.ApiTelegramException: A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: message text is empty
2025-11-16 19:07 INFO
2025-11-16 19:07 ERROR Окак
Traceback (most recent call last):
  File "/opt/TelegramBotEscortServer/TelegramBot_for_HomeServer.py", line 104, in <module>
    telegram_bot.send_message(message= ssh.message)
  File "/opt/TelegramBotEscortServer/programs.py", line 269, in send_message
    self.bot.send_message(self.settings['chat_id'], message)
  File "/opt/TelegramBotEscortServer/.venv/lib/python3.12/site-packages/telebot/__init__.py", line 1800, in send_message
    apihelper.send_message(
  File "/opt/TelegramBotEscortServer/.venv/lib/python3.12/site-packages/telebot/apihelper.py", line 275, in send_message
    return _make_request(token, method_url, params=payload, method='post')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/TelegramBotEscortServer/.venv/lib/python3.12/site-packages/telebot/apihelper.py", line 168, in _make_request
    json_result = _check_result(method_name, result)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/TelegramBotEscortServer/.venv/lib/python3.12/site-packages/telebot/apihelper.py", line 195, in _check_result
    raise ApiTelegramException(method_name, result, result_json)
telebot.apihelper.ApiTelegramException: A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: message text is empty

'''