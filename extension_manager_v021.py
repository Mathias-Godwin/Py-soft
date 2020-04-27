#!/usr/bin/env python
# coding: utf-8

# Author: Mathias Godwin
# Date: 25-April-2020

import os
import re
import warnings
import path

__author__ = "Mathias Godwin (godwinsaint6@gmail.com)"
__version__ = "0.2.1"
__username__ = os.environ.get('USERNAME')
__userprofile__ = os.environ.get('USERPROFILE')

# Use of this source code is governed by the MIT license.

home_drive = os.environ.get('HOMEDRIVE') + '\\'

class extension_manager:
    """
       Provides with functions to manipulate on files in a dir(s).
       ==========================================================
       ==========================================================
       --- version:: 0.2.0
       
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
    by Nmae:
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
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
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
                        of file extensions you want to work on.
                        
             dir_target_names: default empty list. The names of the targeted
                        directories ``Must be equivalent to the numbers of 
                        names_of_extensions``.
        """ 

 
        def do_the_cmd(self, dir_target_name, searched_ex):
            """
                 Work with the files and the dir(s), command-line based workflow.
            """
            for dir_target, extension_ in zip(dir_target_name, searched_ex):
                for scr in extension_:
                    try:
                        if dir_target not in set(os.listdir(self.Dir)):
                            os.chdir(self.Dir)
                            os.makedirs(dir_target, exist_ok=True)
                        if self.strategy == 'copy':
                            warnings.warn('\nabout to #copy a file to '+ self.Dir + dir_target)
                            dst = path.FastPath.copy2(scr, self.Dir + dir_target)
                        if self.strategy == 'move':
                            warnings.warn('\nabout to #move a file to '+ self.Dir + dir_target)
                            dst = path.FastPath.move(scr, self.Dir + dir_target)
                        if self.strategy == 'delete':
                            warnings.warn('\nabout to #delete a file from  '+ self.Dir + dir_target)
                            dst = path.FastPath.remove(scr)
                    except Exception as error:
                        # Warning :
                        # ---------
                        #  Every error encountered would result in truncatation of the dir
                        continue
                print(f"{len(extension_)} {dir_target} file(s) in {self.Dir}")
                
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

            do_the_cmd(self, dir_target_name = dir_target_names,
                                                             searched_ex = searched_ex)
        elif len(names_of_extensions) == len(dir_target_names):
            searched_ex = []
            for ext, name in zip(names_of_extensions, dir_target_names):
                if not isinstance(name, str):
                    warnings.warn(f"\nexpected dir names is to be a string \nyou provided '{type(ext).__name__}'")
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
                              '.js', '.jsp', '.php', '.rss', '.xhtml'],
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
            for key, value in dic_map.items():
                key = [key + '\\' + i.split('.')[1].upper() for i in value]
                extension_manager(Dir=self.Dir, 
                                 strategy=self.strategy,
                                 by_extension=self.by_extension).group_extension(self.Dir, 
                                                                                 names_of_extensions=value, 
                                                                               dir_target_names=key)

    #______ TO-DO:  (auto_manage task scheduler) _______#

