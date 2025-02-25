# Additional or Modified Rivet info

Staging area for new or modified rivet routines (and REF data, metadata) before they have moved into
a Rivet release.

If you have a new Rivet routine that you want to use locally with Contur, place the .cc, .plot, .info and .yoda(.gz) files in this directory, and it will be compiled when you next execute `make` for Contur. The same applies for any modified versions of existing Rivet files - they will override any files in your existing Rivet release. If you have the .cc file here, you will see a warning about a dulicated Rivet analysis - this is expected and harmless.

For a new Rivet routine, you will also need to add it to the Contur [analysis database](../DB/analysis.sql). See [here](../DB/README.md) for some help on that.

(this version for running with rivet 4.0.3)

## Contents and explanation:

- ATLAS_2019_I1764342 These routines have a bug fix for a scaling error. Should be included in rivet 4.0.4 and removed from here.

- ATLAS_2022_I2023464.plot presentational changes, should be propagated to Rivet (MR submitted)

- ATLAS_2023_I2648096.plot formatting and labelling fixes, should be propagated to Rivet (MR submitted)

- ATLAS_2023_I2690799.plot formatting and labelling fixes, should be propagated to Rivet (MR submitted)

- ATLAS_2024_I2768921.plot formatting and labelling fixes, should be propagated to Rivet (MR submitted)

- ATLAS_2024_I2765017.yoda.gz bug fix version for rmiss plots

- CMS_2022_I2080534.plot, CMS_2022_I2080534.yoda.gz removes the inclusive bin, which is not filled by rivet. Maybe should find a better way to do this in future by masking the bin or something. Or else propagate this to the rivet hepdata fixes?

- ATLAS_2023_I2690799.plot Plot file is missing in Rivet 4.0.3


   
