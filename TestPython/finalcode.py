from getColor import getColor2
from combined_code import classifyMoth

from save_as_csv import saveDataAsCsv
import time
import os
# import dlib
import cv2
import numpy as np
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib import urlopen



def combined_code (data,sizethreshold,distance_threshold,autoSetting=False,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1
,Save=False,imageShow=False,NumberofType=4,BugName=["1","2","3","4"],newFile=False,saveImage=False):

    each_labeled=roi(data,sizethreshold,imageShow=imageShow)

    datalist=getColor2(each_labeled,distance_threshold,autoSetting=autoSetting,imageShow=imageShow,hlist=hlist,sup=sup,sdown=sdown,vup=vup,vdown=vdown)
    
    message,clusterSum,clusterData,TrueorFalse=classifyMoth(datalist,Save,NumberofType,BugName)
    
    saveDataAsCsv(data=b1, bugName=BugName, newFile=newFile)

    if saveImage == True:
        saveDataAsImage(imageData=each_labeled,clusterData=c1,bugName=BugName)

    return message,clusterSum,clusterData,TrueorFalse


















def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
    # try: #python3
    #     resp = urlopen(url)
    # except: #python2
    #     resp = urlopen(url)    
	resp=urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image


def combined_code_url (data_url, sizethreshold,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1
,Save=False,imageShow=False,NumberofType=4,BugName=["1","2","3","4"]):
    data=url_to_image(data_url)

    now=time.localtime()
    outputFileName =str(now.tm_year)+"_"+str(now.tm_mon)+"_"+str(now.tm_mday)+"_"+str(now.tm_hour)+"_"+str(now.tm_min)+"_"+str(now.tm_sec)+"."+ "jpg"
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=filedir[0:strlen-11]
    filedir=filedir+'/Picture/MJPG/'+outputFileName
    cv2.imshow(filedir,data)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(filedir, data)
    a1, b1, c1=combined_code(filedir,sizethreshold,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1
,Save=False,imageShow=False,NumberofType=4,BugName=["1","2","3","4"])
    return a1, b1, c1
 