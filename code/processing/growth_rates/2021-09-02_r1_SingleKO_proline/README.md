---
status: >
    Rejected
description : >
    Data looks ok but is should not be kept as protocol for reaching steady 
    state with the precultures is still not optimized. The sample for ∆nmp was dropped as the 
    variation in the technical replicats was large. Sample of ∆glt was 
    manually truncated by time to appropriately identify the exponential regime.
    Sample of ∆pot did not grow.
---

# 2021-09-02 (Run 1) Single KO L-Proline Growth Rate Determination

## Purpose
This is an experiment measuring the rate of growth of the single KOs of  "useless" proteins in minimal medium supplemented with L-proline.

## Materials

### Growth Media
| **Label** | **Buffer Base** | **Carbon Source & Concentration** |
|:--:|:--:|:--:|
| proline | N-C- + micronutrients | 12 mM proline |

### Strains 
| **Label** | **Parent Strain**|  **Genotype** | **Location(s)**|
|:--: | :--:| :--:| :--:|
|∆mal| NCM3722 | malGEFKM+lamB::attL-FRT-attR| `GC032`|
|∆pot| NCM3722 | potFGHI::attL-FRT-attR| `GC049`|
|∆nmp| NCM3722 | nmpC::attL-FRT-attR | `GC052`|
|∆his| NCM3722 | hisJQMP::attL-FRT-attR | `GC047`|
|∆rbs | NCM3722 | rbsDACB::attL-FRT-attR | `GC050`|
|∆dpp | NCM3722 | dppABCDF::attL-FRT-attR | `GC048`|
|∆opp | NCM3722 | oppABCDF::attL-FRT-attR | `GC053`|
|∆mgl| NCM3722 | mglBAC::attL-FRT-attR | `GC055`|
|∆glt | NCM3722 | gltIJKL::attL-FRT-attR | `GC030`|
|∆flh | NCM3722 | flhDC::attL-FRT-attR | `GC029`|
|WT| NCM3722 | | `GC001`|

### Instrument Settings
| Instrument | BioTek Epoch2 Microplate Reader|
|:--:| :--:|
| Temperature| 37° C|
| Shaking Speed| 1096 cpm (1mm) |
| Shaking Mode | Linear |
| Shaking Duration| 7m00s|
|Read Speed| Normal|
| Read Time | 0m32s|
| Total Interval | 7m32s |
| Number of Measurements |90 | 

### Plate Layout
| **Wells** | **Label** | **Identifier** |
|:--: | :--:  | :--: |
|C3, D3, E3 | ∆mal | `GC032` | 
|C4, D4, E4 | ∆pot | `GC049` |
|C5, D5, E5 | ∆nmp | `GC052` |
|C6, D6, E6 | ∆his | `GC047` |
|C7, D7, E7 | ∆rbs | `GC050` |
|C8, D8, E8 | ∆dpp | `GC048`| 
|C9, D9, E9 | ∆opp | `GC053` |
|C10, D10, E10 | ∆mgl| `GC055` |
|F3, F4, F5 | ∆glt | `GC030` |
|F6, F7, F8 | ∆flh | `GC029` |
|F9, F10, F11 | WT | `GC001` |


## Notes & Results

This experiment revealed how tricky it is to grow samples in L-proline. Samples
for ∆nmp showed high variation between technical replicates, ∆pot simply did
not grow, and ∆glt appeared to have a very large lag time before reaching the
exponential phase. However, the other samples appeared to grow fine and 
the estimated growth rates are in line with previous experiments. For that 
reason, I think that the experiment should be accepted.

### Growth Rate Inference

| **strain** | **growth rate, µ [per hr]** |
|:--: |:--:|
|∆mal | 0.41 ± 0.02|
|∆pot | Not Determined |
|∆nmp | Not Determined| 
|∆his | 0.476 ± 0.007|
|∆rbs | 0.145 ± 0.001|
|∆dpp | 0.466 ± 0.009|
|∆opp | 0.338 ± 0.002|
|∆mgl | 0.464 ± 0.007|   
|∆glt | 0.081 ± 0.002|  
|∆flh | 0.175 ± 0.001|
|WT   | 0.41 ± 0.02|


### Plots

**Fits**

![](output/2021-09-01_r2_SingleKO_proline_fits.png)

**Growth Curves**

![](output/2021-09-01_r2_SingleKO_proline_raw_traces.png)

## Protocol 
1.  Seed cultures were prepared by inoculating 3 mL of LB with a single colony from a fresh (< 2 week old) plate.
2. The LB culture was allowed to grow for 4.5 hours to saturation. 
3. A preculture was prepared by diluting the seed culture 1:1000 into 
prewarmed acetate minimal medium and allowed to grow for 15 hours at 37° C
to an OD_600nm_ of ≈ 0.3.
4. Precultues were diluted  1:20 into fresh acetate minimal medium prewarmed to 37° C. 
4. A fresh 96 well plate was filled with water in blank wells. The remaining wells 
were filled with 200 µL of diluted and mixed cultures as appropriate and described in 
the section "Plate Layout".
5. The lid of the plate was loosely sealed to the plate by applying 4 strips of 
lab tape to the sides, preventing grinding of the plate while shaking. 
6. Plate was placed in the BioTek Epoch2 Plate reader and a kinetic cycle was begun 
as described in "Instrument Settings".
7. Data was saved, backed-up, exported, and analyzed using the `processing.py` and 
`analysis.py` Python scripts.
