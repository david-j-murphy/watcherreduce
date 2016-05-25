# Work with Watcher Data
# Functions to load Watcher FITS files and automatically reduce them

import astropy.io.fits as pyfits
from watcherreduce import reduce
import dateutil.parser
import os
import datetime

import requests
import io

watcherserver = 'http://ssamr.ucd.ie'

from pynapple import getpynfilter, HEADERCONFIG


def searchMasterFlat(night, filter, limit=100, allowNewer=True):
	url = "%s/flatsearch?date=%04d-%02d-%02d&filter=%s&newer=%s&limit=%d" % (watcherserver, night.year, night.month, night.day, filter, allowNewer, limit)
	response = requests.get(url)
	if response.status_code == requests.codes.ok:
		datestring = response.json()['date']
		flatdate = dateutil.parser.parse(datestring)
		return flatdate
	else:
		return None

def downloadMasterFlat(night, filter):
	url = "%s/getflat?date=%04d-%02d-%02d&filter=%s" % (watcherserver, night.year, night.month, night.day, filter)
	response = requests.get(url)
	fitsfile = io.BytesIO(response.content)
	masterflathdu = pyfits.open(fitsfile)[0]
	return masterflathdu


def thisWatcherNight():
	now = datetime.datetime.utcnow()
	return watcherNight(now)


def watcherNight(imageDateTime):
	day = imageDateTime - datetime.timedelta(days = (imageDateTime.hour < 12))
#	date = day.date()
	return day


# Given a path to a FITS file, finds the Watcher night and filter. 
def findFlatDetailsForImage(fitspath,  headerconfig=HEADERCONFIG):
	imagehdu = pyfits.open(fitspath)[0]
	return findFlatDetailsForHDU(imagehdu,  headerconfig=headerconfig)


# Given an image HDU, finds the Watcher night and filter. 
def findFlatDetailsForHDU(imagehdu,  headerconfig=HEADERCONFIG):
	filter = getpynfilter(imagehdu.header)
	headerTime = imagehdu.header[headerconfig.get('Basic','datetime')]
	imageNight = watcherNight(dateutil.parser.parse(headerTime))
	return imageNight, filter


def loadReducedFits(fitspath, flatpath=None, biaspath=None, flatNight=None, headerconfig=HEADERCONFIG):
	imagehdu = pyfits.open(fitspath)[0]
	filter = getpynfilter(imagehdu.header)

	if flatpath:
		masterflathdu = pyfits.open(flatpath)[0]
	else:
		if not flatNight:
			flatNight, __ = findFlatDetailsForHDU(imagehdu, headerconfig=headerconfig)
			validNight = searchMasterFlat(flatNight, filter, limit = 100, allowNewer = True)		
		masterflathdu = downloadMasterFlat(validNight, filter)
	if biaspath:
		biashdu = pyfits.open(biaspath)[0]
	else:
		biashdu = None	
	reducedhdu = reduce.reduceImage(imagehdu, masterflathdu, bias=biashdu)
	return reducedhdu






