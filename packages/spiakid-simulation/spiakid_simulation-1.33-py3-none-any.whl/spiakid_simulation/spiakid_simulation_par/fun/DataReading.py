from yaml.loader import SafeLoader
import yaml
import pydantic
from pydantic import TypeAdapter, ValidationError
from pydantic.dataclasses import dataclass
from typing import Union, Optional


def read_yaml(FilePath):
        r""""
        Read yaml file and store all information in data

        Parameter
        ---------

        FilePath: string
            Position and name of the yaml file

        Attributes
        ----------

        Data: Dictionnary
            Contains all information that contains the yaml file correctly ordered
        """
        with open(FilePath) as f:
            data = yaml.load(f, Loader=SafeLoader)
        return data


def data_check(file: str) -> dict: 
    
    config = read_yaml(file)

    @dataclass
    class Photon:


        @dataclass
        class Telescope:

            @dataclass
            class Detector:
                pix_nbr: int
                pix_size: Union[int,float]
                baseline: str
                calibration: str
                # calibfile: Optional[str]
                weightmap: Optional[Union[bool,str]]
                nbwavelength: int
                point_nb: int
                peakprominence: float

            exposition_time: int
            diameter: Union[int,float]
            obscuration: Union[int,float]
            latitude: Union[int,float]
            transmittance: str
            detector: Detector

        @dataclass
        class Star:

            @dataclass
            class st_distance:
                min: Union[int,float]
                max: Union[int,float]

            @dataclass
            class st_wv:
                min: Union[int,float]
                max: Union[int,float]
                nbr: int
            
            distance: st_distance
            wavelength_array: st_wv
            spectrum_folder: str
            spectrum_desc: str
            crater_file: str

        @dataclass
        class Sky:

            @dataclass
            class sky_guide:
                alt: Union[int,float]
                az: Union[int,float]

            rotation: bool
            guide: sky_guide

        @dataclass
        class psf:
            method: str
            file: str
            pix_nbr: Optional[int] = None 
            size: Optional[Union[int,float]] = None
            seeing: Optional[Union[int,float]] = None
            wind: Optional[Union[int,float,list]] = None
            coeff: Optional[list] = None
            L0: Optional[Union[int,float]] = None

        telescope: Telescope
        star: Star
        sky: Sky
        PSF: Optional[psf] = None

        
        
        
    @dataclass
    class readout_noise:
        scale :Union[int,float]
        noise_type: str

    @dataclass
    class phase:
        
        Calib_File: str
        Phase_Noise: Union[int,float]
        Decay: Union[int,float]
        Readout_Noise: readout_noise
        Phase: bool

    @dataclass
    class electronic:
        nperseg: int
        template_time: Union[int,float]
        trigerinx: int
        point_nb: int

    @dataclass
    class output:
        save: str

    @dataclass
    class SimFile: 
        sim_file : str
        process_nb : int
        Photon_Generation: Photon
     
        Phase: Optional[phase] = None
        Electronic: Optional[electronic] = None
        Output: Optional[output] = None

        

    ta = TypeAdapter(SimFile)
    try: 
        ta.validate_python(config)
        return(config)
        
    
    except pydantic.ValidationError as e:
        print(e)

