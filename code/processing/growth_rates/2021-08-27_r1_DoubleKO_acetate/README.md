---
status: >
   Accepted
description : >
  Experiment went without a hitch. 
---

# 2021-08-27 (Run 1) Double KO Acetate Growth Rate Determination

## Purpose
This is an experiment measuring the rate of growth of the fourth suite of 
double KOs of  "useless" proteins in minimal medium supplemented with acetate.

## Materials

### Growth Media
| **Label** | **Buffer Base** | **Carbon Source & Concentration** |
|:--:|:--:|:--:|
| acetate | N-C- + micronutrients | 30 mM acetate |

### Strains 
| **Label** | **Parent Strain**|  **Genotype** | **Location(s)**|
|:--: | :--:| :--:| :--:|
|∆mal ∆his| NCM3722 | malGEFKM+lamB::attL-FRT-attR hisJQMP::attL-FRT-attR | `GC110`|
|∆mal ∆pot| NCM3722 | malGEFKM+lamB::attL-FRT-attR potFGHI::attL-FRT-attR| `GC108`|
|∆pot ∆his| NCM3722 | potFGHI::attL-FRT-attR hisJQMP::attL-FRT-attR | `GC094`|
|∆mal ∆nmp| NCM3722 | malGEFKM+lamB::attL-FRT-attR nmpC::attL-FRT-attR | `GC089`|
|∆his ∆nmp| NCM3722 | hisJQMP::attL-FRT-attR nmpC::attL-FRT-attR | `GC092`|
|∆pot ∆nmp| NCM3722 | potFGHI::attL-FRT-attR nmpC::attL-FRT-attR | `GC101`|
|∆pot ∆mgl| NCM3722 | potFGHI::attL-FRT-attR mglBAC::attL-FRT-attR | `GC103`|
|∆mal ∆mgl| NCM3722 | malGEFKM+lamB::attL-FRT-attR mglBAC::attL-FRT-attR | `GC088`|
|∆nmp ∆mgl| NCM3722 | nmpC::attL-FRT-attR mglBAC::attL-FRT-attR | `GC091`|
|∆his ∆mgl| NCM3722 | hisJQMP::attL-FRT-attR mglBAC::attL-FRT-attR | `GC078`|
|∆mal ∆opp| NCM3722 | malGEFKM+lamB::attL-FRT-attR oppABCDF::attL-FRT-attR | `GC087`|
|∆pot ∆opp| NCM3722 | potFGHI::attL-FRT-attR oppABCDF::attL-FRT-attR | `GC096`|

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
| Number of Measurements |96 | 

### Plate Layout
| **Wells** | **Label** | **Identifier** |
|:--: | :--:  | :--: |
|C3, D3, E3 | ∆mal ∆his| `GC110` | 
|C4, D4, E4 | ∆mal ∆pot| `GC108` |
|C5, D5, E5 | ∆pot ∆his| `GC094` |
|C6, D6, E6 | ∆mal ∆nmp| `GC089` |
|C7, D7, E7 | ∆his ∆nmp| `GC092` |
|C8, D8, E8 | ∆pot ∆nmp| `GC101` | 
|C9, D9, E9 | ∆pot ∆mgl| `GC103` |
|C10, D10, E10 | ∆mal ∆mgl| `GC088` |
|C11, D11, E11 | ∆nmp ∆mgl| `GC091` |
|F3, F4, F5 | ∆his ∆mgl| `GC078` |
|F6, F7, F8 | ∆mal ∆opp| `GC087` |
|F9, F10, F11 | ∆pot ∆opp| `GC096` |


## Notes & Results

### Growth Rate Inference

| **strain** | **growth rate, µ [per hr]** |
|:--: |:--:|
|∆mal ∆his| 0.527 ± 0.004|
|∆mal ∆pot| 0.505 ± 0.004|
|∆pot ∆his| 0.510 ± 0.003| 
|∆mal ∆nmp| 0.504 ± 0.005|
|∆his ∆nmp| 0.236 ± 0.015|
|∆pot ∆nmp| 0.502 ± 0.002|
|∆pot ∆mgl| 0.491 ± 0.004|
|∆mal ∆mgl| 0.512 ± 0.002|   
|∆nmp ∆mgl| 0.500 ± 0.004|  
|∆his ∆mgl| 0.522 ± 0.003|
|∆mal ∆opp| 0.468 ± 0.002|
|∆pot ∆opp| 0.471 ± 0.003|


### Plots

**Fits**

![](output/2021-08-27_r1_DoubleKO_acetate_fits.png)

**Growth Curves**

![](output/2021-08-27_r1_DoubleKO_acetate_raw_traces.png)

## Protocol 
1.  Seed cultures were prepared by inoculating 3 mL of LB with a single colony from a fresh (< 2 week old) plate.
2. The LB culture was allowed to grow for 4.5 hours to saturation. 
3. A preculture was prepared by diluting the seed culture 1:1000 into 
prewarmed acetate minimal medium and allowed to grow for 12 hours at 37° C
to an OD_600nm_ of ≈ 0.5.
4. Precultues were diluted  1:20 into fresh acetate minimal medium prewarmed to 37° C. The
cultures of ∆his ∆nmp, ∆mal ∆opp, and ∆pot ∆opp were not diluted as their OD was considerably 
lower.
4. A fresh 96 well plate was filled with water in blank wells. The remaining wells 
were filled with 200 µL of diluted and mixed cultures as appropriate and described in 
the section "Plate Layout".
5. The lid of the plate was loosely sealed to the plate by applying 4 strips of 
lab tape to the sides, preventing grinding of the plate while shaking. 
6. Plate was placed in the BioTek Epoch2 Plate reader and a kinetic cycle was begun 
as described in "Instrument Settings".
7. Data was saved, backed-up, exported, and analyzed using the `processing.py` and 
`analysis.py` Python scripts.
