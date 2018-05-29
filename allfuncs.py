import os, sys, glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

#ignore image size warnings
import warnings
#warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", message="Image size")

def testfunc(n):
    print(n)
    return


#scale and img width/height have to be in same distance units
#in this case, miles
#NEED TO PUT MIN/MAX CONTROLS
def resize(newscale, img_name='lestermadeline_BW.jpg', img_width=2600, img_height=1600, fig_width=12, fig_height=10):
    img = Image.open(img_name)
    px_width, px_height = img.size
    
    widthscale = 1.0*img_width/px_width
    heightscale = 1.0*img_height/px_height
    
    new_px_width = int(1.0*px_width/(1.0*newscale/widthscale))
    new_px_height = int(1.0*px_height/(1.0*newscale/heightscale))
    #print(new_px_width, new_px_height)
    
    plt.rcParams['figure.figsize'] = [fig_width, fig_height]
    fig = plt.figure()

    new_img = img.resize((new_px_width, new_px_height))
    imshow(np.asarray(new_img), cmap='gray')
    plt.axis('off')
    
    plt.show()
    
    return 

#function to help with rebinning a grey scale image
def rebin_func(value, imgscale):
    return np.where(imgscale <= value)[0][-1]

#NEED TO ADD MIN/MAX CONTROL
def rebin(nbins, img_name='lestermadeline_BW_5mile.jpg', fig_width=12, fig_height=10):
    img = Image.open(img_name)
    imgarray = np.asarray(img)
    
    imgmin = np.min(imgarray)
    imgmax = np.max(imgarray)
    imgscale = np.linspace(imgmin, imgmax, nbins+1)
    new_img = [[rebin_func(val, imgscale) for val in x] for x in imgarray]
    
    plt.rcParams['figure.figsize'] = [fig_width, fig_height]
    fig = plt.figure()

    imshow(new_img, cmap='gray')
    plt.axis('off')
    
    plt.show()
    
    return 
    