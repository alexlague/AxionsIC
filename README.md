# AxionsIC

Code to generate CAMB files which can be read by MUSIC
To get axion ICs, use the axionCAMB code: https://github.com/dgrin1/axionCAMB

Run ./axionCAMB params.ini once to get PREFIX_transfer_out.dat file
Run python generate_modified_CAMB_files.py <PREFIX_transfer_out.dat> <output_name>
This will produce to files to be read by MUSIC to generate the axion and CDM ICs separately
Run MUSIC twice with the transfer: camb_file option and the filename matching the output of the python script in the .conf file e.g.
./MUSIC axion_ICs.conf
./MUSIC	CDM_ICs.conf
Finally, you can run mixed axion DM sims with axionNYX

NOTES

(1) Make sure the transfer redshift matches the redshift of the ICs.
(2) Note the value of sigma8 which is printed on the screen when running axionCAMB
    this value will be needed for the MUSIC parameter files.
(3) As usual, make sure the values in the axionCAMB parameter files 
    are the same as the MUSIC and axionNYX parameters files.

