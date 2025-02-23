try:	import numpy as np
except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")

try:	import pandas as pd
except ImportError: print("\t(Warning): Couldn't import the pandas module. This is required for loading sp2 files from Prodigy. Install it with the command 'pip install pandas'")

def load(fileName,**kwargs):

	beQuiet=kwargs.get('beQuiet')
	regionIndex=kwargs.get('regionIndex')
	testMode=False

	if testMode==True:
		print("TestMode")
		loadedSpectrum={}
		loadedSpectrum['Metadata']={}
		loadedSpectrum['Metadata']['CurrentFilePath']=fileName
		loadedSpectrum['Axis']=[[],[]]
		loadedSpectrum['AxisLabel']=["",""]
		loadedSpectrum['AxisUnits']=["",""]

		dataStarted = False

		imageIndex=0
		fp=pd.read_csv(fileName)
		for i, line in enumerate(fp):
			if dataStarted==False:
				if line.startswith("# lensmode"): loadedSpectrum['Metadata']['Lens Mode']=line.replace("# lensmode           = \"","").rstrip('"\n')
				
				if line.startswith("# Ep"): loadedSpectrum['Metadata']['Pass Energy']=float(line.replace("# Ep                 = ","").replace("# [eV]\n",""))

				if line.startswith("# Creation Date"): 
					values = line.replace("# Creation Date = \"","").split(" ")
					loadedSpectrum['Metadata']['Date']=values[0]
					loadedSpectrum['Metadata']['Time']=values[1]

				if line.startswith("# Images"):

					values = line.replace("\"","").split("= ")[1].rstrip("\n")
					numImages = len(values.split(" "))
					if beQuiet==False and numImages>1: 
						print("There are {} images in this sp2 file, will return image {}".format(numImages,regionIndex))

				if line.startswith("# ERange"):
					values=line.replace("# ERange             = ","").split(" ")
					energyStart = float(values[0])
					energyEnd = float(values[1])

				if line.startswith("# aRange"):
					values=line.replace("# aRange             = ","").split(" ")
					angleStart = float(values[0])
					angleEnd = float(values[1])          

				if line.startswith("# SIZE_X"): 
					numEnergySteps=int(line.split("=")[-1].split()[0])

				if line.startswith("# SIZE_Y"): 
					numAngleSteps=int(line.split("=")[-1].split()[0])
			

				if line.startswith("#") == False and i>0:
					#print(i)
					dataStarted = True
					numEnergySteps=int(line.split(" ")[0])
					numAngleSteps=int(line.split(" ")[1])
					numPixels=int(line.split(" ")[2])
					#print(numImages,numAngleSteps,numEnergySteps,numAngleSteps*numEnergySteps)
					loadedImages=np.zeros((numImages,numAngleSteps*numEnergySteps))
					linesToSkip=1
					imageIndex=0
					pixelIndex=0

			elif dataStarted==True:
				if line.startswith("P2"):
					imageIndex+=1
					pixelIndex=0
					linesToSkip=1
				elif linesToSkip>0:
					linesToSkip-=1
				else:
					loadedImages[imageIndex][pixelIndex]=float(line)
					pixelIndex+=1

		loadedSpectrum['data']=loadedImages[regionIndex-1].reshape((numAngleSteps,numEnergySteps,)).T
		loadedSpectrum['Axis'][1]=np.linspace(angleStart,angleEnd,numAngleSteps)
		loadedSpectrum['AxisLabel'][1]="Angle"  
		loadedSpectrum['AxisUnits'][1]=r"$\degree$" 
		loadedSpectrum['Axis'][0]=np.linspace(energyStart,energyEnd,numEnergySteps)
		loadedSpectrum['AxisLabel'][0]="Kinetic energy"
		loadedSpectrum['AxisUnits'][0]="eV" 

		loadedSpectrum['Metadata']['Acquisition Mode'] = 'Fixed'
		loadedSpectrum['Metadata']['File Path']=fileName
		return loadedSpectrum
	else:
		loadedSpectrum={}
		loadedSpectrum['Metadata']={}
		loadedSpectrum['Metadata']['CurrentFilePath']=fileName
		loadedSpectrum['Axis']=[[],[]]
		loadedSpectrum['AxisLabel']=["",""]
		loadedSpectrum['AxisUnits']=["",""]

		dataStarted = False

		imageIndex=0
		with open(fileName) as fp:
			for i, line in enumerate(fp):
				if dataStarted==False:
					if line.startswith("# lensmode"): loadedSpectrum['Metadata']['Lens Mode']=line.replace("# lensmode           = \"","").rstrip('"\n')
					
					if line.startswith("# Ep"): loadedSpectrum['Metadata']['Pass Energy']=float(line.replace("# Ep                 = ","").replace("# [eV]\n",""))

					if line.startswith("# Creation Date"): 
						values = line.replace("# Creation Date = \"","").split(" ")
						loadedSpectrum['Metadata']['Date']=values[0]
						loadedSpectrum['Metadata']['Time']=values[1]

					if line.startswith("# Images"):

						values = line.replace("\"","").split("= ")[1].rstrip("\n")
						numImages = len(values.split(" "))
						if beQuiet==False and numImages>1: 
							print("There are {} images in this sp2 file, will return image {}".format(numImages,regionIndex))

					if line.startswith("# ERange"):
						values=line.replace("# ERange             = ","").split(" ")
						energyStart = float(values[0])
						energyEnd = float(values[1])

					if line.startswith("# aRange"):
						values=line.replace("# aRange             = ","").split(" ")
						angleStart = float(values[0])
						angleEnd = float(values[1])          

					if line.startswith("# SIZE_X"): 
						numEnergySteps=int(line.split("=")[-1].split()[0])

					if line.startswith("# SIZE_Y"): 
						numAngleSteps=int(line.split("=")[-1].split()[0])
				

					if line.startswith("#") == False and i>0:
						#print(i)
						dataStarted = True
						numEnergySteps=int(line.split(" ")[0])
						numAngleSteps=int(line.split(" ")[1])
						numPixels=int(line.split(" ")[2])
						#print(numImages,numAngleSteps,numEnergySteps,numAngleSteps*numEnergySteps)
						loadedImages=np.zeros((numImages,numAngleSteps*numEnergySteps))
						linesToSkip=1
						imageIndex=0
						pixelIndex=0

				elif dataStarted==True:
					if line.startswith("P2"):
						imageIndex+=1
						pixelIndex=0
						linesToSkip=1
					elif linesToSkip>0:
						linesToSkip-=1
					else:
						loadedImages[imageIndex][pixelIndex]=float(line)
						pixelIndex+=1

		loadedSpectrum['data']=loadedImages[regionIndex-1].reshape((numAngleSteps,numEnergySteps,)).T
		loadedSpectrum['Axis'][1]=np.linspace(angleStart,angleEnd,numAngleSteps)
		loadedSpectrum['AxisLabel'][1]="Angle"  
		loadedSpectrum['AxisUnits'][1]=r"$\degree$" 
		loadedSpectrum['Axis'][0]=np.linspace(energyStart,energyEnd,numEnergySteps)
		loadedSpectrum['AxisLabel'][0]="Kinetic energy"
		loadedSpectrum['AxisUnits'][0]="eV" 

		loadedSpectrum['Metadata']['Acquisition Mode'] = 'Fixed'
		loadedSpectrum['Metadata']['File Path']=fileName
		return loadedSpectrum