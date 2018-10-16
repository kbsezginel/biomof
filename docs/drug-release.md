Drug release
============

Drug release can be approximated by calculating molecular diffusion. However, since degradation of
MOF is crucial for the release calculating bulk diffusion is not sufficient. Here I will decribe an
alternative approack to simulate drug release from MOFs.

Process Summary
---------------
1. Generate packed MOF coordinates (ex: 2x2x2)
2. Find linker atoms and calculate their distances to the center
3. Delete linkers according to their distance to center (far ones first) for given degradation rate
4. Add solvent (water) and drug molecules (packmol)
5. Add deleted linkers as solutes (???)
6. Convert xyz -> cif
7. Assign force field parameters
8. Generate LAMMPS input files
9. Run simulation
10. Calculate diffusion of drug molecules
11. Compare bulk and interface diffusion

Initially I started by separating IRMOF-1 into linkers and nodes.
I separated the Zn<sub>4</sub>O nodes and C<sub>8</sub>H<sub>4</sub>O<sub>4</sub> linkers by identifying their atom indices in a 111 packed IRMOF-1 xyz file.


Questions
---------

#### Degradation
I am not sure what is the best way to simulate degradation. I believe separating linkers and nodes
from the coordination bonds is a relatively good approach as those are likely to be the weaker bonds
however currently for the linkers at the boundaries I need to delete half of a linker that belongs
to one of the unit cells.

Another issue is with the packing of linkers and nodes. I am packing the degraded linkers and nodes
throughout the unit cell however I am not sure if those species would float like that individually.

Also, the degradation might happen in groups as well. Some part of the MOF can just break and
collectively diffuse together. Like a single unit cell can separate from multiple cells.

#### Packing drug molecues


#### Calculating diffusivity
