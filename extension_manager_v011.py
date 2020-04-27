#!/usr/bin/env python
# coding: utf-8


# Author: Mathias Godwin
# Date: 21-April-2020
# Authenticity : under-construction

import os
import re
import warnings

__author__ = 'Mathias Godwin (godwinsaint6@gmail.com)'
__version__ = '0.1.1'

home_drive = os.environ.get('HOMEDRIVE') + '\\'
class extension_manager:
    """
       Provides with functions to manipulate on files in a dir(s).
       ==========================================================
       ==========================================================
       --- version:: 0.1.1
       
       Parameters:
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
             "False" when searching file names rather than extension.
       strategy : action to perform with the file if found
             Available: (copy, move, delete)
        Note:
        ----
            your files will never be duplicated even if it has duplicates.
            auto_manage does some pretty stuffs for you, except that it's limited 
            to some files.
        DISCLAIMER:
        -------
            You're advise to use this code only if you're comfortable about
            how it works so not to cause any sort of damages to your files.
            __I'm hoping to add more documentations as possible soon__
        New:
        ----
           Reduced windows pop up when working with the OS module.
    """
    def __init__(self, Dir=home_drive, name_or_extension=None, *, by_extension=True, strategy='copy'):
        self.Dir = Dir
        self.name_or_extension = name_or_extension
        self.by_extension = by_extension
        self.strategy = strategy.lower()
        self.en_list = []
        
    def extension_search(self):
        """
           Walks through all directories in the drive specified looking for the required
           file for management.
        """
        if self.name_or_extension is None:
            pass
        elif self.by_extension:
            for root, dirs, file in os.walk(self.Dir):
                get_files_tolist = [os.path.join(root, name) for name in file]
                for file in get_files_tolist:
                    search_ = re.search(self.name_or_extension, file)
                    if ((search_ is not None) and (file[-len(self.name_or_extension):] == self.name_or_extension)):
                        self.en_list.append(file)
        else:
            for root, dirs, files in os.walk(self.Dir):
                get_files_tolist = [os.path.join(root, name) for name in files]
                for file in get_files_tolist:
                    search_ = re.search(self.name_or_extension, file)
                    if (search_ is not None) and search_.span()[0] == (search_.span()[1] - len(self.name_or_extension)):
                        self.en_list.append(file)
        return self.en_list
    
    def group_extension(self, extensions_dir=home_drive, 
                        names_of_extensions=[], *, dir_target_names=[]):
        """
             extensions_dir: drive to perform actions on e.g 'D:\\'.
             
             names_of_extensions: default empty list. This should be list
                        of file extensions you want to work with.
                        
             dir_target_names: default empty list. The names of the targeted
                        directories. Must be equivalent to the numbers of 
                        names_of_extensions.
        """ #                 all_at_once += all_at_once

        
        def do_the_cmd(self, dir_target_name, searched_ex):
            """
                 command-line based workflow.
            """
            # command mght be too much for the commmand prompt,
            # a help function
            def help_do_the_cmd(self, dir_target, all_at_once, extension_, dr):
                
                all_at_once = all_at_once[:-8]
                if dir_target not in set(os.listdir(self.Dir)):
                    os.chdir(self.Dir)
                    os.mkdir(dir_target)
                if self.strategy == 'copy':
                    warnings.warn('\nabout to #copy a file to '+ self.Dir + dir_target)
                    os.chdir(self.Dir + dir_target)
                    os.system(f'{all_at_once}')
                if self.strategy == 'move':
                    warnings.warn('\nabout to #move a file to '+ self.Dir + dir_target)
                    os.chdir(self.Dir + dir_target)
                    os.system(f'move "{dr}"')
                if self.strategy == 'delete':
                    warnings.warn('\nabout to #delete a file from  '+ self.Dir + dir_target)
                    os.chdir(self.Dir + dir_target)
                    os.system(f'del "{dr}"')
                    
            for dir_target, extension_ in zip(dir_target_name, searched_ex):
                all_at_once = f'{self.strategy}'
                for dr in extension_:
                    all_at_once += f' "{dr}" && {self.strategy}'
                    if (all_at_once.count(self.Dir) or all_at_once.count('&&')) == 100:
                        help_do_the_cmd(self, dir_target, all_at_once, extension_, dr)
                        all_at_once = f'{self.strategy}'
                    else:
                        pass
                help_do_the_cmd(self, dir_target, all_at_once, extension_, dr)

        if extensions_dir != self.Dir:
            warnings.warn(f"\ndidn't provide directory\n***** using default: {extensions_dir} *****")
            self.Dir = extensions_dir
        if len(names_of_extensions) == 0:
            raise ValueError('you must provide dir(s) to work on')
        if not len(names_of_extensions) == len(dir_target_names):
            warnings.warn('\ntarget directory name not provided \n************ over-riding dir target names ************')
            dir_target_names = []
            searched_ex = []
            for ext in names_of_extensions:
                if ext.startswith('.'):
                    _, dir_target_n = ext.split('.')
                    dir_target_names.append(dir_target_n)
                else:
                    dir_target_names.append(ext)
        #***********************************************#
                searched_ex.append(extension_manager(self.Dir, ext, 
                                                     strategy=self.strategy, 
                                                     by_extension=self.by_extension).extension_search())
        #***********************************************#

            extension_, dir_target, Dira = do_the_cmd(self, dir_target_name = dir_target_names,
                                                             searched_ex = searched_ex)
        elif len(names_of_extensions) == len(dir_target_names):
            searched_ex = []
            for ext, name in zip(names_of_extensions, dir_target_names):
                if not isinstance(name, str):
                    warnings.warn(f"expected dir names is to be a string \nyou provided '{type(ext).__name__}'")
                    group_extension(names_of_extensions=names_of_extensions)

        #***********************************************#
                searched_ex.append(extension_manager(self.Dir, ext, 
                                                     strategy=self.strategy, 
                                                     by_extension=self.by_extension).extension_search())
        #***********************************************#
            do_the_cmd(self, dir_target_name = dir_target_names,
                                                            searched_ex = searched_ex)
        print(f'{self.strategy} completed!')
    
    def auto_manage(self):
        if self.by_extension:
            dic_map =             {
                'Documents': ['.rtf', '.doc', '.docx', '.txt'],
                'E-Books' : ['.pdf', '.epub'],
                'Music': ['.mp3'],
                'Videos': ['.mp4', '.webm', '.mkv', '.m4v', '.avi'],
                'Pictures': ['.jpg', '.jpeg', '.png', '.jfif', '.gif']
                # Coming soon !...
             }
            for key, value in dic_map.items():
                key = [key for i in range(len(value))]
                extension_manager(Dir=self.Dir, 
                                 strategy=self.strategy,
                                 by_extension=self.by_extension).group_extension(self.Dir, 
                                                                                 names_of_extensions=value, 
                                                                                 dir_target_names=key)
    #______ TO-DO:  (auto_manage task scheduler) _______#

