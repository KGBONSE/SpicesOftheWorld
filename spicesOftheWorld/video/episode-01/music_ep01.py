"""Original afrobeat/highlife-style music bed for Ep 1 (same synth recipe as the farm-to-fire chips Short).
Royalty-free because it is generated here. Sections follow the episode's chapters."""
import numpy as np, wave, sys
SR=44100; BPM=104; BEAT=60/BPM; S16=BEAT/4; BAR=4*BEAT
DUR=float(sys.argv[1]); OUT=sys.argv[2]
N=int(SR*(DUR+3)); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(11)
def add(sig,t,g=1.0,pan=0.0):
    i=int(t*SR); j=min(N,i+len(sig))
    if i>=N or j<=i: return
    L[i:j]+=sig[:j-i]*g*(1-max(0,pan)); R[i:j]+=sig[:j-i]*g*(1+min(0,pan))
def kick():
    n=int(.35*SR); t=np.arange(n)/SR; f=48+80*np.exp(-t*35); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t*7)
def clap():
    n=int(.25*SR); t=np.arange(n)/SR; x=rng.standard_normal(n)
    x=x*(np.exp(-t*25)+0.6*np.exp(-np.maximum(0,t-0.012)*40)*(t>0.012))
    return (np.convolve(x,np.ones(6)/6,'same')-np.convolve(x,np.ones(40)/40,'same'))*0.8
SH=[None,None]
def shaker(acc):
    k=int(acc)
    if SH[k] is None:
        n=int(.07*SR); t=np.arange(n)/SR; x=rng.standard_normal(n); x=x-np.convolve(x,np.ones(8)/8,'same')
        SH[k]=x*np.minimum(1,t/0.01)*np.exp(-t*60)*(0.26 if acc else 0.12)
    return SH[k]
def rim():
    n=int(.08*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*1700*t)+0.5*np.sin(2*np.pi*820*t))*np.exp(-t*60)*0.3
def logdrum(freq,dur=0.4):
    n=int(dur*SR); t=np.arange(n)/SR; f=freq*(1+0.6*np.exp(-t*40)); ph=2*np.pi*np.cumsum(f)/SR
    return np.tanh((np.sin(ph)+0.25*np.sin(2*ph))*1.8)*np.exp(-t*5.5)*0.5
PL={}
def pluck(freq,dur=0.55):
    key=round(freq,2)
    if key in PL: return PL[key]
    n=int(dur*SR); p=max(2,int(SR/freq)); buf=rng.uniform(-1,1,p); out=np.zeros(n)
    for i in range(n):
        out[i]=buf[i%p]; buf[i%p]=0.5*(buf[i%p]+buf[(i+1)%p])*0.996
    PL[key]=out*np.minimum(1,np.arange(n)/(SR*0.002))*0.33; return PL[key]
def marimba(freq,dur=0.5):
    n=int(dur*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*freq*t)+0.35*np.sin(2*np.pi*freq*4*t)*np.exp(-t*30))*np.exp(-t*6)*0.26
def pad(freqs,dur):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for f in freqs:
        for dt in (-0.004,0.004): s+=np.sin(2*np.pi*f*(1+dt)*t)+0.3*np.sin(2*np.pi*2*f*(1+dt)*t)
    return s*np.minimum(1,t/0.5)*np.minimum(1,np.maximum(0,dur-t)/0.5)*0.03
def bass(freq,dur):
    n=int(dur*SR); t=np.arange(n)/SR
    return np.tanh(np.sin(2*np.pi*freq*t)*1.5)*np.exp(-t*3)*np.minimum(1,t/0.005)*0.22
mid=lambda m:440*2**((m-69)/12)
PROG={'A':([[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]],[41,40,38,36]),   # Fmaj7 Em7 Dm7 Cmaj7
      'B':([[57,60,64,67],[50,53,57,60],[55,59,62,65],[48,52,55,59]],[45,38,43,36]),   # Am7 Dm7 G7 Cmaj7 (highlife)
      'C':([[48,52,55,60],[53,57,60,65],[55,59,62,67],[53,57,60,65]],[36,41,43,41])}   # C F G F
# (start sec, prog, layers) — layers: pad, gtr, shk, kick, clap, rim, log, mar, bass
SECT=[(0,'A','pad gtr'),(20,'A','pad gtr shk'),(80,'B','pad gtr shk kick log bass'),
      (122,'B','pad gtr shk kick rim log bass'),(175,'A','pad gtr shk mar'),
      (241,'C','pad gtr shk kick clap rim log mar bass'),(304,'C','pad gtr shk kick clap rim log bass'),
      (404,'B','pad gtr shk kick clap rim log mar bass'),(480,'A','pad gtr shk kick log mar'),
      (506,'C','pad gtr shk kick clap rim log mar bass')]
def sect(t):
    s=SECT[0]
    for x in SECT:
        if t>=x[0]: s=x
    return s
nb=int(np.ceil(DUR/BAR))+1
for b in range(nb):
    t0=b*BAR; st,pk,lay=sect(t0); lay=set(lay.split()); chs,roots=PROG[pk]
    ch=chs[b%4]; r=roots[b%4]
    if 'pad' in lay: add(pad([mid(m) for m in ch],BAR+0.4),t0)
    if 'bass' in lay:
        for s,m in ((0,r),(6,r),(10,r+7),(14,r+12)): add(bass(mid(m),S16*3),t0+s*S16,0.9)
    for s in range(16):
        t=t0+s*S16+(0.012 if s%2 else 0)
        if 'kick' in lay and (s in (0,8) or s==11): add(kick(),t,0.8)
        if 'clap' in lay and s in (4,12): add(clap(),t,0.4)
        if 'rim' in lay and s in (3,7,10,14): add(rim(),t,0.5,pan=0.3)
        if 'shk' in lay: add(shaker(s%4==2),t,1.0,pan=-0.25)
        if 'log' in lay and s in (0,3,6,10,12): add(logdrum(mid(r+12) if s!=10 else mid(r+19)),t,0.6)
        if 'gtr' in lay and s in (2,5,8,10,13,15):
            m=ch[[1,2,3,2,1,3][[2,5,8,10,13,15].index(s)]]+12; add(pluck(mid(m)),t,0.65,pan=0.35)
        if 'mar' in lay and s in (0,6,12) and b%2==1: add(marimba(mid(ch[3]+24 if s==6 else ch[2]+24)),t,0.7,pan=-0.4)
    # a soft marimba flourish on each new section
    if any(abs(t0-x[0])<BAR/2 and x[0]>0 for x in SECT):
        for i,m in enumerate((ch[0]+24,ch[1]+24,ch[2]+24,ch[3]+24)): add(marimba(mid(m)),t0-BEAT+i*S16,0.6)
st=np.stack([L,R],1)[:int(SR*DUR)]
st=np.tanh(st*1.1)/np.tanh(1.1)
f=np.ones(len(st)); n=int(2.5*SR); f[-n:]=np.linspace(1,0,n); n2=int(1.5*SR); f[:n2]=np.linspace(0,1,n2)
st*=f[:,None]; st/=np.max(np.abs(st))*1.12
w=wave.open(OUT,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st*32767).astype(np.int16).tobytes()); w.close(); print('ok',len(st)/SR)
