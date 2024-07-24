################################################
## Python script to create temporal
## Tick mask for LymeApp
## This version uses 8-day decad data only
##
## Scriptname: tempporalTickMask-Process.py
##
## Version: 0.9
##
##  Author: Neil Alexander
##  Updated and Edited by: Roya Olyazadeh
## Environmental Research Group Oxford
##
## Edited Date: 11/04/23
##
################################################
## Libraries ##
import os
import os.path
import time
import glob

## Global variables and working directories
# inDir = '/cumtemp/data/'
inDir = '/media/idata/cumtemp/VIIRS/AppEEARS/'



### To download data https://appears.earthdatacloud.nasa.gov

## Define variables
year = '2024'
inDirVNP21A2 = inDir + '/VNP21A2/' + year + '/'
inDirVNP21A1 = inDir + '/VNP21A1D/'+ year + '/'
inVNP21A2=[]
inVNP21A1=[]
TilesA2 = []
TilesA1 = []
mTiffs = []
mTiffsA1 = []
o68Tiffs = []
c68Tiffs = []
missTile = []
startTime = time.strftime('%X %x')


  
## Over6: Recode 1 if >279.15 or 13958 scaled by 0.02   NodataValue has been replaced from 0 to -999
inVNP21A2 = glob.glob(inDirVNP21A2 + "*.tif")
for tifFile in inVNP21A2:
  YY = tifFile[-17:-15]
  day = tifFile[-15:-12]
  print day
  tt = str(int(round(int(day)/8+0.5))).zfill(2)
  o6Tiff = inDir + "tif/vo68/A2/"+ year +"/ER" + YY + tt + "O68.tif"
  u6Tiff = inDir + "tif/vo68/A2/"+ year +"/ER" + YY + tt + "U68.tif"
  o26Tiff = inDir + "tif/vo68/A2/"+ year +"/ER"  + YY + tt +"O26.tif"
  if not os.path.isfile(o6Tiff):
    os.system("gdal_calc.py -A " + tifFile + " --outfile=" + o6Tiff + " --calc=\"((A*(A>13957)/A)) \" --NoDataValue=-999")
  if not os.path.isfile(u6Tiff):
    os.system("gdal_calc.py -A " + tifFile + " --outfile=" + u6Tiff + " --calc=\"((A*(logical_and(A>0,A<13958))/A))\" --NoDataValue=-999")
  if not os.path.isfile(o26Tiff):
    os.system("gdal_calc.py -A " + tifFile + " --outfile=" + o26Tiff + " --calc=\"((A*(A>14958))/A)\" --NoDataValue=-999")
  o68Tiffs.append(o6Tiff)


# 1 day processing
inVNP21A1 = glob.glob(inDirVNP21A1 + "*.tif")
for tifFile1 in inVNP21A1:
  YY = tifFile1[-17:-15]
  day = tifFile1[-15:-12]  
  ttt = str(int(day)).zfill(3)
  outTiffA1 = inDir + "tif/vo68/A1/" + year +"/ER" + YY + ttt +  "A1O68.tif"
  if not os.path.isfile(outTiffA1):
    os.system("gdal_calc.py -A " + tifFile1 + " --outfile=" + outTiffA1 + " --calc=\"((A*(A>13957)/A))\" --NoDataValue=-999" )


## consec8: 2 consecutive dekadals over6 = 1
o68Tiffs.sort()
for o68Tiff in o68Tiffs: 
  tt = o68Tiff[-9:-7]
  yy = o68Tiff[-11:-9]
  yyprev = int(yy)-1 
  if int(tt)-1 == 0:
    yyttPrev = str(yyprev).zfill(2) + '46'
  else:
    yyttPrev = yy + str(int(tt)-1).zfill(2)  
  o68Prev =  o68Tiff[:-11] + yyttPrev + "O68.tif"
  c68Prev = inDir + "tif/vc68/"+ year +"/ER" + yyttPrev + "C68.tif"
  outTiffTemp = inDir + "tif/vc68/"+ year +"/temp/ER" + yy + tt + "C68.tif"
  outTiff = inDir + "tif/vc68/"+ year +"/ER"  + yy + tt + "C68.tif"
  o68TiffsA1 = []
  if os.path.isfile(o68Prev) == True:
    for x in range (8):
      ttt = str((8*int(tt)-7) + x).zfill(3)
      o68A1 = inDir + "tif/vo68/A1/" + year +"/ER" + yy + ttt + "A1O68.tif"
      o68TiffsA1.append(o68A1)
  if os.path.isfile(c68Prev) == True:
    if os.path.isfile(outTiffTemp) == False:
      os.system("gdal_calc.py -A " + o68TiffsA1[0] + " -B " + o68TiffsA1[1] + " -C " + o68TiffsA1[2] + " -D " + o68TiffsA1[3] + " -E " + o68TiffsA1[4] + " -F " + o68TiffsA1[5] + " -G " + o68TiffsA1[6] + " -H " + o68TiffsA1[7] + " -I " + o68Tiff + " -J " + o68Prev + " -K " + c68Prev + " --outfile " + outTiffTemp + " --calc=\"maximum((K+((I*J)*(K==0))),(((A+B+C+D+E+F+G+H)>3)/((A+B+C+D+E+F+G+H)>3)))\"")
      if int(tt) > 3:
        yyttPrev2 = yy + str(int(tt)-2).zfill(2)
        u68Prev2 =  o68Tiff[:-11] + yyttPrev2 + "U68.tif"
        u68Prev1 =  o68Tiff[:-11] + yyttPrev + "U68.tif"
        u68Tiff =  o68Tiff[:-7] + "U68.tif"
        o26Prev1 =  o68Tiff[:-11] + yyttPrev + "O26.tif"
        o26Tiff =  o68Tiff[:-7] + "O26.tif"
        outTiff2 = inDir + "tif/vc68/" + year +"/fin/ER" + yy + tt + "C68.tif"
        os.system("gdal_calc.py -A " + u68Tiff + " -B " + u68Prev1 + " -C " + u68Prev2 + " -D " + o26Tiff + " -E " + o26Prev1 + " -F " + outTiffTemp + " --outfile " + outTiff + " --calc=\"minimum(F*((D*E)==0), F*((A*B)==0))\"")
      else:
       os.system("mv " + outTiffTemp + " " + outTiff)
  elif os.path.isfile(o68Prev) == True:
    os.system("gdal_calc.py -A " + o68TiffsA1[0] + " -B " + o68TiffsA1[1] + " -C " + o68TiffsA1[2] + " -D " + o68TiffsA1[3] + " -E " + o68TiffsA1[4] + " -F " + o68TiffsA1[5] + " -G " + o68TiffsA1[6] + " -H " + o68TiffsA1[7] + " -I " + o68Tiff + " -J " + o68Prev + " --outfile " + outTiff + " --calc=\"maximum((I*J),(((A+B+C+D+E+F+G+H)>3)/((A+B+C+D+E+F+G+H)>3)))\"")
  c68Tiffs.append(outTiff)
  print outTiff

for c68Tiff in c68Tiffs:
  outTiff = inDir + "tif/vc68/" + year +"/WGS/" + c68Tiff[-13:-7] + "C68.tif"
  os.system("gdalwarp -s_srs \"+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs\" -t_srs EPSG:4326 -r near -tr 0.008333333 0.008333333 -te -32 10 69 82 -te_srs EPSG:4326 -of GTiff " + c68Tiff + " " + outTiff)


os.system("rm " + inDir + "tif/vc68/"+ year +"/temp/*.tif")
endTimeR = time.strftime('%X %x')

print startTime + " - Start time"
print endTimeR + " - Reflectance bands complete"
  
