#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

start_delimiter = '<!--start_pdf_comment-->\n'
end_delimiter = '<!--end_pdf_comment-->\n'

krylov_topics = ['index','cg_derivation','cg_error','finite_precision_cg']
os.system(f"cat {' '.join([t+'.md' for t in krylov_topics])} > krylov.md")

with open(f'krylov.md','r') as old_md_file, open(f'krylov1.md','w+') as new_md_file:
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
            old_md_file.readline()
        else:
            new_md_file.write(line)
            
os.system('mv krylov1.md krylov.md')
os.system('pandoc -o krylov.pdf krylov.md')