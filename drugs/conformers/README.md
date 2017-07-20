# Conformer Search

A molecular conformer search is performed to *simulate* molecule flexibility. By simulation adsorption of many conformers and averaging a flexible adsorption simulation can be emulated.

## CSD Python API

To search for conformers [CSD Python API] is used. The [CSD conformer tutorial][CSD Conformer Tutorial] is used as an example to generate given number of conformers and perform force field minimisation. More information can be found in [CSD conformer API][CSD Conformer API].

## OpenBabel Conformer Search

Alternatively conformer search can also be performed using OpenBabel genetic algorithm or Confab.

[OpenBabel Multiple Conformers](http://open-babel.readthedocs.io/en/latest/3DStructureGen/multipleconformers.html)

-----------------------------------------------------------------------
[CSD Python API]: https://downloads.ccdc.cam.ac.uk/documentation/API/
[CSD Conformer Tutorial]: https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_docs/conformer.html
[CSD Conformer API]: https://downloads.ccdc.cam.ac.uk/documentation/API/modules/conformer_api.html
