try:	import numpy as np
except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")


def load(fileName,**kwargs):

	beQuiet=kwargs.get('beQuiet')
	loadedSpectrum={}
	loadedSpectrum['Metadata']={}
	loadedSpectrum['Metadata']['CurrentFilePath']=fileName

	file=open(fileName).readlines()

	label,units,axisStart,axisEnd=[],[],[],[]
	for i, line in enumerate(file):
		if 'WAVES/S/N' in line: 
			dimensions=[int(ii) for ii in line.split("=")[1].split(" ")[0][1:-1].split(",")]  #Example: WAVES/S/N=(500,500) '1_Spectrum'
		if '//Created Date' in line: 
			loadedSpectrum['Metadata']['Date']=line.split(": ")[1].split(" ")[0]
			loadedSpectrum['Metadata']['Time']=line.split(": ")[1].split(" ")[1].strip("\n")
			#print(line)

		if '//Scan Mode' in line: 			loadedSpectrum['Metadata']['Scan Mode']=line.split("=")[1].rstrip("\n")
		if '//User Comment' in line: 		loadedSpectrum['Metadata']['Comments']=line.split("=")[1].rstrip("\n")
		if '//Analysis Mode' in line: 		loadedSpectrum['Metadata']['Analysis Mode']=line.split("=")[1].rstrip("\n")
		if '//Lens Mode' in line: 			loadedSpectrum['Metadata']['Lens Mode']=line.split("= ")[1].rstrip("\n")
		if '//Lens Voltage' in line: 		loadedSpectrum['Metadata']['Lens Voltage']=line.split("= ")[1].rstrip("\n")
		if '//Analyzer Slits' in line: 		loadedSpectrum['Metadata']['Analyzer Slits']=line.split("= ")[1].rstrip("\n")
		if '//Number of Scans' in line: 	loadedSpectrum['Metadata']['Number of Sweeps']=int(line.split("=")[1].rstrip("\n"))
		if '//Spectrum ID' in line: 		loadedSpectrum['Metadata']['Spectrum ID']=int(line.split("=")[1].rstrip("\n"))
		if '//Pass Energy' in line: 		loadedSpectrum['Metadata']['Pass Energy']=float(line.split("=")[1].rstrip("\n"))
		if '//WorkFunction' in line: 		loadedSpectrum['Metadata']['WorkFunction']=float(line.split("=")[1].rstrip("\n"))

		if 'BEGIN\n' in line:	headerLength = i

		if any(x in line for x in ['SetScale/I x','SetScale/I y','SetScale/I z']):

			#
			info = line.split(", ")

			if '[' in line:
				label.append(info[3].split("[")[1].lstrip(" [").rstrip("]\""))
				units.append(info[3].split("[")[0].rstrip(" [").lstrip("\""))
			else:
				label.append(info[3].split("(")[1].lstrip(" (").rstrip(")\""))
				units.append(info[3].split("(")[0].rstrip(" (").lstrip("\""))
			axisStart.append(float(info[1]))
			axisEnd.append(float(info[2]))


	if len(dimensions)==2:
		loadedSpectrum['Axis']=[[],[]]
		loadedSpectrum['AxisLabel']=["",""]
		loadedSpectrum['AxisUnits']=["",""]

		loadedSpectrum['data']=np.zeros((dimensions[0],dimensions[1]),np.float32)

		for ii in range(dimensions[0]):
			loadedSpectrum['data'][ii,:]=[float(ii) for ii in file[headerLength+1 + (ii)].rstrip("\n").split(" ")]

	if len(dimensions)==3:
		loadedSpectrum['Axis']=[[],[],[]]
		loadedSpectrum['AxisLabel']=["","",""]
		loadedSpectrum['AxisUnits']=["","",""]

		loadedSpectrum['data']=np.zeros((dimensions[0],dimensions[1],dimensions[2]),np.float32)
		
		for frameIndex in range(dimensions[2]):
			for energyIndex in range(dimensions[1]):
				loadedSpectrum['data'][:,energyIndex,frameIndex]=np.fromstring(file[headerLength+1 +(frameIndex)*(dimensions[0]+1) + energyIndex],dtype=float,sep=' ')
		loadedSpectrum['data']=loadedSpectrum['data'].transpose(1,0,2)

	for axisIndex in range(len(dimensions)):

		if label[axisIndex]=='Non-Energy Channel': 
			label[axisIndex]="Analyzer angle"
		if label[axisIndex]=='SAL X': label[axisIndex]="Deflector angle"
		loadedSpectrum['AxisLabel'][axisIndex]=label[axisIndex]
		loadedSpectrum['AxisUnits'][axisIndex]=units[axisIndex]
		loadedSpectrum['Axis'][axisIndex]=np.linspace(axisStart[axisIndex],axisEnd[axisIndex],num=dimensions[axisIndex],endpoint=True)

	if len(dimensions)==2:
		return transposeSpectrum(loadedSpectrum,[1,0])

	if len(dimensions)==3:
		return transposeSpectrum(loadedSpectrum,[1,0,2])

def transposeSpectrum(spectrum,a):
	assert(len(spectrum['Axis'])==len(a)), "The 'a' input doesn't match the axes of the input spectrum"

	spectrum['data']=spectrum['data'].transpose(a)
	spectrum['Axis']=[spectrum['Axis'][ii] for ii in a]
	spectrum['AxisLabel']=[spectrum['AxisLabel'][ii] for ii in a]
	spectrum['AxisUnits']=[spectrum['AxisUnits'][ii] for ii in a]
	return spectrum