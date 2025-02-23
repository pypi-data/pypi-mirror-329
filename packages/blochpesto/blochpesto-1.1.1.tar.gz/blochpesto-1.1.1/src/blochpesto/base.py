ANALYZER_WORKFUNCTION = 4.34

from packaging.version import Version

try:	
	import matplotlib
	print("Using matplotlib\t{}".format(matplotlib.__version__))
	if Version(matplotlib.__version__) < Version("3.9.0"): pass
	else: print("(warning): matplotlib < 3.9.0 is required. Regress with 'pip uninstall matplotlib' followed by 'pip install \"matplotlib<3.9\"'".format(matplotlib.__version__))

except ImportError: print("\t(ERROR): Couldn't import the matplotlib module. This is required for basic functionality. Install it with the command 'pip install matplotlib'")

try:	
	import numpy as np
	print("Using numpy\t\t{}".format(np.__version__))
	if Version(np.__version__) < Version("2.0.0"): pass
	else: print("(warning): numpy < 2.0 is required. Regress with 'pip uninstall numpy' followed by 'pip install \"numpy<2.0\"'".format(np.__version__))

except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")


try:	import scipy
except ImportError: print("\t(Warning): Couldn't import the scipy module. This is required for basic functionality. Install it with the command 'pip install scipy'")

#import warnings
#warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

try:	
	import ipywidgets
	print("Using ipywidgets\t{}".format(ipywidgets.__version__))
	if Version(ipywidgets.__version__) >= Version("8.1.5"): pass
	else: print("(warning): ipywidgets >= 8.1.5 is required. Regress with 'pip uninstall ipywidgets' followed by 'pip install \"ipywidgets>=1.8.4\"'".format(ipywidgets.__version__))

except ImportError: print("\t(ERROR): Couldn't import the ipywidgets module. You will not be able to use any interactive functions")

try:	
	import ipympl
	print("Using ipympl\t\t{}".format(ipympl.__version__))
	if Version(ipympl.__version__) >= Version("0.9.3"): pass
	else: print("(warning): ipympl >= 0.9.3 is required. Regress with 'pip uninstall ipympl' followed by 'pip install \"ipympl>=0.9.3\"'".format(ipympl.__version__))

except ImportError: print("\t(ERROR): Couldn't import the ipympl module. You will not be able to use any interactive functions")


try: 	from lmfit import minimize, Parameters
except ImportError: print("\t(Warning): Couldn't import the lmfit module. Fermi edge fitting will not work. Install it from the terminal with the command 'pip install lmfit'")


import blochpesto as pesto
import blochpesto.spin
import blochpesto.interactive
import blochpesto.DFT
from .fileLoaders import *

import os,math,time,copy
import numpy as np




def getAnalyzerWorkFunction():
	return ANALYZER_WORKFUNCTION

def setAnalyzerWorkFunction(value):
	global ANALYZER_WORKFUNCTION
	ANALYZER_WORKFUNCTION=value

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


def transposeSpectrum(spectrum,a):
	assert(len(spectrum['Axis'])==len(a)), "The 'a' input doesn't match the axes of the input spectrum"

	spectrum['data']=spectrum['data'].transpose(a)
	
	spectrum['Axis']=[spectrum['Axis'][ii] for ii in a]
	spectrum['AxisLabel']=[spectrum['AxisLabel'][ii] for ii in a]
	spectrum['AxisUnits']=[spectrum['AxisUnits'][ii] for ii in a]

	
	return spectrum

def tree(spectrum,indentLevel=0):
	indentString=""
	for ii in range(indentLevel): indentString+="\t"
	if isinstance(spectrum,list):
		if len(spectrum)>0:
			if isinstance(spectrum[0],float): 
				print("{} {}".format(indentString,np.shape(spectrum))) 
			if isinstance(spectrum[0],list): 
				for ii in spectrum:
					print("{} {} [{} ... {}]".format(indentString,np.shape(ii),ii[0],ii[-1]))  
			if isinstance(spectrum[0],np.ndarray): 
				for ii in spectrum:
					print("{} {} [{} ... {}]".format(indentString,np.shape(ii),ii[0],ii[-1])) 
			if isinstance(spectrum[0],str): 
				for ii in spectrum:
					print("{} {}".format(indentString,ii)) 
	elif isinstance(spectrum,np.ndarray): 
		if len(np.shape(spectrum))==1:
			print("{} {} [{} ... {}]".format(indentString,np.shape(spectrum),spectrum[0],spectrum[-1])) 
		else:
			print("{} {}".format(indentString,np.shape(spectrum)))      
	else:
		for index,ii in enumerate(spectrum):
			if isinstance(spectrum,list) and isinstance(ii,str):
				print(indentString + "{}. [{}]".format(index,ii))
			elif isinstance(spectrum,list) and isinstance(ii,np.ndarray):
				print("{} {} [{} ... {}]".format(indentString,np.shape(ii),ii[0],ii[-1]))  
 
			elif isinstance(spectrum[ii],float) or isinstance(spectrum[ii],int) or isinstance(spectrum[ii],str):
				print(indentString + f"{ii:<25} [{spectrum[ii]}]")
			else:
				print("{} [{}] ({})".format(indentString,ii,type(spectrum[ii])))
				tree(spectrum[ii],indentLevel+1)
				


def loadSpectrum(fileName,**kwargs):

	defaultKwargs = {'beQuiet':False, 'regionIndex':1 ,'whichManipulatorAxis':'','mask':[]}
	kwargs = { **defaultKwargs, **kwargs }

	valid_kwargs = ['regionIndex','whichManipulatorAxis','mask','beQuiet']

	for k in kwargs:
		if not k in valid_kwargs:
			if not k in valid_kwargs:
				print("!! Invalid argument passed: '{}'' \n\nValid arguments are: {}".format(k,valid_kwargs))
				return

	supportedFormats=["SES .txt","SES .ibw","SES .pxt","SES .zip","Prodigy .sp2","Prodigy .itx","Prodigy .xy","i4 snapshot scanner .sr","Bloch .nxs","i05 .nxs","Bloch pickle"]
	

	if fileName.endswith(".sp2"): loadedSpectrum = Prodigy_sp2.load(fileName,**kwargs)
	elif fileName.endswith(".txt"): loadedSpectrum = SES_txt.load(fileName,**kwargs)			
	elif fileName.endswith(".ibw") or fileName.endswith(".pxt"): loadedSpectrum = SES_ibw.load(fileName,**kwargs)	
	elif fileName.endswith(".zip"): loadedSpectrum = SES_zip.load(fileName,**kwargs)
	elif fileName.endswith(".itx"): loadedSpectrum = Prodigy_itx.load(fileName,**kwargs)
	elif fileName.endswith(".xy"): loadedSpectrum = Prodigy_xy.load(fileName,**kwargs)
	elif fileName.endswith(".sr"): loadedSpectrum = i4_sr.load(fileName,**kwargs)
	elif fileName.endswith(".nxs"): loadedSpectrum = nxs.load(fileName,**kwargs)
	elif fileName.endswith(".pickle"): loadedSpectrum = Bloch_pickle.load(fileName,**kwargs)

	else:
		print("I don't know how to load this file. Currently supported formats are:")
		for ii in supportedFormats:
			print(ii)
		return

	if kwargs['beQuiet']==False: 
		try:
			printMetaData(spectrum=loadedSpectrum)
		except:
			pass

	return loadedSpectrum


def printMetaData(spectrum):

	if 'File Path' in spectrum['Metadata']: print("\nFile:\t\t{}".format(spectrum['Metadata']['File Path']))
	if 'Facility' in spectrum['Metadata']:  print("Measured at:\t{}".format(spectrum['Metadata']['Facility']))
	if 'Region Name' in spectrum['Metadata']: print("Region name:\t{}".format(spectrum['Metadata']['Region Name']))

	if 'SpectrumID' in spectrum['Metadata']: print("\nSpectrum ID:\t{}".format(spectrum['Metadata']['SpectrumID']))

	if 'Time' in spectrum['Metadata']: print("Acquired:\t{} {}".format(spectrum['Metadata']['Date'],spectrum['Metadata']['Time']))

	if all(x in spectrum['Metadata'] for x in ['Lens Mode','Pass Energy']): print("Settings:\t{}, Ep = {}eV".format(spectrum['Metadata']['Lens Mode'],spectrum['Metadata']['Pass Energy']))

	if 'Excitation Energy' in spectrum['Metadata']: print("Monochromator energy:\t{0:.2f} eV".format(spectrum['Metadata']['Excitation Energy']))


	try: print("XYZAPT:\t\t{} / {} / {} / {} / {} / {}".format(spectrum['Metadata']['Manipulator X'],
														  spectrum['Metadata']['Manipulator Y'],
														  spectrum['Metadata']['Manipulator Z'],
														  spectrum['Metadata']['Manipulator Azimuth'],
														  spectrum['Metadata']['Manipulator Polar'],
														  spectrum['Metadata']['Manipulator Tilt']))
	except KeyError: pass
	
	if len(np.shape(spectrum['data']))>1:
		if len(spectrum['Axis'][0])>1:
			print("Measured:\t{:.2f}eV..{:.2f}eV step {:.1f}meV".format(spectrum['Axis'][0][0],
																		spectrum['Axis'][0][-1],
																		(spectrum['Axis'][0][1]-spectrum['Axis'][0][0])*1000 ))
		else:
			print("Measured at fixed energy \t{:.2f}eV".format(spectrum['Axis'][0][0]))

	if len(np.shape(spectrum['data']))==1:
		print("Measured:\t{:.2f}eV..{:.2f}eV step {:.1f}meV".format(spectrum['Axis'][0],
																	spectrum['Axis'][-1],
																	(spectrum['Axis'][1]-spectrum['Axis'][0])*1000 ))

	if 'Number of Sweeps' in spectrum['Metadata']: print("Number of sweeps: ",spectrum['Metadata']['Number of Sweeps'])
	
	if 'Comments' in spectrum['Metadata']:
		if len(spectrum['Metadata']['Comments'])>0:
			print("Comments:\t{}".format(spectrum['Metadata']['Comments']))


	try:
		if spectrum['AxisLabel'][2]=="Photon energy":
			print("Photon energy:\t{:.2f}eV --> {:.2f}eV step {:.1f}eV".format(spectrum['Axis'][2][0],
																	spectrum['Axis'][2][-1],
																	(abs(spectrum['Axis'][2][1]-spectrum['Axis'][2][0]) )))
	except:
		pass 



def drawHighSymmetryLabels(points,axis):

	tform = matplotlib.transforms.blended_transform_factory(axis.transData, axis.transAxes)
	yMax,yMin = axis.get_ylim()[1],axis.get_ylim()[0]

	axisReversed=False
	xLeft,xRight = axis.get_xlim()[0],axis.get_xlim()[1]
	if xLeft>xRight: axisReversed=True

	if axisReversed==False:
		pointsWithinAxis = [x for x in points if (x[1]>=axis.get_xlim()[0] and x[1] <=axis.get_xlim()[1])]
		pointsOutsideLeft=[x for x in points if x[1]<axis.get_xlim()[0]]
		pointsOutsideRight=[x for x in points if x[1]>axis.get_xlim()[1]]
	else:
		pointsWithinAxis = [x for x in points if (x[1]>=axis.get_xlim()[1] and x[1] <=axis.get_xlim()[0])]
		pointsOutsideLeft=[x for x in points if x[1]>axis.get_xlim()[0]]
		pointsOutsideRight=[x for x in points if x[1]<axis.get_xlim()[1]]	

	for line in pointsWithinAxis:
		axis.plot([line[1],line[1]],[yMin,yMax],'--',color='black',lw=0.2)
		axis.text(x=line[1],y=1,s=line[0],va='bottom', ha='center',transform=tform)

	if len(pointsOutsideRight)>0: #Only draw the first point if there are severa
		axis.text(1,1,r"$ \rightarrow$"+pointsOutsideRight[0][0],ha='right', va='bottom',transform=axis.transAxes)

	if len(pointsOutsideLeft)>0:
		axis.text(0,1,pointsOutsideLeft[0][0]+r"$\leftarrow$",ha='left', va='bottom',transform=axis.transAxes)  	


def quickPlot(spectrum,**kwargs):

	defaultKwargs = { 'hv':None,'axis':None,'label':None,'cmap':'bone_r','cmin':None,
	'cmax':None,'lw':1,'color':None,'logscale':False,'beQuiet':True,'returnIm':None,'XPS':False,
	'errorbars':None,'filled':False,'alpha':1,'scatter':False }
	kwargs = { **defaultKwargs, **kwargs }

	valid_kwargs = ['cmax','hv','axis','label','cmap','cmin','cmax',
					'lw', 'color','logscale', 'XPS','returnIm','spinProjection',
					'filled','alpha','kPath','nkpnts','drawHighSymmetryLabels',
					'bandIndicesToPlot','Eb','errorbars','fillToZero','alpha','scatter','beQuiet']

	for k in kwargs:
		if not k in valid_kwargs:
			if not k in valid_kwargs:
				print("!! Invalid argument passed: '{}'' \n\nValid arguments are: {}".format(k,valid_kwargs))
				return

	try:
		if spectrum.endswith(".ibw") or spectrum.endswith(".txt") or spectrum.endswith(".itx") or spectrum.endswith(".xy"): spectrum=loadSpectrum(spectrum,beQuiet=True)
	except AttributeError: pass

	if spectrum is None:
		return
	#assert(len(np.shape(spectrum['data'])) < 3), "Expected a 1D or 2D spectrum as input"

	if kwargs['beQuiet']==False:
		printMetaData(spectrum)
	
	if 'isDFT' in spectrum['Metadata']:
		return pesto.DFT.quickPlot(spectrum=spectrum,**kwargs)

	if kwargs['XPS']==True:
		spectrum = getProfile(spectrum,samplingAxis='y',beQuiet=True)
	
	if 'MeasurementType' in spectrum['Metadata']:
		if spectrum['Metadata']['MeasurementType'] in ["Spin EDC","Spin MDC","Spin Image","Spin energy surface"]:
			return pesto.spin.quickPlot(spectrum=spectrum,**kwargs)

	# Line profiles

	if len(np.shape(spectrum['data']))==1:
		print("LINE PROFILE")
		x = spectrum['Axis']
		y = spectrum['data']
		if kwargs['errorbars'] is not None: 
			err=spectrum['errorbars']



		if kwargs['axis']==None: fig,ax=matplotlib.pyplot.subplots(figsize=(7,5))
		else: ax = kwargs['axis']


		#If the energy scale is kinetic BUT a photon energy was passed in, plot in binding energy
		if kwargs['hv'] is not None and spectrum['AxisLabel'].startswith("Kinetic"): 
			Eb = [kwargs['hv']-getAnalyzerWorkFunction()-ii for ii in x]
			if kwargs['errorbars'] is not None: ax.fill_between(Eb,y+err,y-err,lw=0,color=kwargs['color'],alpha=kwargs['alpha'])
			if kwargs['filled'] is True: im=ax.fill_between(Eb,y,0,color=kwargs['color'],alpha=kwargs['alpha'])
			
			im=ax.plot(Eb,y,label=kwargs['label'],lw=kwargs['lw'],color=kwargs['color'])
			ax.set_xlabel('Binding energy (eV)')	
			ax.set_xlim([max(Eb),min(Eb)])

		elif spectrum['AxisLabel'].startswith("Binding"): 
			Eb=spectrum['Axis']
			if kwargs['errorbars'] is not None: ax.fill_between(x,y+err,y-err,lw=0,color=kwargs['color'],alpha=kwargs['alpha'])
			if kwargs['filled'] is True: im=ax.fill_between(x,y,0,color=kwargs['color'],alpha=kwargs['alpha'])
			im=ax.plot(x,y,label=kwargs['label'],lw=kwargs['lw'],color=kwargs['color'])
			ax.set_xlabel(spectrum['AxisLabel'])
			ax.set_xlim([np.max(Eb),np.min(Eb)])		
		else:
			if kwargs['errorbars'] is True: ax.fill_between(x,y+err,y-err,lw=0,color=kwargs['color'],alpha=kwargs['alpha'])			
			if kwargs['filled'] is True: im=ax.fill_between(x,y,0,color=kwargs['color'],alpha=kwargs['alpha'])
			if kwargs['scatter'] is False:
				im=ax.plot(x,y,label=kwargs['label'],lw=kwargs['lw'],color=kwargs['color'])
			else:
				im=ax.scatter(x,y,label=kwargs['label'],color=kwargs['color'])
			ax.set_xlabel(spectrum['AxisLabel'])
			
		ax.set_ylabel('Intensity (a.u.)')

		if kwargs['logscale']==True:
			ax.set_yscale("log")
		if kwargs['axis']==None:
			matplotlib.pyplot.show()
		if kwargs['returnIm']==True: 
			return im
		return


	#--------------------------------
	# 2D images
	elif len(np.shape(spectrum['data']))==2:
		x = spectrum['Axis'][1]
		xstep = abs(spectrum['Axis'][1][1]-spectrum['Axis'][1][0])
		y = spectrum['Axis'][0]
		ystep = abs(spectrum['Axis'][0][1]-spectrum['Axis'][0][0])


		if kwargs['logscale']==True:
			image = np.log(copy.deepcopy(spectrum['data']))
		else:
			image=spectrum['data']
		if spectrum['AxisUnits'][0]==spectrum['AxisUnits'][1]: aspect='equal'
		else: aspect = 'auto'
		if spectrum['AxisLabel'][1] == 'Photon energy': aspect = 'auto' # You don't want equal aspect ratio in an Eb vs photon energy frame, despite having the same units

		if kwargs['axis']==None: fig,ax=matplotlib.pyplot.subplots(figsize=(7,5))
		else: ax = kwargs['axis']

		cmin,cmax,cmap=kwargs['cmin'],kwargs['cmax'],kwargs['cmap']

		if cmin!=None and cmax!=None:
			if cmin>cmax:
				cmin,cmax = cmax,cmin
				if cmap[-2:]=='_r':cmap=cmap[:-2]
				else:cmap=cmap+'_r'	

		hv,cmap = kwargs['hv'],kwargs['cmap']
		# Covert to Eb for the plot if requested and if the energy axis is not already converted
		if hv is not None and (spectrum['AxisLabel'][0].startswith("Kinetic") or spectrum['AxisLabel'][0].startswith("Ek")):  
			Eb = [hv-getAnalyzerWorkFunction()-ii for ii in y]
			im=ax.imshow(image,clim=[cmin,cmax],aspect=aspect,cmap=cmap,interpolation='none',extent=[x[0]-xstep/2,x[-1]+xstep/2,Eb[-1]+ystep/2,Eb[0]-ystep/2],alpha=kwargs['alpha'])
			ax.set_ylabel('Binding energy (eV)')	
			ax.invert_yaxis()
		elif hv is None and (spectrum['AxisLabel'][0].startswith("Kinetic") or spectrum['AxisLabel'][0].startswith("Ek")):  
			im=ax.imshow(image,clim=[cmin,cmax],aspect=aspect,cmap=cmap,interpolation='none',extent=[x[0]-xstep/2,x[-1]+xstep/2,y[-1]+ystep/2,y[0]-ystep/2],alpha=kwargs['alpha'])
			ax.set_ylabel("{} ({})".format(spectrum['AxisLabel'][0],spectrum['AxisUnits'][0]))
			ax.invert_yaxis()

		elif(spectrum['AxisLabel'][0].startswith("Binding") or spectrum['AxisLabel'][0].startswith("Eb")): 
			im=ax.imshow(image,clim=[cmin,cmax],aspect=aspect,cmap=cmap,interpolation='none',extent=[x[0]-xstep/2,x[-1]+xstep/2,y[-1]+ystep/2,y[0]-ystep/2],alpha=kwargs['alpha'])
			ax.set_ylabel("{} ({})".format(spectrum['AxisLabel'][0],spectrum['AxisUnits'][0]))
			ax.invert_yaxis()
		else:
			im=ax.imshow(image,clim=[cmin,cmax],aspect=aspect,cmap=cmap,interpolation='none',extent=[x[0]-xstep/2,x[-1]+xstep/2,y[-1]+ystep/2,y[0]-ystep/2],alpha=kwargs['alpha'])
			ax.set_ylabel("{} ({})".format(spectrum['AxisLabel'][0],spectrum['AxisUnits'][0]))
			#matplotlib.pyplot.locator_params(axis='x', nbins=5)

		
		ax.set_xlabel("{} ({})".format(spectrum['AxisLabel'][1],spectrum['AxisUnits'][1]))

		if kwargs['returnIm']==True: 
			return im
		else: 
			return

	else:
		print("quickPlot: Sorry, I don't know how to deal data types of 3+ dimensions")
	print("quickPlot: Fell through without returning?")
	
def normalize(spectrum):

	outputSpectrum=copy.deepcopy(spectrum)

	bg=np.min(spectrum['data'])
	amplitude=np.max(spectrum['data'])-bg
	outputSpectrum['data'] = (spectrum['data']-bg)/amplitude

	return outputSpectrum


























def getProfileArbitrary(spectrum,startPoint,endPoint,sliceIntegration=0,beQuiet=False):

	assert(len(np.shape(spectrum['data']))==2),"Expected a 2D input spectrum"
	assert(spectrum['AxisUnits'][0]==spectrum['AxisUnits'][1]),"Expected a spectrum where both dimensions have the same units - here you have {} and {}".format(spectrum['AxisUnits'][0],spectrum['AxisUnits'][1])

	# Given a point [x,y] and a line through it with slope [dX,dY], return the coordinates of a 
	# point a distance R from [x,y] along the perpendicular bisector of the line
	def getProfileArbitrary__getStartPoint(xy,dX,dY,R):
		if abs(dX)>0: angle = math.atan(dY/dX)
		else: angle=math.pi/2*np.copysign(1,dY)

		xoffset = -math.sin(angle)*R*np.copysign(-1,dX)
		yoffset = math.cos(angle)*R*np.copysign(-1,dX)

		xy = [xy[0]+xoffset,xy[1]+yoffset]

		return xy

	def getProfileArbitrary__pixel2data_coords(xy,xAxis,yAxis):
		x_axis_units_per_pixel= (xAxis[1]-xAxis[0])
		x = xy[0]
		x_axis_offset = xAxis[0]

		y_axis_units_per_pixel= (yAxis[1]-yAxis[0])
		y = xy[1]
		y_axis_offset = yAxis[0]

		return [(x*x_axis_units_per_pixel) + x_axis_offset, (y*y_axis_units_per_pixel) +y_axis_offset]



	def getProfileArbitrary__data2pixel_coords(xy,xAxis,yAxis):
		x_axis_units_per_pixel= (xAxis[1]-xAxis[0])
		x = xy[0]
		x_axis_offset = xAxis[0]

		y_axis_units_per_pixel= (yAxis[1]-yAxis[0])
		y = xy[1]
		y_axis_offset = yAxis[0]

		return [(x-x_axis_offset)*(1/x_axis_units_per_pixel),(y-y_axis_offset)*(1/y_axis_units_per_pixel)]


	yAxis=spectrum['Axis'][0]
	yAxisLabel = spectrum['AxisLabel'][0]
	xAxis=spectrum['Axis'][1]
	xAxisLabel = spectrum['AxisLabel'][1]
	sourceImage = spectrum['data']
	# -------------------------------------
	# Calculate the axis length of the output profile 
	
	startPoint_pix = getProfileArbitrary__data2pixel_coords(startPoint,xAxis,yAxis)
	endPoint_pix = getProfileArbitrary__data2pixel_coords(endPoint,xAxis,yAxis)

	if beQuiet==False: print("Primary slice starts at pixel coordinates [{:.1f},{:.1f}], ends at [{:.1f},{:.1f}]".format(startPoint_pix[0],startPoint_pix[1],endPoint_pix[0],endPoint_pix[1]))

	numpixels_x = abs(1+(endPoint_pix[0]-startPoint_pix[0]))
	numpixels_y = abs(1+(endPoint_pix[1]-startPoint_pix[1]))
	
	dest_numPixels = math.ceil(math.sqrt(numpixels_x**2 + numpixels_y**2))
	
	# What is the increment in X and Y per pixel of the sampling line?
	dX = (endPoint_pix[0]-startPoint_pix[0])/dest_numPixels
	dY = (endPoint_pix[1]-startPoint_pix[1])/dest_numPixels

	destProfile = np.zeros([dest_numPixels])
	
	# ------------------------------------------------
	# Calculate the span of the output slice in data coordinates
	
	dest_xrange=(startPoint[0]-endPoint[0]) 
	dest_yrange=(startPoint[1]-endPoint[1]) 

	dest_AxisRange = math.sqrt(dest_xrange**2 + dest_yrange**2)
	
	destProfile_Axis = np.linspace(0,dest_AxisRange,dest_numPixels)
	destProfile_Axis_step = destProfile_Axis[1]-destProfile_Axis[0]
	


	# ------------------------------------------------
	# Extract the destination profile out of the source image using bi-linear interpolation (since we 
	# will in general have non-integer indices)
	

	# Slice integration is specified in physical units, so first we need to decide the slice sampling density you need in order to 
	# not miss anything.
	#
	# A safe if inefficient approach is to just sample with the same density as the most dense axis, so that's what I'm doing.

	if sliceIntegration>0:
		maxDensity = 1/min((xAxis[1]-xAxis[0]),(yAxis[1]-yAxis[0]))
		numLines =math.ceil(sliceIntegration*maxDensity*0.5)
		if numLines<2:
			sliceIntegration=0
			numLines=1
			if beQuiet==False: print("Data density does not support such a small integration width, falling back to no integration")

	if sliceIntegration==0:
		for pixelindex in range(dest_numPixels):

			sourceX = startPoint_pix[0] + dX*pixelindex
			sourceY = startPoint_pix[1] + dY*pixelindex 

			xy = [sourceX,sourceY]


			# Bilinear interpolation
			r0 = math.floor(xy[1])
			r1 = r0 + 1   
			r0w=r1-xy[1]
			r1w=xy[1]-r0

			c0 = math.floor(xy[0])
			c1 = c0 + 1   
			c0w=c1-xy[0]
			c1w=xy[0]-c0

			interpolatedPoint=0
			if r0<len(yAxis) and c0<len(xAxis) and c1<len(xAxis):
				interpolatedPoint+=sourceImage[r0,c0]*r0w*c0w
				interpolatedPoint+=sourceImage[r0,c1]*r0w*c1w
			if r1<len(yAxis) and c0<len(xAxis) and c1<len(xAxis):
				interpolatedPoint+=sourceImage[r1,c0]*r1w*c0w
				interpolatedPoint+=sourceImage[r1,c1]*r1w*c1w

			destProfile[pixelindex] += interpolatedPoint 

	else:
		firstSliceStart,firstSliceEnd=0,0
		lastSliceStart,lastSliceEnd=0,0
		for ii in np.linspace(start=-sliceIntegration/2,stop=sliceIntegration/2,num=numLines,endpoint=True):
			for pixelindex in range(dest_numPixels):

				sourceX = startPoint_pix[0] + dX*pixelindex
				sourceY = startPoint_pix[1] + dY*pixelindex 

				sourceXY = getProfileArbitrary__pixel2data_coords([sourceX,sourceY],xAxis,yAxis) # Where you are along the main sampling line			

				xy = getProfileArbitrary__getStartPoint(xy=sourceXY,dX=dest_xrange,dY=dest_yrange,R=ii) # Where you are on one of the (parallel) integration lines

				if ii==-sliceIntegration/2 and pixelindex==0: 
					firstSliceStart=xy
					xy=getProfileArbitrary__data2pixel_coords(firstSliceStart,xAxis,yAxis)
	
				elif ii==sliceIntegration/2 and pixelindex==0: 
					lastSliceStart=xy
					xy=getProfileArbitrary__data2pixel_coords(lastSliceStart,xAxis,yAxis)

				else:
					xy=getProfileArbitrary__data2pixel_coords(xy,xAxis,yAxis)


				# Bilinear interpolation
				r0 = math.floor(xy[1])
				r1 = r0 + 1   
				r0w=r1-xy[1]
				r1w=xy[1]-r0

				c0 = math.floor(xy[0])
				c1 = c0 + 1   
				c0w=c1-xy[0]
				c1w=xy[0]-c0


				interpolatedPoint=0
				if r0<len(yAxis) and c0<len(xAxis) and c1<len(xAxis):
					interpolatedPoint+=sourceImage[r0,c0]*r0w*c0w
					interpolatedPoint+=sourceImage[r0,c1]*r0w*c1w
				if r1<len(yAxis) and c0<len(xAxis) and c1<len(xAxis):
					interpolatedPoint+=sourceImage[r1,c0]*r1w*c0w
					interpolatedPoint+=sourceImage[r1,c1]*r1w*c1w

				destProfile[pixelindex] += interpolatedPoint 

			if ii==-sliceIntegration/2: firstSliceEnd=[(xy[0]*(xAxis[1]-xAxis[0]))+xAxis[0],(xy[1]*(yAxis[1]-yAxis[0]))+yAxis[0]]
			if ii==sliceIntegration/2: lastSliceEnd=[(xy[0]*(xAxis[1]-xAxis[0]))+xAxis[0],(xy[1]*(yAxis[1]-yAxis[0]))+yAxis[0]]


		destProfile=destProfile/numLines

	outputSpectrum={}
	outputSpectrum['Metadata']={}
	outputSpectrum['Axis']=[]
	outputSpectrum['AxisLabel']=[""]
	outputSpectrum['AxisUnits']=[""]
	outputSpectrum['data']=destProfile
	outputSpectrum['Axis']=destProfile_Axis
	outputSpectrum['AxisLabel']=spectrum['AxisLabel'][0]
	outputSpectrum['AxisUnits']=spectrum['AxisUnits'][0]

	if beQuiet==False:


		fig,axes=matplotlib.pyplot.subplots(figsize=[12,5],ncols=2)

		# Left hand panel showing a constant energy cut and where the slice is being taken

		ax=axes[0]
		pesto.quickPlot(spectrum,axis=ax)
		ax.add_patch(matplotlib.patches.ConnectionPatch(xyA=startPoint,xyB=endPoint,coordsA="data",coordsB="data",color="tab:blue",lw=2,arrowstyle="-|>"))  
		
		if sliceIntegration>0:        
			ax.add_patch(matplotlib.patches.ConnectionPatch(xyA=firstSliceStart,xyB=firstSliceEnd,coordsA="data",coordsB="data",color="tab:orange",lw=1,arrowstyle="-"))  
			ax.add_patch(matplotlib.patches.ConnectionPatch(xyA=lastSliceStart,xyB=lastSliceEnd,coordsA="data",coordsB="data",color="tab:orange",lw=1,arrowstyle="-")) 
			ax.add_patch(matplotlib.patches.ConnectionPatch(xyA=lastSliceStart,xyB=firstSliceStart,coordsA="data",coordsB="data",color="tab:orange",lw=1,arrowstyle="-")) 
			ax.add_patch(matplotlib.patches.ConnectionPatch(xyA=lastSliceEnd,xyB=firstSliceEnd,coordsA="data",coordsB="data",color="tab:orange",lw=1,arrowstyle="-")) 

		ax=axes[1] #Right hand panel showing the extracted slice
		pesto.quickPlot(outputSpectrum,axis=ax)

		matplotlib.pyplot.tight_layout()
		matplotlib.pyplot.show()
	



	return outputSpectrum



























def getProfile(spectrum,samplingAxis='x',xAxisRange=[None,None],yAxisRange=[None,None],beQuiet=False):
	# Find the image coordinates closest to the x/y values you requested

	im = spectrum['data']
	assert(len(np.shape(im)) == 2), "Expected a 2D spectrum as input"
	assert(samplingAxis=='x' or samplingAxis=='X' or samplingAxis=='y' or samplingAxis=='Y'), "The axis parameter should be 'x' or 'y'"


	a=spectrum['Axis'][0]

	if yAxisRange[0] is None: yStartIndex,yStartVal=0,a[0]

	else:
		yStartIndex = indexOfClosestValue(a,yAxisRange[0])
		yStartVal = a[yStartIndex]

	if yAxisRange[1] is None: yStopIndex,yStopVal=len(a),a[-1]

	else:
		yStopIndex = indexOfClosestValue(a,yAxisRange[1])
		yStopVal = a[yStopIndex]

	if yStartVal>yStopVal:	yStartVal,yStopVal = yStopVal,yStartVal
	if yStartIndex>yStopIndex:	yStartIndex,yStopIndex = yStopIndex,yStartIndex	


	a=spectrum['Axis'][1]
	if xAxisRange[0] is None: xStartIndex,xStartVal=0,a[0]

	else:
		xStartIndex = indexOfClosestValue(a,xAxisRange[0])
		xStartVal = a[xStartIndex]

	if xAxisRange[1] is None: xStopIndex,xStopVal=len(a),a[-1]

	else:
		xStopIndex = indexOfClosestValue(a,xAxisRange[1])
		xStopVal = a[xStopIndex]

	if xStartVal>xStopVal:	xStartVal,xStopVal = xStopVal,xStartVal
	if xStartIndex>xStopIndex:	xStartIndex,xStopIndex = xStopIndex,xStartIndex	


	subImage = np.array(im)[yStartIndex:yStopIndex+1,xStartIndex:xStopIndex+1]

	if samplingAxis=='x' or samplingAxis=='X': 
		axis=0
		slice_intensity = np.sum(subImage,axis=0) 
	if samplingAxis=='y' or samplingAxis=='Y': 
		axis=1
		slice_intensity = np.sum(subImage,axis=1)

	slice_axis=[]
	if axis == 1: slice_axis=spectrum['Axis'][0][yStartIndex:yStopIndex+1]
	else: slice_axis=spectrum['Axis'][1][xStartIndex:xStopIndex+1]

	if beQuiet == False:
		fig,ax=matplotlib.pyplot.subplots(figsize=[10,4],ncols=2)
		quickPlot(spectrum,axis=ax[0])
		ROI = matplotlib.patches.Rectangle([xStartVal,yStartVal],  (xStopVal-xStartVal),(yStopVal-yStartVal),linewidth=1, edgecolor = 'r',facecolor='none')
		ax[0].add_patch(ROI)

	

	outputSpectrum={}
	outputSpectrum['Metadata']={}
	outputSpectrum['data']=slice_intensity
	outputSpectrum['Axis']=slice_axis
	if axis==0: 
		outputSpectrum['AxisLabel']=spectrum['AxisLabel'][1]
		outputSpectrum['AxisUnits']=spectrum['AxisUnits'][1]
	if axis==1:
		outputSpectrum['AxisLabel']=spectrum['AxisLabel'][0]
		outputSpectrum['AxisUnits']=spectrum['AxisUnits'][0]

	if beQuiet == False:
		quickPlot(outputSpectrum,axis=ax[1])
		matplotlib.pyplot.tight_layout()
		matplotlib.pyplot.show() 

	return outputSpectrum


def getSliceArbitrary(spectrum,startPoint,endPoint,sliceIntegration=0,beQuiet=False,previewEnergy=0):

	assert(len(np.shape(spectrum['data']))==3),"Expected a 3D input spectrum"
	assert(spectrum['AxisUnits'][1]==spectrum['AxisUnits'][2]),"Expected a spectrum where dimensions 1 and 2 have the same units - here you have {} and {}".format(spectrum['AxisUnits'][1],spectrum['AxisUnits'][2])

	# Given a point [x,y] and a line through it with slope [dX,dY], return the coordinates of a 
	# point a distance R from [x,y] along the perpendicular bisector of the line
	def getSliceArbitrary__getStartPoint(xy,dX,dY,R):
		# Note:
		# It took me quite a while to get this logic correct for non-zero slice integration, so it probably doesn't seem self explanatory.
		# it works (test it!) but I'm not clever enough to clearly explain the reasoning just at the moment.

		if abs(dX)>0: angle = math.atan(dY/dX)
		else: angle=math.pi/2*np.copysign(1,dY)

		xoffset = -math.sin(angle)*R*np.copysign(-1,dX)
		yoffset = math.cos(angle)*R*np.copysign(-1,dX)

		xy = [xy[0]+xoffset,xy[1]+yoffset]

		return xy

	def getSliceArbitrary__pixel2data_coords(xy,xAxis,yAxis):
		return [(xy[0]*(xAxis[1]-xAxis[0]))+xAxis[0],(xy[1]*(yAxis[1]-yAxis[0]))+yAxis[0]]


	def getSliceArbitrary__data2pixel_coords(xy,xAxis,yAxis):
		return [(xy[0]-xAxis[0])/(xAxis[1]-xAxis[0]),(xy[1]-yAxis[0])/(yAxis[1]-yAxis[0])]



	eAxis=spectrum['Axis'][0]
	eAxisLabel = spectrum['AxisLabel'][0]
	yAxis=spectrum['Axis'][1]
	yAxisLabel = spectrum['AxisLabel'][1]
	xAxis=spectrum['Axis'][2]
	xAxisLabel = spectrum['AxisLabel'][2]
	matrix = spectrum['data']
	# -------------------------------------
	# Calculate the number of pixels to use for the angle axis of the output slice 
	
	startPoint_pix = getSliceArbitrary__data2pixel_coords(startPoint,xAxis,yAxis)
	endPoint_pix = getSliceArbitrary__data2pixel_coords(endPoint,xAxis,yAxis)

	#if beQuiet==False: print("Primary slice starts at pixel coordinates [{:.1f},{:.1f}], ends at [{:.1f},{:.1f}]".format(startPoint_pix[0],startPoint_pix[1],endPoint_pix[0],endPoint_pix[1]))

	numpixels_x = abs(1+(endPoint_pix[0]-startPoint_pix[0]))
	numpixels_y = abs(1+(endPoint_pix[1]-startPoint_pix[1]))
	
	dest_numAnglePixels = math.ceil(math.sqrt(numpixels_x**2 + numpixels_y**2))
	
	# What is the increment in X and Y per pixel of the sampling line?
	dX = (endPoint_pix[0]-startPoint_pix[0])/dest_numAnglePixels
	dY = (endPoint_pix[1]-startPoint_pix[1])/dest_numAnglePixels

	destImage = np.zeros([dest_numAnglePixels,len(eAxis)])
	
	# ------------------------------------------------
	# Calculate the span of the output slice in data coordinates
	
	dest_xrange=(startPoint[0]-endPoint[0]) 
	dest_yrange=(startPoint[1]-endPoint[1]) 

	dest_AngleRange = math.sqrt(dest_xrange**2 + dest_yrange**2)
	
	destImage_xAxis = np.linspace(0,dest_AngleRange,dest_numAnglePixels)
	destImage_xAxis_step = destImage_xAxis[1]-destImage_xAxis[0]
	
	# ------------------------------------------------
	# Extract the destination image out of the source 
	# matrix using bi-linear interpolation (since we 
	# will have non-integer indices for the two angular 
	# dimensions)   
	

	# Slice integration is specified in physical units, so first we need to decide the slice sampling density you need in order to 
	# not miss anything.
	#
	# For example, if you extract a slice along the analyzer axis the angle step per pixel is very small. The perpendicular axis will 
	# typically have a much larger angle step, so you don't need many slices to fully sample an integration range of (say) 1deg.
	# 
	# Now consider the opposite case where you are taking for example a slice along the polar axis of a manipulator scan. The perpendicular
	# axis is now the dense analyzer axis, so you would need a lot of slices to fully sample the same 1deg span.
	#
	# A safe if inefficient approach is to just sample with the same density as the most dense axis, so that's what I'm doing.

	if sliceIntegration>0:
		maxDensity = 1/min((xAxis[1]-xAxis[0]),(yAxis[1]-yAxis[0]))
		numLines =math.ceil(sliceIntegration*maxDensity*0.5)
		if numLines<2:
			sliceIntegration=0
			numLines=1
			if beQuiet==False: print("Data density does not support such a small integration width, falling back to no integration")

	if sliceIntegration==0:
		for angleIndex in range(dest_numAnglePixels):

			sourceX = startPoint_pix[0] + dX*angleIndex
			sourceY = startPoint_pix[1] + dY*angleIndex 

			xy = [sourceX,sourceY]


			# Bilinear interpolation
			r0 = math.floor(xy[1])
			r1 = r0 + 1   
			r0w=r1-xy[1]
			r1w=xy[1]-r0

			c0 = math.floor(xy[0])
			c1 = c0 + 1   
			c0w=c1-xy[0]
			c1w=xy[0]-c0

			# take all energy values at once
			interpolatedLine=np.zeros([len(eAxis)])

			if r0<len(yAxis) and c0<len(xAxis) and c1<len(xAxis):
				interpolatedLine+=matrix[:,r0,c0]*r0w*c0w
				interpolatedLine+=matrix[:,r0,c1]*r0w*c1w
			if r1<len(yAxis) and c0<len(xAxis) and c1<len(xAxis):
				interpolatedLine+=matrix[:,r1,c0]*r1w*c0w
				interpolatedLine+=matrix[:,r1,c1]*r1w*c1w

			destImage[angleIndex,:] += interpolatedLine 



	else:
		for ii in np.linspace(start=-sliceIntegration/2,stop=sliceIntegration/2,num=numLines,endpoint=True):
			for angleIndex in range(dest_numAnglePixels):

				sourceX = startPoint_pix[0] + dX*angleIndex
				sourceY = startPoint_pix[1] + dY*angleIndex 

				sourceXY = getSliceArbitrary__pixel2data_coords([sourceX,sourceY],xAxis,yAxis) # Where you are along the main sampling line			

				xy = getSliceArbitrary__getStartPoint(xy=sourceXY,dX=dest_xrange,dY=dest_yrange,R=ii) # Where you are on one of the (parallel) integration lines

				if ii==-sliceIntegration/2 and angleIndex==0: 
					firstSliceStart=xy
					
					xy=getSliceArbitrary__data2pixel_coords(firstSliceStart,xAxis,yAxis)
					#print(xy)
	
				elif ii==sliceIntegration/2 and angleIndex==0: 
					lastSliceStart=xy

					xy=getSliceArbitrary__data2pixel_coords(lastSliceStart,xAxis,yAxis)
					#print(xy)
				else:
					xy=getSliceArbitrary__data2pixel_coords(xy,xAxis,yAxis)


				# Bilinear interpolation
				r0 = math.floor(xy[1])
				r1 = r0 + 1   
				r0w=r1-xy[1]
				r1w=xy[1]-r0

				c0 = math.floor(xy[0])
				c1 = c0 + 1   
				c0w=c1-xy[0]
				c1w=xy[0]-c0

				# take all energy values at once
				interpolatedLine=np.zeros([len(eAxis)])

				if r0<len(yAxis) and c0<len(xAxis) and c1<len(xAxis):
					interpolatedLine+=matrix[:,r0,c0]*r0w*c0w
					interpolatedLine+=matrix[:,r0,c1]*r0w*c1w
				if r1<len(yAxis) and c0<len(xAxis) and c1<len(xAxis):
					interpolatedLine+=matrix[:,r1,c0]*r1w*c0w
					interpolatedLine+=matrix[:,r1,c1]*r1w*c1w

				destImage[angleIndex,:] += interpolatedLine 

			if ii==-sliceIntegration/2: firstSliceEnd=[(xy[0]*(xAxis[1]-xAxis[0]))+xAxis[0],(xy[1]*(yAxis[1]-yAxis[0]))+yAxis[0]]
			if ii==sliceIntegration/2: lastSliceEnd=[(xy[0]*(xAxis[1]-xAxis[0]))+xAxis[0],(xy[1]*(yAxis[1]-yAxis[0]))+yAxis[0]]


		destImage=destImage/numLines

	if beQuiet==False:


		matplotlib.pyplot.figure(figsize=[12,5])

		# Left hand panel showing a constant energy cut and where the slice is being taken
		matplotlib.pyplot.subplot(121)

		if previewEnergy==0: frameIndex=int(len(eAxis)/2)
		else: frameIndex=indexOfClosestValue(eAxis,previewEnergy)
		image=matrix[frameIndex,:,:]
		matplotlib.pyplot.imshow(image,aspect='equal',cmap='gray_r',interpolation='none',extent=[xAxis[0],xAxis[-1],yAxis[-1],yAxis[0]])
		matplotlib.pyplot.xlabel(xAxisLabel)
		matplotlib.pyplot.ylabel(yAxisLabel)

		ax=matplotlib.pyplot.gca()
		matplotlib.pyplot.text(0.04, 0.96,'E = {:.3f}eV'.format(eAxis[frameIndex]),horizontalalignment='left',verticalalignment='top',transform = ax.transAxes)  

		connection = matplotlib.patches.ConnectionPatch(xyA=startPoint,xyB=endPoint,coordsA="data",coordsB="data",color="tab:blue",lw=2,arrowstyle="-|>")
		matplotlib.pyplot.gca().add_patch(connection)  
		
		if sliceIntegration>0:        
			connection = matplotlib.patches.ConnectionPatch(xyA=firstSliceStart,xyB=firstSliceEnd,coordsA="data",coordsB="data",color="tab:orange",lw=1,arrowstyle="-")
			matplotlib.pyplot.gca().add_patch(connection)  
			connection = matplotlib.patches.ConnectionPatch(xyA=lastSliceStart,xyB=lastSliceEnd,coordsA="data",coordsB="data",color="tab:orange",lw=1,arrowstyle="-")
			matplotlib.pyplot.gca().add_patch(connection) 
			connection = matplotlib.patches.ConnectionPatch(xyA=lastSliceStart,xyB=firstSliceStart,coordsA="data",coordsB="data",color="tab:orange",lw=1,arrowstyle="-")
			matplotlib.pyplot.gca().add_patch(connection) 
			connection = matplotlib.patches.ConnectionPatch(xyA=lastSliceEnd,xyB=firstSliceEnd,coordsA="data",coordsB="data",color="tab:orange",lw=1,arrowstyle="-")
			matplotlib.pyplot.gca().add_patch(connection) 
		matplotlib.pyplot.gca().invert_yaxis()
		# Right hand panel showing the extracted slice
		matplotlib.pyplot.subplot(122)            
		matplotlib.pyplot.imshow(destImage.T,aspect='auto',cmap='gray_r',interpolation='none',extent=[destImage_xAxis[0],destImage_xAxis[-1],eAxis[-1],eAxis[0]])
		
		if spectrum['AxisUnits'][2]==r'$\\AA^{-1}$':
			matplotlib.pyplot.xlabel(r"k ($\AA^{-1}$)")
		else:
			matplotlib.pyplot.xlabel(r"Angle ($\degree$)")
		matplotlib.pyplot.ylabel(eAxisLabel)
		matplotlib.pyplot.gca().invert_yaxis()
		connection = matplotlib.patches.ConnectionPatch(xyA=[0,1.05],xyB=[1,1.05],coordsA="axes fraction",coordsB="axes fraction",color="tab:blue",lw=2,arrowstyle="-|>")
		matplotlib.pyplot.gca().add_patch(connection)  

		matplotlib.pyplot.tight_layout()
		matplotlib.pyplot.show()

	outputSpectrum={}
	outputSpectrum['Metadata']={}
	outputSpectrum['Axis']=[[],[]]
	outputSpectrum['AxisLabel']=["",""]
	outputSpectrum['AxisUnits']=["",""]
	outputSpectrum['data']=destImage.T
	outputSpectrum['Axis'][0]=eAxis
	outputSpectrum['AxisLabel'][0]=spectrum['AxisLabel'][0]
	outputSpectrum['AxisUnits'][0]=spectrum['AxisUnits'][0]
	outputSpectrum['Axis'][1]=destImage_xAxis

	if spectrum['AxisUnits'][2]==r'$\\AA^{-1}$':
		outputSpectrum['AxisLabel'][1]="k"
		outputSpectrum['AxisUnits'][1]=r"$\AA^{-1}$"
	else:
		outputSpectrum['AxisLabel'][1]="Angle"
		outputSpectrum['AxisUnits'][1]=r"$\degree$"

	return outputSpectrum





def getSlice(spectrum,axis,axisValue,sliceIntegration=0,normalized=False,beQuiet=True):

	assert(len(np.shape(spectrum['data'])) == 3), "Expected a 3D spectrum as input"
	assert(axis in [0,1,2]), "Invalid 'axis' parameter. Valid axis choices are 0 (typically energy axis), 1 (typically analyzer angle axis) or 2"

	def getSlice__arraySlice(a, axis, start, end, step=1):
		if start==end: end=start+1
		return a[(slice(None),) * (axis % a.ndim) + (slice(start, end, step),)]

	a = np.asarray(spectrum['Axis'][axis])
	if sliceIntegration==0:
		frameIndex = (np.abs(a - axisValue)).argmin()
		image=getSlice__arraySlice(spectrum['data'],axis=axis,start=frameIndex,end=frameIndex)
		image=np.sum(image,axis=axis)

	else:
		value = axisValue-(sliceIntegration/2)
		startFrameIndex = (np.abs(a - value)).argmin()

		value = axisValue+(sliceIntegration/2)
		endFrameIndex = (np.abs(a - value)).argmin()

		if startFrameIndex>endFrameIndex: startFrameIndex,endFrameIndex=endFrameIndex,startFrameIndex

		if beQuiet==False: 		
			print("Requested axisValue {} along axis {} ('{}')".format(axisValue,axis,spectrum['AxisLabel'][axis]))
			print("That axis spans {:.4f} ... {:.4f} and contains {} points".format(a[0],a[-1],len(a)))
			if startFrameIndex == endFrameIndex and sliceIntegration!=0:
				print("Requested integration is too small, only returning a single frame")
			if startFrameIndex == endFrameIndex: print("Extracting frame index {} ({:.4f}) of axis '{}'".format(startFrameIndex,a[startFrameIndex],spectrum['AxisLabel'][axis]))
			else: print("An integration of {} {} means summing over indices {} through {}".format(sliceIntegration,spectrum['AxisUnits'][axis],startFrameIndex,endFrameIndex))

		#image=spectrum['data'].take(indices=range(startFrameIndex, endFrameIndex+1), axis=axis)
		image=getSlice__arraySlice(spectrum['data'],axis=axis,start=startFrameIndex,end=endFrameIndex)

		image=np.sum(image,axis=axis)
		if normalized==True:
			image=image/(1+endFrameIndex-startFrameIndex)

	
	if axis==0: ii,jj = 1,2
	if axis==1: ii,jj = 0,2
	if axis==2: ii,jj = 0,1

	outputSpectrum={}
	outputSpectrum['Axis']=[[],[]]
	outputSpectrum['AxisLabel']=[[],[]]
	outputSpectrum['AxisUnits']=[[],[]]

	outputSpectrum['Metadata']=spectrum['Metadata']


	outputSpectrum['data']=image


	outputSpectrum['Axis'][0]=spectrum['Axis'][ii]
	outputSpectrum['Axis'][1]=spectrum['Axis'][jj]
	outputSpectrum['AxisLabel'][0]=spectrum['AxisLabel'][ii]
	outputSpectrum['AxisLabel'][1]=spectrum['AxisLabel'][jj]
	outputSpectrum['AxisUnits'][0]=spectrum['AxisUnits'][ii]
	outputSpectrum['AxisUnits'][1]=spectrum['AxisUnits'][jj]		

	return outputSpectrum


def getFrameFrom4DScan(spectrum,axes,axisValues,beQuiet=True):

	assert(len(np.shape(spectrum['data'])) == 4), "Expected a 4D spectrum as input"
	assert len(axes)==2 and len(axisValues)==2, "This is a 4D dataset, to extract a 2D slice I need two axis names and a value for each axis. (e.g. axes=['X','Y'],axisValues=[-0.3,274])"
	assert axes[0] in spectrum['AxisLabel'] and axes[1] in spectrum['AxisLabel'], "axes inputs must be chosen from: {}".format(spectrum['AxisLabel'])

	ax,val=axes[0],axisValues[0]
	axisIndices=[ii for ii in spectrum['AxisLabel']]
	axisIndex=spectrum['AxisLabel'].index(ax)
	if beQuiet==False: print("Requested axisValue {} along axis {} ('{}')".format(val,ax,axisIndex))

	frameIndex=indexOfClosestValue(spectrum['Axis'][axisIndex],val)
	if beQuiet==False: print("This comes at axis index ",frameIndex)

	# np.take is an alternative approach here that would elegantly let me leave the axis as a variable. However, it's much, much, much slower for some reason. So we'll go with this hack instead:
	#matrix3D=spectrum['data'].take(indices=frameIndex, axis=axisIndex)
	if axisIndex==0: matrix3D=spectrum['data'][frameIndex,:,:,:]
	if axisIndex==1: matrix3D=spectrum['data'][:,frameIndex,:,:]
	if axisIndex==2: matrix3D=spectrum['data'][:,:,frameIndex,:]
	if axisIndex==3: matrix3D=spectrum['data'][:,:,:,frameIndex]

	axisIndices.remove(ax)


	ax,val=axes[1],axisValues[1]
	axisIndex=spectrum['AxisLabel'].index(ax) #In the original data chunk
	if beQuiet==False: print("Requested axisValue {} along axis {} ('{}')".format(val,ax,axisIndex))

	frameIndex=indexOfClosestValue(spectrum['Axis'][axisIndex],val)
	if beQuiet==False: print("This comes at axis index ",frameIndex)

	axisIndex=axisIndices.index(ax) #in our reduced data chunk - not necessarily the same since we deleted one dimension earlier

	# np.take is an alternative approach here that would elegantly let me leave the axis as a variable. However, it's much, much, much slower for some reason. So we'll go with this hack instead:
	#matrix2D=matrix3D.take(indices=frameIndex, axis=axisIndex)
	if axisIndex==0: matrix2D=matrix3D[frameIndex,:,:]
	if axisIndex==1: matrix2D=matrix3D[:,frameIndex,:]
	if axisIndex==2: matrix2D=matrix3D[:,:,frameIndex]

	kk=[0,1,2,3]
	axisLabels=[ii for ii in spectrum['AxisLabel']]
	kk.remove(axisLabels.index(axes[1]))
	kk.remove(axisLabels.index(axes[0]))
	ii,jj=kk[0],kk[1]


	outputSpectrum={}
	outputSpectrum['Axis']=[[],[]]
	outputSpectrum['AxisLabel']=[[],[]]
	outputSpectrum['AxisUnits']=[[],[]]

	outputSpectrum['Metadata']={}
	outputSpectrum['data']=matrix2D

	outputSpectrum['Axis'][0]=spectrum['Axis'][ii]
	outputSpectrum['Axis'][1]=spectrum['Axis'][jj]
	outputSpectrum['AxisLabel'][0]=spectrum['AxisLabel'][ii]
	outputSpectrum['AxisLabel'][1]=spectrum['AxisLabel'][jj]
	outputSpectrum['AxisUnits'][0]=spectrum['AxisUnits'][ii]
	outputSpectrum['AxisUnits'][1]=spectrum['AxisUnits'][jj]		

	return outputSpectrum



def fitFermiEdge(spectrum,angleRange=[None,None],energyRange=[None,None],linearBG=False,temperature=20,beQuiet=False):

	def fitFermiEdge__model(params,x,linearBG):

		Amplitude = params['Amplitude'].value
		Ef = params['FermiLevel'].value
		Temperature = params['Temperature'].value
		ResolutionFWHM = params['ResolutionFWHM'].value
		BG_offset = params['BG_offset'].value
		if linearBG==True: BG_slope = params['BG_slope'].value
		x_range=x[-1]-x[0]
		x_delta=x[1]-x[0]
		#print(x)
		
		# Make a new x wave associated with the convolution Gaussian
		# It should have the same delta as the input x-wave, but be much 
		# wider in x range to avoid edge effects.
		# Centered on zero

		#print("x_range ",x_range)
		conv_x=np.arange((-5*x_range), (5*x_range), x_delta)
		convolutionGaussian=np.exp(  -4*np.log(2)*np.power(conv_x/ResolutionFWHM,2)  )
		#print("convx: ",conv_x[0],conv_x[-1])
		#print("Delta: ",((-5*x_range)) - ((5*x_range)))
		#print((-5*x_range), (5*x_range), x_delta)
		#print("len(conv_x): ",len(conv_x))
		#print("len(convolutionGaussian): ",len(convolutionGaussian))

		# Also make an extended x-wave associated with our convolved model. Same center as the input data
		conv_x=np.arange((x[0]-(5*x_range)), x[-1]+(5*x_range), x_delta)
		#print("x: ",x[0],x[-1])
		#print("convx: ",conv_x[0],conv_x[-1])
		#print((x[0]-(5*x_range)), x[-1]+(5*x_range), x_delta)
		#print("Delta: ",(x[-1]+(5*x_range)) - (x[0]-(5*x_range)))
		#print("len(conv_x): ",len(conv_x))

		unconvolvedModel = (1 / (np.exp((conv_x-Ef)/(8.617e-5*Temperature)) + 1)) 
		#print("len(unconvolvedModel): ",len(unconvolvedModel))
		convolutionOutput = np.convolve(unconvolvedModel,convolutionGaussian,mode="full")

		# The convolution output has the same xdelta and central x as our input wave, but the range is still extended.
		# So we need to trim from both ends until it matches the x-range of our input wave
		amountToTrim=int((len(convolutionOutput)-len(x))/2)
		#print("AmountToTrim ",amountToTrim)
		#print("len(convolutionOutput) ",len(convolutionOutput))
		#print("len(x) ",len(x))
		#print(x_range/x_delta)
		
		convolvedModel=[]
		for ii in range(amountToTrim,amountToTrim+len(x)):
			convolvedModel.append(convolutionOutput[ii])

		v_max=max(convolvedModel)
		convolvedModel = (convolvedModel/v_max) #Normalize
		if linearBG==True: convolvedModel = convolvedModel*(1+(BG_slope*(x-x[-1]))) #Add the linear background
		convolvedModel = convolvedModel*Amplitude #Scale it to match experimental data
		convolvedModel += BG_offset  #Offset to match experimental data
		return convolvedModel

	def fitFermiEdge__residual(params, x, y,linearBG):

		return (y-fitFermiEdge__model(params,x,linearBG))

	try:
		if spectrum.endswith(".txt") or spectrum.endswith(".ibw"): spectrum=loadSpectrum(spectrum,beQuiet=True)
	except AttributeError:
		pass


	temperature=float(temperature)

	input_is_2D = False
	
	if len(np.shape(spectrum['data']))>1:
		input_is_2D=True
		angle,energy=spectrum['Axis'][1],spectrum['Axis'][0]

		if angleRange[0] is None: angleStart=angle[0]
		else: angleStart = angle[indexOfClosestValue(angle,angleRange[0])]
		if angleRange[1] is None: angleEnd=angle[-1]
		else: angleEnd = angle[indexOfClosestValue(angle,angleRange[1])]

		if energyRange[0] is None: energyStart=energy[0]
		else: energyStart = energy[indexOfClosestValue(energy,energyRange[0])]
		if energyRange[1] is None: energyEnd=energy[-1]
		else: energyEnd = energy[indexOfClosestValue(energy,energyRange[1])]

		profile=getProfile(
			spectrum=spectrum,
			samplingAxis='y',
			xAxisRange=angleRange,
			yAxisRange=energyRange,
			beQuiet=True)

		EDC_intensity = profile['data']
		EDC_energy = profile['Axis']

	else:
		energy=spectrum['Axis']
		if energyRange[0] is None: energyStart=energy[0]
		else: energyStart = energy[indexOfClosestValue(energy,energyRange[0])]
		if energyRange[1] is None: energyEnd=energy[-1]
		else: energyEnd = energy[indexOfClosestValue(energy,energyRange[1])]

		#print(energyStart,energyEnd)
		profile=clipSpectrum(spectrum,xRange=[energyStart,energyEnd])
		
		EDC_intensity = profile['data']
		EDC_energy = profile['Axis']

	# -----------------
	# --- Curve fit ---
	# -----------------
	
	amplitudeGuess = EDC_intensity[0]-EDC_intensity[-1]
	BG_offsetGuess = EDC_intensity[-1]

	# Miniumum of the derivative gives a good starting guess of the fermi level

	EfGuess= EDC_energy[np.argmin(np.diff(EDC_intensity))]

	params = Parameters()
	params.add('Amplitude', 	value=amplitudeGuess, vary=True)
	params.add('FermiLevel', 	value=EfGuess, min=EDC_energy[0],max=EDC_energy[-1],vary=True)
	params.add('Temperature', 	value=temperature, vary=False)
	params.add('ResolutionFWHM', value=0.01, vary=True,	min=0)
	params.add('BG_offset', 	value=BG_offsetGuess,	min=0,vary=True)
	if linearBG==True: params.add('BG_slope', 	value=-1,vary=True)


	out = minimize(fitFermiEdge__residual, params,args=(EDC_energy, EDC_intensity,linearBG),method='leastsq')

	EfFitted = 0

	# -------------------------------------
	# --- Plot the source image and EDC ---
	# -------------------------------------
	
	if beQuiet==False:
		if input_is_2D==True: ncols=3
		else: ncols=2

		fig,axes=matplotlib.pyplot.subplots(figsize=[12,4],ncols=ncols)

		panelIndex=0

		if input_is_2D==True:
			ax=axes[panelIndex]
			quickPlot(spectrum,axis=ax)
			rect = matplotlib.patches.Rectangle([angleStart,energyStart],  (angleEnd-angleStart),(energyEnd-energyStart),linewidth=1, edgecolor = 'g',facecolor='none')
			ax.add_patch(rect)
			ax.set_title("Input spectrum")
			panelIndex+=1

		ax=axes[panelIndex]
		quickPlot(profile,axis=ax)
		fittedCurve=fitFermiEdge__model(out.params,EDC_energy,linearBG)
		ax.plot(EDC_energy,fittedCurve)
		ax.set_title("EDC + fit")
		panelIndex+=1

		ax=axes[panelIndex]
		ax.plot(EDC_energy,out.residual)
		ax.axhline(y=0,color='gray',ls='--')
		ax.set_title("Residuals")
		ax.set_xlabel("{} ({})".format(spectrum['AxisLabel'][0],spectrum['AxisUnits'][0]))


		matplotlib.pyplot.tight_layout()
		matplotlib.pyplot.show()
		for key, par in out.params.items():
			if key=='FermiLevel':
				EfFitted=par.value
				print("Fermi level \t\t{1:.3f} eV".format(key, par.value))
			if key=='Temperature':
				print("Temperature \t\t{1:.2f} K (fixed)".format(key, par.value))
			elif key=='ResolutionFWHM':
				print("Resolution FWHM\t\t{1:.2f} meV".format(key, par.value*1000))
			#elif key=='BG_slope':
			#	print("BG_slope\t\t{1:.2e} ".format(key, par.value))


		print("\nPhoton energy: {0:.3f} + {1:.3f} = {2:.3f}".format(EfFitted,getAnalyzerWorkFunction(),EfFitted+getAnalyzerWorkFunction()))

	return out.params



#----------------------------------------------------------------------------	
#----------------------------------------------------------------------------
#---------------------------- Calculators -----------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


def SBZ():
	return pesto.interactive.SBZ()



def kCalculator():

	def build_panel(hv,angle,k):

		print("With {}eV photons,".format(hv))
		print("\t{}\u00b0 from normal is {:.2f} Å-1 at Ef".format(angle,0.512*np.sqrt(hv-getAnalyzerWorkFunction())*np.sin(np.deg2rad(angle))))
		print("\t{:.2f} Å-1 is {:.2f}\u00b0 from normal at Ef".format(k,np.rad2deg(np.arcsin(k/(0.512*np.sqrt(hv-getAnalyzerWorkFunction()))))))
		minhv = (k/(0.512*math.sin(math.radians(angle))))**2 + getAnalyzerWorkFunction()
		print("\nMinimum photon energy to reach k={:.2f} Å-1 at Ef within an angular acceptance of {:.2f}\u00b0 is {:.1f} eV".format(k,angle,minhv))

	style = {'description_width': 'initial'}

	hv=ipywidgets.widgets.IntSlider(
	value=50,
	min = 10,
	max = 200,
	step=1,
	description='Photon energy (eV)',
	disabled=False,
	layout=ipywidgets.Layout(width='600px'),
	style=style
	)

	k=ipywidgets.widgets.FloatSlider(
	value=1,
	min = 0,
	max = 10,
	step=0.05,
	description='k_// (Å-1)',
	disabled=False,
	layout=ipywidgets.Layout(width='600px'),
	style=style
	)

	angle=ipywidgets.widgets.FloatSlider(
	value=14,
	min = 0,
	max = 89,
	step=0.05,
	description='Angle (\u00b0)',
	disabled=False,
	layout=ipywidgets.Layout(width='600px'),
	style=style
	)

	w = ipywidgets.interactive(
		build_panel,
		hv=hv,
		k=k,
		angle=angle
	)
	return w 







def kwarp(spectrum,Eb_offset=getAnalyzerWorkFunction(), polar_offset=0,tilt_offset=0,hv=0,resolutionDivider=1,corrected_hvAxis=[],energyOffset=[],beQuiet=False):

	eV_per_J = 1.602176e-19
	hbar__Js = 1.054571e-34
	electron_mass__kg = 9.109e-31
	angstroms_per_meter=1e-10
	prefactor = (math.sqrt(2*electron_mass__kg*eV_per_J)/(hbar__Js))*angstroms_per_meter # = 0.51234


	#def kwarp__wholeMatrix_timeScan_kwarp(spectrum,polar_offset,tilt_offset,hv,resolutionDivider,energyOffset,beQuiet):
	#	print("stub")

	#-------------------------------------------------------------------------------------------------------------------------------------------------
	def kwarp__wholeMatrix_hvscan_warp(spectrum,tilt_offset,Eb_offset,corrected_hvAxis,resolutionDivider,beQuiet):
		t0=time.time()

		tilt_offset_rad = math.radians(tilt_offset)

		#-------------------------- Properties of the source matrix
		sourceMatrix= spectrum['data']

		source_energyAxis__Eb = np.array(spectrum['Axis'][0])
		source_energyAxis_corrected__Eb = source_energyAxis__Eb - Eb_offset
		source_energyAxis_step = abs(source_energyAxis__Eb[1]-source_energyAxis__Eb[0])

		source_angleAxis = np.array(spectrum['Axis'][1])
		source_angleAxis_step = abs(source_angleAxis[1]-source_angleAxis[0])

		source_hvAxis = np.array(spectrum['Axis'][2])

		if source_hvAxis[0]>source_hvAxis[-1]: # Handle the case where photon energy was swept down rather than up:
			source_hvAxis = np.array([ii for ii in reversed(spectrum['Axis'][2])])
			sourceMatrix = np.flip(sourceMatrix,2)		



		#-------------------------- Properties of output (destination) matrix	
		# Find the dimensions of an output matrix that will fit the entire kwarped dataset without compromising resolution 

		# First we find the max and min k values, by just calculating for each hv frame what the k limits and minimum k stepsize is on each frame
		# We'll then take the min and max from that list to determine the boundaries and number of points in the output matrix.
		
		kLimits=[]
		kSteps = []

		global_maxEb,global_minEb = -999,999 #Needed if a corrected hv axis has been passed in

		if len(corrected_hvAxis)==0:
			global_maxEb,global_minEb=max(source_energyAxis_corrected__Eb),min(source_energyAxis_corrected__Eb)
		
		for index,hv in enumerate(source_hvAxis): #For each frame in the dataset

			Ek = hv - source_energyAxis_corrected__Eb
			Ek_max,Ek_min = max(Ek),min(Ek)

			if len(corrected_hvAxis)>0: #Special case if there is a corrected hv axis - the energy range for each frame will now be different
				Ek_corrected = Ek + (corrected_hvAxis[index]-hv)
				Eb_corrected = source_energyAxis_corrected__Eb + (corrected_hvAxis[index]-hv)
				Ek_max = max(Ek_corrected)
				Eb_min = min(Eb_corrected)
				Ek_min = min(Ek_corrected)
				Eb_max = max(Eb_corrected)
				if Eb_max>global_maxEb: global_maxEb=Eb_max
				if Eb_min<global_minEb: global_minEb=Eb_min
			# For this photon energy we can now calculate the max and min k values:
			kLimits.append(angle_to_ky_manipulator(alpha=source_angleAxis[0],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_max))
			kLimits.append(angle_to_ky_manipulator(alpha=source_angleAxis[-1],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_max))

			# And the max and min k stepsizes:
			kSteps.append(abs(angle_to_ky_manipulator(alpha=source_angleAxis[0],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_min)-angle_to_ky_manipulator(alpha=source_angleAxis[1],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_min)))
			kSteps.append(abs(angle_to_ky_manipulator(alpha=source_angleAxis[-1],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_min)-angle_to_ky_manipulator(alpha=source_angleAxis[-2],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_min)))

		kMax,kMin = max(kLimits),min(kLimits)
		kStepMax,kStepMin = max(kSteps),min(kSteps)




		# Downscale according to the divider that got passed in
		if resolutionDivider!=1 and beQuiet==False: print("Scaling resolution by {}x, kStep now {:.4f} compared to minimum possible {:.4f}".format(resolutionDivider,kStepMax*resolutionDivider,kStepMin))
		
		num_kSteps = int((kMax-kMin)/(kStepMax*resolutionDivider))
		outputMatrix_kAxis = np.linspace(kMin,kMax,num_kSteps)

		# Now do the same exercise for the energy scale

		"""
		if len(corrected_hvAxis)==0:
			eMin = min(source_energyAxis_corrected__Eb)
			eMax = max(source_energyAxis_corrected__Eb)
		else:
			source_hvAxis = np.array(source_hvAxis)
			corrected_hvAxis = np.array(corrected_hvAxis)

			hv_delta = max(corrected_hvAxis-source_hvAxis,key=abs) #Find the largest value, retain the sign
			#min_hv_delta = min(corrected_hvAxis-source_hvAxis,key=abs) #Find the largest value, retain the sign
			

			eMin = min(source_energyAxis_corrected__Eb)
			eMax = max(source_energyAxis_corrected__Eb)
			if beQuiet==False:
				print("Largest hv correction to consider is {}. The binding energy scale of the output will thus be modified from {}--{} to {}--{}".format(hv_delta,eMin,eMax,eMin+hv_delta,eMax+hv_delta))
			if hv_delta<0:
				eMin+=hv_delta

			#eMax-=hv_delta
		"""
		num_eSteps = int((global_maxEb-global_minEb)/(source_energyAxis_step*resolutionDivider))
		outputMatrix_eAxis = np.linspace(global_maxEb,global_minEb,num_eSteps)

		# Initialize the output (kwarped) matrix
		outputMatrixSize = (outputMatrix_eAxis.size,outputMatrix_kAxis.size,source_hvAxis.size)
		outputMatrix=np.zeros(outputMatrixSize)
		#--------------------------


		#-------------------------- Perform the reverse mapping (look up source pixel from output pixel)

		for hv_index,photonEnergy in enumerate(source_hvAxis): #For each photon energy
	
			if beQuiet==False:
				printProgressBar(hv_index, len(source_hvAxis)-1, prefix = 'Progress:', suffix = 'Complete', length = 50)

			im = sourceMatrix[:,:,hv_index] #Extract the energy-angle image, it will be [energy,angle]

			if len(corrected_hvAxis)==0: 
				source_Ek_axis = photonEnergy-getAnalyzerWorkFunction()-source_energyAxis_corrected__Eb
			else:
				source_Ek_axis= photonEnergy+(photonEnergy-corrected_hvAxis[hv_index])-getAnalyzerWorkFunction() -source_energyAxis_corrected__Eb

			output_Ek_axis = photonEnergy-getAnalyzerWorkFunction()-outputMatrix_eAxis

			# prepare for the the interpolation

			spl = scipy.interpolate.RectBivariateSpline(source_Ek_axis,source_angleAxis, im,kx=1,ky=1)



			# Pre-compute some things outside of the loop for speed
			C_axis = prefactor*np.sqrt(source_Ek_axis) 
			C2_axis = C_axis**2
			k2_axis = outputMatrix_kAxis**2

			source_angleAxis_min=min(source_angleAxis)
			source_angleAxis_max=max(source_angleAxis)

			for output_energyPixel,output_Ek in enumerate(output_Ek_axis): 

				if output_Ek>min(source_Ek_axis) and output_Ek<max(source_Ek_axis):
					sourceEnergy__Pixel=indexOfClosestValue(list(source_Ek_axis),output_Ek)

					C = C_axis[sourceEnergy__Pixel]
					C2 = C2_axis[sourceEnergy__Pixel]
					E = np.sqrt((C2-k2_axis))
					
					# Based on kparr = 0.512*sqrt(Ek)*sin(alpha+tilt), except we've precomputed 0.512*sqrt(Ek)
					source_angle_degrees = np.degrees(np.arcsin(outputMatrix_kAxis/C)-np.radians(tilt_offset)) #Contains all angle pixels at this energy value and this hv
					
					source_angle_degrees = [float('NaN') if (ii>source_angleAxis_max or ii<source_angleAxis_min) else ii for ii in source_angle_degrees]
					outputMatrix[output_energyPixel,:,hv_index]=np.nan_to_num(spl(output_Ek,source_angle_degrees,grid=False))



		outputSpectrum={}
		outputSpectrum['Metadata']={}
		outputSpectrum['data']=outputMatrix
		outputSpectrum['Axis']=[[],[],[]]
		outputSpectrum['AxisLabel']=["","",""]
		outputSpectrum['AxisUnits']=["","",""]

		if len(corrected_hvAxis)==0:
			outputSpectrum['Axis'][2]=list(source_hvAxis)
		else:
			outputSpectrum['Axis'][2]=list(corrected_hvAxis)
		outputSpectrum['AxisLabel'][2]="Photon energy" 
		outputSpectrum['AxisUnits'][2]='eV'

		outputSpectrum['Axis'][0]=list(outputMatrix_eAxis)
		outputSpectrum['AxisLabel'][0]="Binding energy"  
		outputSpectrum['AxisUnits'][0]='eV'

		outputSpectrum['Axis'][1]=list(outputMatrix_kAxis)
		outputSpectrum['AxisLabel'][1]="kY"
		outputSpectrum['AxisUnits'][1]=r'$\AA^{-1}$'



		if beQuiet==False: print("Time taken: {:.2f} seconds".format(time.time()-t0))
		return outputSpectrum
			
	#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def kwarp__wholeMatrix_kwarp(spectrum,polar_offset,tilt_offset,hv,resolutionDivider,beQuiet=True):
		tilt_offset=-tilt_offset #For consistency with the other functions
		polar_offset=-polar_offset

		# ----- Input properties:

		e = spectrum['Axis'][0] # energy
		y = spectrum['Axis'][1] # angle 1 (analyzer)
		x = spectrum['Axis'][2] # angle 2 (deflector or polar)

		data = spectrum['data']

		# ----- Output properties:

		outputMatrixSize = tuple(int(ii/resolutionDivider) for ii in data.shape)
		outputMatrix=np.empty(outputMatrixSize)

		Ek_max = max(e)
		x_first, x_last = x[0]-polar_offset,x[-1]-polar_offset
		x = [ii - polar_offset for ii in x]
		x_k_first=angle_to_kx_manipulator(alpha=0,polar_offset = x[0], Ek = Ek_max)
		x_k_last=angle_to_kx_manipulator(alpha=0,polar_offset = x[-1], Ek = Ek_max)

		y_k_max=angle_to_ky_manipulator(alpha=np.max(y),polar_offset = min(np.abs(x)),tilt_offset= tilt_offset,Ek = Ek_max)
		y_k_min=angle_to_ky_manipulator(alpha=np.min(y),polar_offset = max(np.abs(x)),tilt_offset= tilt_offset,Ek = Ek_max)

		x_k_step=((x_k_last-x_k_first)/(outputMatrix.shape[2]-1))
		y_k_step=((y_k_max-y_k_min)/(outputMatrix.shape[1]-1))
		e_step = ((e[-1]-e[0])/(outputMatrix.shape[0]-1))

		x_kAxis = [x_k_first+(index*x_k_step) for index in range(outputMatrix.shape[2])]
		x_kAxis=np.array(x_kAxis)
		y_kAxis = [y_k_min+(index*y_k_step) for index in range(outputMatrix.shape[1])]
		y_kAxis=np.array(y_kAxis)
		Ek_axis = [e[0]+(index*e_step) for index in range(outputMatrix.shape[0])]

		x_step = x[1]-x[0]
		y_step = y[1]-y[0]

		sin_tiltOffset_radians = math.sin(math.radians(tilt_offset))
		cos_tiltOffset_radians = math.cos(math.radians(tilt_offset))
		# ---- For every energy value

		interpolator = scipy.interpolate.RegularGridInterpolator(points=(e,y,x),values=data, method='linear',bounds_error=False,fill_value=0)

		outputImage_xAngles = np.empty((outputMatrixSize[1],outputMatrixSize[2]))
		outputImage_yAngles = np.empty((outputMatrixSize[1],outputMatrixSize[2]))
		outputImage_Ek = np.empty((outputMatrixSize[1],outputMatrixSize[2]))
			
		outputImage_EMatrix = np.empty(outputMatrixSize)

		E_x=np.tile(np.atleast_2d(x_kAxis).T, (1,len(y_kAxis)))	
		E_y=np.tile(y_kAxis, (len(x_kAxis),1))


		for Ek_index,Ek in enumerate(Ek_axis):

			outputImage_Ek[:]=Ek
			if beQuiet==False: printProgressBar(Ek_index, len(Ek_axis)-1, prefix = 'Progress:', suffix = 'Complete', length = 50)
				
			#Extract a constant energy surface
			inputImage = data[int(Ek_index*resolutionDivider),:,:]
			C = prefactor*math.sqrt(Ek)
			outputImage_EMatrix = np.sqrt(((C**2)-(E_x**2)-(E_y**2)))

			nnn = sin_tiltOffset_radians*outputImage_EMatrix
			ppp = cos_tiltOffset_radians*outputImage_EMatrix

			qqq = cos_tiltOffset_radians*y_kAxis
			zzz = sin_tiltOffset_radians*y_kAxis

			# ---- For every polar value
			for jj,kx in enumerate(x_kAxis):
				# compute all analyzer angle-->k mappings at once (1D array --> 1D array)
				E = outputImage_EMatrix[jj]
				alpha_rad = (np.arcsin((nnn[jj] - qqq)/C )) 
				y_angle = np.degrees(alpha_rad)
				outputImage_yAngles[:,jj]=y_angle

				polar_rad = (np.arctan((kx) / (zzz + ppp[jj] )))
				x_angle = np.degrees(polar_rad)
				outputImage_xAngles[:,jj]=x_angle


			outputMatrix[Ek_index,:,:]=interpolator((outputImage_Ek,outputImage_yAngles,outputImage_xAngles))

		outputMatrix[np.isnan(outputMatrix)]=0
		
		outputSpectrum={}
		outputSpectrum['Metadata']={}
		outputSpectrum['data']=outputMatrix
		outputSpectrum['Axis']=[[],[],[]]
		outputSpectrum['AxisLabel']=["","",""]
		outputSpectrum['AxisUnits']=["","",""]

		outputSpectrum['Axis'][2]=x_kAxis
		outputSpectrum['AxisUnits'][2]=r'$\AA^{-1}$'
		outputSpectrum['AxisLabel'][2]="k_X" 

		if hv!=0:
			outputSpectrum['Axis'][0]=[hv - ii - getAnalyzerWorkFunction() for ii in Ek_axis]
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Binding energy"  
		else:
			outputSpectrum['Axis'][0]=Ek_axis
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Kinetic energy"			

		outputSpectrum['Axis'][1]=y_kAxis
		outputSpectrum['AxisUnits'][1]=r'$\AA^{-1}$'
		outputSpectrum['AxisLabel'][1]="k_Y"  
		return outputSpectrum

	def kwarp__wholeMatrix_kwarp_deflector(spectrum,polar_offset,tilt_offset,hv,resolutionDivider,beQuiet):
		import time

		resolutionDivider=resolutionDivider

		t0=time.time()

		# ----- Input properties:

		x = spectrum['Axis'][2] # Typically angle 2 (deflector, polar). Will be mapped to kx
		y = spectrum['Axis'][1] # Typically angle 1 (analyzer). Will be mapped to ky
		e = spectrum['Axis'][0] # Typically energy

		data = spectrum['data']

		# If the deflection or polar goes backwards, flip both the data matrix and the axis values
		# I don't think this is possible with deflector scans, but it is with polar maps

		if x[0]>x[-1]:
			x = [ii for ii in reversed(spectrum['Axis'][2])]
			data = np.flip(data,2)

		Ek_max = max(e)


		# ----- Output properties:

		outputMatrixSize = tuple(int(ii/resolutionDivider) for ii in data.shape)
		outputMatrix=np.zeros(outputMatrixSize)

	
		#print("Output matrix has shape:",outputMatrix.shape)

		x_k_first=angle_to_kx_deflector(alpha=0,beta= x[0],polar_offset = polar_offset,Ek = Ek_max)
		x_k_last=angle_to_kx_deflector(alpha=0,beta= x[-1],polar_offset = polar_offset,Ek = Ek_max)

		y_k_max=angle_to_ky_deflector(alpha=np.max(y),beta=0,polar_offset = polar_offset,tilt_offset= tilt_offset,Ek = Ek_max)
		y_k_min=angle_to_ky_deflector(alpha=np.min(y),beta=0,polar_offset = polar_offset,tilt_offset= tilt_offset,Ek = Ek_max)

		x_k_step=((x_k_last-x_k_first)/(outputMatrix.shape[2]-1))
		y_k_step=((y_k_max-y_k_min)/(outputMatrix.shape[1]-1))

		e_step = ((e[-1]-e[0])/(outputMatrix.shape[0]-1))

		x_kAxis = [x_k_first+(index*x_k_step) for index in range(outputMatrix.shape[2])]
		x_kAxis=np.array(x_kAxis)
		#print("x_kAxis spans {:.3f} through {:.3f}, step {:.3f}. len{}".format(x_kAxis[0],x_kAxis[-1],x_k_step,len(x_kAxis)))
		y_kAxis = [y_k_min+(index*y_k_step) for index in range(outputMatrix.shape[1])]
		y_kAxis=np.array(y_kAxis)
		#print("y_kAxis spans {:.3f} through {:.3f}, step {:.3f}".format(y_kAxis[0],y_kAxis[-1],y_k_step))
		#print(len(x_kAxis),len(y_kAxis))
		Ek_axis = [e[0]+(index*e_step) for index in range(outputMatrix.shape[0])]
		#print("Ek_axis spans {:.3f} through {:.3f}, step {:.3f}".format(Ek_axis[0],Ek_axis[-1],e_step))

		x_step = x[1]-x[0]
		y_step = y[1]-y[0]

		polar_rad = math.radians(polar_offset)
		tilt_rad = math.radians(tilt_offset)
		st=math.sin(tilt_rad)
		ct=math.cos(tilt_rad)
		sp=math.sin(polar_rad)
		cp=math.cos(polar_rad)

		t12 = ct
		t13 = -st
		t21 = -cp
		t22 = sp*st
		t23 = sp*ct
		t31 = sp
		t32 = cp*st
		t33 = cp*ct	

		# Step through every constant energy slice and perform the warping 'all at once' on each slice
		for index,Ek in enumerate(Ek_axis):

			if beQuiet==False: printProgressBar(index, len(Ek_axis)-1, prefix = 'Progress:', suffix = 'Complete', length = 50)
			
			#print("Extracting a constant energy slice:")
			inputImage = data[int(index*resolutionDivider),:,:]
			#inputImage = data[:,:,int(index*resolutionDivider)]
			#inputImage is a constant energy slice
			#print("size is:",np.shape(inputImage))
			#print(len(x),len(y))

			# Fast method of doing 2D interpolation from the source energy slice

			spl = scipy.interpolate.RectBivariateSpline(y,x, inputImage,kx=1,ky=1)
			
			#print("Ek = ",Ek)
			C = prefactor*math.sqrt(Ek)

			for jj,kx in enumerate(x_kAxis):
				E = np.sqrt((C**2-kx**2-y_kAxis**2))
				zz = np.sqrt(C**2 - (t31*kx + t32*y_kAxis + t33*E)**2)
				precalc1 = -np.arccos((t31*kx + t32*y_kAxis + t33*E)/C)/zz
				beta_rad = precalc1  * (t21*kx + t22*y_kAxis + t23*E)
				x_angle= np.degrees(beta_rad)
				alpha_rad = precalc1 * (t12*y_kAxis + t13*E)
				y_angle= -np.degrees(alpha_rad) # Notice that I flipped the sign!	

				temp = spl(y_angle,x_angle,grid=False)
				#print(len(temp))
				outputMatrix[index,:,jj]=temp
			


		outputSpectrum={}
		outputSpectrum['Metadata']={}
		outputSpectrum['data']=outputMatrix
		outputSpectrum['Axis']=[[],[],[]]
		outputSpectrum['AxisLabel']=["","",""]
		outputSpectrum['AxisUnits']=["","",""]

		outputSpectrum['Axis'][2]=x_kAxis
		outputSpectrum['AxisUnits'][2]=r'$\AA^{-1}$'
		outputSpectrum['AxisLabel'][2]="k_X" 

		if hv!=0:
			outputSpectrum['Axis'][0]=[hv - ii - getAnalyzerWorkFunction() for ii in Ek_axis]
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Binding energy"
		else:
			outputSpectrum['Axis'][0]=Ek_axis
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Kinetic energy"			

		outputSpectrum['Axis'][1]=y_kAxis
		outputSpectrum['AxisUnits'][1]=r'$\AA^{-1}$'
		outputSpectrum['AxisLabel'][1]="k_Y"  

		if beQuiet == False: print("time taken:",time.time()-t0)
		return outputSpectrum

	def kwarp__energyAngleImage(spectrum,polar_offset=0,tilt_offset=0,resolutionDivider=1,beQuiet=False):

		def kwarp__energyAngleImage__linearInterpolation(row,column,image):

			c0 = math.floor(column)
			c1 = math.ceil(column)   
			c0_weight=c1-column
			c1_weight=column-c0
			
			interpolatedPixel=0
			if c0<image.shape[1]:	interpolatedPixel+=image[row][c0]*c0_weight
			if c1<image.shape[1]:	interpolatedPixel+=image[row][c1]*c1_weight

			return interpolatedPixel

		def k_to_alpha_manipulator(kx,ky,tilt_offset,Ek):

			tilt_rad = math.radians(tilt_offset)

			try: C = prefactor*math.sqrt(Ek)
			except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

			if (C**2-kx**2-ky**2)<0:
				#print("Impossibly large kx/ky components for this kinetic energy ({:.2f},{:.2f})".format(kx,ky))
				return np.nan

			E = math.sqrt(((C**2)-(kx**2)-(ky**2)))

			
			alpha_rad = (math.asin((math.sin(tilt_rad)*E - math.cos(tilt_rad)*ky)/C )) 

			return -math.degrees(alpha_rad) # Notice that I flipped the sign!


		source_energyAxis=spectrum['Axis'][0] # Energy axis
		source_angleAxis=spectrum['Axis'][1] # Angle axis
		im=spectrum['data']

		source_numPixels = len(source_angleAxis)
		e_midpoint = min(source_energyAxis)+((max(source_energyAxis)-min(source_energyAxis))/2)
		a_step = abs(source_angleAxis[1]-source_angleAxis[0])

		# -------------------------------------
		# Initialize the destination image
		dest_numPixels = math.ceil(source_numPixels/resolutionDivider)
		destImage = np.zeros([len(source_energyAxis),dest_numPixels])
		

		# ------------------------------------------------
		# Calculate the k axis scale of the dest image
		if polar_offset==0: kx=0
		else: kx = angle_to_kx_manipulator(alpha=0,polar_offset=polar_offset,Ek=e_midpoint)

		# ky limits - what is the largest and smallest ky value we will find in the k-warped image?
		ky_1 = angle_to_ky_manipulator(alpha=source_angleAxis[0],polar_offset=polar_offset,tilt_offset=tilt_offset,Ek=max(source_energyAxis))
		ky_2 = angle_to_ky_manipulator(alpha=source_angleAxis[-1],polar_offset=polar_offset,tilt_offset=tilt_offset,Ek=max(source_energyAxis))
				
		destImage_kAxis = np.linspace(ky_1,ky_2,dest_numPixels)

		# ------------------------------------------------
		# Extract the destination image out of the source image
		

		# This is split into two cases for speed reasons - the simple case is nearly 50% faster
		if polar_offset==0:
			# prepare for the the interpolation
			spl = scipy.interpolate.RectBivariateSpline(source_energyAxis,source_angleAxis, im,kx=1,ky=1)

			# Pre-compute some things outside of the loop for speed
			C_axis = prefactor*np.sqrt(source_energyAxis) 
			C2_axis = C_axis**2
			k2_axis = destImage_kAxis**2

			source_angleAxis_min=min(source_angleAxis)
			source_angleAxis_max=max(source_angleAxis)

			for output_energyPixel,output_Ek in enumerate(source_energyAxis): 
					
				sourceEnergy__Pixel=output_energyPixel
					
				C = C_axis[sourceEnergy__Pixel]
				C2 = C2_axis[sourceEnergy__Pixel]
				E = np.sqrt((C2-k2_axis))
					
				# Compute all angle pixels at this Ek value
				# Based on an inversion of kparr = 0.512*sqrt(Ek)*sin(alpha+tilt), except we've precomputed 0.512*sqrt(Ek) as 'C'		
				source_angle_degrees = np.degrees(np.arcsin(destImage_kAxis/C)-np.radians(tilt_offset)) 
				source_angle_degrees = [float('NaN') if (ii>source_angleAxis_max or ii<source_angleAxis_min) else ii for ii in source_angle_degrees]
					
				destImage[output_energyPixel,:]=np.nan_to_num(spl(output_Ek,source_angle_degrees,grid=False))


		else:	
			minXAngle = 90
			maxXAngle = -90
			for energy_pixel,Ek in enumerate(source_energyAxis):

				for jj,k in enumerate(destImage_kAxis):
					if beQuiet==False:
						# This calculation is not used for interpolation, just to keep track of how bad this approximation is
						x_angle = k_to_polar_manipulator(kx=kx,ky=k,polar_offset=0,tilt_offset=tilt_offset,Ek=Ek)
						if x_angle<minXAngle: minXAngle = x_angle
						if x_angle>maxXAngle: maxXAngle = x_angle
							
					y_angle = k_to_alpha_manipulator(kx=kx,ky=k,tilt_offset=tilt_offset,Ek=Ek)
						
					# Find the pixel coordinate corresponding to this angle
					sourceAnglePixel = (y_angle-source_angleAxis[0])/a_step
						
					destImage[energy_pixel,jj] = kwarp__energyAngleImage__linearInterpolation(row=energy_pixel,column=sourceAnglePixel,image=im)
				
			if beQuiet==False:
				if(abs(minXAngle-maxXAngle)>0.02):
					print("\nYou acquired this image at a polar angle of {:.3f}".format(polar_offset))
					print("This kwarp is an approximation. An error-free kwarp would require a polar map spanning {:.2f}deg to {:.2f}deg".format(minXAngle,maxXAngle))

		outputSpectrum={}
		outputSpectrum['Metadata']={}
		outputSpectrum['Axis']=[[],[]]
		outputSpectrum['AxisLabel']=["",""]
		outputSpectrum['AxisUnits']=["",""]

		outputSpectrum['Metadata']=spectrum['Metadata'].copy()
		outputSpectrum['data']=destImage
		outputSpectrum['Axis'][1]=destImage_kAxis
		outputSpectrum['AxisLabel'][1]=r"k$_{\parallel}$"
		outputSpectrum['AxisUnits'][1]=r"$\AA^{-1}$"
		if hv!=0:
			outputSpectrum['Axis'][0]=[hv - ii - getAnalyzerWorkFunction() for ii in source_energyAxis]
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Binding energy"
		else:
			outputSpectrum['Axis'][0]=source_energyAxis
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Kinetic energy"

		return outputSpectrum

	if len(np.shape(spectrum['data']))==2 and spectrum['AxisUnits'][1] in ["deg","$\\degree$"]:
		return kwarp__energyAngleImage(spectrum=spectrum,polar_offset=polar_offset,tilt_offset=tilt_offset,resolutionDivider=resolutionDivider,beQuiet=beQuiet)
	elif len(np.shape(spectrum['data']))==3 and spectrum['AxisUnits'][2]=="eV":
		return kwarp__wholeMatrix_hvscan_warp(spectrum,tilt_offset=tilt_offset,Eb_offset=Eb_offset,resolutionDivider=resolutionDivider,corrected_hvAxis=corrected_hvAxis,beQuiet=beQuiet)
	
	elif len(np.shape(spectrum['data']))==3 and spectrum['AxisLabel'][2] in ["Deflector angle","Shift X","Shift Y"]:
		return kwarp__wholeMatrix_kwarp_deflector(spectrum,polar_offset,tilt_offset,hv=hv,resolutionDivider=resolutionDivider,beQuiet=beQuiet)
	
	elif len(np.shape(spectrum['data']))==3 and spectrum['AxisUnits'][2]=="$\\degree$":
		return kwarp__wholeMatrix_kwarp(spectrum,polar_offset,tilt_offset,hv=hv,resolutionDivider=resolutionDivider,beQuiet=beQuiet)

	#elif len(np.shape(spectrum['data']))==3:
	#	return kwarp__wholeMatrix_timeScan_kwarp(spectrum,polar_offset,tilt_offset,hv=hv,resolutionDivider=resolutionDivider,energyOffset=energyOffset,beQuiet=beQuiet)

	else:
		print("I don't know how to k-warp this type of spectrum")
	


def angle_to_kx_deflector(alpha,beta,polar_offset,Ek):

	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")


	alpha_rad = -math.radians(alpha) # Notice that I flipped the sign!
	beta_rad = math.radians(beta)
	polar_rad = math.radians(polar_offset) 

	D = math.sqrt(alpha_rad**2 + beta_rad**2)
				
	# Be careful, we can't use np.sinc since that uses the engineering form sin(pi*x)/(pi*x)
	if D==0: 	sincD = 1 
	else: 		sincD = math.sin(D)/D

	kx = C * (beta_rad*math.cos(polar_rad)*sincD + math.sin(polar_rad)*math.cos(D))

	return kx


def angle_to_kx_manipulator(alpha,polar_offset,Ek):
	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	alpha_rad = math.radians(alpha)
	polar_rad = math.radians(polar_offset) 
  
	kx = C*math.sin(polar_rad)*math.cos(-alpha_rad)

	return kx

def angle_to_ky_deflector(alpha,beta,polar_offset,tilt_offset,Ek):
	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	alpha_rad = -math.radians(alpha)
	beta_rad = math.radians(beta)
	polar_rad = math.radians(polar_offset)
	tilt_rad = math.radians(tilt_offset)

	D = math.sqrt(alpha_rad**2 + beta_rad**2)

	if D==0: 	sincD = 1
	else: 		sincD = math.sin(D)/D
			
	ky = C * (sincD*(-alpha_rad*math.cos(tilt_rad)-beta_rad*math.sin(tilt_rad)*math.sin(polar_rad)) + math.cos(D)*math.sin(tilt_rad)*math.cos(polar_rad))

	return ky

def angle_to_ky_manipulator(alpha,polar_offset,tilt_offset,Ek):
	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	alpha_rad = math.radians(alpha)
	polar_rad = math.radians(polar_offset)
	tilt_rad = math.radians(tilt_offset)

	ky = C * (math.cos(-alpha_rad)*math.sin(tilt_rad)*math.cos(polar_rad) - math.cos(tilt_rad)*math.sin(-alpha_rad))

	return ky

def k_to_alpha_deflector(kx,ky,polar_offset,tilt_offset,Ek):
	polar_rad = math.radians(polar_offset)
	tilt_rad = math.radians(tilt_offset)

	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	if (C**2-kx**2-ky**2)<0:
		#print("Impossibly large kx/ky components for this kinetic energy ({:.2f},{:.2f})".format(kx,ky))
		return np.nan

	E = math.sqrt(((C**2)-(kx**2)-(ky**2)))

	st=math.sin(tilt_rad)
	ct=math.cos(tilt_rad)
	sp=math.sin(polar_rad)
	cp=math.cos(polar_rad)

	t12 = ct
	t13 = -st
	t31 = sp
	t32 = cp*st
	t33 = cp*ct

	zz = math.sqrt(C**2 - (t31*kx + t32*ky + t33*E)**2)

	if  zz == 0:	alpha_rad=0
	else:			alpha_rad = -math.acos( (t31*kx + t32*ky + t33*E)/C) * (t12*ky + t13*E) / zz
		
	return -math.degrees(alpha_rad) 



def k_to_beta_deflector(kx,ky,polar_offset,tilt_offset,Ek):

	polar_rad = math.radians(polar_offset)
	tilt_rad = math.radians(tilt_offset)

	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	if (C**2-kx**2-ky**2)<0:
		#print("Impossibly large kx/ky components for this kinetic energy ({:.2f},{:.2f})".format(kx,ky))
		return np.nan

	E = math.sqrt((C**2-kx**2-ky**2))

	st=math.sin(tilt_rad)
	ct=math.cos(tilt_rad)
	sp=math.sin(polar_rad)
	cp=math.cos(polar_rad)
		
	t21 = -cp
	t22 = sp*st
	t23 = sp*ct
	t31 = sp
	t32 = cp*st
	t33 = cp*ct

	zz = math.sqrt(C**2 - (t31*kx + t32*ky + t33*E)**2)

	if zz==0:	beta_rad= 0
	else:		beta_rad = -math.acos((t31*kx + t32*ky + t33*E)/C)  * (t21*kx + t22*ky + t23*E) /zz
		

	return math.degrees(beta_rad)


def k_to_polar_manipulator(kx,ky,polar_offset,tilt_offset,Ek):

	tilt_rad = math.radians(tilt_offset)

	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	if (C**2-kx**2-ky**2)<0:
		#print("Impossibly large kx/ky components for this kinetic energy ({:.2f},{:.2f})".format(kx,ky))
		return np.nan
		

	E = math.sqrt((C**2-kx**2-ky**2))

	polar =  (math.atan((kx) / (math.sin(tilt_rad)*ky + math.cos(tilt_rad)*E )))

	return math.degrees(polar)+polar_offset


def concatenateSpectra(s1,s2):

	assert(s1['AxisLabel'][0] == s2['AxisLabel'][0]), "The two spectra must have the same property on dimension 0 for this to work"
	assert(s1['AxisLabel'][1] == s2['AxisLabel'][1]), "The two spectra must have the same property on dimension 1 for this to work"
	assert(np.shape(s1['data'])[0] == np.shape(s2['data'])[0]), "The two spectra must have identical length energy axes for this to work"


	outputSpectrum=copy.deepcopy(s1)
	outputSpectrum['data']= np.concatenate((s1['data'], s2['data']), axis=1)
	outputSpectrum['Axis'][1]=np.concatenate((s1['Axis'][1], s2['Axis'][1]), axis=0)
	outputSpectrum['Axis'][0]=s1['Axis'][0]
	
	return outputSpectrum    
	
	
def clipSpectrum(spectrum,xRange=[None,None],yRange=[None,None]):

	assert(len(np.shape(spectrum['data'])) < 3), "Expected a 1D or 2D spectrum as input"


	if len(np.shape(spectrum['data'])) ==2:

		x,y,im = list(spectrum['Axis'][1]),list(spectrum['Axis'][0]),spectrum['data']

		if xRange[0] is None: xStartIndex=0
		else: xStartIndex = indexOfClosestValue(x,xRange[0])
		if xRange[1] is None: xEndIndex=len(x)-1
		else: xEndIndex = indexOfClosestValue(x,xRange[1])
		if yRange[0] is None: yStartIndex=0
		else: yStartIndex = indexOfClosestValue(y,yRange[0])
		if yRange[1] is None: yEndIndex=len(y)-1
		else: yEndIndex = indexOfClosestValue(y,yRange[1])


		needToFlipHorizontally=False
		needToFlipVertically=False

		if xStartIndex>xEndIndex:
			needToFlipHorizontally=True
			xStartIndex,xEndIndex = xEndIndex,xStartIndex

		if yStartIndex>yEndIndex:
			needToFlipVertically=True
			yStartIndex,yEndIndex = yEndIndex,yStartIndex

		outputSpectrum=copy.deepcopy(spectrum)
		outputSpectrum['data']=im[yStartIndex:yEndIndex+1,xStartIndex:xEndIndex+1]
		outputSpectrum['Axis'][1]=x[xStartIndex:xEndIndex+1]
		outputSpectrum['Axis'][0]=y[yStartIndex:yEndIndex+1]

		if needToFlipHorizontally:
			outputSpectrum['Axis'][1]=[ii for ii in reversed(outputSpectrum['Axis'][1])]
			outputSpectrum['data']=np.flip(outputSpectrum['data'],axis=1)

		if needToFlipVertically:
			outputSpectrum['Axis'][0]=[ii for ii in reversed(outputSpectrum['Axis'][0])]
			outputSpectrum['data']=np.flip(outputSpectrum['data'],axis=0)

		return outputSpectrum

	if len(np.shape(spectrum['data'])) ==1:

		x,data = list(spectrum['Axis']),spectrum['data']

		if xRange[0] is None: xStartIndex=0
		else: xStartIndex = indexOfClosestValue(x,xRange[0])
		if xRange[1] is None: xEndIndex=len(x)-1
		else: xEndIndex = indexOfClosestValue(x,xRange[1])

		needToFlip=False

		if xStartIndex>xEndIndex:
			needToFlip=True
			xStartIndex,xEndIndex = xEndIndex,xStartIndex


		outputSpectrum=copy.deepcopy(spectrum)
		outputSpectrum['data']=data[xStartIndex:xEndIndex+1]
		outputSpectrum['Axis']=x[xStartIndex:xEndIndex+1]

		if needToFlip:
			outputSpectrum['Axis']=[ii for ii in reversed(outputSpectrum['Axis'])]
			outputSpectrum['data']=np.flip(outputSpectrum['data'],axis=1)

		return outputSpectrum


def explorer(spectrum):
	import time
	try:
		if True in [spectrum.endswith(x) for x in [".ibw",".txt",".xy",".zip",".sp2",".itx",".nxs"]]: spectrum=loadSpectrum(spectrum,beQuiet=True)
	except AttributeError: pass

	if 'Analyzer' in spectrum['Metadata']:
		if spectrum['Metadata']['Analyzer']=="PhoibosSpin":
			print("explorer currently does not support spin EDCs/MDCs")
			return

	if len(np.shape(spectrum['data']))==3:
		return pesto.interactive.cubeExplorer(spectrum)

	elif len(np.shape(spectrum['data']))==4:
		return pesto.interactive.spatialMapExplorer(spectrum)
	#
	elif len(np.shape(spectrum['data']))==2:
		return pesto.interactive.imageExplorer(spectrum)

	else:
		print("explorer currently only supports datasets with dimension 2,3 or 4")


def indexOfClosestValue(axis,value):
	axis=list(axis)
	return axis.index(min(axis, key=lambda x:abs(x-value)))


def spatialMap__RelativeIntensityContrastImage(spectrum,ROI_Angle,ROI_AngleIntegration,ROI_Energy,ROI_EnergyIntegration,ROI2_Angle,ROI2_AngleIntegration,ROI2_Energy,ROI2_EnergyIntegration):
	
	ROI_AngleStart,ROI_AngleStop=ROI_Angle-ROI_AngleIntegration/2,ROI_Angle+ROI_AngleIntegration/2
	ROI_EnergyStart,ROI_EnergyStop=ROI_Energy-ROI_EnergyIntegration/2,ROI_Energy+ROI_EnergyIntegration/2		
	ROI2_AngleStart,ROI2_AngleStop=ROI2_Angle-ROI2_AngleIntegration/2,ROI2_Angle+ROI2_AngleIntegration/2
	ROI2_EnergyStart,ROI2_EnergyStop=ROI2_Energy-ROI2_EnergyIntegration/2,ROI2_Energy+ROI2_EnergyIntegration/2		
	
	yStartIndex = (np.abs(spectrum['Axis'][0] - ROI_EnergyStart)).argmin()
	yStopIndex = (np.abs(spectrum['Axis'][0] - ROI_EnergyStop)).argmin()
	yStartIndex2 = (np.abs(spectrum['Axis'][0] - ROI2_EnergyStart)).argmin()
	yStopIndex2 = (np.abs(spectrum['Axis'][0] - ROI2_EnergyStop)).argmin()
	if yStartIndex>yStopIndex: yStartIndex,yStopIndex=yStopIndex,yStartIndex
	if yStartIndex2>yStopIndex2: yStartIndex2,yStopIndex2=yStopIndex2,yStartIndex2
	xStartIndex = (np.abs(spectrum['Axis'][1] - ROI_AngleStart)).argmin()
	xStopIndex = (np.abs(spectrum['Axis'][1] - ROI_AngleStop)).argmin()
	xStartIndex2 = (np.abs(spectrum['Axis'][1] - ROI2_AngleStart)).argmin()
	xStopIndex2 = (np.abs(spectrum['Axis'][1] - ROI2_AngleStop)).argmin()
	if xStartIndex>xStopIndex: xStartIndex,xStopIndex=xStopIndex,xStartIndex
	if xStartIndex2>xStopIndex2: xStartIndex2,xStopIndex2=xStopIndex2,xStartIndex2

	signal_image = np.sum(spectrum['data'][yStartIndex:yStopIndex+1,xStartIndex:xStopIndex+1,:,:],axis=(0,1))
	bg_image = np.sum(spectrum['data'][yStartIndex2:yStopIndex2+1,xStartIndex2:xStopIndex2+1,:,:],axis=(0,1))
	image=signal_image.T/bg_image.T

	if np.max(image)>0:image=image/np.max(image)

	outputSpectrum={}
	outputSpectrum['Axis']=[spectrum['Axis'][3]]
	outputSpectrum['Axis'].append(spectrum['Axis'][2])
	
	outputSpectrum['AxisLabel']=[spectrum['AxisLabel'][3],spectrum['AxisLabel'][2]]
	outputSpectrum['AxisUnits']=[spectrum['AxisUnits'][3],spectrum['AxisUnits'][2]]
	outputSpectrum['Metadata']={}
	outputSpectrum['data']=image
	return outputSpectrum

def spatialMap__IntensityContrastImage(spectrum,ROI_Angle,ROI_AngleIntegration,ROI_Energy,ROI_EnergyIntegration):
	
	ROI_AngleStart,ROI_AngleStop=ROI_Angle-ROI_AngleIntegration/2,ROI_Angle+ROI_AngleIntegration/2
	ROI_EnergyStart,ROI_EnergyStop=ROI_Energy-ROI_EnergyIntegration/2,ROI_Energy+ROI_EnergyIntegration/2		

	yStartIndex = (np.abs(spectrum['Axis'][0] - ROI_EnergyStart)).argmin()
	yStopIndex = (np.abs(spectrum['Axis'][0] - ROI_EnergyStop)).argmin()
	xStartIndex = (np.abs(spectrum['Axis'][1] - ROI_AngleStart)).argmin()
	xStopIndex = (np.abs(spectrum['Axis'][1] - ROI_AngleStop)).argmin()

	if yStartIndex>yStopIndex: yStartIndex,yStopIndex=yStopIndex,yStartIndex
	if xStartIndex>xStopIndex: xStartIndex,xStopIndex=xStopIndex,xStartIndex

	signal_image = np.sum(spectrum['data'][yStartIndex:yStopIndex+1,xStartIndex:xStopIndex+1,:,:],axis=(0,1))
	image=signal_image.T
	if np.max(image)>0:image=image/np.max(image)

	outputSpectrum={}

	#if spectrum['Axis'][3][1]>spectrum['Axis'][3][0]: outputSpectrum['Axis']=[[ii for ii in reversed(spectrum['Axis'][3])]]
	#else: 
	outputSpectrum['Axis']=[spectrum['Axis'][3]]
	outputSpectrum['Axis'].append(spectrum['Axis'][2])
	
	outputSpectrum['AxisLabel']=[spectrum['AxisLabel'][3],spectrum['AxisLabel'][2]]
	outputSpectrum['AxisUnits']=[spectrum['AxisUnits'][3],spectrum['AxisUnits'][2]]
	outputSpectrum['Metadata']={}
	outputSpectrum['data']=image
	return outputSpectrum

def spatialMap__SharpnessContrastImage(spectrum,EDC_or_MDC,profileAngle,profileAngleIntegration,profileEnergy,profileEnergyIntegration,smoothing):
	profileAngleStart,profileAngleStop=profileAngle-profileAngleIntegration/2,profileAngle+profileAngleIntegration/2
	profileEnergyStart,profileEnergyStop=profileEnergy-profileEnergyIntegration/2,profileEnergy+profileEnergyIntegration/2

	yStartIndex = (np.abs(spectrum['Axis'][0] - profileEnergyStart)).argmin()
	yStopIndex = (np.abs(spectrum['Axis'][0] - profileEnergyStop)).argmin()
	xStartIndex = (np.abs(spectrum['Axis'][1] - profileAngleStart)).argmin()
	xStopIndex = (np.abs(spectrum['Axis'][1] - profileAngleStop)).argmin()
	
	if yStartIndex>yStopIndex: yStartIndex,yStopIndex=yStopIndex,yStartIndex
	if xStartIndex>xStopIndex: xStartIndex,xStopIndex=xStopIndex,xStartIndex

	if EDC_or_MDC=='MDC':
		data_subset = np.sum(copy.deepcopy(spectrum['data'][yStartIndex:yStopIndex+1,xStartIndex:xStopIndex+1,:,:]),axis=(0))
	else:
		data_subset = np.sum(spectrum['data'][yStartIndex:yStopIndex+1,xStartIndex:xStopIndex+1,:,:],axis=(1))

	smoothed=scipy.ndimage.uniform_filter1d(data_subset, smoothing, 0)	
	derivative = np.diff(smoothed, n=1, axis=0)
	derivative_smoothed = scipy.ndimage.uniform_filter1d(derivative, smoothing, 0)
	maximum = np.max(np.absolute(derivative_smoothed),axis=0)
	image=maximum.T

	outputSpectrum={}

	outputSpectrum['Axis']=[spectrum['Axis'][3]]
	outputSpectrum['Axis'].append(spectrum['Axis'][2])
	
	outputSpectrum['AxisLabel']=[spectrum['AxisLabel'][3],spectrum['AxisLabel'][2]]
	outputSpectrum['AxisUnits']=[spectrum['AxisUnits'][3],spectrum['AxisUnits'][2]]
	outputSpectrum['Metadata']={}
	outputSpectrum['data']=image
	return outputSpectrum

def spatialMap__XPSContrastImage(spectrum,signalEnergy,signalIntegration,backgroundEnergy,backgroundIntegration):

	ROI_EnergyStart,ROI_EnergyStop=signalEnergy-signalIntegration/2,signalEnergy+signalIntegration/2		
	ROI2_EnergyStart,ROI2_EnergyStop=backgroundEnergy-backgroundIntegration/2,backgroundEnergy+backgroundIntegration/2		
	
	yStartIndex = (np.abs(spectrum['Axis'][0] - ROI_EnergyStart)).argmin()
	yStopIndex = (np.abs(spectrum['Axis'][0] - ROI_EnergyStop)).argmin()
	yStartIndex2 = (np.abs(spectrum['Axis'][0] - ROI2_EnergyStart)).argmin()
	yStopIndex2 = (np.abs(spectrum['Axis'][0] - ROI2_EnergyStop)).argmin()
	if yStartIndex>yStopIndex: yStartIndex,yStopIndex=yStopIndex,yStartIndex
	if yStartIndex2>yStopIndex2: yStartIndex2,yStopIndex2=yStopIndex2,yStartIndex2
	signal_image = np.sum(spectrum['data'][yStartIndex:yStopIndex+1,:,:,:],axis=(0,1))
	bg_image = np.sum(spectrum['data'][yStartIndex2:yStopIndex2+1,:,:,:],axis=(0,1))
	image=signal_image.T/bg_image.T

	if np.max(image)>0:image=image/np.max(image)

	outputSpectrum={}
	outputSpectrum['Axis']=[spectrum['Axis'][3]]
	outputSpectrum['Axis'].append(spectrum['Axis'][2])
	outputSpectrum['AxisLabel']=[spectrum['AxisLabel'][3],spectrum['AxisLabel'][2]]
	outputSpectrum['AxisUnits']=[spectrum['AxisUnits'][3],spectrum['AxisUnits'][2]]
	outputSpectrum['Metadata']={}
	outputSpectrum['data']=image
	return outputSpectrum

def roundToNearest(axis,range):
	startIndex=indexOfClosestValue(list(axis),range[0])
	stopIndex = indexOfClosestValue(list(axis),range[1])
	start,stop = axis[startIndex],axis[stopIndex]
	if start>stop: start,stop = stop,start
	if startIndex>stopIndex: startIndex,stopIndex = stopIndex,startIndex
	return start,stop,startIndex,stopIndex

def align(spectrum):
	pesto.interactive.align(spectrum)



