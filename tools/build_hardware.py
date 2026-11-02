from pathlib import Path
import json, uuid, math, shutil
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1]
HW=ROOT/'hardware'; HW.mkdir(exist_ok=True)
LIB=Path('/home/yon/.local/opt/kicad-local/root/usr/share/kicad/footprints')
def uid(): return str(uuid.uuid4())
def q(s): return json.dumps(str(s))
def mm(x,y): return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
boards={}
def comp(board,ref,value,pins,foot,x,y,rot=0):
    boards[board]['parts'].append(dict(ref=ref,value=value,pins={str(k):v for k,v in pins.items()},foot=foot,x=x,y=y,rot=rot))
for n,w,h in [('controller',100,100)]: boards[n]=dict(width=w,height=h,parts=[])
pico={1:'NC_GP0',2:'NC_GP1',3:'GND',4:'NC_GP2',5:'NC_GP3',6:'GND',7:'NC_GP4',8:'RUN_BTN',9:'LAP_BTN',10:'PAGE_BTN',11:'GND',12:'BEEP',13:'NC_GP9',14:'NC_GP10',15:'TFT_BL',16:'GND',17:'TFT_DC',18:'TFT_RST',19:'PIXEL2_3V3',20:'PIXEL_3V3',21:'TFT_MISO',22:'TFT_CS',23:'GND',24:'TFT_SCK',25:'TFT_MOSI',26:'NC_GP20',27:'NC_GP21',28:'GND',29:'NC_GP22',30:'RUN',31:'BRIGHTNESS',32:'AMBIENT',33:'GND',34:'TARGET',35:'NC_ADCREF',36:'+3V3',37:'NC_3V3EN',38:'GND',39:'VSYS',40:'NC_VBUS'}
comp('controller','U1','Raspberry Pi Pico RP2040',pico,'SplitBeacon:Pico_Socket',12,8)
comp('controller','J1','5V REGULATED INPUT',{1:'+5V_IN',2:'GND'},'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',85,10)
comp('controller','F1','MF-R050 500mA PTC',{1:'+5V_IN',2:'+5V_DISPLAY'},'SplitBeacon:PTC_5mm',73,8)
comp('controller','D1','1N5817 VSYS OR-ing',{1:'VSYS',2:'+5V_DISPLAY'},'Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal',38,8)
comp('controller','J2','RGB MATRIX DIN HARNESS',{1:'+5V_DISPLAY',2:'GND',3:'PIXEL_DATA'},'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical',85,28)
comp('controller','J8','RGB RIGHT HARNESS',{1:'+5V_DISPLAY',2:'GND',3:'PIXEL2_DATA'},'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical',85,38)
comp('controller','J3','TFT LOGIC HARNESS',{1:'+3V3',2:'GND',3:'TFT_SCK',4:'TFT_MOSI',5:'TFT_CS',6:'TFT_DC',7:'TFT_RST',8:'TFT_BL',9:'TFT_MISO'},'Connector_PinHeader_2.54mm:PinHeader_1x09_P2.54mm_Vertical',85,48)
comp('controller','J4','10K TARGET POT',{1:'+3V3',2:'TARGET',3:'GND'},'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical',44,52)
comp('controller','J5','10K BRIGHTNESS POT',{1:'+3V3',2:'BRIGHTNESS',3:'GND'},'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical',63,52)
comp('controller','J6','PASSIVE PIEZO',{1:'PIEZO_OUT',2:'GND'},'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',71,74)
comp('controller','J7','LDR AT PANEL',{1:'+3V3',2:'AMBIENT'},'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',72,57)
comp('controller','R1','330R',{1:'PIXEL_3V3',2:'PIXEL_DATA'},'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',67,32)
comp('controller','R2','330R',{1:'PIXEL2_3V3',2:'PIXEL2_DATA'},'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',52,36)
comp('controller','R7','100k',{1:'PIXEL2_3V3',2:'GND'},'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',35,37)
comp('controller','R3','100k',{1:'PIXEL_3V3',2:'GND'},'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',37,45)
comp('controller','R4','10k',{1:'AMBIENT',2:'GND'},'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',68,64)
comp('controller','R5','1k',{1:'BEEP',2:'PIEZO_OUT'},'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',56,72)
comp('controller','R6','10k',{1:'RUN',2:'+3V3'},'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',37,14)
comp('controller','C1','100nF',{1:'+5V_DISPLAY',2:'GND'},'Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm',61,15)
comp('controller','C2','100nF',{1:'+3V3',2:'GND'},'Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm',35,64)
comp('controller','C3','1000uF 10V',{1:'+5V_DISPLAY',2:'GND'},'Capacitor_THT:CP_Radial_D10.0mm_P5.00mm',73,20)
comp('controller','C4','100nF',{1:'BRIGHTNESS',2:'GND'},'Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm',53,63)
comp('controller','C5','100nF',{1:'AMBIENT',2:'GND'},'Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm',58,43)
for i,(title,net,x) in enumerate([('RUN STOP','RUN_BTN',12),('LAP','LAP_BTN',36),('VIEW','PAGE_BTN',60)]):
 comp('controller','SW'+str(i+1),title,{1:net,2:'GND'},'SplitBeacon:Button_6mm',x,85)
# Standalone local footprint library, including footprints copied from KiCad licensed upstream.
pretty=HW/'SplitBeacon.pretty';pretty.mkdir(exist_ok=True)
def custom(name,pads,outline):
    s=f'(footprint "{name}" (version 20221018) (generator pcbnew) (layer "F.Cu") (attr through_hole)\n'
    s+='(fp_text reference "REF**" (at 0 -3) (layer "F.SilkS") (effects (font (size 1 1) (thickness .15))))\n'
    s+=f'(fp_text value "{name}" (at 0 3) (layer "F.Fab") (effects (font (size 1 1) (thickness .15))))\n'
    for n,x,y,net in pads:
        shape='rect' if n==1 else 'circle'
        s+=f'(pad "{n}" thru_hole {shape} (at {x} {y}) (size 1.8 1.8) (drill 1) (layers "*.Cu" "*.Mask"))\n'
    x1,y1,x2,y2=outline;s+=f'(fp_rect (start {x1} {y1}) (end {x2} {y2}) (stroke (width .15) (type default)) (fill none) (layer "F.Fab"))\n)'
    (pretty/(name+'.kicad_mod')).write_text(s)
custom('Pico_Socket',[(n,0,2.54*(n-1),'') if n<=20 else (n,17.78,2.54*(40-n),'') for n in range(1,41)],(-1.61,-1.5,19.39,50.5))
custom('Button_6mm',[(1,0,0,''),(1,0,4.5,''),(2,6.5,0,''),(2,6.5,4.5,'')],(-.7,-.7,7.2,5.2))
custom('PTC_5mm',[(1,0,0,''),(2,5.08,0,'')],(-2,-1.5,7,1.5))
custom('BPW85C',[(1,-1.27,0,''),(2,1.27,0,'')],(-1.7,-1.8,1.7,1.8))
custom('IR_5mm',[(1,-1.27,0,''),(2,1.27,0,'')],(-2.7,-2.7,2.7,2.7))
for bd in boards.values():
 for c in bd['parts']:
    if c['foot'].startswith('SplitBeacon:'):continue
    lib,name=c['foot'].split(':'); src=LIB/(lib+'.pretty')/(name+'.kicad_mod')
    if not src.exists():raise FileNotFoundError(src)
    shutil.copy(src,pretty/(name+'.kicad_mod'));c['foot']='SplitBeacon:'+name
(HW/'fp-lib-table').write_text('(fp_lib_table (lib (name "SplitBeacon") (type "KiCad") (uri "${KIPRJMOD}/SplitBeacon.pretty") (options "") (descr "Local project footprints")))')
# General rectangular symbols with explicit logical pin names. Passive parts use a two-pin box.
def symbol(c):
    n=c['ref']; pins=c['pins'];count=len(pins); rows=math.ceil(count/2) if count>8 else count
    half=12.7;top=(rows-1)*1.27; pinpositions={};s=f'(symbol "SplitBeacon:{n}" (pin_names (offset 0.508)) (in_bom yes) (on_board yes)\n'
    for k,v,x,y in [('Reference',n,0,top+5.08),('Value',c['value'],0,top+2.54),('Footprint',c['foot'],0,-top-5.08)]:
        s+=f'(property "{k}" {q(v)} (at {x} {y} 0) (effects (font (size 1 1))'+(' hide' if k=='Footprint' else '')+'))\n'
    s+=f'(symbol "{n}_0_1" (rectangle (start {-half} {top+1.27}) (end {half} {-top-1.27}) (stroke (width .254) (type default)) (fill (type background))))\n'
    s+=f'(symbol "{n}_1_1"\n'
    for j,(number,net) in enumerate(pins.items()):
        right=count>8 and j>=rows;r=j-rows if right else j
        x=(half+5.08)*(1 if right else -1); y=top-r*2.54;angle=180 if right else 0
        name=net.removeprefix('RAW_') if n=='U1' else net
        s+=f'(pin passive line (at {x} {y} {angle}) (length 5.08) (name {q(name)} (effects (font (size .85 .85)))) (number {q(number)} (effects (font (size .85 .85)))))\n'
        pinpositions[number]=(x,-y,right)
    return s+'))',pinpositions,rows
shutil.copy(LIB/'MountingHole.pretty'/'MountingHole_3.2mm_M3.kicad_mod',pretty/'MountingHole_3.2mm_M3.kicad_mod')
for name,bd in boards.items():
    out=HW/name;out.mkdir(exist_ok=True)
    # Each board carries local table pointing upward.
    (out/'fp-lib-table').write_text('(fp_lib_table (lib (name "SplitBeacon") (type "KiCad") (uri "${KIPRJMOD}/../SplitBeacon.pretty") (options "") (descr "Local project footprints")))')
    sheetid=uid();libs=[];instances=[];wires=[];texts=[];positions=[]
    # Large A2 single-page schematic: grouped component blocks with explicit net labels.
    col=0;rowy=34;colx=40
    for c in bd['parts']:
        lib,pins,rows=symbol(c);libs.append(lib);height=max(14,rows*2.54+12)
        if rowy+height>380:colx+=100;rowy=34
        x=colx;y=rowy+(rows-1)*1.27+5.08;rowy+=height
        cid=uid();c['uuid']=cid
        inst=f'(symbol (lib_id "SplitBeacon:{c["ref"]}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid "{cid}")\n'
        for k,v,yy in [('Reference',c['ref'],y-(rows-1)*1.27-5.08),('Value',c['value'],y-(rows-1)*1.27-2.54),('Footprint',c['foot'],y+rows*1.27+5.08)]:
            inst+=f'(property "{k}" {q(v)} (at {x} {yy} 0) (effects (font (size 1 1))'+(' hide' if k=='Footprint' else '')+'))\n'
        for num in pins:inst+=f'(pin "{num}" (uuid "{uid()}"))\n'
        inst+=f'(instances (project "{name}" (path "/{sheetid}" (reference "{c["ref"]}") (unit 1)))))';instances.append(inst)
        for num,(dx,dy,right) in pins.items():
            net=c['pins'][num];px=x+dx;py=y+dy
            if net.startswith('NC_'):
                wires.append(f'(no_connect (at {px} {py}) (uuid "{uid()}"))');continue
            ex=px+(7.62 if right else -7.62)
            wires.append(f'(wire (pts (xy {px} {py}) (xy {ex} {py})) (stroke (width 0) (type default)) (uuid "{uid()}"))')
            wires.append(f'(label {q(net)} (at {ex} {py} {180 if right else 0}) (effects (font (size 1 1)) (justify {"right" if right else "left"} bottom)) (uuid "{uid()}"))')
    sch=f'(kicad_sch (version 20230121) (generator eeschema) (uuid "{sheetid}") (paper "A2") (title_block (title "SplitBeacon - {name}") (date "2026-11-01") (rev "A") (company "AI-assisted engineering prototype"))\n(lib_symbols '+''.join(libs)+')\n'+''.join(wires)+''.join(instances)+'\n(sheet_instances (path "/" (page "1"))))'
    (out/(name+'.kicad_sch')).write_text(sch)
    board=p.BOARD();board.SetCopperLayerCount(2)
    nets={}
    for net in sorted({v for c in bd['parts'] for v in c['pins'].values() if not v.startswith('NC_')}):
        ni=p.NETINFO_ITEM(board,net);board.Add(ni);nets[net]=ni
    for c in bd['parts']:
        fp=p.FootprintLoad(str(pretty),c['foot'].split(':')[1]);fp.SetReference(c['ref']);fp.SetValue(c['value']);fp.SetPosition(mm(c['x'],c['y']));fp.SetOrientationDegrees(c['rot']);fp.SetPath(p.KIID_PATH('/'+sheetid+'/'+c['uuid']))
        # Ensure IDs point to bundled lib.
        fp.SetFPID(p.LIB_ID('SplitBeacon',c['foot'].split(':')[1]))
        board.Add(fp)
        for pad in fp.Pads():
            net=c['pins'].get(pad.GetNumber())
            if net in nets:pad.SetNet(nets[net])
        fp.Reference().SetTextSize(mm(.85,.85));fp.Value().SetVisible(False)
    w,h=bd['width'],bd['height']
    for (a,b) in [((0,0),(w,0)),((w,0),(w,h)),((w,h),(0,h)),((0,h),(0,0))]:
        l=p.PCB_SHAPE();l.SetShape(p.SHAPE_T_SEGMENT);l.SetStart(mm(*a));l.SetEnd(mm(*b));l.SetLayer(p.Edge_Cuts);l.SetWidth(p.FromMM(.05));board.Add(l)
    for x,y in ([(4,4),(96,4),(4,96),(96,96)] if name=='controller' else [(3,9),(86,9)]):
        f=p.FootprintLoad(str(pretty),'MountingHole_3.2mm_M3');f.SetReference('H'+str(x)+str(y));f.SetPosition(mm(x,y));f.SetFPID(p.LIB_ID('SplitBeacon','MountingHole_3.2mm_M3'));f.Reference().SetVisible(False);f.Value().SetVisible(False);board.Add(f)
    txt=p.PCB_TEXT(board);txt.SetText('SPLITBEACON / '+name.upper()+' / REV A');txt.SetPosition(mm(w/2,3 if name=='controller' else h-1.5));txt.SetTextSize(mm(1,1));txt.SetTextThickness(p.FromMM(.15));txt.SetLayer(p.F_SilkS);board.Add(txt)
    board.Save(str(out/(name+'.kicad_pcb')))
    # Standard project with conservative rules, no hidden exclusions.
    project={'board':{'design_settings':{'rules':{'min_clearance':.25,'min_track_width':.25,'min_via_diameter':.7,'min_through_hole_diameter':.3,'min_via_annular_width':.15,'min_hole_clearance':.25},'defaults':{'board_outline_line_width':.05}}},'net_settings':{'classes':[{'name':'Default','clearance':.25,'track_width':.3,'via_diameter':.8,'via_drill':.4,'microvia_diameter':.3,'microvia_drill':.1,'diff_pair_width':.25,'diff_pair_gap':.25,'diff_pair_via_gap':.25}]}}
    (out/(name+'.kicad_pro')).write_text(json.dumps(project,indent=2))
(HW/'design.json').write_text(json.dumps(boards,indent=2))
print('Generated SplitBeacon schematic, placed PCB, and local footprint library')
