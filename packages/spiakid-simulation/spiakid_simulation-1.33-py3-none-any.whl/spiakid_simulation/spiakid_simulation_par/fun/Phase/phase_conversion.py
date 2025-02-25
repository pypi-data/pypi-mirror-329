import numpy as np
import multiprocessing as mp
import csv
from scipy.optimize import least_squares
import scipy.signal as sg
from scipy import interpolate

def ConvInterp(CalibData):

    convwv = []
    convph = []
    for wv in CalibData[1]:
        bin = 50
        a = np.histogram(CalibData[0][str(wv)], bins = bin)

        y = a[0]
        x = a[1]
        x = x[:-1]

        val = sg.find_peaks(y, width = 6, distance = 10)

        if len(val[0]) == 0:
            while len(val[0]) == 0:

                # Reduce histogram bins to detect peaks
                bin_inter = int(bin -1)
                a = np.histogram(CalibData[0][str(wv)], bins = bin_inter)
                y = a[0]
                x = a[1]
                x = x[:-1]
                val = sg.find_peaks(y, width=5)
                bin = bin_inter
        
        if len(val[0]) > 1:
            center = []
            peaks_indx = val[0]
            center0 = x[peaks_indx[0]]
            dpeak = x[peaks_indx[1]] - center0
            for j in range(2):
                sigma, mu, amp = fit_gauss(y, x, x[val[0][0]] + j * dpeak)
                center.append(mu)
                y = y - 1/(np.sqrt(2*np.pi) * sigma) * amp * np.exp(-(x - mu)**2/(2*sigma**2))

            if center[0] > center [1]:
                    mu = center[0]
            


            
        else:
            sigma, mu, amp = fit_gauss(y, x, x[val[0][0]])
            
        convwv.append(wv)
        convph.append(mu)
 
    phwvfunc = interpolate.CubicSpline(convph[::-1], convwv[::-1], bc_type = 'not-a-knot')
    wvphfunc = interpolate.CubicSpline(convwv, convph, bc_type = 'not-a-knot')
    return(phwvfunc, wvphfunc)



def fit_gauss(data,time,center):
        def model(x,u):
            return( x[2]/(x[0]*np.sqrt(2*np.pi))*np.exp(-((u-x[1])**2/(2*x[0]**2))))
        
        def fun (x,u,y):
            return( model(x,u)-y)

        def Jac (x,u,y):
            J = np.empty((u.size,x.size))
            J[:,0] = x[2]*np.exp(-(u-x[1])**2/(2*x[0]**2))/(x[0]**4*np.sqrt(2*np.pi))*(u-x[0]-x[1])*(u+x[0]-x[1])
            J[:,1] = x[2]/(x[0]**3*np.sqrt(2*np.pi))*np.exp(-(u-x[1])**2/(2*x[0]**2))*(u-x[1])
            J[:,2] = 1/(x[0]*np.sqrt(2*np.pi))*np.exp(-(u-x[1])**2/(2*x[0]**2))
            return J
        dat = np.array(data)
        t = np.array(time)
        x0 = np.array([1,center,1000])

        res = least_squares(fun, x0, args=(t, dat), jac=Jac, bounds= ([0,0,0],[np.inf,np.inf,np.inf]))
        return res.x[0],res.x[1],res.x[2]

def ConversionTab(Photon, conversion, k, l):

    pix, conv_wv, conv_phase = conversion

    for p in range(len(pix)):
        i, j = np.int64(pix[p].split(sep='_'))

        if i == k and j == l:
            convtab = fit_parabola(conv_wv[i], conv_phase[i])

    return(convtab)

def fit_parabola(wavelength, phase):
        def model(x,u):
            return(x[0]*u**2 + x[1]*u + x[2])     
        def fun(x,u,y):
            return(model(x,u) - y)
        def Jac(x,u,y):
            J = np.empty((u.size,x.size))
            J[:,0] = u**2
            J[:,1] = u
            J[:,2] = 1
            return(J)
        t = np.array(wavelength)
        dat = np.array(phase)
        x0 = [1,1,1]
        res = least_squares(fun, x0, jac=Jac, args=(t,dat)) 
        return res.x[0],res.x[1],res.x[2]


def photon2phase(Photon, convf, nphase):
    r"""Convert the wavelength in phase

    Parameters:
    -----------

    Photon: array
        Photon's wavelength

    convf: list interpolation
        function to convert wavelength into phase

    conv_phase: array
        Calibration's phase

    Output:
    -------

    signal: array
        Signal converted in phase 
    
    
    """

    
    # dim_x, dim_y= np.shape(Photon[0])

    # signal = np.copy(Photon)
    # for i in range(dim_x):
    #     for j in range(dim_y):

    #             ph = curv[i,j][0] * np.array(Photon[0][i,j]) ** 2 +  curv[i,j][1] * np.array(Photon[0][i,j]) + curv[i,j][2]
    #             sigma = ph / (2*resolution*np.sqrt(2*np.log10(2)))

    #             signal[0][i,j] = np.where(Photon[0][i,j]==0,0,np.random.normal(ph, sigma))
    
    signal = np.copy(Photon)

    ph = convf[1](signal[0])
    sigma = ph / (2 * nphase * np.sqrt(2*np.log10(2)))
    signal[0] = np.where(Photon[0] == 0, 0, np.random.normal(ph, sigma))
    return(signal)


def PhaseNoise(photon, scale, baseline = None):

    # dimx, dimy = np.shape(photon[0])
    # sig = np.zeros(shape = 2, dtype = object)
    # sig[0] = np.zeros(shape = (dimx, dimy), dtype = object)
    # sig[1] = np.zeros(shape = (dimx, dimy), dtype = object)


    # for i in range(dimx):
    #     for j in range(dimy):
    #         sig[0][i,j] = []
    #         sig[1][i,j] = []
    #         if len(photon[0][i,j]) >0:
    #             for k in range(len(photon[0][i,j])):
    #                 if baseline == None:
    #                     sig[0][i,j].append(rand.normal(loc = 0,scale = scale, size = len(photon[0][i,j][k] )) + photon[0][i,j][k])
    #                 else:
    #                     sig[0][i,j].append(rand.normal(loc = baseline[i,j],scale = scale, size = len(photon[0][i,j][k] )) + photon[0][i,j][k])
    #                 sig[1][i,j].append(np.copy(photon[1][i,j][k]))
    sig = np.zeros(shape = 2, dtype = object)
    sig[0] = []
    sig[1] = []
    
    if len(photon[0]) > 0:
        for k in range(len(photon[0])):
            if baseline == None:
                sig[0].append(np.random.normal(loc = 0,scale = scale, size = len(photon[0][k] )) + photon[0][k])
            else:
                sig[0].append(np.random.normal(loc = baseline,scale = scale, size = len(photon[0][k] )) + photon[0][k])
            sig[1].append(np.copy(photon[1][k]))
    
    return(sig)



def exp_adding(photon,decay, exptime):
    r""" Add the exponential decay after the photon arrival

    Parameters:
    -----------

    sig: array
        Signal with the photon arrival

    decay: float
        The decay of the decreasing exponential
    
    Output:
    -------
    
    signal: array
        The signal with the exponential decrease
    
    """

    listph = np.zeros(np.shape(photon[0]), dtype = object)
    listtime = np.zeros(np.shape(photon[0]), dtype = object)
 
    
    listph = []
    listtime = []
    
    if np.size(photon[0])>0:
                for k in range(np.size(photon[0])):
                    
                    if int(photon[1][k]) + 500 < exptime * 1e6:
                        listtime.append(np.linspace(0,499,500, dtype = int)+int(photon[1][k]))
                        listph.append(photon[0][k] * np.exp(decay * np.linspace(0,499,500, dtype = int)/1e6) )
                    else:
                        t = int( (int(photon[1][k]) + 500)- int(exptime*1e6))

                        listph.append(photon[0][k] * np.exp(decay * np.linspace(0,t-1,t)/1e6))
                        listtime.append(np.linspace(0,t-1,t, dtype = int)+int(photon[1][k]))


    return([listph, listtime])



def read_csv(Path,sep='/'):
    r"""Read the calibration file

    Parameters:
    -----------

    Path: string
        Path to the calibration file
    
    sep: string
        The delimiter

    Output:
    -------

    pix: array
        The pixel id

    wv: array
        Calibration wavelength

    phase: array
        Calibration phase          
    
    
    """
    pix = []
    wv = []
    phase = []
    with open(Path,'r') as file:
        data = csv.reader(file,delimiter = sep)
        for i in data:
            pix.append(i[0])
            wv.append(eval(i[2]))
            phase.append(eval(i[1]))
    return(pix,wv,phase)




def PhotonPhase(photondetect, pxnbr, conversion, nphase, decay, exptime, baseline, baselinepix, nreadoutscale, CalibData):
    phase = []
    if len(photondetect) > 0:
        phaseconv = PhaseConversion(photondetect, conversion, nphase, CalibData)
        expphase = PhaseExp(phaseconv, decay, exptime)
        nexpphase = PhaseExpNoise(expphase, baseline, baselinepix, nreadoutscale)
        for ph in range(0, len(nexpphase[0])):
            phase.append([nexpphase[1][ph], nexpphase[0][ph]])
    
    
    # for i in range(0, pxnbr):
    #     for j in range(0, pxnbr):
    #         phase[i,j] = []
    #         for ph in range(0, len(nexpphase[0][i,j])):
    #             phase[i,j].append([nexpphase[1][i,j][ph],nexpphase[0][i,j][ph]])
    
    return(phase)

def PhaseConversion(photondetect, conversion, nphase, CalibData):

    # convfunc = ConversionTab(photondetect,conversion, k, l)
    convfunc = ConvInterp(CalibData)
    phaseconv = photon2phase(photondetect,convfunc, nphase)
    
    return(phaseconv)
                
def PhaseExp(phaseconv, decay, exptime):
               
    expphase = exp_adding(phaseconv, decay, exptime)
    return(expphase)
        
def PhaseExpNoise(expphase, baseline, baselinepix, nreadoutscale):
    nexpphase=[]            
    if baseline == 'uniform':
        nexpphase = PhaseNoise(expphase, nreadoutscale)
    elif baseline == 'random':
        nexpphase = PhaseNoise(expphase, nreadoutscale, baselinepix)
    return(nexpphase)