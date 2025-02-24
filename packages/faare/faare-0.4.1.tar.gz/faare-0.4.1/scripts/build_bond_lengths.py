import json
import os

ROOT = os.path.dirname(__file__)

def main():
    with open(os.path.join(ROOT, '..', 'faare', 'settings', 'atom_colors.json'), 'r') as f:
        atoms = json.load(f)['atom_colors'].keys()
    
    bond_distances = {}
    for i,a1 in enumerate(atoms):
        for j,a2 in enumerate(atoms):
            atomlist = [a1, a2]
            atomlist.sort()
            key = '%s-%s' % tuple(atomlist)
            
            if i <= 18 and j <= 18:
                distance = 1.5
            elif i <= 18 or j <= 18:
                distance = 2.5
            else:
                distance = 3.5
            
            if not key in bond_distances:
                bond_distances[key] = distance
       
    data = {'bond_distances' : bond_distances}
    with open(os.path.join(ROOT, '..', 'faare', 'settings', 'bonds.json'), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()