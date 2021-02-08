# Generate input files from axionCAMB
# MUSIC only reads ordinary CAMB transfer_out file
# and MUSIC expects a more recent version of CAMB than the modifed
# axionCAMB code
# Solution: Generate two CAMB-like files, one for axions, one for CDM

import numpy as np
from scipy.interpolate import interp1d
import argparse

parser = argparse.ArgumentParser(description='Generate CAMB files for MUSIC for mixed axion ICs')
parser.add_argument('input_file', help='Input file name from axionCAMB e.g. 1e-27axions_transfer_out.dat')
parser.add_argument('output_file', help='Output file root which leads to file names OUT_cdm.dat and OUT_axions.dat')
args = parser.parse_args()

input_file_name  = args.input_file
output_file_name = args.output_file

# Load data from regular CAMB for modification
# MUSIC will be run twice for the mixed case: 
# once for the axions particles and once for the cdm particles

data_CAMB = np.loadtxt('example_CAMB_transfer_out.dat') # Example CAMB output of the version compatible with MUSIC

# Data from axionCAMB
data_axionCAMB = np.loadtxt(input_file_name)

# Calculate transfer functions
k     = data_axionCAMB[:,0]
Tkc   = data_axionCAMB[:,1]
Tkb   = data_axionCAMB[:,2]
Tkax  = data_axionCAMB[:,6]
Tktot = data_axionCAMB[:,8]

mixed_transfer_cdm    = interp1d(k, Tkc, bounds_error=False, fill_value=Tkc[0])
mixed_transfer_axions = interp1d(k, Tkax, bounds_error=False, fill_value=Tkax[0])
mixed_transfer_total  = interp1d(k, Tktot, bounds_error=False, fill_value=Tktot[0])

### AXIONS ###
factor = mixed_transfer_axions(data_CAMB[:,0]) / mixed_transfer_cdm(data_CAMB[:,0]) # Growth suppression taken as ratio of CDM growth to axion growth

modified_output_axions      = data_CAMB.copy()
modified_output_axions[:,1] = mixed_transfer_axions(data_CAMB[:,0])
modified_output_axions[:,6] = mixed_transfer_total(data_CAMB[:,0])


# Use baryons as the placeholder for DM on a grid
modified_output_axions[:,2]   = mixed_transfer_axions(data_CAMB[:,0]) # baryon transfer function
modified_output_axions[:,10] *= factor # Newtonian-gauge CDM velocity
modified_output_axions[:,11] = modified_output_axions[:,10] # Newtonian-gauge baryon velocity
modified_output_axions[:,12] *= factor # relative baryon-CDM velocity (may not be needed)

np.savetxt(output_file_name + '_axions.dat', modified_output_axions, delimiter='\t')


### CDM ###
modified_output_cdm       = data_CAMB.copy()
modified_output_cdm[:,1]  = mixed_transfer_cdm(data_CAMB[:,0])
modified_output_cdm[:,6]  = mixed_transfer_total(data_CAMB[:,0])
modified_output_cdm[:,2]  = modified_output_cdm[:,1] # usually baryons, now replaced with DM on grid
modified_output_cdm[:,11] = modified_output_cdm[:,10] # same as above but for velocity

np.savetxt(output_file_name + '_cdm.dat', modified_output_cdm, delimiter='\t')
