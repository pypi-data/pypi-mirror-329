import os
import sys

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, '..'))

# load package
from faare import Faare

fobj = Faare()
fobj.build_render_vasp(os.path.join(ROOT, 'data', 'OUTCAR'),
                       os.path.join(ROOT, 'manifest.json'))

fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                    os.path.join(ROOT, 'vasp.png'))