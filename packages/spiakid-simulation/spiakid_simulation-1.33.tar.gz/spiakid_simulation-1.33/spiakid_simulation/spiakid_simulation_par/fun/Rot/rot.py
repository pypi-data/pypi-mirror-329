import numpy as np
from scipy import interpolate
from astropy.coordinates import SkyCoord, EarthLocation, Angle, ICRS, FK5
from astropy.timeseries import TimeSeries
from astropy.time import Time
from astropy import units as u



def ParallacticAngle(locationAltAz, time, location,locationFK5):
  a = locationAltAz.az.radian - np.pi
  z = np.pi/2 - locationAltAz.alt.radian
  
  SiderealTime = Time(time,location = location).sidereal_time('mean').radian
  # print(SiderealTime,locationFK5.ra.radian)
  H = SiderealTime - locationFK5.ra.radian
  cosS = np.cos(a)*np.cos(H)+np.sin(a)*np.sin(H)*np.sin(location.lat.radian)
  
  if z > np.pi*0.01:
    sinS=np.cos(location.lat.radian)*np.sin(H)/np.sin(z)
  else:
    sinS=np.cos(location.lat.radian)*np.sin(a)/np.cos(locationFK5.dec.radian)
  ParaAngle = np.arctan2(sinS,cosS)
  return np.degrees(ParaAngle)

def EarthRotation(lat_tel,coo_guide,coo_star,time,size):
  # Rotation speed of earth
  omega = - 2 * np.pi / 24 / 3600 * np.cos(lat_tel)

  
  
  loc = EarthLocation(lon = -17.89*u.deg,lat =lat_tel*u.rad, height = 2200*u.m)
  # print(loc.lon)
  t = np.linspace(0,time,time+1 )
  period = TimeSeries(time_start='2020-01-01 20:00:00',time_delta = 1*u.s,n_samples =len(t))
  alt, az = coo_guide
  X0, Y0, Z0 = [np.cos(alt)*np.cos(az), -np.cos(alt)*np.sin(az), np.sin(alt)]
  coo_guide = np.array([X0,Y0,Z0])
  # print('coo_guide: ',coo_guide)
  R_inv = np.array([[-X0*Z0/np.sqrt((X0**2+Y0**2)*(X0**2+Y0**2+Z0**2)), Y0/np.sqrt(X0**2+Y0**2), X0/np.sqrt(X0**2+Y0**2+Z0**2)],
                  [-Y0*Z0/np.sqrt((X0**2+Y0**2)*(X0**2+Y0**2+Z0**2)), -X0/np.sqrt(X0**2+Y0**2), Y0/np.sqrt(X0**2+Y0**2+Z0**2)],
                  [np.sqrt(X0**2+Y0**2)/np.sqrt((X0**2+Y0**2+Z0**2)), 0, Z0/np.sqrt(X0**2+Y0**2+Z0**2)]])
  new_pos_x = np.zeros(len(t))
  new_pos_y = np.zeros(len(t))
  alt_ev = np.zeros(len(t))
  alt_az_guide = []
  for i in range (len(t)):
    normalisation = 10 * size
    coo = [coo_star[0]/normalisation,coo_star[1]/normalisation]
    
    z = np.sqrt(1-coo[0]**2 - coo[1]**2)

    coo.append(z)
    # print('coo_star: ',coo_star)
    r1_prime = np.array(coo) - np.array([0,0,1])
    # print('r1_prime:' ,r1_prime)
    r1   = R_inv@r1_prime 
    # print('r1: ',r1)
    coo_star_XYZ = r1 + coo_guide

    theta = omega * t[i]

    Up = np.array([[np.cos(lat_tel)**2 + np.sin(lat_tel)**2 * np.cos(theta), -np.sin(lat_tel) * np.sin(theta), (1-np.cos(theta))*np.cos(lat_tel)*np.sin(lat_tel)],
                [np.sin(lat_tel) * np.sin(theta), np.cos(theta), -np.cos(lat_tel) * np.sin(theta)],
                [(1-np.cos(theta))*np.cos(lat_tel)*np.sin(lat_tel), np.cos(lat_tel)*np.sin(theta), np.sin(lat_tel)**2+np.cos(lat_tel)**2*np.cos(theta)]])

    pos_guide_t = Up@coo_guide
    pos_star_t = Up@coo_star_XYZ
    X0_t = pos_guide_t[0]
    Y0_t = pos_guide_t[1]
    Z0_t = pos_guide_t[2]
    new_alt = np.arcsin(Z0_t)
    new_az = np.arccos(X0_t/np.cos(new_alt))
    alt_az_guide.append([new_alt,new_az])
    r1 = pos_star_t - pos_guide_t


    R_t = np.array([[-X0_t*Z0_t/np.sqrt((X0_t**2+Y0_t**2)*(X0_t**2+Y0_t**2+Z0_t**2)), -Y0_t*Z0_t/np.sqrt((X0_t**2+Y0_t**2)*(X0_t**2+Y0_t**2+Z0_t**2)), np.sqrt(X0_t**2 + Y0_t**2)/np.sqrt(X0_t**2+Y0_t**2+Z0_t**2)],
              [Y0_t/np.sqrt(X0_t**2 + Y0_t**2), -X0_t/np.sqrt(X0_t**2+Y0_t**2), 0],
              [X0_t/np.sqrt(X0_t**2 + Y0_t**2 + Z0_t**2), Y0_t/np.sqrt(X0_t**2 + Y0_t**2 + Z0_t**2), Z0_t/np.sqrt(X0_t**2 + Y0_t**2 + Z0_t**2)]])

    res = R_t@r1
    norm = np.sqrt(res[0]**2+res[1]**2)
    angle = np.arctan2(res[1],res[0])
    x = norm * np.cos(angle)
    y = norm * np.sin(angle)
    new_pos_x[i] = x * normalisation
    new_pos_y[i] = y * normalisation
    alt_ev[i] = np.arcsin(Z0_t)
    # print(new_pos_x)

  new_pos_func_x = interpolate.interp1d(t,new_pos_x)
  new_pos_func_y = interpolate.interp1d(t,new_pos_y)
  new_pos = [new_pos_func_x,new_pos_func_y]
  alt_func = interpolate.interp1d(t,alt_ev)
  alt_az_guide = np.array(alt_az_guide)
  coord = SkyCoord(alt=alt_az_guide[:,0], az=alt_az_guide[:,1], unit='rad', frame = 'altaz', location = loc, obstime = period.time)
  icrs = coord.transform_to('icrs')
  
  alt_az_t = []
  ra_dec_t = []
  ang = []
  period.time.format = 'isot'
  fk5 = FK5(equinox = period.time[0])
  locationFK5 = icrs.transform_to(fk5)
  for i in range(len(coord)):
    alt_az_t.append([coord[i].alt.rad,coord[i].az.rad,i])
    ra_dec_t.append([icrs.ra[i].rad,icrs.dec[i].rad,i])
    ang.append(ParallacticAngle(locationAltAz=coord[i], time = period.time[i],location = loc, locationFK5= locationFK5[i]))
  return(new_pos,alt_func,alt_az_t,ra_dec_t,ang, [new_pos_x, new_pos_y])


def Rotation(rotation, altguide, azguide, latitude, posx, posy, exptime, pxnbr):
               
  if rotation == True:
                
               
    guide = [altguide,azguide]

    rot,evalt, alt_az_t, ra_dec_t, ang, pos = EarthRotation(lat_tel=latitude,coo_guide=guide,coo_star=[posx, posy],time = exptime,size=pxnbr)
  else:
    t = np.linspace(0,exptime,exptime+1 )
    pos = [posx, posy]
    rot = [interpolate.interp1d([0,exptime],[posx,posy]),interpolate.interp1d([0,exptime],[t,t])]
    evalt = interpolate.interp1d([0,exptime],[np.pi/2,np.pi/2])
    alt_az_t =[altguide,azguide,0]
    ra_dec_t = [0,0,0]
    ang = 0
  return(rot, evalt, alt_az_t, ra_dec_t, ang, pos)