#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
os.environ['PATH'] += os.pathsep + '/home/tyler/anaconda3/bin/'


def build_html(file_name):
    """
    generate html file from markdown
    """

    print(f'now building {file_name}')

    # convert md to html

    options = ['--from markdown+tex_math_single_backslash-auto_identifiers',
               '--to html5',
               '--wrap=preserve',
               '--standalone ',
               '--mathjax',
               f'--data-dir={os.getcwd()}',
               f'--variable depth={"../"*file_name.count("/")}'
               ]

    os.system(f'pandoc {" ".join(options)} -o {file_name}.html {file_name}.md --template template.html')
    #os.system(f'pandoc -o {file_name}.pdf src/{file_name}.md')

build_html('index')


