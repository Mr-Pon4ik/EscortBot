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
        program.working_status = True
        escort_logger.debug(f'Module "{program.PROGRAM_NAME}" ready to start')
        escort_logger.debug('------------------------------------------------')
        if program.PROGRAM_NAME != 'Logging':
            possible_launch = True

escort_logger.info('')
escort_logger.info('Program start')

ssh_time_change = 0
ssh_log_last_position = 0

if (telegram_bot.check_id_status == False):
    @telegram_bot.bot.message_handler(commands=['start'])
    def welcome(message):
        telegram_bot.bot.send_message(message.chat.id, f'Hello, your chat id: {message.chat.id}'.format(message.from_user, telegram_bot.bot.get_me()))
    telegram_bot.bot.polling(none_stop=True)

telegram_bot.send_message(message= '👾Hello, it is EscortBot for your server. I was just launched ;)')

while(possible_launch):
    #***---------------SSH module-----------------***
    try:
        if ssh.working_status == True and os.path.getmtime(ssh.get_path()) != ssh_time_change:
            ssh_last_byte_line = programs.get_last_strings_from_file( path_file=ssh.get_path(), 
                                                                      quantity_strings=10)
            if ssh_last_byte_line[0][0] == -1:
                telegram_bot.send_message(message=f'⚠️ SSH error: {ssh_last_byte_line[0][1]}')
                escort_logger.error(f'SSH error: {ssh_last_byte_line[0][1]}')
                ssh_time_change = os.path.getmtime(ssh.get_path())
                continue
            else:
                ssh_time_change = os.path.getmtime(ssh.get_path())
            send_message_flag = False
            ssh_sort_line = programs.search_for_lines_by_words( byte_list_line=ssh_last_byte_line,
                                                                position_last_find=ssh_log_last_position,
                                                                turple_keyword=['sshd'],
                                                                turple_stopword=['closed'] )
            ssh_log_last_position = ssh_sort_line[0]
            for line in ssh_sort_line[1]:
                if send_message_flag == False:
                    telegram_bot.send_message(message= '‼️‼️‼️ ATTENTION, an attempt was made to connect to the server via ssh.')
                    send_message_flag = True
                if re.search('RSA', line):
                    line = line[:re.search('RSA', line).end()]
                    escort_logger.info(line)
                    telegram_bot.send_message(message= line)
                else:
                    escort_logger.info(line)
                    telegram_bot.send_message(message= line)
    except Exception as error:
        escort_logger.exception(f'Окак')
        telegram_bot.send_message(message= f'{error}')
        telegram_bot.send_message(message= f'Bot: Окак')
    
    time.sleep(1)



