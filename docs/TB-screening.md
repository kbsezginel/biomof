# Simulation Details

### Drugs and MOF Structures

In order to identify MOFs with high drug loading capacity we performed an intial screening to calculate theoretical loading capacity for all three drugs and a database of 5109 MOFs.[1] Before calculating loading capacities MOF database was refined in three steps:

1. Removing known duplicate structures.[1, 2]
2. Selecting MOFs with following metals: Zn, Cu, Cd, Mn, Fe, Na, Mg, Ca, and Sr.
3. Geometric refinement by selecting top 500 MOFs with highest pore volume (Vp > 0.682).

The top 500 MOFs were used to calculate theoretical drug loading capacity using Grand Canonical Monte Carlo (GCMC) simulations.  The molecular structures for drug molecules were taken from DrugBank. [3] The structures were geometrically optimized with Density Functional Theory calculations using ORCA software package [4] at the BP86/def2-SVP level.

|Drug         | PDB | DrugBank |
|-------------|-----| ---------|
|Isoniazid    | NIZ | DB00951  |
|Pyrazinamide | PZA | DB00339  |
|Rifampicin   | RFP | DB01045  |
|Cycloserine  | -   | DB00260  |
|Moxifloxacin | -   | DB00218  |

After the loading capacities are calculated the top 50 MOFs were selected according to their average drug loading among the three drugs. These MOFs were manually investigated for toxicity and ease of synthesis. Consequently, IRMOF-1 was selected as it was found to be the less toxic, easy to synthesize and stable.


### Theoretical Drug Loading Capacity

The theoretical drug loading capacity is calculated using Grand Canonical Monte Carlo (GCMC) simulations with RASPA software package. Both drug molecule atoms and framework atoms were kept rigid during simulations. Universal Force Field (UFF) parameters were used to calculate interatomic energies with a Lennard Jones potential and a cut-off radius of 12 A. 5000 initialization cycles followed by 10000 production cycles were used for GCMC simulations at 298 K. In each MC cycle translation, rotation, reinsertions, and swap moves were used with equal probability. Pressure was adjusted to 100 bar to approximate maximum loading possible. Framework unit cells were extended in each direction to exceed distance of 2 * Rc.

### Drug Release Kinetics

#### References

[1]: Chung, Yongchul G., et al. "Computation-ready, experimental metal–organic frameworks: A tool to enable high-throughput screening of nanoporous crystals." Chemistry of Materials 26.21 (2014): 6185-6192.

[2]: Sezginel, K. B., T. Feng, and C. E. Wilmer. "Discovery of hypothetical hetero-interpenetrated MOFs with arbitrarily dissimilar topologies and unit cell shapes." CrystEngComm 19.31 (2017): 4497-4504.

[3]: Wishart, David S., et al. "DrugBank 5.0: a major update to the DrugBank database for 2018." Nucleic Acids Research (2017).

[4]: Neese, Frank. "The ORCA program system." Wiley Interdisciplinary Reviews: Computational Molecular Science 2.1 (2012): 73-78.

[5]: Dubbeldam, David, et al. "RASPA: molecular simulation software for adsorption and diffusion in flexible nanoporous materials." Molecular Simulation 42.2 (2016): 81-101.
