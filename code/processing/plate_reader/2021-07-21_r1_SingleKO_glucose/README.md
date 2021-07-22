---
status: >
    Accepted 
description : >
    Experiment appears to have been successful with no aberrant results. 
---

# 2021-07-21 Single KO Glucose Growth Rate Determination

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
| Instrument | BioTek Epoch2 Microplate Reader|
|:--:| :--:|
| Temperature| 37° C|
| Shaking Speed| 1096 cpm (1mm) |
| Shaking Mode | Linear |
| Shaking Duration| 7m00s|
|Read Speed| Normal|
| Read Time | 0m32s|
| Total Interval | 7m32s |
| Number of Measurements | 96 | 

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

### Growth Rate Inference
The experiment appears to be successful in that we were able to measure steady-state
exponential-phase growth for WT and the single knockouts using the plate reader.
Doing a cursory analysis of the growth rates (meaning, a simple regression rather 
than a formal Bayesian analysis), we find the following growth rates:

| **strain** | **growth rate, µ [per hr]** |
|:--: |:--:|
|WT | 1.02 ± 0.01 |
|∆dpp | 1.01 ± 0.01 |
|∆flh | 1.04 ± 0.01 | 
|∆glt | 0.987 ± 0.007 |
|∆his | 1.02 ± 0.02 |
|∆mal | 0.91 ± 0.01 |
|∆mgl | 1.00 ± 0.01 |
|∆nmp | 0.994 ± 0.004 |
|∆opp | 0.937 ± 0.006 |
|∆pot | 1.019 ± 0.005 |
|∆rbs | 0.963 ± 0.009 |

Again, ∆opp appears to have a slight growth rate defect compared to the 
wildtype. Interestingly, compared to the experiment on 2021-07-20, the ∆mal
KO has also grew considerably slower than in glucose.


### Shape of profiles
As in the experiment on 2021-07-20, the full curves of the growth cycle are very
interesting. For most of the strains, one can see the diauxic shift to the cells 
eating their own secreted acetate. Perhaps more interestingly, one can see that 
for ∆flh, ∆rbs, and ∆opp, there is a **massive** drop in the OD once they reach 
saturation, with what appears to be no lag time at all. In future experiments, 
it will be good to look at the cells during this point on the microscope


### Plots
**Fits**
![](output/2021-07-21_r1_SingleKO_glucose_fits.png)

**Growth Curves**
![](output/2021-07-21_r1_SingleKO_glucose_raw_traces.png)

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
