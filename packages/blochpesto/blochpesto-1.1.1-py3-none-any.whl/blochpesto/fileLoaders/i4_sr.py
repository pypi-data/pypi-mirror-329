import blochpesto as pesto
import numpy as np

def load(fileName,**kwargs):

	beQuiet=kwargs.get('beQuiet')

	with open(fileName) as fp:
		for i, line in enumerate(fp):
			if i==0:
				colHeaders = line.rstrip("\n").split("\t")
				scanReport={}
				for ii in colHeaders:
					scanReport['{}'.format(ii)]=[]

			else:
				vals = line.rstrip("\n").split("\t")
				if(len(vals))>0:
					for ii,name in enumerate(colHeaders):
						scanReport[name].append(vals[ii]) 

	frames=[]
	path = fileName.rstrip("fsm.sr")
	for ii,fileName in enumerate(scanReport["File name"]):
		frames.append(pesto.loadSpectrum(path+fileName,beQuiet=True))
		pesto.printProgressBar(ii,len(scanReport["File name"]))


	scan = pesto.loadSpectrum(path+scanReport["File name"][0],beQuiet=True)

	loadedSpectrum={}
	loadedSpectrum['Metadata']={}
	loadedSpectrum['Axis']=[[],[],[]]
	loadedSpectrum['AxisLabel']=["","",""]
	loadedSpectrum['AxisUnits']=["","",""]


	loadedSpectrum['Axis'][0]=scan['Axis'][0]
	loadedSpectrum['Axis'][1]=scan['Axis'][1]
	loadedSpectrum['Axis'][2]=np.array([float(ii) for ii in scanReport['Theta']])

	loadedSpectrum['AxisLabel'][0]=scan['AxisLabel'][0]
	loadedSpectrum['AxisLabel'][1]=scan['AxisLabel'][1]
	loadedSpectrum['AxisLabel'][2]="Polar angle"

	loadedSpectrum['AxisUnits'][0]=scan['AxisUnits'][0]
	loadedSpectrum['AxisUnits'][1]=scan['AxisUnits'][1]
	loadedSpectrum['AxisUnits'][2]="$\degree$"

	loadedSpectrum['data']=scan['data']

	loadedSpectrum['data'] = np.stack([ii['data'] for ii in frames])
	loadedSpectrum['data']=loadedSpectrum['data'].transpose(1,2,0)
	
	return loadedSpectrum