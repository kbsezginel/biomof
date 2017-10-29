"""
Conformer search using OpenBabel.
"""
import os
import glob
import shutil
import argparse
import subprocess
from raspa_molecule import write_raspa_molecule
from raspa_input import write_raspa_file
from replace_lines import replace_lines
from write_soap import write_soap


parser = argparse.ArgumentParser(
    description="""
-------------------------------------------------
Molecular conformer search using OpenBabel.
-------------------------------------------------
    """,
    epilog="""
Example:
python obabel_onformer_search.py my_molecule.xyz

would generate maximum conformers of the given molecule and save them to obconf.xyz.
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter)

# Positional arguments
parser.add_argument('molecule', type=str, help='Molecule file to create conformers')

# Optional arguments
parser.add_argument('--conformers', '-c', default=None, type=int, metavar='',
                    help="Number of conformers (default: None)")
parser.add_argument('--algorithm', '-a', default='confab', type=str, metavar='',
                    help="Conformer generation algorithm (confab/genetic) (default: confab)")
parser.add_argument('--format', '-f', default='xyz', type=str, metavar='',
                    help="File format used to save molecule files (default: xyz)")
parser.add_argument('--output', '-o', default='obconf', type=str, metavar='',
                    help="File name to save conformer files (default: obconf)")
parser.add_argument('--verbose', '-v', action='store_true', default=True,
                    help="OpenBabel verbosity (default: True)")
parser.add_argument('--raspa', '-r', action='store_true', default=False,
                    help="create .def files for RASPA (default: False)")
parser.add_argument('--initialize', '-i', action='store_true', default=False,
                    help="Initialize files for RASPA (default: False)")
parser.add_argument('--unitcell', '-uc', metavar='', nargs=3, default=[1, 1, 1], type=int,
                    help="Unit cell packing for RASPA (default: 1 1 1)")
parser.add_argument('--source', '-s', metavar='', type=str, default=r'source',
                    help="Source files directory for RASPA (default: ./source)")
parser.add_argument('--soap', action='store_true', default=False,
                    help="create xyz files for SOAP (default: False)")

args = parser.parse_args()


def run_obabel(args):
    """ Run openbabel command line """
    opt_args = ''
    ob_exec = ['obabel', '%s' % args.molecule, '-O', '%s' % '%s.%s' % (args.output, args.format)]
    if args.algorithm == 'genetic':
        ob_exec += ['--conformer', '--writeconformers']
        if args.conformers is not None:
            ob_exec += ['--nconf', '%i' % args.conformers]
    elif args.algorithm == 'confab':
        ob_exec += ['--confab']
        if args.conformers is not None:
            ob_exec += ['--conf', '%i' % args.conformers]
    ob = subprocess.run(ob_exec, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = ob.stdout.decode()
    stderr = ob.stderr.decode()
    if args.verbose:
        print('Stdout:\n%s\nStderr:\n%s\n' % (stdout, stderr))


# Generate conformers ------------------------------------------------------------------------------
mol_name = os.path.splitext(os.path.basename(args.molecule))[0]
print('Generating conformers for %s...' % mol_name)
print('Algorithm: %s' % args.algorithm)
print('N. conformers: %s' % args.conformers)
print('Output file: %s.%s' % (args.output, args.format))
run_obabel(args)

print('Conformers saved to: %s.%s \n' % (args.output, args.format))

# TODO
"""
I need the coordinates for the input and output files to be able to create RASPA and SOAP inputs
An easy  way to get around that is to only use xyz format for RASPA and SOAP.
Other formats can still be used with OpenBabel but not the others.
Still, I need functions to read the xyz files which should not be hard.
Alternatively, I can also use Openbabel python API but that seems like too much work.

Need to figure out bonds!!!!!!!!
A quick way to get around that is to convet input file to a bonded format (ex: mol) using obabel
Read bonds from there and feed to RASPA
"""

# Generate RASPA molecule definition files ---------------------------------------------------------
if args.raspa:
    # Create .def files
    print('Creating molecule definition files for RASPA...')
    raspa_dir = '%s-conformers-RASPA' % mol_name
    if not os.path.isdir(raspa_dir):
        os.makedirs(raspa_dir)
    if args.initialize:
        source_dir = args.source
        source_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]
        cif_name = [os.path.splitext(os.path.basename(f))[0] for f in source_files if '.cif' in f][0]
        print('Initializing RASPA simulation files from: %s' % args.source)
    for conf_idx, conf in enumerate(conformers_mol):
        mol = conf
        molecule = {'elements': [str(atom.atomic_symbol) for atom in mol.atoms],
                    'coordinates': [list(atom.coordinates) for atom in mol.atoms],
                    'bonds': [[bond.atoms[0].index, bond.atoms[1].index] for bond in mol.bonds]}
        conf_name = '%s-%i' % (mol_name, conf_idx + 1)

        if args.initialize:
            raspa_conf_dir = os.path.join(raspa_dir, conf_name)
            if not os.path.isdir(raspa_conf_dir):
                os.makedirs(raspa_conf_dir)
            write_raspa_molecule(molecule, save=raspa_conf_dir, name=conf_name)
            input_file = os.path.join(raspa_conf_dir, 'simulation.input')
            write_raspa_file(input_file, cif_name, adsorbate=conf_name, uc=args.unitcell)
            for f in source_files:
                shutil.copy(f, raspa_conf_dir)
            job_name = ['#PBS -N %s-%s\n' % (cif_name, conf_name)]
            qsub_file = glob.glob(os.path.join(raspa_conf_dir, '*qsub*'))[0]  # Find qsub file
            replace_lines(qsub_file, [3], job_name)                       # Replace job name lines
        else:
            write_raspa_molecule(molecule, save=raspa_dir, name=conf_name)

    print('Done!\n')

if args.soap:
    write_soap(conformers_mol, mol_name, soap='soap.xyz', sort_key='header')

print('Finished!\n' + '-' * 40)
