#!/usr/bin/env python
# coding: utf-8



# Author: Mathias Godwin
# Date: 25-April-2020

import os
import re
import path
import shlex
import curses
import warnings
import fastcache
import subprocess
from fastcache import lru_cache, clru_cache

__author__ = "Mathias Godwin (godwinsaint6@gmail.com)"
__version__ = "0.2.2"
__username__ = os.environ.get('USERNAME')
__userprofile__ = os.environ.get('USERPROFILE')



# Use of this source code is governed by the GNU license.

home_drive = os.environ.get('HOMEDRIVE') + '\\'


class extension_manager(object):
    """
       Provides with functions to manipulate on files in a dir(s).
       ==========================================================
       ==========================================================
       --- version:: ...
       
       Paramaters:
       ----------
       Dir : directory (of folders) to a file extension or file name.
       Example:
       -------
             "C:\\" or "C:\\Gwin\\"
       name_or_extension : name or extension of file to work with.
              name:
              ----
              When provided with name, set "by_extension to False".
              The function would lookup or
              search for whatever matches that name in the Directory
              and all sub-directories.
              extension:
              ---------
              When provided with extension, set "by_extension to "True".
              It then perform same logic as above.   
       Example:
       --------
              name:
                   'python', 'music', 'text', ..etc
              extension:
                   '.html', '.mp3', '.mp4', ..etc
       by_extension: bool, default True
             * "False" when searching file names rather than extension.
       strategy : action to perform with the file if found
            * Available: (copy, move, delete)
        Note:
        ----
            * your files will never be duplicated even if it has duplicates.
            * auto_manage does some pretty stuffs for you, except that it's limited 
              to some files.
        DISCLAIMER: 
        -------
            * You're advise to use this code only if you're comfortable about
              how it works so not to cause any sort of damages to your files.
        New:
        ----
            * No command prompt poping up anymore.
            * ``auto_manage()`` got some new files to work on.
            
            
    Example:
    by Name:
    >>> # get the dir(s) of files having the name ```python``` on them in drive 'C:\'.
    >>> python_related = extension_manager('C:\\', name_or_extension='python', by_extension=False)
    >>> # use the extension search method
    >>> python_related.extension_search() # return a list of dir(s)
    ////////////////////////////////////////////////////
    
    by Extension:
    >>> # get the dir(s) of every ```.py``` files in drive 'C:\'.
    >>> python_files = extension_manager('C:\\', name_or_extension='.py', by_extension=True)
    >>> # use the extension search method
    >>> python_files.extension_search() # return a list of dir(s)
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
    """
#     curses.filter()
    screen = curses.initscr()
    screen.addstr(
        'Filehack Version [1.0.0] Copyright (C) 2020 Mathias Godwin. \nType "help", "copyright", "credits" for more information.\n')
    text_miner = ''
    def __init__(self, Dir=home_drive, *, by_extension=True, strategy='copy'):
        self.Dir = Dir
        self.by_extension = by_extension
        self.strategy = strategy.lower()
        self.en_list = []
        self.all_keywords = ['search', 'copy', 'move', 'delete', 'quit', 'exit', 'help', 'license', 'credits', 'copyright', 'from', 'to', 'me', 'cmd']
        self.curses = curses
        self.ch_texter = None
        self.screen.scrollok(True)
        self.__inputs__ = ['']
        self.screen.idlok(1)
        self.dic_map = {
                'Documents': ['.rtf', '.doc', '.docx', '.txt', '.log', 
                              '.msg', '.odt', '.pages', '.tex', '.wpd', '.wps'],
                'E-Books' : ['.pdf', '.epub'],
                'Music': ['.mp3', '.aif', '.iff', '.m3u', '.m4a', 
                          '.mid', '.mpa', '.wav', '.wma'],
                'Videos': ['.mp4', '.webm', '.mkv', '.m4v', '.avi', 
                           '.3g2', '.3gp', '.asf', '.flv', '.m4v', '.mpg', '.rm', '.srt', '.wmv'],
                '3D Images': ['.3dm', '.3ds','.max', '.obj'],
                'Pictures': ['.jpg', '.jpeg', '.png', '.jfif', '.gif',
                             '.bmp', '.dds', '.tif', '.tiff', '.thm', 
                             '.pspimage', '.psd', '.heic', '.yuv', '.ai', 
                             '.svg', '.eps'],
                
                'Spreadsheet Files': ['.xlr', '.xls', '.xlsx'],
                'Database Files': ['.accdb', '.db', '.dbf', '.mdb', 
                                   '.pdb', '.sql'],
                'Executable Files': ['.exe', '.bat', '.cgi', '.apk', 
                                     '.app', '.com', '.gadget', '.jar', '.wsf'],
                'Web Files': ['.html', '.htm', '.asp', '.aspx', 
                              '.cer', '.cfm', '.csr', '.css', '.dcr', 
                              '.js', '.jsp', '.php', '.rss', '.xhtml', '.xml'],
                'Plugin Files': ['.crx', '.plugin'],
                
                'Font Files': ['.fnt', '.fon', '.otf', '.ttf'],
                'Compressed Files': ['.7z', '.cbr', '.deb', '.gz', '.pkg',
                                     '.rar', '.rpm', '.sitx', '.tar.gz', '.zip',
                                    '.zipx'],
                'Developer Files': ['.py', '.c', '.class', '.cpp', '.cs', 
                                    '.dtd', '.fla', '.h', '.java', '.lua', 
                                    '.m', '.pl', '.sh', '.swift', '.vb', 
                                    '.vcxproj', '.xcodeproj'],
                'Misc Files': ['.crdownload', '.ics', '.msi', '.part', '.torrent']
                # Coming soon !...
             }
#         self.curses.filter()
        self.screen.keypad(True)
        
    def _get_text(self):
        try:
            self.screen.timeout(-1)
            self.screen.refresh()
            text_ch = self.screen.getch()
        except Exception as error:
            print('INPUT ERROR:\n', error)
#             continue
        return  text_ch

    def __stdin__(self):
        self.curses.start_color()
        self.curses.init_pair(1, self.curses.COLOR_CYAN, self.curses.COLOR_BLACK)
        self.screen.addstr('[In :] ', self.curses.color_pair(1))
        self.screen.idlok(1)
        self.screen.refresh()
        
    def __stdout__(self, text):
        try:
            
            if type(text).__name__ == 'tuple':
                text = [lis for sublis in [*text] for lis in sublis]
            if type(text).__name__ == 'list':
                for i in text:
                    self.screen.addstr(f'[Out:] {i}\n')
#                     self.screen.addstr('\n')
                self.screen.addstr(f'{len(text)} Total {self.text_miner.strip()} Found \n')
            else:
                self.screen.addstr(f'[Out:] {text}\n')
        except Exception as error:
            print(error)
        finally:
            self.screen.refresh()        
            text = ''
    def _stop(self, x, y, g_sign=True):
        if g_sign:
            if self.curses.getsyx()[1] >= x:
                    self.curses.beep()
#                     self.text_miner = ''
                    self.screen.move(self.curses.getsyx()[0], x)
                    self.screen.refresh()
        else:
            if self.curses.getsyx()[1] <= x:
#                 self.curses.beep()
                    self.text_miner = ''
                    self.screen.move(curses.getsyx()[0], x)
                    self.screen.refresh()
            
    def is_keyword(self, text):
        if text in self.all_keywords:
            return True
        return False

    def destroy(self):
        if self.text_miner == 'quit\n' or self.text_miner == 'exit\n':
            self.curses.nocbreak()
            self.screen.keypad(False)
            self.curses.echo()
            self.curses.endwin()
            
            import os as __os
            p_id = __os.getpid()
            __os.kill(p_id, 1)
                
            
    def key_backspace(self):
        if self.ch_texter == self.curses.KEY_BACKSPACE or self. ch_texter == 127 or self.ch_texter == 8:
            self.screen.refresh()
            self.screen.clrtoeol()
            self.screen.move(self.curses.getsyx()[0], self.curses.getsyx()[1])
            self.screen.refresh()
            self.screen.addstr('')
#             self.screen.move(self.curses.getsyx()[0], self.curses.getsyx()[1]+1)
            if self.curses.getsyx()[1] <= 7:
                self._stop(7, 0, False)
            elif self.curses.getsyx()[1] != 7:
                pass
                
    def key_enter(self, text):
#         self.___stdin__s__.append(text)
        self.__stdout__(text)
        self.text_miner = ''
        self.__stdin__()
        
    def key_scrollup(self):
#         if False:
#             self.screen.scroll(1)
#             self.screen.refresh()
        i = 0
        if False:
            i += 1
            self.__stdout__(self.__inputs__[:-i])
            self.__stdin__()
#         i = 0
    def key_scrolldown(self):
        if False:
            self.screen.scroll(-1)
            self.screen.refresh()
        
    def _make_search(self, text):
        return text.split('search')[1]
    
    def _mine_text(self):
        self.ch_texter = self._get_text()
        ch_text = chr(self.ch_texter)
        self.text_miner += ch_text
        self.screen.refresh()
        
        if self.text_miner == 'quit\n' or self.text_miner == 'exit\n':
            self.destroy()
        if self.is_keyword(self.text_miner):
            curses.init_pair(2, self.curses.COLOR_GREEN, self.curses.COLOR_BLACK)
            self.screen.addstr(self.curses.getsyx()[0], self.curses.getsyx()[1]-len(self.text_miner),
                                   self.text_miner, self.curses.color_pair(2))
                
        if self.ch_texter in [self.curses.KEY_BACKSPACE, 127, 8]:
            self.key_backspace()
        if self.ch_texter in [ord('ă'), self.curses.KEY_SF]:
            self.key_scrollup()
        if self.ch_texter in [ord('Ă'), self.curses.KEY_SR]:
            self.key_scrollup()
        if self.ch_texter in [ord("ą"), self.curses.KEY_RIGHT]:
            self.screen.move(curses.getsyx()[0], self.curses.getsyx()[1]+1)
            if self.curses.getsyx()[1] >= 100:
                self._stop(100, 0, True)
        if self.ch_texter in [ord("Ą"), self.curses.KEY_LEFT]:
            self.screen.move(curses.getsyx()[0], self.curses.getsyx()[1]-1)
            if self.curses.getsyx()[1] <= 7:
                self._stop(7, 0, False)
    @lru_cache(maxsize=1000, typed=False)   
    def extension_search(self, name_or_extension):
        """
           Walks through all directories in the drive specified looking for the required
           file for management.
        """

        name_or_extension = name_or_extension.strip()
        if name_or_extension == '':
            print('top', name_or_extension)
            pass
        
        elif self.by_extension:
            for root, dirs, file in os.walk(self.Dir):
                get_files_tolist = [os.path.join(root, name) for name in file]
                for file in get_files_tolist:
                    search_ = re.search(name_or_extension, file)
                    if ((search_ is not None) and (file[-len(name_or_extension):] == name_or_extension)):
                        self.en_list.append(file)
                    
        else:
            for root, dirs, files in os.walk(self.Dir):
                get_files_tolist = [os.path.join(root, name) for name in files]
                for file in get_files_tolist:
                    search_ = re.search(name_or_extension.strip(), file)
                    if (search_ is not None) and search_.span()[0] == (search_.span()[1] - len(name_or_extension)):
                        self.en_list.append(file)

        return self.en_list
    #, extension_manager.extension_search
#     cmd, host_drive, names_of_extensions=[file], fname=file, dir_target_names=[guest_drive]
    def group_extension(self, cmd, extensions_dir=home_drive, 
                        names_of_extensions=[], fname=None, *, dir_target_names=[]):
        """
             extensions_dir: drive to perform actions on e.g 'D:\\'.
             
             names_of_extensions: default empty list. This should be list
                        of file extensions you want to work on.
                        
             dir_target_names: default empty list. The names of the targeted
                        directories ``Must be equivalent to the numbers of 
                        names_of_extensions``.extension_manager('E:\\').
        """ 
        host_drive = extensions_dir
        guest_drive = dir_target_names
        
#         @lru_cache(maxsize=1000, typed=False) 
        def do_the_cmd(self, dir_target_name, searched_ex, strategy):
            """
                 Work with the files and the dir(s), command-line based workflow.
            """
            self.strategy = strategy.strip()
            for dir_target, extension_ in zip(dir_target_name, searched_ex):
                for scr in extension_:
                    try:
#                         if self.strategy not in ['delete']: # " Needs `subprocessing` "
# #                             print('Not delete')
#                             for key, lis in self.dic_map.items():
# #                                 print('key', key, 'value', lis)
#                                 for value in lis:
#                                     print(value)
#                                     if fname.strip() == value:
#                                         keyn = key
#                                     else:
#                                         keyn = "Misc Files"
#                                 if keyn or fname.strip() not in list(os.listdir(guest_drive)):
#                                     print('Not in dir')
#                                     os.chdir(guest_drive)
#                                     os.mkdir(key)
#                                     dir_target = key
#                                     break
# 

                         
                        if self.strategy == 'delete':
                            pass
                        else:
                            try:
                                key = 'Misc Files'
                                if dir_target not in set(os.listdir(guest_drive)):
                                    print('already in dir')
                                    os.chdir(guest_drive)
                                    os.mkdir(key)
                                    dir_target = key
                                else:
                                    dir_target = key
                                    
                            except Exception as error:
                                self.__stdout__(f'{error}')

                        if self.strategy == 'copy':
                            warnings.warn('\nabout to #copy a file to '+ guest_drive)
                            dst = path.FastPath.copy2(scr, f'{guest_drive}\\{dir_target}')
                            self.__stdout__(f'{dst}')
                        if self.strategy == 'move':
                            warnings.warn('\nabout to #move a file to '+ guest_drive) # delete .csr from E:\
                            dst = path.FastPath.move(scr, f'{guest_drive}\\{dir_target}')
                            self.__stdout__(f'{dst}')
                        elif self.strategy == 'delete':
                            warnings.warn('\nabout to #delete a file from  '+ host_drive)
                            dst = path.FastPath.remove(scr)
                            self.__stdout__(f'{dst}')
                        else:
                            self.__stdout__(f'ERROR:: ')
                    except Exception as error:
                        self.__stdout__(f'{error}')
                        print('COMMAND ERROR:\n', error)
                        # Warning :
                        # ---------
                        #  Every error encountered would result in truncatation of the dir
                        continue
                self.__stdout__(f"{len(extension_)} {dir_target} file(s) in {host_drive}")
                

        if len(names_of_extensions) == 0:
            raise ValueError('you must provide dir(s) to work on')
        if True:
            dir_target_names = []
            searched_ex = []
            for ext in names_of_extensions:
                ext = ext.strip()
                if ext.startswith('.'):
                    by_extension = True
                    _, dir_target_n = ext.split('.')
                    dir_target_names.append(dir_target_n)
                else:
                    by_extension = False
                    dir_target_names.append(ext)
        #***********************************************#
                searched_ex.append(extension_manager(Dir=host_drive, 
                                                     strategy=cmd, 
                                                     by_extension= by_extension).extension_search(fname))
        #***********************************************#

            do_the_cmd(self, dir_target_name = dir_target_names,
                                                             searched_ex = searched_ex, strategy = cmd )
        print(f'{self.strategy} completed!')
    
        
    @clru_cache(maxsize=1000, typed=False)
    def auto_manage(self):
        if self.by_extension:
            for key, value in self.dic_map.items():
                key = [key + '\\' + i.split('.')[1].upper() for i in value]
                extension_manager(Dir=self.Dir, 
                                 strategy=self.strategy,
                                 by_extension=self.by_extension).group_extension(self.Dir, 
                                                                                 names_of_extensions=value, 
                                                                               dir_target_names=key)
    def main(self):
        while 1:
            _ = self._mine_text()
            if self.curses.getsyx()[1] >= 100 or len(self.text_miner) >= 100:
                self._stop(100, 0, True)
            if self.ch_texter == ord('\n'):
                self.__inputs__.append(self.text_miner)
                if self.text_miner.startswith('search '):
                    shell_l = shlex.shlex(self.text_miner)
                    shell_l.whitespace_split = True
                    to_list = list(shell_l)
                    if len(to_list) != 3:
                        self.key_enter(f'syntax error::\n\t "|{to_list}|"\n try:\n\t search .<extension name> <source drive>  \n\t OR \n\t search filename <source drive>')
                    else:
                        try:
                            cmd, file, host_drive = to_list
                            if file.strip().startswith('.'):
                                output = extension_manager(Dir=host_drive, by_extension=True).extension_search(file)
                                self.key_enter(output)
                            else:
                                output = extension_manager(Dir=host_drive, by_extension=False).extension_search(file)
                                self.key_enter(output)
                        except Exception as error:
                            print('SEARCH ERROR:\n', error)
                    
                elif self.text_miner.startswith('copy '):
                    shell_l = shlex.shlex(self.text_miner)
                    shell_l.whitespace_split = True
                    to_list = list(shell_l)
                    if len(to_list) != 6:
                        self.key_enter(f'syntax error::\n\t "|{to_list}|"\n try:\n\t copy .<extenion name> from <source drive> to <destination drive> \n\t OR \n\t copy filename from <source drive> to <destination drive>')
                    else:
                        try:
                            cmd, file, direct_from, host_drive, direct_to, guest_drive = to_list
                            print(cmd, file, direct_from, host_drive, direct_to, guest_drive)
                            self.group_extension(cmd, extensions_dir=host_drive, names_of_extensions=[file],
                                             fname=file, dir_target_names=guest_drive)
                            self.key_enter('Copy completed')
                        except Exception as error:
                            print('COPY ERROR:\n', error)
                        
                elif self.text_miner.startswith('move '):
                    shell_l = shlex.shlex(self.text_miner)
                    shell_l.whitespace_split = True
                    to_list = list(shell_l)
                    if len(to_list) != 6:
                        self.curses.beep()
                        self.curses.flash()
                        self.key_enter(f'syntax error::\n\t "|{to_list}|"\n try:\n\t move .<extenion> from <source drive> to <destination drive> \n\t OR \n\t move filename from <source drive> to <destination drive>')
                    else:
                        try:
                            cmd, file, direct_from, host_drive, direct_to, guest_drive = to_list
                            self.group_extension(cmd, extensions_dir=host_drive, names_of_extensions=[file],
                                             fname=file, dir_target_names=guest_drive)
                            self.key_enter('Move completed\n')
                        except Exception as error:
                            print('MOVE ERROR:\n', error)
                        
                elif self.text_miner.startswith('delete '):
                    shell_l = shlex.shlex(self.text_miner)
                    shell_l.whitespace_split = True
                    to_list = list(shell_l)
                    if len(to_list) != 4:
                        self.key_enter(f'syntax error::\n\t "|{to_list}|"\n try:\n\t delete .<extenion> from <source drive> \n\t OR \n\t delete filename from <source drive>')
                    else:
                        try:
                            cmd, file, direct_from , host_drive = to_list
                            self.group_extension(cmd, extensions_dir=host_drive, names_of_extensions=[file], fname=file)
                            self.key_enter('delete complete')
                        except Exception as error:
                            print('DELETE ERROR:\n', error)
                elif self.text_miner.startswith('cmd'):
                    self.__stdout__("About to open command prompt...")
                    self.curses.napms(2000)
                    self.curses.endwin()
                    
                    if os.name == 'nt':
                         shell = 'cmd.exe'
                    else:
                         shell = 'sh'
                    subprocess.call(shell)                    
                    self.screen.refresh()
                    self.curses.napms(2000)
                    self.key_enter('Finally back !')


                elif self.text_miner.startswith('help'):
                    self.key_enter('\t /*========== Please contact the developer ===========*/\n\t Email: godwinsaint6@gmail.com \n\t Cell: +234 7061 0096 72')
            
                elif self.text_miner.startswith('copyright'):
                    self.key_enter(
                        "\t\t/*========== Copyright (C) 2020 Mathias Godwin ==========*/\n\t This program is free software: you can redistribute it and/or modify it\n under the terms of the GNU General Public License as published by the Free Software Foundation,\n either version 3 of the License or any later version. This program is distributed in the hope that it will be useful,\n but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program.\n If not, see <http://www.gnu.org/licenses/>.")
                    
                elif self.text_miner.startswith('credits'):
                    self.key_enter('\t\t/*========== Credits ==========*/\nThanks to the team builders of python and all the awesome "liberaries" and "packages".\nSpecial thanks to all my "Friends" and "Family" for their supports and encouragements.\nFinal thanks to you for using it.')
                elif self.text_miner.startswith('me'):
                    homes = ['USERNAME', 'COMPUTERNAME', 'HOMEDRIVE', 'HOMEPATH', 
                             'USERDOMAIN', 'SYSTEMDRIVE', 'USERPROFILE', 'SESSIONNAME', 
                             'OS', 'PUBLIC', 'TEMP', 'PATHEXT', 
                             'PROCESSOR_ARCHITECTURE', 'WINDIR', 'NUMBER_OF_PROCESSORS', 'PSMODULEPATH']
                    for en in homes:
                        self.__stdout__(f'{en}: {os.getenv(en)}')
                    self.__stdout__(f'FILEHACK_PID: {os.getpid()}')
                    self.key_enter(f'FILEHACK_PATH: {None}')
#                 elif self.text_miner.startswith(''):
#                     self.key_enter(self.text_miner)
                else:
                    self.curses.flash()
                    self.key_enter(f'"{self.text_miner.strip()}" is an invalid command !, try again.')
#                     print(type(self.text_miner).__name__)
#                 else:
#                     self.key_enter(self.text_miner)
#             print(self.__inputs__)
        
#______ TO-DO:  (auto_manage task scheduler) _______# copy .csr from C:\ to E:\
#_____ TO-DO: (a logger for every activity) ________#

extension_manager().__stdin__()
extension_manager().main()


