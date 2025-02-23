try:	import h5py
except ImportError: print("\t(Warning): Couldn't import the h5py module. You will not be able to load or export nexus data files.  Install it from the terminal with the command 'pip install h5py'")

import os,math,time,copy,random

try:	import numpy as np
except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")

try:	import matplotlib
except ImportError: print("\t(ERROR): Couldn't import the matplotlib module. This is required for basic functionality. Install it with the command 'pip install matplotlib'")

try:	import scipy
except ImportError: print("\t(Warning): Couldn't import the scipy module. This is required for basic functionality. Install it with the command 'pip install scipy'")

def nxs(spectrum,fileName): #NeXus export

	with h5py.File(fileName,'w') as f:

		# Per the NeXus format manual:
		# every file must contain NXsample, NXmonitor, NXdata and NXinstrument groups

		# Further, recommended names for these are sample, control, data and instrument (https://manual.nexusformat.org/rules.html)
		# data group typically contains links to where to find the default plottable

		# When doing scans, the scanned direction must always be the first dimension in the data. (This is because  HDF allows data to be appended 
		# to the first dimension during a scan)

		# NXcollection is the recomended class to use for storing beamline parameters

		# NeXus dates and times should be stored using the ISO 8601 [5] format'(https://www.w3.org/TR/NOTE-datetime)

		# Eventually you should be storing M4 drain current in the monitor group, it's intended for normalization data


		f.attrs['default'] = 'entry'

		nxentry = f.create_group('entry')
		nxentry.attrs["NX_class"] = 'NXentry'
		nxentry.attrs['default'] = 'data'

		# MANDATORY DATA GROUP  ----> SPECIFIC TO THE DATA TYPE BEING SAVED
		nxdata = nxentry.create_group('data')	
		nxdata.attrs["NX_class"] = 'NXdata'
		nxdata["data"] = h5py.SoftLink('/entry/instrument/analyser/data')
		

		if len(np.shape(spectrum['data']))==1:
			softlink = "/entry/instrument/analyser/{}".format(spectrum['AxisLabel'])
			nxdata[spectrum['AxisLabel']] = h5py.SoftLink(softlink)
			nxdata.attrs["axes"] = spectrum['AxisLabel']
		
		else:
			for ii,axis in enumerate(spectrum['Axis']):	
				softlink = "/entry/instrument/analyser/{}".format(spectrum['AxisLabel'][ii])
				nxdata[spectrum['AxisLabel'][ii]] = h5py.SoftLink(softlink)
			nxdata.attrs["axes"] = [ii for ii in spectrum['AxisLabel']] 


		nxdata.attrs["signal"] = 'data' # REQUIRED
		

		# MANDATORY INSTRUMENT GROUP --> FOR ENDSTATION STATUS
		nxinstrument = nxentry.create_group('instrument')
		nxinstrument.attrs["NX_class"] = 'NXinstrument'	
		nxinstrument.create_dataset('name',data="Bloch")

		manipulator = nxinstrument.create_group('manipulator')
		manipulator.attrs["NX_class"] = 'NXgoniometer'
		try:
			manipulator.create_dataset('X',data=spectrum['Metadata']['Manipulator X']).attrs["units"]='mm'
			manipulator.create_dataset('Y',data=spectrum['Metadata']['Manipulator Y']).attrs["units"]='mm'
			manipulator.create_dataset('Z',data=spectrum['Metadata']['Manipulator Z']).attrs["units"]='mm'
			manipulator.create_dataset('Azimuth',data=spectrum['Metadata']['Manipulator Azimuth']).attrs["units"]='degrees'
			manipulator.create_dataset('Polar',data=spectrum['Metadata']['Manipulator Polar']).attrs["units"]='degrees'
			manipulator.create_dataset('Tilt',data=spectrum['Metadata']['Manipulator Tilt']).attrs["units"]='degrees'
		except Exception as e: 
			print("failed to write manipulator positions: ",e)

		anaPressure = random.random()*100
		nxinstrument.create_dataset('Analysis_chamber_pressure',data=anaPressure).attrs["units"]='mBar'

		cryoTemp = random.random()*100
		nxinstrument.create_dataset('Cryostat_Temperature',data=cryoTemp).attrs["units"]='K'


		# (OPTIONAL) DETECTOR GROUP --> FOR ANALYZER INFO

		nxanalyser = nxinstrument.create_group('analyser')
		nxanalyser.attrs["NX_class"] = 'NXdetector'
		nxanalyser.create_dataset('data',data=spectrum['data'])

		if len(np.shape(spectrum['data']))==1:
			jj=nxanalyser.create_dataset(spectrum['AxisLabel'],data=spectrum['Axis'])
			jj.attrs["Units"] = spectrum['AxisUnits']	

		else:	
			for ii,axis in enumerate(spectrum['Axis']):	
				jj=nxanalyser.create_dataset(spectrum['AxisLabel'][ii],data=axis)
				jj.attrs["Units"] = spectrum['AxisUnits'][ii]


		#NeXus dates and times should be stored using the ISO 8601 [5] format'(https://www.w3.org/TR/NOTE-datetime)
		#datetime.datetime.now().isoformat()
		#nxanalyser.create_dataset('Measurement start time',data='0')
		#datetime.datetime.now().isoformat()
		#nxanalyser.create_dataset('Measurement finish time',data='0')

		nxanalyser.create_dataset('entrance_slit_direction',data='vertical')
		nxanalyser.create_dataset('entrance_slit_shape',data='straight')




		# MANDATORY SAMPLE GROUP
		nxsample = nxentry.create_group('sample')
		nxsample.attrs["NX_class"] = 'NXsample'	

		# MANDATORY MONITOR GROUP
		nxmonitor = nxentry.create_group('control')
		nxmonitor.attrs["NX_class"] = 'NXmonitor'	

		# (OPTIONAL) COLLECTION GROUP --> FOR BEAMLINE STATUS
		beamline = nxentry.create_group('beamline')
		beamline.attrs["NX_class"] = 'NXcollection'	

		#EPU_gap = random.random()*100
		#beamline.create_dataset('EPU gap',data=EPU_gap).attrs["units"]='mm'

		#EPU_phase = random.random()*100
		#beamline.create_dataset('EPU phase',data=EPU_phase).attrs["units"]='mm'

		#----------------------------
		#monochromator = beamline.create_group('monochromator')
		#monochromator.attrs["NX_class"] = 'NXmonochromator'

		#hv = random.random()*100
		#monochromator.create_dataset('energy_corrected',data=hv).attrs["units"]='eV'

		# Grating, cff,
		#slit_vgap = random.random()*100
		#monochromator.create_dataset('exit_slit_vgap',data=slit_vgap).attrs["units"]='um'

		#slit_hgap = random.random()*100
		#monochromator.create_dataset('exit_slit_hgap',data=slit_hgap).attrs["units"]='um'

		#resolution = random.random()*100
		#monochromator.create_dataset('calculated_beamline_resolution',data=resolution).attrs["units"]='meV'

		#beam_hsize = random.random()*100
		#monochromator.create_dataset('calculated_spotsize_horizontal',data=beam_hsize).attrs["units"]='um'

		#beam_vsize = random.random()*100
		#monochromator.create_dataset('calculated_spotsize_vertical',data=beam_vsize).attrs["units"]='um'

		#--------------
		#R1 = beamline.create_group('Ring')
		#R1.attrs["NX_class"] = 'NXsource'

		#ringCurrent = random.random()*100
		#R1.create_dataset('Current',data=ringCurrent).attrs["units"]='mA'



	f.close()



def txt(spectrum,fileName=""):
	if fileName=="":
		print("I need a name for this exported file")
		return

	if len(np.shape(spectrum['data']))==1:
		with open(fileName,'w+') as f:
			f.write("{}\tIntensity\n".format(spectrum['AxisLabel']))
			for ii,jj in zip(spectrum['Axis'],spectrum['data']):
				f.write("{}\t{}\n".format(ii,jj))

	else:
		print("Sorry, I can currently only export 1D data")

