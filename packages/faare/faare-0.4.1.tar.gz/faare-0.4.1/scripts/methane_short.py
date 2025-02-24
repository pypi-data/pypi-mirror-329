import os
import sys

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, '..'))

# load package
from faare import Faare
import numpy as np

# set root
ROOT = os.path.dirname(__file__)

# create object
fobj = Faare()

# create boilerplate manifest file
fobj.boilerplate(os.path.join(ROOT, 'manifest.json'))

# create a dictionary
data = {
    'atoms': [
        ('C', ( 0.00000,  0.00000,  0.00000)),
        ('H', ( 0.00000,  0.00000,  1.08900)),
        ('H', ( 1.02672,  0.00000, -0.36300)),
        ('H', (-0.51336, -0.88916, -0.36300)),
        ('H', (-0.51336,  0.88916, -0.36300)),
    ],
    'camera_location': (10.0, 0.0, 0.0),
    'camera_scale': 5.0,
    'camera_rotation': (np.pi/2, 0.0, np.pi/2)
}
fobj.update_manifest(os.path.join(ROOT, 'manifest.json'), data)

# render system
fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                    os.path.join(ROOT, 'methane.png'))