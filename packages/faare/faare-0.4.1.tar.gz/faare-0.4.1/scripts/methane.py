import os
import sys

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, '..'))

from faare import Faare
import faare

def main():
    fobj = Faare()
    print(faare.__version__)

    fobj.boilerplate(os.path.join(ROOT, 'manifest.json'))

    data = {
        'atoms': [
            ('C', ( 0.00000,  0.00000,  0.00000)),
            ('H', ( 0.00000,  0.00000,  1.08900)),
            ('H', ( 1.02672,  0.00000, -0.36300)),
            ('H', (-0.51336, -0.88916, -0.36300)),
            ('H', (-0.51336,  0.88916, -0.36300)),
        ],
        'camera_location': (0.0, 0.0, 10.0),
        'camera_scale': 5.0,
        'resolution': 512,
        'samples': 512
    }
    fobj.update_manifest(os.path.join(ROOT, 'manifest.json'), data)

    fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                        os.path.join(ROOT, 'methane.png'),
                        os.path.join(ROOT, 'log.txt'))
    
    # overwrite some colors
    data = {
        'color_overrides': [
            'C/0/0/#FF0000',
            'H/0/0/#00FF00',
        ]
    }
    fobj.update_manifest(os.path.join(ROOT, 'manifest.json'), data)
    fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                        os.path.join(ROOT, 'methane_colorfull.png'),
                        os.path.join(ROOT, 'log.txt'))

if __name__ == '__main__':
    main()
