import ase.io
import os
import numpy as np
import json
import subprocess
import shutil
from sys import platform
import tempfile

ROOT = os.path.dirname(__file__)

class Faare:
    def __init__(self):
        self.__executable = self.__find_blender()

    def boilerplate(self,
                   manifestout:str,
                   manifestin:str=None,
                   verbose:bool=False):

        manifest = self.__create_template(manifestout,
                                          manifestin,
                                          verbose)
        # store as json file
        with open(manifestout, 'w') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=4)

    def build_render_vasp(self, 
                          filename:str,
                          manifestout:str,
                          manifestin:str=None,
                          verbose:bool=False):
        
        manifest = self.__create_template(manifestout, manifestin, verbose)
        
        if not os.path.exists(filename):
            raise Exception('Invalid path: %s')
        
        # grab structure from file
        struc = ase.io.read(filename)

        # get atomic data from structure
        unitcell = np.array(struc.get_cell()[:])
        atoms = struc.get_chemical_symbols()
        positions = struc.get_positions()

        # encode unit cell and atoms in dictionary
        manifest['unitcell'] = [[unitcell[i,j]  for j in range(0,3)] for i in range(0,3)]
        manifest['atoms'] = []
        for a,p in zip(atoms, positions):
            manifest['atoms'].append((a, (p[0], p[1], p[2])))
        
        # auto-orient camera
        rt = unitcell @ np.array([1.0, 1.0, 0.0])
        scale = max(rt[0], rt[1])
        camera_location = unitcell @ np.array([0.5, 0.5, 0])
        camera_location += np.array([0, 0, 100])
        manifest["camera_location"] = [camera_location[i] for i in range(3)]
        manifest["camera_scale"] = scale * 1.1

        # overwrite any items from a manifest in file
        if manifestin is not None:
            with open(manifestin, 'r') as f:
                manifest.update(json.load(f))

        # store as json file
        with open(manifestout, 'w') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=4)

    def update_manifest(self,
                        manifestpath:str,
                        data:dict):
        
        # open file
        with open(manifestpath, 'r') as f:
            manifest = json.load(f)

        # append custom data to manifest
        for key,value in data.items():
            manifest[key] = value

        # re-store file
        with open(manifestpath, 'w') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=4)

    def execute_render(self, 
                       manifestpath:str,
                       pngpath:str,
                       logpath:str = None):
        self.__run_blender(manifestpath, pngpath, logpath)

    def __create_template(self,
                          manifestout:str,
                          manifestin:str=None,
                          verbose:bool=False):
        
        # start with default json files
        with open(os.path.join(ROOT, 'settings', 'settings.json'), 'r') as f:
            manifest = json.load(f)
        with open(os.path.join(ROOT, 'settings', 'atom_colors.json'), 'r') as f:
            manifest.update(json.load(f))
        with open(os.path.join(ROOT, 'settings', 'atom_radii.json'), 'r') as f:
            manifest.update(json.load(f))
        with open(os.path.join(ROOT, 'settings', 'bonds.json'), 'r') as f:
            manifest.update(json.load(f))

        return manifest  

    def __find_blender(self):
        """
        Find the Blender executable
        """
        if platform == "linux" or platform == "linux2":
            ex = '/opt/blender-3.6.7-linux-x64/blender' # preferred version and path
            if os.path.exists(ex):
                return ex

            print('Cannot find proper Blender executable. For Linux, please install Blender LTS 3.6.7 in /opt/blender-3.6.7-linux-x64/.')
            print('For more details on how to install Blender, please consult the instructions in the manual.')

            return None

        return None

    def __run_blender(self, 
                      manifestpath:str, 
                      pngfile:str,
                      logpath:str = None):
        # create temporary folder
        tempdir = tempfile.mkdtemp()

        # copy manifest file and rendering script
        shutil.copyfile(manifestpath, os.path.join(tempdir, 'manifest.json'))
        shutil.copyfile(os.path.join(ROOT, 'blender', 'blender_render_molecule.py'), 
                        os.path.join(tempdir, 'blender_render_molecule.py'))
        
        out = subprocess.check_output(
            ['ls'],
            cwd=tempdir
        )

        # run blender
        out = subprocess.check_output(
            [self.__executable, '-b', '-P', os.path.join(tempdir, 'blender_render_molecule.py')],
            cwd=tempdir
        )
    
        # copy result file
        shutil.copyfile(os.path.join(tempdir, 'render.png'), pngfile)

        # write log file
        if logpath is not None:
            log = []
            log.append("### START LOG ###")
            for line in out.splitlines():
                log.append(line.decode('utf-8'))
            log.append("### END LOG ###")

            with open(logpath, 'w') as f:
                for line in log:
                    f.write(line + '\n')
                f.close()

        # remove temporary folder
        shutil.rmtree(tempdir)

        return out