from pathlib import Path
import xml.etree.ElementTree as E,json
import pcbnew as p
R=Path(__file__).resolve().parents[1];b=p.LoadBoard(str(R/'hardware/controller/controller.kicad_pcb'))
sch=E.parse(R/'hardware/controller/controller.xml')
a={}
for net in sch.findall('.//nets/net'):
 name=net.attrib['name'].lstrip('/')
 for node in net.findall('node'): a[(node.attrib['ref'],node.attrib['pin'])]=name
c={}
for fp in b.GetFootprints():
 for pad in fp.Pads():
  if pad.GetNetname():c[(fp.GetReference(),pad.GetNumber())]=pad.GetNetname()
# NC pads appear as isolated nets in schematic exports; exclude only explicitly NC pins.
expected=json.loads((R/'hardware/design.json').read_text())['controller']['parts']
logical={(x['ref'],pin):net for x in expected for pin,net in x['pins'].items() if not net.startswith('NC_')}
errors=[]
for key,net in logical.items():
 if a.get(key)!=net or c.get(key)!=net:errors.append([key,net,a.get(key),c.get(key)])
assert not errors, errors
(R/'verification/netlist-check.txt').write_text(f'PASS: {len(logical)} connected logical pins match schematic export and routed PCB.\nExplicit NC pins excluded; mounting holes are mechanical only.\nThis is a connectivity consistency check, not electrical ERC.\n')
print('PASS',len(logical),'logical pin mappings')
