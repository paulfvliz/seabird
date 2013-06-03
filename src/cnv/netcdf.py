#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Export the parced data into a NetCDF following different patterns
"""

from datetime import datetime

try:
    import netCDF4
except:
    import pupynere

def cnv2nc(data, filename):
    """
    """
    print "Saving netcdf output file: %s" % filename

    nc = netCDF4.Dataset(filename, 'w', format='NETCDF4')

    nc.history = "Created by cnv2nc (PyCNV)"

    nc.DATE_CREATION = datetime.now().strftime("%Y%m%s%H%M%S")

    #print "Global attributes"
    A = data.attributes.keys(); A.sort()
    for a in A:
        try:
            nc.__setattr__(a, data.attributes[a])
        except:
            print "Problems with %s" % a

    nc.createDimension('scan', int(data.attributes['nvalues']))

    print "\nVariabes"
    cdf_variables = {}
    for k in data.keys():
        print k
        cdf_variables[k] = nc.createVariable(k, 'd', ('scan',))
        dir(cdf_variables[k])
        cdf_variables[k].missing_value = data[k].fill_value
        for a in data[k].attributes.keys():
            print "\t\033[93m%s\033[0m: %s" % (a, data[k].attributes[a])
            #cdf_variables[k].__setattr__(a, data[k].attributes[a])
        cdf_variables[k][:] = data[k].data

    nc.close()
