import os
import glob


def write_xyz(file_name, names, coors, header='mol'):
    """ Write given atomic coordinates to a file in xyz format """
    with open(file_name, 'w') as xyz_file:
        xyz_file.write(str(len(coors)) + '\n')
        xyz_file.write(header + '\n')
        format = '%s %.4f %.4f %.4f\n'
        for atom, coor in zip(names, coors):
            xyz_file.write(format % (atom, coor[0], coor[1], coor[2]))


def join_xyz(xyz_dir, output_file='soap.xyz', sort_key='header', rev=False):
    """
    Read, sort and join xyz file for SOAP.
    sort_key options: 'name' / 'n_atoms' / 'header'
    """
    xyz_files = glob.glob(os.path.join(xyz_dir, '*.xyz'))
    structures = {'lines': [], 'n_atoms': [], 'header': [], 'name': []}
    for xyz in xyz_files:
        with open(xyz, 'r') as f:
            lines = f.readlines()
        n_atoms = int(lines[0].strip())
        header = int(lines[1].strip()) if lines[1].strip().isdigit() else lines[1].strip()
        structures['lines'].append(lines)
        structures['header'].append(header)
        structures['name'].append(os.path.basename(xyz))
        structures['n_atoms'].append(n_atoms)

    # Sort by selected key ('name' / 'n_atoms' / 'info')
    sorted_lines = [x for (y, x) in sorted(zip(structures[sort_key], structures['lines']), reverse=rev)]
    sorted_files = [x for (y, x) in sorted(zip(structures[sort_key], xyz_files), reverse=rev)]
    soap_lines = [item for innerlist in sorted_lines for item in innerlist]
    xyz_list_file = os.path.join(xyz_dir, '..', 'xyz_list')
    with open(xyz_list_file, 'w') as xyz_list:
        for f in sorted_files:
            xyz_list.write('%s\n' % os.path.basename(f))

    # Write joined xyz file
    soap_file = os.path.join(xyz_dir, '..', output_file)
    with open(soap_file, 'w') as soap:
        for line in soap_lines:
            soap.write(line)


def write_soap(conformers, mol_name, soap='soap.xyz', sort_key='header'):
    """
    Write SOAP xyz file for given conformers
    """
    soap_dir = '%s-conformers-SOAP' % mol_name
    if not os.path.isdir(soap_dir):
        os.makedirs(soap_dir)
    xyz_dir = os.path.join(soap_dir, 'xyz')
    if not os.path.isdir(xyz_dir):
        os.makedirs(xyz_dir)
    print('Writing xyz files for SOAP to -> %s' % xyz_dir)
    for conf_idx, mol in enumerate(conformers):
        molecule = {'elements': [str(atom.atomic_symbol) for atom in mol.atoms],
                    'coordinates': [list(atom.coordinates) for atom in mol.atoms]}
        conf_name = '%s-%i' % (mol_name, conf_idx + 1)
        xyz_path = os.path.join(xyz_dir, '%s.xyz' % conf_name)
        write_xyz(xyz_path, molecule['elements'], molecule['coordinates'], header=str(conf_idx))

    print('Writing %s and ordered xyz list...\n' % soap)
    join_xyz(xyz_dir, output_file=soap, sort_key=sort_key)
