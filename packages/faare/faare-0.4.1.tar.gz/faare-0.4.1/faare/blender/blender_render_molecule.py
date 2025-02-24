import bpy
import numpy as np
import os
import time
import json

#
# IMPORTANT
#
# Do not run this script natively. This script is meant to be run in Blender
# via one of the call routines
#

with open(os.path.join(os.path.dirname(__file__), 'manifest.json')) as f:
    manifest = json.load(f)

def main():
    # set the scene
    set_environment(manifest)

    # read molecule file and load it
    create_atoms(manifest['atoms'])
    create_bonds(manifest['atoms'])

    # render the scene
    render_scene(manifest['png_output'])

def create_atoms(mol):
    """
    Create atoms
    """
    for i,at in enumerate(mol):

        # grab scale from defaults
        scale = manifest['atom_radii'][str(at[0])]

        # check if there is any override present
        if 'radius_overrides' in manifest.keys():
            for override in manifest['radius_overrides']:
                if override.startswith(at[0]):
                    pieces = override.split('/')
                    if ((i+1) >= int(pieces[1]) and (i+1) <= int(pieces[2])) or \
                        int(pieces[1]) == int(pieces[2]) == 0:
                        scale = float(pieces[3])

        bpy.ops.surface.primitive_nurbs_surface_sphere_add(
            radius=scale,
            enter_editmode=False,
            align='WORLD',
            location=at[1])
        obj = bpy.context.view_layer.objects.active
        obj.name = "atom-%s-%03i" % (at[0],i)
        bpy.ops.object.shade_smooth()

        # set a material
        mat = create_material(at[0], manifest['atom_colors'][str(at[0])])

        # if an override is present, overwrite the material
        if 'color_overrides' in manifest.keys():
            for override in manifest['color_overrides']:
                if override.startswith(at[0]):
                    pieces = override.split('/')
                    if ((i+1) >= int(pieces[1]) and (i+1) <= int(pieces[2])) or \
                        int(pieces[1]) == int(pieces[2]) == 0:
                        mat = create_material(at[0] + '-%i' % (i+1), pieces[3], override=True)
        
        obj.data.materials.append(mat)

def create_bonds(mol):
    """
    Create bonds between atoms
    """
    # set default orientation of bonds (fixed!)
    z = np.array([0,0,1])

    # add new bonds material if it does not yet exist
    matbond = create_material('bond', manifest['bond_color'])

    for i,at1 in enumerate(mol):
        r1 = np.array(at1[1])
        for j,at2 in enumerate(mol[i+1:]):
            r2 = np.array(at2[1])
            dist = np.linalg.norm(r2 - r1)

            # construct bond pair
            atomelements = [at1[0], at2[0]]
            atomelements.sort()

            # only create a bond if the distance is less than 1.5 A
            if dist < manifest['bond_distances']['%s-%s' % tuple(atomelements)]:
                axis = np.cross(z,r2-r1)
                if np.linalg.norm(axis) < 1e-5:
                    axis = np.array([0,0,1])
                    angle = 0.0
                else:
                    axis /= np.linalg.norm(axis)
                    angle = np.arccos(np.dot(r2-r1,z)/dist)

                bpy.ops.surface.primitive_nurbs_surface_cylinder_add(
                    enter_editmode=False,
                    align='WORLD',
                    location=tuple((r1 + r2) / 2)
                )

                obj = bpy.context.view_layer.objects.active
                thickness = min(manifest['atom_radii'][at1[0]], manifest['atom_radii'][at2[0]]) / 2
                obj.scale = (thickness, thickness, dist/2)
                obj.rotation_mode = 'AXIS_ANGLE'
                obj.rotation_axis_angle = (angle, axis[0], axis[1], axis[2])

                obj.name = "bond-%s-%03i-%s-%03i" % (at1[0],i,at2[0],j)
                bpy.ops.object.shade_smooth()
                obj.data.materials.append(matbond)

def set_environment(settings):
    """
    Specify canvas size, remove default objects, reset positions of
    camera and light, define film and set background
    """
    enable_gpus("CUDA")
    print('Set render engine to: CYCLES')
    bpy.context.scene.render.engine = 'CYCLES'
    print('Set rendering device to GPU')
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.render.resolution_x = settings['resolution']
    bpy.context.scene.render.resolution_y = settings['resolution']
    print('Setting resolution to: ', settings['resolution'])
    bpy.context.scene.cycles.samples = manifest['samples']
    bpy.context.scene.cycles.tile_size = settings['resolution'] // 2

    # remove cube
    if 'Cube' in bpy.data.objects:
        o = bpy.data.objects['Cube']
        bpy.data.objects.remove(o, do_unlink=True)

    # set camera into default position
    bpy.data.objects['Camera'].location = tuple(settings['camera_location'])
    bpy.data.objects['Camera'].rotation_euler = tuple(settings['camera_rotation'])
    bpy.data.objects['Camera'].data.clip_end = 1000
    bpy.data.objects['Camera'].data.type = 'ORTHO'
    bpy.data.objects['Camera'].data.ortho_scale = settings['camera_scale']

    # set lights
    bpy.data.objects['Light'].data.type = 'AREA'
    bpy.data.objects['Light'].data.energy = 1e4
    bpy.data.objects['Light'].location = (-10,10,10)
    bpy.data.objects['Light'].rotation_euler = tuple(np.radians([55, 0, 225]))
    bpy.data.objects['Light'].data.shape = 'DISK'
    bpy.data.objects['Light'].data.size = 10

    # set film
    bpy.context.scene.render.film_transparent = True

    # set background
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1,1,1,1)
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 1

def create_material(name, color, override=False):
    """
    Build a new material
    """
    # early exit if material already exists and no override is present
    if name in bpy.data.materials:
        if not override:
            return bpy.data.materials[name]
        else:
            bpy.data.materials.remove(bpy.data.materials[name])

    mat = bpy.data.materials.new(name)
    mat.use_nodes = True

    matsettings = {
        'Base Color': hex2rgbtuple(color),
        'Subsurface': manifest['default_material_settings']['Subsurface'],
        'Subsurface Radius': manifest['default_material_settings']['Subsurface Radius'],
        'Subsurface Color': hex2rgbtuple(manifest['default_material_settings']['Subsurface Color']),
        'Metallic': manifest['default_material_settings']['Metallic'],
        'Roughness': manifest['default_material_settings']['Roughness'],
        'Alpha': manifest['default_material_settings']['Alpha']
    }

    for key,target in mat.node_tree.nodes["Principled BSDF"].inputs.items():
        for refkey,value in matsettings.items():
            if key == refkey:
                target.default_value = value

    return mat

def render_scene(outputfile, samples=512):
    """
    Render the scene
    """
    bpy.context.scene.cycles.samples = samples

    print('Start render')
    start = time.time()
    bpy.data.scenes['Scene'].render.filepath = outputfile
    bpy.ops.render.render(write_still=True)
    end = time.time()
    print('Finished rendering frame in %.1f seconds' % (end - start))

def enable_gpus(device_type, use_cpus=False):
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons["cycles"].preferences
    cycles_preferences.refresh_devices()
    devices = cycles_preferences.devices

    if not devices:
        raise RuntimeError("Unsupported device type")

    activated_gpus = []
    for device in devices:
        if device.type == "CPU":
            device.use = use_cpus
        else:
            device.use = True
            activated_gpus.append(device.name)
            print('Activated GPU: ', device.name)

    cycles_preferences.compute_device_type = device_type
    bpy.context.scene.cycles.device = "GPU"

    return activated_gpus

def hex2rgbtuple(hexcode):
    """
    Convert 6-digit color hexcode to a tuple of floats
    """
    hexcode += "FF"
    hextuple = tuple([int(hexcode[i:i+2], 16)/255.0 for i in [1,3,5,7]])

    return tuple([color_srgb_to_scene_linear(c) for c in hextuple])

def color_srgb_to_scene_linear(c):
    """
    Convert RGB to sRGB
    """
    if c < 0.04045:
        return 0.0 if c < 0.0 else c * (1.0 / 12.92)
    else:
        return ((c + 0.055) * (1.0 / 1.055)) ** 2.4

if __name__ == '__main__':
    main()