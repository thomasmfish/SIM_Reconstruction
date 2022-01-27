# -*- coding: utf-8 -*-
"""

These functions generate the Zernike functions on the unit circle
@copywrite, Ruizhe Lin and Peter Kner, University of Georgia, 2019

"""

import numpy as np
from scipy.special import factorial as fac
from operator import itemgetter
    
def jnm(mx):
    ''' Noll Zernike ordering !!! '''
    a = []
    for n in range(mx):
        for m in range(-n,n+1,2):
            a.append((n,m,abs(m)))
    #a.sort(lambda a,b: int(a[0]-b[0] or a[2]-b[2] or a[1]-b[1]))
    a.sort(key=itemgetter(0,2,1))
    c = []
    for j,t in enumerate(a):
        c.append(t[:2])
    b = np.array(c)
    #return dict(zip(c,np.arange(mx)))
    return (b,dict(zip(c,np.arange(len(a)))))

global nj, nb
nb,nj = jnm(15)

def rhofunc(i,j,x0,y0,Nx):
#    i = (i<=Nx/2)*i + (i>Nx/2)*(Nx-i)
#    j = (j<=Nx/2)*j + (j>Nx/2)*(Nx-j)
    x = (i-x0)
    y = (j-y0)
    r = np.sqrt(x**2 + y**2)
    return r

def thetafunc(i,j,x0,y0,Nx):
#    i = (i<=Nx/2)*i + (i>Nx/2)*(Nx-i)
#    j = (j<=Nx/2)*j + (j>Nx/2)*(Nx-j)
    x = (i-x0)
    y = (j-y0)
    t = np.arctan2(y,x)
    return t

def getrho(rad,orig,Nx):
    x0 = orig[0]
    y0 = orig[1]
    rho = np.fromfunction(lambda i,j: rhofunc(i,j,x0,y0,Nx),(Nx,Nx),dtype=np.float32)
    rho = rho/rad #np.where(rho<=rad,rho/rad,0)
    return rho
    
def gettheta(rad,orig,Nx):
    x0 = orig[0]
    y0 = orig[1]
    theta = np.fromfunction(lambda i,j: thetafunc(i,j,x0,y0,Nx),(Nx,Nx),dtype=np.float32)
    return theta

def R(m,n,rad,orig,Nx):
    ''' n>=m, n-m even '''
    rho = getrho(rad,orig,Nx)
    bigr = np.zeros((Nx,Nx),dtype=np.float32)
    for s in range(1+int((n-m)/2)):
        coeff = (-1)**s*fac(n-s)/(fac(s)*fac((n+m)/2-s)*fac((n-m)/2-s))
        bigr = bigr + coeff*rho**(n-2*s)
    bigr = bigr*(rho<=1.0)
    return bigr
    
def Z(m,n,rad=None,orig=None,Nx=256):
    if rad==None:
        rad = Nx/2
    t = Nx/2-0.5
    cntr = [t,t]
    if (abs(m)>n):
        raise Exception('m must be less than n!')
    if not((n-abs(m))%2==0):
        raise Exception('n-m must be even!')
    theta = gettheta(rad,cntr,Nx)
    if m==0:
        Z = np.sqrt(n+1)*R(0,n,rad,cntr,Nx)
    elif (m>0):
        Z = np.sqrt(2*(n+1))*R(abs(m),n,rad,cntr,Nx)*np.cos(m*theta)
    else:
        Z = np.sqrt(2*(n+1))*R(abs(m),n,rad,cntr,Nx)*np.sin(m*theta)
    if not orig==None:
        orig = np.array(orig)-(Nx/2)
        Z = np.roll(np.roll(Z,int(orig[0]),0),int(orig[1]),1)
    return Z
    
def Zm(j,rad=None,orig=None,Nx=256):
    ''' Zernike modes with single index now, with Noll ordering '''
    n,m = nb[j]
    return Z(m,n,rad,orig,Nx)