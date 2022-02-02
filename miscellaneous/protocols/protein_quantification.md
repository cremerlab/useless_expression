# Protein Quantification

## Description
This protocol describes a method by which one can determine the total protein
concentration in a given sample. This is typically used in conjunction with the 
RNA quantification method (`RNA_quantification.md`) to determine the RNA/Protein
ratio.


## Materials

|**Name** | **Concentration** | **Storage**| 
|:--:|:--:|:--:|
|Sodium Hydroxide (NaOH) | 3 M | Room Temp |
|Copper Sulfate (CuSO<sub>4</sub>) | 1.6 % w/v | Room Temp|
|Bovine Serum Albumin (BSA) | 10 mg / mL | 4 °C |


## Protocolß
1. Collect ≈ 1.5 mL of cell culture at an OD<sub>600</sub> ≈ 0.4 - 0.5 and 
place in a clean eppendorf tube. 
2. Pellet the cells for 2 min at 15000xg.
3. Measure and record the OD<sub>600nm</sub> of the supernatant. 
4. Resuspend the pellet with 1 mL of ddH<sub>2</sub>O and spin at 15000xg for 
30 seconds. 
5. Measure the OD<sub>600nm</sub> of teh supernatant. 
6. Resuspend pellets in 200 µL of ddH<sub>2</sub>O and transfer to a new eppendorf tube
and place on dry ice. 
7. Add 1.5 mL of ddH<sub>2</sub>O to the now-empty eppendorf tube (where you resuspended the pellet),
mix gently, and measure teh OD<sub>600nm</sub> of the solution.
8. Add 100 µL of 3M NaOH to the frozen pellets and transfer to a pre-heated 100 °C heat block. Allow 
the cells to lyse for 5 min. 
9. Remove the tubes from the heat block and allow them to cool to room temperature (5 min).
10. Once cooled, add 100 µL of 1.6% CuSO<sub>4</sub> and mix thoroughly. Allow mixture to 
incubate for 5 min at room temperature. 
11. Centrifuge the tubes at max speed for 3 min. Remove the supernatant and measure 
the A<sub>550nm</sub>.

## Calculation
This method requires a standard calibration curve. There should be a linear relationship
between the amount of protein per mL and the A<sub>555</sub>. To make a calibration 
curve, create a titration series of a standard BSA solution and measure the absorbance. 
To the data, perform a linear regression (with proper propagation of errors) and 
determine the concentration of protein per mL in your sample solution. Divide this 
value by the total OD<sub>600nm</sub> of cells that made it (subtracting the measured OD<sub>600nm</sub> 
of the supernatants) to get mass of protein per OD per mL.


## Reference

Herbert, D; Phipps, P.J.; Strange, R.E.; 1971. "Chemical analysis of microbial cells." *Methods in Microbiology