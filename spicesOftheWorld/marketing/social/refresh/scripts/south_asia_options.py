import math, random, cairosvg
DARK='#5a1a0c'; CREAM='#fbe3c0'; ORANGE='#e8741c'; GOLD='#f4a53a'
def frame(inner):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000">
<defs><clipPath id="c"><circle cx="500" cy="500" r="452"/></clipPath></defs>
<circle cx="500" cy="500" r="470" fill="{CREAM}"/><circle cx="500" cy="500" r="455" fill="{DARK}"/>
<g clip-path="url(#c)">{inner}</g></svg>'''
def save(name,inner):
    s=frame(inner); open(name+'.svg','w').write(s)
    cairosvg.svg2png(bytestring=s.encode(),write_to=name+'.png',output_width=1000)
random.seed(4)
# ---------- 1. Masala dabba
def bowl(cx,cy,r,col,speck,kind='dots'):
    s=f'<circle cx="{cx}" cy="{cy}" r="{r+10}" fill="#d9c9b0" stroke="{DARK}" stroke-width="5"/>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>'
    n=int(r*1.4)
    for _ in range(n):
        a=random.uniform(0,6.283); d=r*math.sqrt(random.random())*0.9
        x=cx+d*math.cos(a); y=cy+d*math.sin(a)
        if kind=='dots': s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(2.5,5):.1f}" fill="{speck}"/>'
        elif kind=='seeds': s+=f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="7" ry="3" transform="rotate({random.randint(0,180)} {x:.1f} {y:.1f})" fill="{speck}"/>'
        elif kind=='flakes': s+=f'<path d="M{x:.1f},{y:.1f} l{random.uniform(-9,9):.1f},{random.uniform(-9,9):.1f} l{random.uniform(-9,9):.1f},{random.uniform(-9,9):.1f}z" fill="{speck}"/>'
    return s
d=f'<circle cx="500" cy="500" r="370" fill="#e9dcc6" stroke="{CREAM}" stroke-width="10"/>'
d+=f'<circle cx="500" cy="500" r="345" fill="none" stroke="#c9b79c" stroke-width="4"/>'
spices=[('#f2b705','#d98e04','dots'),('#c0321a','#7d1508','flakes'),('#8a4a1f','#5e2e10','seeds'),
        ('#a7a05a','#6f6a2f','dots'),('#3a2418','#16100b','dots'),('#e8741c','#b04c0c','flakes')]
for i,(c1,c2,k) in enumerate(spices):
    a=math.radians(90+60*i); d+=bowl(500+215*math.cos(a),500-215*math.sin(a),92,c1,c2,k)
# centre: dried chillies
d+=f'<circle cx="500" cy="500" r="102" fill="#d9c9b0" stroke="{DARK}" stroke-width="5"/><circle cx="500" cy="500" r="92" fill="#7d1508"/>'
for i in range(7):
    a=i*51; d+=f'<g transform="translate(500,500) rotate({a})"><path d="M0,-8 C30,-22 70,-12 80,4 C60,10 25,14 0,8 Z" fill="#c0321a" stroke="{DARK}" stroke-width="3"/><path d="M0,0 l-14,-4" stroke="#6f6a2f" stroke-width="5" stroke-linecap="round"/></g>'
# spoon
d+=f'<g transform="rotate(-35 500 500)"><ellipse cx="500" cy="260" rx="30" ry="20" fill="#cfc2ad" stroke="{DARK}" stroke-width="4"/><rect x="494" y="275" width="12" height="190" rx="6" fill="#cfc2ad" stroke="{DARK}" stroke-width="4"/></g>'
save('opt-masala-dabba',d)
# ---------- 2. Chilli rangoli
def chilli(fill):
    return f'<path d="M0,-150 C22,-150 30,-120 28,-80 C26,-40 12,0 0,30 C-12,0 -26,-40 -28,-80 C-30,-120 -22,-150 0,-150 Z" fill="{fill}" stroke="{DARK}" stroke-width="5"/><path d="M0,-150 C0,-165 8,-175 18,-180" stroke="#7a8b3a" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M-14,-150 Q0,-140 14,-150" stroke="#7a8b3a" stroke-width="8" fill="none" stroke-linecap="round"/>'
def petal(len_,w,fill):
    return f'<path d="M0,0 C{w},{-len_*0.3} {w*0.6},{-len_*0.8} 0,{-len_} C{-w*0.6},{-len_*0.8} {-w},{-len_*0.3} 0,0 Z" fill="{fill}" stroke="{DARK}" stroke-width="5"/>'
r=''
for i in range(0):
    a=math.radians(i*15); r+=f'<circle cx="{500+420*math.cos(a):.1f}" cy="{500+420*math.sin(a):.1f}" r="9" fill="{CREAM}"/>'
for i in range(8):  # outer chillies, stems outward
    r+=f'<g transform="translate(500,500) rotate({i*45+22.5}) translate(0,-255) scale(0.9)">{chilli("#d33a1c")}</g>'
for i in range(8):
    r+=f'<g transform="translate(500,500) rotate({i*45})">{petal(250,70,CREAM)}</g>'
for i in range(8):
    r+=f'<g transform="translate(500,500) rotate({i*45+22.5})">{petal(200,60,GOLD)}</g>'
for i in range(8):
    r+=f'<g transform="translate(500,500) rotate({i*45})">{petal(130,45,ORANGE)}</g>'
for i in range(16):
    a=math.radians(i*22.5); r+=f'<circle cx="{500+95*math.cos(a):.1f}" cy="{500+95*math.sin(a):.1f}" r="7" fill="{CREAM}"/>'
r+=''.join(f'<g transform="translate(500,500) rotate({i*45+22.5}) translate(0,-255) scale(0.9)">{chilli("#d33a1c")}</g>' for i in range(8))
r+=''.join(f'<circle cx="{500+420*math.cos(math.radians(i*45)):.1f}" cy="{500+330*math.sin(math.radians(i*45)):.1f}" r="10" fill="{CREAM}"/>' for i in range(8))
r+=f'<circle cx="500" cy="500" r="62" fill="{DARK}" stroke="{CREAM}" stroke-width="6"/><circle cx="500" cy="500" r="30" fill="{ORANGE}"/><circle cx="500" cy="500" r="10" fill="{CREAM}"/>'
for i in range(8):
    a=math.radians(i*45); r+=f'<circle cx="{500+262*math.cos(a):.1f}" cy="{500+262*math.sin(a):.1f}" r="0" />'
save('opt-chilli-rangoli',r)
# ---------- 3. Elephant
shapes=['<path d="M300,540 C280,440 360,395 470,392 L620,395 C660,398 690,420 700,450 L700,560 C680,590 330,595 300,540 Z"/>',
        '<circle cx="705" cy="455" r="92"/>',
        '<rect x="325" y="520" width="78" height="190" rx="22"/>','<rect x="420" y="530" width="78" height="185" rx="22"/>',
        '<rect x="555" y="530" width="78" height="185" rx="22"/>','<rect x="640" y="520" width="78" height="190" rx="22"/>']
trunk='M775,500 C810,540 835,520 845,470 C855,420 840,360 810,330 C795,315 775,330 790,345'
e=f'<g fill="{CREAM}" stroke="{CREAM}" stroke-width="16" stroke-linejoin="round">{"".join(shapes)}</g>'
e+=f'<path d="{trunk}" fill="none" stroke="{CREAM}" stroke-width="62" stroke-linecap="round"/>'
e+=f'<g fill="{ORANGE}">{"".join(shapes)}</g>'
e+=f'<path d="{trunk}" fill="none" stroke="{ORANGE}" stroke-width="46" stroke-linecap="round"/>'
# chilli held in trunk
e+=f'<g transform="translate(795,300) rotate(-40) scale(0.55)">{chilli("#d33a1c")}</g>'
# toenails
for x in (345,375,440,470,575,605,660,690): e+=f'<path d="M{x},712 a10,10 0 0 1 20,0" fill="{CREAM}"/>'
# ear
e+=f'<path d="M640,395 C600,420 590,520 625,560 C660,585 700,540 690,480 C685,440 670,405 640,395 Z" fill="{GOLD}" stroke="{DARK}" stroke-width="6"/>'
e+=f'<circle cx="745" cy="440" r="10" fill="{DARK}"/>'
e+=f'<path d="M760,505 C790,520 815,510 830,490" stroke="{CREAM}" stroke-width="14" fill="none" stroke-linecap="round"/>'
# blanket
e+=f'<path d="M410,392 L600,395 L612,500 Q590,525 568,500 Q546,525 524,500 Q502,525 480,500 Q458,525 436,500 Q414,525 398,500 Z" fill="{CREAM}" stroke="{DARK}" stroke-width="6"/>'
e+=f'<path d="M405,470 L608,470" stroke="{ORANGE}" stroke-width="8"/>'
for i,x in enumerate(range(440,600,42)):
    e+=f'<g transform="translate({x},445) scale(0.28) rotate(20)"><path d="M0,0 C-48,0 -60,-45 -50,-85 C-40,-125 -10,-160 8,-205 C14,-222 34,-218 30,-198 C24,-165 44,-130 48,-85 C54,-35 40,0 0,0 Z" fill="{ORANGE}" stroke="{DARK}" stroke-width="10"/></g>'
for x in (398,436,480,524,568,612): e+=f'<line x1="{x}" y1="505" x2="{x}" y2="530" stroke="{GOLD}" stroke-width="6"/><circle cx="{x}" cy="534" r="7" fill="{GOLD}"/>'
e+=f'<path d="M298,470 C270,490 262,520 268,545" stroke="{CREAM}" stroke-width="8" fill="none" stroke-linecap="round"/>'
save('opt-elephant',f'<g transform="translate(500,520) scale(1.12) translate(-570,-540)">{e}</g>')
