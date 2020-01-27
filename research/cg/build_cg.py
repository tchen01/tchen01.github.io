#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

cg_topics = ['index','arnoldi_lanczos','cg_derivation','cg_lanczos','cg_error','finite_precision_cg','communication_hiding_variants']#,'current_research']
os.system(f"cat {' '.join([t+'.md' for t in cg_topics])} > cg.md")

with open(f'cg.md','r') as old_md_file, open(f'cg1.md','w+') as new_md_file:
    # pass first header
    for j in range(7):
        new_md_file.write(old_md_file.readline())

    new_md_file.write('# Introduction')
    while True:
        line = old_md_file.readline()
        if not line:
            break

        if line == '<!--start_pdf_comment-->\n':

            # skip to end delimiter
            while old_md_file.readline() != '<!--end_pdf_comment-->\n':
                pass
        
        elif line == '---\n':

            # skip to end delimiter
            while True:
                line = old_md_file.readline()

                if line == '...\n':
                    break

                if line[:6] == 'title:':
                    new_md_file.write('#'+line[6:])
                
                

        else:
            new_md_file.write(line)
            
os.system('mv cg1.md cg.md')

# incerase markdown level by one
#os.system(r"sed -i -e ':a;N;$!ba;s/\n#/\n/g' cg.md")

file_name = 'cg'
options = ['--from markdown-auto_identifiers',
           '--wrap=preserve',
           f'--data-dir={os.getcwd()}',
           ]

os.system(f'pandoc {" ".join(options)} -o cg.tex cg.md --template template.tex')
os.system("sed -i -e 's/.svg}/.pdf}/g' cg.tex")
os.system(f'xelatex cg.tex')

#os.system('pandoc --pdf-engine=xelatex -o cg.pdf cg.md')

individual_files = ['remez','linear_algebra_review']
for file in individual_files:
    os.system(f'pandoc --pdf-engine=xelatex -o {file}.pdf {file}.md')

#os.system('pandoc --pdf-engine=xelatex --filter pandoc-citeproc --bibliography=krylov.bib -o krylov.pdf krylov.md')
