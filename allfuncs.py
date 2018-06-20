import os, time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from astropy.io import fits
import requests, zipfile
from ipywidgets import interact_manual
#from IPython.display import display

#ignore image size warnings
import warnings
#warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", message="Image size")

#function to resize an opened image
def rescale_img(img, newscale, img_width, img_height):
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
def rescale(newscale, img_name="lestermadeline_BW.jpg", img_width=2600, img_height=1600):
    img = Image.open(img_name)
 
    fig = plt.figure()

    new_img = rescale_img(img, newscale, img_width, img_height)
    imshow(np.asarray(new_img), cmap='gray')
    plt.axis('off')
    
    plt.show()
    
    return 

#function to help with rebinning a grey scale image
def rebin_func(value, imgscale, truescale):
    return truescale[np.where(imgscale <= value)[0][-1]]

#function takes an opened image to rebin
def rebin_img(img, nbins):
    bands = img.getbands()
    if len(bands) > 1: img = img.convert('L')
    
    imgarray = np.asarray(img)
    
    if nbins < 0:
        print("Warning: the number of bins has to be greater than 0; defaulting to 1 bin")
        nbins = 0
    if nbins > 256:
        print("Warning: maximum number of bins available is 256")
        
    imgmin = np.min(imgarray)
    imgmax = np.max(imgarray)
    imgscale = np.linspace(imgmin, imgmax, nbins+1)
    truescale = np.linspace(0, 255, nbins+1)
    return [[rebin_func(val, imgscale, truescale) for val in x] for x in imgarray]


def rebin_rgb_func(img, nbins):
    return Image.fromarray(np.uint8(rebin_img(img, nbins)))


def rebin_RGB(nbins, img_name="monterey.png"):
    img = Image.open(img_name)
    r,g,b = img.split()
    rnew = rebin_rgb_func(r, nbins)
    gnew = rebin_rgb_func(g, nbins)
    bnew = rebin_rgb_func(b, nbins)
    new_img = Image.merge("RGB",(rnew, gnew, bnew))
    
    fig = plt.figure()
    imshow(new_img)
    plt.axis('off')
    plt.show()
    
    return 
        

def rebin(nbins, img_name="lestermadeline_BW_5mile.jpg"):
    nbins = int(nbins)
    img = Image.open(img_name)
    
    new_img = rebin_img(img, nbins)
    
    fig = plt.figure()

    imshow(new_img, cmap='gray')
    plt.axis('off')
    
    plt.show()
    
    return 

def rescale_rebin(scale=100, bins=10, img_name="lestermadeline_BW_5mile.jpg", img_width=2600, img_height=1600):
    img = Image.open(img_name)
    resized = rescale_img(img, scale, img_width, img_height)
    recolored = rebin_img(resized, bins)
    
    fig = plt.figure()
    imshow(recolored, cmap='gray')
    plt.axis('off')
    plt.show()

    return

def rescale_rebin_RGB(scale=10, bins=10, img_name="Disneyland.png", img_width=390, img_height=220):
    img = Image.open(img_name)
    resized = rescale_img(img, scale, img_width, img_height)
    recolored = rebin_rgb_func(resized, bins)
    
    fig = plt.figure()
    imshow(recolored)
    plt.axis('off')
    plt.show()

    return


def splitRGB(img_name="rainbowvalley.jpg", flip=True):
    img = Image.open(img_name)
    bandnames = img.getbands()
    r,g,b = img.split()
    outnames = [img_name.split('.')[0]+'_'+band+'.fits' for band in bandnames]
    for band_data, fname in zip([r,g,b], outnames):
        if os.path.exists(fname): os.system('rm '+fname)
        outdata = np.asarray(band_data)
        if flip: outdata = np.flipud(outdata)
        outfits = fits.PrimaryHDU(data=outdata)    
        outfits.writeto(fname)
        
    zf = zipfile.ZipFile(img_name.split('.')[0]+".zip", "w")    
    for fname in outnames: zf.write(fname)
    zf.close()
    
    for fname in outnames: os.system('rm '+fname)
        
    return
 
def downloader(url, img_name):
    f = open(img_name, 'wb')
    f.write(requests.get(url).content)
    f.close()
    return
    