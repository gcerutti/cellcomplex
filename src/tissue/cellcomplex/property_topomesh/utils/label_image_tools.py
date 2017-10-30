import numpy as np
import scipy.ndimage as nd

from copy import deepcopy


def euclidean_sphere(radius, voxelsize=(1,1,1)):
    x,y,z = np.mgrid[-radius/float(voxelsize[0]):radius/float(voxelsize[0])+1,
                     -radius/float(voxelsize[1]):radius/float(voxelsize[1])+1,
                     -radius/float(voxelsize[2]):radius/float(voxelsize[2])+1]

    distance = np.linalg.norm([x*float(voxelsize[0]),y*float(voxelsize[1]),z*float(voxelsize[2])],axis=0)

    return (distance<=radius).astype(np.uint8)


def label_median_filter(img,radius=1):

    sphere = euclidean_sphere(radius,voxelsize=img.voxelsize)
    # print sphere.sum()

    from time import time

    start_time = time()
    print "--> Counting labels inside spherical neighborhoods..."

    image_labels = np.unique(img)
    count_max = np.zeros_like(img).astype(int)
    filtered_img = deepcopy(img)

    for l in image_labels:
        label_start_time = time()
        print "  --> Cell ",l

        label_img = (img==l).astype(int)

        label_coords = np.where(label_img)
        bbox = (np.maximum([0,0,0],np.min(label_coords,axis=1)-(radius/np.array(img.voxelsize)).astype(int)),
                np.minimum(np.array(img.shape)-1,np.max(label_coords,axis=1)+(radius/np.array(img.voxelsize)).astype(int)))
        print bbox

        label_count = np.zeros_like(img).astype(int)

        label_count[bbox[0][0]:bbox[1][0],bbox[0][1]:bbox[1][1],bbox[0][2]:bbox[1][2]] = nd.filters.convolve(label_img[bbox[0][0]:bbox[1][0],bbox[0][1]:bbox[1][1],bbox[0][2]:bbox[1][2]],sphere)

        # print "    ",(label_count>count_max).sum()," voxels changed"

        filtered_img[label_count>count_max] = l
        count_max = np.max([count_max,label_count],axis=0)

        label_end_time = time()
        #print "  <-- Cell ",l," : ",np.round(label_img.sum()*np.prod(img.voxelsize),2)," microm3 [",label_end_time-label_start_time,"s]"
        print "  <-- Cell ",l,"    [",label_end_time-label_start_time,"s]"

    end_time = time()
    print "<-- Counting labels inside spherical neighborhoods [",end_time-start_time,"s]"

    return filtered_img



