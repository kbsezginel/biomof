"""
IRMOF-1 Structure information. All indices start from 1.

LINKER:

      H       H
       \     /
O       C---C       O
 \     /     \     /
  C---C       C---C
 /     \     /     \
O       C---C       O
       /     \
      H       H
All linkers have been written from top to bottom and left to right.

NODE:

O    O
 \  /
  Zn
 /  \
O    O
"""
import yaml


with open('irmof1.yaml', 'r') as irmof1_yaml:
    irmof1 = yaml.load(irmof1_yaml)

node1 = [33, 35, 92, 115, 163]     # Zn, Zn, Zn, O, Zn
node2 = [38, 40, 96, 125, 209]     # Zn, Zn, Zn, O, Zn
node3 = [37, 39, 57, 122, 227]     # Zn, Zn, Zn, O, Zn
node4 = [34, 36, 118, 119, 145]    # Zn, Zn, Zn, O, Zn
node5 = [58, 59, 95, 126, 221]     # Zn, Zn, Zn, O, Zn
node6 = [93, 94, 116, 121, 157]    # Zn, Zn, Zn, O, Zn
node7 = [113, 114, 117, 120, 151]  # Zn, Zn, O, Zn, Zn
node8 = [123, 124, 127, 133, 215]  # Zn, O, Zn, Zn, Zn
nodes = [node1, node2, node3, node4, node5, node6, node7, node8]

linker1 = [179, 272, 180, 181, 183, 274, 182, 273, 255, 213, 256, 214, 212, 211, 254, 210]
linker2 = [236, 189, 190, 191, 238, 193, 237, 192, 149, 261, 150, 262, 148, 147, 146, 260]
linker3 = [228, 248, 229, 230, 232, 250, 231, 249, 276, 172, 277, 173, 171, 170, 275, 169]
linker4 = [266, 164, 165, 166, 268, 168, 267, 167, 202, 240, 203, 241, 201, 200, 199, 239]

linker5 = [336, 296, 297, 298, 338, 300, 337, 299, 304, 328, 305, 329, 303, 302, 301, 327]
linker6 = [316, 321, 317, 318, 320, 323, 319, 322, 340, 289, 341, 290, 288, 287, 339, 286]
linker7 = [333, 291, 292, 293, 335, 295, 334, 294, 309, 331, 310, 332, 308, 307, 306, 330]
linker8 = [311, 324, 312, 313, 315, 326, 314, 325, 343, 284, 344, 285, 283, 282, 342, 281]

linker9 = [245, 222, 223, 224, 247, 226, 246, 225, 177, 279, 178, 280, 176, 175, 174, 278]
linker10 = [158, 263, 159, 160, 162, 265, 161, 264, 243, 207, 244, 208, 206, 205, 242, 204]
linker11 = [269, 184, 185, 186, 271, 188, 270, 187, 219, 252, 220, 253, 218, 217, 216, 251]
linker12 = [194, 233, 195, 196, 198, 235, 197, 234, 258, 155, 259, 156, 154, 153, 257, 152]

linker13 = [410, 412, 417, 418, 420, 424, 419, 423, 108, 100, 109, 101, 99, 98, 107, 97]
linker14 = [356, 346, 365, 366, 384, 368, 383, 367, 73, 81, 74, 82, 72, 71, 70, 80]
linker15 = [349, 358, 385, 386, 388, 396, 387, 395, 55, 44, 56, 45, 43, 42, 54, 41]
linker16 = [354, 351, 369, 370, 380, 372, 379, 371, 63, 90, 64, 91, 62, 61, 60, 89]

linker17 = [142, 128, 129, 130, 144, 132, 143, 131, 4, 15, 5, 16, 3, 2, 1, 14]
linker18 = [347, 359, 397, 398, 400, 406, 399, 405, 31, 25, 32, 26, 24, 23, 30, 22]
linker19 = [134, 139, 135, 136, 138, 141, 137, 140, 12, 9, 13, 10, 8, 7, 11, 6]
linker20 = [348, 360, 401, 402, 404, 408, 403, 407, 28, 20, 29, 21, 19, 18, 27, 17]

linker21 = [350, 357, 389, 390, 392, 394, 391, 393, 52, 49, 53, 50, 48, 47, 51, 46]
linker22 = [352, 353, 373, 374, 376, 378, 375, 377, 87, 68, 88, 69, 67, 66, 86, 65]
linker23 = [411, 409, 413, 414, 422, 416, 421, 415, 105, 111, 106, 112, 104, 103, 102, 110]
linker24 = [345, 355, 361, 362, 364, 382, 363, 381, 84, 78, 85, 79, 77, 76, 83, 75]
linkers = [linker1, linker2, linker3, linker4, linker5, linker6, linker7, linker8, linker9, linker10,
           linker11, linker12, linker13, linker14, linker15, linker16, linker17, linker18, linker19,
           linker20, linker21, linker22, linker23, linker24]

# Make sure every atom is included in nodes and linkers
all_nodes = [i for s in nodes for i in s]
all_linkers = [i for s in linkers for i in s]
assert set(all_nodes + all_linkers) == set(range(1, len(irmof1['atoms']) + 1))

# Make sure there are no duplicates
assert len(all_nodes + all_linkers) == 424

# Make sure all linkers have same number of atoms
assert all(len(x) == 16 for x in linkers)

# Make sure all nodes have same number of atoms
assert all(len(x) == 5 for x in nodes)

irmof1['nodes'], irmof1['linkers'] = [], []
for n in nodes:
    irmof1['nodes'].append([i - 1 for i in n])
for l in linkers:
    irmof1['linkers'].append([i - 1 for i in l])

irmof1['cell'] = [25.832, 25.832, 25.832, 90, 90, 90]
irmof1['com'] = [12.916, 12.916, 12.916]
