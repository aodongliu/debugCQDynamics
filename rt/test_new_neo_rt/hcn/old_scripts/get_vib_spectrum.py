import h5py
import matplotlib.pyplot as plt
import numpy

from functional import *


DAMP = 0.001

def read_dataset(fname, path):
    f = h5py.File(fname)
    return numpy.array(f[path])

# Raw data
time = read_dataset('HCN_ccpVDZ_prot_8s8p8d_dx_0p001.bin', "RT/TIME")

ux = read_dataset('HCN_ccpVDZ_prot_8s8p8d_dx_0p001.bin', "RT/LEN_ELEC_DIPOLE")[:,0]
uy = read_dataset('HCN_ccpVDZ_prot_8s8p8d_dy_0p001.bin', "RT/LEN_ELEC_DIPOLE")[:,1]
uz = read_dataset('HCN_ccpVDZ_prot_8s8p8d_dz_0p001.bin', "RT/LEN_ELEC_DIPOLE")[:,2]

dt = time[1] - time[0]

signals = [ux, uy, uz]

# Fourier transformed spectra
spects = []
freq = None
for s in signals:
    s -= s[0]
    s *= np.exp(-DAMP*time)
    #w, f = fourier_tx(s, dt, 0)
    w, f = pade_tx(s, dt, (0,5))
    freq = w
    spects.append(f)

total = sum([f.imag for f in spects]) / 3
total *= freq

# Plotting
plt.plot(freq*27.2114, total, c='k')
plt.xlim(0.24,0.8509)
#plt.ylim(0,0.175)
plt.ylabel("Intensity", fontsize=12)
plt.xlabel("Energy (cm$^{-1}$)", fontsize=12)
plt.tight_layout()
plt.title("HCN Proton vibrational spectra, RT-NEO-TDDFT/ccpVDZ, 8s8p8z")
#plt.savefig("HCN_single_proton.pdf")
plt.show()
