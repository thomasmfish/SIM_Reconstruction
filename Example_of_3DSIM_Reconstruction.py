# -*- coding: utf-8 -*-
"""
An example of running the 3D structured illumination microscopy image reconstruction codes
@copyright, Ruizhe Lin and Peter Kner, University of Georgia, 2021

"""

import numpy as np
import tifffile as tf
from hifi_sim import sim_3drecon_p36 as si

def main():
    fns = r'C:\Users\jin81932\Desktop\TestSIM\20210205-111731_NV10G2_D4C_FL'  # raw 3dsim data file
    nphases = 5
    nangles = 3
    # fns is ordered: angles, zs, phases (0, 1, 2)
    # target is: zs, angles, phases (0, 2, 1)
    with tf.TiffFile(fns) as tif:
        array = tif.asarray()
    nz = len(array) / (nangles * nphases)
    tmp_phases = np.zeros((nz * nphases, *array.shape[1:]))
    for i in range(nangles):
        for j in range(0, nz):
            itr = j * nphases
            tmp_phases[itr:,:, :] = array[itr:itr + nz, :, :]
        tmp_phases[]
    p = si.si3D(
        fns, # filepath or ndarray NOTE: order of images should be phases, angles, zslices
        nphases, # number of phases
        nangles, # number of angles
        0.488, # wavelength in microns
        0.9, # numerical aperture
        0.125, # pixel size in microns
        0.125, # z step in microns
        )

    #set parameters 
    p.mu = 0.001
    p.strength = 1.0
    p.sigma = 4
    p.eta = 0.1
    p.expn = 1.    
    p.axy = 0.8
    p.az = 0.8
    p.zoa = 1.

    #initiate angles and spacings estimation
    x0 = np.array([3.147, 0.285]) 
    x1 =  np.array([-1.103, 0.286])
    x2 =  np.array([1.019, 0.271])
    z0 = np.array([1.45])
    z1 = np.array([1.45])
    z2 = np.array([1.35])

    #search 1st angle
    p.separate(0)
    p.shift0() 
    x0_2 = p.mapoverlap2(x0[0], x0[1], nps=10, r_ang=0.02, r_sp=0.02)
    x0_2 = p.mapoverlap2(x0_2[0], x0_2[1], nps=10, r_ang=0.005, r_sp=0.005)
    x0_2 = p.mapoverlap2(x0_2[0], x0_2[1], nps=10, r_ang=0.005, r_sp=0.005)
    z0 = p.mapoverlapz(x0_2[0], x0_2[1], z0[0], nps=50, r_spz=0.25)
    x0_1 = p.mapoverlap1(x0_2[0], x0_2[1], z0[0], nps=10, r_ang=0.005, r_sp=0.005)
    x0_1 = p.mapoverlap1(x0_1[0], x0_1[1], z0[0], nps=10, r_ang=0.005, r_sp=0.005)

    #search 2nd angle
    p.separate(1)
    p.shift0()
    x1_2 = p.mapoverlap2(x1[0], x1[1], nps=10, r_ang=0.02, r_sp=0.02)
    x1_2 = p.mapoverlap2(x1_2[0], x1_2[1], nps=10, r_ang=0.005, r_sp=0.005)
    x1_2 = p.mapoverlap2(x1_2[0], x1_2[1], nps=10, r_ang=0.005, r_sp=0.005)
    z1 = p.mapoverlapz(x1_2[0], x1_2[1],  z1[0], nps=50, r_spz=0.25)
    x1_1 = p.mapoverlap1(x1_2[0], x1_2[1], z1[0], nps=10, r_ang=0.005, r_sp=0.005)
    x1_1 = p.mapoverlap1(x1_1[0], x1_1[1], z1[0], nps=10, r_ang=0.005, r_sp=0.005)

    #search 3rd angle
    p.separate(2)
    p.shift0()
    x2_2 = p.mapoverlap2(x2[0], x2[1], nps=10, r_ang=0.02, r_sp=0.02)
    x2_2 = p.mapoverlap2(x2_2[0], x2_2[1], nps=10, r_ang=0.005, r_sp=0.005)
    x2_2 = p.mapoverlap2(x2_2[0], x2_2[1], nps=10, r_ang=0.005, r_sp=0.005)
    z2 = p.mapoverlapz(x2_2[0], x2_2[1],  z2[0], nps=50, r_spz=0.25)
    x2_1 = p.mapoverlap1(x2_2[0], x2_2[1], z2[0], nps=10, r_ang=0.005, r_sp=0.005)
    x2_1 = p.mapoverlap1(x2_1[0], x2_1[1], z2[0], nps=10, r_ang=0.005, r_sp=0.005)    

    #display results
    print(x0_1)
    print(x0_2)
    print(z0)
    print(x1_1)
    print(x1_2)
    print(z1)
    print(x2_1)
    print(x2_2)
    print(z2)

    #save results
    fn = fns.split('.')[0] + '.txt'
    np.savetxt(fn, ('1st angle', x0_1, z0, x0_2, 
                    '2nd angle', x1_1, z1, x1_2, 
                    '3rd angle', x2_1, z2, x2_2), fmt='%s')

    # End of Parameter computation
    del p


if __name__ == "__main__":
    main()
