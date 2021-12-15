import pandas as pd
import  numpy as np
import sys
import math as m

# from collections import defaultdict
def topsis(filename,weights,impacts,outputFile):
    

    # filename=sys.argv[1]
    # weights = sys.argv[2]
    # impacts = sys.argv[3]
    # outputFile=sys.argv[4]

    weights = list(map(float ,weights.split(',')))
    impacts = list(map(str ,impacts.split(',')))

    for imp in  impacts:
        if imp =='+' or imp=='-':
            pass
        
        else:
            raise Exception("impact must be positive(+) or negative (-)")
    try:
        dataset = pd.read_csv(filename,index_col=False)
    except:
        print("Input Error:File Read Error/File Not Found")
        sys.exit()
    data=[]
    print(dataset)
    try:
        data=dataset.iloc[ :,1:].values.astype(float)
    except ValueError:
        print("Not all data in CSV file is numeric")
        sys.exit()
    data=dataset.iloc[ :,1:].values.astype(float)
    (r,c)=data.shape

    if c<3:
        raise Exception("Insufficient data in CSV file(less than 3 columns)")
    s=sum(weights)

    if len(weights) != c:
        raise Exception("Insufficient Weights")
    if len(impacts) != c:
        raise Exception("Insufficient Impacts")


    for i in range(c):
        weights[i]/=s


    a=[0]*(c)


    for i in range(0,r):
        for j in range(0,c):
            a[j]=a[j]+(data[i][j]*data[i][j])


    for j in range(c):
        a[j]=m.sqrt(a[j])


    for i in range(r):
        for j in range(c):
            data[i][j]/=a[j]
            data[i][j]*=weights[j]

    ## WEIGHTED NORMALIZED DECISION MATRIX


    ideal_positive=np.amax(data,axis=0) # MAX IN VERTICAL COL
    ideal_negative=np.amin(data,axis=0) # MIN IN EACH COL

    for i in range(len(impacts)):
        if(impacts[i]=='-'):         # SWAPPING TO STORE REQUIRED IN IDEAL_POSITIVE
            temp=ideal_positive[i]
            ideal_positive[i]=ideal_negative[i]
            ideal_negative[i]=temp

    dist_pos=list()
    dist_neg=list()

    for i in range(r):
        s=0
        for j in range(c):
            s+=pow((data[i][j]-ideal_positive[j]), 2)

        dist_pos.append(float(pow(s,0.5)))


    for i in range(r):
        s=0
        for j in range(c):
            s+=pow((data[i][j]-ideal_negative[j]), 2)

        dist_neg.append(float(pow(s,0.5)))


    performance_score=dict()

    for i in range(r):
        performance_score[i+1]=dist_neg[i]/(dist_neg[i]+dist_pos[i])

    b=sorted(performance_score.items(), key=lambda x: x[1],reverse=True)
    for i in range(r):
        b[i]=b[i]+(i+1,)

    b=sorted(b,key=lambda x:x[0])

    col=["Topsis Score","Rank"]

    for i in range(2):
        dataset[col[i]]=[x[i+1] for x in b]
    print(dataset)
    return dataset
    # dataset.to_csv(outputFile,index=False)

