# Copyright 2014-2017 CERN. This software is distributed under the
# terms of the GNU General Public Licence version 3 (GPL Version 3),
# copied verbatim in the file LICENCE.md.
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.
# Project website: http://blond.web.cern.ch/

'''
Protvino U-70

Tracking near transition and at transition
incliding high order MCF
Jump also considered

:Authors: **Sergey Kolokolchikov**
:E-mail:sergey.bell13@gmail.com
'''

#  General Imports
from __future__ import division, print_function

import os
from builtins import range

import matplotlib as mpl
import numpy as np
import scipy.constants as const
import shutil

from blond.beam.beam import Beam, Proton
from blond.beam.distributions import bigaussian, parabolic
from blond.beam.profile import CutOptions, FitOptions, Profile
from blond.input_parameters.rf_parameters import RFStation
#  BLonD Imports
from blond.input_parameters.ring import Ring
from blond.monitors.monitors import BunchMonitor
from blond.plots.plot import Plot
from blond.trackers.tracker import RingAndRFTracker

# My IMPORT
from blond.plots.plot_parameters import plot_voltage_programme
from blond.beam.coasting_beam import generate_coasting_beam
# Impedance
from blond.impedances.impedance import (InducedVoltageFreq, InducedVoltageTime,
                                        InductiveImpedance,
                                        TotalInducedVoltage,
                                        InducedVoltageResonator)
from blond.impedances.impedance_sources import Resonators
from blond.plots.plot_impedance import plot_induced_voltage_vs_bin_centers

mpl.use('Agg')

this_directory = os.path.dirname(os.path.realpath(__file__)) + '/'

os.makedirs(this_directory + '../output_files/U-70_jump', exist_ok=True)


# Simulation parameters -------------------------------------------------------
# Bunch parameters
N_b = 1.0e12                 # Design Intensity in SIS100
N_p = 100000                 # Macro-particles
#tau_0 = 1200.0e-9           # Initial bunch length, 4 sigma [s]

# Machine
m_p = 0.938e9            # mass of proton in eV
C_ring = 1483.699        # Machine circumference [m]
#E_inj = 1.32e9          # Injection Energy, [eV]
#E_exp = 69e9            # Injection Energy, [eV]
#E_tr = 7.957e9        # Injection Energy, [eV] before JUMP
#E_inj = 7.832e9        # Injection Energy, [eV] before JUMP
E_inj = 6.9e9        # Injection Energy, [eV] before JUMP
gamma_inj = E_inj/m_p + 1
beta_inj = np.sqrt(1-1/gamma_inj**2)
p_inj = np.sqrt((E_inj+m_p)**2-m_p**2)

alpha_0 =  0.011120           # 1st order mom. comp. factor stationary
alpha_0_st =  0.011120           # 1st order mom. comp. factor stationary
#alpha_1 =  0.0                # 2nd order mom. comp. factor stationary
alpha_1 =  0.01031066         # 2nd order mom. comp. factor stationary
alpha_2 =  0.0                # 3d order mom. comp. factor stationary
gamma_tr = 1/np.sqrt(alpha_0) # Transition gamma 9.483

# Tracking details
N_t = 10000           # Number of turns to track
dt_plt = 1000        # Time steps between plots

n1=0
dn21 = 7210
dn32 = 200
dn32_2 = 100

#RF Parameters
Vamp = 40*10000
#Vamp = 45*1000
U = Vamp * 1/2              # Accelerating Voltage, [eV]

E_fin = E_inj + U * N_t
gamma_fin = E_fin/m_p + 1
p_fin = np.sqrt((E_fin+m_p)**2-m_p**2)

print (E_inj, E_fin)

# Simulation setup ------------------------------------------------------------
print("Setting up the simulation...")
print("")
alpha_0 = []

#7210 turns
d_alpha_0 = 0.01120 - 0.00927579
a1 = - d_alpha_0 / dn21
a2 = d_alpha_0 / dn32

b1 = alpha_0_st
b2 = alpha_0_st - a2*(dn21 + dn32)

for i in range (0, n1):
    alpha_0.append(alpha_0_st)
    #alpha_1.append(alpha_1_st)
    i = i + 1
for i in range (n1, n1+dn21):
    alpha_0.append(a1*i+b1)
    i = i + 1
print(i)
#200 turns
for i in range (n1+dn21, n1+dn21+dn32):
    alpha_0.append(a2*i+b2)
    i = i + 1
print(i)
#other turns
for i in range (n1+dn21+dn32, N_t+1):
    alpha_0.append(alpha_0_st)
    i = i + 1
print(i)

# Define general parameters
#np.linspace(E_inj, E_fin, N_t+1)
#ring = Ring(C_ring, alpha, E_inj, Proton(), N_t,
#            synchronous_data_type='kinetic energy')
#ring = Ring(C_ring, alpha_0, np.linspace(E_inj, E_fin, N_t+1), Proton(), N_t,
#            synchronous_data_type='kinetic energy')
# High order MCF included
ring = Ring(C_ring, alpha_0, np.linspace(E_inj, E_fin, N_t+1), Proton(), N_t,
            synchronous_data_type='kinetic energy',
            alpha_1=alpha_1)
#Transition jump
#ring = Ring(C_ring, alpha_0,
#            np.linspace(E_inj, E_fin, N_t+1), Proton(), N_t,
#            synchronous_data_type='kinetic energy',
#            alpha_1=alpha_1,alpha_2=alpha_2)

# Define beam and distribution
beam = Beam(ring, N_p, N_b)

h=30
V=10000*40
dphi=0
n_rf=1

harm=30
dphi=0.0

N_tr = 4785
Vamp=400000 #10 kV
#Vamp=45000 #45 kV
Volt = []
harmonic = []
dphi_arr = []
for i in range (0, n1+dn21+dn32_2):
    Volt.append(Vamp)
    harmonic.append(harm)
    dphi_arr.append(dphi)
    i = i + 1
for i in range (n1+dn21+dn32_2, N_t+1):
    Volt.append(Vamp)
    harmonic.append(harm)
    dphi_arr.append(dphi+2*np.pi/3)
    #+np.pi/2+np.pi/6
    i = i + 1


print("RF parameters set")
#print([harmonic], [V], [dphi_arr])
# Define RF station parameters and corresponding tracker
rf = RFStation(ring, [harmonic], [Volt], [dphi_arr])
#rf = RFStation(ring, h, V, dphi, n_rf)
#rf = RFStation(ring, [h], [V], [dphi])


long_tracker = RingAndRFTracker(rf, beam, solver='exact')

# DISTRIBUTIONS
bigaussian(ring, rf, beam, 1.2*1e3*1e-9/4/h/2, reinsertion='on', seed=1)
#parabolic(ring, rf, beam, 1.8*1e3*1e-9/h/2.5, seed=1)
#generate_coasting_beam(beam, 0, 1.7e-6/harm, spread=3E-3,
#                           spread_type='dp/p', energy_offset=0,
#                           distribution='gaussian', user_distribution=None,
#                           user_probability=None)


# Need slices for the Gaussian fit
profile = Profile(beam, CutOptions(n_slices=100),
                  FitOptions(fit_option='gaussian'))

# Define what to save in file
bunchmonitor = BunchMonitor(ring, rf, beam,
                            this_directory + '../output_files/U-70_jump', Profile=profile)

format_options = {'dirname': this_directory + '../output_files/U-70_jump'}
plots = Plot(ring, rf, beam, dt_plt, N_t,
             700e-9/h*4, 2000e-9/h*4, -600e6, 600e6, xunit='s', separatrix_plot=True,
             Profile=profile, h5file=this_directory + '../output_files/U-70_jump',
             format_options=format_options)

# For testing purposes
test_string = ''
test_string += '{:<17}\t{:<17}\t{:<17}\t{:<17}\n'.format(
    'mean_dE', 'std_dE', 'mean_dt', 'std_dt')
test_string += '{:+10.10e}\t{:+10.10e}\t{:+10.10e}\t{:+10.10e}\n'.format(
    np.mean(beam.dE), np.std(beam.dE), np.mean(beam.dt), np.std(beam.dt))

# LOAD IMPEDANCE TABLES--------------------------------------------------------
Z_0 = 377
a = 1.2
b = 2.86
SC_Imp_N = - (Z_0*(1+2*np.log(b/a)))/(2*beta_inj*(gamma_inj**2))
SC_Imp_N = -10
ZoN = InductiveImpedance(beam, profile, [SC_Imp_N] * N_t, rf, deriv_mode='diff')

print(SC_Imp_N)

total_ind_volt_ZoN = TotalInducedVoltage(beam, profile, [ZoN])

# Accelerator map
#+ [total_ind_volt_ZoN]
map_ = [profile] + [total_ind_volt_ZoN] +\
       [long_tracker]  + [bunchmonitor] + [plots]
print("Map set")
print("")

# Tracking --------------------------------------------------------------------
for i in range(1, N_t + 1):

    # Plot has to be done before tracking (at least for cases with separatrix)
    if (i % dt_plt) == 0:
        print("Outputting at time step %d..." % i)
        print("   Beam momentum %.6e eV" % beam.momentum)
        print("   Beam gamma %3.3f" % beam.gamma)
        print("   Beam beta %3.3f" % beam.beta)
        print("   Beam energy %.6e eV" % beam.energy)
        print("   Four-times r.m.s. bunch length %.4e s" % (4. * beam.sigma_dt))
        print("   Gaussian bunch length %.4e s" % profile.bunchLength)
    if (i % dt_plt) == 0:
        plot_induced_voltage_vs_bin_centers(total_ind_volt_ZoN, figure_index=i,
                                            style='.', dirname=this_directory + '../output_files/U-70_jump/1')
    # Track
    for m in map_:
        m.track()

    # Define losses according to separatrix and/or longitudinal position
    beam.losses_separatrix(ring, rf)
    #beam.losses_longitudinal_cut(1.65e-7, 1.90e-7)

# For testing purposes
test_string += '{:+10.10e}\t{:+10.10e}\t{:+10.10e}\t{:+10.10e}\n'.format(
    np.mean(beam.dE), np.std(beam.dE), np.mean(beam.dt), np.std(beam.dt))
with open(this_directory + '../output_files/U-70_jump.txt', 'w') as f:
    f.write(test_string)

source = r"/Users/Bell/GIT_REPOS/Protvino/BLonD-master/__EXAMPLES/output_files/U-70_jump.h5"
target = r"/Users/Bell/GIT_REPOS/Protvino/BLonD-master/__EXAMPLES/output_files/U-70_jump/U-70_jump.h5"

shutil.copyfile(source, target)

#plt.figure()
#plt.plot(profile.bin_centers * 1e9, total_ind_volt_time.induced_voltage,
#         lw=2, alpha=0.75, label='Resonator time domain')
#plt.plot(profile.bin_centers * 1e9, total_ind_volt_ZoN.induced_voltage,
#         lw=2, alpha=0.75, label=r'Z/n = -10 $\Omega$')
#plt.xlabel('Time [ns]')
#plt.ylabel('Induced voltage [V]')
#plt.legend(loc=2, fontsize='medium')
#plt.savefig(this_directory + '../output_files/U-70_jump/fig.png')

print("Done!")
