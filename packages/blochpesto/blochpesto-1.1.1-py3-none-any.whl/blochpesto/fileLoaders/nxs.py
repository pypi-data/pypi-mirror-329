try:	import h5py
except ImportError: print("\t(Warning): Couldn't import the h5py module. You will not be able to load or export nexus data files.  Install it from the terminal with the command 'pip install h5py'")

try:	import numpy as np
except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")


def load(fileName,**kwargs):

	beQuiet=kwargs.get('beQuiet')
	regionIndex=kwargs.get('regionIndex')
	whichManipulatorAxis=kwargs.get('whichManipulatorAxis')
	loadedSpectrum={}
	loadedSpectrum['Metadata']={}
	loadedSpectrum['Metadata']['CurrentFilePath']=fileName


	with h5py.File(fileName, "r") as nx:
		try: nx_entry = nx[nx.attrs["default"]]
		except: nx_entry = nx[list(nx.keys())[0]] # Assume the default entry is the first one

		nx_data = nx_entry[nx_entry.attrs["default"]]
		signal = nx_data[nx_data.attrs["signal"]]
		attr_axes = nx_data.attrs["axes"]

		if len(np.shape(signal))>1: axes = [nx_data[ii] for ii in attr_axes]
		else: axes = nx_data[attr_axes]

		loadedSpectrum={}
		loadedSpectrum['Metadata']={}

		if len(np.shape(signal))>1:
			loadedSpectrum['Axis'],loadedSpectrum['AxisLabel'],loadedSpectrum['AxisUnits']=[],[],[]
			for ii in axes:
				loadedSpectrum['Axis'].append(np.array(ii))
				loadedSpectrum['AxisLabel'].append(ii.name.split("/")[-1])
				loadedSpectrum['AxisUnits'].append(ii.attrs['Units'])
		else:
			loadedSpectrum['Axis']=np.array(axes)
			loadedSpectrum['AxisLabel']=axes.name.split("/")[-1]
			loadedSpectrum['AxisUnits']=axes.attrs['Units']  
			
		loadedSpectrum['data']=np.array(signal)
	
	return loadedSpectrum

"""

	d = f[list(f.keys())[1-regionIndex]]

	try:
		facility_name=d['instrument/name'][()]
		if len(np.shape(facility_name))>0: facility_name=d['instrument/name'][()][0]
		facility_name=facility_name.decode()
		loadedSpectrum['Metadata']['Facility']=facility_name

	except Exception as e:
		print("Had an error trying to find a facility identifier in the metadata: ",e)

	try: loadedSpectrum['Metadata']['Lens Mode']=d['instrument/analyser/lens_mode'][0].decode()
	except: pass
	try: loadedSpectrum['Metadata']['Pass Energy']=d['instrument/analyser/pass_energy'][0]
	except: pass
	try: loadedSpectrum['Metadata']['Acquisition Mode']=d['instrument/analyser/acquisition_mode'][0].decode()
	except: pass
	





	dataShape = np.shape(d['analyser']['data'])
	
	#print("Data matrix has shape {}".format(dataShape))
	if dataShape[0]==1:
		reducedData = np.reshape(d['analyser']['data'],(dataShape[1],dataShape[2]))
		#print("Reduced shape is {}".format(np.shape(reducedData)))	
	else:
		reducedData=d['analyser']['data']
	dataDimensions = len(np.shape(reducedData))

	if dataDimensions==2:
		print("This is a single image (2D dataset)")

		try: loadedSpectrum['Metadata']['Manipulator Azimuth']=d["instrument/manipulator/saazimuth"][()][0]
		except: pass
		try: loadedSpectrum['Metadata']['Manipulator Polar']=d["instrument/manipulator/sapolar"][()][0]
		except: pass
		try: loadedSpectrum['Metadata']['Manipulator Tilt']=d["instrument/manipulator/satilt"][()][0]
		except: pass
		try: loadedSpectrum['Metadata']['Manipulator X']=d["instrument/manipulator/sax"][()][0]
		except: pass
		try: loadedSpectrum['Metadata']['Manipulator Y']=d["instrument/manipulator/say"][()][0]
		except: pass
		try: loadedSpectrum['Metadata']['Manipulator Z']=d["instrument/manipulator/saz"][()][0]
		except: pass
		loadedSpectrum['Axis']=[[],[]]
		loadedSpectrum['AxisLabel']=["",""]
		loadedSpectrum['AxisUnits']=["",""]
		
		# Collapse the energy axis if required
		if len(np.shape(d['analyser/energies']))>1:
			#print("COLLAPSING ENERGY AXIS")
			loadedSpectrum['Axis'][0]=d['analyser/energies'][0,:]
		else:
			#print("NOT COLLAPSING ENERGY AXIS")
			loadedSpectrum['Axis'][0]=d['analyser/energies']
		loadedSpectrum['AxisLabel'][0]="Kinetic energy"
		loadedSpectrum['AxisUnits'][0]="eV" 

		loadedSpectrum['Axis'][1]=[ii for ii in d['analyser/angles']]
		loadedSpectrum['AxisLabel'][1]="Angle"  
		loadedSpectrum['AxisUnits'][1]="$\degree$" 

		loadedSpectrum['data'] = np.moveaxis(reducedData,source=(0,1),destination=(1,0))


	if dataDimensions==3:
		print("This is a 1D scan (3D dataset)")
		analyserEntries = list(d['analyser'].keys())
		axes=[ii for ii in analyserEntries if ii!="data"]
		#print("Axis names are:",axes)

		measurementType=None
		if "energies" in axes and "angles" in axes and "deflector_x" in axes:
			measurementType="deflector"
			print("I think the scanned axis was the deflector")
		if "energies" in axes and "angles" in axes and "sapolar" in axes:
			measurementType="polar"
			print("I think the scanned axis was manipulator polar")

		loadedSpectrum['Axis']=[[],[],[]]
		loadedSpectrum['AxisLabel']=["","",""]
		loadedSpectrum['AxisUnits']=["","",""]
		
		# Collapse the energy axis if required
		if len(np.shape(d['analyser']['energies']))>1:
			#print("COLLAPSING ENERGY AXIS")
			loadedSpectrum['Axis'][0]=d['analyser']['energies'][0,:]
		else:
			#print("NOT COLLAPSING ENERGY AXIS")
			loadedSpectrum['Axis'][0]=d['analyser']['energies']

		loadedSpectrum['AxisLabel'][0]="Kinetic energy"
		loadedSpectrum['AxisUnits'][0]="eV" 

		loadedSpectrum['Axis'][1]=[ii for ii in d['analyser']['angles']]
		loadedSpectrum['AxisLabel'][1]="Angle"  
		loadedSpectrum['AxisUnits'][1]="$\degree$" 

		if measurementType=="polar":
			loadedSpectrum['Axis'][2]=[ii for ii in d['analyser']['sapolar']]
			loadedSpectrum['AxisLabel'][2]="Angle"  
			loadedSpectrum['AxisUnits'][2]="$\degree$" 

		if measurementType=="deflector":
			loadedSpectrum['Axis'][2]=[ii for ii in d['analyser']['deflector_x']]
			loadedSpectrum['AxisLabel'][2]="Angle"  
			loadedSpectrum['AxisUnits'][2]="$\degree$" 

		loadedSpectrum['data'] = np.moveaxis(d['analyser']['data'],source=(0,1,2),destination=(2,1,0))

	if dataDimensions==4:
		print("This is a 2D scan (4D dataset), I'll assume for now that it's an x-y scan")

		loadedSpectrum['Axis']=[[],[],[],[]]
		loadedSpectrum['AxisLabel']=["","","",""]
		loadedSpectrum['AxisUnits']=["","","",""]
		
		# Collapse the energy axis if required
		if len(np.shape(d['analyser']['energies']))>1:
			#print("COLLAPSING ENERGY AXIS")
			loadedSpectrum['Axis'][0]=d['analyser']['energies'][0,:]
		else:
			#print("NOT COLLAPSING ENERGY AXIS")
			loadedSpectrum['Axis'][0]=d['analyser']['energies']
		loadedSpectrum['AxisLabel'][0]="Kinetic energy"
		loadedSpectrum['AxisUnits'][0]="eV" 

		loadedSpectrum['Axis'][1]=np.asarray(d['analyser']['angles'])
		loadedSpectrum['AxisLabel'][1]="Angle"  
		loadedSpectrum['AxisUnits'][1]="$\degree$" 

		loadedSpectrum['Axis'][2]=np.asarray(d['analyser']['smy'][:,0])
		loadedSpectrum['AxisLabel'][2]="Y"  
		loadedSpectrum['AxisUnits'][2]="um" 
		# Should be 31 elements

		loadedSpectrum['Axis'][3]=np.asarray(d['analyser']['smx'][0,:])
		loadedSpectrum['AxisLabel'][3]="X"  
		loadedSpectrum['AxisUnits'][3]="um" 
		# Should be 46 elements



		loadedSpectrum['minorAxis']=loadedSpectrum['Axis'][2]
		loadedSpectrum['minorAxisLabel']=loadedSpectrum['AxisLabel'][2]
		loadedSpectrum['minorAxisUnits']=loadedSpectrum['AxisUnits'][2]
		loadedSpectrum['majorAxis']=loadedSpectrum['Axis'][3]
		loadedSpectrum['majorAxisLabel']=loadedSpectrum['AxisLabel'][3]
		loadedSpectrum['majorAxisUnits']=loadedSpectrum['AxisUnits'][3]

		# Stored as smy,smx,angles,energies ((31, 46, 1000, 1064))
		# pesto would prefer energies,angles,smy,smx
		loadedSpectrum['data'] = np.transpose(d['analyser']['data'],axes=[3,2,0,1])





	del f
	return loadedSpectrum
"""
