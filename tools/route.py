from pathlib import Path
import pcbnew as p, math, heapq, json, sys, time
ROOT=Path(__file__).resolve().parents[1]
G=.25

def route(name):
 path=ROOT/'hardware'/name/(name+'.kicad_pcb'); b=p.LoadBoard(str(path)); W,H=(100,100) if name=='controller' else (90,18);nx=int(W/G)+1;ny=int(H/G)+1
 blocked=[{},{}];nodes={}; padinfo=[];novia=set()
 def xy(pos):return p.ToMM(pos.x),p.ToMM(pos.y)
 def idx(x,y):return round(x/G),round(y/G)
 def paint(layer,x,y,r,net):
  ix,iy=idx(x,y);rr=math.ceil(r/G)
  for dx in range(-rr,rr+1):
   for dy in range(-rr,rr+1):
    if dx*dx+dy*dy<=(r/G+.72)**2:
     key=(ix+dx,iy+dy);prev=blocked[layer].get(key)
     blocked[layer][key]=net if prev is None or prev==net else -999
 for fp in b.GetFootprints():
  for pd in fp.Pads():
   x,y=xy(pd.GetPosition());net=pd.GetNetCode();sx,sy=xy(pd.GetSize()); radius=(math.hypot(sx,sy)/2 if pd.GetShape()==p.PAD_SHAPE_RECT else max(sx,sy)/2)+.25+.15+.05
   if pd.GetAttribute()==p.PAD_ATTRIB_NPTH:radius=max(sx,sy)/2+.4
   
   hr=max(p.ToMM(pd.GetDrillSize().x),p.ToMM(pd.GetDrillSize().y))/2+.2+.27
   ix,iy=idx(x,y)
   for dx in range(-math.ceil(hr/G)-1,math.ceil(hr/G)+2):
    for dy in range(-math.ceil(hr/G)-1,math.ceil(hr/G)+2):
     if math.hypot((ix+dx)*G-x,(iy+dy)*G-y)<hr:novia.add((ix+dx,iy+dy))
   padinfo.append((pd,x,y,net));paint(0,x,y,radius,net);paint(1,x,y,radius,net)
   if net: nodes.setdefault(net,[]).append((x,y))
 def valid(x,y,l,net):return 4<=x<nx-4 and 4<=y<ny-4 and blocked[l].get((x,y),net)==net
 def astar(a,z,net):
  start=(*idx(*a),0);start2=(*idx(*a),1);target=idx(*z);queue=[(0,0,start),(0,0,start2)];best={start:0,start2:0};came={};finish=None
  def heuristic(x,y):return (abs(x-target[0])+abs(y-target[1]))*.9
  n=0
  while queue:
   _,cost,cur=heapq.heappop(queue)
   if cost!=best.get(cur):continue
   x,y,l=cur;n+=1
   if (x,y)==target:finish=cur;break
   if n>500000:break
   for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
    xx=x+dx;yy=y+dy
    if not valid(xx,yy,l,net):continue
    step=1.0 if (l==0 and dy==0) or (l==1 and dx==0) else 1.12
    nxt=(xx,yy,l);nc=cost+step
    if nc<best.get(nxt,1e12):best[nxt]=nc;came[nxt]=cur;heapq.heappush(queue,(nc+heuristic(xx,yy),nc,nxt))
   # Via needs .4 radius+.25 clearance+.15 trace width: checked against pad/track maps enlarged a little.
   ok=(x,y) not in novia
   for ll in (0,1):
    for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
     if not valid(x+dx,y+dy,ll,net):ok=False
   if ok:
    nxt=(x,y,1-l);nc=cost+18
    if nc<best.get(nxt,1e12):best[nxt]=nc;came[nxt]=cur;heapq.heappush(queue,(nc+heuristic(x,y),nc,nxt))
  if finish is None:return None
  arr=[finish]
  while arr[-1] in came:arr.append(came[arr[-1]])
  return arr[::-1]
 def track(a,z,layer,net):
  if a==z:return
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(p.FromMM(a[0]),p.FromMM(a[1])));t.SetEnd(p.VECTOR2I(p.FromMM(z[0]),p.FromMM(z[1])));t.SetWidth(p.FromMM(.3));t.SetLayer(p.F_Cu if layer==0 else p.B_Cu);t.SetNetCode(net);b.Add(t)
 def add(path,a,z,net):
  # preserve exact pad centers rather than quantizing pad positions
  track(a,(path[0][0]*G,path[0][1]*G),path[0][2],net)
  begin=path[0];prev=path[0];direction=None
  for cur in path[1:]:
   if cur[2]!=prev[2]:
    track((begin[0]*G,begin[1]*G),(prev[0]*G,prev[1]*G),prev[2],net)
    v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(p.FromMM(cur[0]*G),p.FromMM(cur[1]*G)));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(net);b.Add(v)
    paint(0,cur[0]*G,cur[1]*G,.4+.25+.15,net);paint(1,cur[0]*G,cur[1]*G,.4+.25+.15,net);begin=cur;direction=None
   else:
    d=(cur[0]-prev[0],cur[1]-prev[1])
    if direction is not None and d!=direction:
     track((begin[0]*G,begin[1]*G),(prev[0]*G,prev[1]*G),prev[2],net);begin=prev
    direction=d
   paint(cur[2],cur[0]*G,cur[1]*G,.15+.25+.15,net);prev=cur
  track((begin[0]*G,begin[1]*G),(prev[0]*G,prev[1]*G),prev[2],net);track((prev[0]*G,prev[1]*G),z,prev[2],net)
 tasks=[]
 for net,pts in nodes.items():
  done=[pts[0]];remain=pts[1:]
  while remain:
   dist,a,z=min((abs(a[0]-z[0])+abs(a[1]-z[1]),a,z) for a in done for z in remain);tasks.append((dist,net,a,z));done.append(z);remain.remove(z)
 tasks.sort(key=lambda t:t[0]);failed=[]
 for k,(dist,net,a,z) in enumerate(tasks):
  path2=astar(a,z,net)
  if path2 is None:failed.append((net,a,z));print(name,'FAILED',net,a,z,flush=True)
  else:add(path2,a,z,net)
 b.BuildConnectivity();b.Save(str(path));print(name,len(tasks),'links',len(failed),'failed',flush=True)
 (ROOT/'verification'/(name+'-routing.json')).write_text(json.dumps({'links':len(tasks),'failed':failed},indent=2))
 print('DRC',p.WriteDRCReport(b,str(ROOT/'verification'/(name+'-drc.txt')),p.EDA_UNITS_MILLIMETRES,True),flush=True)
for name in sys.argv[1:] or ['controller']:route(name)
