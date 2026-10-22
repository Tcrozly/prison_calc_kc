#!/usr/bin/env python3
from pathlib import Path
import re
path=Path('dist/index.html')
if not path.exists(): raise SystemExit('Missing compiled index.html')
html=path.read_text(encoding='utf-8')
for marker in ('KC_LOCAL_RATE_SALT_MARKER_83c2fae14b_V1','KC_LOCAL_RATE_IV_MARKER_83c2fae14b_V1','KC_LOCAL_RATE_CIPHERTEXT_MARKER_83c2fae14b_V1'):
    if html.count(marker)!=1:
        raise SystemExit('Expected exactly one marker in compiled output: '+marker)
for expected in ('<script','<style','data:image/jpeg;base64,','data:image/png;base64,','@font-face'):
    if expected not in html: raise SystemExit('Missing embedded offline asset: '+expected)
if re.search(r'<script\b[^>]*\bsrc\s*=',html): raise SystemExit('External JavaScript script found')
if 'fonts.googleapis.com' in html or 'fonts.gstatic.com' in html: raise SystemExit('External font reference found')
if 'kiergroup2026$' in html: raise SystemExit('Hard-coded fallback passphrase found')
out=Path('dist/Prison_Cost_Estimator_BLANK_TEMPLATE.html')
path.rename(out)
print('Verified offline blank template:',out)
