#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

start_delimiter = '<body>\n'
end_delimiter = '</body>\n'

def build_html(folder,file_name):
    print(f'now building {folder}/{file[:-3]}')

    # convert md to html
    os.system(f'pandoc --mathjax -o {folder}/{file_name}1.html {folder}/{file}')
    
    # generate updated pdf
    os.system(f'pandoc -o {folder}/{file_name}.pdf {folder}/{file}')
    
    # open old html file, pandoc converted html file, and temp new file
    with open(f'{folder}/{file_name}.html','r') as old_html_file, open(f'{folder}/{file[:-3]}1.html','r') as new_html_content, open(f'{folder}/{file_name}2.html','w+') as new_html_file:
        
        while True:
            
            # loop over original html file
            line = old_html_file.readline()
            if not line:
                break
            
            # look for start delimiter
            if line == start_delimiter:
                
                new_html_file.write(start_delimiter+'\n')
                
                # skip to end delimiter
                while old_html_file.readline() != end_delimiter:
                    pass
                
                # write new file contents from pandoc html file
                new_html_file.write('<div id="contentContainer">\n')
                
                with open(f'{folder}/{file}','r') as md_file:
                    title = md_file.readline().replace('%','')
                    authors = md_file.readline().replace('%','')

                new_html_file.write(f'<h1>{title}</h1>\n')
                new_html_file.write(f'<p class="authors">{authors}</p>\n')
                
                # idk if we want this..
                if file[:-3] != 'index' and folder not in ['research/krylov']:
                     new_html_file.write(f'<p>A pdf version of this page can be found <a href="./{file[:-3]}.pdf">here</a></p>\n')
                
                for new_line in new_html_content:
                    new_html_file.write(new_line+'\n')

                if file[:-3] != 'index':
                    new_html_file.write(f'{footers[folder]}\n')
                new_html_file.write('</div>\n')
                new_html_file.write(end_delimiter)

                line = ''
            
            new_html_file.write(line)
            
    os.system(f'rm {folder}/{file_name}1.html')
    os.system(f'mv {folder}/{file_name}2.html {folder}/{file_name}.html')

# folders
folders = ['.', 'research','research/krylov','research/pubs', 'thoughts']
footers = {'.':'', 
           'research':'<p class="footer">The rest of my research can be found <a href="./">here</a>.</p>',
           'research/krylov':'<p class="footer">More about Krylov methods can be found <a href="./">here</a>.</p>',
           'research/pubs':'<p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>',
           'thoughts':'<p class="footer">More writing about my opinions on academia can be found <a href="./">here</a>.</p>'}


# search through files
for folder in folders:
    
    files = sorted(os.listdir(f"./{folder}"))
    html_files = list(filter(lambda f: f[-5:]=='.html' != -1, files))
    md_files = list(filter(lambda f: f[-3:]=='.md' != -1, files))
    
    for file in md_files:
        #check if we have an html file for a md file
        if file[:-3]+'.html' in html_files:
            build_html(folder,file[:-3])




