---
status: >
    Rejected
description : >
    Experiment is still ongoing 
---

# 2021-08-14 (Run 1) Double KO Acetate Growth Rate Determination

## Purpose
This is an experiment measuring the rate of growth of the first suite of 
double KOs of  "useless" proteins in minimal medium supplemented with acetate.

## Materials

### Growth Media
| **Label** | **Buffer Base** | **Carbon Source & Concentration** |
|:--:|:--:|:--:|
| acetate | N-C- + micronutrients | 30 mM acetate |

### Strains 
| **Label** | **Parent Strain**|  **Genotype** | **Location(s)**|
|:--: | :--:| :--:| :--:|
|∆rbs ∆glt | NCM3722 | rbsDACB::attL-FRT-attR gltIJKL::attL-FRT-attR | `GC073`|
|∆flh ∆glt | NCM3722 | flhDC::attL-FRT-attR gltIJKL::attL-FRT-attR | `GC069`|
|∆dpp ∆glt | NCM3722 | dppABCDF::attL-FRT-attR gltIJKL::attL-FRT-attR | `GC075`|
|∆opp ∆glt | NCM3722 | oppABCDF::attL-FRT-attR gltIJKL::attL-FRT-attR | `GC070`|
|∆mgl ∆glt | NCM3722 | mglBAC::attL-FRT-attR gltIJKL::attL-FRT-attR | `GC065`|
|∆nmp ∆glt | NCM3722 | nmpC::attL-FRT-attR gltIJKL::attL-FRT-attR | `GC098`|
|∆his ∆glt | NCM3722 | hisJQMP::attL-FRT-attR gltIJKL::attL-FRT-attR | `GC074`|
|∆pot ∆glt | NCM3722 | potFGHI::attL-FRT-attR gltIJKL::attL-FRT-attR | `GC097`|
|∆mal ∆glt | NCM3722 | malGEFKM+lamB::attL-FRT-attR gltIJKL::attL-FRT-attR | `GC084`|
|∆flh ∆rbs | NCM3722 | flhDC::attL-FRT-attR rbsDACB::attL-FRT-attR | `GC106`|
|∆dpp ∆rbs | NCM3722 | dppABCDF::attL-FRT-attR rbsDACB::attL-FRT-attR | `GC100`|

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
| Number of Measurements | 91 | 

### Plate Layout
| **Wells** | **Label** | **Identifier** |
|:--: | :--:  | :--: |
|C3, D3, E3 | ∆rbs ∆glt | `GC073` | 
|C4, D4, E4 | ∆flh ∆glt | `GC069` |
|C5, D5, E5 | ∆dpp ∆glt | `GC075` |
|C6, D6, E6 | ∆opp ∆glt | `GC070` |
|C7, D7, E7 | ∆mgl ∆glt| `GC065` |
|C8, D8, E8 | ∆nmp ∆glt | `GC098` | 
|C9, D9, E9 | ∆his ∆glt | `GC074` |
|C10, D10, E10 | ∆pot ∆glt | `GC097` |
|F3, F4, F5 | ∆mal ∆glt | `GC084` |
|F6, F7, F8 | ∆flh ∆rbs | `GC106` |
|F9, F10, F11 | ∆dpp ∆rbs | `GC100` |


## Notes & Results
The precultures were slightly more dense than they have usually been. Thus, 
when setting up the precultures, I did a 1:100 dilution instead of 1:20.

### Growth Rate Inference

| **strain** | **growth rate, µ [per hr]** |
|:--: |:--:|
|∆rbs ∆glt |  |
|∆flh ∆glt |  |
|∆dpp ∆glt |  | 
|∆opp ∆glt |  |
|∆mgl ∆glt |  |
|∆nmp ∆glt |  |
|∆his ∆glt |  |
|∆pot ∆glt |  |
|∆mal ∆glt |  |
|∆flh ∆rbs |  |
|∆dpp ∆rbs |  |


### Plots

**Fits**

![](output/2021-08-13_r1_DoubleKO_acetate_fits.png)

**Growth Curves**

![](output/2021-08-13_r1_DoubleKO_acetate_raw_traces.png)

## Protocol 
1.  Seed cultures were prepared by inoculating 3 mL of LB with a single colony from a fresh (< 2 week old) plate.
2. The LB culture was allowed to grow for 4.5 hours to saturation. 
3. A preculture was prepared by diluting the seed culture 1:1000 into 
prewarmed acetate minimal medium and allowed to grow for 12 hours at 37° C
to an OD_600nm_ of ≈ 0.7.
4. Precultues were diluted  1:100 into fresh acetate minimal medium prewarmed to 37° C.
4. A fresh 96 well plate was filled with water in blank wells. The remaining wells 
were filled with 200 µL of diluted and mixed cultures as appropriate and described in 
the section "Plate Layout".
5. The lid of the plate was loosely sealed to the plate by applying 4 strips of 
lab tape to the sides, preventing grinding of the plate while shaking. 
6. Plate was placed in the BioTek Epoch2 Plate reader and a kinetic cycle was begun 
as described in "Instrument Settings".
7. Data was saved, backed-up, exported, and analyzed using the `processing.py` and 
`analysis.py` Python scripts.
