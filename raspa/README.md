# [RASPA 2](https://github.com/WilmerLab/raspa2)
RASPA is a general purpose classical simulation package that can be used for the simulation of molecules in gases, fluids, zeolites, aluminosilicates, metal-organic frameworks, carbon nanotubes and external fields.

Installation and usage instructions can be found [here][raspa-tutorial].

## Drug Uptake
RASPA is used to estimate drug uptake in Metal-Organic Frameworks.

### Example

#### ZIF-8
As an example input files for simulation uptake of 5 different drugs in ZIF-8 are provided [here][zif8-example]. After installing RASPA and entering any of the drug directories under ZIF-8 RASPA simulation can be run as:
```bash
simulate simulation.input
```
Alternatively the qsub files can be used to submit jobs to a computer cluster.

-------------------------------------------------------------------------
[raspa-tutorial]: https://github.com/kbsezginel/chem-tools-tutorials/tree/master/RASPA
[zif8-example]: https://github.com/kbsezginel/biomof/tree/master/raspa/example/ZIF-8
