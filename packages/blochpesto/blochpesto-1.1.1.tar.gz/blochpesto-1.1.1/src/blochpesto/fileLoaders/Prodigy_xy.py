try:	import numpy as np
except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")

import re,time
import blochpesto as pesto

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


def load(fileName,**kwargs):

	# Default parameter names:
	PARAMETER_SHIFTX = "ShiftX [a.u.]"
	PARAMETER_SHIFTY = "ShiftY [a.u.]"
	PARAMETER_SCATTERINGENERGY = "ScatteringEnergy [V]"
	PARAMETER_TARGETPOLARIZATION = "NegativePolarity"


	"""
	Initial remarks about the xy file format:
	-----------------------------------------
	- The xy file format is madness and misery

	- For a spin measurement, a 'cycle' in these files corresponds to one iteration in a 'Profiling' or 'Step Profiling' sequence. 

	- A single CCD ARPES image consists of a single 'cycle' that has many 'curves', each corresponding to an EDC 

	- The parameter 'Step' refers to step profiling - usually this is magnetization cycles (coil neg/pos) but it could also be ShiftX/ShiftY points in an arbitrary MDC

	- A 'scan' is generally a repeat of a measurement to accumulate statistics.


	File loading logic:
	------------------
	We first read the file header, stopping when the measurement data begins

	Then we iterate over the data and load everything into memory

	Then we try to deduce what the measurement was, and reassemble the information into a meaningful structure


	Output format:
	--------------
	As a pesto 'spectrum' dictionary. There is generally an extra dimension to the data field corresponding to target magnetizations, and the corresponding polarity is stored in metadata 
	
	
	counts/s --> counts conversion:
	-------------------------------
	By default Prodigy exports xy files with intensity in counts/s instead of total counts. (It's possible to manually override this for each export).
	This matters for error bar calculations in spin, where we assume the error scales as sqrt of the total counts.

	This loader defaults to always converting from counts/s to counts. To do this we only need to know dwell time. The number of scans is not needed - if it's more than one, 
	a file that was exported in counts/s without separating scans is reporting the AVERAGE intensity, not the SUM.
	
	(A file exported in counts instead of counts/s behaves as expected (i.e. if scans are not separated, it reports the sum not the average))
	
	"""

	def lineContainsData(line):
		if not '#' in line and len(line)>1: return True 
		else: return False

	def findUniqueElements(inputList):
		unique_list=[]
		for ii in inputList:
			if ii not in unique_list:
				unique_list.append(ii)
		return unique_list

	if kwargs['mask']==None: mask=[]
	else: mask=kwargs['mask']

	beQuiet=kwargs.get('beQuiet')

	loadedSpectrum={}
	loadedSpectrum['Metadata']={}
	loadedSpectrum['Metadata']['CurrentFilePath']=fileName

	with open(fileName) as f:
		file = f.readlines()

	#**********************************************************************************************************************************************
	#
	# 							Extract information from the file header
	#
	#**********************************************************************************************************************************************
	
	intensityIsInCountsPerSecond=False
	readingComment=False
	scanMode=""

	for i, line in enumerate(file):

		if '# Created by:' in line:
			SpecsLabVersion =  line.split("Version")[1]
			versionNumberString = (SpecsLabVersion.split("-")[0])
			versionNumber = versionNumberString.split(".")[0] + "." + versionNumberString.split(".")[1]
			loadedSpectrum['Metadata']['SpecsLabVersion'] = float(versionNumber)

		if '#   Count Rate:' in line: 	
			countFormat = line.split()[-1].rstrip("\n")
			if countFormat == 'Second': intensityIsInCountsPerSecond = True
			continue

		if '# Spectrum ID:' in line: 	
			loadedSpectrum['Metadata']['SpectrumID']=int(line.split()[-1].rstrip("\n"))
			continue

		if '# Acquisition Date' in line: 
			loadedSpectrum['Metadata']['Date']=line.split(": ")[1].split()[0]
			loadedSpectrum['Metadata']['Time']=line.split(": ")[1].split()[1]
			continue

		if '# Analyzer: ' in line: 		
			loadedSpectrum['Metadata']['Analyzer']=line.split()[-1].rstrip("\n")
			continue

		if '# Analyzer Lens:' in line: 			
			loadedSpectrum['Metadata']['LensMode']=line.split()[-1].split()[0]

			continue

		if '# Scan Mode:' in line: 		
			scanMode=line.split()[-1].rstrip("\n")
			continue

		if '# Curves/Scan: ' in line:
			curves_per_scan = int(line.split()[-1].rstrip("\n"))	
			loadedSpectrum['Metadata']['num_nonEnergyVals'] = curves_per_scan
			continue

		if '# Values/Curve: ' in line: 	
			loadedSpectrum['Metadata']['num_EnergyVals'] = int(line.split()[-1].rstrip("\n"))
			continue

		if 'Dwell Time:' in line: 			
			loadedSpectrum['Metadata']['Dwell Time']=float(line.split()[-1].rstrip("\n"))
			continue

		if '# Pass Energy: ' in line: 			
			loadedSpectrum['Metadata']['Pass Energy']=float(line.split()[-1].rstrip("\n"))
			continue

		if '# Comment: ' in line: 	
			readingComment=True		
			loadedSpectrum['Metadata']['Comment']=line
			continue
		if '#' in line and readingComment==True:
			loadedSpectrum['Metadata']['Comment']+=line

		if not '#' in line and readingComment==True:
			readingComment=False

		if '# Cycle:' in line and not 'Curve' in line: # We've reached the start of data and hence the end of the header
			break



	if scanMode=="SnapshotFAT" and loadedSpectrum['Metadata']['num_EnergyVals']==1:  #need to look at the data file to determine the number of energy values

		cycleDataLoadInProgress=False
		energyVals=[]
		for i, line in enumerate(file):
			if lineContainsData(line):
				if cycleDataLoadInProgress==False: cycleDataLoadInProgress=True

				energyVals.append(float(line.split()[0]))

			elif cycleDataLoadInProgress==True:
				break

		loadedSpectrum['Metadata']['num_EnergyVals']=len(energyVals)


	#**********************************************************************************************************************************************
	#
	# 							Extract data from the file body
	#
	#**********************************************************************************************************************************************
	
	cycles=[]
	readingCycle=False
	cycleDataLoadCompleted=False
	cycleDataLoadInProgress=False
	cycleIndex=-1
	scanIndex=0
	curveIndex=0

	for i, line in enumerate(file):

		if beQuiet==False and len(file)>1e6:
			if i%int(len(file)/200)==0:
				printProgressBar(i, len(file)-1, prefix = 'Progress:', suffix = 'Complete', length = 50)

		if '# Cycle:' in line and not 'Curve' in line and readingCycle==False:
			#print("New cycle starts on line {}: {}".format(i,line))
			cycleIndex+=1
			curveIndex,scanIndex=-1,0

			cycles.append({})
			cycles[cycleIndex]['index']=int(line.split(":")[1].split(",")[0].rstrip("\n"))
			cycles[cycleIndex]['parameters']={}
			cycles[cycleIndex]['energy']=[]
			cycles[cycleIndex]['counts']=[]

			readingCycle = True
			continue
		
		if readingCycle==True:
			if '# Parameter:' in line:
				#print("Parameter info: {}: {}".format(i,line))

				key = re.findall('"([^"]*)"',line)[0] # Return the first substring that is contained within quotes, e.g. Parameter: "Lens1 [V]" = 220 --> Lens1 [V]
				key = key.replace("(","[").replace(")","]") #Change round to square brackets, precaution against Prodigy changing convention later
				cycles[cycleIndex]['parameters'][key]=line.split()[-1].rstrip("\n")
				continue

			if '# NonEnergyOrdinate' in line: # Expect to see this once per curve, in a CCD measurement
				key = 'NonEnergyOrdinate'
				if not key in cycles[cycleIndex]['parameters']: cycles[cycleIndex]['parameters'][key]=[]
				if key in cycles[cycleIndex]['parameters']: cycles[cycleIndex]['parameters'][key].append(line.split()[-1].rstrip("\n"))
				continue
	
			if '# Cycle:' in line and "Curve" in line:  
				
				new_curveIndex=int(line.split("Curve:")[-1].split(",")[0])
				#print("Starting on curve {} of an anticipated {}".format(new_curveIndex+1,loadedSpectrum['Metadata']['num_nonEnergyVals']))

				# Is this a new curve, or a repeat of one we've already met? (this can happen if there are multiple uncollapsed scans)
				if new_curveIndex!=curveIndex and new_curveIndex==0:
					 cycles[cycleIndex]['counts'].append(np.zeros((loadedSpectrum['Metadata']['num_EnergyVals'],loadedSpectrum['Metadata']['num_nonEnergyVals']),np.float32))
					 cycles[cycleIndex]['energy'].append(np.zeros((loadedSpectrum['Metadata']['num_EnergyVals']),np.float32))
				curveIndex=new_curveIndex


			elif '# Cycle:' in line and "Scan" in line and curveIndex==0: 
				cycles[cycleIndex]['counts'].append(np.zeros((loadedSpectrum['Metadata']['num_EnergyVals'],loadedSpectrum['Metadata']['num_nonEnergyVals']),np.float32))
				cycles[cycleIndex]['energy'].append(np.zeros((loadedSpectrum['Metadata']['num_EnergyVals']),np.float32))
				scanIndex=int(line.split("Scan:")[-1].split(",")[0])

			if lineContainsData(line):
				if cycleDataLoadInProgress==False:
					datapointIndex = 0
					cycleDataLoadInProgress=True
				
				energy,intensity= float(line.split()[0]), float(line.split()[-1].rstrip("\n"))

				cycles[cycleIndex]['energy'][scanIndex][datapointIndex]=energy
				cycles[cycleIndex]['counts'][scanIndex][datapointIndex,curveIndex]=intensity

				datapointIndex+=1
				#print("Read datapoint {} of an anticipated {}".format(datapointIndex,loadedSpectrum['Metadata']['num_EnergyVals']))
				if datapointIndex == loadedSpectrum['Metadata']['num_EnergyVals']: #Loaded all the data for this curve/scan
					if curveIndex == loadedSpectrum['Metadata']['num_nonEnergyVals']-1:
						readingCycle=False
					cycleDataLoadInProgress=False
				
				continue

	if beQuiet==False: print("")

	if loadedSpectrum['Metadata']['SpecsLabVersion']<4.99:
		if beQuiet==False: print("This version of Prodigy had a different deflector terminology ('SAL X' instead of 'Shift X')".format(SpecsLabVersion))
		PARAMETER_SHIFTX,PARAMETER_SHIFTY = "SAL X [deg]","SAL Y [deg]"
	else: PARAMETER_SHIFTX,PARAMETER_SHIFTY = "ShiftX [a.u.]","ShiftY [a.u.]"

	uniqueParameterValues={}

	for parameterName in cycles[0]['parameters'].keys():
		#print("Scanning for values of parameter {}".format(parameterName))
		allValues=[]
		try:
			for cycle in cycles:
				try: allValues.append(cycle['parameters'][parameterName])
				except KeyError: pass

		except Exception as e: 
			if beQuiet==False: print("\nException trying to scan for values of parameter {}: {}".format(parameterName,e))
			pass

		uniqueParameterValues[parameterName]=findUniqueElements(allValues)




	#**********************************************************************************************************************************************
	#
	# 							Figure out what this measurement is, and compile the separate cycles accordingly
	#
	#**********************************************************************************************************************************************


	try: analyzer = loadedSpectrum['Metadata']['Analyzer']
	except Exception as e:
		print("Wasn't able to identify an analyer type in this file, so I dont know how to interpret it")
		return 0


	scanIdentified = False

	###----------------------------------------------
	##    Target scattering scan
	###----------------------------------------------
		# It's a target scattering scan if:
		# analyzer is "PhoibosSpin", 
		# AND the parameter PARAMETER_SCATTERINGENERGY has been swept


	if analyzer == "PhoibosSpin":
		if PARAMETER_SCATTERINGENERGY in uniqueParameterValues.keys():
			if len(uniqueParameterValues[PARAMETER_SCATTERINGENERGY]) > 1:
				if beQuiet==False: print("I deduce that this is a target scattering scan\n")
				scanIdentified=True
				print("KAJDFLHADFLKJ")
				loadedSpectrum['Metadata']['MeasurementType']="Ferrum target scattering scan"
				loadedSpectrum['Axis']=[float(ii) for ii in uniqueParameterValues[PARAMETER_SCATTERINGENERGY]]
				loadedSpectrum['AxisLabel']="Scattering Energy"
				loadedSpectrum['AxisUnits']="V"
				loadedSpectrum['data']=np.zeros((len(loadedSpectrum['Axis'])),np.float32)

				for ii,scatteringEnergy in enumerate(uniqueParameterValues[PARAMETER_SCATTERINGENERGY]):
					for cycle in cycles:
						if cycle['parameters'][PARAMETER_SCATTERINGENERGY]==scatteringEnergy:
							loadedSpectrum['data'][ii]+=np.sum(cycle['counts'])

				loadedSpectrum['Metadata']['TargetScatteringScan']=True
				return loadedSpectrum

	###----------------------------------------------
	##   3D CCD ARPES image
	###----------------------------------------------
		# It's a 3D CCD ARPES volume if:
		# analyzer is "PhoibosCCD", 
		# AND the parameter PARAMETER_SHIFTX has been swept


	if analyzer=="PhoibosCCD" and scanIdentified==False:

		if PARAMETER_SHIFTX in uniqueParameterValues.keys():
			if len(uniqueParameterValues[PARAMETER_SHIFTX]) > 1:
				if beQuiet==False: print("I deduce that this is a CCD deflector map, with {} deflector values\n".format(len(uniqueParameterValues[PARAMETER_SHIFTX])))
				scanIdentified=True
				loadedSpectrum['Metadata']['MeasurementType']="3D CCD ShiftX map"

				loadedSpectrum['Axis']=[[],[],[]]
				loadedSpectrum['AxisLabel']=["","",""]
				loadedSpectrum['AxisUnits']=["","",""]

				loadedSpectrum['AxisLabel'][0]="Kinetic energy"
				loadedSpectrum['AxisUnits'][0]="eV"
				loadedSpectrum['Axis'][0]=np.array(cycles[0]['energy'][0])

				loadedSpectrum['AxisLabel'][1]="Analyzer angle"
				loadedSpectrum['AxisUnits'][1]="deg"
				loadedSpectrum['Axis'][1]=np.array([float(ii) for ii in findUniqueElements(cycles[0]['parameters']['NonEnergyOrdinate'])])

				loadedSpectrum['AxisLabel'][2]="Shift X"
				loadedSpectrum['AxisUnits'][2]="deg"
				loadedSpectrum['Axis'][2]=[float(ii) for ii in uniqueParameterValues[PARAMETER_SHIFTX]]

				loadedSpectrum['data']=np.zeros((len(loadedSpectrum['Axis'][0]),len(loadedSpectrum['Axis'][1]),len(loadedSpectrum['Axis'][2])),np.float32)

			for ii,shiftX in enumerate(uniqueParameterValues[PARAMETER_SHIFTX]):
				for cycle in cycles:
					if cycle['parameters'][PARAMETER_SHIFTX]==shiftX:
						for scan in cycle['counts']:
							loadedSpectrum['data'][:,:,ii]+=scan


	
	###----------------------------------------------
	##   2D CCD ARPES image
	###----------------------------------------------
		# It's a 2D CCD ARPES volume if:
		# analyzer is "PhoibosCCD", 
		# AND the parameter PARAMETER_SHIFTX has NOT been swept
		# AND the parameter PARAMETER_SHIFTY has NOT been swept

	if analyzer=="PhoibosCCD" and scanIdentified==False:
		is_an_image=False
		if PARAMETER_SHIFTX not in uniqueParameterValues.keys():
			is_an_image=True
		if PARAMETER_SHIFTX in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTX]) == 1:
			is_an_image=True

		if is_an_image==True:
			if beQuiet==False: print("I deduce that this is a 2D CCD measurement")
			scanIdentified=True
			loadedSpectrum['Metadata']['MeasurementType']="2D CCD image"
					
			loadedSpectrum['Axis']=[[],[]]
			loadedSpectrum['AxisLabel']=["",""]
			loadedSpectrum['AxisUnits']=["",""]

			loadedSpectrum['AxisLabel'][0]="Kinetic energy"
			loadedSpectrum['AxisUnits'][0]="eV"
			loadedSpectrum['Axis'][0]=np.array(cycles[0]['energy'][0])

			loadedSpectrum['AxisLabel'][1]="Analyzer angle"
			loadedSpectrum['AxisUnits'][1]="deg"
			loadedSpectrum['Axis'][1]=np.array([float(ii) for ii in findUniqueElements(cycles[0]['parameters']['NonEnergyOrdinate'])])
			
			loadedSpectrum['data']=np.zeros((len(loadedSpectrum['Axis'][0]),len(loadedSpectrum['Axis'][1])),np.float32)
			for cycle in cycles:
				for scan in cycle['counts']:
					loadedSpectrum['data']+=scan


	###----------------------------------------------
	##----------------- Spin EDC
	###----------------------------------------------
		# It's a spin-resolved EDC if:
		# analyzer is "PhoibosSpin", 
		# AND the parameter PARAMETER_SHIFTX has NOT been swept
		# AND the parameter PARAMETER_SHIFTY has NOT been swept

	if analyzer=="PhoibosSpin" and scanIdentified==False:

		is_an_EDC=True

		if PARAMETER_SHIFTX in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTX])>1:
			is_an_EDC=False
		if PARAMETER_SHIFTY in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTY])> 1:
			is_an_EDC=False
		if PARAMETER_SCATTERINGENERGY in uniqueParameterValues.keys():
			is_an_EDC=False

		if is_an_EDC==True:
			if beQuiet==False: print("I deduce that this is a spin EDC\n")
			scanIdentified=True

			loadedSpectrum['Metadata']['MeasurementType']="Spin EDC"

			loadedSpectrum['Axis']=[[],[]]
			loadedSpectrum['AxisLabel']=["",""]
			loadedSpectrum['AxisUnits']=["",""]

			loadedSpectrum['AxisLabel'][0]="Kinetic energy"
			loadedSpectrum['AxisUnits'][0]="eV"
			loadedSpectrum['Axis'][0]=np.array(cycles[0]['energy'][0])
			energyAxis=loadedSpectrum['Axis'][0]

			loadedSpectrum['AxisLabel'][1]="Step index"
			loadedSpectrum['AxisUnits'][1]=""
			
			rawStepAxis = np.array(sorted([int(ii) for ii in uniqueParameterValues['Step']]))
			if mask!=[]:
				if len(mask)!=len(rawStepAxis):
					print("ERROR: length of mask ({}) does not match number of coil polarity steps ({})".format(len(mask),len(rawStepAxis)))
					loadedSpectrum['Axis'][1]=rawStepAxis

				else: 
					maskedStepAxis = [jj for ii,jj in zip(mask,rawStepAxis) if ii!=0]
					loadedSpectrum['Axis'][1]=maskedStepAxis
			else:
				loadedSpectrum['Axis'][1]=rawStepAxis

			stepAxis=loadedSpectrum['Axis'][1]

			loadedSpectrum['data']=np.zeros((len(energyAxis),len(stepAxis)),np.float32)
			
			loadedSpectrum['Metadata']['CoilPolarity'] = np.zeros(len(stepAxis),dtype=object)

		
			# Determine the coil polarity corresponding to each step. Also verify that there is only a single polarity associated with each step
			# In the same loop, compile the intensity values into the data field
			for ii,stepNumber in enumerate(stepAxis):
				polarity=[]
				for cycle in cycles:
					if int(cycle['parameters']['Step'])==stepNumber:
						polarity.append(cycle['parameters']['NegativePolarity'])

						for scan in cycle['counts']: #Collapse scans if necessary
							loadedSpectrum['data'][:,ii]+=scan[:,0] 

				if len(set(polarity))==1:
					loadedSpectrum['Metadata']['CoilPolarity'][ii]=polarity[0]
				else:
					print("ERROR! Coil polarities not well defined!")
					return 0
	
			







	###----------------------------------------------
	##----------------- Spin MDC
	###----------------------------------------------
		# It's a spin-resolved MDC if:
		# analyzer is "PhoibosSpin", 
		# AND any of (PARAMETER_SHIFTX,PARAMETER_SHIFTY) have been swept, 
		# AND it corresponds to a single line through angle space (otherwise it's an energy surface or 3D volume)
		# AND there is only a single energy value (otherwise it's a spin image)

		# To check whether it's a single line through angle space or a 2D raster, we can look at how many cycles there are.
		# For a 1D linecut, there should be (major axis)*(steps) number of cycles.
		# for a 2D k-k image, there should be (outer angle axis)*(inner angle axis)*(steps) number of cycles.

		# But what is the major axis? In the simplest case, only ShiftX or ShiftY will be swept, i.e. an orthogonal MDC cut. In that case, we should use the swept axis as the 'main' angle axis

		# Arbitrary cuts (ShiftX and ShiftY are both swept) are a little more complicated. We can't just pick one and call it the 'main' angle axis, since they are 
		# not guaranteed to be monotonic - it's possible to define scans in such a way that either ShiftX or ShiftY (or both!) have repeating values.

		# A way to handle this is to make the 'main' angle axis a composite one that tracks distance covered in angle space, i.e. sqrt(ShiftX**2 + ShiftY**2)
		# Unfortunately there is nothing like a "step number" index in the file, so the only way to know how many distinct (ShiftX,ShiftY) coordinates are in the scan is to search for them

		# A potential problem with this is telling the difference between an arbitrary MDC and a 2D raster-scanned k-k image.
		# In both cases two axes have been swept, but the raster scan will possess (num ShiftX values)*(num ShiftY values) datapoints.
		# which will always be more than for a 1D linecut.

	if analyzer=="PhoibosSpin" and scanIdentified==False:
		is_an_MDC=False
		arbitrary_sweep = False

		majorAxes=[]
		if len(np.array(cycles[0]['energy'][0]))==1:
			if PARAMETER_SHIFTX in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTX])>1:
				is_an_MDC=True
				majorAxes.append(PARAMETER_SHIFTX)
			if PARAMETER_SHIFTY in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTY])> 1:
				is_an_MDC=True
				majorAxes.append(PARAMETER_SHIFTY)

			# Simple case where only 1 axis is being swept
			if len(majorAxes)==1 and len(cycles) != len(uniqueParameterValues[majorAxes[0]]) * len(uniqueParameterValues['Step']):
				is_an_MDC=False

			elif len(majorAxes)>1: 
				arbitrary_sweep=True
				uniqueCoordinates=[]

				for cycle in cycles:
					
					coordinate = np.array([float(cycle['parameters'][PARAMETER_SHIFTX]),float(cycle['parameters'][PARAMETER_SHIFTY])])
					
					if len(uniqueCoordinates)==0: uniqueCoordinates.append(coordinate)
					
					else:
						already_known = np.any(np.all(coordinate == uniqueCoordinates, axis=1))
						if not already_known: uniqueCoordinates.append(coordinate)

				angularSeparations=[np.linalg.norm(a-b) for a,b in zip(uniqueCoordinates[1:],uniqueCoordinates[:-1])]
				angularSeparations.insert(0,0)	
				compositeAxis=np.cumsum(angularSeparations)
				if len(cycles) != len(compositeAxis) * len(uniqueParameterValues['Step']):
					is_an_MDC=False
				if len(cycles) == len(uniqueParameterValues[PARAMETER_SHIFTX]) * len(uniqueParameterValues[PARAMETER_SHIFTY])* len(uniqueParameterValues['Step']):
					is_an_MDC=False #Because it's a raster scan instead



		if is_an_MDC==True:

			loadedSpectrum['Metadata']['MeasurementType']="Spin MDC"

			loadedSpectrum['Axis']=[[],[]]
			loadedSpectrum['AxisLabel']=["",""]
			loadedSpectrum['AxisUnits']=["",""]

			if arbitrary_sweep==False:

				if beQuiet==False: print("I deduce that this is a simple spin MDC sweeping only one deflector axis\n")
				scanIdentified=True
				if majorAxes[0]==PARAMETER_SHIFTX: 
					loadedSpectrum['AxisLabel'][0]="ShiftX"
					loadedSpectrum['Axis'][0]=np.array(sorted([float(ii) for ii in uniqueParameterValues[PARAMETER_SHIFTX]]))
					loadedSpectrum['AxisUnits'][0]="deg"

				elif majorAxes[0]==PARAMETER_SHIFTY: 
					loadedSpectrum['AxisLabel'][0]="ShiftY"
					loadedSpectrum['Axis'][0]=np.array(sorted([float(ii) for ii in uniqueParameterValues[PARAMETER_SHIFTY]]))
					loadedSpectrum['AxisUnits'][0]="deg"

			if arbitrary_sweep==True:

				if beQuiet==False: print("I deduce that this is an 'arbitrary' spin MDC sweeping two deflector axes. \nThe angle axis will be converted to euclidian path length; the raw deflector coordinates are available in metadata\n")
				scanIdentified=True
				loadedSpectrum['AxisLabel'][0]="Angle"
				loadedSpectrum['Axis'][0]=compositeAxis
				loadedSpectrum['AxisUnits'][0]="deg"

				loadedSpectrum['Metadata']['MajorAxes']=[]
				loadedSpectrum['Metadata']['MajorAxes'].append({})
				loadedSpectrum['Metadata']['MajorAxes'][-1]['AxisLabel']="ShiftX"
				loadedSpectrum['Metadata']['MajorAxes'][-1]['AxisUnits']="deg"
				loadedSpectrum['Metadata']['MajorAxes'][-1]['Axis']=np.array(sorted([ii for (ii,jj) in uniqueCoordinates]))

				loadedSpectrum['Metadata']['MajorAxes'].append({})
				loadedSpectrum['Metadata']['MajorAxes'][-1]['AxisLabel']="ShiftY"
				loadedSpectrum['Metadata']['MajorAxes'][-1]['AxisUnits']="deg"
				loadedSpectrum['Metadata']['MajorAxes'][-1]['Axis']=np.array(sorted([jj for (ii,jj) in uniqueCoordinates]))


			loadedSpectrum['AxisLabel'][1]="Step index"
			loadedSpectrum['AxisUnits'][1]=""

			rawStepAxis = np.array(sorted([int(ii) for ii in uniqueParameterValues['Step']]))
			if mask!=[]:
				if len(mask)!=len(rawStepAxis):
					print("ERROR: length of mask ({}) does not match number of coil polarity steps ({})".format(len(mask),len(rawStepAxis)))
					loadedSpectrum['Axis'][1]=rawStepAxis

				else: 
					maskedStepAxis = [jj for ii,jj in zip(mask,rawStepAxis) if ii!=0]
					loadedSpectrum['Axis'][1]=maskedStepAxis
			else:
				loadedSpectrum['Axis'][1]=rawStepAxis

			angleAxis = loadedSpectrum['Axis'][0]
			stepAxis = loadedSpectrum['Axis'][1]

			loadedSpectrum['data']=np.zeros((len(angleAxis),len(stepAxis)),np.float32)

			loadedSpectrum['Metadata']['CoilPolarity'] = np.zeros(len(stepAxis),dtype=object)

			if arbitrary_sweep==False:
				# Determine the coil polarity corresponding to each step. Also verify that there is only a single polarity associated with each step
				# In the same loop, compile the intensity values into the data field
				for ii,stepNumber in enumerate(stepAxis):
					polarity=[]
					for kk,angle in enumerate(angleAxis):
						for cycle in cycles:
							if int(cycle['parameters']['Step'])==stepNumber and float(cycle['parameters'][majorAxes[0]])==angle:
								polarity.append(cycle['parameters']['NegativePolarity'])

								for scan in cycle['counts']: #Collapse scans if necessary
									loadedSpectrum['data'][kk,ii]+=scan[:,0] 

					assert(len(set(polarity))==1), "Coil polarities in this save file seem to be inconsistent"
					loadedSpectrum['Metadata']['CoilPolarity'][ii]=polarity[0]

			if arbitrary_sweep==True:
				# Determine the coil polarity corresponding to each step. Also verify that there is only a single polarity associated with each step
				# In the same loop, compile the intensity values into the data field
				for ii,stepNumber in enumerate(stepAxis):
					polarity=[]
					for kk,coordinate in enumerate(uniqueCoordinates):

						for cycle in cycles:
							#print(coordinate[0],coordinate[1],float(cycle['parameters'][PARAMETER_SHIFTX]),float(cycle['parameters'][PARAMETER_SHIFTY]))
							if int(cycle['parameters']['Step'])==stepNumber and float(cycle['parameters'][PARAMETER_SHIFTX])==coordinate[0] and float(cycle['parameters'][PARAMETER_SHIFTY])==coordinate[1]:
								polarity.append(cycle['parameters']['NegativePolarity'])

								for scan in cycle['counts']: #Collapse scans if necessary
									loadedSpectrum['data'][kk,ii]+=scan[:,0] 

					assert(len(set(polarity))==1), "Coil polarities in this save file seem to be inconsistent"
					loadedSpectrum['Metadata']['CoilPolarity'][ii]=polarity[0]


	###-----------------------------------------------------------------------------
	##----------------- Single magnetization E-k image (typically 'alignment ARPES')
	###-----------------------------------------------------------------------------
		# It's a single-magnetization E-k image if:
		# analyzer is "PhoibosSpin" or "PhoibosIntensity"
		# any of (PARAMETER_SHIFTX,PARAMETER_SHIFTY) have been swept, 
		# AND it corresponds to a single line through angle space (otherwise it's an energy surface or 3D volume)
		# AND there is more than a single energy value
		# AND there is NOT a PARAMETER_TARGETPOLARIZATION parameter

	if analyzer in ["PhoibosSpin","PhoibosIntensity"] and scanIdentified==False:

		is_an_image=False
		majorAxes=[]
		if len(np.array(cycles[0]['energy'][0]))>1:

			if PARAMETER_SHIFTX in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTX])>1:
				majorAxes.append(PARAMETER_SHIFTX)
				is_an_image=True
			elif PARAMETER_SHIFTY in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTY])> 1:
				majorAxes.append(PARAMETER_SHIFTY)
				is_an_image=True
			if PARAMETER_TARGETPOLARIZATION in uniqueParameterValues.keys():
				is_an_image=False

						
		if is_an_image==True:
			if beQuiet==False: print("I deduce that this is ARPES with the spin detector\n")
			scanIdentified=True
			loadedSpectrum['Metadata']['MeasurementType']="ARPES with the spin detector"

			loadedSpectrum['Axis']=[[],[]]
			loadedSpectrum['AxisLabel']=["",""]
			loadedSpectrum['AxisUnits']=["",""]

			
			loadedSpectrum['AxisLabel'][0]="Kinetic energy"
			loadedSpectrum['AxisUnits'][0]="eV"
			loadedSpectrum['Axis'][0]=np.array(cycles[0]['energy'][0])

			if majorAxes[0]==PARAMETER_SHIFTX: 
				loadedSpectrum['AxisLabel'][1]="ShiftX"
				loadedSpectrum['Axis'][1]=np.array(sorted([float(ii) for ii in uniqueParameterValues[PARAMETER_SHIFTX]]))

			elif majorAxes[0]==PARAMETER_SHIFTY: 
				loadedSpectrum['AxisLabel'][1]="ShiftY"
				loadedSpectrum['Axis'][1]=np.array(sorted([float(ii) for ii in uniqueParameterValues[PARAMETER_SHIFTY]]))

			loadedSpectrum['AxisUnits'][1]="deg"


			loadedSpectrum['data']=np.zeros((len(loadedSpectrum['Axis'][0]),len(loadedSpectrum['Axis'][1])),np.float32)


			for jj,angle in enumerate(loadedSpectrum['Axis'][1]):
				for cycle in cycles:
					if float(cycle['parameters'][majorAxes[0]])==angle:
						for scan in cycle['counts']:
							loadedSpectrum['data'][:,jj]+=scan[:,0]


	###----------------------------------------------
	##----------------- Spin E-k image
	###----------------------------------------------
		# It's a spin-resolved E-k image if:
		# analyzer is "PhoibosSpin"
		# any of (PARAMETER_SHIFTX,PARAMETER_SHIFTY) have been swept, 
		# AND it corresponds to a single line through angle space (otherwise it's an energy surface or 3D volume)
		# AND there is more than a single energy value

		# To check whether it's a single line through angle space, we can look at how many cycles there are.
		# For a 1D linecut, there should be (major axis)*(steps) number of cycles.
		# for a 2D E-k image, there should be (angle axis)*(steps) number of cycles.

		# But what is the major axis? In the simplest case, only ShiftX or ShiftY will be swept, i.e. an orthogonal MDC cut. In that case, we should use the swept axis as the 'main' angle axis

		# Arbitrary cuts (ShiftX and ShiftY are both swept) are a little more complicated. We can't just pick one and call it the 'main' angle axis, since they are 
		# not guaranteed to be monotonic - it's possible to define scans in such a way that either ShiftX or ShiftY (or both!) have repeating values.

		# A way to handle this is to make the 'main' angle axis a composite one that tracks distance covered in angle space, i.e. sqrt(ShiftX**2 + ShiftY**2)
		# Unfortunately there is nothing like a "step number" index in the file, so the only way to know how many distinct (ShiftX,ShiftY) coordinates are in the scan is to search for them

	if analyzer=="PhoibosSpin" and scanIdentified==False:
		is_a_spin_image=False
		arbitrary_sweep = False
		majorAxes=[]

		if len(np.array(cycles[0]['energy'][0]))>1:
			if PARAMETER_SHIFTX in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTX])>1:
				majorAxes.append(PARAMETER_SHIFTX)
				is_a_spin_image=True
			if PARAMETER_SHIFTY in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTY])> 1:
				majorAxes.append(PARAMETER_SHIFTY)
				is_a_spin_image=True
			if PARAMETER_TARGETPOLARIZATION not in uniqueParameterValues.keys():
				is_a_spin_image=False

			# Simple case where only 1 axis is being swept
			if len(majorAxes)==1 and len(cycles) != len(uniqueParameterValues[majorAxes[0]]) * len(uniqueParameterValues['Step']):
				is_a_spin_image=False

			elif len(majorAxes)>1: 
				arbitrary_sweep=True
				uniqueCoordinates=[]

				for cycle in cycles:
					
					coordinate = np.array([float(cycle['parameters'][PARAMETER_SHIFTX]),float(cycle['parameters'][PARAMETER_SHIFTY])])
					
					if len(uniqueCoordinates)==0: uniqueCoordinates.append(coordinate)
					
					else:
						already_known = np.any(np.all(coordinate == uniqueCoordinates, axis=1))
						if not already_known: uniqueCoordinates.append(coordinate)

				angularSeparations=[np.linalg.norm(a-b) for a,b in zip(uniqueCoordinates[1:],uniqueCoordinates[:-1])]
				angularSeparations.insert(0,0)	
				compositeAxis=np.cumsum(angularSeparations)
				if len(cycles) != len(compositeAxis) * len(uniqueParameterValues['Step']):
					is_a_spin_image=False

		if is_a_spin_image==True:
			scanIdentified=True
			loadedSpectrum['Metadata']['MeasurementType']="Spin Image"
			loadedSpectrum['Metadata']['MajorAxes']=[]
			loadedSpectrum['Axis']=[[],[],[]]
			loadedSpectrum['AxisLabel']=["","",""]
			loadedSpectrum['AxisUnits']=["","",""]

			
			loadedSpectrum['AxisLabel'][0]="Kinetic energy"
			loadedSpectrum['AxisUnits'][0]="eV"
			loadedSpectrum['Axis'][0]=np.array(cycles[0]['energy'][0])



			if arbitrary_sweep==False:

				if beQuiet==False: print("I deduce that this is a simple spin-resolved energy-angle image, sweeping only one deflector axis\n")

				if majorAxes[0]==PARAMETER_SHIFTX: 
					loadedSpectrum['AxisLabel'][1]="ShiftX"
					loadedSpectrum['Axis'][1]=np.array(sorted([float(ii) for ii in uniqueParameterValues[PARAMETER_SHIFTX]]))
					loadedSpectrum['AxisUnits'][1]="deg"

				elif majorAxes[0]==PARAMETER_SHIFTY: 
					loadedSpectrum['AxisLabel'][1]="ShiftY"
					loadedSpectrum['Axis'][1]=np.array(sorted([float(ii) for ii in uniqueParameterValues[PARAMETER_SHIFTY]]))
					loadedSpectrum['AxisUnits'][1]="deg"


			if arbitrary_sweep==True:

				if beQuiet==False: print("I deduce that this is an 'arbitrary' spin-resolved energy-angle image, sweeping two deflector axes. \nThe angle axis will be converted to euclidian path length; the raw deflector coordinates are available in metadata\n")

				loadedSpectrum['AxisLabel'][1]="Angle"
				loadedSpectrum['Axis'][1]=compositeAxis
				loadedSpectrum['AxisUnits'][1]="deg"

				loadedSpectrum['Metadata']['MajorAxes']=[]
				loadedSpectrum['Metadata']['MajorAxes'].append({})
				loadedSpectrum['Metadata']['MajorAxes'][-1]['AxisLabel']="ShiftX"
				loadedSpectrum['Metadata']['MajorAxes'][-1]['AxisUnits']="deg"
				loadedSpectrum['Metadata']['MajorAxes'][-1]['Axis']=np.array(sorted([ii for (ii,jj) in uniqueCoordinates]))

				loadedSpectrum['Metadata']['MajorAxes'].append({})
				loadedSpectrum['Metadata']['MajorAxes'][-1]['AxisLabel']="ShiftY"
				loadedSpectrum['Metadata']['MajorAxes'][-1]['AxisUnits']="deg"
				loadedSpectrum['Metadata']['MajorAxes'][-1]['Axis']=np.array(sorted([jj for (ii,jj) in uniqueCoordinates]))

			loadedSpectrum['AxisLabel'][2]="Step index"
			loadedSpectrum['AxisUnits'][2]=""

			rawStepAxis = np.array(sorted([int(ii) for ii in uniqueParameterValues['Step']]))
			if mask!=[]:
				if len(mask)!=len(rawStepAxis):
					print("ERROR: length of mask ({}) does not match number of coil polarity steps ({})".format(len(mask),len(rawStepAxis)))
					loadedSpectrum['Axis'][2]=rawStepAxis

				else: 
					maskedStepAxis = [jj for ii,jj in zip(mask,rawStepAxis) if ii!=0]
					loadedSpectrum['Axis'][2]=maskedStepAxis
			else:
				loadedSpectrum['Axis'][2]=rawStepAxis

			energyAxis = loadedSpectrum['Axis'][0]
			angleAxis = loadedSpectrum['Axis'][1]
			stepAxis = loadedSpectrum['Axis'][2]

			loadedSpectrum['data']=np.zeros((len(energyAxis),len(angleAxis),len(stepAxis)),np.float32)

			loadedSpectrum['Metadata']['CoilPolarity'] = np.zeros(len(stepAxis),dtype=object)




			if arbitrary_sweep==False:
				# Determine the coil polarity corresponding to each step. Also verify that there is only a single polarity associated with each step
				# In the same loop, compile the intensity values into the data field
				for ii,stepNumber in enumerate(stepAxis):
					polarity=[]
					for kk,angle in enumerate(angleAxis):
						for cycle in cycles:
							if int(cycle['parameters']['Step'])==stepNumber and float(cycle['parameters'][majorAxes[0]])==angle:
								polarity.append(cycle['parameters']['NegativePolarity'])

								for scan in cycle['counts']: #Collapse scans if necessary
									loadedSpectrum['data'][:,kk,ii]+=scan[:,0] 

					assert(len(set(polarity))==1), "Coil polarities in this save file seem to be inconsistent"
					loadedSpectrum['Metadata']['CoilPolarity'][ii]=polarity[0]

			if arbitrary_sweep==True:
				# Determine the coil polarity corresponding to each step. Also verify that there is only a single polarity associated with each step
				# In the same loop, compile the intensity values into the data field
				for ii,stepNumber in enumerate(stepAxis):
					polarity=[]
					for kk,coordinate in enumerate(uniqueCoordinates):
						for cycle in cycles:
							if int(cycle['parameters']['Step'])==stepNumber and float(cycle['parameters'][PARAMETER_SHIFTX])==coordinate[0] and float(cycle['parameters'][PARAMETER_SHIFTY])==coordinate[1]:
								polarity.append(cycle['parameters']['NegativePolarity'])

								for scan in cycle['counts']: #Collapse scans if necessary
									loadedSpectrum['data'][:,kk,ii]+=scan[:,0] 

					assert(len(set(polarity))==1), "Coil polarities in this save file seem to be inconsistent"
					loadedSpectrum['Metadata']['CoilPolarity'][ii]=polarity[0]




	###----------------------------------------------
	##----------------- Spin k-k image
	###----------------------------------------------

	if analyzer=="PhoibosSpin"  and scanIdentified==False:

		# It's by definition an energy surface if:
		# any of (PARAMETER_SHIFTX,PARAMETER_SHIFTY) have been swept, 
		# AND there is only a single energy value (otherwise it's a spin volume)
		# AND it corresponds to a 2D raster scan through angle space (otherwise it's a 1D MDC)

		# To check whether it's a single line through angle space or a 2D raster, we can look at how many cycles there are.
		# For a 1D linecut, there should be (major axis)*(steps) number of cycles.
		# for a 2D k-k image, there should be (outer angle axis)*(inner angle axis)*(steps) number of cycles.

		# The major axis is the outer loop variable ('slow scan' axis)
		# 
		#
		#


		is_an_energySurface=False

		if len(np.array(cycles[0]['energy'][0]))==1:

			if PARAMETER_SHIFTX in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTX])>1:
				is_an_energySurface=True
			elif PARAMETER_SHIFTY in uniqueParameterValues.keys() and len(uniqueParameterValues[PARAMETER_SHIFTY])> 1:
				is_an_energySurface=True		
			
			if len(cycles) != len(uniqueParameterValues[PARAMETER_SHIFTX]) * len(uniqueParameterValues[PARAMETER_SHIFTY]) * len(uniqueParameterValues['Step']):
				is_an_energySurface=False

		if is_an_energySurface==True:
			if beQuiet==False: print("I deduce that this is a spin energy surface\n")
			scanIdentified=True
			loadedSpectrum['Metadata']['MeasurementType']="Spin Image"
	

			initial_shiftX=cycles[0]['parameters'][PARAMETER_SHIFTX]
			initial_shiftY=cycles[0]['parameters'][PARAMETER_SHIFTY]

			majorAxis,minorAxis=0,0
			for cycle in cycles[1:]:
				if cycle['parameters'][PARAMETER_SHIFTX] != initial_shiftX:
					innerAxisLabel = PARAMETER_SHIFTX
					outerAxisLabel = PARAMETER_SHIFTY
					break
				if cycle['parameters'][PARAMETER_SHIFTY] != initial_shiftY:
					innerAxisLabel = PARAMETER_SHIFTY
					outerAxisLabel = PARAMETER_SHIFTX
					break

			loadedSpectrum['Axis']=[[],[],[]]
			loadedSpectrum['AxisLabel']=["","",""]
			loadedSpectrum['AxisUnits']=["","",""]

			if innerAxisLabel == PARAMETER_SHIFTY: loadedSpectrum['AxisLabel'][0]="ShiftY"
			if innerAxisLabel == PARAMETER_SHIFTX: loadedSpectrum['AxisLabel'][0]="ShiftX"
			loadedSpectrum['AxisUnits'][0]="deg"
			loadedSpectrum['Axis'][0]=np.array(sorted([float(ii) for ii in uniqueParameterValues[innerAxisLabel]]))

			if outerAxisLabel == PARAMETER_SHIFTY: loadedSpectrum['AxisLabel'][1]="ShiftY"
			if outerAxisLabel == PARAMETER_SHIFTX: loadedSpectrum['AxisLabel'][1]="ShiftX"
			loadedSpectrum['AxisUnits'][1]="deg"
			loadedSpectrum['Axis'][1]=np.array(sorted([float(ii) for ii in uniqueParameterValues[outerAxisLabel]]))

			if beQuiet==False: print("Angle axis (inner loop) was {}, scanned from {} to {}".format(loadedSpectrum['AxisLabel'][0],loadedSpectrum['Axis'][0][0],loadedSpectrum['Axis'][0][-1]))
			if beQuiet==False: print("Angle (outer loop) was {}, scanned from {} to {}".format(loadedSpectrum['AxisLabel'][1],loadedSpectrum['Axis'][1][0],loadedSpectrum['Axis'][1][-1]))
			
			loadedSpectrum['AxisLabel'][2]="Step index"
			loadedSpectrum['AxisUnits'][2]=""
			rawStepAxis = np.array(sorted([int(ii) for ii in uniqueParameterValues['Step']]))
			if mask!=[]:
				if len(mask)!=len(rawStepAxis):
					print("ERROR: length of mask ({}) does not match number of coil polarity steps ({})".format(len(mask),len(rawStepAxis)))
					loadedSpectrum['Axis'][2]=rawStepAxis

				else: 
					maskedStepAxis = [jj for ii,jj in zip(mask,rawStepAxis) if ii!=0]
					loadedSpectrum['Axis'][2]=maskedStepAxis
			else:
				loadedSpectrum['Axis'][2]=rawStepAxis
				
			innerAxis,outerAxis,stepAxis = loadedSpectrum['Axis'][0],loadedSpectrum['Axis'][1],loadedSpectrum['Axis'][2]

			loadedSpectrum['data']=np.zeros((len(innerAxis),len(outerAxis),len(stepAxis)),np.float32)

			#----- ORIGINAL
			"""
			loadedSpectrum['Metadata']['CoilPolarity']=np.zeros((len(loadedSpectrum['Axis'][0]),len(loadedSpectrum['Axis'][1]),len(loadedSpectrum['Axis'][2])),dtype=object)

			for ii,majorAngle in enumerate(loadedSpectrum['Axis'][0]):
				for jj,minorAngle in enumerate(loadedSpectrum['Axis'][1]):
					for kk,step in enumerate(loadedSpectrum['Axis'][2]):				
						for cycle in cycles:
							if int(cycle['parameters']['Step']) == step and float(cycle['parameters'][majorAxis])==majorAngle and float(cycle['parameters'][minorAxis])==minorAngle:
								loadedSpectrum['Metadata']['CoilPolarity'][ii,jj,kk]=cycle['parameters'][PARAMETER_TARGETPOLARIZATION]
								for scan in cycle['counts']:
									loadedSpectrum['data'][ii,jj,kk]+=scan
			"""
			#--------------------

			loadedSpectrum['Metadata']['CoilPolarity'] = np.zeros(len(stepAxis),dtype=object)
		
			# Determine the coil polarity corresponding to each step. Also verify that there is only a single polarity associated with each step
			# In the same loop, compile the intensity values into the data field
			for ii,stepNumber in enumerate(stepAxis):
				polarity=[]
				for jj,innerAngle in enumerate(innerAxis):
					for kk,outerAngle in enumerate(outerAxis):
						for cycle in cycles:
							if int(cycle['parameters']['Step'])==stepNumber and float(cycle['parameters'][innerAxisLabel])==innerAngle and float(cycle['parameters'][outerAxisLabel])==outerAngle:
								polarity.append(cycle['parameters']['NegativePolarity'])

								for scan in cycle['counts']: #Collapse scans if necessary
									loadedSpectrum['data'][jj,kk,ii]+=scan[:,0]

				if len(set(polarity))==1:
					loadedSpectrum['Metadata']['CoilPolarity'][ii]=polarity[0]
				else:
					print("ERROR! Coil polarities are not well defined!")
					return 0

	#if beQuiet==False: print("-----> Operation took {:.2f}s\n".format(time.time()-t0))

	if intensityIsInCountsPerSecond==True:
		loadedSpectrum['data']=loadedSpectrum['data']*loadedSpectrum['Metadata']['Dwell Time']


	#Negative Polarity = OFF is a confusing way of saying Positive, so I'm rephrasing it here
	if 'CoilPolarity' in loadedSpectrum['Metadata']:
		polarity = loadedSpectrum['Metadata']['CoilPolarity']
		polarity[polarity=="OFF"] = "Positive"
		polarity[polarity=="ON"] = "Negative"


	return loadedSpectrum





