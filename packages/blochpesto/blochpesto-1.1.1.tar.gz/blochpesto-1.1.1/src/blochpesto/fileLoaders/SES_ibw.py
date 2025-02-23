try:	from igor2 import binarywave
except ImportError:
	try:	
		from igor import binarywave
		print("\t(Warning): Couldn't import the igor2 module, but was able to fall back to the earlier igor module. Upgrade with the command 'pip install igor2'")
	except ImportError:
		print("\t(Warning): Couldn't import the igor2 module. You will not be able to work with .ibw files.  Install it from the terminal with the command 'pip install igor2'")


try:	import numpy as np
except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")


def load(fileName,**kwargs):

	beQuiet=kwargs.get('beQuiet')
	regionIndex=kwargs.get('regionIndex')
	whichManipulatorAxis=kwargs.get('whichManipulatorAxis')
	majorAxis=kwargs.get('majorAxis')
	minorAxis=kwargs.get('minorAxis')
	loadedSpectrum={}
	loadedSpectrum['Metadata']={}
	loadedSpectrum['Metadata']['CurrentFilePath']=fileName


	t=binarywave.load(fileName)

	""" Figure out what kind of measurement file this is. Unfortunately SES is not consistent 
	about using the 'RunMode' metadata entry, so we have to make some inferences based on data dimensions.

	t['wave']['wave_header']['nDim'] is always 4 elements long, but unused dimensions will be set to zero.
	So the dimensionality of the dataset is the number of non-zero elements in ['nDim']
	"""

	if t['wave']['wave_header']['nDim'][1]==0 and t['wave']['wave_header']['nDim'][2]==0 and t['wave']['wave_header']['nDim'][3]==0: #Only 1 of 4 dimensions used
		if beQuiet==False: print("1D dataset")
		numDataDimensions=1
		loadedSpectrum['Axis']=[]
		loadedSpectrum['AxisLabel']=""
		loadedSpectrum['AxisUnits']=""
		fileType='1D trace'

	elif t['wave']['wave_header']['nDim'][2]==0 and t['wave']['wave_header']['nDim'][3]==0: #Only 2 of 4 dimensions used
		if beQuiet==False: print("2D dataset, must be an image")
		numDataDimensions=2
		loadedSpectrum['Axis']=[[],[]]
		loadedSpectrum['AxisLabel']=["",""]
		loadedSpectrum['AxisUnits']=["",""]
		fileType='2D image'
		
	elif t['wave']['wave_header']['nDim'][3]==0: #Only 3 of 4 dimensions unused
		if beQuiet==False: print("3D dataset, I think it's...")
		numDataDimensions=3

		loadedSpectrum['Axis']=[[],[],[]]
		loadedSpectrum['AxisLabel']=["","",""]
		loadedSpectrum['AxisUnits']=["","",""]


		RunMode = str(t['wave']['note']).replace("\\r","\n").split('[Run Mode Information]')[1].splitlines()[1].replace("Name=","")
		LensMode = str(t['wave']['note']).replace("\\r","\n").split('Lens Mode=')[1].splitlines()[0]
		if RunMode == 'CIS':
			if LensMode == 'Transmission': fileType = 'XPS photon energy scan'
			else: fileType = 'ARPES photon energy scan'	

		else:
			fileType = '1D Manipulator Scan'

			numImages = t['wave']['wave_header']['nDim'][2]
			manipulatorInfoStartLine=99999
			loadedSpectrum['Metadata']['Manipulator Axis Names']=[]
			loadedSpectrum['Metadata']['Manipulator Axis Units']=[]
			loadedSpectrum['Metadata']['Manipulator Axes']=[]

		if beQuiet==False: print(fileType)

	else: #All four dimensions used
		if beQuiet==False: print("4D dataset, must be a 2D manipulator scan")
		if beQuiet==False: print("Detector image size is {} energy pixels and {} angle pixels".format(t['wave']['wave_header']['nDim'][0],t['wave']['wave_header']['nDim'][1]))
		numDataDimensions=4
		loadedSpectrum['Axis']=[[],[],[],[]]
		loadedSpectrum['AxisLabel']=["","","",""]
		loadedSpectrum['AxisUnits']=["","","",""]

		fileType='2D Manipulator Scan'
		numImages = t['wave']['wave_header']['nDim'][2]*t['wave']['wave_header']['nDim'][3]

		manipulatorInfoStartLine=99999
		loadedSpectrum['Metadata']['Manipulator Axis Names']=[]
		loadedSpectrum['Metadata']['Manipulator Axis Units']=[]
		loadedSpectrum['Metadata']['Manipulator Axes']=[]



	""" Every scan type has the two dimensions corresponding to the detector image.
	Retrieve this information now"""

	energyStart=t['wave']['wave_header']['sfB'][0]
	energyStart=float(np.format_float_positional(energyStart, precision=5))
	energyStep=t['wave']['wave_header']['sfA'][0]
	energyStep=float(np.format_float_positional(energyStep, precision=5))
	numEnergySteps=t['wave']['wave_header']['nDim'][0]
	energyEnd=energyStart+(energyStep*(numEnergySteps-1))

	if numDataDimensions>1:
		angleStart=t['wave']['wave_header']['sfB'][1]
		angleStep=t['wave']['wave_header']['sfA'][1]
		numAngleSteps=t['wave']['wave_header']['nDim'][1]
		angleEnd=angleStart+(angleStep*(numAngleSteps-1))

		loadedSpectrum['Axis'][1]=np.linspace(angleStart,angleEnd,numAngleSteps)
		loadedSpectrum['AxisLabel'][1]="Angle"  
		loadedSpectrum['AxisUnits'][1]=r"$\degree$" 

		loadedSpectrum['Axis'][0]=np.linspace(energyStart,energyEnd,numEnergySteps)

		if str(t['wave']['dimension_units']).startswith("b'Binding"):
			loadedSpectrum['AxisLabel'][0]="Binding energy"
			loadedSpectrum['AxisUnits'][0]="eV" 
		else: 
			loadedSpectrum['AxisLabel'][0]="Kinetic energy"
			loadedSpectrum['AxisUnits'][0]="eV" 
	else:
		loadedSpectrum['Axis']=np.linspace(energyStart,energyEnd,numEnergySteps)

		if str(t['wave']['dimension_units']).startswith("b'Binding"):
			loadedSpectrum['AxisLabel']="Binding energy"
			loadedSpectrum['AxisUnits']="eV" 
		else: 
			loadedSpectrum['AxisLabel']="Kinetic energy"
			loadedSpectrum['AxisUnits']="eV" 		

	""" Get the n-dimensional dataset:"""
	# Note: Our convention here is:
	# Dimension 0: energy
	# Dimension 1: analyzer angle
	# Dimension 2: polar angle / hv / deflector angle
	# Getting it like this requires(?) some transposition:

	if len(np.shape(t['wave']['wData']))<=2:
		loadedSpectrum['data']=t['wave']['wData']#.transpose(1,0)
	elif len(np.shape(t['wave']['wData']))==3:
		loadedSpectrum['data']=t['wave']['wData'].transpose(0,1,2)
	elif len(np.shape(t['wave']['wData']))==4:
		loadedSpectrum['data']=t['wave']['wData'].transpose(0,1,2,3)

	""" Parse and load the metadata:"""
	for linenumber,line in enumerate((str(t['wave']['note']).replace("\\r","\n")).splitlines()):
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
		
		if fileType!='1D Manipulator Scan' and fileType!='2D Manipulator Scan': #Unless it's a manipulator scan, there is one constant set of manipulator values
			if line.startswith("A="): loadedSpectrum['Metadata']['Manipulator Azimuth']=float(line.replace("A=","").rstrip('\n').replace(",","."))
			if line.startswith("P="): loadedSpectrum['Metadata']['Manipulator Polar']=float(line.replace("P=","").rstrip('\n').replace(",","."))
			if line.startswith("T="): loadedSpectrum['Metadata']['Manipulator Tilt']=float(line.replace("T=","").rstrip('\n').replace(",","."))
			if line.startswith("X="): loadedSpectrum['Metadata']['Manipulator X']=float(line.replace("X=","").rstrip('\n').replace(",","."))
			if line.startswith("Y="): loadedSpectrum['Metadata']['Manipulator Y']=float(line.replace("Y=","").rstrip('\n').replace(",","."))
			if line.startswith("Z="): loadedSpectrum['Metadata']['Manipulator Z']=float(line.replace("Z=","").rstrip('\n').replace(",","."))

		if fileType == 'XPS photon energy scan' or fileType == 'ARPES photon energy scan':
			hvStart=t['wave']['wave_header']['sfB'][2]
			hvStep=t['wave']['wave_header']['sfA'][2]
			numhvSteps=t['wave']['wave_header']['nDim'][2]
			hvEnd=hvStart+(hvStep*(numhvSteps-1))
			loadedSpectrum['Axis'][2]=np.linspace(hvStart,hvEnd,numhvSteps)				
			loadedSpectrum['AxisLabel'][2]="Photon energy"
			loadedSpectrum['AxisUnits'][2]="eV"

		if fileType=='1D Manipulator Scan' or fileType=='2D Manipulator Scan':

			if line.startswith("[Run Mode Information]"): 
				manipulatorInfoStartLine=linenumber+1
				if fileType=='2D Manipulator Scan': manipulatorInfoStartLine+=1  # For some reason 2D maps include an extra 'Name=Manipulator Scan' element that 1D maps don't have. Offset by one to skip past it to the axis names.
			
			if linenumber==manipulatorInfoStartLine:
				for axisName in line.split('\\x0b'):
					axisNames={}
					axisNames['A']='Azimuth'
					axisNames['P']='Polar'
					axisNames['T']='Tilt'
					axisUnits={}
					axisUnits['A']=r'$\degree$'
					axisUnits['P']=r'$\degree$'
					axisUnits['T']=r'$\degree$'
					axisUnits['X']='mm'
					axisUnits['Y']='mm'
					axisUnits['Z']='mm'						
					try:
						loadedSpectrum['Metadata']['Manipulator Axis Names'].append(axisNames[axisName.rstrip('\n')])
					except KeyError:
						loadedSpectrum['Metadata']['Manipulator Axis Names'].append(axisName.rstrip('\n'))

					try:
						loadedSpectrum['Metadata']['Manipulator Axis Units'].append(axisUnits[axisName.rstrip('\n')])
					except KeyError:
						loadedSpectrum['Metadata']['Manipulator Axis Units'].append("")

					loadedSpectrum['Metadata']['Manipulator Axes'].append([])
				
				if beQuiet==False: print("I found the following axis names in the metadata:",[ii for ii in loadedSpectrum['Metadata']['Manipulator Axis Names']])


			if linenumber>manipulatorInfoStartLine and linenumber<=manipulatorInfoStartLine+numImages:
				data = line.split('\\x0b')
				#print(data)
				for index,axisName in enumerate(loadedSpectrum['Metadata']['Manipulator Axis Names']):

					loadedSpectrum['Metadata']['Manipulator Axes'][index].append(float(data[index]))

	if fileType=='2D Manipulator Scan':
		""" 
		The 'position' axis holds the value of the outer loop axis variable (major)
		The 'point' axis holds the value of the inner loop variable (minor)

		This lets us deduce the names of the scanned axes
		"""

		numAxes = len(loadedSpectrum['Metadata']['Manipulator Axis Names'])
		majorAxis = loadedSpectrum['Metadata']['Manipulator Axes'][0]
		minorAxis = loadedSpectrum['Metadata']['Manipulator Axes'][1]
		lenMajorAxis = t['wave']['wave_header']['nDim'][3]
		lenMinorAxis = t['wave']['wave_header']['nDim'][2]

		if loadedSpectrum['Metadata']['Manipulator Axis Names'][0] == 'Position [au]':
			print("(!!) Something was not right with your scan settings. Check that you assigned unique inner and outer loop variables.") 
		if loadedSpectrum['Metadata']['Manipulator Axis Names'][1] == 'Point [au]':
			print("(!!) Something was not right with your scan settings. Check that you assigned unique inner and outer loop variables.") 


		lenMajorAxis = t['wave']['wave_header']['nDim'][3]
		lenMinorAxis = t['wave']['wave_header']['nDim'][2]


		foundMajorAxis=False
		foundMinorAxis=False
		

		num_misses_Major=[]
		num_misses_Minor=[]

		# Scan through all manipulator axes in the metadata (except the first two, which are just position and point)
		for index,name in enumerate(loadedSpectrum['Metadata']['Manipulator Axis Names'][2:]):
			num_misses_Major.append(0)

			if foundMajorAxis==False:
				for ii,jj in zip(loadedSpectrum['Metadata']['Manipulator Axes'][index+2],majorAxis):
					if ii!=jj: num_misses_Major[-1]+=1
			if loadedSpectrum['Metadata']['Manipulator Axes'][index+2] == majorAxis:
				loadedSpectrum['majorAxisLabel']=name
				loadedSpectrum['majorAxis']=majorAxis[0::lenMinorAxis]
				foundMajorAxis=True


			num_misses_Minor.append(0)

			if foundMinorAxis==False:
				for ii,jj in zip(loadedSpectrum['Metadata']['Manipulator Axes'][index+2],minorAxis):
					if ii!=jj: num_misses_Minor[-1]+=1

			if loadedSpectrum['Metadata']['Manipulator Axes'][index+2] == minorAxis:
				loadedSpectrum['minorAxisLabel']=name
				loadedSpectrum['minorAxis']=minorAxis[0:lenMinorAxis]
				foundMinorAxis=True		

		
		if foundMajorAxis==False:
			print("(!!) WARNING: Something is a bit odd with this file. The major scan axis doesn't seem to correspond exactly to any of the manipulator axes")
			if min(num_misses_Major)!=max(num_misses_Major):
				bestGuessIndex = num_misses_Major.index(min(num_misses_Major))+2
				bestGuessAxisName = loadedSpectrum['Metadata']['Manipulator Axis Names'][bestGuessIndex]
				print(r"   The closest match seems to be axis {} ({}) with a {}% overlap , so I'll assume it was that one".format(bestGuessIndex,bestGuessAxisName,(100*len(majorAxis)-min(num_misses_Major))/len(majorAxis)))
				loadedSpectrum['majorAxisLabel']=bestGuessAxisName
				loadedSpectrum['majorAxis']=loadedSpectrum['Metadata']['Manipulator Axes'][bestGuessIndex][0::lenMinorAxis]
				foundMajorAxis=True
				#loadedSpectrum['majorAxis']=bestGuessAxisName
				

		if foundMinorAxis==False:
			print("(!!) WARNING: Something is a bit odd with this file. The minor scan axis doesn't seem to correspond exactly to any of the manipulator axes")
			if min(num_misses_Minor)!=max(num_misses_Minor):
				bestGuessIndex = num_misses_Minor.index(min(num_misses_Minor))+2
				bestGuessAxisName = loadedSpectrum['Metadata']['Manipulator Axis Names'][bestGuessIndex]
				print("   The closest match seems to be axis {} ({}), so I'll assume it was that one".format(bestGuessIndex,bestGuessAxisName))
				loadedSpectrum['minorAxisLabel']=bestGuessAxisName
				loadedSpectrum['minorAxis']=minorAxis[0:lenMinorAxis]
				foundMinorAxis=True

		if foundMajorAxis==False or foundMinorAxis==False:
			print("I'm sorry, I don't know how to proceed with this file :(")
			
		else: 
			majorLength = len(loadedSpectrum['majorAxis'])
			majorStep =(loadedSpectrum['majorAxis'][-1]-loadedSpectrum['majorAxis'][0])/(len(loadedSpectrum['majorAxis'])-1)
			majorStart = loadedSpectrum['majorAxis'][0]
			loadedSpectrum['majorAxis'] = np.array([float("{:.4f}".format(majorStart + ii*majorStep)) for ii in range(majorLength)]) 
			
			loadedSpectrum['Axis'][3] = np.array(loadedSpectrum['majorAxis'])
			loadedSpectrum['AxisLabel'][3]=loadedSpectrum['majorAxisLabel']
			if loadedSpectrum['AxisLabel'][3]=="X" or loadedSpectrum['AxisLabel'][3]=="Y":
				loadedSpectrum['AxisUnits'][3]="mm"
			else:
				loadedSpectrum['AxisUnits'][3]=r"$\degree$"
			minorLength = len(loadedSpectrum['minorAxis'])
			minorStep =(loadedSpectrum['minorAxis'][-1]-loadedSpectrum['minorAxis'][0])/(len(loadedSpectrum['minorAxis'])-1)
			minorStart = loadedSpectrum['minorAxis'][0]
			loadedSpectrum['minorAxis'] = np.array([float("{:.4f}".format(minorStart + ii*minorStep)) for ii in range(minorLength)])


			loadedSpectrum['Axis'][2] = np.array(loadedSpectrum['minorAxis'])
			loadedSpectrum['AxisLabel'][2]=loadedSpectrum['minorAxisLabel']
			if loadedSpectrum['AxisLabel'][2]=="X" or loadedSpectrum['AxisLabel'][2]=="Y":
				loadedSpectrum['AxisUnits'][2]="mm"
			else:
				loadedSpectrum['AxisUnits'][2]=r"$\degree$"

			if beQuiet==False:print("Major scan axis was {}, from {:.3f} to {:.3f} step {:.4f} ({} points)".format(loadedSpectrum['majorAxisLabel'],loadedSpectrum['majorAxis'][0],loadedSpectrum['majorAxis'][-1],loadedSpectrum['majorAxis'][1]-loadedSpectrum['majorAxis'][0],len(loadedSpectrum['majorAxis'])))
			if beQuiet==False:print("Minor scan axis was {}, from {:.3f} to {:.3f} step {:.4f} ({} points)".format(loadedSpectrum['minorAxisLabel'],loadedSpectrum['minorAxis'][0],loadedSpectrum['minorAxis'][-1],loadedSpectrum['minorAxis'][1]-loadedSpectrum['minorAxis'][0],len(loadedSpectrum['minorAxis'])))
			if beQuiet==False: print("Recalculated axis values, since SES header rounds to 3 decimal places")


	if fileType=='1D Manipulator Scan':	

		manipulatorScannedAxisNames=[]
		numberOfScannedAxes=0               
		for linenumber,axisName in enumerate(loadedSpectrum['Metadata']['Manipulator Axis Names']):
			if loadedSpectrum['Metadata']['Manipulator Axes'][linenumber][-1]!=loadedSpectrum['Metadata']['Manipulator Axes'][linenumber][0]:
				numberOfScannedAxes+=1
				manipulatorScannedAxisNames.append(axisName)
				#if beQuiet==False: print(loadedSpectrum['Metadata']['Manipulator Axes'][linenumber])
				stepSize = abs(loadedSpectrum['Metadata']['Manipulator Axes'][linenumber][-1]-loadedSpectrum['Metadata']['Manipulator Axes'][linenumber][0])/(numImages-1)
				if beQuiet==False: print("Axis \'{}\' was scanned from {} to {} in steps of {:.5f}".format(axisName,loadedSpectrum['Metadata']['Manipulator Axes'][linenumber][0],loadedSpectrum['Metadata']['Manipulator Axes'][linenumber][-1],stepSize))
			elif beQuiet==False: print("Axis \'{}\' was {}".format(axisName,loadedSpectrum['Metadata']['Manipulator Axes'][linenumber][0]))

		if numberOfScannedAxes==1:
			#print("\nInferring that the primary manipulator scan axis must be:",[ii for ii in manipulatorScannedAxisNames])
			primaryAxislinenumber = loadedSpectrum['Metadata']['Manipulator Axis Names'].index(manipulatorScannedAxisNames[0])         
			primaryManipulatorAxis = loadedSpectrum['Metadata']['Manipulator Axes'][primaryAxislinenumber]
		

		elif whichManipulatorAxis in manipulatorScannedAxisNames:
			if beQuiet==False: print("Treating {} as the primary scan axis".format(whichManipulatorAxis))
			primaryAxislinenumber = loadedSpectrum['Metadata']['Manipulator Axis Names'].index(whichManipulatorAxis)         
			primaryManipulatorAxis = loadedSpectrum['Metadata']['Manipulator Axes'][primaryAxislinenumber]
		
		elif numberOfScannedAxes==2:
			if beQuiet==False: print("There are two scanned axes, but one of them is just the index. Treating {} as the primary scan axis".format(manipulatorScannedAxisNames[1]))
			primaryAxislinenumber = loadedSpectrum['Metadata']['Manipulator Axis Names'].index(manipulatorScannedAxisNames[1])         
			primaryManipulatorAxis = loadedSpectrum['Metadata']['Manipulator Axes'][primaryAxislinenumber]				

		else:
			if(whichManipulatorAxis==''):
				if beQuiet==False: print("\n-------- !! WARNING !! ---------")
				if beQuiet==False: print("I don't know which of these is the primary manipulator scan axis, and you didn't specify.")
				if beQuiet==False: print("I will therefore assume that the primary axis is ",manipulatorScannedAxisNames[0])
				if beQuiet==False: print("To choose a different primary axis, please call this function again, passing the additional argument whichManipulatorAxis=n, where n is one of:",[ii for ii in manipulatorScannedAxisNames])
				if beQuiet==False: print("---------------------------------")
				primaryAxislinenumber = loadedSpectrum['Metadata']['Manipulator Axis Names'].index(manipulatorScannedAxisNames[0])         
				primaryManipulatorAxis = loadedSpectrum['Metadata']['Manipulator Axes'][primaryAxislinenumber]
					
			else:
				if beQuiet==False: print("\n-------- !! WARNING !! ---------")
				if beQuiet==False: print("The name of the primary manipulator scan axis that you provided ({}) is not the name of a scanned axis ({}).".format(whichManipulatorAxis,manipulatorScannedAxisNames))
				if beQuiet==False: print("I will therefore assume that the primary axis is ",manipulatorScannedAxisNames[0])
				if beQuiet==False: print("To choose a different primary axis, please call this function again, passing the additional argument whichManipulatorAxis=n, where n is one of:",[ii for ii in manipulatorScannedAxisNames])
				if beQuiet==False: print("---------------------------------")
				primaryAxislinenumber = loadedSpectrum['Metadata']['Manipulator Axis Names'].index(manipulatorScannedAxisNames[0])         
				primaryManipulatorAxis = loadedSpectrum['Metadata']['Manipulator Axes'][primaryAxislinenumber]

			
		if beQuiet==False: print("Recalculated axis values, since SES header rounds to 3 decimal places")
		axisStepSize = (loadedSpectrum['Metadata']['Manipulator Axes'][primaryAxislinenumber][-1]-loadedSpectrum['Metadata']['Manipulator Axes'][primaryAxislinenumber][0])/(numImages-1)
		axisStart = loadedSpectrum['Metadata']['Manipulator Axes'][primaryAxislinenumber][0] 
		loadedSpectrum['Axis'][2] = np.array([axisStart + ii*axisStepSize for ii in range(numImages)])
		loadedSpectrum['AxisLabel'][2]=loadedSpectrum['Metadata']['Manipulator Axis Names'][primaryAxislinenumber]
		loadedSpectrum['AxisUnits'][2]=loadedSpectrum['Metadata']['Manipulator Axis Units'][primaryAxislinenumber]

	return loadedSpectrum