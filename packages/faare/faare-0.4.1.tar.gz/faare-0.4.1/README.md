# Fully Agnostic Atomic Render Environment

[![pipeline status](https://gitlab.tue.nl/inorganic-materials-chemistry/faare/badges/master/pipeline.svg)](https://gitlab.tue.nl/inorganic-materials-chemistry/faare/-/commits/master)
[![PyPI](https://img.shields.io/pypi/v/faare?color=green)](https://pypi.org/project/faare/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

FAARE is a pure-Python package for automated rendering of VASP structures on headless
servers. Note that FAARE is designed for Linux Debian/Ubuntu and is not intended
to work on other operating systems.

## Installation

### Installing Blender

FAARE is designed to operate with Blender LTS 3.6 and assumes Blender is installed
in the /opt folder. Below, a brief set of instructions are provided to install
Blender.

```bash
sudo apt install -y libxrender-dev libxxf86vm-dev libxfixes-dev libxi-dev libxkbcommon-dev libsm-dev 
sudo mkdir /opt
cd /opt
sudo wget https://ftp.halifax.rwth-aachen.de/blender/release/Blender3.6/blender-3.6.7-linux-x64.tar.xz
sudo tar -xvf blender-3.6.7-linux-x64.tar.xz
sudo rm blender-3.6.7-linux-x64.tar.xz
```

### PyPi

First, make sure the required dependencies are installed

```bash
sudo apt install python3-venv
```

Next, create a virtual environment (compliant with PEP668) and activate it.

```bash
python3 -m venv ~/.venv
source ~/.venv/bin/activate
```

Finally, install `faare` in your virtual environment. The installation script
will automatically download all dependencies.

```bash
pip install faare
```

### Testing your installation

Create a new folder and place in the folder an `OUTCAR` file. Next, create a
`run.py` file that has the following contents

```python
from faare import Faare
import os

def main():
    ROOT = os.path.dirname(__file__)

    faare = Faare()
    faare.build_render(os.path.join(ROOT, 'OUTCAR'),
                       os.path.join(ROOT, 'manifest.json'))
    faare.execute_render(os.path.join(ROOT, 'manifest.json'),
                         os.path.join(ROOT, 'render.png'),
                         os.path.join(ROOT, 'renderlog.txt'))

if __name__ == '__main__':
    main()
```

Save the file and run it using `python run.py`. Three files should be written
in the folder:

* `render.png`: The picture of your system.
* `renderlog.txt`: A log file on the rendering procedure.
* `manifest.json`: A manifest file containing all the Blender settings.

### Updating your installation

Assuming you are logged into your Python virtual environment, run

```bash
pip install faare --upgrade
```

## Manual

See: https://faare-inorganic-materials-chemistry-6980722ff50f253a4f45dd9bd22.pages.tue.nl/