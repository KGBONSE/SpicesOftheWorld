import math, cairosvg
DARK='#5a1a0c'; CREAM='#fbe3c0'; ORANGE='#e8741c'; GOLD='#f4a53a'; RED='#d33a1c'
PA=("M0,0 C-48,0 -60,-45 -50,-85 C-40,-125 -10,-160 8,-205 "
    "C14,-222 34,-218 30,-198 C24,-165 44,-130 48,-85 C54,-35 40,0 0,0 Z")
def paisley(sc,fill,sw=7):
    return (f'<g transform="scale({sc})"><path d="{PA}" fill="{fill}" stroke="{DARK}" stroke-width="{sw}"/>'
            f'<ellipse cx="0" cy="-45" rx="27" ry="34" fill="{ORANGE}"/>'
            f'<ellipse cx="0" cy="-45" rx="13" ry="17" fill="{DARK}"/>'
            f'<circle cx="3" cy="-48" r="5" fill="{CREAM}"/></g>')
def frame(inner):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000">
<defs><clipPath id="c"><circle cx="500" cy="500" r="452"/></clipPath></defs>
<circle cx="500" cy="500" r="470" fill="{CREAM}"/><circle cx="500" cy="500" r="455" fill="{DARK}"/>
<g clip-path="url(#c)">{inner}</g></svg>'''
def save(n,inner):
    s=frame(inner); open(n+'.svg','w').write(s); cairosvg.svg2png(bytestring=s.encode(),write_to=n+'.png',output_width=1000)
BODY=f'''
<path d="M362,300 C372,284 400,286 404,306 C410,340 405,390 440,430 C480,470 540,480 578,545
 C565,605 490,618 450,592 C400,560 386,502 381,452 C377,410 381,370 369,336 Z"
 fill="{ORANGE}" stroke="{CREAM}" stroke-width="7" stroke-linejoin="round"/>
<path d="M366,304 L326,322 L368,330 Z" fill="{GOLD}" stroke="{CREAM}" stroke-width="4" stroke-linejoin="round"/>
<circle cx="384" cy="308" r="8" fill="{DARK}"/><circle cx="386" cy="306" r="3" fill="{CREAM}"/>
<path d="M388,288 L366,240 M392,287 L390,228 M396,289 L414,238" stroke="{CREAM}" stroke-width="5" stroke-linecap="round"/>
<circle cx="366" cy="235" r="9" fill="{CREAM}"/><circle cx="390" cy="222" r="9" fill="{CREAM}"/><circle cx="415" cy="233" r="9" fill="{CREAM}"/>
<path d="M455,500 C480,500 520,515 545,548 C520,570 485,572 462,552 Z" fill="{GOLD}" stroke="{DARK}" stroke-width="5"/>
<path d="M470,535 C490,532 510,540 528,553 M480,515 C500,515 518,525 535,540" stroke="{DARK}" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M470,605 L462,690 M505,610 L512,690" stroke="{CREAM}" stroke-width="7" stroke-linecap="round"/>
<path d="M440,694 L482,694 M492,694 L534,694" stroke="{CREAM}" stroke-width="6" stroke-linecap="round"/>'''
def q(p0,c,p1,t):
    x=(1-t)**2*p0[0]+2*(1-t)*t*c[0]+t*t*p1[0]; y=(1-t)**2*p0[1]+2*(1-t)*t*c[1]+t*t*p1[1]
    return x,y,2*(1-t)*(c[0]-p0[0])+2*t*(p1[0]-c[0]),2*(1-t)*(c[1]-p0[1])+2*t*(p1[1]-c[1])
def train():
    base=(545,555); out=''; order=[]
    for c,e in [((720,470),(880,560)),((740,600),(840,745)),((650,700),(690,860)),((560,700),(540,850))]:
        out+=f'<path d="M{base[0]},{base[1]} Q{c[0]},{c[1]} {e[0]},{e[1]}" stroke="{CREAM}" stroke-width="4" fill="none" opacity=".7"/>'
        for i,t in enumerate([0.42,0.7,1.0]):
            x,y,dx,dy=q(base,c,e,t); th=math.degrees(math.atan2(-dx,dy))
            order.append((t,f'<g transform="translate({x:.1f},{y:.1f}) rotate({th:.1f})">{paisley(0.45+0.4*t,CREAM if i==2 else GOLD)}</g>'))
    return out+''.join(s for _,s in sorted(order))
SIDE=train()+BODY
# 1 classic side
save('p1-side', f'<g transform="translate(500,505) scale(1.1) translate(-602,-537)">{SIDE}</g>')
# 2 full fan, front
PX,PY=500,700; f=''
for R,step,sc,col,off in [(345,14,0.95,CREAM,0),(245,16,0.72,GOLD,8),(150,20,0.5,ORANGE,0)]:
    angs=[a for a in range(-98+off,99,step)]
    for a in angs:
        r=math.radians(a); x=PX+R*math.sin(r); y=PY-R*math.cos(r)
        f+=f'<line x1="{PX}" y1="{PY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{CREAM}" stroke-width="2.5" opacity=".45"/>' if col==CREAM else ''
        f+=f'<g transform="translate({x:.1f},{y:.1f}) rotate({a+180})">{paisley(sc,col if col!=ORANGE else GOLD)}</g>'
fb=f'''<path d="M500,760 C448,748 440,660 468,618 C484,594 488,560 487,520 C486,470 488,430 500,420 C512,430 514,470 513,520 C512,560 516,594 532,618 C560,660 552,748 500,760 Z" fill="{ORANGE}" stroke="{CREAM}" stroke-width="7"/>
<ellipse cx="500" cy="402" rx="24" ry="30" fill="{ORANGE}" stroke="{CREAM}" stroke-width="7"/>
<path d="M492,420 L500,446 L508,420 Z" fill="{GOLD}" stroke="{CREAM}" stroke-width="3"/>
<circle cx="490" cy="398" r="5" fill="{DARK}"/><circle cx="510" cy="398" r="5" fill="{DARK}"/>
<path d="M500,372 L480,322 M500,372 L500,314 M500,372 L520,322" stroke="{CREAM}" stroke-width="5" stroke-linecap="round"/>
<circle cx="480" cy="318" r="9" fill="{CREAM}"/><circle cx="500" cy="308" r="9" fill="{CREAM}"/><circle cx="520" cy="318" r="9" fill="{CREAM}"/>
<circle cx="490" cy="665" r="5" fill="{GOLD}"/><circle cx="510" cy="665" r="5" fill="{GOLD}"/><circle cx="500" cy="690" r="5" fill="{GOLD}"/><circle cx="488" cy="715" r="5" fill="{GOLD}"/><circle cx="512" cy="715" r="5" fill="{GOLD}"/>
<path d="M485,758 L480,820 M515,758 L520,820" stroke="{CREAM}" stroke-width="7" stroke-linecap="round"/>'''
save('p2-fan', f'<g transform="translate(0,-40)">{f}{fb}</g>')
# 3 pair facing a chilli
def chilli(sc):
    return f'<g transform="scale({sc})"><path d="M0,-150 C22,-150 30,-120 28,-80 C26,-40 12,0 0,30 C-12,0 -26,-40 -28,-80 C-30,-120 -22,-150 0,-150 Z" fill="{RED}" stroke="{CREAM}" stroke-width="6"/><path d="M0,-150 C0,-165 8,-175 18,-180" stroke="#8a9a45" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M-16,-150 Q0,-138 16,-150" stroke="#8a9a45" stroke-width="9" fill="none" stroke-linecap="round"/></g>'
pair=(f'<g transform="translate(335,168) scale(0.62)">{SIDE}</g>'
      f'<g transform="translate(665,168) scale(-0.62,0.62)">{SIDE}</g>'
      f'<g transform="translate(500,500)">{chilli(1.05)}</g>'
      '')
save('p3-pair', pair)
# 4 tail wraps round the circle
w=''; TB=(551,601)
angs=[88-15*i for i in range(12)]
for i,a in enumerate(angs):
    r=math.radians(a); x=500+335*math.cos(r); y=500+335*math.sin(r)
    w+=f'<line x1="{TB[0]}" y1="{TB[1]}" x2="{x:.1f}" y2="{y:.1f}" stroke="{CREAM}" stroke-width="3" opacity=".5"/>'
for i,a in enumerate(angs):
    r=math.radians(a); x=500+335*math.cos(r); y=500+335*math.sin(r)
    th=math.degrees(math.atan2(-math.cos(r),math.sin(r)))
    w+=f'<g transform="translate({x:.1f},{y:.1f}) rotate({th:.1f})">{paisley(0.62,CREAM if i%2 else GOLD)}</g>'
save('p4-wrap', w+f'<g transform="translate(470,520) scale(0.95) translate(-460,-470)">{BODY}</g>')
