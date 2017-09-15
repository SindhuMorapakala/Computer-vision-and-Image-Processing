a = [15,7,2,8,32,81,3,1,80]
for i in range(0,len(a)-1):
    for j in range(0,len(a) - i - 1):
        if a[j] > a[j+1]:
            a[j],a[j+1] = a[j+1],a[j]
for i in range(0,len(a)):
    print(a[i])