import numpy as np
from scipy.optimize import least_squares
import numpy.random as rand
from scipy.signal import find_peaks, lfilter
# from pybaselines import Baseline

def photon_calib(wv, typecalib):

    wv_len = len(wv)
    wv_step = np.linspace(start = wv[int(0.1*wv_len)],stop =wv[int(0.9*wv_len)], num = wv_len)
    wv_calib = np.zeros(shape = wv_len, dtype = object)
    # x_det,y_det = dim, dim
   
    for wv in range(len(wv_step)):
        # print(wv)
        if typecalib == 'passband':
            Wavelength = np.ones([2000]) * (wv_step[wv] + np.random.uniform(-0.005, 0.005, 2000))
        elif typecalib == 'laser':
            Wavelength = np.ones([2000]) * wv_step[wv]
        Time = np.ones([2000]) * np.linspace(0+500,1e6-500,2000, dtype = int)
        # detect = np.zeros([x_det,y_det],dtype = object)

        wv_calib[wv] = [Wavelength, Time]
    # print(len(dict_wv))
    return(wv_calib)


def ConversionPixCalib(conversion, k, l):
    # dim_x, dim_y, _ = np.shape(Photon[0])
    pix, conv_wv, conv_phase = conversion
    # convtab = np.zeros(shape = (dim_x, dim_y), dtype = object)
    for p in range(len(pix)):
        i, j = np.int64(pix[p].split(sep='_'))

        if i == k and j ==l:
            conv = fit_parabola(conv_wv[i], conv_phase[i])

    return(conv)

def PhaseNoiseCalib(photon, scale, baseline):

    # dimx, dimy = np.shape(photon[0])
    # sig = np.zeros(shape = (dimx, dimy), dtype = object)
    
    # for i in range(dimx):
    #     for j in range(dimy):
    #         sig[i,j] = [photon[1][i,j], baseline[i,j] + photon[0][i,j] + rand.normal(loc = 0,scale = scale, size = len(photon[0][i,j] ))]
    
    
    sig = [photon[1], photon[0] + baseline + np.random.normal(loc = 0,scale = scale, size = len(photon[0]))]
    return(sig)


def extractDigits(lst, decay):
    return list(map(lambda el:np.array(el * np.exp(decay * np.linspace(0,498,499) * 1e-6)).astype(np.float64), lst))


def AddingExp(ph, photonlist, time):
 
    addmatrix = np.zeros(shape = (len(ph)))
    for (t, photon) in zip(time, photonlist):

        addmatrix[int(t):int(t+len(photon))] = photon
    ph = ph + addmatrix
    return(ph)

def exp_adding_calib(photon,decay, exptime):

    # # phasecalib = np.copy(photon)
    
    # dimx, dimy,_ = np.shape(photon[0])
    # phasecalib = np.zeros(shape=2, dtype = object)
    # phasecalib[1] = np.zeros(shape=(dimx, dimy), dtype = object)
    # phasecalib[0] = np.zeros(shape=(dimx, dimy), dtype = object)
    # for i in range(dimx):
    #     for j in range(dimy):
    #         # print(time)
            
    #         photonlist = extractDigits(photon[0][i,j], decay)

    #         if photon[1][i,j][-1] + 500 > exptime:
    #             ph = np.zeros(shape= (photon[1][i,j][-1] + 500))
                
    #             extphoton = AddingExp(ph, photonlist, photon[1][i,j])
    #             phasecalib[0][i,j] = extphoton[:exptime]
    #             phasecalib[1][i,j] = np.linspace(0,exptime-1,exptime, dtype = int)
            
    #         else:
    #             ph = np.zeros(shape = exptime, dtype = int)

    #             phasecalib[0][i,j] = AddingExp(ph, photonlist, photon[1][i,j])
    #             phasecalib[1][i,j] = np.linspace(0,exptime-1,exptime, dtype = int)

    phasecalib = np.zeros(shape = 2, dtype = object)
    photonlist = extractDigits(photon[0], decay)

    if photon[1][-1] + 500 > exptime:
        ph = np.zeros(shape = photon[1][-1]+500)
        extphoton = AddingExp(ph, photonlist, photon[1])
        phasecalib[0] = extphoton[:exptime]
        phasecalib[1] = np.linspace(0, exptime -1, exptime, dtype = int)

    else:
        ph = np.zeros(shape = exptime, dtype = int)
        phasecalib[0] = AddingExp(ph, photonlist, photon[1])
        phasecalib[1] = np.linspace(0, exptime-1, exptime, dtype = int)

    return(phasecalib)

def Photon2PhaseCalib(Photon, curv, resolution):
    r"""Convert the wavelength in phase

    Parameters:
    -----------

    Photon: array
        Photon's wavelength on each pixel

    conv_wv: array
        Calibration's wavelength

    conv_phase: array
        Calibration's phase

    Output:
    -------

    signal: array
        Signal converted in phase 
    
    
    """

    signal = np.copy(Photon)
    ph = curv[0] * np.array(Photon[0]) ** 2 + curv[1] * np.array(Photon[0]) + curv[2] 
    sigma = ph /(2*resolution* np.sqrt(2*np.log10(2)))
    signal[0] = np.where(Photon[0]==0, 0, np.random.normal(ph, sigma))
    signal[1] = Photon[1]
    
    return(signal)


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


def Calib(*args):

    [
        wv, nbwv, calibtype, conversion, save_type, filter, noisetimeline,
        nphase, decay, timelinestep, nreadoutscale, baselinepix, wmap,peakprominence, k, l
        ] = args
    calib = {}
   
    wvcalib = np.linspace(wv[0], wv[-1], nbwv)
    photondetectcalib = photon_calib(wvcalib, calibtype)
    conv = ConversionPixCalib(conversion, k, l)
    if save_type == 'photon_list':
        for i in range(len(wvcalib)):
                calib[str(wvcalib[i])] = CalibCompute(photondetectcalib[i], conv, nphase, decay, timelinestep, filter, nreadoutscale, baselinepix, wmap, noisetimeline, wvcalib[i],  peakprominence)
    
    return(calib, wvcalib)


# def CalibCompute(tab, wvcalib, phcalib, noisetimeline,output = False):

def CalibCompute(*args):
    phcalib, tab, nphase, decay, timelinestep, filter, nreadoutscale, baselinepix, wmap, noisetimeline, wvcalib,  peakprominence = args
    phaseconvcalib = Photon2PhaseCalib(phcalib, tab, nphase)
    expphasecalib = exp_adding_calib(phaseconvcalib, decay, timelinestep)
    nexpphasecalib = PhaseNoiseCalib(expphasecalib, nreadoutscale, baselinepix)


    fphase = lfilter(filter, 1, nexpphasecalib)

    # x = np.linspace(0, len(fphase[0]) - 1, len(fphase[0]))
    
    # y = fphase[1]
    # print(y, flush=True)
    
    
    # baseline_fitter = Baseline(x_data = x)
    # lbd = 10**6
    # bkg, params = baseline_fitter.arpls(y, lam=lbd)


    fnoise = lfilter(filter, 1, noisetimeline[1])
 
    peaks, _ = find_peaks(fphase[1], prominence=peakprominence, height=fnoise)
    nbpeaks = int((len(peaks)) * wmap)
    peaks = peaks[:nbpeaks]
    # return(fphase[1][peaks] - bkg[peaks])
    return(fphase[1][peaks])
