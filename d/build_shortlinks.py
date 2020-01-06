#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import qrcode
import qrcode.image.svg

os.environ['PATH'] += os.pathsep + '/home/tyler/anaconda3/bin/'
factory = factory = qrcode.image.svg.SvgPathImage


def get_redir_HTML(redir):
    html = f"""<!DOCTYPE html>
<html>
   <head>
      <title>HTML Meta Tag</title>
      <meta http-equiv = "refresh" content = "0; url = {redir}" />
   </head>
   <body>
      <p><a href="{redir}">redirect</a></p>
   </body>
</html>
"""
    return html


def gen_redir(short,redir):
    html = get_redir_HTML(redir)
    
    os.system(f'mkdir -p ./{short}')
    f = open(f'{short}/index.html', 'a')
    f.write(html)
    f.close()
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=0,
    )
    qr.add_data('chen.pw/d/'+short)
    qr.make(fit=True)
    
    img = qr.make_image(image_factory=factory)
    img.save(f"./{short}/{short}.svg")
    
    os.system(f"inkscape -D -z --file=./{short}/{short}.svg --export-pdf=./{short}/{short}.pdf")


maps = {
    'f5b':'./../research/talks/general.pdf',
    'i7g':'https://github.com/tchen01/new_cg_variants/tree/master/predict_and_recompute',
}

for key,val in maps.items():
    gen_redir(key,val)