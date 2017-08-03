# BioMOF Results

## MOF-5 and GWMOF-8 (PARHEW)
This initial test was performed to estimate drug uptakes in a common MOF (MOF-5) and a calcium adipic acid MOF, GWMOF-8 (CCDC: PARHEW). GWMOF-8 has the largest pore among calcium MOFs in CoRE database. However, it is not able to load RFP due to its 3D pore structure.

![alt_text][MOF-5-PARHEW]

## Initial Screening of [CoRE Database][CoRE]
An initial screening of ~80 MOFs were performed using MOFs in [CoRE database][CoRE]. MOFs with Ca, Na, Mg, Sr, and K metal centers, void fraction bigger than 0.3, and largest pore bigger than 6 Å were selected.
Overall DMOG, PZA, and NIZ uptakes were generally quite high followed by ETB and RFP. Around 65 of the MOFs weren't able to uptake any RFP since its a relatively large molecule.

![alt_text][screening-1]

## ZIF-8
Drug uptakes have been calculated at 298 K for ZIF-8 using RASPA to estimate maximum drug uptake capacity:

![alt_text][ZIF-8-uptake]

## DMOG Conformers
Initially 100 conformers for DMOG have been generated using CSD Python API. Then RASPA *.def* files and simulation input files were generated using the command line interface given in this repository. Below, 50 of these conformers are shown:

![alt_text][DMOG-conformers]

DMOG uptakes in IRMOF-1 and RUFMUA were calculated for all these conformers:

**IRMOF-1**

![alt_text][IRMOF-1-DMOG]

**RUFMUA**

![alt_text][RUFMUA-DMOG]

-------------------------------------------------------------------------
[ZIF-8-uptake]: https://goo.gl/Qt5ZVF
[screening-1]: https://goo.gl/AAv5Zf
[MOF-5-PARHEW]: https://goo.gl/r7jPNd
[CoRE]: http://pubs.acs.org/doi/abs/10.1021/cm502594j
[DMOG-conformers]: https://goo.gl/FyDE9a
[IRMOF-1-DMOG]: https://goo.gl/odopfU
[RUFMUA-DMOG]: https://goo.gl/muRpdv
