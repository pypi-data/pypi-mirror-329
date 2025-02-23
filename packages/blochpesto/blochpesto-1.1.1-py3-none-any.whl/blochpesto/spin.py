import blochpesto as pesto
import blochpesto.interactive
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math,copy

def quickPlot(spectrum,**kwargs):
	###----------------------------------------------
	##----------------- Spin EDC
	###----------------------------------------------
	if spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC"]:
		fig,axes=matplotlib.pyplot.subplots(figsize=[9,3],ncols=3)
		ax=axes[0]
		ax.set_title("Target scattering EDCs")
		for scanIndex,scanNumber in enumerate(spectrum['Axis'][1]):
			EDC = pesto.getProfile(spectrum,samplingAxis='y',xAxisRange=[scanNumber,scanNumber],beQuiet=True)
			if spectrum['Metadata']['CoilPolarity'][scanIndex]=='Positive': color='tab:red'
			else: color='tab:blue'
			pesto.quickPlot(EDC,axis=ax,color=color)
			legend_entries = [matplotlib.lines.Line2D([0], [0], color='tab:red', lw=3),matplotlib.lines.Line2D([0], [0], color='tab:blue', lw=3)]

		ax.legend(legend_entries, ['Coil+', 'Coil-'])

		ax=axes[1]
		ax.set_title("Averaged EDCs")
		pos,neg=average(spectrum)
		pesto.quickPlot(pos,axis=ax,color='tab:red')
		pesto.quickPlot(neg,axis=ax,color='tab:blue')
		ax=axes[2]
		ax.set_title("Asymmetry \n(C+ - C-) / (C+ + C-)")
		pesto.quickPlot(asymmetry(spectrum),axis=ax,color='black',errorbars=True,alpha=0.3)
		ax.axhline(y=0,ls='--',color='black')

		matplotlib.pyplot.tight_layout()
		matplotlib.pyplot.show()


	###----------------------------------------------
	##----------------- Spin image
	###----------------------------------------------

	if spectrum['Metadata']['MeasurementType'] in ["Spin energy surface","Spin Image"]:
		fig,axes=matplotlib.pyplot.subplots(figsize=[9,3],ncols=3)

		pos,neg = average(spectrum)
		asymmetryImage = asymmetry(spectrum)

		ax=axes[0]
		pesto.quickPlot(pos,axis=ax)
		ax.set_title("Coil plus avg")
		ax=axes[1]
		pesto.quickPlot(neg,axis=ax)
		ax.set_title("Coil minus avg")
		ax=axes[2]
		im=pesto.quickPlot(asymmetryImage,axis=ax,cmap='bwr',cmax=np.nanmax(asymmetryImage['data']),cmin=-np.nanmax(asymmetryImage['data']),returnIm=True,alpha=kwargs['alpha'])
		plt.colorbar(im)
		ax.set_title("Asymmetry \n(C+ - C-) / (C+ + C-)")
		matplotlib.pyplot.tight_layout()
		matplotlib.pyplot.show()



def despike(spectrum,interactive=True,toleranceFactor=1):
	assert('MeasurementType' in spectrum['Metadata']), "The input spectrum doesn't contain a 'MeasurementType' field in its Metadata, so I'm not sure what it is"
	assert(spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC","Spin Image"]), "This is the wrong type of spectrum for this function, expecting the MeasurementType field to be one of ('Spin EDC','Spin MDC', or 'Spin Image')"

	if interactive==True:
		if spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC"]:
			pesto.interactive.despike1D(spectrum)
		if spectrum['Metadata']['MeasurementType'] in ["Spin Image"]:
			pesto.interactive.despike2D(spectrum)	
	else:	
		stdev,median = pesto.spin.standardDeviation(spectrum),pesto.spin.median(spectrum)
		deviation = np.abs(median-spectrum['data'])/stdev
		despiked=copy.deepcopy(spectrum)
		despiked['data'][deviation>(toleranceFactor)]=np.NaN
		return despiked



#----------------------------
# Mainly intended as an internal function

def median(spectrum):
	assert('MeasurementType' in spectrum['Metadata']), "The input spectrum doesn't contain a 'MeasurementType' field in its Metadata, so I'm not sure what it is"
	assert(spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC","Spin Image"]), "This is the wrong type of spectrum for this function, expecting the MeasurementType field to be one of ('Spin EDC','Spin MDC', or 'Spin Image')"

	if spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC"]:

		positive_median=np.zeros((len(spectrum['Axis'][0])),np.float32)
		negative_median=np.zeros((len(spectrum['Axis'][0])),np.float32)

		median = np.zeros((len(spectrum['Axis'][0]),len(spectrum['Axis'][1])),np.float32)

		for scanPointIndex,scanPoint in enumerate(spectrum['Axis'][0]): #For every energy 
			coilPlusDatapoints=[]
			coilMinusDatapoints=[]

			for stepIndex,step in enumerate(spectrum['Axis'][1]): # For every coil polarity step

				datapoint = spectrum['data'][scanPointIndex,stepIndex]
				if spectrum['Metadata']['CoilPolarity'][stepIndex]=='Positive': 
					coilPlusDatapoints.append((datapoint if not math.isnan(datapoint) else math.nan))
				else: coilMinusDatapoints.append((datapoint if not math.isnan(datapoint) else math.nan))

			positive_median[scanPointIndex] = np.median(coilPlusDatapoints)
			negative_median[scanPointIndex] = np.median(coilMinusDatapoints)

		for ii,scanPoint in enumerate(spectrum['Axis'][0]):
			for jj,step in enumerate(spectrum['Axis'][1]):
				if spectrum['Metadata']['CoilPolarity'][jj]=='Positive': median[ii,jj]=positive_median[ii]
				else: median[ii,jj]=negative_median[ii]

		return median

	elif spectrum['Metadata']['MeasurementType'] in ["Spin Image"]:

		positive_median=np.zeros((len(spectrum['Axis'][0]),len(spectrum['Axis'][1])),np.float32)
		negative_median=np.zeros((len(spectrum['Axis'][0]),len(spectrum['Axis'][1])),np.float32)

		median = np.zeros((len(spectrum['Axis'][0]),len(spectrum['Axis'][1]),len(spectrum['Axis'][2])),np.float32)

		for ii in range(len(spectrum['Axis'][0])): #For every energy 
			for jj in range(len(spectrum['Axis'][1])): #For every angle 
				coilPlusDatapoints=[]
				coilMinusDatapoints=[]

				for stepIndex,step in enumerate(spectrum['Axis'][2]): # For every coil polarity step
					datapoint = spectrum['data'][ii,jj,stepIndex]

					if spectrum['Metadata']['CoilPolarity'][stepIndex]=='Positive': 
						coilPlusDatapoints.append((datapoint if not math.isnan(datapoint) else math.NaN))
					else: coilMinusDatapoints.append((datapoint if not math.isnan(datapoint) else math.NaN))

				positive_median[ii,jj] = np.median(coilPlusDatapoints)
				negative_median[ii,jj] = np.median(coilMinusDatapoints)

		for ii in range(len(spectrum['Axis'][0])): #For every energy 
			for jj in range(len(spectrum['Axis'][1])): #For every angle 
				for kk,step in enumerate(spectrum['Axis'][2]): # For every coil polarity step
					if spectrum['Metadata']['CoilPolarity'][kk]=='Positive':
						median[ii,jj,kk]=positive_median[ii,jj]
					else:
						median[ii,jj,kk]=negative_median[ii,jj]

		return median


def standardDeviation(spectrum):
	assert(spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC","Spin Image"]), "This is the wrong type of spectrum for this function, expecting the MeasurementType field to be one of ('Spin EDC','Spin MDC', or 'Spin Image')"

	if spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC"]:

		positive_stdev=np.zeros((len(spectrum['Axis'][0])),np.float32)
		negative_stdev=np.zeros((len(spectrum['Axis'][0])),np.float32)

		stdev = np.zeros((len(spectrum['Axis'][0]),len(spectrum['Axis'][1])),np.float32)

		for scanPointIndex,scanPoint in enumerate(spectrum['Axis'][0]): #For every energy 
			coilPlusDatapoints=[]
			coilMinusDatapoints=[]

			for stepIndex,step in enumerate(spectrum['Axis'][1]): # For every coil polarity step

				datapoint = spectrum['data'][scanPointIndex,stepIndex]
				if spectrum['Metadata']['CoilPolarity'][stepIndex]=='Positive': 
					coilPlusDatapoints.append((datapoint if not math.isnan(datapoint) else math.nan))
				else: coilMinusDatapoints.append((datapoint if not math.isnan(datapoint) else math.nan))

			
			positive_stdev[scanPointIndex]=np.std(coilPlusDatapoints)
			negative_stdev[scanPointIndex]=np.std(coilMinusDatapoints)

		for ii,scanPoint in enumerate(spectrum['Axis'][0]):
			for jj,step in enumerate(spectrum['Axis'][1]):
				if spectrum['Metadata']['CoilPolarity'][jj]=='Positive':
					stdev[ii,jj]=positive_stdev[ii]
				else:
					stdev[ii,jj]=negative_stdev[ii]

		return stdev

	elif spectrum['Metadata']['MeasurementType'] in ["Spin Image"]:

		positive_stdev=np.zeros((len(spectrum['Axis'][0]),len(spectrum['Axis'][1])),np.float32)
		negative_stdev=np.zeros((len(spectrum['Axis'][0]),len(spectrum['Axis'][1])),np.float32)

		stdev = np.zeros((len(spectrum['Axis'][0]),len(spectrum['Axis'][1]),len(spectrum['Axis'][2])),np.float32)



		# THIS PROBABLY DOESNT NEED TO ITERATE OVER ENERGY!!!!!!!!
		# ------- To be optimized --------------
		for ii in range(len(spectrum['Axis'][0])): #For every energy 
			for jj in range(len(spectrum['Axis'][1])): #For every angle 
				coilPlusDatapoints=[]
				coilMinusDatapoints=[]

				for stepIndex,step in enumerate(spectrum['Axis'][2]): # For every coil polarity step
					datapoint = spectrum['data'][ii,jj,stepIndex]

					if spectrum['Metadata']['CoilPolarity'][stepIndex]=='Positive': 
						coilPlusDatapoints.append((datapoint if not math.isnan(datapoint) else math.NaN))
					else: coilMinusDatapoints.append((datapoint if not math.isnan(datapoint) else math.NaN))

				positive_stdev[ii,jj]=np.std(coilPlusDatapoints)
				negative_stdev[ii,jj]=np.std(coilMinusDatapoints)


		for ii in range(len(spectrum['Axis'][0])): #For every energy 
			for jj in range(len(spectrum['Axis'][1])): #For every angle 
				for kk,step in enumerate(spectrum['Axis'][2]): # For every coil polarity step
					if spectrum['Metadata']['CoilPolarity'][kk]=='Positive':
						stdev[ii,jj,kk]=positive_stdev[ii,jj]
					else:
						stdev[ii,jj,kk]=negative_stdev[ii,jj]

		# ------- To be optimized --------------
		return stdev




def separateByPolarity(spectrum):
	try: 
		if spectrum.endswith(".xy"): spectrum=pesto.loadSpectrum(spectrum,beQuiet=True)
	except: pass

	if 'MeasurementType' in spectrum['Metadata']:
		if spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC"]:

			polarityMatrix = spectrum['Metadata']['CoilPolarity']
			energyAxis = spectrum['Axis'][0]
			stepAxis = spectrum['Axis'][1]			

			# Shortcut way of preparing new spectrum dictionaries that inherit the axes and metadata. We'll overwrite the data field
			numPositiveScans = int((spectrum['Metadata']['CoilPolarity']=="Positive").sum())
			positive=copy.deepcopy(spectrum)
			positive['data']=np.zeros((len(energyAxis),numPositiveScans))
			positive['Axis'][1]=np.zeros((numPositiveScans))
			positive['Metadata']=copy.deepcopy(spectrum['Metadata'])
			positive['Metadata']['CoilPolarity']=["Positive" for ii in range(numPositiveScans)]

			numNegativeScans = int((spectrum['Metadata']['CoilPolarity']=="Negative").sum())
			negative=copy.deepcopy(spectrum)
			negative['data']=np.zeros((len(energyAxis),numNegativeScans))
			positive['Axis'][1]=np.zeros((numNegativeScans))
			negative['Metadata']=copy.deepcopy(spectrum['Metadata'])
			negative['Metadata']['CoilPolarity']=["Positive" for ii in range(numNegativeScans)]


			positiveIndex,negativeIndex=0,0
			for stepIndex,stepNumber in enumerate(stepAxis):
				if polarityMatrix[stepIndex]=='Positive':
					positive['data'][:,positiveIndex]=spectrum['data'][:,stepIndex]
					positiveIndex+=1
				if polarityMatrix[stepIndex]=='Negative':
					negative['data'][:,negativeIndex]=spectrum['data'][:,stepIndex]
					negativeIndex+=1


		elif spectrum['Metadata']['MeasurementType'] in ["Spin Image"]:
			polarity = spectrum['Metadata']['CoilPolarity']
			energyAxis = spectrum['Axis'][0]
			angleAxis = spectrum['Axis'][1]
			stepAxis = spectrum['Axis'][2]		

			numPositiveScans = int((spectrum['Metadata']['CoilPolarity']=="Positive").sum())

			# Shortcut way of preparing new spectrum dictionaries that inherit the axes and metadata. We'll overwrite the data field
			positive=copy.deepcopy(spectrum)
			positive['data']=np.zeros((len(energyAxis),len(angleAxis),numPositiveScans))
			positive['Axis'][2]=np.zeros((numPositiveScans))
			positive['Metadata']=copy.deepcopy(spectrum['Metadata'])
			positive['Metadata']['CoilPolarity']=np.array(["Positive" for ii in range(numPositiveScans)])

			numNegativeScans = int((spectrum['Metadata']['CoilPolarity']=="Negative").sum())

			negative=copy.deepcopy(spectrum)
			negative['data']=np.zeros((len(energyAxis),len(angleAxis),numNegativeScans))
			negative['Axis'][2]=np.zeros((numNegativeScans))
			negative['Metadata']=copy.deepcopy(spectrum['Metadata'])
			negative['Metadata']['CoilPolarity']=np.array(["Negative" for ii in range(numNegativeScans)])

			positiveIndex,negativeIndex=0,0
			for stepIndex,stepNumber in enumerate(stepAxis):
				if polarity[stepIndex]=='Positive':
					positive['data'][:,:,positiveIndex]=spectrum['data'][:,:,stepIndex]
					positiveIndex+=1
				if polarity[stepIndex]=='Negative':
					negative['data'][:,:,negativeIndex]=spectrum['data'][:,:,stepIndex]
					negativeIndex+=1



		elif spectrum['Metadata']['MeasurementType'] in ["Spin energy surface"]:
			polarityMatrix = spectrum['Metadata']['CoilPolarity']
			majorAxis = spectrum['Axis'][0]
			minorAxis = spectrum['Axis'][1]
			stepAxis = spectrum['Axis'][2]		

			
			numPositiveScans = int((spectrum['Metadata']['CoilPolarity']=="Positive").sum() / (len(spectrum['Axis'][0])*len(spectrum['Axis'][1])))

			# Shortcut way of preparing new spectrum dictionaries that inherit the axes and metadata. We'll overwrite the data field
			positive=copy.deepcopy(spectrum)
			positive['data']=np.zeros((len(majorAxis),len(minorAxis),numPositiveScans))
			positive['Axis'][2]=np.zeros((numPositiveScans))
			positive['Metadata']=copy.deepcopy(spectrum['Metadata'])
			positive['Metadata']['CoilPolarity']=np.array(["Positive" for ii in range(numPositiveScans)])

			numNegativeScans = int((spectrum['Metadata']['CoilPolarity']=="Negative").sum() / (len(spectrum['Axis'][0])*len(spectrum['Axis'][1])))

			negative=copy.deepcopy(spectrum)
			negative['data']=np.zeros((len(majorAxis),len(minorAxis),numNegativeScans))
			negative['Axis'][2]=np.zeros((numNegativeScans))
			negative['Metadata']=copy.deepcopy(spectrum['Metadata'])
			negative['Metadata']['CoilPolarity']=np.array(["Negative" for ii in range(numNegativeScans)])



			for majorIndex,majorAngle in enumerate(majorAxis):
				for minorIndex,minorAngle in enumerate(minorAxis):
					positiveIndex,negativeIndex=0,0
					for stepIndex,stepNumber in enumerate(stepAxis):
						if polarityMatrix[majorIndex][minorIndex][stepIndex]=='Positive':
							positive['data'][majorIndex,minorIndex,positiveIndex]=spectrum['data'][majorIndex,minorIndex,stepIndex]
							positiveIndex+=1
						elif polarityMatrix[majorIndex][minorIndex][stepIndex]=='Negative':
							negative['data'][majorIndex,minorIndex,negativeIndex]=spectrum['data'][majorIndex,minorIndex,stepIndex]
							negativeIndex+=1

		return positive,negative


def sum(spectrum):
	try: 
		if spectrum.endswith(".xy"): spectrum=pesto.loadSpectrum(spectrum,beQuiet=True)
	except: pass

	pos,neg = separateByPolarity(spectrum)

	if 'MeasurementType' in spectrum['Metadata']:
		if spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC"]:
			posSum=pesto.getProfile(spectrum,samplingAxis='y',beQuiet=True)
			posSum['data']=np.nansum(pos['data'],axis=1)
			negSum=pesto.getProfile(spectrum,samplingAxis='y',beQuiet=True)
			negSum['data']=np.nansum(neg['data'],axis=1)	

		elif spectrum['Metadata']['MeasurementType'] in ["Spin Image","Spin energy surface"]:
			posSum=pesto.getSlice(pos,axis=2,axisValue=0,beQuiet=True)
			posSum['data']=np.nansum(pos['data'],axis=2)
			posSum['Metadata']['MeasurementType']=""
			negSum=pesto.getSlice(neg,axis=2,axisValue=0,beQuiet=True)
			negSum['data']=np.nansum(neg['data'],axis=2)	
			negSum['Metadata']['MeasurementType']=""
		else:
			print("I'm sorry, I don't know how to do this operation on the spectrum you provided")
			return 0
	else:
		print("I'm sorry, I couldn't find a 'MeasurementType' field in metadata to know what this is")
		return 0	
	
	total = copy.deepcopy(posSum)
	total['data']=posSum['data']+negSum['data']
	return posSum,negSum,total



def average(spectrum):
	try: 
		if spectrum.endswith(".xy"): spectrum=pesto.loadSpectrum(spectrum,beQuiet=True)
	except: pass

	pos,neg = separateByPolarity(spectrum)

	if 'MeasurementType' in spectrum['Metadata']:
		if spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC"]:
			posAvg=pesto.getProfile(spectrum,samplingAxis='y',beQuiet=True)
			posAvg['data']=np.nanmean(pos['data'],axis=1)
			negAvg=pesto.getProfile(spectrum,samplingAxis='y',beQuiet=True)
			negAvg['data']=np.nanmean(neg['data'],axis=1)	

		elif spectrum['Metadata']['MeasurementType'] in ["Spin Image","Spin energy surface"]:
			posAvg=pesto.getSlice(pos,axis=2,axisValue=0,beQuiet=True)
			posAvg['data']=np.nanmean(pos['data'],axis=2)
			posAvg['Metadata']['MeasurementType']=""
			negAvg=pesto.getSlice(neg,axis=2,axisValue=0,beQuiet=True)
			negAvg['data']=np.nanmean(neg['data'],axis=2)	
			negAvg['Metadata']['MeasurementType']=""
		else:
			print("I'm sorry, I don't know how to do this operation on the spectrum you provided")
			return 0
	else:
		print("I'm sorry, I couldn't find a 'MeasurementType' field in metadata to know what this is")
		return 0	
	
	return posAvg,negAvg


def asymmetry(spectrum):
	try: 
		if spectrum.endswith(".xy"): spectrum=pesto.loadSpectrum(spectrum,beQuiet=True)
	except: pass


	if 'MeasurementType' in spectrum['Metadata']:
		if spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC"]:
			posAvg,negAvg = average(spectrum)
			posSum,negSum,total = sum(spectrum)
			asymmetry=pesto.getProfile(spectrum,samplingAxis='y',beQuiet=True)
			asymmetry['data']=(posAvg['data']-negAvg['data'])/(posAvg['data']+negAvg['data'])
			asymmetry['errorbars'] = np.sqrt(1/total['data'])
			return asymmetry

		elif spectrum['Metadata']['MeasurementType'] in ["Spin Image","Spin energy surface"]:
			posAvg,negAvg = average(spectrum)
			posSum,negSum,total = sum(spectrum)
			asymmetry=pesto.getSlice(spectrum,axis=2,axisValue=0,beQuiet=True)
			asymmetry['data']=(posAvg['data']-negAvg['data'])/(posAvg['data']+negAvg['data'])
			asymmetry['errorbars'] = np.sqrt(1/total['data'])
			asymmetry['Metadata']=copy.deepcopy(spectrum['Metadata'])
			asymmetry['Metadata']['MeasurementType']=""
			return asymmetry


		else:
			print("I'm sorry, I don't know how to do this operation on the spectrum you provided")
			return 0
	else:
		print("I'm sorry, I couldn't find a 'MeasurementType' field in metadata to know what this is")
		return 0		

def polarization(c2rp=None,c2rm=None,c1=None,sherman=0.29,polar_offset=0):
	if c2rp is not None and c2rm is not None:
		try: 
			if c2rp.endswith(".xy"): c2rp=pesto.loadSpectrum(c2rp,beQuiet=True)
		except: pass
		try: 
			if c2rm.endswith(".xy"): c2rm=pesto.loadSpectrum(c2rm,beQuiet=True)
		except: pass

		if 'MeasurementType' in c2rp['Metadata']:
			if c2rp['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC","Spin Image","Spin energy surface"]:

				a1=asymmetry(c2rp)
				a2=asymmetry(c2rm)
				ii = sum(c2rp)[2]
				kk = sum(c2rm)[2]
				pxpy_sumcounts=copy.deepcopy(ii)
				pxpy_sumcounts['data']=ii['data']+kk['data']

				px={}
				px['Axis']=a1['Axis']
				px['AxisLabel']=a1['AxisLabel']
				px['AxisUnits']=a1['AxisUnits']
				px['data']=np.array([math.sqrt(2)*(ii-jj)/(2*sherman) for ii,jj in zip(a1['data'],a2['data'])])
				px['Metadata']={}
				px['errorbars']=math.sqrt(2)*np.sqrt(1/(pxpy_sumcounts['data'] * sherman**2))

				py={}
				py['Axis']=a1['Axis']
				py['AxisLabel']=a1['AxisLabel']
				py['AxisUnits']=a1['AxisUnits']
				py['data']=np.array([-math.sqrt(2)*(ii+jj)/(2*sherman) for ii,jj in zip(a1['data'],a2['data'])])
				py['Metadata']={}
				py['errorbars']=math.sqrt(2)*np.sqrt(1/(pxpy_sumcounts['data'] * sherman**2))

	else:
		px,py=None,None

	if c1 is not None: 
		try:
			if c1.endswith(".xy"): c1=pesto.loadSpectrum(c1,beQuiet=True)
		except: pass
		if c1['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC","Spin Image","Spin energy surface"]:
			a3=asymmetry(c1)
			pz_sumcounts = sum(c1)[2]
			pz={}
			pz['Axis']=a3['Axis']
			pz['AxisLabel']=a3['AxisLabel']
			pz['AxisUnits']=a3['AxisUnits']
			pz['data']=np.array([(ii)/sherman for ii in a3['data']])
			pz['Metadata']={}
			pz['errorbars']=np.sqrt(1/(pz_sumcounts['data'] * sherman**2))

	else:
		pz=None

	if polar_offset!=0:
		px_corrected=px['data']*np.cos(np.radians(polar_offset)) + pz['data']*np.sin(np.radians(polar_offset))
		pz_corrected=pz['data']*np.cos(np.radians(polar_offset)) - px['data']*np.sin(np.radians(polar_offset))

		px['data']=px_corrected
		pz['data']=pz_corrected
	return px,py,pz	

def componentIntensity(c2rp=None,c2rm=None,c1=None,sherman=0.29,polar_offset=0):
	px,py,pz = polarization(c2rp=c2rp,c2rm=c2rm,c1=c1,sherman=sherman,polar_offset=polar_offset)

	c2rp_sum,c2rm_sum,c1_sum = None,None,None
	nx_plus,nx_minus,ny_plus,ny_minus,nz_plus,nz_minus,totalCounts=None,None,None,None,None,None,None
	if px is not None:
		totalCounts = copy.deepcopy(px)
		measurementType = c2rp['Metadata']['MeasurementType']
	elif pz is not None:
		totalCounts = copy.deepcopy(pz)
		measurementType = c1['Metadata']['MeasurementType']
	else:
		print("Wasn't able to calculate a polarization from the input given")
		return 0
	totalCounts['data']=0

	if measurementType in ["Spin EDC","Spin MDC"]:
		if c2rp is not None and c2rm is not None:
			c2rp_sum = sum(c2rp)[2]
			totalCounts['data']+=c2rp_sum['data']
			c2rm_sum = sum(c2rm)[2]
			totalCounts['data']+=c2rm_sum['data']
		if c1 is not None:
			c1_sum = sum(c1)[2]
			totalCounts['data']+=c1_sum['data']

		if px is not None and py is not None:
			nx_plus={}
			nx_plus['Axis'] = px['Axis']
			nx_plus['AxisLabel'] = px['AxisLabel']
			nx_plus['AxisUnits'] = px['AxisUnits']
			nx_plus['Metadata'] = {}
			nx_plus['data']=np.zeros(np.shape(px['data']))
			nx_minus= copy.deepcopy(nx_plus)		
			ny_plus = copy.deepcopy(nx_plus)
			ny_minus= copy.deepcopy(nx_plus)	
			
			nx_plus['data'] = (totalCounts['data']) * (1+px['data'])
			nx_minus['data'] = (totalCounts['data']) * (1-px['data'])

			ny_plus['data'] = (totalCounts['data']) * (1+py['data'])
			ny_minus['data'] = (totalCounts['data']) * (1-py['data'])
		else:
			nx_plus,nx_minus,ny_plus,ny_plus=None,None,None,None

		if pz is not None:
			nz_plus={}
			nz_plus['Axis'] = pz['Axis']
			nz_plus['AxisLabel'] = pz['AxisLabel']
			nz_plus['AxisUnits'] = pz['AxisUnits']
			nz_plus['Metadata'] = {}
			nz_plus['data']=np.zeros(np.shape(pz['data']))
			nz_plus = copy.deepcopy(nz_plus)
			nz_minus= copy.deepcopy(nz_plus)	
			nz_plus['data'] = (totalCounts['data']) * (1+pz['data'])
			nz_minus['data'] = (totalCounts['data']) * (1-pz['data'])
		else:
			nz_plus,nz_minus=None,None

	if measurementType in ["Spin Image","Spin energy surface"]:
		if c2rp is not None and c2rm is not None:
			c2rp_sum = sum(c2rp)[2]
			totalCounts['data']+=c2rp_sum['data']
			c2rm_sum = sum(c2rm)[2]
			totalCounts['data']+=c2rm_sum['data']
		if c1 is not None:
			c1_sum = sum(c1)[2]
			totalCounts['data']+=c1_sum['data']

		if px is not None and py is not None:
			nx_plus={}
			nx_plus['Axis'] = px['Axis']
			nx_plus['AxisLabel'] = px['AxisLabel']
			nx_plus['AxisUnits'] = px['AxisUnits']
			nx_plus['Metadata'] = {}
			nx_plus['data']=np.zeros(np.shape(px['data']))
			nx_minus= copy.deepcopy(nx_plus)		
			ny_plus = copy.deepcopy(nx_plus)
			ny_minus= copy.deepcopy(nx_plus)	
			
			nx_plus['data'] = (totalCounts['data']) * (1+px['data'])
			nx_minus['data'] = (totalCounts['data']) * (1-px['data'])

			ny_plus['data'] = (totalCounts['data']) * (1+py['data'])
			ny_minus['data'] = (totalCounts['data']) * (1-py['data'])
		else:
			nx_plus,nx_minus,ny_plus,ny_plus=None,None,None,None

		if pz is not None:
			nz_plus={}
			nz_plus['Axis'] = pz['Axis']
			nz_plus['AxisLabel'] = pz['AxisLabel']
			nz_plus['AxisUnits'] = pz['AxisUnits']
			nz_plus['Metadata'] = {}
			nz_plus['data']=np.zeros(np.shape(pz['data']))
			nz_plus = copy.deepcopy(nz_plus)
			nz_minus= copy.deepcopy(nz_plus)	
			nz_plus['data'] = (totalCounts['data']) * (1+pz['data'])
			nz_minus['data'] = (totalCounts['data']) * (1-pz['data'])
		else:
			nz_plus,nz_minus=None,None		

	return nx_plus,nx_minus,ny_plus,ny_minus,nz_plus,nz_minus,totalCounts

def quickSummary(c2rp=None,c2rm=None,c1=None,hv=None,sherman=0.29,polarizationMax=1,componentMax=None,polar_offset=0):

	if c2rp is not None:
		measurementType = c2rp['Metadata']['MeasurementType']
	elif c1 is not None:
		measurementType = c1['Metadata']['MeasurementType']
	else:
		print("Wasn't able to identify the measurement type from the input provided")
		return

	px,py,pz=polarization(c2rp,c2rm,c1,sherman=sherman,polar_offset=polar_offset)
	nx_plus,nx_minus,ny_plus,ny_minus,nz_plus,nz_minus,totalCounts=componentIntensity(c2rp,c2rm,c1,sherman=sherman,polar_offset=polar_offset)

	nrows = 0
	if px is not None: nrows+=1
	if py is not None: nrows+=1
	if pz is not None: nrows+=1

	if measurementType in ["Spin EDC","Spin MDC"]:

		fig,axes=plt.subplots(figsize=[12,3.5*nrows],nrows=nrows,ncols=3,squeeze=False)
		p_index=0
		if px is not None:		
			ax=axes[p_index][0]
			pesto.quickPlot(totalCounts,axis=ax,color='black',hv=hv)
			ax.set_title("Total intensity")

			ax=axes[p_index][1]
			pesto.quickPlot(px,axis=ax,color='black',hv=hv,errorbars=True,alpha=0.3)
			ax.axhline(y=0,ls='--',color='black')
			ax.set_ylim([-polarizationMax,polarizationMax])
			ax.set_title("Px")

			ax=axes[p_index][2]
			pesto.quickPlot(nx_plus,axis=ax,color='tab:red',hv=hv,filled=True,alpha=0.5)
			pesto.quickPlot(nx_minus,axis=ax,color='tab:blue',hv=hv,filled=True,alpha=0.5)
			ax.set_title("Px components")
			p_index+=1

		if py is not None:		
			ax=axes[p_index][0]
			pesto.quickPlot(totalCounts,axis=ax,color='black',hv=hv)
			ax.set_title("Total intensity")

			ax=axes[p_index][1]
			pesto.quickPlot(py,axis=ax,color='black',hv=hv,errorbars=True,alpha=0.3)
			ax.axhline(y=0,ls='--',color='black')
			ax.set_ylim([-polarizationMax,polarizationMax])
			ax.set_title("Py")

			ax=axes[p_index][2]
			pesto.quickPlot(ny_plus,axis=ax,color='tab:red',hv=hv,filled=True,alpha=0.5)
			pesto.quickPlot(ny_minus,axis=ax,color='tab:blue',hv=hv,filled=True,alpha=0.5)
			ax.set_title("Py components")
			p_index+=1

		if pz is not None:		
			ax=axes[p_index][0]
			pesto.quickPlot(totalCounts,axis=ax,color='black',hv=hv)
			ax.set_title("Total intensity")

			ax=axes[p_index][1]
			pesto.quickPlot(pz,axis=ax,color='black',hv=hv,errorbars=True,alpha=0.3)
			ax.axhline(y=0,ls='--',color='black')
			ax.set_ylim([-polarizationMax,polarizationMax])
			ax.set_title("Pz")

			ax=axes[p_index][2]
			pesto.quickPlot(nz_plus,axis=ax,color='tab:red',hv=hv,filled=True,alpha=0.5)
			pesto.quickPlot(nz_minus,axis=ax,color='tab:blue',hv=hv,filled=True,alpha=0.5)
			ax.set_title("Pz components")
			p_index+=1


		plt.tight_layout()

		plt.show()

	elif measurementType in ["Spin Image","Spin energy surface"]:
		fig,axes=plt.subplots(figsize=[12,3.5*nrows],nrows=nrows,ncols=3,squeeze=False)
		p_index=0

		if px is not None:
			ax=axes[p_index][0]
			pesto.quickPlot(totalCounts,axis=ax,hv=hv)
			ax.set_title("Total intensity")

			ax=axes[p_index][1]
			im=pesto.quickPlot(px,axis=ax,cmap='bwr',hv=hv,cmax=polarizationMax,cmin=-polarizationMax,returnIm=True)
			plt.colorbar(im)
			ax.set_title("Px")

			ax=axes[p_index][2]
			component = copy.deepcopy(nx_plus)
			component['data']-=nx_minus['data']
			if componentMax==None: im=pesto.quickPlot(component,cmap='bwr',cmax=np.nanmax(component['data']),cmin=-np.nanmax(component['data']),axis=ax,hv=hv,returnIm=True)
			else: im=pesto.quickPlot(component,cmap='bwr',cmax=componentMax,cmin=-componentMax,axis=ax,hv=hv,returnIm=True)
			plt.colorbar(im)
			ax.set_title("Px component intensity")
			p_index+=1

		if py is not None:
			ax=axes[p_index][0]
			pesto.quickPlot(totalCounts,axis=ax,hv=hv)
			ax.set_title("Total intensity")

			ax=axes[p_index][1]
			im=pesto.quickPlot(py,axis=ax,cmap='bwr',hv=hv,cmax=polarizationMax,cmin=-polarizationMax,returnIm=True)
			plt.colorbar(im)
			ax.set_title("Py")

			ax=axes[p_index][2]
			component = copy.deepcopy(ny_plus)
			component['data']-=ny_minus['data']
			if componentMax==None: im=pesto.quickPlot(component,cmap='bwr',cmax=np.nanmax(component['data']),cmin=-np.nanmax(component['data']),axis=ax,hv=hv,returnIm=True)
			else: im=pesto.quickPlot(component,cmap='bwr',cmax=componentMax,cmin=-componentMax,axis=ax,hv=hv,returnIm=True)
			plt.colorbar(im)
			ax.set_title("Py component intensity")
			p_index+=1

		if pz is not None:
			ax=axes[p_index][0]
			pesto.quickPlot(totalCounts,axis=ax,hv=hv)
			ax.set_title("Total intensity")

			ax=axes[p_index][1]
			im=pesto.quickPlot(pz,axis=ax,cmap='bwr',hv=hv,cmax=polarizationMax,cmin=-polarizationMax,returnIm=True)
			plt.colorbar(im)
			ax.set_title("Pz")

			ax=axes[p_index][2]
			component = copy.deepcopy(nz_plus)
			component['data']-=nz_minus['data']
			if componentMax==None: im=pesto.quickPlot(component,cmap='bwr',cmax=np.nanmax(component['data']),cmin=-np.nanmax(component['data']),axis=ax,hv=hv,returnIm=True)
			else: im=pesto.quickPlot(component,cmap='bwr',cmax=componentMax,cmin=-componentMax,axis=ax,hv=hv,returnIm=True)
			plt.colorbar(im)
			ax.set_title("Pz component intensity")
			p_index+=1

		plt.tight_layout()

		plt.show()


