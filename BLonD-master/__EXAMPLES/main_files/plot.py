from __future__ import division
import h5py as hp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.layout_engine import PlaceHolderLayoutEngine

def plot_several_bunch_length_evol(turns,
                           h5file1, label1,
                           h5file2, label2,
                           h5file3, label3,
                           h5file4=None, label4=None,
                           h5file5=None, label5=None,
                           output_freq = 1, dirname = 'fig', show_plot = False):

    h5data1 = hp.File(h5file1, 'r')
    h5data2 = hp.File(h5file2, 'r')
    h5data3 = hp.File(h5file3, 'r')
    if h5file4 is not None:
        h5data4 = hp.File(h5file4, 'r')
    if h5file5 is not None:
        h5data5 = hp.File(h5file5, 'r')
    time_step = int(turns)

    # Get bunch energy data in eVs
    if output_freq < 1:
        output_freq = 1
    ndata = int(time_step/output_freq)
    t = output_freq*np.arange(ndata)
    bl1 = np.array(h5data1["/Beam/sigma_dt"][0:ndata], dtype = np.double)
    bl2 = np.array(h5data2["/Beam/sigma_dt"][0:ndata], dtype = np.double)
    bl3 = np.array(h5data3["/Beam/sigma_dt"][0:ndata], dtype = np.double)
    if h5file4 is not None:
        bl4 = np.array(h5data4["/Beam/sigma_dt"][0:ndata], dtype = np.double)
        bl4 *= 4
        bl4[time_step:] = np.nan
    if h5file5 is not None:
        bl5 = np.array(h5data5["/Beam/sigma_dt"][0:ndata], dtype = np.double)
        bl5 *= 4
        bl5[time_step:] = np.nan
    bl1 *= 4
    bl2 *= 4
    bl3 *= 4

    bl1[time_step:] = np.nan
    bl2[time_step:] = np.nan
    bl3[time_step:] = np.nan

    # Plot
    fig = plt.figure(1)
    fig.set_size_inches(8,6)
    ax = plt.axes()
    ax.plot(t, bl1, linewidth=2, label=label1)
    ax.legend()
    ax.plot(t, bl2, linewidth=2, label=label2)
    ax.legend()
    ax.plot(t, bl3, linewidth=2, label=label3)
    ax.legend()
    if h5file4 is not None:
        ax.plot(t, bl4, linewidth=2, label=label4)
        ax.legend()
    if h5file5 is not None:
        ax.plot(t, bl5, linewidth=2, label=label5)
        ax.legend()
    ax.set_xlabel(r"No. turns [T$_0$]")
    ax.set_ylabel (r"Bunch length, $\Delta t_{4\sigma}$ r.m.s. [s]")
    if time_step > 100000:
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    # Output plot
    if show_plot:
        plt.show()
    else:
        fign = dirname +'/several_bunch_length_evol.png'
        plt.savefig(fign)
    plt.clf()

def plot_several_plot_emittance_evol(turns,
                           h5file1, label1,
                           h5file2, label2,
                           h5file3, label3,
                           h5file4=None, label4=None,
                           h5file5=None, label5=None,
                           output_freq = 1, dirname = 'fig', show_plot = False):

    h5data1 = hp.File(h5file1, 'r')
    h5data2 = hp.File(h5file2, 'r')
    h5data3 = hp.File(h5file3, 'r')
    if h5file4 is not None:
        h5data4 = hp.File(h5file4, 'r')
    if h5file5 is not None:
        h5data5 = hp.File(h5file5, 'r')
    time_step = int(turns)

    # Get bunch energy data in eVs
    if output_freq < 1:
        output_freq = 1
    ndata = int(time_step/output_freq)
    t = output_freq*np.arange(ndata)
    bl1 = np.array(h5data1["/Beam/epsn_rms_l"][0:ndata], dtype = np.double)
    bl2 = np.array(h5data2["/Beam/epsn_rms_l"][0:ndata], dtype = np.double)
    bl3 = np.array(h5data3["/Beam/epsn_rms_l"][0:ndata], dtype = np.double)
    if h5file4 is not None:
        bl4 = np.array(h5data4["/Beam/epsn_rms_l"][0:ndata], dtype = np.double)
        bl4 *= 6
        bl4[time_step:] = np.nan
    if h5file5 is not None:
        bl5 = np.array(h5data5["/Beam/epsn_rms_l"][0:ndata], dtype = np.double)
        bl5 *= 6
        bl5[time_step:] = np.nan
    bl1 *= 6
    bl2 *= 6
    bl3 *= 6

    bl1[time_step:] = np.nan
    bl2[time_step:] = np.nan
    bl3[time_step:] = np.nan

    # Plot
    fig = plt.figure(1)
    fig.set_size_inches(8,6)
    ax = plt.axes()
    ax.plot(t, bl1, linewidth=2, label=label1)
    ax.legend()
    ax.plot(t, bl2, linewidth=2, label=label2)
    ax.legend()
    ax.plot(t, bl3, linewidth=2, label=label3)
    ax.legend()
    if h5file4 is not None:
        ax.plot(t, bl4, linewidth=2, label=label4)
        ax.legend()
    if h5file5 is not None:
        ax.plot(t, bl5, linewidth=2, label=label5)
        ax.legend()
    ax.set_xlabel(r"No. turns [T$_0$]")
    ax.set_ylabel (r"95% Emittance, $6\pi \Delta E_{\sigma} \Delta t_{\sigma}$ r.m.s. [eVs]")
    if time_step > 100000:
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    # Output plot
    if show_plot:
        plt.show()
    else:
        fign = dirname +'/several_bunch_emittance.png'
        plt.savefig(fign)
    plt.clf()

def plot_several_bunch_energy_spread_evol(turns,
                           h5file1, label1,
                           h5file2, label2,
                           h5file3, label3,
                           h5file4=None, label4=None,
                           h5file5=None, label5=None,
                           output_freq = 1, dirname = 'fig', show_plot = False):

    h5data1 = hp.File(h5file1, 'r')
    h5data2 = hp.File(h5file2, 'r')
    h5data3 = hp.File(h5file3, 'r')
    if h5file4 is not None:
        h5data4 = hp.File(h5file4, 'r')
    if h5file5 is not None:
        h5data5 = hp.File(h5file5, 'r')
    time_step = int(turns)

    # Get bunch energy data in eVs
    if output_freq < 1:
        output_freq = 1
    ndata = int(time_step/output_freq)
    t = output_freq*np.arange(ndata)
    bl1 = np.array(h5data1["/Beam/sigma_dE"][0:ndata], dtype = np.double)
    bl2 = np.array(h5data2["/Beam/sigma_dE"][0:ndata], dtype = np.double)
    bl3 = np.array(h5data3["/Beam/sigma_dE"][0:ndata], dtype = np.double)
    if h5file4 is not None:
        bl4 = np.array(h5data4["/Beam/sigma_dE"][0:ndata], dtype = np.double)
        bl4 *= 4
        bl4[time_step:] = np.nan
    if h5file5 is not None:
        bl5 = np.array(h5data5["/Beam/sigma_dE"][0:ndata], dtype = np.double)
        bl5 *= 4
        bl5[time_step:] = np.nan
    bl1 *= 4
    bl2 *= 4
    bl3 *= 4

    bl1[time_step:] = np.nan
    bl2[time_step:] = np.nan
    bl3[time_step:] = np.nan

    # Plot
    fig = plt.figure(1)
    fig.set_size_inches(8,6)
    ax = plt.axes()
    ax.plot(t, bl1, linewidth=2, label=label1)
    ax.legend()
    ax.plot(t, bl2, linewidth=2, label=label2)
    ax.legend()
    ax.plot(t, bl3, linewidth=2, label=label3)
    ax.legend()
    if h5file4 is not None:
        ax.plot(t, bl4, linewidth=2, label=label4)
        ax.legend()
    if h5file5 is not None:
        ax.plot(t, bl5, linewidth=2, label=label5)
        ax.legend()
    ax.set_xlabel(r"No. turns [T$_0$]")
    ax.set_ylabel (r"Energy Spread, $\Delta E_{4\sigma}$ r.m.s. [eV]")
    if time_step > 100000:
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    # Output plot
    if show_plot:
        plt.show()
    else:
        fign = dirname +'/several_bunch_energy_spread.png'
        plt.savefig(fign)
    plt.clf()


# DIFFERENT MCF AND MODELS, WO JUMP, WO SC
h5file1 = '/Users/Bell/GIT_REPOS/Protvino/BLonD-master/__EXAMPLES/output_files/U-70_7.0-13.0(simple)/U-70.h5'
h5file2 = '/Users/Bell/GIT_REPOS/Protvino/BLonD-master/__EXAMPLES/output_files/U-70_7.0-13.0(exact)/U-70.h5'
h5file3 = '/Users/Bell/GIT_REPOS/Protvino/BLonD-master/__EXAMPLES/output_files/U-70_7.0-13.0_MCF(exact)/U-70.h5'
label1='simple, first-order'
label2='exact, first-order'
label3='exact, second-order'

# DIFFERENT MCF, WO JUMP, SC, INTENCITY
h5file4 = '/Users/Bell/GIT_REPOS/Protvino/BLonD-master/__EXAMPLES/output_files/U-70_7.0-13.0_MCF(exact)/U-70.h5'
h5file5 = '/Users/Bell/GIT_REPOS/Protvino/BLonD-master/__EXAMPLES/output_files/U-70_7.0-9.0_MCF_+10(exact)/U-70.h5'
h5file6 = '/Users/Bell/GIT_REPOS/Protvino/BLonD-master/__EXAMPLES/output_files/U-70_7.0-9.0_MCF_+10_int(exact)/U-70.h5'
h5file7 = '/Users/Bell/GIT_REPOS/Protvino/BLonD-master/__EXAMPLES/output_files/U-70_7.0-9.0_MCF_-10(exact)/U-70.h5'
h5file8 = '/Users/Bell/GIT_REPOS/Protvino/BLonD-master/__EXAMPLES/output_files/U-70_7.0-9.0_MCF_-10_int(exact)/U-70.h5'

label4='exact, first-order, Z=+10i'
label5='exact, second-order, Z=+10i'
label6='exact, second-order, Z=+10i, int'
label7='exact, second-order, Z=-10i'
label8='exact, second-order, Z=-10i, int'

# DIFFERENT MCF, JUMP, WO SC

# JUMP, SC, INTENCITY

#turns = 30000-1
#plot_several_bunch_energy_spread_evol(turns,
#                                   h5file1, label1,
#                                   h5file2, label2,
#                                   h5file3, label3)
#plot_several_bunch_length_evol(turns,
#                                   h5file1, label1,
#                                   h5file2, label2,
#                                   h5file3, label3)
#plot_several_plot_emittance_evol(turns,
#                                   h5file1, label1,
#                                   h5file2, label2,
#                                   h5file3, label3)

turns = 10000-1
plot_several_bunch_energy_spread_evol(turns,
                                   h5file3, label3,
                                   h5file5, label5,
                                   h5file6, label6,
                                   h5file7, label7,
                                   h5file8, label8)
plot_several_bunch_length_evol(turns,
                                   h5file3, label3,
                                   h5file5, label5,
                                   h5file6, label6,
                                   h5file7, label7,
                                   h5file8, label8)
plot_several_plot_emittance_evol(turns,
                                   h5file3, label3,
                                   h5file5, label5,
                                   h5file6, label6,
                                   h5file7, label7,
                                   h5file8, label8)
