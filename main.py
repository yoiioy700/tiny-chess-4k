import base64,json,os,sys,zlib;from urllib.request import*
T=zlib.decompress(base64.b85decode('c-l3R-EPz{5QX1@H>fIv3hnM@6WjA^kDX-GX17(V!WC3PLI}kBUou<hL~=4tW-{kH7Wo%FrwDD1ff+?63{1r|2Pj%=u}Ip+)7sMKm*eyO*9rfZ$wj>BQ%G^xAhSV=Sh86IP%EQVLbJR1-s<i+pPs%wELYvbT#uUGz3;cjOStG6BH%u1G0{4S6pv<^e4R>GR=b^NWtb0#>2~H|3C7iSgMQeDPAP$ysXszO&h&8?Ac;`lhjXeiqP8|sB5SiPM{Co1d_1*f@@~gG9yno!Fl>9uk_!t6GD%Sk=z@ep0ATa|q<LJIHSS4Z9q)pSWnB&n%w>~9E24DWLCyei*9{Q19QM1e-=>6N2+(6Yx2SRCM8x~yQ#IK1Qr<Y0oU<pSO1?V$%tRzSwQ^=)&tINS>)qqi?_WP&zQ6qZ^Hw)(BgC}5?h=w)*hOY9P4O()!K5U$)|`DKXU5b83XCCcZ}zS_Twg|vgy0wxu_BzQ`5Xk!!0l&Gi(mdDpM}*``d19>GLZ<~ZV@I>7bSwP$b5Jt5Y6fWP+ujo=sB3YosTEk^_m-<wGXkQA$2hh-m`adMYCm1qb=h!SE+4T59{psZ<on(s?%X@qhPJgk4fG15d*|7pqAptA#twN6chXVnvwk0rY6~HsmoH(irHNARqxIeO@9G~H^Cb'))
R=range;V=[[0]*128 for _ in R(13)]
for k in R(384):p=k>>6;s=(k&63)+(k&56);w=(0,1,1,2,4,0)[p]<<32;V[p+1][s]=d=w+(-43,20,27,55,192,-64)[p]+T[k]+((-40,6,10,64,170,-64)[p]+T[k+384]<<16);V[-p-1][s^112]=2*w-d
E=15,17,-15,-17;F=1,-1,16,-16;D=0,(-15,-17),(14,18,31,33,-14,-18,-31,-33),E,F,E+F,E+F;I=32000;B=board=[0]*128;side=1;H=N=X=XR=0;Z=-1;C=set();K=[];Q=0;NODES=25000
def set_fen(f):
 global side,C,Z,H,Q;P=f.split();B[:]=[0]*128;s=112
 for c in P[0]:B[s]='kqrbnp.PNBRQK'.find(c)-6 if c>'@'else 0;s+=int(c)if'/'<c<'A'else-24 if c<'0'else 1
 side=1-2*(P[1]<'w');C={(7,0,119,112)[i]for i in R(4)if'KQkq'[i]in P[2]};Z=ord(P[3][0])+16*int(P[3][1])-113 if P[3]>'-'else-1;H=int((P+[0])[4]);K[:]=[];Q=sum(V[B[i]][i]for i in R(128))
def A(s,c):
 for k in R(1,7):
  for d in D[k]:
   t=s
   while not(t:=t+d*c)&136:
    if B[t]==k*c:return 1
    if B[t]or k in(1,2,6):break
attacked=A
def gen(q):
 s=side;m=[];G=m.append
 for f in R(128):
  if(p:=B[f]*s)==1:
   t=f+16*s;h=t<8 or t>111
   for u in t-1,t+1,t:
    if(not(B[t]or h and q)if u==t else not u&136 and(B[u]*s<0 or u==Z)):
     for r in(5,2,4,3)[:4-3*q]if h else(0,):G(f|u<<7|r<<14)
     if u==t and f>>4 in(1,6)and not h and not B[t+16*s]:G(f|t+16*s<<7)
  elif p>1:
   for d in D[p]:
    t=f
    while not(t:=t+d)&136:
     if(c:=B[t])*s<0 or not(c or q):G(f|t<<7)
     if c or p in(2,6):break
   for i,d in((3,1),(-4,-1))*(p==6 and not q):
    if f+i in C and not(B[f+d]or B[f+2*d]or B[f+i-d]or A(f,-s)or A(f+d,-s)):G(f|f+2*d<<7)
 return m
def make(m):
 global side,C,Z,H,Q;f=m&127;t=m>>7&127;p=B[f];c=B[t];s=side;K.append((B[:],C,Z,H,Q));H=0 if c or p==s else H+1;Q+=V[(m>>14)*s or p][t]-V[p][f]-V[c][t];B[f]=0
 if p==s and t==Z:B[t-16*s]=0;Q-=V[-p][t-16*s]
 if p==6*s and abs(t-f)==2:r=f+3 if t>f else f-4;Q+=V[4*s][f+t>>1]-V[4*s][r];B[f+t>>1]=4*s;B[r]=0
 B[t]=(m>>14)*s or p;Z=f+16*s if p==s and t-f==32*s else-1;C=C-{f,t,f+3,f-4};side=-s
def U():global side,C,Z,H,Q;B[:],C,Z,H,Q=K.pop();side=-side
unmake=U
def S(d,a,b,y,n):
 global N,X,XR,Z,H,side;s=side;c=A(B.index(6*s),-s);d+=bool(c)*(d>0);q=d<=0;N+=1
 if N>NODES:raise
 if y and not q and(H>99 or B in[x[0]for x in K[-2:-H-1:-2]]):return 0
 x=Q;e=x+32768>>16;m=x-(e<<16);h=e+32768>>16;e-=h<<16;v=0 if h<2 and not{1,-1}&set(B)else(m*min(h,24)+e*max(0,24-h))//6*s+10
 if q and v>=b:return v
 a=max(a,v)if q else a;v=v if q else-I;g=0
 for m in sorted(gen(q),key=lambda m:abs(B[m&127])-(abs(B[m>>7&127])+(m>>14))*16+(not y and m==XR)*99999):
  u=not(m>>14 or B[m>>7]);make(m)
  if A(B.index(6*s),-s):U();continue
  g+=1;r=d>2 and u and g>3 and not c;w=-S(d-1-r,-a-1,-a,y+1,1)if g>1 and not q else a+1
  if w>a:w=-S(d-1,-b,-a,y+1,1)
  U();v=max(v,w)
  if w>a:a=w;XR=m if not y else XR
  if a>=b:break
 if not y:X=XR
 return v if g or q else y-30000 if c else 0
W=lambda s:chr(97+s%8)+chr(49+(s>>4));uci=lambda m:W(m&127)+W(m>>7&127)+' pnbrqk'[m>>14].strip();P=lambda p,b:json.load(urlopen(Request(J+p,json.dumps(b).encode(),{'content-type':'application/json'})))
if J:=os.getenv('MAKEFUN_ENV_URL'):
 while(g:=P('/game',{}))['status']!='done':
  while g['status']=='your_move':
   try:N=X=XR=0;set_fen(g['start_fen']);[make(m)for u in g['moves']for m in gen(0)if uci(m)==u];[S(d,-I,I,0,0)for d in R(1,64)]
   except:0
   g=P('/move',{'game':g['game'],'move':u if(u:=uci(X))in(L:=g['legal_moves'])else L[0]})
  print(g,file=sys.stderr)
