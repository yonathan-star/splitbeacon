import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'firmware'))
from core import *

class TimingTests(unittest.TestCase):
 def test_pause_excludes_wall_time(self):
  s=Session();s.toggle(0);s.tick(1234);s.toggle(2000);s.tick(9000)
  self.assertEqual(s.elapsed_ms,2000)
  s.toggle(10000);s.tick(11000);self.assertEqual(s.current_ms,3000)
 def test_lap_latches_target_and_rejects_double_press(self):
  s=Session(30);s.toggle(0);s.target_ms=40000
  self.assertTrue(s.lap(29000));self.assertEqual(s.laps,[(29000,30000)])
  self.assertEqual(s.lap_target_ms,40000);self.assertFalse(s.lap(29100))
 def test_single_cue_per_lap(self):
  s=Session(5);s.toggle(0);s.tick(5000)
  self.assertTrue(s.cue_due());self.assertFalse(s.cue_due())
  s.lap(6000);s.tick(11000);self.assertTrue(s.cue_due())
 def test_history_bound_and_reset(self):
  s=Session(5);s.toggle(0)
  for n in range(1,101):s.lap(n*5000)
  self.assertEqual(len(s.laps),64);s.reset(500001)
  self.assertFalse(s.running);self.assertEqual(s.laps,[]);self.assertEqual(s.current_ms,0)
 def test_debounce(self):
  d=Debounce();self.assertFalse(d.update(True,0));self.assertFalse(d.update(False,5))
  self.assertFalse(d.update(True,10));self.assertTrue(d.update(True,40));self.assertFalse(d.update(True,90))
 def test_matrix_permutation(self):
  self.assertEqual(sorted(matrix_index(x,y) for y in range(4) for x in range(16)),list(range(64)))
 def test_all_display_pages_clamp_every_channel(self):
  s=Session(5);s.toggle(0);s.tick(8000);s.lap(8000)
  for page in range(3):
   s.page=page
   for b in (-1,0,.2,1,100):
    f=matrix_frame(s,b);self.assertEqual(len(f),64)
    self.assertTrue(all(0<=c<=16 for rgb in f for c in rgb))
 def test_corrupt_saved_data(self):
  for x in (None,42,{},'x'):self.assertEqual(restore_laps(x),[])
  self.assertEqual(restore_laps([[2000,0],[3000,30000],['x',30000],[-1,10]]),[(3000,30000)])
 def test_adc_endpoints(self):
  self.assertEqual(target_from_adc(0),5);self.assertEqual(target_from_adc(65535),600)
  self.assertGreater(brightness_from_adc(0,0),0);self.assertEqual(brightness_from_adc(65535,65535),1)
 def test_stop_blocks_lap(self):
  s=Session();s.tick(10000);self.assertFalse(s.lap(10001));self.assertEqual(s.laps,[])
if __name__=='__main__':unittest.main(verbosity=2)
