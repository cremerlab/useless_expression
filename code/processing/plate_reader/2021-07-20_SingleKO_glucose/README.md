---
status: >
    Accepted 
description : >
    Experiment appears to have been successful. It looks like the wild-type 
    strain is growing slightly faster than usual, though w
---

# 2021-07-20 Single KO Glucose Growth Rate Determination

## Purpose
This is an experiment measuring the rate of growth of single knockouts of 
"useless" proteins in minimal medium supplemented with glucose.

## Materials

### Growth Media
| **Label** | **Buffer Base** | **Carbon Source & Concentration** |
|:--:|:--:|:--:|
| glucose | N-C- + micronutrients | 10 mM glucose |

### Strains 
| **Label** | **Parent Strain**|  **Genotype** | **Location(s)**|
|:--: | :--:| :--:| :--:|
| WT | NCM3722 | wildtype | `GC001` |
| ∆glt | NCM3722 | gltIJKL::attL-FRT-attR | `GC030` |
| ∆flh | NCM3722 | flhDC::attL-FRT-attR | `GC029` |
| ∆rbs | NCM3722 | rbsDACB::attL-FRT-attR | `GC050` |
| ∆dpp | NCM3722 | dppABCDF::attL-FRT-attR | `GC048` |
| ∆opp | NCM3722 | oppABCDF::attL-FRT-attR | `GC053` |
| ∆mal | NCM3722 | malGEFKM+lamB::attL-FRT-attR | `GC032` |
| ∆pot | NCM3722 | potFGHI::attL-FRT-attR | `GC049` |
| ∆nmp | NCM3722 | nmpC::attL-FRT-attR | `GC052` | 
| ∆mgl | NCM3722 | mglBAC::attL-FRT-attR | `GC055` | 
| ∆his | NCM3722 | hisJQMP::attL-FRT-attR | `GC047` |

### Instrument Settings
**Instrument**: BioTek Epoch2 Microplate Reader
**Temperature**: 37° C
**Shaking Speed**: 1096 cpm (1mm) 
**Shaking Mode**: Linear 
**Shaking Duration**: 7m00s
**Read Speed**: Normal
**Read Time**: 0m32s

### Plate Layout
| **Wells** | **Label** | **Identifier** |
|:--: | :--:  | :--: |
|C3, D3, E3 | ∆glt | `GC030` | 
|C4, D4, E4 | ∆flh | `GC029` |
|C5, D5, E5 | ∆rbs | `GC050` |
|C6, D6, E6 | ∆dpp | `GC048` |
|C7, D7, E7 | ∆opp | `GC053` |
|C8, D8, E8 | ∆mal | `GC032` | 
|C9, D9, E9 | ∆pot | `GC049` |
|C10, D10, E10 | ∆nmp | `GC052` |
|F3, F4, F5 | ∆mgl | `GC055` |
|F6, F7, F8 | ∆his | `GC047` |
|F9, F10, F11 | WT | `GC001` |


## Notes & Results
The experiment appears to be successful in that we were able to measure steady-state
exponential-phase growth for WT and the single knockouts using the plate reader.
Doing a cursory analysis of the growth rates (meaning, a simple regression rather 
than a formal Bayesian analysis), we find the following growth rates:

| **strain** | **growth rate, µ [per hr]** |
|:--: |:--:|
|WT | 1.05 ± 0.01 |
|∆dpp | 1.07 ± 0.02 |
|∆flh | 0.99 ± 0.01 | 
|∆glt | 1.00 ± 0.01 |
|∆his | 1.05 ± 0.01 |
|∆mal |1.00 ± 0.02 |
|∆mgl | 0.98 ± 0.02 |
|∆nmp | 1.00 ± 0.01 |
|∆opp | 0.92 ± 0.01 |
|∆pot | 1.06 ± 0.01 |
|∆rbs | 1.04 ± 0.02 |

As I saw when doing an exploratory experiment growing the mutants in tubes, the 
mutant ∆opp appears to have  growth rate defect in glucose that is beyond 
statistical error of all others. 

### Plots
![](output/2021-07-20_SingleKO_glucose_fits.png)

## Protocol 
1.  Precultures were prepared by inoculating 3 mL of glucose minimal medium spiked 
with 3 µL of LB with a single colony from a fresh (< 2 week old) plate.
2. Preculture was allowed to grow at 37° C with aeration for 3 to 4 hours to an OD_600nm_ 
of approximately 0.2 - 0.3. 
3. Precultues were diluted 1:20 into fresh glucose minimal medium prewarmed to 37° C
growth medium. 
4. A fresh 96 well plate was filled with water in blank wells. The remaining wells 
were filled with 200 µL of diluted and mixed cultures as appropriate and described in 
the section "Plate Layout".
5. The lid of the plate was loosely sealed to the plate by applying 4 strips of 
lab tape to the sides, preventing grinding of the plate while shaking. 
6. Plate was placed in the BioTek Epoch2 Plate reader and a kinetic cycle was begun 
as described in "Instrument Settings".
7. Data was saved, backed-up, exported, and analyzed using the `processing.py` and 
`analysis.py` Python scripts.
