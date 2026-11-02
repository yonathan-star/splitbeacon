from pathlib import Path
import sys
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'firmware'))
from core import Session,matrix_frame
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def f(s):return ImageFont.truetype(font,s)
im=Image.new('RGB',(1500,1000),'#0b1422');d=ImageDraw.Draw(im)
d.text((70,45),'SPLITBEACON',font=f(48),fill='#e9f4ff')
d.text((72,110),'A lap timer that makes your pace visible.',font=f(26),fill='#8fa8be')
d.rounded_rectangle((70,185,830,925),radius=28,fill='#253b50',outline='#6e879b',width=3)
s=Session(30);s.toggle(0);s.tick(17300)
colors=matrix_frame(s)
# Render the real mapping back into x/y coordinates at visible brightness.
from core import matrix_index
for y in range(4):
 for x in range(16):
  rgb=colors[matrix_index(x,y)];rgb=tuple(min(255,v*15) for v in rgb)
  xx=115+x*41;yy=235+y*41
  d.rounded_rectangle((xx,yy,xx+27,yy+27),radius=6,fill=rgb,outline='#526577')
d.rounded_rectangle((110,460,485,675),radius=12,fill='#06101d',outline='#91aab9',width=2)
d.text((130,477),'SPLITBEACON         RUN',font=f(17),fill='#26dfe5')
d.text((130,521),'00:17.30',font=f(52),fill='white')
d.text((130,594),'TARGET 30s    NEXT 30s',font=f(18),fill='#26dfe5')
d.text((130,628),'TOTAL 01:47.30  LAPS 03',font=f(17),fill='#b6cbd9')
for x,label in [(580,'TARGET'),(735,'BRIGHT')]:
 d.ellipse((x-43,495,x+43,581),fill='#101d2b',outline='#b0c3d0',width=3);d.line((x,505,x+19,526),fill='#ffb349',width=5)
 d.text((x-47,603),label,font=f(20),fill='#d8e7f2')
for x,label in [(220,'RUN / PAUSE'),(400,'LAP'),(580,'VIEW')]:
 d.ellipse((x-29,781,x+29,839),fill='#f0a34d',outline='#ffcb87',width=2)
 d.text((x-len(label)*6,863),label,font=f(19),fill='#e3edf5')
for y,title,body in [(225,'Glanceable progress','64 RGB pixels across two panels'),(345,'Useful detail','240 x 135 TFT with three views'),(465,'Made for repeat sessions','Pause, record splits, compare pace'),(585,'Controls that make sense','Target and brightness knobs'),(705,'A complete design package','Custom PCB, firmware and print files')]:
 d.text((910,y),title,font=f(26),fill='#dcecf8');d.text((910,y+43),body,font=f(19),fill='#9cb3c8')
d.text((910,877),'DESIGN VISUALIZATION',font=f(18),fill='#f0a34d')
d.text((910,910),'Not a photograph or hardware test.',font=f(17),fill='#9cb3c8')
im.save(R/'preview'/'splitbeacon.png')
