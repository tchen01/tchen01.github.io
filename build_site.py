#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
os.environ['PATH'] += os.pathsep + '/home/tyler/anaconda3/bin/'

start_delimiter = '<body>\n'
end_delimiter = '</body>\n'


def pub_to_html(bib_file_loc,bib_file_name):
    """
    given bibtex file location, output html string.
    """
    
    bib_info = {}

    with open(bib_file_loc+bib_file_name+'.bib','r') as bib_file:
        for raw_line in bib_file:
            line = raw_line.strip()
            eq_loc = line.find('=')
            l_loc = line.find('{')
            r_loc = line.find('}')

            bib_info[line[:eq_loc].strip()] = line[l_loc+1:r_loc].replace(' and', ',')

    html = '<div class="paper">\n'\
           +f'<div class="title"><a href="./publications/{bib_file_name}.html">{bib_info["title"]}</a>.</div>\n'\
           +f'<div class="authors">{bib_info["author"].replace("Tyler Chen","<strong>Tyler Chen</strong>")}.</div>\n'\
           +(f'<div class="eprint">arXiv:<a href="https://arxiv.org/abs/{bib_info["eprint"]}">{bib_info["eprint"]}</a>.</div>\n' if "eprint" in bib_info.keys() else '')\
           +'</div>\n'
    
    return html

def talk_to_html(bib_file_loc,bib_file_name):
    """
    given bibtex file location, output html string.
    """
    
    bib_info = {}

    with open(bib_file_loc+bib_file_name+'.bib','r') as bib_file:
        for raw_line in bib_file:
            line = raw_line.strip()
            eq_loc = line.find('=')
            l_loc = line.find('{')
            r_loc = line.find('}')

            bib_info[line[:eq_loc].strip()] = line[l_loc+1:r_loc].replace(' and', ',')

    html = '<div class="paper">\n'\
           +f'<div class="title">{bib_info["title"]}</a>.</div>\n'\
           +f'<div class="authors">{bib_info["author"].replace("Tyler Chen","<strong>Tyler Chen</strong>")}.</div>\n'\
           +f'<div class="notes">{bib_info["note"]}.</div>\n'\
           +f'<div class="eprint"><a href="./talks/{bib_file_name}.pdf">[pdf]</a></div>\n'\
           +'</div>\n'
    
    return html



def build_html(folder,file_name):
    print(f'now building {folder}/{file_name}')

    # only generate pdf for articles (still may be better to just render print css well for text articles).
    if is_article(folder,file_name): 
        opts = '--pdf-engine=xelatex'
        os.system(f'pandoc {opts} -o {folder}/{file_name}.pdf {folder}/{file_name}.md')

    # convert md to html
    os.system(f'pandoc --from markdown+markdown_in_html_blocks --mathjax -o {folder}/{file_name}1.html {folder}/{file_name}.md')

    # open old html file, pandoc converted html file, and temp new file
    with open(f'{folder}/{file_name}.html','r') as old_html_file, open(f'{folder}/{file_name}1.html','r') as new_html_content, open(f'{folder}/{file_name}2.html','w+') as new_html_file:
        
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
                css_class = 'class="article"' if is_article(folder,file_name) else '' 
                new_html_file.write(f'<div id="contentContainer" {css_class} >\n')
                
                with open(f'{folder}/{file_name}.md','r') as md_file:

                    title = ''
                    authors = ''
                    md_line = md_file.readline()
                    # if using YAML header
                    if md_line[:3].find('---') != -1: 
                        
                        while True:
                            md_line = md_file.readline()
                            
                            if md_line.find('title') != -1:
                                title = md_line
                                for y in YAML_clean:
                                    title = title.replace(y,'')
                            elif md_line.find('author') != -1:
                                authors = md_line
                                for y in YAML_clean:
                                    authors = authors.replace(y,'')
                            
                            if md_line[:3].find('---') != -1:
                                break

                    # otherwise using simple title type
                    elif md_line[:1] == '%':
                        title = md_line.replace('%','')
                        authors = md_file.readline().replace('%','')

                new_html_file.write(f'<h1>{title}</h1>\n')
                new_html_file.write(f'<p class="authors">{authors}</p>\n')
                

                if file_name != 'index' and folder in ['thoughts']:
                     new_html_file.write(f'<p>A pdf version of this page can be found <a href="./{file_name}.pdf">here</a>.</p>\n')
                
                for new_line in new_html_content:

                    # if reach a citation point
                    if new_line == '<p>[bibtex]</p>\n':
                        with open(f'{folder}/{file_name}.bib','r') as bib_file:
                            new_html_file.write('<pre><code>')
                            for bib_line in bib_file:
                                new_html_file.write(bib_line)
                            new_html_file.write('</code></pre>')
                        new_line = ''

                    # if want to generate publication list
                    elif new_line[:8] == '<p>[pub:':

                        # get publication (short) name
                        pub_name = new_line[8:].split(']')[0]
                        
                        # loop over bibfiles
                        html_bib = pub_to_html(f'{folder}/publications/',pub_name)

                        new_html_file.write(html_bib)
                        new_line = ''

                    # if want to generate publication list
                    elif new_line[:9] == '<p>[talk:':

                        # get publication (short) name
                        pub_name = new_line[9:].split(']')[0]
                        
                        # loop over bibfiles
                        html_bib = talk_to_html(f'{folder}/talks/',pub_name)

                        new_html_file.write(html_bib)
                        new_line = ''

                    new_html_file.write(new_line)

                if file_name != 'index':
                    new_html_file.write(f'{footers[folder]}\n')
                elif folder in ['research','thoughts']:
                    new_html_file.write(f'{index_footer}\n')
                new_html_file.write('</div>\n')
                new_html_file.write(end_delimiter)

                line = ''
            
            new_html_file.write(line)
            
    os.system(f'rm {folder}/{file_name}1.html')
    os.system(f'mv {folder}/{file_name}2.html {folder}/{file_name}.html')

def is_article(folder,file_name):
    if folder == 'thoughts':
        if file_name != 'index':
            return True

    return False

YAML_clean = ['title', 'author',':', r'\sffamily ',r'\textbf',"'",'https','//','chen.pw','(',')','[',']','{','}']

# folders
folders = ['.', 'research','research/cg','research/publications','research/krylov','thoughts']
folders = ['research','research/publications']
footers = {'.':'', 
           'research':'<p class="footer">The rest of my research can be found <a href="./">here</a>.</p>',
           'research/cg':'<p class="footer">More about the conjugate gradient method can be found <a href="./">here</a>.</p>',
           'research/publications':'<p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>',
           'research/krylov':'<p class="footer">The rest of my research can be found <a href="../">here</a>.</p>',
           'thoughts':'<p class="footer">More writing about my opinions on academia can be found <a href="./">here</a>.</p>'}
index_footer = '<p class="footer">Return to my <a href="../">homepage</a>.</p>'

#%%
def build_cg():
    print('building CG')
    os.chdir('research/cg')
    os.system('python build_cg.py')
    os.chdir('../..')

#build_cg()


# search through files
for folder in folders:
    
    files = sorted(os.listdir(f"./{folder}"))
    html_files = list(filter(lambda f: f[-5:]=='.html' != -1, files))
    md_files = list(filter(lambda f: f[-3:]=='.md' != -1, files))
    
    for file in md_files:
        #check if we have an html file for a md file
        if file[:-3]+'.html' in html_files:
            build_html(folder,file[:-3])




