import hashlib
from pathlib import Path
import tempfile
import unittest
from main import snapshot, compare

class Tests(unittest.TestCase):
    def test_hash_and_binary(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp,'a').write_bytes(b'\x00\xff')
            self.assertEqual(snapshot(tmp)['a'], hashlib.sha256(b'\x00\xff').hexdigest())
    def test_all_change_types(self):
        self.assertEqual(compare({'a':'1','b':'2'}, {'a':'3','c':'4'}), dict(added=['c'],removed=['b'],modified=['a']))
    def test_unchanged(self): self.assertEqual(compare({'a':'1'},{'a':'1'}),dict(added=[],removed=[],modified=[]))
    def test_missing_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError): snapshot(Path(tmp,'missing'))
    def test_nested_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp,'sub').mkdir(); Path(tmp,'sub','a').write_text('x')
            self.assertEqual(list(snapshot(tmp)), ['sub/a'])
