import os
import pylab
import numpy as np
import random
from PIL import Image
from scipy import ndimage




os.chdir("/home/hatef/Desktop/PhD/Phase_01_imageProcessing/RandomSpheres/pics_2_[0.1,1]")


def findAreaFrac(img,CropScale=[10,530,220,740],thresh=205):
	
	img = img.convert("L")
	img = np.asarray(img)
	img=img[CropScale[0]:CropScale[1],CropScale[2]:CropScale[3]]
	img = 1*(img<thresh)
	#pylab.imshow(img,cmap=pylab.cm.gray, interpolation='nearest')
	#pylab.show()
	img=ndimage.binary_fill_holes(img,structure=np.ones((5,5))).astype(int)
	#pylab.imshow(img,cmap=pylab.cm.gray, interpolation='nearest')
	return np.sum(img)/float(np.size(img))



areafrac=[]
volfrac = [float(line.strip()) for line in open("volfrac", 'r')]
n=len(volfrac)
n=50
for i in range(n):
	
	name = "img"+str(i)
	image = Image.open(name)
	areafrac.append(findAreaFrac(image))
	print(str(100*i/float(n)) + "%")

error = [100*abs(volfrac[i]-areafrac[i])/float(volfrac[i]) for i in range(len(areafrac))]
print("100%")
print("Operation complete.") 

va=0
aa=0
for i in range(len(areafrac)):
	aa += areafrac[i]
	va += volfrac[i]
AvE=abs(((va-aa)/float(len(areafrac))) - (va/float(len(areafrac))))/(va/float(len(areafrac)))



mean = sum(volfrac)/float(len(volfrac))
std = 0
for vol in volfrac:
	std += (vol - mean)**2
std = (std/float(len(volfrac)))**(1/2)

pylab.hist(error,bins=20)
pylab.xlabel("% error")
pylab.ylabel("Frequency")
pylab.title("Error in area fraction (with vf mean: {0}, sigma: {1})".format("{0:.3f}".format(mean),std)) 
pylab.legend(["Average Error: "+str("{0:.2f}".format(AvE))+"%"])


pylab.show()
		
		
		
		
		
