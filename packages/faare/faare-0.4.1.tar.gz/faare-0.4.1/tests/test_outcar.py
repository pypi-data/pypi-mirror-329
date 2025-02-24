import unittest
import sys
import os

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT, '..'))

from faare import Faare

class TestOUTCAR(unittest.TestCase):

    def test_reading_outcar(self):
        fobj = Faare()
        fobj.build_render_vasp(os.path.join(ROOT, 'data', 'OUTCAR'),
                               os.path.join(ROOT, 'manifest.json'))

if __name__ == '__main__':
    unittest.main()
