import sys, math
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.boundsPen import BoundsPen
f=TTFont(sys.argv[1]); gs=f.getGlyphSet(); glyf=f['glyf']; hmtx=f['hmtx']
def bb(n):
    p=BoundsPen(gs); gs[n].draw(p); return p.bounds
def add(name, uni, parts, adv):
    pen=TTGlyphPen(gs)
    for g,t in parts: pen.addComponent(g,t)
    glyf[name]=pen.glyph(); hmtx[name]=(adv,0)
    for t in f['cmap'].tables:
        if t.isUnicode(): t.cmap[uni]=name
def above(base, mark, sx, sy, shear, gap, xoff=0):
    b=bb(base); m=bb(mark)
    # mark transformed: x' = sx*x + shear*y ; y' = sy*y
    mx=(sx*(m[0]+m[2])/2 + shear*(m[1]+m[3])/2)
    dx=(b[0]+b[2])/2 - mx + xoff
    dy=b[3]+gap - sy*m[1]
    return (mark,(sx,0,shear,sy,dx,dy))
names={'a':'aacute','e':'eacute','i':'iacute','o':'oacute','u':'uacute','A':'Aacute','E':'Eacute','I':'Iacute','O':'Oacute','U':'Uacute'}
unis=dict(zip('aeiouAEIOU',[0xE1,0xE9,0xED,0xF3,0xFA,0xC1,0xC9,0xCD,0xD3,0xDA]))
for ch,n in names.items():
    add(n, unis[ch], [(ch,(1,0,0,1,0,0)), above(ch,'quotesingle',1.0,0.75,0.45,40)], hmtx[ch][0])
for ch,n,u in (('n','ntilde',0xF1),('N','Ntilde',0xD1)):
    add(n,u,[(ch,(1,0,0,1,0,0)), above(ch,'hyphen',0.95,0.9,0,45)], hmtx[ch][0])
for ch,n,u in (('u','udieresis',0xFC),('U','Udieresis',0xDC)):
    add(n,u,[(ch,(1,0,0,1,0,0)), above(ch,'period',0.8,0.8,0,45,-75), above(ch,'period',0.8,0.8,0,45,75)], hmtx[ch][0])
for ch,n,u in (('question','questiondown',0xBF),('exclam','exclamdown',0xA1)):
    b=bb(ch); h=b[3]-b[1]
    add(n,u,[(ch,(-1,0,0,-1,b[0]+b[2],b[1]+b[3]-0.22*h))], hmtx[ch][0])
b=bb('period'); add('periodcentered',0xB7,[('period',(1,0,0,1,0,260))], hmtx['period'][0])
if 'DSIG' in f: del f['DSIG']
f.flavor='woff'; f.save(sys.argv[2])
