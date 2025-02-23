try:	import numpy as np
except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")

import linecache

def load(fileName,**kwargs):

	beQuiet=kwargs.get('beQuiet')
	regionIndex=kwargs.get('regionIndex')
	whichManipulatorAxis=kwargs.get('whichManipulatorAxis')

	def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 80, fill = '█'):
		"""
		Call in a loop to create terminal progress bar
		Courtesy of S.O. user Greenstick, https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
		"""
		percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
		filledLength = int(length * iteration // total)
		bar = fill * filledLength + '-' * (length - filledLength)
		print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
		# Print New Line on Complete
		if iteration == total: 
			print()
		
	def listRegions(fileName): #Evaluate how many regions are in the file, and where the requested region starts in the file
		regionCounter=0
		if fileName.endswith(".txt"):
			with open(fileName) as fp:
				validRegions = []
				for i, line in enumerate(fp):
					if line.startswith("[Region "): 
						regionCounter+=1
						validRegions.append([regionCounter,i])      
		return validRegions 
		
	def get_txt_manipulatorscan_axis(fileName,whichManipulatorAxis='',fixRounding=True,regionIndex=1,beQuiet=False):

		def deleteFromLeft(string,substring):
			if string.startswith(substring):
				string=string[len(substring):]  
			return string

		assert fileName.endswith(".txt"), "Only SES .txt files are supported"

		validRegions = listRegions(fileName)

		with open(fileName) as f:

			energyAxis=[]
			analyzerAxis=[]
			manipulatorAxisNames=[]
			manipulatorAxes=[]

			manipulatorInfoStartLine=np.NaN
			eK_axis_line=np.NaN
			manipulatorAxisLength=0
			for index,line in enumerate(f):
				if index>validRegions[regionIndex-1][1]:
					if line.startswith('Dimension 1 scale='):
						line=deleteFromLeft(line,'Dimension 1 scale=')          
						energyAxis = np.fromstring(line.rstrip('\n'), sep='  ').tolist()

					if line.startswith('Dimension 2 scale='):
						line=deleteFromLeft(line,'Dimension 2 scale=')
						analyzerAxis=np.fromstring(line.rstrip('\n'), sep='  ').tolist()
					
					if line.startswith('Dimension 3 size='):
						line=deleteFromLeft(line,'Dimension 3 size=')
						manipulatorAxisLength=int(line.rstrip('\n'))

					if line.startswith("[Run Mode Information 1]"):
						manipulatorInfoStartLine=index+1

					if index==manipulatorInfoStartLine: 
						for axisName in line.split('\x0b')[1:]:
							manipulatorAxisNames.append(axisName.rstrip('\n'))
							manipulatorAxes.append([])
						
						if beQuiet==False: print("I found the following axis names in the metadata:",[ii for ii in manipulatorAxisNames])
						
					if index>manipulatorInfoStartLine and index<=manipulatorInfoStartLine+manipulatorAxisLength:
						data = line.split('\x0b')[1:]
						for index,axisName in enumerate(manipulatorAxisNames):
							manipulatorAxes[index].append(float(data[index]))
							
					if index==manipulatorInfoStartLine+manipulatorAxisLength+1:
						manipulatorScannedAxisNames=[]
						numberOfScannedAxes=0               
						for index,axisName in enumerate(manipulatorAxisNames):
							if manipulatorAxes[index][-1]!=manipulatorAxes[index][0]:
								numberOfScannedAxes+=1
								manipulatorScannedAxisNames.append(axisName)
								stepSize = abs(manipulatorAxes[index][-1]-manipulatorAxes[index][0])/(manipulatorAxisLength-1)
								if beQuiet==False: print("Axis \'{}\' was scanned from {} to {} in steps of {:.5f}".format(axisName,manipulatorAxes[index][0],manipulatorAxes[index][-1],stepSize))
						
						if numberOfScannedAxes==1:
							#print("\nInferring that the primary manipulator scan axis must be:",[ii for ii in manipulatorScannedAxisNames])
							primaryAxisIndex = manipulatorAxisNames.index(manipulatorScannedAxisNames[0])         
							primaryManipulatorAxis = manipulatorAxes[primaryAxisIndex]
							primaryManipulatorAxisName = manipulatorAxisNames[primaryAxisIndex]
						
						else:
							if(whichManipulatorAxis==''):
								if beQuiet==False: print("\n-------- !! WARNING !! ---------")
								if beQuiet==False: print("I don't know which of these is the primary manipulator scan axis, and you didn't specify.")
								if beQuiet==False: print("I will therefore assume that the primary axis is ",manipulatorScannedAxisNames[0])
								if beQuiet==False: print("To choose a different primary axis, please call this function again, passing the additional argument whichManipulatorAxis=n, where n is one of:",[ii for ii in manipulatorScannedAxisNames])
								if beQuiet==False: print("---------------------------------")
								primaryAxisIndex = manipulatorAxisNames.index(manipulatorScannedAxisNames[0])         
								primaryManipulatorAxis = manipulatorAxes[primaryAxisIndex]
								primaryManipulatorAxisName = manipulatorAxisNames[primaryAxisIndex]
							
							elif whichManipulatorAxis in manipulatorScannedAxisNames:
								if beQuiet==False: print("Treating {} as the primary scan axis".format(whichManipulatorAxis))
								primaryAxisIndex = manipulatorAxisNames.index(whichManipulatorAxis)         
								primaryManipulatorAxis = manipulatorAxes[primaryAxisIndex]
								primaryManipulatorAxisName = manipulatorAxisNames[primaryAxisIndex]
								
							else:
								if beQuiet==False: print("\n-------- !! WARNING !! ---------")
								if beQuiet==False: print("The name of the primary manipulator scan axis that you provided ({}) is not the name of a scanned axis ({}).".format(whichManipulatorAxis,manipulatorScannedAxisNames))
								if beQuiet==False: print("I will therefore assume that the primary axis is ",manipulatorScannedAxisNames[0])
								if beQuiet==False: print("To choose a different primary axis, please call this function again, passing the additional argument whichManipulatorAxis=n, where n is one of:",[ii for ii in manipulatorScannedAxisNames])
								if beQuiet==False: print("---------------------------------")
								primaryAxisIndex = manipulatorAxisNames.index(manipulatorScannedAxisNames[0])         
								primaryManipulatorAxis = manipulatorAxes[primaryAxisIndex]
								primaryManipulatorAxisName = manipulatorAxisNames[primaryAxisIndex]
								
						if fixRounding==True:
							if beQuiet==False: print("I recalculated the axis values, since SES rounds in the file header to 3 decimal places")
							axisStepSize = (manipulatorAxes[primaryAxisIndex][-1]-manipulatorAxes[primaryAxisIndex][0])/(manipulatorAxisLength-1)
							axisStart = manipulatorAxes[primaryAxisIndex][0] 
							primaryManipulatorAxis = [axisStart + ii*axisStepSize for ii in range(manipulatorAxisLength)] 

						if primaryManipulatorAxisName == 'P':
							primaryManipulatorAxisName = "Polar angle"
							axisUnits = "$\degree$"
						return energyAxis,analyzerAxis,primaryManipulatorAxis,primaryManipulatorAxisName,axisUnits

		assert(False),"Error getting axis information from file" 


	# Evaluate how many regions are in the file, and where the requested region starts in the file
	# Avoid enumerating through the entire file if possible, it'll take a while for 3d datasets	
	loadedSpectrum={}
	loadedSpectrum['Metadata']={}
	loadedSpectrum['Metadata']['CurrentFilePath']=fileName
	loadedSpectrum['Axis']=[[],[]]
	loadedSpectrum['AxisLabel']=["",""]
	loadedSpectrum['AxisUnits']=["",""]

	validRegions = listRegions(fileName)
	validRegionNumbers = [ii[0] for ii in validRegions]
	assert(regionIndex in validRegionNumbers), "Invalid Region requested: valid regions are {}".format(validRegionNumbers)
	if beQuiet==False:print("Loading region #{} of {}".format(regionIndex,len(validRegions)))

	# Check for the presence of a third data dimension in the selected region
	# Unfortunately this is necessary because SES doesn't write a 'run-mode' entry for manipulator scans.
	# We do this by assuming that the Dimension 3 scale information always comes at a fixed offset from the Region start line.
	# If you go to that line and find it blank, it's because SES didn't write anything about a third dimension.
	
	testLine = linecache.getline(fileName, validRegions[regionIndex-1][1]+9)
	if testLine.startswith("Dimension 3"):
		loadedSpectrum['Axis'].append([])
		loadedSpectrum['AxisLabel'].append("")
		loadedSpectrum['AxisUnits'].append("")

		numImages = int(linecache.getline(fileName, validRegions[regionIndex-1][1]+10).split("=")[1])
		numAngleSteps = int(linecache.getline(fileName, validRegions[regionIndex-1][1]+7).split("=")[1])
		numEnergySteps = int(linecache.getline(fileName, validRegions[regionIndex-1][1]+4).split("=")[1])
		loadedSpectrum['data']=np.zeros((numEnergySteps,numAngleSteps,numImages),np.float32)
		


		if testLine.split("=")[1].startswith("Photon"):
			fileType = 'ARPES photon energy scan'
			if beQuiet==False: 
				print("Inferring from the presence and name of dimension 3 that this is a photon energy scan")

		else:
			fileType = '1D Manipulator Scan'
			if beQuiet==False: 
				print("Inferring from the presence of an unnamed dimension 3 that this is a 1D manipulator scan")
			

			e,a,m,m_name,m_units = get_txt_manipulatorscan_axis(fileName=fileName,
				whichManipulatorAxis='',
				fixRounding=True,
				regionIndex=validRegions[regionIndex-1][0],
				beQuiet=False)
			loadedSpectrum['Axis'][2]=m
			loadedSpectrum['AxisLabel'][2]=m_name 
			loadedSpectrum['AxisUnits'][2]=m_units
			loadedSpectrum['data']=np.zeros((len(e),len(a),len(m)))




			
	else:
		if beQuiet==False: print("Inferring from data dimension that this is single 2D image")
		fileType='2D image'
		numAngleSteps = int(linecache.getline(fileName, validRegions[regionIndex-1][1]+7).split("=")[1])
		numEnergySteps = int(linecache.getline(fileName, validRegions[regionIndex-1][1]+4).split("=")[1])
		loadedSpectrum['data']=np.zeros((numEnergySteps,numAngleSteps),np.float32)


	regionStartLine = validRegions[regionIndex-1][1]
	dataStartLine = 9999999
	loadedSpectrum['Axis'][0]=[]
	frameNumber=0
	with open(fileName) as fp:
		for linenumber, line in enumerate(fp):
			if linenumber<regionStartLine:
				pass
			elif fileType=='2D image' and linenumber>(dataStartLine+len(loadedSpectrum['Axis'][0])): #data load finished
				break
			elif (fileType=='1D Manipulator Scan' or fileType=='ARPES photon energy scan') and frameNumber == numImages: #data load (Photon energy scan or 1D manipulator scan) finished
				break
			else:
				if line.startswith("Dimension 1 scale="): #Energy axis scale
					Axis=line.rstrip('\n').split("=")[1].split(" ")
					loadedSpectrum['Axis'][0]=[float(ii) for ii in Axis]
			
				if line.startswith("Dimension 1 name="):
					AxisLabel=line.rstrip('\n').split("=")[1]
					if AxisLabel.startswith("Binding"): 
						loadedSpectrum['AxisLabel'][0] = "Binding energy"
						loadedSpectrum['AxisUnits'][0] = "eV" 
					else: 
						loadedSpectrum['AxisLabel'][0]  = "Kinetic energy"
						loadedSpectrum['AxisUnits'][0] = "eV" 

				if line.startswith("Dimension 2 scale="): #Angle axis scale
					Axis=line.rstrip('\n').split("=")[1].split(" ")
					loadedSpectrum['Axis'][1]=[float(ii) for ii in Axis]
					loadedSpectrum['AxisLabel'][1] = "Angle" 
					loadedSpectrum['AxisUnits'][1] ="$\degree$" 
					if fileType=='2D image':
						loadedSpectrum['data']=np.zeros((len(loadedSpectrum['Axis'][0]),len(loadedSpectrum['Axis'][1])))


				if line.startswith("Dimension 3 scale=") and fileType=='ARPES photon energy scan': 
					zAxis=line.rstrip('\n').split("=")[1].split(" ")
					loadedSpectrum['Axis'][2]=[float(ii) for ii in zAxis]       	
					loadedSpectrum['AxisLabel'][2] = "Photon energy"  
					loadedSpectrum['AxisUnits'][2] = "eV"
					loadedSpectrum['data']=np.zeros((len(loadedSpectrum['Axis'][0]),len(loadedSpectrum['Axis'][1]),len(loadedSpectrum['zAxis'][2])))

				if line.startswith("Region Name="): loadedSpectrum['Metadata']['Region Name']=line.replace("Region Name=","").rstrip('\n')
				if line.startswith("Lens Mode="): loadedSpectrum['Metadata']['Lens Mode']=line.replace("Lens Mode=","").rstrip('\n')
				if line.startswith("Pass Energy="): loadedSpectrum['Metadata']['Pass Energy']=int(line.replace("Pass Energy=","").rstrip('\n'))
				if line.startswith("Number of Sweeps="): loadedSpectrum['Metadata']['Number of Sweeps']=int(line.replace("Number of Sweeps=","").rstrip('\n'))
				if line.startswith("Excitation Energy="): loadedSpectrum['Metadata']['Excitation Energy']=float(line.replace("Excitation Energy=","").rstrip('\n').replace(",","."))
				if line.startswith("Energy Scale="): loadedSpectrum['Metadata']['Energy Scale']=line.replace("Energy Scale=","").rstrip('\n')
				if line.startswith("Acquisition Mode="): loadedSpectrum['Metadata']['Acquisition Mode']=line.replace("Acquisition Mode=","").rstrip('\n')
				if line.startswith("Energy Unit="): loadedSpectrum['Metadata']['Energy Unit']=line.replace("Energy Unit=","").rstrip('\n')
				if line.startswith("Center Energy="): loadedSpectrum['Metadata']['Center Energy']=float(line.replace("Center Energy=","").rstrip('\n').replace(",","."))
				if line.startswith("Low Energy="): loadedSpectrum['Metadata']['Low Energy']=float(line.replace("Low Energy=","").rstrip('\n').replace(",","."))
				if line.startswith("High Energy="): loadedSpectrum['Metadata']['High Energy']=float(line.replace("High Energy=","").rstrip('\n').replace(",","."))
				if line.startswith("Energy Step="): loadedSpectrum['Metadata']['Energy Step']=float(line.replace("Energy Step=","").rstrip('\n').replace(",","."))
				if line.startswith("Step Time="): loadedSpectrum['Metadata']['Step Time']=float(line.replace("Step Time=","").rstrip('\n').replace(",","."))
				if line.startswith("Detector First X-Channel="): loadedSpectrum['Metadata']['Detector First X-Channel']=int(line.replace("Detector First X-Channel=","").rstrip('\n'))
				if line.startswith("Detector Last X-Channel="): loadedSpectrum['Metadata']['Detector Last X-Channel']=int(line.replace("Detector Last X-Channel=","").rstrip('\n'))
				if line.startswith("Detector First Y-Channel="): loadedSpectrum['Metadata']['Detector First Y-Channel']=int(line.replace("Detector First Y-Channel=","").rstrip('\n'))
				if line.startswith("Detector Last Y-Channel="): loadedSpectrum['Metadata']['Detector Last Y-Channel']=int(line.replace("Detector Last Y-Channel=","").rstrip('\n'))
				if line.startswith("Number of Slices="): loadedSpectrum['Metadata']['Number of Slices']=int(line.replace("Number of Slices=","").rstrip('\n'))
				if line.startswith("File="):
					path = line.replace("File=","").rstrip('\n').replace("\\\\","\\")
					loadedSpectrum['Metadata']['File Path']= path[:path.rindex('\\')+1] + fileName                        
				if line.startswith("Sequence="): loadedSpectrum['Metadata']['Sequence']=line.replace("Sequence=","").rstrip('\n').replace("\\\\","\\")
				if line.startswith("Spectrum Name="): loadedSpectrum['Metadata']['Spectrum Name']=line.replace("Spectrum Name=","").rstrip('\n')
				if line.startswith("Instrument="): loadedSpectrum['Metadata']['Instrument']=line.replace("Instrument=","").rstrip('\n')
				if line.startswith("Location="): loadedSpectrum['Metadata']['Location']=line.replace("Location=","").rstrip('\n')
				if line.startswith("User="): loadedSpectrum['Metadata']['User']=line.replace("User=","").rstrip('\n')
				if line.startswith("Sample="): loadedSpectrum['Metadata']['Sample']=line.replace("Sample=","").rstrip('\n')
				if line.startswith("Comments="): loadedSpectrum['Metadata']['Comments']=line.replace("Comments=","").rstrip('\n')
				if line.startswith("Date="): loadedSpectrum['Metadata']['Date']=line.replace("Date=","").rstrip('\n')
				if line.startswith("Time="): loadedSpectrum['Metadata']['Time']=line.replace("Time=","").rstrip('\n')
				if line.startswith("Time per Spectrum Channel="): loadedSpectrum['Metadata']['Time per Spectrum Channel']=float(line.replace("Time per Spectrum Channel=","").rstrip('\n').replace(",","."))
				if line.startswith("DetectorMode="): loadedSpectrum['Metadata']['DetectorMode']=line.replace("DetectorMode=","").rstrip('\n')

				if fileType!='1D Manipulator Scan':
						if line.startswith("A="): loadedSpectrum['Metadata']['Manipulator Azimuth']=float(line.replace("A=","").rstrip('\n').replace(",","."))
						if line.startswith("P="): loadedSpectrum['Metadata']['Manipulator Polar']=float(line.replace("P=","").rstrip('\n').replace(",","."))
						if line.startswith("T="): loadedSpectrum['Metadata']['Manipulator Tilt']=float(line.replace("T=","").rstrip('\n').replace(",","."))
						if line.startswith("X="): loadedSpectrum['Metadata']['Manipulator X']=float(line.replace("X=","").rstrip('\n').replace(",","."))
						if line.startswith("Y="): loadedSpectrum['Metadata']['Manipulator Y']=float(line.replace("Y=","").rstrip('\n').replace(",","."))
						if line.startswith("Z="): loadedSpectrum['Metadata']['Manipulator Z']=float(line.replace("Z=","").rstrip('\n').replace(",","."))
				
				
				if (fileType=='ARPES photon energy scan' or fileType=='1D Manipulator Scan') and line.startswith("[Data {}:".format(regionIndex)):
					loadedImage = np.genfromtxt(fp,delimiter='  ',skip_header=0,max_rows=len(loadedSpectrum['Axis'][0]))
					loadedSpectrum['data'][:,:,frameNumber]=loadedImage[:,1:]
					frameNumber+=1
					if beQuiet==False: printProgressBar(frameNumber, len(loadedSpectrum['Axis'][2]), prefix = 'Progress:', suffix = 'Complete', length = 50)			 
					
				if fileType=='2D image' and line.startswith("[Data {}]".format(regionIndex)):
					dataStartLine=linenumber+1

				if fileType=='2D image':		
					if linenumber>=dataStartLine and linenumber<(dataStartLine+len(loadedSpectrum['Axis'][0])):

						cps=line.rstrip('\n').split("  ")
						for index,element in enumerate(cps):
							if index==0: pass
							else:loadedSpectrum['data'][linenumber-dataStartLine][index-1]=float(element)


	return loadedSpectrum