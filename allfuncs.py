import os, sys, glob
import numpy as np

def testfunc(n):
    print(n)
    return

#scale and img width/height have to be in same distance units
#in this case, miles
def resize(newscale, imgname='lestermadeline_BW.jpg', img_width=2600, img_height=1600, fig_width=12, fig_height=10):
    img = Image.open(imagename)
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