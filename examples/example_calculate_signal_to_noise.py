# %%
"""
.. calculate_signal_to_noise:

=================================
Calculate Signal-to-Noise
=================================

This example demonstrates how to use DNPLab to calculate the signal-to-noise ratio of an FID signal after applying a Fourier transform.

"""

# %%
# Load NMR Spectrum
# ---------------------------------
# Start by importing DNPLab. 

import dnplab as dnp

# First use some sample 1D TopSpin data. Example data is located in the data folder. All data enters into the same object structure so this example applies to any NMR format.

data = dnp.dnpImport.load("../data/topspin/5")

# %% Workspace
# We create a workspace to store multiple copies of the data, e.g. before each manipulation.

ws = dnp.create_workspace()
ws.add("raw", data)
ws.copy("raw", "proc")

# %%
# Raw data are in the processing buffer ws["proc"] and ws["raw"]. The following processing steps will only modify ws["proc"] but leave ws["raw"] untouched. That way, you can always return to the original data.
# We also process the data by removing the DC offset, applying apodization, performing a Fourier transform, and removing the phase angle.

dnp.dnpNMR.remove_offset(ws)
dnp.dnpNMR.window(ws)
dnp.dnpNMR.fourier_transform(ws)
dnp.dnpNMR.autophase(ws)

# %%
# Calculating Signal-to-Noise
# --------------------------
# First, calculate signal-to-noise with default values:

dnp.dnpTools.signal_to_noise(ws)

# As you can see, this uses the default values
# dim="f2",
# signal_center=0,
# signal_width="full",
# noise_center="default",
# noise_width="default".
# It returns a data object with the attributes "s_n", "signal", and "noise" added. These contain the signal-to-noise ratio, the signal region, and the noise region. To see this, simply print the attributes of the new data object.

print(ws["proc"].attrs)
print("Signal-to-noise ratio:", ws["proc"].attrs["s_n"])
print("Signal:", ws["proc"].attrs["signal"])
print("Noise:", ws["proc"].attrs["noise"])

# %% Adjusting noise_center
# Adding the parameter "noise_center" allows you to define noise at the low end of the spectrum. The default noise region is the top 5% of the number of data points.

dnp.dnpTools.signal_to_noise(ws, noise_center=10)

# Below is a plot of the spectrum with an overlay of the signal (green) and noise (red) regions.

dnp.dnpResults.plt.figure()
dnp.dnpResults.plot(ws['proc'], 'k-', label="Spectrum")
dnp.dnpResults.plot(ws['proc'].attrs["signal"], 'g-', label="Signal")
dnp.dnpResults.plot(ws['proc'].attrs["noise"], 'r:', label="Noise", alpha=0.5)
dnp.dnpResults.plt.legend()
dnp.dnpResults.plt.show()

# After each of the signal_to_noise calls, a plot is made showing the locations of the signal and noise regions.

# %% Noise width
# You can also manually define the noise width, and if it is too large it will be adjusted to fit within the data.

dnp.dnpTools.signal_to_noise(ws, noise_width=100)
dnp.dnpResults.plt.figure()
dnp.dnpResults.plot(ws['proc'], 'k-', label="Spectrum")
dnp.dnpResults.plot(ws['proc'].attrs["signal"], 'g-', label="Signal")
dnp.dnpResults.plot(ws['proc'].attrs["noise"], 'r:', label="Noise", alpha=0.5)
dnp.dnpResults.plt.legend()
dnp.dnpResults.plt.show()

# %% Signal width & center
# Similarly, the signal can be centered around a default value or manually defined, and the signal width can be either default or defined.

dnp.dnpTools.signal_to_noise(ws, signal_center=20, signal_width=10)
dnp.dnpResults.plt.figure()
dnp.dnpResults.plot(ws['proc'], 'k-', label="Spectrum")
dnp.dnpResults.plot(ws['proc'].attrs["signal"], 'g-', label="Signal")
dnp.dnpResults.plot(ws['proc'].attrs["noise"], 'r:', label="Noise", alpha=0.5)
dnp.dnpResults.plt.legend()
dnp.dnpResults.plt.show()

# %% Dimension of data
# You can also specify the dimension of the data to work with. The default is "f2".

dnp.dnpTools.signal_to_noise(ws, dim="t2")
dnp.dnpResults.plt.figure()
dnp.dnpResults.plot(ws['proc'], 'k-', label="Spectrum")
dnp.dnpResults.plot(ws['proc'].attrs["signal"], 'g-', label="Signal")
dnp.dnpResults.plot(ws['proc'].attrs["noise"], 'r:', label="Noise", alpha=0.5)
dnp.dnpResults.plt.legend()
dnp.dnpResults.plt.show()
