Usage
=====

Basics
------

To produce an image of your system using Blender, the first task is to
produce a :code:`manifest.json` file. In the most simple situation, this
corresponds to running a boilerplate method which copies the default settings
to the working directory.

.. code-block:: python

    # load modules
    from faare import Faare
    import os

    # set root
    ROOT = os.path.dirname(__file__)

    # create object
    fobj = Faare()

    # create boilerplate manifest file
    fobj.boilerplate(os.path.join(ROOT, 'manifest.json'))

.. caution::

    When creating a :code:`Faare` object, use a name like :code:`fobj` for the
    variable and not something like :code:`faare` to avoid overlap with the
    module name.

In principle, this :code:`manifest.json` file can already be rendered, but we
have not added any atoms to the systems, so the result would be rather boring.
Let us start simple and add a He atom.

.. code-block:: python

    # load modules
    from faare import Faare
    import os

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
    }

    # update manifest
    fobj.update_manifest(os.path.join(ROOT, 'manifest.json'), data)

    # render system
    fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                        os.path.join(ROOT, 'helium.png'))

Executing the above script will show us a quite lonely Helium atom (see image
below).

.. image:: /_static/img/usage/basics/helium_01.png
    :width: 50%
    :align: center

Camera settings
---------------

You will note that the He atom is pretty small. This is because the
default camera **scale** is set to 10. Let us therefore modify the
:code:`camera_scale` directive and decrease its value to zoom in on the He atom.

.. code-block:: python

    # load modules
    from faare import Faare
    import os

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

    # update manifest
    fobj.update_manifest(os.path.join(ROOT, 'manifest.json'), data)

    # render system
    fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                        os.path.join(ROOT, 'helium.png'))

.. image:: /_static/img/usage/basics/helium_02.png
    :width: 50%
    :align: center

Besides changing the camera scale, we can also change its location. Changing
the location will not have a huge impact when rendering a single atom, so let
us look into the methane molecule.

We will start by rendering methane using a camera position located at the
positive :code:`z`-axis. By default, the camera is looking down, so no further
adjustments are necessary.

.. code-block:: python

    # load modules
    from faare import Faare
    import os

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
        'camera_location': (0.0, 0.0, 10.0),
        'camera_scale': 5.0,
    }

    # update manifest
    fobj.update_manifest(os.path.join(ROOT, 'manifest.json'), data)

    # render system
    fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                        os.path.join(ROOT, 'methane.png'))

Executing the above script yields the following result.

.. image:: /_static/img/usage/basics/methane_01.png
    :width: 50%
    :align: center

Let us now modify the camera such that it is located at the positive
:code:`x`-axis. Since the default orientation of the camera is looking down,
i.e. in the direction of the negative :code:`z`-axis, we would not see an
image if we would make no further adjustments. In order to observe the methane
molecule, we also need to **rotate** the camera. Rotation instructions are given
by means of [Euler angles](https://en.wikipedia.org/wiki/Euler_angles). To
re-orient the camera such that the methane molecule is in plain view, we have
to rotate the camera by :math:`\pi/2` radians over the :code:`x`-axis after which
we need to rotate the camera by :math:`\pi/2` over the :code:`z`-axis.

.. caution::

    Note that inclusion of :code:`import numpy as np` in the code below.

.. code-block:: python

    # load modules
    from faare import Faare
    import numpy as np
    import os

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
        'camera_rotation': (np.pi/4, 0.0, np.pi/4)
    }

    # update manifest
    fobj.update_manifest(os.path.join(ROOT, 'manifest.json'), data)

    # render system
    fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                        os.path.join(ROOT, 'methane.png'))

.. image:: /_static/img/usage/basics/methane_02.png
    :width: 50%
    :align: center

Rendering settings
------------------

By default, a picture of 1024x1024px is created with a transparent background
and using 1024 samples. Depending on your use case, this might either be too
much or too little. We can of course adjust it using the keywords
:code:`resolution` and :code:`samples`. For example, the code below would
reduce the number of samples and the resolution.

.. code-block::
    
    data = {
        'resolution': 512,
        'samples': 512
    }
    fobj.append_manifest(os.path.join(ROOT, 'manifest.json'), data)

Changing atomic attributes
--------------------------

We can change the color and size of the atoms using the concept
of **overrides**. These overrides are read right before the atom is placed
in the scene. The overrides are supplied to the program using a series of
strings where each string is a 4-tuple of values separated by :code:`/`. This
is best explained using a few examples.

To change all carbon atoms in the scene with atom ids in between 
2 and 42 (inclusive), you would use :code:`C/2/42/#FF0000`.
The color values are always written in hexadecimal notation and the :code:`#`
is mandatory. There is also the option to use :code:`/0/0/` as a wildcard to
override the color of **all** carbon atoms in the scene: :code:`C/0/0/#FF0000`.
Finally, note that overrides are written in consecutive fashion and one override
can be overwritten by a later override. It is thus possible to first change the
color of all atoms of a certain element and thereafter change the color back 
for a few atoms. (examples of this will follow suit)

Besides changing the color of atoms, we can also change the radius of the atoms.
The process is fairly similar to changing colors, but instead of supplying a
hexcode string, we need to supply a single scalar value. For example, to change
the radius of all H atoms with atom indices 1 to 5 (inclusive), we would use
:code:`H/0/0/0.5`.

.. important::

    :program:`FAARE` uses one-based counting for indexing atoms.

In the example below, we will change the color of all carbon atoms to red and
of all hydrogen atoms to green. Furthermore, the radius of the carbon atoms
is increased to 0.75 angstrom and for the hydrogen atoms to 0.4 angstrom.

.. code-block:: python

    # load modules
    from faare import Faare
    import numpy as np
    import os

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
        'camera_scale': 5.0,
        'color_overrides': [
            'C/0/0/#FF0000',
            'H/0/0/#00FF00',
        ],
        'radius_overrides': [
            'C/0/0/0.75',
            'H/0/0/0.4',
        ]
    }
    fobj.update_manifest(os.path.join(ROOT, 'manifest.json'), data)

    # render system
    fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                        os.path.join(ROOT, 'methane.png'))

.. image:: /_static/img/usage/basics/methane_03.png
    :width: 50%
    :align: center

Let us repeat upon the above procedure and show how overrides can be overwritten
by newer overrides. Consider the script below where we first change the color
of all hydrogen atoms to green after which we change (update) the color of 
the first hydrogen atom (with index 2) to blue.

.. code-block:: python

    # load modules
    from faare import Faare
    import numpy as np
    import os

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
        'camera_scale': 5.0,
        'color_overrides': [
            'C/0/0/#FF0000',
            'H/0/0/#00FF00',
            'H/2/2/#0000FF',
        ],
        'radius_overrides': [
            'C/0/0/0.75',
            'H/0/0/0.4',
        ]
    }
    fobj.update_manifest(os.path.join(ROOT, 'manifest.json'), data)

    # render system
    fobj.execute_render(os.path.join(ROOT, 'manifest.json'),
                        os.path.join(ROOT, 'methane.png'))

.. image:: /_static/img/usage/basics/methane_04.png
    :width: 50%
    :align: center

