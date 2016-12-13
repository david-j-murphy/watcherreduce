import copy
import numpy as np


def reduceImage(imagehdu, masterflathdu, bias=None):
	biasdata = safeBiasData(bias)
	reduceddata = (imagehdu.data - biasdata)/masterflathdu.data
	reducedhdu = copy.copy(imagehdu)
	reducedhdu.data = np.copy(reduceddata)
	return reducedhdu


def safeBiasData(biashdu):
	if biashdu:
		biasdata = biashdu.data
	else:
		biasdata = np.full((1024,1024), 400.0) # Maybe fix hardcoded size in future!
	return biasdata



