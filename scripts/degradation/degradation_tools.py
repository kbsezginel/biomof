import math
from copy import deepcopy
from irmof1 import irmof1
from file_io import write_xyz
from thermof.trajectory.tools import center_of_mass


MW = dict(PZA=123.113, RFP=822.94, NIZ=137.139, H2O=18.01528, NODE=277.5194, LINKER=164.115)


def pack_mof(atoms, coordinates, cell, packing):
    """
    Pack MOF

    Args:
    - atoms (list): list of elements -> ['O', 'C', 'H', ...]
    - coordinates (list): 2D list of atomic coordinates -> [[x1, y1, z1], ... , [xn, yn, zn]]
    - cell (list): Cell dimensions -> [a, b, c, alpha, beta, gamma]
    - packing (list): Packing of the cell -> [2, 2, 2]

    Returns:
    - dict: Packed MOF with atoms, coordinates and cell keys
    """
    v_cell = cell_vectors(cell)
    v_translation = translation_vectors(packing, v_cell)
    cell_coor = supercell_coordinates(v_translation, packing, v_cell, coordinates)
    packed_coordinates = [coor for cell in cell_coor for coor in cell]
    packed_atoms = atoms * (packing[0] * packing[1] * packing[2])
    packed_cell = [i * j for i, j in zip(cell[:3], packing)] + cell[3:6]
    return {'atoms': packed_atoms, 'coordinates': packed_coordinates, 'cell': packed_cell, 'pack': packing}


def cell_vectors(cell):
    """
    Calculate unit cell vectors for given cell dimensions -> [a, b, c, alpha, beta, gamma]
    """
    a, b, c = cell[:3]
    alpha, beta, gamma = [math.radians(i) for i in cell[3:6]]

    x_v = [a, 0, 0]
    y_v = [b * math.cos(gamma), b * math.sin(gamma), 0]
    z_v = [0.0] * 3
    z_v[0] = c * math.cos(beta)
    z_v[1] = (c * b * math.cos(alpha) - y_v[0] * z_v[0]) / y_v[1]
    z_v[2] = math.sqrt(c * c - z_v[0] * z_v[0] - z_v[1] * z_v[1])
    return [x_v, y_v, z_v]


def translation_vectors(packing_factor, cell_vectors):
    """
    Calculate translation vectors for given packing factor and uc vectors
    """
    packing_amount = []
    for x in range(packing_factor[0]):
        for y in range(packing_factor[1]):
            for z in range(packing_factor[2]):
                packing_amount.append([x, y, z])

    x_v, y_v, z_v = cell_vectors
    translation_vectors = []
    for pack in packing_amount:
        x_trans = x_v[0] * pack[0] + y_v[0] * pack[1] + z_v[0] * pack[2]
        y_trans = x_v[1] * pack[0] + y_v[1] * pack[1] + z_v[1] * pack[2]
        z_trans = x_v[2] * pack[0] + y_v[2] * pack[1] + z_v[2] * pack[2]
        translation_vectors.append([x_trans, y_trans, z_trans])
    return translation_vectors


def supercell_coordinates(translation_vectors, packing_factors, cell_vectors, coordinates):
    """
    Calculate packed coordinates for given:
    - translation vectors  - packing factor     - unit cell vectors    - atom coordinates
    """
    x_v, y_v, z_v = cell_vectors
    packed_coors = [[] for i in range(len(translation_vectors))]
    translation_factor = []
    origin_trans_vec = []
    for dim, factor in enumerate(packing_factors):
        translation_factor.append((factor - 1) / 2)
        origin_translation = (factor - 1) / 2 * x_v[dim] + (factor - 1) / 2 * y_v[dim]
        origin_translation += (factor - 1) / 2 * z_v[dim]
        origin_trans_vec.append(origin_translation)

    packing_index = 0
    for translation in translation_vectors:
        for coor in coordinates:
            x = coor[0] + translation[0] - origin_trans_vec[0]
            y = coor[1] + translation[1] - origin_trans_vec[1]
            z = coor[2] + translation[2] - origin_trans_vec[2]
            packed_coors[packing_index].append([x, y, z])
        packing_index += 1
    return packed_coors


def calculate_distance(p1, p2):
    """
    Calculate euclidian distance between two points.
    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def pack_linkers_nodes(packed_mof):
    """
    Calculate atomic indices for packed linkers and nodes.
    """
    n_cells = packed_mof['pack'][0] * packed_mof['pack'][1] * packed_mof['pack'][2]
    n_atoms = int(len(packed_mof['atoms']) / n_cells)
    single_mof = deepcopy(irmof1)
    packed_mof['linkers'], packed_mof['nodes'] = [], []
    for c in range(n_cells):
        for l in single_mof['linkers']:
            packed_mof['linkers'].append([i + c * n_atoms for i in l])
        for n in single_mof['nodes']:
            packed_mof['nodes'].append([i + c * n_atoms for i in n])
    return packed_mof


def delete_linkers_nodes(packed_mof, n_linkers_del, n_nodes_del):
    """
    Delete atoms that belong to selected linkers and nodes.

    Args:
        - packed_mof (dict): MOF atoms, coordinates
        - n_linkers_del (int): Number of linkers to delete
        - n_nodes_del (int): Number of nodes to delete
    """
    mof_com = center_of_mass(packed_mof['atoms'], packed_mof['coordinates'])
    # --- Calculate distance of linkers to MOF center of mass
    d_linkers = []
    for link in packed_mof['linkers']:
        link_coors = [packed_mof['coordinates'][i] for i in link]
        link_atoms = [packed_mof['atoms'][i] for i in link]
        l_com = center_of_mass(link_atoms, link_coors)
        d_linkers.append(calculate_distance(mof_com, l_com))
    # --- Calculate distance of nodes to MOF center of mass
    d_nodes = []
    for node in packed_mof['nodes']:
        node_coors = [packed_mof['coordinates'][i] for i in node]
        node_atoms = [packed_mof['atoms'][i] for i in node]
        n_com = (center_of_mass(node_atoms, node_coors))
        d_nodes.append(calculate_distance(mof_com, n_com))
    # --- Sort nodes and linkers according to their distance and get the indices
    sorted_node_idx = sorted(range(len(d_nodes)), key=lambda k: d_nodes[k], reverse=True)
    sorted_linker_idx = sorted(range(len(d_linkers)), key=lambda k: d_linkers[k], reverse=True)
    # --- Get all the linkers to be deleted
    linkers_del = [packed_mof['linkers'][l] for l in sorted_linker_idx[:n_linkers_del]]
    # --- Flatten to list to get all linker atoms to delete
    linker_atoms_del = [i for s in linkers_del for i in s]
    # --- Get all the nodes to be deleted
    nodes_del = [packed_mof['nodes'][n] for n in sorted_node_idx[:n_nodes_del]]
    # --- Flatten to list to get all linker atoms to delete
    node_atoms_del = [i for s in nodes_del for i in s]
    # --- Join list of atoms to delete
    all_atoms_del = linker_atoms_del + node_atoms_del
    # --- Select the atoms for degraded MOF
    degraded_mof = dict(atoms=[], coordinates=[])
    for i, (atom, coor) in enumerate(zip(packed_mof['atoms'], packed_mof['coordinates'])):
        if i not in all_atoms_del:
            degraded_mof['atoms'].append(atom)
            degraded_mof['coordinates'].append(coor)
    return degraded_mof


def degrade_mof(packed_mof, degradation, file_name):
    """
    Degrade packed MOF.

    Args:
        - packed_mpf (dict): MOF atoms, coordinates
        - degradation (tuple): Degradation fractions for linkers and nodes (d_l, d_n)
        - file_name (str): File name to save degradaded MOF coordinates
    """
    n_cells = packed_mof['pack'][0] * packed_mof['pack'][1] * packed_mof['pack'][2]
    n_linkers, n_nodes = len(irmof1['linkers']) * n_cells, len(irmof1['nodes']) * n_cells
    n_linkers_del, n_nodes_del = int(degradation[0] * n_linkers), int(degradation[1] * n_nodes)
    print('%i / %i linkers will be deleted...' % (n_linkers_del, n_linkers))
    print('%i / %i nodes will be deleted...' % (n_nodes_del, n_nodes))
    print('Packing linkers and nodes...')
    packed_mof = pack_linkers_nodes(packed_mof)
    print('Deleting linker and note atoms...')
    degraded_mof = delete_linkers_nodes(packed_mof, n_linkers_del, n_nodes_del)
    print('Writing to file...')
    write_xyz(file_name, degraded_mof['atoms'], degraded_mof['coordinates'])
    print('Done! Saved as -> %s' % file_name)
