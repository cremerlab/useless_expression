---
status: >
    Rejected 
description : >
    Experiment was to identify a potential contamination in the water source
    and is not a final experimental measurement. 
---

# 2021-08-06 WT Growth in Acetate With Different Water Sources 

## Purpose
This is an experiment to compare different water sources and micronutrient concentrations to see if trace elements have a large impact on the growth rate

## Materials

## Water Sources 
|**Label**| **Source** | **Notes**|
|:--:|:--:|:--:|
| CCSR | CCSR Building at Stanford | MQ water from another lab and building |
| MQ + | Clark Center MQ | MQ water with active ion filtering |
| MQ - | Clar Center MQ | MQ water without active ion filtering |
| Carboy | Clark Center MQ | MQ water from the lab water Carboy | 

### Growth Media
| **Label** | **Buffer Base** | **Carbon Source & Concentration** |
|:--:|:--:|:--:|
| glucose | N-C- +/- micronutrients | 30 mM acetate |

### Strains 
| **Label** | **Parent Strain**|  **Genotype** | **Location(s)**|
|:--: | :--:| :--:| :--:|
| WT | NCM3722 | wild-type *E. coli* NCM3722 | `GC001`

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
| Number of Measurements |  86 | 

### Plate Layout
| **Wells** | **Label** |
|:--: | :--:  | :--: |
|C3, C4, C5, C6 | CCSR + micronutrients |
|D3, D4, D5, D6 | CCSR - micronutrients |
|E3, E4, E5, E6 | MQ+ + micronutrients |
|F3, F4, F5, F6 | MQ+ - micronutrients |
|C7, C8, C9, C10 | MQ- + micronutrients |
|D7, D8, D9, D10 | MQ- - micronutrients |
|E7, E8, E9, E10 | Carboy + micronutrients |
|F7, F8, F9, F10 | Carboy - micronutrients |

## Notes & Results

It appears that there isi little difference in teh growth rates using different 
water sources. The primary difference comes down to whether or not there are 
micronutrients present.

### Growth Rate Inference

The inferred growth rates were as follows

| **condition** | **growth rate, µ [per hr]** |
|:--: |:--:|
|CCSR + micronutrients| 0.71 ± 0.02|
|CCSR - micronutrients | 0.413 ± 0.006|
|MQ+ + micronutrients | 0.67 ± 0.02 |
|MQ+ - micronutrients | 0.400 ± 0.006 | 
|MQ- + micronutrients | 0.629 ± 0.004 |
|MQ- - micronutrients | 0.385 ± 0.002 |
|Carboy + micronutrients | 0.65 ± 0.01 | 
|Carboy - micronutrients | 0.384 ± 0.004 | 

### Plots

**Fits**
![](output/2021-08-06_r1_WT_acetate_water_comparison_fits.png)

*Growth Curves**
![](output/2021-08-06_r1_WT_acetate_water_comparison_raw_traces.png)

## Protocol 
1.  Seed cultures were prepared by inoculating 3 mL of LB with a single colony from a fresh (< 2 week old) plate.
2. The LB culture was allowed to grow for 4.5 hours to saturation. 
3. A preculture was prepared by diluting the seed culture 1:1000 into 
prewarmed acetate minimal medium and allowed to grow for 12 hours at 37° C
to an OD_600nm_ of ≈ 0.4.
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
