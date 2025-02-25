import numpy as np
import numpy.random as rand
from astropy.io import fits
from pathlib import Path
from scipy import interpolate
import h5py
import itertools

import multiprocessing as mp

from spiakid_simulation.spiakid_simulation_par.fun.PSF.turbulence import PSF_creation, PSF_creation_mult
from spiakid_simulation.spiakid_simulation_par.fun.DataReading import data_check
from spiakid_simulation.spiakid_simulation_par.fun.Photon.sim_image_photon import StarPhoton, PhotonJoin, Timeline
from spiakid_simulation.spiakid_simulation_par.fun.Rot.rot import Rotation
from spiakid_simulation.spiakid_simulation_par.fun.Phase.phase_conversion import read_csv, PhotonPhase
from spiakid_simulation.spiakid_simulation_par.fun.Calibration.Calib import Calib
from spiakid_simulation.spiakid_simulation_par.fun.Filter.filter import PixFilter

import spiakid_simulation.spiakid_simulation_par.fun.Crater.CraterSpectrum as cs

from spiakid_simulation.spiakid_simulation_par.fun.output.HDF5_creation import recursively_save_dict_contents_to_group





class Simulation():
    __slots__ = ('detect', 'psf', 'stars', 'photons', 'wmap')

    @staticmethod
    def InitSeed():
        np.random.seed()


    @staticmethod
    def ParFun(args):

        [
            k,l,baseline, decay, templatetime, trigerinx, pointnb, nperseg, nreadoutscale, baselinepix,
            wv, nbwv, calibtype, conversion, save_type, nphase, decay, timelinestep, wmap, photons , peakprominence
        ] = args
        # print([k, l, seed], flush = True)
        pixfilter = PixFilter(baseline, decay, templatetime, trigerinx, pointnb, nperseg, nreadoutscale, baselinepix, k, l)
    
        pixcalib = Calib(wv, nbwv, calibtype, conversion, save_type, pixfilter[0], pixfilter[1],nphase, decay, timelinestep, nreadoutscale, baselinepix, wmap,peakprominence, k, l)
       
        pixphase = PhotonPhase(photons, pxnbr, conversion, nphase, decay, exptime, baseline, baselinepix, nreadoutscale, pixcalib)
     
        pixpeaks, ftime =  Timeline(pixphase, exptime, pixfilter[0], pixfilter[1], nreadoutscale, timelinestep, wmap, peakprominence)
        
        return([k, l, pixfilter, pixcalib, pixpeaks, ftime])
    
    def __init__(self,file ):

        # Data reading
     
        global DATA
        DATA = data_check(file)

        global path
        path = DATA['sim_file']
        global process_nb
        process_nb = DATA['process_nb']

        global h5file
        h5file = h5py.File(path, 'w')

        global phgen
        phgen = DATA['Photon_Generation']

        global telescope
        telescope = phgen['telescope']
        global exptime 
        exptime = telescope['exposition_time']
        global diameter 
        diameter = telescope['diameter']
        global obscuration
        obscuration = telescope['obscuration']
        global latitude
        latitude = telescope['latitude'] * np.pi / 180 
        global transmittance
        transmittance = telescope['transmittance']
        global pxnbr
        pxnbr = telescope['detector']['pix_nbr']
        global pxsize 
        pxsize = telescope['detector']['pix_size']

        S = (pxsize * pxnbr)**2

        global baseline
        baseline =  telescope['detector']['baseline']
        global peakprominence
        peakprominence =  telescope['detector']['peakprominence']


        if baseline =='random':
            global baselinepix
            baselinepix = np.random.uniform(low = 10, high = 20, size = (pxnbr, pxnbr))

            h5file['baseline/Baseline'] = baselinepix
            
        elif baseline == 'uniform':
            baselinepix = np.zeros(shape = (pxnbr, pxnbr))
    
        global weightmap
        weightmap = telescope['detector']['weightmap']

        global timelinestep 
        timelinestep = telescope['detector']['point_nb']
        global calibtype
        calibtype = telescope['detector']['calibration']

        global nbwv
        nbwv = telescope['detector']['nbwavelength']

        st = phgen['star']
        global stnbr 
        stnbr = 3 # int(S * 0.13)
        global stdistmin
        stdistmin = st['distance']['min']
        global stdistmax
        stdistmax = st['distance']['max']
        global wv
        wv = np.linspace(st['wavelength_array']['min'],
                        st['wavelength_array']['max'],
                        st['wavelength_array']['nbr'])
        global spectrum 
        spectrum = st['spectrum_folder']

        global spectrum_desc
        spectrum_desc = st['spectrum_desc']

        global crater_file
        crater_file = st['crater_file']

        sky = phgen['sky']


        global rotation
        rotation = sky['rotation']
        global altguide 
        altguide = sky['guide']['alt'] * np.pi / 180 
        global azguide 
        azguide = sky['guide']['az'] * np.pi / 180 
        
        

  
        global spectrumlist 
        spectrumlist = []
        files = Path(spectrum).glob('*')
        for i in files:
            spectrumlist.append(i)

        

        
        
        try:
            global save_type
            save_type = DATA['Output']['save']
        except: pass

        try: DATA['Phase']
        except: pass
        else:
            global calibfile
            calibfile = DATA['Phase']['Calib_File']
            global conversion
            conversion = read_csv(calibfile)
            global nphase
            nphase = DATA['Phase']['Phase_Noise']
            global decay
            decay = - DATA['Phase']['Decay']
            global nreadoutscale
            nreadoutscale = DATA['Phase']['Readout_Noise']['scale']
            global nreadouttype
            nreadouttype = DATA['Phase']['Readout_Noise']['noise_type']

            

            global nperseg
            nperseg = DATA['Electronic']['nperseg']

            global templatetime
            templatetime = DATA['Electronic']['template_time']
            
            global trigerinx
            trigerinx = DATA['Electronic']['trigerinx']

            global pointnb
            pointnb = DATA['Electronic']['point_nb']



            # Detector Creation
            # self.detect = self.Detector()
        recursively_save_dict_contents_to_group(h5file, '/', DATA)
        print('DATA DONE')
        #PSF computing
        self.psf = self.PSF()
        print('PSF done')
        self.stars = {}
        # Star and photon creation
        sp_dict = cs.CMDFileRead(crater_file)
        inx, spdict = cs.FindSpiakidSp(sp_dict, stnbr, spectrum_desc)
        for i in range(0, stnbr):
            print('star %i'%i)
            
            self.stars['star_'+str(i)] = self.Star(self.psf,i, spdict)
          
          
        print('Star done')


        self.photons = PhotonJoin(self.stars, pxnbr, nreadoutscale, exptime)
        print('Photon done')


        for i in range(pxnbr):
            for j in range(pxnbr):
                if len(self.photons[i,j][0]) > 0:
                    h5file['Photons/Photons/'+str(i)+'_'+str(j)] = list(zip(self.photons[i,j][0], self.photons[i,j][1]))
            
        

        try: DATA['Phase']
        except: pass
        else:

            if weightmap == True:
                self.wmap = np.random.uniform(low = 0.5, high = 1, size = (pxnbr, pxnbr))
      
            else:
                self.wmap = np.ones(shape = (pxnbr, pxnbr))
            h5file['WeightMap'] = self.wmap
            
            # Photon distribution on the detector 
            args = []
            pixlist = np.linspace(0, pxnbr-1, pxnbr, dtype = int)
            pix = list(itertools.product(pixlist, pixlist))

            
            for i in range(len(pix)):
                k, l = pix[i][0], pix[i][1]
                rng = np.random.default_rng(np.random.randint(low = 0, high = 10000))
                subseeds = rng.choice(10000, size = 3, replace = False)
           
                args.append(np.array([k,l,baseline, decay, templatetime, trigerinx, pointnb, nperseg, nreadoutscale, baselinepix[k,l],
                             wv, nbwv, calibtype, conversion, save_type, nphase, decay, timelinestep, self.wmap[k,l], self.photons[k,l],
                             peakprominence ], dtype = object))
          
            # l = np.linspace(1,10,1000)
            # a = np.linspace(1,5,1000)
            # args = []

            # for j in range(len(a)):
                # args.append([a[j],l[j]])

            with mp.Pool(processes=process_nb, initializer=Simulation.InitSeed) as pool:
                res = pool.map(Simulation.ParFun, args)
                pool.close()
                pool.join()
            print('res')
            for r in res:
                k, l = r[0], r[1] 
                pixfilter = r[2][0]
                pixcalib = r[3]
                pixpeaks = r[4]
                ftime = r[5]
               

                h5file['Filter/'+str(k)+'_'+str(l)] = pixfilter
                for i in range(len(pixcalib[1])):
                   
                    h5file['Calib/'+str(pixcalib[1][i])+'/'+str(k)+'_'+str(l)] = pixcalib[0][str(pixcalib[1][i])]
                    
                
                for i in range(len(pixpeaks)):
                  
                    h5file['Photons/'+str(i)+'/'+str(k)+'_'+str(l)] = pixpeaks[i]
                    h5file['ftime/'+str(i)+'/'+str(k)+'_'+str(l)] = ftime[i]
               


            # self.stars['Detector'] = self.PhotonDetection(self.stars, self.detect.noisetimeline, self.detect.wmap)
        print('End detector', flush = True)
    
    # @staticmethod
    # def ParFun(args):
    #     a, l = args
    #     return(a+l)

        
    

    class PSF():
            __slots__ = ('psfpxnbr', 'psfsize','psfenergy','psfpos','maxpsf','psf')
            def __init__(self):

        
                try: phgen['PSF']
                except:
                        self.gaussian_psf(pxnbr=pxnbr, pxsize=pxsize, wv=wv)
                else:
                        psf = phgen['PSF']
                        psfmeth = psf['method']
                        psffile = psf['file']
                        try: psfmeth == 'Download'
                        except:
                            self.defined_psf(psf=psf,psffile=psffile, wv=wv, diameter=diameter,
                                            obscuration=obscuration,exptime=exptime)
                        else:
                            file = fits.open(psffile)[0]
                            self.psf = file.data
                            list_axis = [file.header['NAXIS1'],file.header['NAXIS2'],file.header['NAXIS3']]
                            if (list_axis.count(file.header['NAXIS1']) == 2)  and (file.header['CUNIT1'] == 'arcsec'):
                                self.psfpxnbr = file.header['NAXIS1']
                                self.psfsize = self.psfpxnbr * file.header['CDELT1']
                            else:
                                if file.header['CUNIT2'] == 'arcsec':
                                    self.psfpxnbr =file.header['NAXIS2']
                                    self.psfsize = self.psfpxnbr * file.header['CDELT2']


                # Create a minimum of intensity on the psf to place a photon
                self.psfenergy = np.zeros(shape = np.shape(wv), dtype = object)
                self.psfpos = np.zeros(shape = np.shape(wv), dtype = object)
                self.maxpsf = []
         
                for wvl in range(len(wv)):
                    self.maxpsf.append(1.1 * np.max(self.psf[wvl]))
                    self.psfpos[wvl]  = []
                    self.psfenergy[wvl] = []
                    lim = np.max(self.psf[wvl])/100
                    data  = self.psf[wvl]
                    for i in range(self.psfpxnbr):
                        for j in range(self.psfpxnbr):
                            if self.psf[wvl][i,j]> lim: 
                                self.psfpos[wvl].append([i,j])
                                self.psfenergy[wvl].append(data[i,j])
                    h5file['PSF/psfpos/'+str(wvl)] = self.psfpos[wvl]
                    h5file['PSF/psfenergy/'+ str(wvl)] = [self.psfenergy[wvl]]
               

                    

            def gaussian_psf(self, pxnbr, pxsize, wv):
                self.psfpxnbr = pxnbr
                psf_grid = np.zeros(shape = (pxnbr,pxnbr,len(wv)))
                psf_grid[np.int8(pxnbr/2),np.int8(pxnbr/2),:] = 1
                    # point = np.linspace(0,1,pix_nbr)
                    # psf = interpolate.RegularGridInterpolator((point,point,wavelength_array),psf_grid)
                    # psf_pix_nbr = pix_nbr
                self.psfsize = pxsize * pxnbr
                self.psf = psf_grid
             

            def defined_psf(self, psf, psffile, wv, diameter, obscuration, exptime):
                self.psfpxnbr = psf['pix_nbr']
                self.psfsize = psf['size']
                seeing = psf['seeing']
                wind = psf['wind']
                L0 = psf['L0']

                if type[wind] == list:
                    coeff = psf['coeff']
                    self.psf = PSF_creation_mult(fov_tot=self.psfsize, nb_pixels_img=self.psfpxnbr,
                                                wavelength_array=wv, seeing=seeing, wind=wind,
                                                D=diameter, obscuration=obscuration, L0=L0,
                                                obs_time=exptime, coeff=coeff,save_link=psffile)
                else:
                    self.psf = PSF_creation(fov_tot=self.psfsize, nb_pixels_img=self.psfpxnbr,
                                            wavelength_array=wv, seeing=seeing, wind=wind,
                                            D=diameter, obscuration=obscuration, L0=L0,
                                            obs_time=exptime, save_link=psffile)

    class Star():
            __slots__ = ('posx', 'posy', 'spectrumchoice', 'stardist', 'starintensity', 'spectrum', 'phase', 'alt_az_t', 'ra_dec_t', 'ang', 'photondetect')
            def __init__(self, psf,i, sp):
                
                self.posx  = rand.uniform(low = -(0.9 * pxnbr)/2, high= (0.9 * pxnbr)/2)
                self.posy  = rand.uniform(low = -(0.9 * pxnbr)/2, high= (0.9 * pxnbr)/2)
                print(self.posx+pxnbr/2,self.posy+pxnbr/2, flush = True)
                spname = sp['star_'+str(i)]['Spectrum'] 
                ratio = sp['star_'+str(i)]['ratio']
                T = sp['star_'+str(i)]['Temp']
                mag = sp['star_'+str(i)]['Mag']
                sp = np.loadtxt(spectrum + '/'+ spname)
                self.spectrumchoice = interpolate.interp1d(sp[:,0],sp[:,1])
                self.stardist = rand.uniform(stdistmin, stdistmax)
                self.starintensity = 1 * (10 / self.stardist**2)
                self.spectrum = [wv*10**3, (10 /self.stardist**2) * self.spectrumchoice(wv*10**3) * ratio]
                rot, evalt, self.alt_az_t,self.ra_dec_t,self.ang, pos = Rotation(rotation, altguide, azguide, latitude, self.posx, self.posy, exptime, pxnbr)

                self.photondetect = StarPhoton(i, psf, rot, evalt, wv, self.spectrum, exptime, diameter, timelinestep, transmittance, pxnbr, pxsize, h5file)
                
                h5file['Stars/'+str(i)+'/Spectrum'] = sp
                h5file['Stars/'+str(i)+'/Rotation'] = pos
                h5file['Stars/'+str(i)+'/Pos'] = [self.posx, self.posy]
                h5file['Stars/'+str(i)+'/Dist'] = self.stardist
                h5file['Stars/'+str(i)+'/Intensity'] = self.starintensity
                h5file['Stars/'+str(i)+'/ra_dec_t'] = self.ra_dec_t
                h5file['Stars/'+str(i)+'/alt_az_t'] = self.alt_az_t
                h5file['Stars/'+str(i)+'/Temp'] = T
                h5file['Stars/'+str(i)+'/SpecName'] = spname
                h5file['Stars/'+str(i)+'/Mag'] = mag

                

                # try: DATA['Phase']
                # except: pass
                # else:
                #     self.phase = StarPhase(photondetect, pxnbr, conversion, nphase, decay, exptime, baseline, baselinepix, nreadoutscale)
                
    class Detector():
        __slots__ = ('pixfilter', 'noisetimeline', 'photondetectcalib', 'wmap')
        def __init__(self,):

            
            print('Detector part', flush = True)
            # WeightMap creation 
            
            if weightmap == True:
                self.wmap = np.random.uniform(low = 0.5, high = 1, size = (pxnbr, pxnbr))
      
            else:
                self.wmap = np.ones(shape = (pxnbr, pxnbr))

            # Saving Weight Map in hdf5 file
            h5file['WeightMap'] = self.wmap

            # Filter creation
            self.pixfilter, self.noisetimeline = PixFilter(pxnbr, baseline, decay, templatetime, trigerinx, pointnb, nperseg, nreadoutscale, baselinepix)

            # Calibration data creation
            Calib(wv, nbwv, pxnbr, calibtype, conversion, save_type, self.noisetimeline, nphase, decay, timelinestep, nreadoutscale, baselinepix, self.wmap, h5file)
   
