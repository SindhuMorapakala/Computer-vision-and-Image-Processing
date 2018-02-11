#===============================================================================
#                   Sum of Squared Differences (SSD) Matching
#===============================================================================


import cv2
import numpy as np
import scipy.signal
from matplotlib import pyplot as plt

#Read the left and right images along with the ground truth images
left = cv2.imread('C:\Users\Inspiron\Desktop\UB\CVIP_CSE573\FinalProject\View1.png')
right = cv2.imread('C:\Users\Inspiron\Desktop\UB\CVIP_CSE573\FinalProject\View5.png')
disp1 = cv2.imread('C:\Users\Inspiron\Desktop\UB\CVIP_CSE573\FinalProject\disp1.png')
disp2 = cv2.imread('C:\Users\Inspiron\Desktop\UB\CVIP_CSE573\FinalProject\disp5.png')

#convert read images to grayscale
left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
disp1 = cv2.cvtColor(disp1, cv2.COLOR_BGR2GRAY)
disp2 = cv2.cvtColor(disp2, cv2.COLOR_BGR2GRAY)

#Determine the size of each image
Lheight, Lwidth = left.shape
Rheight, Rwidth = right.shape

#Pad each left and right image with zeros
padleft = np.lib.pad(left,((4,4),(4,4)), mode='constant',constant_values=(0,0))
padright = np.lib.pad(right,((4,4),(4,4)), mode='constant',constant_values=(0,0))

#Padded images size
pheight,pwidth = padleft.shape

Lssd3 = 0
Rssd3 = 0

#Initialise Disparity map
Ldisp = np.zeros((pheight, pwidth))
Rdisp = np.zeros((pheight, pwidth))

#Run loop from the points where pixels values are present in the padded image
for i in range(4,pheight-4):
    for j in range(4, pwidth -4):
        Lminssd = 100000
        Rminssd = 100000
        lcol = 0
        rcol = 0
        k = j

        #Initialise the Windows         
        lwin = padleft[i-4:i+5,j-4:j+5]
        rwin = padright[i-4:i+5,j-4:j+5]
        while((j-k <75) and (k != 3)):#Assuming that the difference of localtions of same pixel is within 75
            Lssd3 = 0
            ldiff = padright[i-4:i+5,k-4:k+5] - lwin 
            Lssd3 = np.sum(np.square(ldiff ))#Computing SSD for left disparity
           
            if(Lminssd > Lssd3):#Determining the minimum SSD
                Lminssd = Lssd3
                lcol = k
            k = k - 1
        Ldisp[i,j] = abs(j - lcol)
        
        for k in range(j, j + 75):#Repeating for the right disparity map
        
            if(k < Rwidth + 4):
                Rssd3 = 0
                rdiff = rwin - padleft[i-4:i+5,k-4:k+5]
                Rssd3 = np.sum(np.square(rdiff))#SSD computation for right
                if(Rminssd > Rssd3):# Checking for least SSD
                    Rminssd = Rssd3
                    rcol = k
                Rdisp[i,j] = abs(j - rcol)

#Removing the padding                        
ldisp = Ldisp[4:pheight-4,4:pwidth-4]
rdisp = Rdisp[4:pheight -4,4:pwidth -4]

#Determining MSE
Lmse = np.mean(np.mean(np.square(disp1 - ldisp)))
Rmse =  np.mean(np.mean(np.square(disp2 - rdisp)))

print "MSE OF LEFT DISPARITY %d" %(Lmse)
print "MSE OF RIGHT DISPARITY %d" %(Rmse)

cv2.imshow('Left Disparity[9x9]', ldisp/Ldisp.max())
cv2.imshow('Right Disparity[9x9]',rdisp/Rdisp.max())
