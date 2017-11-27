"""
Read RASPA output file for gas adsorption simulations.
"""
import os
import sys
import glob


def parse_output(data_file, verbose=False, save=False, loading='absolute'):
    """Parse output file for gas adsorption data.
    Args:
        data_file (str): path to RASPA simulation output file.
    Returns:
        results (dict): absolute and excess molar, gravimetric, and volumetric
            gas loadings, as well as energy of average, van der Waals, and
            Coulombic host-host, host-adsorbate, and adsorbate-adsorbate
            interactions.
    """
    with open(data_file) as ads_data:
        data_lines = ads_data.readlines()

    results = dict(ads={}, finished=False, warnings=[],
                   framework=os.path.basename(data_file).split('_')[1])
    for i, line in enumerate(data_lines):
        if 'Number of molecules:' in line:
            ads_start = i
        if 'Average Widom Rosenbluth factor:' in line:
            ads_end = i
        if 'Simulation finished' in line:
            results['finished'] = True
        if 'WARNING' in line:
            results['warnings'].append(line)
    if len(results['warnings']) > 0:
        print('%s - %i warning(s) found -> %s' %
              (results['name'], len(results['warnings']),
               results['warnings'][0].strip())) if verbose else None

    if results['finished']:
        ads_lines = data_lines[ads_start:ads_end]
        for i, line in enumerate(ads_lines):
            if 'Component' in line:
                comp_name = line.split()[2].replace('[', '').replace(']', '')
                results['ads'][comp_name] = {'id': line.split()[1]}
            if 'Average loading %s [molecules/unit cell]' % loading in line:
                results['ads'][comp_name]['mol/uc'] = float(ads_lines[i].split()[5])
                results['ads'][comp_name]['mol/kg'] = float(ads_lines[i + 1].split()[5])
                results['ads'][comp_name]['mg/g'] = float(ads_lines[i + 2].split()[5])
                results['ads'][comp_name]['cc/g'] = float(ads_lines[i + 3].split()[6])
                results['ads'][comp_name]['cc/cc'] = float(ads_lines[i + 4].split()[6])
        if verbose:
            units = ['mol/uc', 'mg/g', 'cc/cc']
            for component in results['ads']:
                print("%s\n%-15s\t%s\n%s" % ('=' * 30, '%s [%s]' % (component, results['ads'][component]['id']), loading, '-' * 30))
                for u in units:
                    print('%s\t\t%8.3f' % (u, results['ads'][component][u]))
            print('=' * 30)

        if save:
            import yaml
            with open('raspa_ads.yaml', 'w') as rads:
                yaml.dump(results, rads)
    else:
        print('Simulation not finished!') if verbose else None

    return results


if __name__ == "__main__":
    ads_path = glob.glob(os.path.join(sys.argv[1], 'Output', 'System_0', '*.data'))[0]
    if len(sys.argv) > 2 and sys.argv[2] == 's':
        parse_output(ads_path, verbose=True, save=True)
    else:
        parse_output(ads_path, verbose=True, save=False)
