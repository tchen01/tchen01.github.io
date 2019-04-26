#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

start_delimiter = '<!--start_pdf_comment-->\n'
end_delimiter = '<!--end_pdf_comment-->\n'

cg_topics = ['index','arnoldi_lanczos','cg_derivation','cg_lanczos','cg_error','finite_precision_cg','communication_hiding_variants','current_research']
os.system(f"cat {' '.join([t+'.md' for t in cg_topics])} > cg.md")

with open(f'cg.md','r') as old_md_file, open(f'cg1.md','w+') as new_md_file:
    # pass author and original title
    for j in range(2):
        new_md_file.write(old_md_file.readline())

    while True:
        line = old_md_file.readline()
        if not line:
            break
        if line == start_delimiter:

            # skip to end delimiter
            while old_md_file.readline() != end_delimiter:
                pass
            
        if line[0] == '%':
            new_md_file.write(line.replace('%','#'))
            old_md_file.readline() # skip over author
        else:
            new_md_file.write(line)
            
os.system('mv cg1.md cg.md')
os.system('pandoc --pdf-engine=xelatex -o cg.pdf cg.md')

individual_files = ['remez','linear_algebra_review']
for file in individual_files:
    os.system(f'pandoc --pdf-engine=xelatex -o {file}.pdf {file}.md')

#os.system('pandoc --pdf-engine=xelatex --filter pandoc-citeproc --bibliography=krylov.bib -o krylov.pdf krylov.md')
