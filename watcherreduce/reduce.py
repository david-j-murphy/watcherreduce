import copy
import numpy as np


def reduceImage(imagehdu, masterflathdu, bias=None):
	biasdata = safeBiasData(bias)
	reduceddata = (imagehdu.data - biasdata)/masterflathdu.data
	reducedhdu = copy.deepcopy(imagehdu)
	reducedhdu.data[:,:] = reduceddata[:,:]
	return reducedhdu


def safeBiasData(biashdu):
	if biashdu:
		biasdata = biashdu.data
	else:
		biasdata = np.full((1024,1024), 400) # Maybe fix hardcoded size in future!
	return biasdata



