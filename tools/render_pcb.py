from pathlib import Path
import pcbnew as p
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];b=p.LoadBoard(str(R/'hardware/controller/controller.kicad_pcb'))
s=10;off=100
im=Image.new('RGB',(1200,1300),'#0b1422');d=ImageDraw.Draw(im)
def xy(v):return (off+p.ToMM(v.x)*s,off+p.ToMM(v.y)*s)
d.rectangle((100,100,1100,1100),fill='#174e40',outline='#8dbbb0',width=3)
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):
  x,y=xy(t.GetPosition());r=p.ToMM(t.GetWidth())*s/2;d.ellipse((x-r,y-r,x+r,y+r),fill='#c5c9ae');d.ellipse((x-2,y-2,x+2,y+2),fill='#102b29')
 else:d.line((xy(t.GetStart()),xy(t.GetEnd())),fill='#ca7658' if t.GetLayer()==p.F_Cu else '#5c9ac4',width=max(2,round(p.ToMM(t.GetWidth())*s)))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
for fp in b.GetFootprints():
 for pd in fp.Pads():
  x,y=xy(pd.GetPosition());sz=pd.GetSize();rx=p.ToMM(sz.x)*s/2;ry=p.ToMM(sz.y)*s/2
  if pd.GetShape()==p.PAD_SHAPE_RECT:d.rectangle((x-rx,y-ry,x+rx,y+ry),fill='#e6ce8d')
  else:d.ellipse((x-rx,y-ry,x+rx,y+ry),fill='#e6ce8d')
  rr=p.ToMM(pd.GetDrillSize().x)*s/2;d.ellipse((x-rr,y-rr,x+rr,y+rr),fill='#0b1422')
 if not fp.GetReference().startswith('H'):d.text(xy(fp.Reference().GetPosition()),fp.GetReference(),fill='white',font=font)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',27)
d.text((100,1150),'SplitBeacon Rev A / 100 x 100 mm / 2 copper layers',font=f,fill='white')
d.text((100,1200),'Plot from routed KiCad geometry. See DRC report for validation.',font=font,fill='#b7cddd')
im.save(R/'preview'/'pcb.png')
