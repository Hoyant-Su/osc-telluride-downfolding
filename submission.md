# Discovery: canonical downfolding of TiTe2 and two PdTe2 polytypes

Author: Haoyang Su, Fudan University and Shanghai Innovation Institute. GitHub: [Hoyant-Su](https://github.com/Hoyant-Su). Contact: 240107100018@sii.edu.cn.

I propose three C2DB materials for the Discovery track: OSC-00353 (`1TiTe2-1`), OSC-00789 (`1PdTe2-1`), and OSC-00790 (`1PdTe2-2`). The contribution contains completed Quantum ESPRESSO calculations, their eigenvalues and occupations, and reproducible postprocessing. These materials were outside the active set when selected on October 30, 2026.

The scientific question is how the challenge's fixed downfolding protocol represents metallic tellurides with different band fillings and coordination. The two PdTe2 polytypes provide a comparison at fixed composition. TiTe2 provides a related telluride with a different transition metal. The calculated density of states alone does not determine their pairing index. The selected band and its occupation determine the Hubbard filling sector, which must also be reported.

## Results

| C2DB material | N(E_F), states/eV/atom | n_band | t, eV | Solver Ne | Ne after particle-hole mapping | Index from published table |
|---|---:|---:|---:|---:|---:|---:|
| 1TiTe2-1 | 0.65233751 | 0.19666676 | 0.15251509 | 6 | 6 | Pending organizer reference |
| 1PdTe2-1 | 0.16798776 | 1.99290497 | 0.25696470 | 70 | 2 | 0.142624 |
| 1PdTe2-2 | 0.60434174 | 0.15842777 | 0.13562472 | 6 | 6 | Pending organizer reference |

The published `scoring_meta.json` does not contain Ne=6. I leave those two indices unassigned and request the organizer's canonical reference for that sector. I have not interpolated a pairing amplitude or substituted an independent many-body calculation. The PdTe2 value uses the published Ne=2 amplitude after the documented particle-hole mapping and remains a provisional table estimate.

All three calculations converged. Electron counts reconstructed from the k-point weights and occupations agree with the corresponding XML electron counts within 1e-7 electrons. The submitted analysis reports every band crossing the Fermi level, so the organizer can review the active-band choice in these multiband materials.

## Protocol and control

The calculations use Quantum ESPRESSO 6.7, PBE, the original C2DB structures without relaxation, and GBRV ultrasoft pseudopotentials. The settings follow the protocol in [discussion 58](https://huggingface.co/datasets/FINAL-Bench/OSC-Superconductor/discussions/58): 35/280 Ry wavefunction/charge cutoffs, an unshifted 6 by 6 by 1 mesh, non-spin-polarized occupations, Marzari–Vanderbilt smearing of 0.02 Ry, SCF convergence threshold 1e-6 Ry, and mixing beta 0.3. Postprocessing uses Gaussian DOS broadening of 0.15 eV, includes both spins, and divides by the atom count. The single-band hopping is the active-band width divided by eight, with U/t=8.

Before calculating the three proposed materials, I reproduced the active control OSC-00747 (`2NiS-5`). Its calculated n_band is 0.84350609 and N(E_F) is 1.40205104, compared with the published 0.8435 and 1.40205. The derived Ne=30 matches the published sector. The agreement supports reproduction of the published protocol. It does not establish identical software builds or a converged physical description.

The observed SCF wall times with eight CPU processes per material were 33.18 seconds for the control and 7.03, 5.13, and 6.59 seconds for the three proposed materials. No GPU was used.

## Interpretation

The source candidate table gives energy above hull values of 0.009, 0.086, and 0.227 eV/atom for TiTe2, PdTe2-1, and PdTe2-2, respectively. The higher-energy PdTe2 polytype is included as a structural comparison, with no claim of experimental stability.

These are fixed-protocol electronic-structure results. Spin-orbit coupling, structural relaxation, and convergence with respect to the k-point grid were not evaluated. Cold-smearing occupations can slightly exceed the nominal occupied-band limit, as occurs for one competing band in PdTe2-1. The complete occupations are retained. The organizer's nearest-half-filled-band convention is applied without changing the selected band to increase the score.

This contribution does not establish superconductivity, a critical temperature, or an unbiased many-body ground state. Its purpose is to provide reproducible inputs for the organizer's Discovery evaluation, including a low-index polytype and two materials whose filling sector requires a new canonical reference.

## Reproduction and materials

The package contains the four C2DB structures, SCF inputs, complete SCF text logs, compact XML outputs, source metadata, the published scoring table, and three Python scripts. Wavefunctions are regenerated during a fresh calculation.

Install NumPy using `python -m pip install -r requirements.txt`. Run `python analyze.py` to reproduce the reported values from the included XML files. For a complete recalculation, install Quantum ESPRESSO 6.7 and Open MPI. Run `python fetch_pseudopotentials.py`, then `python run.py --ranks 8`, followed by `python analyze.py`. The fetch script retrieves the named GBRV files from their official distribution. On a compute host without internet access, transfer the resulting `pseudo/` directory from an internet-connected machine before running the calculation. Root-operated Open MPI environments require the administrator's usual Open MPI root execution settings.

The materials and derived data are distributed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), following the challenge's [provenance statement](https://huggingface.co/datasets/FINAL-Bench/OSC-Superconductor/blob/main/PROVENANCE.md). C2DB: S. Haastrup et al., *2D Materials* 5, 042002 (2018), and M. N. Gjerding et al., *2D Materials* 8, 044002 (2021). GBRV: K. F. Garrity et al., *Computational Materials Science* 81, 446 (2014), with files obtained from the [official Rutgers distribution](https://www.physics.rutgers.edu/gbrv/). The pseudopotentials retain their upstream GNU license and are downloaded separately. The original scripts in this contribution are released under the MIT license.

AI assistance was used to prepare the scripts, run the calculations, and draft this submission. All numerical results above come from the included calculation outputs.
