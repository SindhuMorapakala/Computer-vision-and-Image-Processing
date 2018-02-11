import cv2
import numpy as np

View1 = cv2.imread('F:\Mugdha\CVIP project\Data\First.png')
GView1 = cv2.cvtColor(View1, cv2.COLOR_BGR2GRAY)
H1, W1 = GView1.shape

View2 = cv2.imread('F:\Mugdha\CVIP project\Data\Fifth.png')
GView2 = cv2.cvtColor(View2, cv2.COLOR_BGR2GRAY)
H2, W2 = GView2.shape

Cost = np.zeros((W1+1,W2+1),dtype=int)
M = np.zeros((W1+1,W2+1),dtype=int)

def opt_match(r):
    Occlusion = 20
    Cost[0,0] = 0
    for i in range(1,W1+1):
        Cost[i,0] = i*Occlusion
    for i in range(1,W2+1):
        Cost[0,i] = i*Occlusion
    for i in range(1,W1+1):
        for j in range(1,W2+1):
            Idiff = abs(GView1[r,i-1] - GView2[r,j-1])
            min1 = Cost[i-1,j-1] + Idiff
            min2 = Cost[i-1,j] + Occlusion
            min3 = Cost[i,j-1] + Occlusion
            cmin = min(min1,min2,min3)
            Cost[i,j] = cmin
            if(min1==cmin):
                M[i-1,j-1] = 1
            if(min2==cmin):
                M[i-1,j-1] = 2
            if(min3==cmin):
                M[i-1,j-1] = 3
 
Ldisparity = np.zeros((H1,W1),dtype=int) 
Rdisparity = np.zeros((H2,W2),dtype=int)
  
def reconstruction(r):
    i = W1-1
    j = W2-1
    while(i>=0 and j>=0):
        if(M[i,j]==1):
            Ldisparity[r,i] = abs(i-j)
            Rdisparity[r,j] = abs(j-i)
            i = i - 1 
            j = j - 1
        elif(M[i,j]==2):
            i = i - 1
        elif(M[i,j]==3):
            j = j - 1
    
                
for r in range(0,H1):
     opt_match(r)
     reconstruction(r)
     
#MSE Calculation

diff1 = np.zeros((H1,W1),dtype=int)
CGT1 = cv2.imread('F:\Mugdha\CVIP project\Data\disp1.png')
GT1 = cv2.cvtColor(CGT1, cv2.COLOR_BGR2GRAY)
for i in range(0,H1):
    for j in range(0,W1):
        if(Ldisparity[i,j] !=0):
            diff1[i,j] = abs(GT1[i,j] - Ldisparity[i,j])
SqArray = np.square(diff1)
sum1 = np.sum(SqArray)
mse1 = sum1/(H1*W1)

diff2 = np.zeros((H1,W1),dtype=int)
CGT2 = cv2.imread('F:\Mugdha\CVIP project\Data\disp5.png')
GT2 = cv2.cvtColor(CGT2, cv2.COLOR_BGR2GRAY)
for i in range(0,H1):
    for j in range(0,W1):
        if(Rdisparity[i,j] !=0):  
            diff2[i,j] = abs(GT2[i,j] - Rdisparity[i,j])
SqArray = np.square(diff2)
sum2 = np.sum(SqArray)
mse2 = sum2/(H1*W1)

print mse1, mse2

cv2.imshow('Left Disparity',np.uint8(Ldisparity))  
cv2.imshow('Right Disparity',np.uint8(Rdisparity)) 