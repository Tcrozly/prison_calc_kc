#!/usr/bin/env python3
from pathlib import Path
import base64, json, re

root = Path.cwd()
if not (root/'src/App.tsx').exists():
    raise SystemExit('Run from short-rfp-style/prison-cost-app')

markers = {
    'salt':'KC_LOCAL_RATE_SALT_MARKER_83c2fae14b_V1',
    'iv':'KC_LOCAL_RATE_IV_MARKER_83c2fae14b_V1',
    'ciphertext':'KC_LOCAL_RATE_CIPHERTEXT_MARKER_83c2fae14b_V1'
}
(root/'src/encryptedRates.ts').write_text(
    '// Blank rate placeholders; private data is embedded locally after building.\n'
    + 'export const ENCRYPTED_RATES = '+json.dumps(markers)+';\n', encoding='utf-8')
app_path = root/'src/App.tsx'
app=app_path.read_text(encoding='utf-8')
app,n=re.subn(r'const SITE_IMAGES:\s*Record<number,\s*string>\s*=\s*\{.*?\};',
    'const SITE_IMAGES: Record<number, string> = OFFLINE_IMAGES;',app,flags=re.S)
if n!=1: raise SystemExit('Site image mapping not found')
app,n=re.subn(r'src="/kiergroup\.png"', 'src={OFFLINE_LOGO}',app)
if n!=1: raise SystemExit('Logo reference not found')
app_path.write_text("import { OFFLINE_IMAGES, OFFLINE_LOGO } from './offlineAssets';\n"+app,encoding='utf-8')
images=[]
for n in range(4,13):
    p=root/'public/pic'/f'Houseblocks Layout_{n}.jpg'
    if not p.exists(): raise SystemExit(f'Missing original image: {p}')
    images.append(f'  {n}: '+json.dumps('data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode('ascii')))
logo=root/'public/kiergroup.png'
if not logo.exists(): raise SystemExit('Missing Kier logo')
(root/'src/offlineAssets.ts').write_text(
    'export const OFFLINE_IMAGES: Record<number,string> = {\n'+',\n'.join(images)+'\n};\n'
    +'export const OFFLINE_LOGO = '+json.dumps('data:image/png;base64,'+base64.b64encode(logo.read_bytes()).decode('ascii'))+';\n',
    encoding='utf-8')
main=root/'src/main.tsx'
imports='\n'.join(
    f"import '@fontsource/{family}/latin-{weight}.css';"
    for family, weights in [('poppins',(400,500,600,700)),('roboto',(400,500,700))]
    for weight in weights)
main.write_text(imports+'\n'+main.read_text(encoding='utf-8'),encoding='utf-8')
index=root/'index.html'
html=index.read_text(encoding='utf-8')
html=re.sub(r'\s*<link\b[^>]*https://fonts\.googleapis\.com[^>]*>','',html)
html=re.sub(r'\s*<link\b[^>]*https://fonts\.gstatic\.com[^>]*>','',html)
fav=root/'public/favicon.svg'
if fav.exists():
    html=html.replace('href="/favicon.svg"', 'href="data:image/svg+xml;base64,'+base64.b64encode(fav.read_bytes()).decode('ascii')+'"')
index.write_text(html,encoding='utf-8')
(root/'vite.offline.config.ts').write_text(
"import { defineConfig } from 'vite';\n"
"import react from '@vitejs/plugin-react';\n"
"import { viteSingleFile } from 'vite-plugin-singlefile';\n"
"export default defineConfig({base:'./',plugins:[react(),viteSingleFile()],"
"build:{assetsInlineLimit:100000000,cssCodeSplit:false,sourcemap:false}});\n",encoding='utf-8')
print('Blank React application prepared. No cost data was provided or read.')
