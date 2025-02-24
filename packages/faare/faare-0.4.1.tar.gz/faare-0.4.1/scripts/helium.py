import os
import sys

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, '..'))

from faare import Faare

# set root
ROOT = os.path.dirname(__file__)

# create object
fobj = Faare()

# create boilerplate manifest file
fobj.boilerplate(os.path.join(ROOT, 'manifest.json'))

# create a dictionary
data = {
    'atoms': [
        ('He', ( 0.00000,  0.00000,  0.00000)),
    ],
    'camera_scale': 5
}

# overwrite the manifest.json file with the dictionary contents
fobj.update_manifest(os.path.join(ROOT, 'manifest.json'), data)

# render system
fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                    os.path.join(ROOT, 'helium.png'))