---
status: >
   Accepted
description : >
   Data looks okay and should be kept. Sample of ∆his ∆dpp has a different 
   saturation point and again a very slow growth rate. 
---

# 2021-08-20 (Run 2) Double KO Acetate Growth Rate Determination

## Purpose
This is an experiment measuring the rate of growth of the third suite of 
double KOs of  "useless" proteins in minimal medium supplemented with acetate.

## Materials

### Growth Media
| **Label** | **Buffer Base** | **Carbon Source & Concentration** |
|:--:|:--:|:--:|
| acetate | N-C- + micronutrients | 30 mM acetate |

### Strains 
| **Label** | **Parent Strain**|  **Genotype** | **Location(s)**|
|:--: | :--:| :--:| :--:|
|∆mal ∆flh| NCM3722 | malGEFKM+lamB::attL-FRT-attR flhDC::attL-FRT-attR | `GC086`|
|∆pot ∆flh| NCM3722 | potFGHI::attL-FRT-attR flhDC::attL-FRT-attR | `GC093`|
|∆nmp ∆dpp| NCM3722 | nmpC::attL-FRT-attR dppABCDF::attL-FRT-attR | `GC077`|
|∆opp ∆dpp| NCM3722 | oppABCDF::attL-FRT-attR dppABCDF::attL-FRT-attR | `GC083`|
|∆pot ∆dpp| NCM3722 | potFGHI::attL-FRT-attR dppABCDF::attL-FRT-attR | `GC095`|
|∆his ∆dpp| NCM3722 | hisJQMP::attL-FRT-attR dppABCDF::attL-FRT-attR | `GC081`|
|∆mgl ∆dpp| NCM3722 | mglBAC::attL-FRT-attR dppABCDF::attL-FRT-attR | `GC080`|
|∆mal ∆dpp| NCM3722 | malGEFKM+lamB::attL-FRT-attR dppABCDF::attL-FRT-attR | `GC107`|
|∆nmp ∆opp| NCM3722 | npmC::attL-FRT-attR oppABCDF::attL-FRT-attR | `GC102`|
|∆mgl ∆opp| NCM3722 | mglBAC::attL-FRT-attR oppABCDF::attL-FRT-attR | `GC076`|
|∆his ∆opp| NCM3722 | malGEFKM+lamB::attL-FRT-attR oppABCDF::attL-FRT-attR | `GC109`|

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
|C3, D3, E3 | ∆mal ∆flh| `GC086` | 
|C4, D4, E4 | ∆pot ∆flh| `GC093` |
|C5, D5, E5 | ∆nmp ∆dpp| `GC077` |
|C6, D6, E6 | ∆opp ∆dpp| `GC083` |
|C7, D7, E7 | ∆pot ∆dpp| `GC095` |
|C8, D8, E8 | ∆his ∆dpp| `GC081` | 
|C9, D9, E9 | ∆mgl ∆dpp| `GC080` |
|C10, D10, E10 | ∆mal ∆dpp| `GC107` |
|F3, F4, F5 | ∆nmp ∆opp| `GC102` |
|F6, F7, F8 | ∆mgl ∆opp| `GC076` |
|F9, F10, F11 | ∆his ∆opp| `GC109` |


## Notes & Results
The OD of the precultures for ∆his ∆dpp was low and I added it straight to the 
plate for growth rate determination.

For the sample of ∆his ∆dpp, there was a slightly different saturation value 
(which I can't yet make sense of) meaning I couldn't just filter on OD to get 
the exponential regime. For this sample, I only kept the measurements prior to 
6 hrs for determination of growth rate.

### Growth Rate Inference

| **strain** | **growth rate, µ [per hr]** |
|:--: |:--:|
|∆mal ∆flh| 0.376 ± 0.004|
|∆pot ∆flh| 0.481 ± 0.003|
|∆nmp ∆dpp| 0.559 ± 0.004| 
|∆opp ∆dpp| 0.537 ± 0.004|
|∆pot ∆dpp| 0.521 ± 0.006|
|∆his ∆dpp| 0.175 ± 0.002|
|∆mgl ∆dpp| 0.559 ± 0.004|
|∆mal ∆dpp| 0.468 ± 0.002|   
|∆nmp ∆opp| 0.464 ± 0.004|  
|∆mgl ∆opp| 0.467 ± 0.005|
|∆his ∆opp| 0.448 ± 0.003|


### Plots

**Fits**

![](output/2021-08-20_r2_DoubleKO_acetate_fits.png)

**Growth Curves**

![](output/2021-08-20_r2_DoubleKO_acetate_raw_traces.png)

## Protocol 
1.  Seed cultures were prepared by inoculating 3 mL of LB with a single colony from a fresh (< 2 week old) plate.
2. The LB culture was allowed to grow for 4.5 hours to saturation. 
3. A preculture was prepared by diluting the seed culture 1:300 into 
prewarmed acetate minimal medium and allowed to grow for 8 hours at 37° C
to an OD_600nm_ of ≈ 0.5.
4. Precultues were diluted  1:20 into fresh acetate minimal medium prewarmed to 37° C. The samples of ∆his ∆dpp
was *not* diluted. 
4. A fresh 96 well plate was filled with water in blank wells. The remaining wells 
were filled with 200 µL of diluted and mixed cultures as appropriate and described in 
the section "Plate Layout".
5. The lid of the plate was loosely sealed to the plate by applying 4 strips of 
lab tape to the sides, preventing grinding of the plate while shaking. 
6. Plate was placed in the BioTek Epoch2 Plate reader and a kinetic cycle was begun 
as described in "Instrument Settings".
7. Data was saved, backed-up, exported, and analyzed using the `processing.py` and 
`analysis.py` Python scripts.
