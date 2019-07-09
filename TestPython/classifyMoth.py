import os
import cv2 
import numpy as np
import itertools
from readcsv import saveData
from readcsv import readData
from getColor import getColor
from getColor import getColor2
from callee import roi


# return value (a,b,c)
# a: Message
# b: The number of Specific bug in the Picture
# c: if the function is failed to run completely - return False.
#    if the function is succeed to run           - return True

def classifyMoth(dataDir,Save=False,NumberofType=4,BugName=["1","2","3","4"]):
    
    # Set the test value
    dirName = os.getcwd()       ##check is it right?
    # print(dirName)
    # print("right?")
    # Filter the Error
    if NumberofType != len(BugName):
        return ("Number of Type and Numberof BugName are not same",0,False)


    # Get Saved Moth data
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=filedir[0:strlen-11]+'/MothData/'
    dirlist=os.listdir(filedir)
    fileList=[]
    for i in dirlist:
        if i.find('csv') is not -1:
            if i.find('Mothdata') is not -1:
                fileList.append(filedir+i)
        # print(filedir+i)    
    dist_data_total=readData(fileList)

    nonfileList=[]
    #dist_non_data_total=readData(nonfileList)
    dist_non_data_total=[[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]]
    # Get Color from moth data
    dist_avg_data_total=[]
    dist_avg_non_data_total=[]
    #####################################!!!!!!!!
    dataDir=dirName[0:strlen-11]+"Picture/Test/03.png"
    

    data=getColor(dataDir,5)
    newdata=np.array(data)

    # Calculate the avearage of the existing data.
    for dist_data in dist_data_total:
        dist_avg_data=[]
        if dist_data[0]==[]:
            print("")
            break
        y = dist_data.astype(np.float)
        dist_avg_data=np.average(y,axis=0)
        avglist =[]
        # Change the scala row data to point row data
        for j in range(0,5):
            avglist.append(dist_avg_data[j*3:j*3+3])
        dist_avg_data_total.append(avglist)

    for dist_non_data in dist_non_data_total:
        dist_avg_non_data=[]
        if dist_non_data[0]==[]:
            print("")
            break
        y = dist_non_data.astype(np.float)
        dist_avg_non_data=np.average(y,axis=0)
        avglist =[]
        # Change the scala row data to point row data
        for j in range(0,5):
            avglist.append(dist_avg_non_data[j*3:j*3+3])
        dist_avg_non_data_total.append(avglist)


    # Set initial value
    lowdist=1
    k=0

    # Set a very very high value
    origin=10000000
    clusterDistance=1000000000

    # Calculte all combination between 5-point of exsisting average data and 5-point of new data
    # Find the order of 5-point data that has the smallest distance value.
    for l,r in enumerate(dist_avg_data_total):
        for i in itertools.permutations([1,2,3,4,0],5):
            distsum=0
            for j,k in enumerate(i):
                # Sum of square of distances between two points.
                distsum=distsum+np.linalg.norm(r[j]-data[k])**2
            if distsum < origin:
                origin = distsum
                bestCombn = i
        if origin < clusterDistance:
            clusterDistance=origin
            cluster=l
            

    for l,r in enumerate(dist_avg_non_data_total):
        for i in itertools.permutations([1,2,3,4,0],5):
            distsum=0
            for j,k in enumerate(i):
                # Sum of square of distances between two points.
                distsum=distsum+np.linalg.norm(r[j]-data[k])**2
            if distsum < clusterDistance:
                cluster=-1
            if cluster==-1:
                break
        if cluster==-1:
            break

    # change the new image data to
    if clusterDistance>80000:
        cluster =-1
    newdata=[]
    for j in bestCombn:
        newdata.append(data[j])
    
    if Save == True & cluster != -1:
        saveData(newdata,cluster)

    # return the meassage informing type of bug
    if cluster == -1:
        return("Meaningless",0 ,True)
    else:
        return("The moth is "+BugName[cluster],1,True)    