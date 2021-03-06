# Drugs

## [Ethambutol - ETB][ethambutol-wiki]
Ethambutol (EMB, E) is a medication primarily used to treat tuberculosis. It is usually given in combination with other tuberculosis medications, such as isoniazid, rifampicin and pyrazinamide.

## [Isoniazid - NIZ][isoniazid-wiki]
Isoniazid, also known as isonicotinylhydrazide (INH), is an antibiotic used for the treatment of tuberculosis.

## [Rifampicin - RFP][rifampicin-wiki]
Rifampicin, also known as rifampin, is an antibiotic used to treat several types of bacterial infections. This includes tuberculosis, leprosy, and Legionnaire's disease.

## [Pyrazinamide - PZA][pyrazinamide-wiki]
Pyrazinamide is a medication used to treat tuberculosis.[2] For active tuberculosis it is often used together with rifampin, isoniazid, and either streptomycin or ethambutol.

## [Dimethyloxalylglycine - DMOG][dmog-pubchem]
Dimethyloxalylglycine is a cancer treatment drug, proposed to inhibit O<sub>2</sub> consumption in cancer cell lines HCT116 and PC12, well before activation of HIF pathways.

## [U6CL98Glp4](https://pubchem.ncbi.nlm.nih.gov/compound/cb-839#section=3D-Conformer)

## [Verteporfin](https://en.wikipedia.org/wiki/Verteporfin)

## Methods

All drug molecules are optimized using [ORCA][orca] with B3LYP basis set. Both experimental and ideal configurations for drugs have been initially considered when available. Eventually, the minimum energy configuration was selected for all drug molecules. Here the sources for initial structure and selected configuration have been provided:

|Drug       |Initial Structure       |Source      |
|:----------|:-----------------------|:-----------|
|ETB        |CCDC: [GEJHOT]          |Experimental|
|NIZ        |RSCB: [NIZ]             |Ideal       |
|RFP        |RSBP: [RFP]             |Experimental|
|PZA        |RSCB: [PZA]             |Experimental|
|DMOG       |Chemdraw                |Ideal       |
|U6CL98Glp4 |PubChem: [71577426]     |Ideal       |
|Verteporfin|Wikipedia [verteporfin] |Ideal       |

## Conformers

To test various configurations of drug molecules, different conformers are generated and drug uptake is calculated for each conformer.
[Conformer generation and drug uptake calculation tutorial.](https://kbsezginel.github.io/research/conformers-bokeh/)

------------------------------------------------------------------------
[ethambutol-wiki]: https://en.wikipedia.org/wiki/Ethambutol
[isoniazid-wiki]: https://en.wikipedia.org/wiki/Isoniazid
[rifampicin-wiki]: https://en.wikipedia.org/wiki/Rifampicin
[pyrazinamide-wiki]: https://en.wikipedia.org/wiki/Pyrazinamide
[dmog-pubchem]: https://pubchem.ncbi.nlm.nih.gov/substance/329798774
[orca]: https://orcaforum.cec.mpg.de/
[GEJHOT]: https://www.ccdc.cam.ac.uk/structures/Search?Ccdcid=gejhot
[NIZ]: https://www4.rcsb.org/ligand/NIZ
[PZA]: https://www4.rcsb.org/ligand/PZA
[RFP]: https://www4.rcsb.org/ligand/RFP
[Verteporfin-21106402]: http://www.chemspider.com/Chemical-Structure.21106402.html
[verteporfin]: https://chemapps.stolaf.edu/jmol/jmol.php?model=COC%28%3DO%29%5BC%40%40H%5D2C%28%3DC%5CC%3DC3%5Cc1cc6nc%28cc5nc%28cc4nc%28cc%28n1%29%5BC%40%5D23C%29C%28%2FC%29%3DC4%2FCCC%28%3DO%29OC%29c%28CCC%28O%29%3DO%29c5C%29C%28%2FC%3DC%29%3DC6%2FC%29%2FC%28%3DO%29OC
[71577426]: https://pubchem.ncbi.nlm.nih.gov/compound/cb-839#section=3D-Conformer
