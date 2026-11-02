// SplitBeacon parametric enclosure, millimetres. Print part base/lid/retainer/plunger.
// Lid is exported flat with its external face on the build plate.
part="assembly";
$fn=48;
W=128; D=150; H=40; wall=2.5;
pcb_origin=[14,38];
board_holes=[[18,42],[110,42],[18,134],[110,134]];
case_holes=[[6,6],[122,6],[6,144],[122,144]];
buttons=[29.25,53.25,77.25];
module ring(od,id,h){difference(){cylinder(d=od,h=h);translate([0,0,-.1])cylinder(d=id,h=h+.2);}}
module base(){
 difference(){
  union(){
   difference(){cube([W,D,H]);translate([wall,wall,wall])cube([W-2*wall,D-2*wall,H]);}
   for(p=board_holes)translate([p[0],p[1],wall])ring(8,2.7,3.5);
   for(p=case_holes)translate([p[0],p[1],wall])ring(9,2.7,H-wall);
  }
  // 8mm DC cable entry; removable lid gives programming access.
  translate([-1,25,13])rotate([0,90,0])cylinder(d=8,h=wall+2);
  // Cooling slots are placed below lid and away from the cable entry.
  for(y=[55:8:95])translate([W-wall-1,y,25])cube([wall+2,3,8]);
 }
}
module lid(){
 difference(){
  union(){
   cube([W,D,wall]);
   translate([wall+.3,wall+.3,wall])difference(){cube([W-2*wall-.6,D-2*wall-.6,2]);translate([1.2,1.2,-.1])cube([W-2*wall-3,D-2*wall-3,3]);}
   // Blind screw bosses for reusable clamp strips. No adhesives needed.
   for(p=[[9,9],[116,9],[9,38],[116,38],[12,55],[50,55],[12,88],[50,88]])translate([p[0],p[1],wall])ring(6,2.5,(p[1]<40 ? 2.7 : 5.7));
   for(x=buttons)translate([x,125.25,wall])ring(13,8.6,3);
  }
  // Matrix windows are inset from 50.8x22.9 module edges.
  translate([12,14,-.1])cube([46.8,18.9,wall+.2]);
  translate([66,14,-.1])cube([46.8,18.9,wall+.2]);
  // TFT active area 24.9x14.0; module retained in 32x27.8 pocket.
  translate([18,63,-.1])cube([25.3,14.5,wall+.2]);
  for(p=case_holes)translate([p[0],p[1],-.1])cylinder(d=3.4,h=wall+.2);
  for(x=buttons)translate([x,125.25,-.1])cylinder(d=8.6,h=wall+6);
  for(x=[75,105])translate([x,73,-.1])cylinder(d=7.6,h=wall+.2);
  translate([105,101,-.1])cylinder(d=5.2,h=wall+.2);
  for(x=[100,103,106,109])translate([x,123,-.1])cylinder(d=1.5,h=wall+.2);
 }
}
module retainer(length=44){difference(){cube([length,10,2]);for(x=[3,length-3])translate([x,5,-.1])cylinder(d=3.4,h=2.2);}}
module plunger(){
 // switch top at z~12.0; assembled lid external surface z42.5.
 // 31.8mm total length gives 0.2mm rest clearance at cap top z44; validate with fit coupon.
 cylinder(d=8,h=7);translate([0,0,7])cylinder(d=11,h=1.5);
 translate([0,0,8.5])cylinder(d=4,h=23.3);
}
module coupon(){difference(){cube([60,20,2.5]);for(i=[0:4])translate([10+i*10,10,-.1])cylinder(d=7.8+i*.2,h=3);}}
if(part=="base")base();
if(part=="lid")lid();
if(part=="retainer")retainer();
if(part=="matrix_retainer")retainer(113);
if(part=="plunger")plunger();
if(part=="coupon")coupon();
if(part=="assembly"){
 color([.07,.12,.19])base();
 translate([0,0,62])color([.15,.23,.32])mirror([0,0,1])lid();
 // Dimensionally bounded module proxies, for interference review only.
 for(x=[10,64])translate([x,12,55])color([.1,.6,.3])cube([50.8,22.9,2.7]);
 translate([14,58,54])color([.1,.4,.55])cube([32,27.8,5.7]);
 translate([14,38,6])color([.08,.4,.25])cube([100,100,1.6]);
 for(x=buttons)translate([x,125.25,67])color([1,.5,.1])rotate([180,0,0])plunger();
}
