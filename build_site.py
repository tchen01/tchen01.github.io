#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
os.environ['PATH'] += os.pathsep + '/home/tyler/anaconda3/bin/'

def bib_to_html(file_loc,bib_file,pub_idx):
    """
    given bibtex string, output html string.
    """
    
    # parse bib file to dictionary
    bib_info = {}
    for raw_line in bib_file.split('\n'):
        line = raw_line.strip()
        eq_loc = line.find('=')
        l_loc = line.find('{')
        r_loc = line.find('}')

        bib_info[line[:eq_loc].strip()] = line[l_loc+1:r_loc].replace(' and', ',')

    # build html
    html = '<div class="paper">\n'\
           +f'<div class="pub-idx">[{pub_idx}]</div>'\
           +f'<div class="pub-container"><div class="title"><a href="./{file_loc}.{"pdf" if file_loc[0]=="t" else "html"}">{bib_info["title"]}</a>.</div>\n'\
           +f'<div class="authors">{bib_info["author"].replace("Tyler Chen","<strong>Tyler Chen</strong>")}.</div>\n'\
           +(f'<div class="notes">{bib_info["note"]}.</div>\n' if "note" in bib_info.keys() else '')\
           +(f'<div class="eprint">arXiv:<a href="https://arxiv.org/abs/{bib_info["eprint"]}">{bib_info["eprint"]}</a>.</div>\n' if "eprint" in bib_info.keys() else '')\
           +'</div></div>\n'
    
    return html

def build_html(file_name):
    """
    generate html file from markdown
    """

    print(f'now building {file_name}')

    # convert md to html

    options = ['--from markdown-auto_identifiers',
               '--to html5',
               '--wrap=preserve',
               '--standalone ',
               '--mathjax',
               f'--data-dir={os.getcwd()}',
               f'--variable depth={"../"*file_name.count("/")}'
               ]

    os.system(f'pandoc {" ".join(options)} -o {file_name}.html {file_name}.md --template template.html')
    #os.system(f'pandoc -o {file_name}.pdf src/{file_name}.md')

def add_bibtex(file_name):
    """
    adds bibtex file to publication page
    """

    pub_data = None
    pub = 'predict_and_recompute'

    f = open(f'research/publications/{file_name}.html','r')
    html_raw = f.read()
    f.close()

    f = open(f'research/publications/{file_name}.bib','r')
    bib_raw = f.read()
    f.close()

    html_new = html_raw.replace("[bibtex]",f'<pre>{bib_raw}</pre>')

    f = open(f'research/publications/{file_name}.html','w')
    f.write(html_new)
    f.close()

def add_publications():
    """
    add publications to research page
    """
    f = open(f'research/index.html','r')
    html_raw = f.read()
    f.close()

    html_new = html_raw

    for loc,regex in [('publications',r'\[pub:(.*?)\]'),('talks',r'\[talk:(.*?)\]')]:
        pubs = re.findall(regex,html_raw)
        for k,pub in enumerate(pubs):
            f = open(f'research/{loc}/{pub}.bib','r')
            bib_raw = f.read()
            f.close()

            pub_html = bib_to_html(f'{loc}/{pub}',bib_raw,len(pubs)-k)

            html_new = html_new.replace(f'[pub:{pub}]',pub_html)
            html_new = html_new.replace(f'[talk:{pub}]',pub_html)

    f = open(f'research/index.html','w')
    f.write(html_new)
    f.close()

def build_cg():
    print('building CG')
    os.chdir('research/cg')
    os.system('python build_cg.py')
    os.chdir('../..')

pages = ['index',
         'research/index',
         'research/cg/index',
         'research/cg/arnoldi_lanczos',
         'research/cg/cg_derivation',
         'research/cg/cg_lanczos',
         'research/cg/cg_error',
         'research/cg/finite_precision_cg',
         'research/cg/communication_hiding_variants',
         'research/cg/current_research',
         'research/cg/remez',
         'research/cg/linear_algebra_review',
         'research/publications/cg_variants_convergence_rates',
         'research/publications/predict_and_recompute_cg',
         'research/computing/index',
         'research/computing/mpi4py',
         'thoughts/index',
         'thoughts/mental_health',
         'thoughts/power_structures',
         'thoughts/reproducibility',
        ]

pubs = ['cg_variants_convergence_rates','predict_and_recompute_cg']


#for page in pages:
#    build_html(page)

build_html('research/index')
for pub in pubs:
    add_bibtex(pub)

add_publications()

#build_cg()

