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
    
    os.makedirs(f'./{short}',exist_ok=True)
    f = open(f'{short}/index.html', 'w')
    f.write(html)
    f.close()
 
    if os.path.exists(f'{short}'):
        return 
   
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
<<<<<<< HEAD
#    '2mn':'../../misc/thesis_proposal.pdf',
#    'f5b':'../../misc/thesis_proposal_slides.pdf',
#    'i7g':'https://github.com/tchen01/new_cg_variants/tree/master/predict_and_recompute',
#    'x13':'../../research/cg/cg.pdf',
#    'k5k':'../../misc/grfp_proposal.pdf',
#    '2v6':'../../misc/grfp_personal.pdf',
    'f91':'https://arxiv.org/abs/1905.01549',
    '0ak':'../../research/talks/predict_and_recompute_PP20.pdf',
=======
    '2mn':'../../misc/thesis_proposal.pdf',
    'f5b':'../../misc/thesis_proposal_slides.pdf',
    'i7g':'https://github.com/tchen01/new_cg_variants/tree/master/predict_and_recompute',
    'x13':'../../research/cg/cg.pdf',
    'k5k':'../../misc/grfp_proposal.pdf',
    '2v6':'../../misc/grfp_personal.pdf',
>>>>>>> ec6f9d63dbb9f1dbfefe096cb625f88d0e29ea7c
}

for key,val in maps.items():
    gen_redir(key,val)
