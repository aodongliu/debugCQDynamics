import h5py
import matplotlib.pyplot as plt
import numpy
from matplotlib.pyplot import figure
from functional import *


DAMP = 0.001

def read_dataset(fname, path):
    f = h5py.File(fname)
    return numpy.array(f[path])

# Raw data
time = read_dataset('HCN_ccpVDZ_prot_8s8p8d_dx_0p001.bin', "RT/TIME")
time_r = read_dataset('HCN_ccpVDZ_prot_8s8p8d_dx_0p001.bin', "RT/TIME")

ux = read_dataset('HCN_ccpVDZ_prot_8s8p8d_dx_0p001.bin', "RT/LEN_ELEC_DIPOLE")[:,0]
uy = read_dataset('HCN_ccpVDZ_prot_8s8p8d_dy_0p001.bin', "RT/LEN_ELEC_DIPOLE")[:,1]
uz = read_dataset('HCN_ccpVDZ_prot_8s8p8d_dz_0p001.bin', "RT/LEN_ELEC_DIPOLE")[:,2]

ux_r = read_dataset('HCN_ccpVDZ_dx_0p001.bin', "RT/LEN_ELEC_DIPOLE")[:,0]
uy_r = read_dataset('HCN_ccpVDZ_dy_0p001.bin', "RT/LEN_ELEC_DIPOLE")[:,1]
uz_r = read_dataset('HCN_ccpVDZ_dz_0p001.bin', "RT/LEN_ELEC_DIPOLE")[:,2]

dt = time[1] - time[0]
dt_r =  time_r[1] - time_r[0]

signals = [ux, uy, uz]
signals_r  = [ux_r , uy_r , uz_r]
# Fourier transformed spectra
spects = []
freq = None
for s in signals:
    s -= s[0]
    s *= np.exp(-DAMP*time)
    #w, f = fourier_tx(s, dt, 0)
    w, f = pade_tx(s, dt, (0,5), res = 10000)
    freq = w
    spects.append(f)
total = sum([f.imag for f in spects]) / 3
total *= freq

spects_r = []
freq_r = None
for s in signals_r:
    s -= s[0]
    s *= np.exp(-DAMP*time_r)
    #w, f = fourier_tx(s, dt, 0)
    w, f = pade_tx(s, dt_r, (0,5),res = 10000)
    freq_r = w
    spects_r.append(f)
total_r = sum([f.imag for f in spects_r]) / 3
total_r *= freq_r

# Plotting
figure(figsize = (8, 6), dpi=300)
plt.plot(freq*27.2114, total, c='b',label="NEO-TDDFT")
plt.plot(freq_r*27.2114, total_r, c='r', label='TDDFT')
#plt.xlim(0,30)
plt.ylim(0,0.12)
plt.ylabel("Intensity", fontsize=12)
plt.xlabel("Energy (eV)", fontsize=12)
#plt.tight_layout()
plt.legend(loc="upper left")
plt.title("HCN Proton vibrational spectra, RT-NEO-TDDFT/ccpVDZ, 8s8p8z")
plt.savefig("HCN_NEOvsTDDFT.pdf")
plt.show()
