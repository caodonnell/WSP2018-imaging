import os#, sys, glob, time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from astropy.io import fits

#ignore image size warnings
import warnings
#warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", message="Image size")

def testfunc(n):
    print(n)
    return

#function to resize an opened image
def resize_img(img, newscale, img_width, img_height):
    px_width, px_height = img.size
    widthscale = 1.0*img_width/px_width
    heightscale = 1.0*img_height/px_height
    
    if newscale < widthscale or newscale < heightscale:
        print("Warning: Your desired image scale is a finer resolution than in the original image; defaulting to the finest scale available")
        newscale = max(widthscale, heightscale)
    if newscale > img_width or newscale > img_height:
        print("Warning: Your desired image scale is larger than the original image; defaulting to the image size")
        newscale = min(img_width, img_height)
          
    new_px_width = int(1.0*px_width/(1.0*newscale/widthscale))
    new_px_height = int(1.0*px_height/(1.0*newscale/heightscale))
    #print(new_px_width, new_px_height)
    return img.resize((new_px_width, new_px_height))

#scale and img width/height have to be in same distance units
#in this case, miles
def resize(newscale, img_name='lestermadeline_BW.jpg', img_width=2600, img_height=1600):
    img = Image.open(img_name)
 
    fig = plt.figure()

    new_img = resize_img(img, newscale, img_width, img_height)
    imshow(np.asarray(new_img), cmap='gray')
    plt.axis('off')
    
    plt.show()
    
    return 

#function to help with rebinning a grey scale image
def rebin_func(value, imgscale):
    return np.where(imgscale <= value)[0][-1]

#function takes an opened image to rebin
def rebin_img(img, nbins):
    imgarray = np.asarray(img)
    
    if nbins < 0:
        print("Warning: the number of bins has to be greater than 0; defaulting to 1 bin")
        nbins = 0
    if nbins > 255:
        print("Warning: maximum number of bins available is 255")
        
    imgmin = np.min(imgarray)
    imgmax = np.max(imgarray)
    imgscale = np.linspace(imgmin, imgmax, nbins+1)
    return [[rebin_func(val, imgscale) for val in x] for x in imgarray]
        

def rebin(nbins, img_name='lestermadeline_BW_5mile.jpg'):
    img = Image.open(img_name)
    imgarray = np.asarray(img)
    
    new_img = rebin_img(img, nbins)
    
    fig = plt.figure()

    imshow(new_img, cmap='gray')
    plt.axis('off')
    
    plt.show()
    
    return 

def pix_and_bins(scale=100, bins=10, img_name='lestermadeline_BW_5mile.jpg', img_width=2600, img_height=1600):
    img = Image.open(img_name)
    resized = resize_img(img, scale, img_width, img_height)
    recolored = rebin_img(resized, bins)
    
    fig = plt.figure()
    imshow(recolored, cmap='gray')
    plt.axis('off')
    plt.show()

    return


def splitRGB(img_name='rainbowvalley.jpg', flip=True):
    img = Image.open(img_name)
    bands = img.getbands()
    r,g,b = img.split()
    for band, name in zip([r,g,b], bands):
        fname = img_name.split('.')[0]+'_'+name+'.fits'
        if os.path.exists(fname): os.system('rm '+fname)
        outdata = np.asarray(band)
        if flip: outdata = np.flipud(outdata)
        outfits = fits.PrimaryHDU(data=outdata)    
        outfits.writeto(fname)
    return
        
    