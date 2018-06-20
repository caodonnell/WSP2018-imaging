import os, time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from astropy.io import fits
import requests, zipfile
import ipywidgets as w
#from IPython.display import display

#ignore image size warnings
import warnings
#warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", message="Image size")

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#all of the interactive functions

def start_rescale():
    #v = interact_manual(open_image,image_name="lestermadeline_BW.jpg", image_width=2600, image_height=1600)
    #display(v)
    width = w.FloatText(value=2600., Text='width')
    height = w.FloatText(value=1600., Text='height')
    w.interact_manual(open_rescale, name='lestermadeline_BW.jpg', width=width, height=height)
    return

def open_rescale(name, width, height):
    #img_width = float(image_width)
    #img_height = float(image_height)
    scale = w.FloatText(value=10., Text='scale')
    w.interact_manual(rescale, scale=scale, image_name=w.fixed(name), 
                      image_width=w.fixed(width), image_height=w.fixed(height))
    return


def start_rebin():
    bins = w.IntSlider(value=10, min=1, max=256, step=1,description='bins', continuous_update=False)
    w.interact(rebin, name='lestermadeline_BW_5mile.jpg', bins=bins)
    return

def start_rescale_rebin():
    width = w.FloatText(value=2600., Text='width')
    height = w.FloatText(value=1600., Text='height')
    w.interact_manual(open_rescale_rebin, name='lestermadeline_BW.jpg', width=width, height=height)
    return 

def open_rescale_rebin(name, width, height):
    scale = w.FloatText(value=10., Text='scale')
    bins = w.IntSlider(value=10, min=1, max=256, step=1,description='bins', continuous_update=False)
    w.interact_manual(rescale_rebin, scale=scale, bins=bins, img_name=w.fixed(name), 
                      img_width=w.fixed(width), img_height=w.fixed(height))
    return

def start_splitRGB():
    w.interact_manual(splitRGB, name='rainbowvalley.jpg', flip=w.fixed(True))
    return

def download():
    w.interact_manual(downloader, url='', name='file.jpg')
    return

def start_rebin_RGB():
    bins = w.IntSlider(value=10, min=1, max=256, step=1,description='bins', continuous_update=False)
    w.interact(rebin_RGB, name='Disneyland.png', bins=bins)
    return

def start_rescale_rebin_RGB():
    width = w.FloatText(value=2600., Text='width')
    height = w.FloatText(value=1600., Text='height')
    w.interact_manual(open_rescale_rebin_RGB, name='lestermadeline_BW.jpg', width=width, height=height)
    return 

def open_rescale_rebin_RGB(name, width, height):
    scale = w.FloatText(value=10., Text='scale')
    bins = w.IntSlider(value=10, min=1, max=256, step=1,description='bins', continuous_update=False)
    w.interact_manual(rescale_rebin_RGB, scale=scale, bins=bins, img_name=w.fixed(name), 
                      img_width=w.fixed(width), img_height=w.fixed(height))
    

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#all of the real functions

#---------------------------------------------------------------------------------

#rescaling an image 

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
def rescale(scale, image_name="lestermadeline_BW.jpg", image_width=2600, image_height=1600):
    img = Image.open(image_name)
 
    fig = plt.figure()
    newscale = scale
    new_img = rescale_img(img, newscale, image_width, image_height)
    imshow(np.asarray(new_img), cmap='gray')
    plt.axis('off')
    
    plt.show()
    img.close()
    return 

#---------------------------------------------------------------------------------
#rebinning a greyscale image

#function to help with rebinning a grey scale image
#def rebin_func(value, imgscale, truescale):
#    return truescale[np.where(imgscale <= value)[0][-1]]

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
    imgscale[-1] = imgscale[-1] + 1 #to capture max value
    truescale = np.linspace(0, 255, nbins)
    newimg = truescale[0]*np.ma.masked_where(np.logical_and(imgarray >= imgscale[0], imgarray < imgscale[1]), imgarray, copy=False).mask
    for i in range(1, nbins): 
        newimg = newimg+truescale[i]*np.ma.masked_where(np.logical_and(imgarray >= imgscale[i], imgarray < imgscale[i+1]), imgarray, copy=False).mask
    return newimg
    #return [[rebin_func(val, imgscale, truescale) for val in x] for x in imgarray]


def rebin(bins, name="lestermadeline_BW_5mile.jpg"):
    img = Image.open(name)
    
    new_img = rebin_img(img, bins)
    
    fig = plt.figure()

    imshow(new_img, cmap='gray')
    plt.axis('off')
    
    plt.show()
    img.close()
    return 

#---------------------------------------------------------------------------------
#rebinning an RGB image (uses the rebin_img function on each band)

def array2Image(array):
    return Image.fromarray(np.uint8(array))

def rebin_rgb_func(img, nbins):
    r,g,b = img.split()
    rnew = array2Image(rebin_img(r, nbins))
    gnew = array2Image(rebin_img(g, nbins))
    bnew = array2Image(rebin_img(b, nbins))
    for band in [rnew, gnew, bnew]:
        bandarray = np.asarray(band)
        #print(np.unique(bandarray))
    return Image.merge("RGB", (rnew, gnew, bnew))
    
def rebin_RGB(bins, name="monterey.png"):
    img = Image.open(name)
    
    new_img = rebin_rgb_func(img, bins)
    
    fig = plt.figure()
    imshow(new_img)
    plt.axis('off')
    plt.show()
    img.close()
    return 


#---------------------------------------------------------------------------------
#functions to combine the rescale and rebin methods

def rescale_rebin(scale=100, bins=10, img_name="lestermadeline_BW_5mile.jpg", img_width=2600, img_height=1600):
    img = Image.open(img_name)
    resized = rescale_img(img, scale, img_width, img_height)
    recolored = rebin_img(resized, bins)
    
    fig = plt.figure()
    imshow(recolored, cmap='gray')
    plt.axis('off')
    plt.show()
    img.close()
    return

def rescale_rebin_RGB(scale=10, bins=10, img_name="Disneyland.png", img_width=390, img_height=220):
    img = Image.open(img_name)
    resized = rescale_img(img, scale, img_width, img_height)
    recolored = rebin_rgb_func(resized, bins)
    
    fig = plt.figure()
    imshow(recolored)
    plt.axis('off')
    plt.show()
    img.close()
    return


#---------------------------------------------------------------------------------
#some other useful methods: split an image into RGB fits files, download an image from the internet

def splitRGB(name="rainbowvalley.jpg", flip=True):
    img = Image.open(name)
    bandnames = img.getbands()
    r,g,b = img.split()
    outnames = [name.split('.')[0]+'_'+band+'.fits' for band in bandnames]
    for band_data, fname in zip([r,g,b], outnames):
        if os.path.exists(fname): os.system('rm '+fname)
        outdata = np.asarray(band_data)
        if flip: outdata = np.flipud(outdata)
        outfits = fits.PrimaryHDU(data=outdata)    
        outfits.writeto(fname)
        
    zname = name.split('.')[0]+".zip"
    zf = zipfile.ZipFile(zname, "w")    
    for fname in outnames: zf.write(fname)
    zf.close()
    
    for fname in outnames: os.system('rm '+fname)
    img.close()
    print(name+' split into RGB files - check the file directory for '+zname)
    return
 
def downloader(url, name):
    f = open(name, 'wb')
    f.write(requests.get(url).content)
    f.close()
    print('downloaded image into '+name)        
    return
    