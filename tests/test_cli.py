import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = str(Path(__file__).resolve().parents[1] / 'main.py')

class CliTests(unittest.TestCase):
    def test_baseline_change_and_exclusive_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp,'watched'); root.mkdir()
            file=root/'config'; file.write_text('before')
            manifest=Path(tmp,'baseline.json')
            baseline=subprocess.run([sys.executable,SCRIPT,'baseline',str(root),str(manifest)],capture_output=True,text=True)
            self.assertEqual(baseline.returncode,0,baseline.stderr)
            repeated=subprocess.run([sys.executable,SCRIPT,'baseline',str(root),str(manifest)],capture_output=True,text=True)
            self.assertEqual(repeated.returncode,2)
            file.write_text('after')
            checked=subprocess.run([sys.executable,SCRIPT,'check',str(root),str(manifest)],capture_output=True,text=True)
            self.assertEqual(checked.returncode,1,checked.stderr)
            self.assertEqual(json.loads(checked.stdout)['modified'],['config'])

    def test_manifest_inside_root_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=subprocess.run([sys.executable,SCRIPT,'baseline',tmp,str(Path(tmp,'baseline.json'))],capture_output=True,text=True)
            self.assertEqual(result.returncode,2)
            self.assertFalse(Path(tmp,'baseline.json').exists())
