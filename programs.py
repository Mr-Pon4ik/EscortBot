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

import sys
import requests
import logging
import telebot
import telebot.apihelper
import os
import re

from io import BytesIO
from logging import getLevelNamesMapping
from logging.handlers import RotatingFileHandler

class Get_data():
    """ Class for get data from another class """
    list_programs = []
    
programs = Get_data()

class Default():
    """ Class for only read log file """

    PROGRAM_NAME = ''
    working_status = False
    
    def __init__(self, name= '', path_log_file= '', name_param_path= None):
        programs.list_programs.append(self)
        self.settings = {
                         str(name_param_path): path_log_file
                        }
        self.path = path_log_file
        self.name_param_path = name_param_path
        self.PROGRAM_NAME = name
    
    def get_path(self):
        return self.settings[self.name_param_path]

    def get_file(self):
        with open(self.settings[self.name_param_path], encoding='utf-8') as f:
            return f.read()
    
    def get_settings(self):
        return self.settings
    
    def ckg_settings(self):
        try: 
            with open(self.settings[self.name_param_path], encoding='utf-8') as f:
                return 'Ok'
        except FileNotFoundError:
            return 'ERROR the path to the log file is not correct'
        except Exception as error:
            return error


class Debug():
    """ Class for control debug log """
    
    PROGRAM_NAME = 'Logging'
    working_status = False
    
    def __init__(self, level= 'INFO', path= ''):
        programs.list_programs.append(self)
        self.settings = {
                         'debug_level': level,
                         'debug_path': path
                         } 
        
    def get_settings(self):
        return self.settings
    
    def ckg_settings(self):
        try:
            with open(str(self.settings['debug_path'] + 'escort.log'), 'a', encoding='utf-8') as f:
                pass
        except:
            return 'ERROR the path to the log file is not correct'
        if getLevelNamesMapping().get(self.settings['debug_level'].upper()) == None:
            return 'ERROR debug level is not correct'
        else:
            return 'Ok'
        
    def creat_custom_logger(self, name_logger="Test",
                                name_log_file="Test.log",
                                log_format=f'%(asctime)s %(levelname)s %(message)s'):
        custom_logger = logging.getLogger(str(name_logger))
        custom_StreamHandler = logging.StreamHandler()
        try: #check logger level
            custom_logger.setLevel(logging.getLevelName(self.settings['debug_level'].upper()))
        except: 
            logging.exception("Error debug_level") 
            sys.exit("Error debug_level")
        try: #check path log file
            custom_handler = logging.FileHandler(f'{self.settings['debug_path']}{name_log_file}', mode='a')
            custom_handler = RotatingFileHandler(
                                                    f'{self.settings["debug_path"]}{name_log_file}', 
                                                    maxBytes=5*1024*1024,  # 5MB
                                                    backupCount=3
                                                )
        except: 
            logging.exception("Error debug_path") 
            sys.exit("Error debug_path")
        custom_formatter= logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M')
        custom_handler.setFormatter(custom_formatter)
        custom_StreamHandler.setFormatter(custom_formatter)
        custom_logger.addHandler(custom_handler)
        custom_logger.addHandler(custom_StreamHandler)
        return custom_logger
            
        
class Nextcloud(Default):
    """ Class for control NextCloud """
    
    def __init__(self, path_log_file= '', urlAPI= None, NC_Token= None):
        super().__init__(name= 'Nextcloud', path_log_file= path_log_file, name_param_path= 'nextcloud_log_file')
        self.settings['nextcloud_url'] = urlAPI
        self.settings['nc-token'] = NC_Token
    
    def get_data(self):
        try:
            return requests.get(    
                                    self.settings['nextcloud_url'],
                                    headers={'NC-Token': self.settings['nc-token']}
                                    )
        except requests.exceptions.HTTPError as errh:
            return(self.name, ': ', errh)
        except requests.exceptions.ConnectionError as errc:
            return(self.name, ': ', errc)
        except requests.exceptions.Timeout as errt:
            return(self.name, ': ', errt)
        except requests.exceptions.RequestException as err:
            return(self.name, ': ', err) 
      
    
class SSH(Default):
    """ Class for control ssh connections """    
    
    def __init__(self, path_log_file=''):
        super().__init__(name= 'SSH', path_log_file= path_log_file, name_param_path= 'ssh_log_path')

    def get_settings(self):
        return self.settings

    
class TelegramBot():
    """Class for setting telegram bot"""

    PROGRAM_NAME = 'TelegramBot'
    working_status = False
    check_id_status = False
    bot = None

    def __init__(self, bot_token= '', chat_id= ''):
        programs.list_programs.append(self)
        self.settings = {
                         'bot_token': bot_token,
                         'chat_id': chat_id
                        }

    def get_token(self):
        return str(self.settings['bot_token'])
    
    def get_chat_id(self):
        return self.settings['chat_id']

    def get_settings(self):
        return self.settings
    
    def ckg_settings(self):
        if (self.settings['bot_token'] != ''):
            self.bot = telebot.TeleBot(token=self.settings['bot_token'])
            try:
                self.bot.get_me()
            except telebot.apihelper.ApiTelegramException:
                return 'Token error, check it for correctness'
            if (self.settings['chat_id'] != ''):
                try:
                    self.check_id_status = True
                    self.bot.send_chat_action(self.settings['chat_id'], 'typing')
                    return 'Ok'
                except telebot.apihelper.ApiTelegramException:
                    return 'Chat id error, check it for correctness'
            else:
                return 'The chat id was not found. The bot is working in chat id sending mode'
        else:
            return 'The token is not specified'
        
    def send_message(self, message=''):
        if(self.working_status == True):
            self.bot.send_message(self.settings['chat_id'], message)

def get_last_strings_from_file(path_file, quantity_strings=1):
    if quantity_strings < 1:
        return []
    lines = []
    try:
        with open(path_file, 'rb') as f:
            temp_binary_file = f.read()
    except FileNotFoundError:
        return [(-1, b'log file disappeared: FileNotFoundError')]
    except PermissionError:
        return [(-1, b'Permission denied to log')]
    binary_file = BytesIO(temp_binary_file)
    binary_file.seek(0, 2)
    cursor_end_position = binary_file.tell()
    for i in range(quantity_strings):
        while binary_file.read(1) != b'\n' and binary_file.tell() >= 2:
            binary_file.seek(-2, 1)
            if (binary_file.tell() == 0):
                break
        if (binary_file.tell() == 0):
                break
        binary_file.seek(-2, 1)
    if binary_file.tell() >= 2:
        binary_file.seek(2, 1)
    while binary_file.tell() != cursor_end_position:
        cursor_position = binary_file.tell()
        line = binary_file.readline()
        lines.append((cursor_position, line))
    return lines

def search_for_lines_by_words(byte_list_line=(), position_last_find=0, turple_keyword=[], turple_stopword=[]):
    lines = [position_last_find, []]
    for line in byte_list_line:
        if line[0] >= position_last_find:
            string_good = True
            for keyword in turple_keyword:
                if re.search(keyword, line[1].decode())==None:
                    string_good = False
                    break
            for stopword in turple_stopword:
                if re.search(stopword, line[1].decode()):
                    string_good = False
                    break
            if string_good:
                lines[1].append(line[1].decode().rstrip('\r\n'))
                lines[0] = line[0] + len(line[1])
    return lines
