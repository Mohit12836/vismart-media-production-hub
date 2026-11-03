import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.remotion_engine import render_remotion_composition

class LegacyRenderTests(unittest.TestCase):
    def test_render_runs_node_directly_without_an_interactive_shell(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'video.mp4'
            output.write_bytes(b'x' * 12000)
            with patch('engine.remotion_engine.subprocess.run', return_value=subprocess.CompletedProcess([], 0, '', '')) as run:
                self.assertTrue(render_remotion_composition('src/index.ts', 'SilentKinetic', str(output), folder))
            args, kwargs = run.call_args
            self.assertEqual(args[0][0], 'node')
            self.assertTrue(args[0][1].endswith('remotion-cli.js'))
            self.assertFalse(kwargs.get('shell', False))
            self.assertEqual(kwargs['timeout'], 7200)

    def test_old_output_does_not_hide_failed_render(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'video.mp4'
            output.write_bytes(b'x' * 12000)
            with patch('engine.remotion_engine.subprocess.run', return_value=subprocess.CompletedProcess([], 1, '', 'renderer failed')):
                self.assertFalse(render_remotion_composition('src/index.ts', 'SilentKinetic', str(output), folder))

if __name__ == '__main__':
    unittest.main()
