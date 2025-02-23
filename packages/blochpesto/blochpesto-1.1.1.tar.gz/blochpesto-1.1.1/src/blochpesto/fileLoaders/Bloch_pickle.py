try:	import numpy as np
except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")

import pickle

def load(fileName,**kwargs):


	with open(fileName, "rb") as f:
		D = pickle.load(f)
	
	loadedSpectrum={}
	loadedSpectrum['Metadata']={}
	loadedSpectrum['Axis']=[[],[],[],[]]
	loadedSpectrum['AxisLabel']=["Ek","Angle","X","Y"]
	loadedSpectrum['AxisUnits']=["eV","deg","mm","mm"]

	analyzer_definition = D.get("snapshot_definition")
	map_definition = D.get("map_definition")

	loadedSpectrum['Metadata']['Dwell Time']=analyzer_definition['dwell_time']
	loadedSpectrum['Metadata']['Pass Energy']=analyzer_definition['Ep']
	loadedSpectrum['Metadata']['Lens Mode']=analyzer_definition['lens_mode']
	
	loadedSpectrum['Axis'][0]=D.get("scan_data_energy")
	loadedSpectrum['Axis'][1]=D.get("scan_data_angle")
	loadedSpectrum['Axis'][2]=np.linspace(map_definition['xstart'],map_definition['xstop'],map_definition['xsteps']+1)
	loadedSpectrum['Axis'][3]=np.linspace(map_definition['ystart'],map_definition['ystop'],map_definition['ysteps']+1)
	loadedSpectrum['data'] = np.zeros((analyzer_definition['energy_channels'],analyzer_definition['angle_channels'],len(loadedSpectrum['Axis'][2]),len(loadedSpectrum['Axis'][3])))
	data=D.get("scan_data_snapshots")
	
	frameIndex=0
	for y_index,y_val in enumerate(loadedSpectrum['Axis'][3]):
		for x_index,x_val in enumerate(loadedSpectrum['Axis'][2]):
			loadedSpectrum['data'][:,:,x_index,y_index]=data[frameIndex].T
			frameIndex+=1




	return loadedSpectrum

