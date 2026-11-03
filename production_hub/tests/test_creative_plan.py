import json
import sys
import unittest
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.creative_plan import arrange_timeline, validate_plan, write_subtitles

class CreativePlanTests(unittest.TestCase):
    def setUp(self):
        path=Path(__file__).resolve().parents[1]/'examples/creative-comparison.json'
        self.examples=json.loads(path.read_text(encoding='utf8'))['variants']

    def test_all_examples_have_visuals_for_every_spoken_scene(self):
        for variant in self.examples:
            item=variant['item']
            plan=validate_plan(item['creative_plan'],item['scenes'])
            self.assertEqual(len(plan['scenes']),len(item['scenes']))

    def test_timeline_is_contiguous_and_exact_length(self):
        timing=arrange_timeline([2.2,4.1,3.0],[[],[],[]],['a','b','c'],20)
        self.assertEqual(timing[0]['from'],0)
        for left,right in zip(timing,timing[1:]):
            self.assertEqual(left['from']+left['duration'],right['from'])
        self.assertEqual(timing[-1]['from']+timing[-1]['duration'],600)
        self.assertTrue(all(item['duration']/30>=duration for item,duration in zip(timing,[2.2,4.1,3.])))

    def test_overlong_voice_is_rejected_without_truncation(self):
        with self.assertRaises(ValueError):
            arrange_timeline([8,9,10],[[],[],[]],['a','b','c'],20)

    def test_unknown_visual_or_incomplete_plan_rejected(self):
        item=self.examples[0]['item']
        item['creative_plan']['scenes'][0]['visual']='run arbitrary code'
        with self.assertRaises(ValueError):
            validate_plan(item['creative_plan'],item['scenes'])
        with self.assertRaises(ValueError):
            validate_plan({},item['scenes'])

    def test_subtitles_use_real_word_times_and_scene_offsets(self):
        with tempfile.TemporaryDirectory() as folder:
            words=[{'text':'साफ','start':.12,'end':.5},{'text':'जवाब','start':.6,'end':1.1}]
            write_subtitles([{'from':90,'words':words}],Path(folder))
            text=(Path(folder)/'subtitles.srt').read_text(encoding='utf8')
            self.assertIn('00:00:03,120 --> 00:00:04,100',text)
            self.assertIn('साफ जवाब',text)
            data=json.loads((Path(folder)/'words.json').read_text(encoding='utf8'))
            self.assertAlmostEqual(data[0]['start'],3.12)

if __name__=='__main__':
    unittest.main()
