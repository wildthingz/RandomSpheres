# RandomSpheres
This code uses blender envirnoment to generate a number of randomly positioned, randomly sized ellipsoids (fig1).
<p align="center"><img src=images/img1.png width="500"></p>
<p align="center"><i>fig1.</i> Randomly sized ellipsoids.</p>
The original purpose behind this code was to compare volume fraction and area fraction. In this regard, a series of functions has been defined to generate a random configuration of ellipsoids in a box, 'RandSphereGen.py'. After saving the value of the volume fraction, blender sections the box from a random position and saves the resultant cross-section as an image (fig2).
<p align="center"><img src=images/img2.png width="500"></p>
<p align="center"><i>fig2.</i> Cross-sectional view of randomly generated ellipsoids.</p>
In part two of this code 'AnalyzeImg.py', a standalone python code has been used to analyze the resultant images, exctrat area fraction and compare the value to the original volume fraction value from blender and plot the results (fig3).
<p align="center"><img src=images/img3.png width="500"></p>
<p align="center"><i>fig3.</i> Comparison of area fraction and volume fraction.</p>
# Tested versions
These scripts have been tested using:
- Blender 2.69.0 (R2013a)
- Python 2.7.11 Anaconda 2.3.0
    
