Installation
============

We assume you are using a Debian-based Linux distribution.

Installing FAARE
----------------

It is highly recommended to install :program:`FAARE` in a Python virtual
environment. The procedure is shown below.

Create a Python virtual environment, activate it and install :program:`FAARE`.

.. code-block:: bash
    
    sudo apt install python3-virtualenv
    python3 -m venv .venv
    . .venv/bin/activate
    pip install faare

Installing Blender
------------------

.. code-block:: bash

    sudo apt install -y libxrender-dev libxxf86vm-dev libxfixes-dev libxi-dev libxkbcommon-dev libsm-dev 
    sudo mkdir /opt
    cd /opt
    sudo wget https://ftp.halifax.rwth-aachen.de/blender/release/Blender3.6/blender-3.6.7-linux-x64.tar.xz
    sudo tar -xvf blender-3.6.7-linux-x64.tar.xz
    sudo rm blender-3.6.7-linux-x64.tar.xz

Testing your installation
-------------------------

To test your installation, create a Python file with the following contents

.. code-block:: python

    import os
    from faare import Faare

    def main():
        fobj = Faare()

        fobj.boilerplate(os.path.join(ROOT, 'manifest.json'))

        # add atoms and position camera (bonds are found automatically)
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
        fobj.append_manifest(os.path.join(ROOT, 'manifest.json'), data)

        fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                            os.path.join(ROOT, 'methane.png'),
                            os.path.join(ROOT, 'log.txt'))

    if __name__ == '__main__':
        main()
