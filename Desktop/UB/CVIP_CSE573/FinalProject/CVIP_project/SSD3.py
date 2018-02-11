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
padleft = np.empty((Lheight + 2, Lwidth + 2), np.uint8)
padright = np.empty((Rheight + 2, Rwidth + 2), np.uint8)

#Padded images size
pheight,pwidth = padleft.shape


padleft[1:pheight-1,1:pwidth - 1] = left
padright[1:pheight-1,1:pwidth - 1] = right

Lssd3 = 0
Rssd3 = 0

#Initialise Disparity map
Ldisp = np.zeros((pheight, pwidth))
Rdisp = np.zeros((pheight, pwidth))

#Run loop from the points where pixels values are present in the padded image
for i in range(1,pheight-1):
    for j in range(1, pwidth -1):
        Lminssd = 100000
        Rminssd = 100000
        lcol = 0
        rcol = 0
        k = j
        #Initialise the Windows    
        lwin = padleft[i-1:i+2,j-1:j+2]
        rwin = padright[i-1:i+2,j-1:j+2]
        while((j-k <75) and (k !=0)):#Assuming that the difference of localtions of same pixel is within 75
           
            Lssd3 = 0
            ldiff = lwin - padright[i-1:i+2,k-1:k+2]
            Lssd3 = np.sum(np.square(ldiff ))#Computing SSD for left disparity
            
            if(Lminssd > Lssd3):
                Lminssd = Lssd3
                lcol = k
            k = k - 1
        Ldisp[i,j] = abs(j - lcol)
        for k in range(j, j +75):#Repeating for the right disparity map
        #print "Value of k %d" %(k)
            if(k <= Rwidth):
                Rssd3 = 0
                rdiff = rwin - padleft[i-1:i+2,k-1:k+2]
                Rssd3 = np.sum(np.square(rdiff))#SSD computation for right 
                if(Rminssd > Rssd3):# Checking for least SSD
                    Rminssd = Rssd3
                    rcol = k
                Rdisp[i,j] = abs(j - rcol)
#Removing the padding      
ldisp = Ldisp[1:pheight-1,1:pwidth-1]
rdisp = Rdisp[1:pheight -1,1:pwidth -1]

#Determining MSE
Lmse = np.mean(np.mean(np.square(disp1 - ldisp)))
Rmse =  np.mean(np.mean(np.square(disp2 - rdisp)))

print "MSE OF LEFT DISPARITY %d" %(Lmse)
print "MSE OF RIGHT DISPARITY %d" %(Rmse)

cv2.imshow('Left Disparity[3x3]',ldisp/Ldisp.max())
cv2.imshow('Right Disparity[3x3]',rdisp/Rdisp.max())
