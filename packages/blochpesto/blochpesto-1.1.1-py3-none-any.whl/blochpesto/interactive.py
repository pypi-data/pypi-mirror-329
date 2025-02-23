import blochpesto as pesto
from blochpesto.spin import *
import math,copy,time

try:	import pyperclip
except ImportError: print("\t(Warning): Couldn't import the pyperclip module. You will not be able to generate code templates to the clipboard. Install it from the terminal with the command 'pip install pyperclip'. (Linux users may also need to call 'sudo apt install xclip')")

try:	import numpy as np
except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")

try:	import matplotlib
except ImportError: print("\t(ERROR): Couldn't import the matplotlib module. This is required for basic functionality. Install it with the command 'pip install matplotlib'")


try:	import scipy
except ImportError: print("\t(Warning): Couldn't import the scipy module. This is required for basic functionality. Install it with the command 'pip install scipy'")

import statistics
from IPython import get_ipython
try: from astropy.convolution import convolve, Box2DKernel,Gaussian2DKernel
except ImportError: print("\t(Warning): Couldn't import the astropy module. You will not be able to produce curvature plots in explorer()")

from pathlib import Path

try:	import ipywidgets
except ImportError: print("\t(Warning): Couldn't import the ipywidgets module. You will not be able to use any interactive functions")
from IPython.display import clear_output




def despike2D(spectrum):

	def despike2D__updateHistogram(deviation,figures,overlays,thresholdFactor):
		overlays['histogram_vline'].set_xdata([thresholdFactor,thresholdFactor])

	def despike2D__updateOutput(spectrum,despiked,deviation,figures,thresholdFactor,cmaprange):
		despiked['data'][:]=spectrum['data'][:]
		despiked['data'][deviation>(thresholdFactor)]=np.nan
		coilPositiveImage,coilNegativeImage = pesto.spin.average(despiked)
		figures['coilPlus'][2].set(array=coilPositiveImage['data'],clim=cmaprange)
		figures['coilMinus'][2].set(array=coilNegativeImage['data'],clim=cmaprange)

	try:
		ipython = get_ipython()
		ipython.magic("matplotlib widget")
	except:
		pass
	assert any(ii in matplotlib.get_backend() for ii in ['ipympl','widget']), f"[Pesto Error]\nInteractive data viewers require the 'widget' backend. Execute '%matplotlib widget' to set this.\n (You are currently using '{matplotlib.get_backend()}'"


	stdev,median = pesto.spin.standardDeviation(spectrum),pesto.spin.median(spectrum)
	sourceData = spectrum['data'][:]
	deviation = np.abs(median-sourceData)/stdev
	initial_thresholdFactor=np.max(deviation)
	despiked = copy.deepcopy(spectrum)
	despiked['data'][deviation>(initial_thresholdFactor)]=np.nan

	figures,overlays={},{}

	matplotlib.pyplot.ioff()

	# Histogram plot
	fig,ax=matplotlib.pyplot.subplots(figsize=(5,4)) 
	fig.canvas.resizable = False
	fig.canvas.header_visible = False
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
	im=ax.hist(deviation.reshape(-1),bins=200,color='tab:blue',lw=0)
	ax.set_xlabel("standard deviations from median")
	ax.set_ylabel("# of occurences")
	ax.set_xlim([0,None])
	overlays['histogram_vline']=ax.axvline(x=2,ls='--',color='tab:red')
	figures['histogram']=[fig,ax,im]

	coilPositiveImage,coilNegativeImage,total=pesto.spin.sum(spectrum)


	# Filtered output, coil positive
	fig,ax=matplotlib.pyplot.subplots(figsize=(3.5,4.5)) 
	fig.canvas.resizable = False
	fig.canvas.header_visible = False
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
	im = pesto.quickPlot(coilPositiveImage,axis=ax,returnIm=True)
	ax.set_yticks([])
	ax.set_title("Coil plus sum")
	figures['coilPlus']=[fig,ax,im]

	# Filtered output, coil negative
	fig,ax=matplotlib.pyplot.subplots(figsize=(3.5,4.5)) 
	fig.canvas.resizable = False
	fig.canvas.header_visible = False
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
	im = pesto.quickPlot(coilNegativeImage,axis=ax,returnIm=True)
	ax.set_title("Coil minus sum")
	ax.set_yticks([])
	figures['coilMinus']=[fig,ax,im]

	matplotlib.pyplot.ion()

	style = {'description_width': 'initial'}

	thresholdSlider=ipywidgets.widgets.FloatSlider(
		value=np.max(deviation),min=0,max=np.max(deviation),step=0.001,description='Cutoff',continuous_update=True,
		layout=ipywidgets.Layout(width='450px'),readout_format='.3f',
		style=style
	)    

	output__colorSlider=ipywidgets.widgets.FloatRangeSlider(
		value=[np.min(spectrum['data']),np.max(spectrum['data'])],
		min=np.min(spectrum['data']),
		max=np.max(spectrum['data'])*1.4,
		step=(np.max(spectrum['data'])*2-np.min(spectrum['data']))/200,
		description='Colormap range:',
		continuous_update=True,
		readout_format='.1f',
		layout=ipywidgets.Layout(width='450px'),
		style=style)	

	histogramOutput=ipywidgets.widgets.interactive_output(despike2D__updateHistogram,{
		'deviation':ipywidgets.fixed(deviation),
		'figures':		ipywidgets.fixed(figures),
		'overlays':	ipywidgets.fixed(overlays),
		'thresholdFactor':thresholdSlider,
	})


	filteredOutput=ipywidgets.widgets.interactive_output(despike2D__updateOutput,{
		'spectrum':ipywidgets.fixed(spectrum),
		'despiked':ipywidgets.fixed(despiked),
		'deviation':ipywidgets.fixed(deviation),
		'figures':		ipywidgets.fixed(figures),
		'thresholdFactor':thresholdSlider,
		'cmaprange':output__colorSlider,
	})

	output__colorscalePanel = ipywidgets.widgets.VBox([output__colorSlider],
		layout=ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',padding='5px 5px 5px 5px',width='480px'))	

	box_layout = ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',
		padding='5px 5px 5px 5px',width='500px',align_items='center')

	controlPanel=ipywidgets.widgets.VBox([thresholdSlider,figures['histogram'][0].canvas],layout=box_layout)

	box_layout = ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',
		padding='5px 5px 5px 5px',width='680px')
	
	figurePanel=ipywidgets.widgets.HBox([figures['coilPlus'][0].canvas,figures['coilMinus'][0].canvas],layout=box_layout)
	outputPanel=ipywidgets.widgets.VBox([figurePanel,output__colorscalePanel],layout=ipywidgets.Layout(width='700px'))

	display(ipywidgets.widgets.HBox([controlPanel,outputPanel],layout=ipywidgets.Layout(width='1200px')))









def despike1D(spectrum):

	def despike1D__updateHistogram(overlays,thresholdFactor):
		overlays['histogram_vline'].set_xdata([thresholdFactor,thresholdFactor])

	def despike1D__updateOutput(spectrum,despiked,deviation,figures,thresholdFactor,yoffset):
		despiked['data'][:]=spectrum['data'][:]
		despiked['data'][deviation>(thresholdFactor)]=np.nan

		for scanIndex,scanNumber in enumerate(despiked['Axis'][1]):
			EDC = pesto.getProfile(despiked,samplingAxis='y',xAxisRange=[scanNumber,scanNumber],beQuiet=True)
			EDC['data'] += yoffset*scanIndex
			#figures['filtered'][2][scanIndex][0].set_ydata(EDC['data']) #If using lineplots instead of scatter plots
			figures['filtered'][3][scanIndex].set_offsets([[ii,jj] for ii,jj in zip(EDC['Axis'],EDC['data'])])

	try:
		ipython = get_ipython()
		ipython.magic("matplotlib widget")
	except:
		pass
	assert any(ii in matplotlib.get_backend() for ii in ['ipympl','widget']), f"[Pesto Error]\nInteractive data viewers require the 'widget' backend. Execute '%matplotlib widget' to set this.\n (You are currently using '{matplotlib.get_backend()}'"

	stdev,median = pesto.spin.standardDeviation(spectrum),pesto.spin.median(spectrum)
	sourceData = spectrum['data'][:]
	deviation = np.abs(median-sourceData)/stdev
	y_offset=np.max(median)/2

	initial_thresholdFactor=np.max(deviation)

	despiked = copy.deepcopy(spectrum)
	despiked['data'][deviation>(initial_thresholdFactor)]=np.nan

	figures={}
	overlays={}

	matplotlib.pyplot.ioff()

	# Histogram plot
	fig,ax=matplotlib.pyplot.subplots(figsize=(6,3.5)) 
	fig.canvas.resizable = False
	im=ax.hist(deviation.reshape(-1),bins=100,color='tab:blue',lw=0)
	ax.set_xlabel("# std_devs from median")
	ax.set_ylabel("# occurences")
	overlays['histogram_vline']=ax.axvline(x=2,ls='--',color='tab:red')
	figures['histogram']=[fig,ax,im]


	# filtered output plot
	fig,ax=matplotlib.pyplot.subplots(figsize=(5,5)) 
	fig.canvas.resizable = False
	
	im_filtered=[]
	im_source=[]

	for scanIndex,scanNumber in enumerate(despiked['Axis'][1]):
		EDC_filtered = pesto.getProfile(despiked,samplingAxis='y',xAxisRange=[scanNumber,scanNumber],beQuiet=True)
		EDC_filtered['data'] += y_offset*scanIndex

		EDC_source = pesto.getProfile(spectrum,samplingAxis='y',xAxisRange=[scanNumber,scanNumber],beQuiet=True)
		EDC_source['data'] += y_offset*scanIndex

		if despiked['Metadata']['CoilPolarity'][scanIndex]=='Positive': color='tab:red'
		else: color='tab:blue'
		im_source.append(pesto.quickPlot(EDC_source,axis=ax,color=color,returnIm=True))
		im_filtered.append(pesto.quickPlot(EDC_filtered,axis=ax,color=color,scatter=True,returnIm=True))

		legend_entries = [matplotlib.lines.Line2D([0], [0], color='tab:red', lw=3),matplotlib.lines.Line2D([0], [0], color='tab:blue', lw=3)]
		ax.legend(legend_entries, ['Coil+', 'Coil-'])	
	figures['filtered']=[fig,ax,im_source,im_filtered]

	#figures['filtered'][2][0].set_offsets([[ii,0] for ii in EDC['Axis']])
	matplotlib.pyplot.ion()


	style = {'description_width': 'initial'}



	thresholdSlider=ipywidgets.widgets.FloatSlider(
		value=np.max(deviation),min=0,max=np.max(deviation),step=0.01,description='Tolerance',continuous_update=True,
		layout=ipywidgets.Layout(width='450px'),
		style=style
	)    


	histogramOutput=ipywidgets.widgets.interactive_output(despike1D__updateHistogram,{
		'overlays':	ipywidgets.fixed(overlays),
		'thresholdFactor':thresholdSlider,
	})

	
	filteredOutput=ipywidgets.widgets.interactive_output(despike1D__updateOutput,{
		'spectrum':ipywidgets.fixed(spectrum),
		'despiked':ipywidgets.fixed(despiked),
		'deviation':ipywidgets.fixed(deviation),
		'figures':		ipywidgets.fixed(figures),
		'yoffset':	ipywidgets.fixed(y_offset),
		'thresholdFactor':thresholdSlider,
	})
	


	

	box_layout = ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',
		padding='5px 5px 5px 5px',width='950px')

	controlPanel=ipywidgets.widgets.VBox([thresholdSlider,figures['histogram'][0].canvas],layout=box_layout)


	box_layout = ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',
		padding='5px 5px 5px 5px',width='950px')
	
	outputPanel=ipywidgets.widgets.HBox([figures['filtered'][0].canvas],layout=box_layout)


	display(ipywidgets.widgets.HBox([controlPanel,outputPanel],layout=ipywidgets.Layout(width='1200px')))












def SBZ():
	try:
		ipython = get_ipython()
		ipython.magic("matplotlib inline")
	except:
		pass

	def SBZ__plot(structure,surface,a):
		font = {'size'   : 14}
		matplotlib.rc('font', **font)
		fig,axes=matplotlib.pyplot.subplots(ncols=2,figsize=(6,3)) 

		img = {}
		img['fcc(100)']=matplotlib.image.imread(Path(__file__).parent.joinpath("assets/fcc(100).png"))
		img['fcc(110)']=matplotlib.image.imread(Path(__file__).parent.joinpath("assets/fcc(110).png"))
		img['fcc(111)']=matplotlib.image.imread(Path(__file__).parent.joinpath("assets/fcc(111).png"))
		img['bcc(100)']=matplotlib.image.imread(Path(__file__).parent.joinpath("assets/bcc(100).png"))
		img['bcc(110)']=matplotlib.image.imread(Path(__file__).parent.joinpath("assets/bcc(110).png"))
		img['hcp(0001)']=matplotlib.image.imread(Path(__file__).parent.joinpath("assets/hcp(0001).png"))
		if surface=='(100)':
			ax=axes[0]
			ax.set_axis_off()
			if structure == 'cubic-bcc': ax.imshow(img['bcc(100)'])
			if structure == 'cubic-fcc': ax.imshow(img['fcc(100)'])

			ax=axes[1]
			a_surface = a/math.sqrt(2)
			GX = math.pi/a_surface
			GM = math.sqrt(2)*GX

			ax.add_patch(matplotlib.patches.RegularPolygon(xy=(0,0),numVertices=4,radius=GM,orientation=math.radians(45),linestyle='--',color='tab:blue',fill=False,lw=2))

			symmetryPoints=[[0,0,r"$\overline{\Gamma}$"],[GM/math.sqrt(2),GM/math.sqrt(2),r"$\overline{M}$"],[0,GX,r"$\overline{X}$"]]
			for point in symmetryPoints:	
				ax.add_patch(matplotlib.patches.Circle(xy=point[0:2],radius=GM/20,linestyle='-',color='tab:blue',fill=True,lw=1))
				ax.text(x=point[0]+GM*0.05,y=point[1]+GM*0.05,s=point[2])

			ax.set_ylim([-GM*1.5,GM*1.5])
			ax.set_xlim([-GM*1.5,GM*1.5])

		if surface=='(111)' or surface=='(0001)':
			ax=axes[0]
			if structure == 'cubic-fcc': ax.imshow(img['fcc(111)'])
			if structure == 'hcp': ax.imshow(img['hcp(0001)'])
			ax.set_axis_off()

			ax=axes[1]
			a_surface =  a/math.sqrt(2)
			GM = 2*math.pi/(np.sqrt(3)*a_surface)
			GK = GM/math.cos(math.radians(30))
			KM = GM*math.tan(math.radians(30))

			ax.add_patch(matplotlib.patches.RegularPolygon(xy=(0,0),numVertices=6,radius=GK,orientation=0,linestyle='--',color='tab:blue',fill=False,lw=2))

			symmetryPoints=[[0,0,r"$\overline{\Gamma}$"],[GM,0,r"$\overline{M}$"],[GM,GM/2,r"$\overline{K}$"]]
			for point in symmetryPoints:	
				ax.add_patch(matplotlib.patches.Circle(xy=point[0:2],radius=GK/20,linestyle='-',color='tab:blue',fill=True,lw=1))
				ax.text(x=point[0]+GK*0.05,y=point[1]+GK*0.05,s=point[2])

			ax.set_ylim([-GK*1.5,GK*1.5])
			ax.set_xlim([-GK*1.5,GK*1.5])

		if structure == 'cubic-fcc' and surface=='(110)':
			ax=axes[0]
			ax.imshow(img['fcc(110)'])
			ax.set_axis_off()

			ax=axes[1]
			GX = math.pi*math.sqrt(2) / a
			GY = math.pi/ a
			GS = math.sqrt(GX**2 + GY**2)

			ax.add_patch(matplotlib.patches.Rectangle(xy=(0-GX,0-GY),width=2*GX,height=2*GY,angle=0,linestyle='--',color='tab:blue',fill=False,lw=2))

			symmetryPoints=[[0,0,r"$\overline{\Gamma}$"],[GX,0,r"$\overline{X}$"],[GX,GY,r"$\overline{S}$"],[0,GY,r"$\overline{Y}$"]]
			for point in symmetryPoints:	
				ax.add_patch(matplotlib.patches.Circle(xy=point[0:2],radius=GS/20,linestyle='-',color='tab:blue',fill=True,lw=1))
				ax.text(x=point[0]+GS*0.05,y=point[1]+GS*0.05,s=point[2])

			ax.set_ylim([-GS*1.5,GS*1.5])
			ax.set_xlim([-GS*1.5,GS*1.5])

		if structure == 'cubic-bcc' and surface=='(110)':
			ax=axes[0]
			ax.imshow(img['bcc(110)'])
			ax.set_axis_off()

			ax=axes[1]

			G=[0,0]
			N=[0,math.sqrt(2)*math.pi/a]
			P=[math.pi/(2*a),math.sqrt(2)*math.pi/a]
			S=[math.pi/a,math.sqrt(2)*math.pi/(2*a)]
			H = [3*math.pi/(2*a),0]

			symmetryPoints=[]
			symmetryPoints.append([0,0,r"$\overline{\Gamma}$"])
			symmetryPoints.append([N[0],N[1],r"$\overline{N}$"])
			symmetryPoints.append([P[0],P[1],r"$\overline{P}$"])
			symmetryPoints.append([S[0],S[1],r"$\overline{S}$"])
			symmetryPoints.append([H[0],H[1],r"$\overline{H}$"])
			for point in symmetryPoints:	
				ax.add_patch(matplotlib.patches.Circle(xy=point[0:2],radius=N[1]/20,linestyle='-',color='tab:blue',fill=True,lw=1))
				ax.text(x=point[0]+N[1]*0.05,y=point[1]+N[1]*0.05,s=point[2])

			matplotlib.pyplot.plot([N[0],P[0],S[0],H[0]],[N[1],P[1],S[1],H[1]],ls='--',color='tab:blue',lw=2)
			matplotlib.pyplot.plot([N[0],P[0],S[0],H[0]],[-N[1],-P[1],-S[1],-H[1]],ls='--',color='tab:blue',lw=2)
			matplotlib.pyplot.plot([-N[0],-P[0],-S[0],-H[0]],[-N[1],-P[1],-S[1],-H[1]],ls='--',color='tab:blue',lw=2)
			matplotlib.pyplot.plot([-N[0],-P[0],-S[0],-H[0]],[N[1],P[1],S[1],H[1]],ls='--',color='tab:blue',lw=2)
			ax.set_ylim([-N[1]*1.5,N[1]*1.5])
			ax.set_xlim([-N[1]*1.5,N[1]*1.5])

		matplotlib.pyplot.axis('off')
		matplotlib.pyplot.show()

	def SBZ__text(structure,surface,a,hv):
		print("\n\n")

		if structure == 'cubic-fcc' and surface=='(100)':
			a_surface = a/math.sqrt(2)
			GX = np.pi/a_surface
			GM = math.sqrt(2)*GX

			GXdeg = pesto.k_to_polar_manipulator(kx=GX,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())		
			if np.isnan(GXdeg): GXdegString = "inaccessible"
			else: GXdegString = "{:.1f}\u00B0 off normal".format(GXdeg)

			GMdeg = pesto.k_to_polar_manipulator(kx=GM,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())
			if np.isnan(GMdeg): GMdegString = "inaccessible"
			else: GMdegString = "{:.1f}\u00B0 off normal".format(GMdeg)

			print("\n\tIn-plane surface lattice constant\t= a/\u221A2 \t= {:.3f} Å".format(a_surface))
			print("\tMonoatomic spacing\t\t\t= a/2\t= {:.3f} Å".format(a/2))
			print("\n\t\u0393-X \t= \u03c0\u221A2/a\n\t\t= {:.3f} Å-1 ({} at Ef with hv={}eV)".format(GX,GXdegString,hv))
			print("\n\t\u0393-M \t= \u221A2 \u0393-X\n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GM,GMdegString,hv))

		if structure == 'cubic-fcc' and surface=='(111)':	
			a_surface =  a/math.sqrt(2)
			GM = 2*math.pi/(math.sqrt(3)*a_surface)
			GK = GM/math.cos(math.radians(30))
			KM = GM*math.tan(math.radians(30))

			GMdeg = pesto.k_to_polar_manipulator(kx=GM,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())		
			if np.isnan(GMdeg): GMdegString = "inaccessible"
			else: GMdegString = "{:.1f}\u00B0 off normal".format(GMdeg)

			GKdeg = pesto.k_to_polar_manipulator(kx=GK,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())		
			if np.isnan(GKdeg): GKdegString = "inaccessible"
			else: GKdegString = "{:.1f}\u00B0 off normal".format(GKdeg)

			print("\n\tIn-plane surface lattice constant\t= a/\u221A2 \t= {:.3f} Å".format(a_surface))
			print("\tMonoatomic step height\t\t\t= a*\u221A3/3 \t= {:.3f} Å".format(a*np.sqrt(3)/3))

			print("\n\t\u0393-M \t= \u221A(2/3) 2\u03c0/a\n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GM,GMdegString,hv))
			
			print("\n\t\u0393-K \t= \u0393-M / cos(\u03c0/6)\n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GK,GKdegString,hv))
			
			print("\n\tK-M \t= \u0393-M tan(\u03c0/6)\n\t\t= {:.3f} Å-1".format(KM))

		if structure == 'cubic-fcc' and surface=='(110)':
			a1 = a
			a2 = a/math.sqrt(2)

			GX = math.pi*math.sqrt(2) / a
			GY = math.pi/ a
			GS = math.sqrt(GX**2 + GY**2)

			GXdeg = pesto.k_to_polar_manipulator(kx=GX,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())		
			if np.isnan(GXdeg): GXdegString = "inaccessible"
			else: GXdegString = "{:.1f}\u00B0 off normal".format(GXdeg)

			GYdeg = pesto.k_to_polar_manipulator(kx=GY,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())
			if np.isnan(GYdeg): GYdegString = "inaccessible"
			else: GYdegString = "{:.1f}\u00B0 off normal".format(GYdeg)

			print("\n\tSurface lattice constants:\ta1 = a ={:.3f} Å, a2=a/\u221A2 = {:.3f} Å".format(a1,a2))
			print("\n\t\u0393-X \t= \u03c0\u221A2/a \n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GX,GXdegString,hv))
			print("\n\t\u0393-Y \t= \u03c0/a \n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GY,GYdegString,hv))
			print("\n\t\u0393-S \t= \u221A(\u0393X^2 + \u0393Y^2)\t= {0:.3f} Å-1".format(GS))

		if structure == 'cubic-bcc' and surface=='(100)':
			a_surface = a
			GX = np.pi/a_surface
			GM = math.sqrt(2)*GX

			GXdeg = pesto.k_to_polar_manipulator(kx=GX,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())		
			if np.isnan(GXdeg): GXdegString = "inaccessible"
			else: GXdegString = "{:.1f}\u00B0 off normal".format(GXdeg)

			GMdeg = pesto.k_to_polar_manipulator(kx=GM,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())
			if np.isnan(GMdeg): GMdegString = "inaccessible"
			else: GMdegString = "{:.1f}\u00B0 off normal".format(GMdeg)

			print("\n\tIn-plane surface lattice constant\t= a \t= {:.3f} Å".format(a))
			print("\tMonoatomic spacing\t\t\t= a/2 \t= {:.3f} Å".format(a/2))
			print("\n\t\u0393-X \t= \u03c0/a \n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GX,GXdegString,hv))
			print("\n\t\u0393-M \t= \u221A2 \u0393-X \n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GM,GMdegString,hv))

		if structure == 'cubic-bcc' and surface=='(110)':
			a_surface =  a
			GN = math.sqrt(2)*math.pi/a
			GP = (3/2)*math.pi/a
			NP = math.pi/(2*a)
			GS = math.sqrt(3/2)*math.pi/a
			GH = 3*math.pi/(2*a)


			GNdeg = pesto.k_to_polar_manipulator(kx=GN,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())		
			if np.isnan(GNdeg): GNdegString = "inaccessible"
			else: GNdegString = "{:.1f}\u00B0 off normal".format(GNdeg)
			GHdeg = pesto.k_to_polar_manipulator(kx=GH,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())		
			if np.isnan(GHdeg): GHdegString = "inaccessible"
			else: GHdegString = "{:.1f}\u00B0 off normal".format(GHdeg)
			GSdeg = pesto.k_to_polar_manipulator(kx=GS,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())		
			if np.isnan(GSdeg): GSdegString = "inaccessible"
			else: GSdegString = "{:.1f}\u00B0 off normal".format(GSdeg)

			print("\n\tIn-plane surface lattice constant \t= a \t= {:.3f} Å".format(a_surface))

			print("\n\t\u0393-N \t= \u221A2\u03c0/a \n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GN,GNdegString,hv))
			print("\n\t\u0393-H \t= 3\u03c0/2a \n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GH,GHdegString,hv))
			print("\n\t\u0393-S \t= \u221A(3/2)\u03c0/a \n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GS,GSdegString,hv))
			print("\n\tN-P \t= \u03c0/(2a) \n\t\t= {:.3f} Å-1".format(NP))

		if (structure == 'hcp' and surface=='(0001)') or (structure == 'hexagonal' and surface=='(111)'):
			GM = 2*math.pi/(np.sqrt(3)*a)
			GK = GM/np.cos(np.deg2rad(30))
			KM = GM*np.tan(np.deg2rad(30))

			GKdeg = pesto.k_to_polar_manipulator(kx=GK,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())		
			if np.isnan(GKdeg): GKdegString = "inaccessible"
			else: GKdegString = "{:.1f}\u00B0 off normal".format(GKdeg)

			GMdeg = pesto.k_to_polar_manipulator(kx=GM,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-pesto.getAnalyzerWorkFunction())
			if np.isnan(GMdeg): GMdegString = "inaccessible"
			else: GMdegString = "{:.1f}\u00B0 off normal".format(GMdeg)

			print("\n\t\u0393-M \t= 2\u03c0/(\u221A3 a) \n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GM,GMdegString,hv))
			print("\n\t\u0393-K \t= \u0393-M/cos(30) \n\t\t= {:.3f} Å-1\t({} at Ef with hv={}eV)".format(GK,GKdegString,hv))
			print("\n\tK-M \t= \u0393-M tan(30)\n\t\t= {0:.3f} Å-1".format(KM))


	box_layout = ipywidgets.widgets.Layout(
		border='dashed 1px gray',
		margin='0px 10px 10px 0px',
		padding='5px 5px 5px 5px',
		width='700px')



	structureSelector = ipywidgets.widgets.Dropdown(
		options=['cubic-fcc','cubic-bcc','hcp','hexagonal'],
		value='cubic-fcc',
		description='Lattice')


	surfaceSelector = ipywidgets.widgets.Dropdown(
		options=['(100)','(111)','(110)','(0001)'],
		value='(100)',
		description='Surface')


	lattice_entries={}
	lattice_entries['a']=ipywidgets.widgets.BoundedFloatText(value=3,min=0.1,max=15,step=0.001,description='a',continuous_update=True,layout=ipywidgets.Layout(width='300px'))	
	photonEnergy=ipywidgets.widgets.BoundedFloatText(value=20,min=1,max=1000,step=0.1,disabled=False,description='hv',continuous_update=True,layout=ipywidgets.Layout(width='300px'))	
	
	sketch_output = ipywidgets.widgets.interactive_output(SBZ__plot,{'structure':structureSelector,'surface':surfaceSelector,'a':lattice_entries['a']})


	text_output = ipywidgets.widgets.interactive_output(SBZ__text,{
		'structure':structureSelector,
		'surface':surfaceSelector,
		'a':lattice_entries['a'],
		'hv':photonEnergy})

	def SBZ__structureUpdated(change):
		if change['new'] in ['cubic-fcc','cubic-bcc']:
			if change['new']=='cubic-fcc':
				surfaceSelector.options=['(100)','(111)','(110)']
				surfaceSelector.value=surfaceSelector.options[0]
			else:
				surfaceSelector.options=['(100)','(110)']
				surfaceSelector.value=surfaceSelector.options[0]				
		elif change['new'] in ['hcp']:
			surfaceSelector.options=['(0001)']
			surfaceSelector.value=surfaceSelector.options[0]		
		elif change['new'] in ['hexagonal']:
			surfaceSelector.options=['(111)']
			surfaceSelector.value=surfaceSelector.options[0]	

	structureSelector.observe(SBZ__structureUpdated, names='value')
	structure_panel = ipywidgets.widgets.VBox([structureSelector,surfaceSelector,lattice_entries['a'],photonEnergy],layout=box_layout)
	output_panel = ipywidgets.widgets.HBox([sketch_output,text_output])
	metaPanel = ipywidgets.widgets.VBox([structure_panel,output_panel],layout=ipywidgets.Layout(width='1200px'))

	return metaPanel



def align(spectrum):

	global mouseState
	mouseState=0

	def align__onMouseClick(event):
		global mouseState
		mouseState=1

	def align__onMouseRelease(event):
		global mouseState
		if mouseState==1:
			mouseState=0
			tiltSlider.value,polarSlider.value = event.ydata, event.xdata

	def align__onMouseDrag(event):
		global mouseState
		if mouseState==1:
			tiltSlider.value,polarSlider.value = event.ydata, event.xdata

	def align__printAngleInformation(spectrum,polar,tilt,shapeAzimuth):
		try:
			if spectrum['Metadata']['Analyzer']=="PhoibosCCD":
				print("This appears to be from the Bloch B-endstation\n")
				if shapeAzimuth<=0:
					print("To achieve the alignment depicted, change:\n\tPolar by {:.1f}\n\n\tAzimuth screw {:.1f} counter-clockwise\n\t(looking at the rear\n\tof the manipulator)\n\n".format(-polar,-shapeAzimuth))
				if shapeAzimuth>0:
					print("To achieve the alignment depicted, change:\n\tPolar by {:.1f}\n\n\tAzimuth screw {:.1f} clockwise\n\t(looking at the rear\n\tof the manipulator)\n".format(-polar,shapeAzimuth))
		except KeyError:
			pass	

		try:	
			if "DA30L" in spectrum['Metadata']['Instrument']:
				initialPolar=spectrum['Metadata']['Manipulator Polar']
				initialTilt=spectrum['Metadata']['Manipulator Tilt']
				initialAzimuth=spectrum['Metadata']['Manipulator Azimuth']
				print("This appears to be from the Bloch A-endstation\n")
				print("Measurement acquired with:\n\tPolar={:.1f}\n\tTilt={:.1f}\n\tAzimuth={:.1f}\n".format(initialPolar,initialTilt,initialAzimuth))
				print("To achieve the alignment depicted, set:\n\tPolar={:.1f}\n\tTilt={:.1f}\n\tAzimuth={:.1f}\n".format(initialPolar+polar,initialTilt+tilt,initialAzimuth+shapeAzimuth))
		except KeyError:
			pass	

	def align__updateOutput(spectrum,im,overlay,shapeType,Ek,sliceIntegration,shapeRadius,polar,tilt,shapeAzimuth,crange):

		# Update the data
		spectrumSlice=pesto.getSlice(spectrum=spectrum,axis=0,axisValue=Ek,sliceIntegration=sliceIntegration,normalized=True,beQuiet=True)
		im.set(array=spectrumSlice['data'],clim=[crange[0],crange[1]])

		# Update the overlays
		shapeAzimuth = shapeAzimuth
		if shapeType == 'Cross hairs':
			for patch in overlay['Cross hairs']:
				patch.angle=shapeAzimuth
				patch.set_visible(True)
			overlay['Cross hairs'][0].set_xy((polar-linewidth/2, tilt))
			overlay['Cross hairs'][0].set_height(shapeRadius)
			overlay['Cross hairs'][1].set_xy((polar-linewidth/2, tilt))
			overlay['Cross hairs'][1].set_height(-shapeRadius)
			overlay['Cross hairs'][2].set_xy((polar, tilt-linewidth/2))
			overlay['Cross hairs'][2].set_width(shapeRadius)
			overlay['Cross hairs'][3].set_xy((polar, tilt-linewidth/2))
			overlay['Cross hairs'][3].set_width(-shapeRadius)
			overlay['CenterCircle'].center=polar, tilt
			overlay['CenterCircle'].set_visible(True)	
		else:
			for patch in overlay['Cross hairs']: patch.set_visible(False)	
			overlay['CenterCircle'].set_visible(False)	

		if shapeType == 'Circle':
			overlay['Circle'].set_visible(True)
			overlay['Circle'].center=polar, tilt
			overlay['Circle'].set_radius(shapeRadius)
		else: overlay['Circle'].set_visible(False)

		if shapeType == 'Square (slit G-X)':
			overlay['Square (slit G-X)'].set_visible(True)
			overlay['Square (slit G-X)'].xy=polar, tilt
			overlay['Square (slit G-X)'].radius=shapeRadius
			overlay['Square (slit G-X)'].orientation=math.radians(shapeAzimuth+45)
		else: overlay['Square (slit G-X)'].set_visible(False)

		if shapeType == 'Square (slit G-M)':
			overlay['Square (slit G-M)'].set_visible(True)
			overlay['Square (slit G-M)'].xy=polar, tilt
			overlay['Square (slit G-M)'].radius=shapeRadius
			overlay['Square (slit G-M)'].orientation=math.radians(shapeAzimuth)
		else: overlay['Square (slit G-M)'].set_visible(False)

		if shapeType == 'Hexagon (slit G-K)':
			overlay['Hexagon (slit G-K)'].set_visible(True)
			overlay['Hexagon (slit G-K)'].xy=polar, tilt
			overlay['Hexagon (slit G-K)'].radius=shapeRadius
			overlay['Hexagon (slit G-K)'].orientation=math.radians(shapeAzimuth)
		else: overlay['Hexagon (slit G-K)'].set_visible(False)

		if shapeType == 'Hexagon (slit G-M)':
			overlay['Hexagon (slit G-M)'].set_visible(True)
			overlay['Hexagon (slit G-M)'].xy=polar, tilt
			overlay['Hexagon (slit G-M)'].radius=shapeRadius
			overlay['Hexagon (slit G-M)'].orientation=math.radians(shapeAzimuth+30)
		else: overlay['Hexagon (slit G-M)'].set_visible(False)



	try:
		if spectrum.endswith(".zip") or spectrum.endswith(".xy") or spectrum.endswith(".itx"): spectrum=pesto.loadSpectrum(spectrum,beQuiet=True)
	except AttributeError:
		pass

	try:
		ipython = get_ipython()
		ipython.magic("matplotlib widget")
	except:
		pass
	assert any(ii in matplotlib.get_backend() for ii in ['ipympl','widget']), f"[Pesto Error]\nInteractive data viewers require the 'widget' backend. Execute '%matplotlib widget' to set this.\n (You are currently using '{matplotlib.get_backend()}'"

	matplotlib.pyplot.ioff()
	fig,ax=matplotlib.pyplot.subplots(figsize=(5,5)) 
	matplotlib.pyplot.ion()
	fig.canvas.toolbar_visible = False
	fig.canvas.header_visible = False
	#fig.canvas.footer_visible = False
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
	fig.canvas.resizable = False

	spectrumSlice=pesto.getSlice(spectrum=spectrum,axis=0,axisValue=0,sliceIntegration=0,normalized=True,beQuiet=True)
	im=pesto.quickPlot(spectrumSlice,axis=ax,returnIm=True)
	ax.set_title("Blue line = analyzer slit")


	# Initialize patches
	overlay={}
	overlay['Cross hairs']=[]
	shapeAzimuth, polar, tilt = 0,0,0
	linewidth=1
	shapeRadius=1
	linewidth = abs(spectrum['Axis'][1][-1]/120)
	overlay['Cross hairs'].append(matplotlib.patches.Rectangle((polar-linewidth/2, tilt), width=linewidth, height=shapeRadius, angle=shapeAzimuth,color='tab:blue',fill=True,lw=0))
	overlay['Cross hairs'].append(matplotlib.patches.Rectangle((polar-linewidth/2, tilt), width=linewidth, height=-shapeRadius, angle=shapeAzimuth,color='tab:blue',fill=True,lw=0))
	overlay['Cross hairs'].append(matplotlib.patches.Rectangle((polar, tilt-linewidth/2), width=shapeRadius, height=linewidth, angle=shapeAzimuth,color='tab:red',fill=True,lw=0))
	overlay['Cross hairs'].append(matplotlib.patches.Rectangle((polar, tilt-linewidth/2), width=-shapeRadius, height=linewidth, angle=shapeAzimuth,color='tab:red',fill=True,lw=0))
	overlay['Circle']=matplotlib.patches.Circle((polar, tilt), radius=shapeRadius, linestyle='-',color='tab:red',fill=False,lw=1)
	overlay['Square (slit G-X)']=matplotlib.patches.RegularPolygon((polar, tilt), numVertices=4, radius=shapeRadius, orientation=math.radians(shapeAzimuth-45),linestyle='-',color='tab:red',fill=False,lw=1)
	overlay['Square (slit G-M)']=matplotlib.patches.RegularPolygon((polar, tilt), numVertices=4, radius=shapeRadius, orientation=math.radians(shapeAzimuth),linestyle='-',color='tab:red',fill=False,lw=1)
	overlay['Hexagon (slit G-K)']=matplotlib.patches.RegularPolygon((polar, tilt), numVertices=6, radius=shapeRadius, orientation=math.radians(shapeAzimuth),linestyle='-',color='tab:red',fill=False,lw=1)
	overlay['Hexagon (slit G-M)']=matplotlib.patches.RegularPolygon((polar, tilt), numVertices=6, radius=shapeRadius, orientation=math.radians(shapeAzimuth-30),linestyle='-',color='tab:red',fill=False,lw=1)
	circleRadius=abs(spectrum['Axis'][1][-1]/60)
	overlay['CenterCircle'] = matplotlib.patches.Circle((polar, tilt), radius=circleRadius, linestyle='-',color='tab:green',fill=True)
	
	for (key,value) in overlay.items():
		if key=='Cross hairs':
			for patch in value:
				ax.add_patch(patch)
		else:
			ax.add_patch(value)
			value.set_visible(False)


	e=list(spectrum['Axis'][0])
	d=list(spectrum['Axis'][2])
	a=list(spectrum['Axis'][1])
	shapeRadiusMax=1.5*max([max([abs(ii) for ii in a]),max([abs(ii) for ii in d])])
	e_midpoint = ((e[-1]-e[0])/2)+e[0]
	e_step = e[1]-e[0]

	style = {'description_width': 'initial'}

	shapeSelector = ipywidgets.widgets.Dropdown(
		options=['Cross hairs','Circle', 'Square (slit G-M)','Square (slit G-X)', 'Hexagon (slit G-K)','Hexagon (slit G-M)'],
		value='Cross hairs',description='Shape:',disabled=False,style=style
	) 

	EkSlider=ipywidgets.widgets.FloatSlider(
		value=e_midpoint,min=e[0],max=e[-1],step=e_step,description='Ek:',continuous_update=True,
		layout=ipywidgets.Layout(width='450px'),
		style=style
	)    
	energySliceIntegration = ipywidgets.widgets.FloatSlider(
		value=0.05,min=0,max=100*e_step,step=2*e_step,description='Integration (eV)',continuous_update=True,
		layout=ipywidgets.Layout(width='450px',description_width='100px'),style=style
	)

	radiusSlider=ipywidgets.widgets.FloatSlider(
		value=shapeRadiusMax/4,step=shapeRadiusMax/100,min=0,max=shapeRadiusMax,description='Radius of overlay   :',continuous_update=True,
		layout=ipywidgets.Layout(width='450px',description_width='100px'),style=style
	)

	polarSlider=ipywidgets.widgets.FloatSlider(
		value=0,min=-90,max=90,step=0.1,description=r'$\Delta$ Polar:',continuous_update=True,
		layout=ipywidgets.Layout(width='450px'),style=style
	) 
	tiltSlider=ipywidgets.widgets.FloatSlider(
		value=0,min=-45,max=45,step=0.1,description=r'$\Delta$ Tilt:',continuous_update=True,
		layout=ipywidgets.Layout(width='450px'),style=style
	) 
	azimuthSlider=ipywidgets.widgets.FloatSlider(
		value=0,min=-90,max=90,step=0.1,description=r'$\Delta$ Azimuth:',continuous_update=True,
		layout=ipywidgets.Layout(width='450px'),style=style
	)   

	colorscaleSlider = ipywidgets.widgets.FloatRangeSlider(
		value=[np.min(spectrum['data']),np.max(spectrum['data'])*1],
		min=np.min(spectrum['data']),max=np.max(spectrum['data'])*2,
		step=(np.max(spectrum['data'])*2-np.min(spectrum['data']))/200,
		description='Color range:',continuous_update=True,
		layout=ipywidgets.Layout(width='450px'),style=style,readout_format='.1f'
	)	

	outputPanel=ipywidgets.widgets.interactive_output(align__updateOutput,{
		'spectrum':ipywidgets.fixed(spectrum),
		'im':ipywidgets.fixed(im),
		'overlay':ipywidgets.fixed(overlay),
		'shapeType':shapeSelector,
		'Ek':EkSlider,
		'shapeRadius':radiusSlider,
		'polar':polarSlider,
		'tilt':tiltSlider,
		'shapeAzimuth':azimuthSlider,
		'sliceIntegration':energySliceIntegration,
		'crange':colorscaleSlider,
	})

	angleOutput = ipywidgets.widgets.interactive_output(align__printAngleInformation, {
		'spectrum':ipywidgets.fixed(spectrum),
		'polar':polarSlider,
		'tilt':tiltSlider,
		'shapeAzimuth':azimuthSlider})

	

	box_layout = ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',
		padding='5px 5px 5px 5px',width='470px')

	controlPanel=ipywidgets.widgets.VBox([shapeSelector,radiusSlider,EkSlider,energySliceIntegration,
		polarSlider,tiltSlider,azimuthSlider,colorscaleSlider],layout=box_layout)

	vbox1 = ipywidgets.widgets.VBox([controlPanel,angleOutput],layout=ipywidgets.Layout(width='500px'))

	fig.canvas.mpl_connect('button_press_event', align__onMouseClick)
	fig.canvas.mpl_connect('button_release_event', align__onMouseRelease)
	fig.canvas.mpl_connect('motion_notify_event', align__onMouseDrag)

	display(ipywidgets.widgets.HBox([vbox1,outputPanel,fig.canvas],layout=ipywidgets.Layout(width='950px')))

def cubeExplorer(spectrum):
	try:
		ipython = get_ipython()
		ipython.magic("matplotlib widget")
	except: pass
	# This assert should not normally trigger, as the code above attempts to switch the backend automatically. But if that fails, we need to bail
	assert any(ii in matplotlib.get_backend() for ii in ['ipympl','widget']), f"[Pesto Error]\nInteractive data viewers require the 'widget' backend. Execute '%matplotlib widget' to set this.\n (You are currently using '{matplotlib.get_backend()}'"

	font = {'size'   : 10}
	matplotlib.rc('font', **font)

	global mouseState
	mouseState=0

	# This extra state variable is needed because the tab event handler fires multiple times when changing tab.
	# With the help of this, I can make sure that there is only one reaction to a tab change.
	global CurrentlySelectedTab 
	CurrentlySelectedTab = 0

	try:
		if spectrum.endswith(".zip"): spectrum=pesto.loadSpectrum(spectrum)
	except AttributeError: pass


	global presmoothing
	presmoothing=8

	global differentiated_spectrum
	differentiated_spectrum=copy.deepcopy(spectrum)
	differentiated_spectrum['data']=scipy.ndimage.uniform_filter1d(differentiated_spectrum['data'], presmoothing, 0) #
	differentiated_spectrum['data'][1:-1,:,:] = np.diff(differentiated_spectrum['data'], n=2,axis=0)



	def cubeExplorer__recomputeDerivative():
		global presmoothing,differentiated_spectrum
		if presmoothing!=second_diff_presmoothing.value:
			presmoothing=second_diff_presmoothing.value
			differentiated_spectrum=copy.deepcopy(spectrum)
			differentiated_spectrum['data']=scipy.ndimage.uniform_filter1d(differentiated_spectrum['data'], presmoothing, 0) #
			differentiated_spectrum['data'][1:-1,:,:] = np.diff(differentiated_spectrum['data'], n=2,axis=0)
			second_diff_panel[0]['integration'].value=second_diff_panel[0]['integration'].value+0.0001

	def cubeExplorer__pasteCodeCell(figIndex):
		templateCode=""
		templateCode+="spectrum=[FILL THIS IN]\n"
		templateCode+="axisValue,integration = {:.3f},{:.3f}\n".format(panel[figIndex]['val'].value,panel[figIndex]['integration'].value)
		templateCode+="\nfig,ax=plt.subplots(figsize=(5,5))\n"
		templateCode+="\nslice=pesto.getSlice(spectrum,axis={},axisValue=axisValue,normalized=True,sliceIntegration=integration,beQuiet=True)\n\n".format(figIndex)
		templateCode+="pesto.quickPlot(slice,axis=ax,cmin={:.2f},cmax={:.2f},cmap='{}')\n".format(panel[figIndex]['crange'].value[0],
			panel[figIndex]['crange'].value[1],
			colorMapSelector.value)
		templateCode+="plt.show()"
		pyperclip.copy(templateCode)

	def cubeExplorer__pasteDerivativeCodeCell(figIndex):
		templateCode=""
		templateCode+="spectrum=[FILL THIS IN]\n"
		templateCode+="differentiated_spectrum=copy.deepcopy(spectrum)\n"
		templateCode+="presmoothing = {}\n".format(presmoothing)
		templateCode+="differentiated_spectrum['data']=scipy.ndimage.uniform_filter1d(differentiated_spectrum['data'], presmoothing, 0)\n"
		templateCode+="differentiated_spectrum['data'][1:-1,:,:] = np.diff(differentiated_spectrum['data'], n=2,axis=0)\n"
		templateCode+="\n"
		templateCode+="axisValue,integration = {:.3f},{:.3f}\n".format(second_diff_panel[figIndex]['val'].value,second_diff_panel[figIndex]['integration'].value)
		templateCode+="\nfig,ax=plt.subplots(figsize=(5,5))\n"
		templateCode+="\nslice=pesto.getSlice(differentiated_spectrum,axis={},axisValue=axisValue,normalized=True,sliceIntegration=integration,beQuiet=True)\n\n".format(figIndex)
		templateCode+="pesto.quickPlot(slice,axis=ax,cmin=-{:.2f},cmax={:.2f},cmap='{}')\n".format(second_diff_panel[figIndex]['cmax'].value,
			second_diff_panel[figIndex]['cmax'].value,
			second_diff_colorMapSelector.value)
		templateCode+="plt.show()"
		pyperclip.copy(templateCode)


	def cubeExplorer__onMouseClick(event,figIndex,canvas):
		global mouseState
		state = canvas.toolbar.mode
		if state=="": 
			mouseState=1
		else: 
			mouseState=0

	def cubeExplorer__onMouseRelease(event,figIndex,canvas):
		global mouseState
		mouseState=0
		state = canvas.toolbar.mode
		if state=="":
			if tab.selected_index==0:
				if figIndex==0:
					closestVal = min(list(spectrum['Axis'][1]), key=lambda x:abs(x-event.ydata))
					panel[1]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][2]), key=lambda x:abs(x-event.xdata))
					panel[2]['val'].value = closestVal

				if figIndex==1:
					closestVal = min(list(spectrum['Axis'][0]), key=lambda x:abs(x-event.ydata))
					panel[0]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][2]), key=lambda x:abs(x-event.xdata))
					panel[2]['val'].value = closestVal

				if figIndex==2:
					closestVal = min(list(spectrum['Axis'][0]), key=lambda x:abs(x-event.ydata))
					panel[0]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][1]), key=lambda x:abs(x-event.xdata))
					panel[1]['val'].value = closestVal

			if tab.selected_index==1:
				if figIndex==0:
					closestVal = min(list(spectrum['Axis'][1]), key=lambda x:abs(x-event.ydata))
					second_diff_panel[1]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][2]), key=lambda x:abs(x-event.xdata))
					second_diff_panel[2]['val'].value = closestVal


				if figIndex==1:
					closestVal = min(list(spectrum['Axis'][0]), key=lambda x:abs(x-event.ydata))
					second_diff_panel[0]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][2]), key=lambda x:abs(x-event.xdata))
					second_diff_panel[2]['val'].value = closestVal

				if figIndex==2:
					closestVal = min(list(spectrum['Axis'][0]), key=lambda x:abs(x-event.ydata))
					second_diff_panel[0]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][1]), key=lambda x:abs(x-event.xdata))
					second_diff_panel[1]['val'].value = closestVal

	def cubeExplorer__onMouseDrag(event,figIndex):
		global mouseState
		if mouseState==1:
			if tab.selected_index==0:
				if figIndex==0:
					closestVal = min(list(spectrum['Axis'][1]), key=lambda x:abs(x-event.ydata))
					panel[1]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][2]), key=lambda x:abs(x-event.xdata))
					panel[2]['val'].value = closestVal


				if figIndex==1:
					closestVal = min(list(spectrum['Axis'][0]), key=lambda x:abs(x-event.ydata))
					panel[0]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][2]), key=lambda x:abs(x-event.xdata))
					panel[2]['val'].value = closestVal

				if figIndex==2:
					closestVal = min(list(spectrum['Axis'][0]), key=lambda x:abs(x-event.ydata))
					panel[0]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][1]), key=lambda x:abs(x-event.xdata))
					panel[1]['val'].value = closestVal

			if tab.selected_index==1:
				if figIndex==0:
					closestVal = min(list(spectrum['Axis'][1]), key=lambda x:abs(x-event.ydata))
					second_diff_panel[1]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][2]), key=lambda x:abs(x-event.xdata))
					second_diff_panel[2]['val'].value = closestVal


				if figIndex==1:
					closestVal = min(list(spectrum['Axis'][0]), key=lambda x:abs(x-event.ydata))
					second_diff_panel[0]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][2]), key=lambda x:abs(x-event.xdata))
					second_diff_panel[2]['val'].value = closestVal

				if figIndex==2:
					closestVal = min(list(spectrum['Axis'][0]), key=lambda x:abs(x-event.ydata))
					second_diff_panel[0]['val'].value = closestVal
					closestVal = min(list(spectrum['Axis'][1]), key=lambda x:abs(x-event.xdata))
					second_diff_panel[1]['val'].value = closestVal

	def cubeExplorer__updateOutput(spectrum,ims,overlays,whichAxis,crange,xValue,yValue,zValue,xIntegration,yIntegration,zIntegration,cmap):

		integration = [xIntegration,yIntegration,zIntegration]
		value = [xValue,yValue,zValue]
		axes = [list(spectrum['Axis'][0]),list(spectrum['Axis'][1]),list(spectrum['Axis'][2])]

		spectrumSlice=pesto.getSlice(spectrum=spectrum,axis=whichAxis,axisValue=value[whichAxis],sliceIntegration=integration[whichAxis],beQuiet=True,normalized=True)
		ims[whichAxis].set(array=spectrumSlice['data'],clim=crange,cmap=cmap)
		
		if whichAxis==0:
			overlays[whichAxis][0].set_xy((-500,yValue-(yIntegration/2)))
			overlays[whichAxis][0].set_height(yIntegration)
			overlays[whichAxis][1].set_xy((zValue-(zIntegration/2),-500))
			overlays[whichAxis][1].set_width(zIntegration)
		if whichAxis==1:
			overlays[whichAxis][0].set_xy((-500,xValue-(xIntegration/2)))
			overlays[whichAxis][0].set_height(xIntegration)
			overlays[whichAxis][1].set_xy((zValue-(zIntegration/2),-500))
			overlays[whichAxis][1].set_width(zIntegration)
		if whichAxis==2:
			overlays[whichAxis][0].set_xy((-500,xValue-(xIntegration/2)))
			overlays[whichAxis][0].set_height(xIntegration)
			overlays[whichAxis][1].set_xy((yValue-(yIntegration/2),-500))
			overlays[whichAxis][1].set_width(yIntegration)

	def cubeExplorer__updateSecondDiffOutput(spectrum,ims,overlays,whichAxis,cmax,xValue,yValue,zValue,xIntegration,yIntegration,zIntegration,cmap):

		integration = [xIntegration,yIntegration,zIntegration]
		value = [xValue,yValue,zValue]
		axes = [list(differentiated_spectrum['Axis'][0]),list(differentiated_spectrum['Axis'][1]),list(differentiated_spectrum['Axis'][2])]

		spectrumSlice=pesto.getSlice(spectrum=differentiated_spectrum,axis=whichAxis,axisValue=value[whichAxis],sliceIntegration=integration[whichAxis],beQuiet=True,normalized=True)
		ims[whichAxis].set(array=spectrumSlice['data'],clim=[-cmax,cmax],cmap=cmap)
		
		if whichAxis==0:
			overlays[whichAxis][0].set_xy((-500,yValue-(yIntegration/2)))
			overlays[whichAxis][0].set_height(yIntegration)
			overlays[whichAxis][1].set_xy((zValue-(zIntegration/2),-500))
			overlays[whichAxis][1].set_width(zIntegration)
		if whichAxis==1:
			overlays[whichAxis][0].set_xy((-500,xValue-(xIntegration/2)))
			overlays[whichAxis][0].set_height(xIntegration)
			overlays[whichAxis][1].set_xy((zValue-(zIntegration/2),-500))
			overlays[whichAxis][1].set_width(zIntegration)
		if whichAxis==2:
			overlays[whichAxis][0].set_xy((-500,xValue-(xIntegration/2)))
			overlays[whichAxis][0].set_height(xIntegration)
			overlays[whichAxis][1].set_xy((yValue-(yIntegration/2),-500))
			overlays[whichAxis][1].set_width(yIntegration)



	ims,figs,overlays = [],[],[]
	matplotlib.pyplot.ioff()

	for panel in [0,1,2]:
		fig,ax=matplotlib.pyplot.subplots(figsize=(3.5,4)) 
		figs.append(fig)
		spectrumSlice=pesto.getSlice(spectrum=spectrum,axis=panel,axisValue=0,sliceIntegration=0,normalized=True,beQuiet=True)
		ims.append(pesto.quickPlot(spectrumSlice,axis=ax,returnIm=True))
		figs[-1].canvas.toolbar_visible = 'fade-in-fade-out'
		figs[-1].canvas.header_visible = False
		#fig.canvas.footer_visible = False
		figs[-1].canvas.resizable = False
		figs[-1].canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
		
		overlays.append([])
		overlays[-1].append(matplotlib.patches.Rectangle((-500, -1), width=1000, height=2, angle=0,color='tab:blue',fill=False,lw=1,ls='--'))
		ax.add_patch(overlays[-1][-1])
		overlays[-1].append(matplotlib.patches.Rectangle((-1, -500), width=2, height=1000, angle=0,color='tab:red',fill=False,lw=1,ls='--'))
		ax.add_patch(overlays[-1][-1])

	matplotlib.pyplot.ion()
	matplotlib.pyplot.tight_layout()

	

	box_layout = ipywidgets.widgets.Layout(
		border='dashed 1px gray',
		margin='0px 10px 10px 0px',
		padding='5px 5px 5px 5px',
		width='930px')

	colorMapSelector = ipywidgets.widgets.Dropdown(value='bone_r', description='Colormap:',
	options=['bone_r', 'inferno', 'viridis','plasma', 'cividis','gray','OrRd','PuBuGn','coolwarm','bwr'])

	colorscale_panel = ipywidgets.widgets.VBox([colorMapSelector],layout=box_layout)

	box_layout = ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',padding='5px 5px 5px 5px',width='500px')


	style = {'description_width': 'initial'}

	panel=[{},{},{}]
	fig= []
	axes=[]
	copyToClipBoardButton=[None,None,None]
	for axis in [0,1,2]:
		ax=list(spectrum['Axis'][axis])
		ax_midpoint = ax[int(len(ax)/2)]
		ax_step = abs(ax[1]-ax[0])	
		ax_range=abs(ax[-1]-ax[0])


		panel[axis]['val']=ipywidgets.widgets.SelectionSlider(
								options=[("{:.3f}".format(i),i) for i in ax],
								value=ax_midpoint,
								description='{}'.format(spectrum['AxisLabel'][axis]),
								continuous_update=True,
								layout=ipywidgets.Layout(width='300px'),
								style=style)
		panel[axis]['crange']=ipywidgets.widgets.FloatRangeSlider(
							value=[np.min(spectrum['data']),np.max(spectrum['data'])*1],
							min=np.min(spectrum['data']),
							max=np.max(spectrum['data'])*2,
							step=(np.max(spectrum['data'])*2-np.min(spectrum['data']))/400,
							description='Color scale:',
							readout_format='.1f',
							continuous_update=True,
							layout=ipywidgets.Layout(width='300px'),
							style=style)	

		panel[axis]['integration']=ipywidgets.widgets.FloatSlider(
									value=0,
									min=0,
									max=ax_range,
									step=ax_step,
									description='Integration ({})'.format(spectrum['AxisUnits'][axis]),
									layout=ipywidgets.Layout(width='300px',description_width='100px'),
									continuous_update=True,
									style=style)	

		copyToClipBoardButton[axis] = ipywidgets.Button(description='Copy template code to clipboard',layout=ipywidgets.Layout(width='auto') )	
		copyToClipBoardButton[axis].on_click(lambda clicked, x=axis: cubeExplorer__pasteCodeCell(x)) 
	
	for axis in [0,1,2]:

		panel[axis]['output']=ipywidgets.widgets.interactive_output(cubeExplorer__updateOutput,{
								'spectrum':ipywidgets.fixed(spectrum),
								'ims':ipywidgets.fixed(ims),
								'whichAxis':ipywidgets.fixed(axis),
								'overlays':ipywidgets.fixed(overlays),
								'crange':panel[axis]['crange'],
								'xValue':panel[0]['val'],
								'yValue':panel[1]['val'],
								'zValue':panel[2]['val'],
								'xIntegration':panel[0]['integration'],
								'yIntegration':panel[1]['integration'],
								'zIntegration':panel[2]['integration'],
								'cmap':colorMapSelector
								})
		panel[axis]['widget'] = ipywidgets.widgets.VBox([figs[axis].canvas,panel[axis]['val'],panel[axis]['crange'],panel[axis]['integration'],copyToClipBoardButton[axis]],layout=box_layout)
		panel[axis]['widget'].children[0].layout.height = '450px'

	outputPanel = ipywidgets.widgets.HBox([panel[0]['widget'],panel[1]['widget'],panel[2]['widget']],layout=ipywidgets.Layout(width='1200px'))
	metaPanel = ipywidgets.widgets.VBox([colorscale_panel,outputPanel],layout=ipywidgets.Layout(width='1200px'))
	
	##-------------------------------------------------------------------------------------------------------

	second_diff_colorMapSelector = ipywidgets.widgets.Dropdown(value='bone_r', description='Colormap:',
	options=['bone','bone_r','gray','gray_r'])
	second_diff_colorscale_panel = ipywidgets.widgets.VBox([second_diff_colorMapSelector],layout=box_layout)

	second_diff_presmoothing = ipywidgets.widgets.IntSlider(
									value=presmoothing,
									min=1,
									max=50,
									step=1,
									description='Pre-derivative smoothing',
									layout=ipywidgets.Layout(width='400px',description_width='100px'),
									continuous_update=True,
									style=style)	
	
	second_diff_presmoothing.on_trait_change(cubeExplorer__recomputeDerivative)
	second_diff_presmoothing_panel = ipywidgets.widgets.VBox([second_diff_presmoothing],layout=box_layout)


	second_diff_panel=[{},{},{}]
	second_diff_copyToClipBoardButton=[None,None,None]
	for axis in [0,1,2]:
		ax=list(spectrum['Axis'][axis])
		ax_midpoint = ax[int(len(ax)/2)]
		ax_step = abs(ax[1]-ax[0])	
		ax_range=abs(ax[-1]-ax[0])

		second_diff_panel[axis]['val']=ipywidgets.widgets.SelectionSlider(
								options=[("{:.3f}".format(i),i) for i in ax],
								value=ax_midpoint,
								description='{}'.format(spectrum['AxisLabel'][axis]),
								continuous_update=True,
								layout=ipywidgets.Layout(width='300px'),
								style=style)

		second_diff_panel[axis]['cmax']=ipywidgets.widgets.FloatSlider(
							value=50,
							min=0,
							max=300,
							step=0.1,
							description='Color range:',
							readout_format='.1f',
							continuous_update=True,
							layout=ipywidgets.Layout(width='300px'),
							style=style)

		second_diff_panel[axis]['integration']=ipywidgets.widgets.FloatSlider(
									value=0,
									min=0,
									max=ax_range,
									step=ax_step,
									description='Integration ({})'.format(spectrum['AxisUnits'][axis]),
									layout=ipywidgets.Layout(width='300px',description_width='100px'),
									continuous_update=True,
									style=style)	
		second_diff_copyToClipBoardButton[axis] = ipywidgets.Button(description='Copy template code to clipboard',layout=ipywidgets.Layout(width='auto') )	
		second_diff_copyToClipBoardButton[axis].on_click(lambda clicked, x=axis: cubeExplorer__pasteDerivativeCodeCell(x))
	
	for axis in [0,1,2]:
		second_diff_panel[axis]['output']=ipywidgets.widgets.interactive_output(cubeExplorer__updateSecondDiffOutput,{
								'spectrum':ipywidgets.fixed(spectrum),
								'ims':ipywidgets.fixed(ims),
								'whichAxis':ipywidgets.fixed(axis),
								'overlays':ipywidgets.fixed(overlays),
								'cmax':second_diff_panel[axis]['cmax'],
								'xValue':second_diff_panel[0]['val'],
								'yValue':second_diff_panel[1]['val'],
								'zValue':second_diff_panel[2]['val'],
								'xIntegration':second_diff_panel[0]['integration'],
								'yIntegration':second_diff_panel[1]['integration'],
								'zIntegration':second_diff_panel[2]['integration'],
								'cmap':second_diff_colorMapSelector
								})

		second_diff_panel[axis]['widget'] = ipywidgets.widgets.VBox([figs[axis].canvas,second_diff_panel[axis]['val'],
			second_diff_panel[axis]['cmax'],
			second_diff_panel[axis]['integration'],
			second_diff_copyToClipBoardButton[axis]],layout=box_layout)
		second_diff_panel[axis]['widget'].children[0].layout.height = '450px'
	

	second_diff_configPanel = ipywidgets.widgets.HBox([second_diff_colorscale_panel,second_diff_presmoothing_panel],layout=ipywidgets.Layout(width='1200px'))
	second_diff_outputPanel = ipywidgets.widgets.HBox([second_diff_panel[0]['widget'],second_diff_panel[1]['widget'],second_diff_panel[2]['widget']],layout=ipywidgets.Layout(width='1200px'))
	second_diff_metaPanel = ipywidgets.widgets.VBox([second_diff_configPanel,second_diff_outputPanel],layout=ipywidgets.Layout(width='1200px'))
	
	tab = ipywidgets.Tab(children = [metaPanel,second_diff_metaPanel])
	[tab.set_title(i, title) for i, title in enumerate(["Main","Second derivative"])]

	for ii in [0,1,2]:
		figs[ii].canvas.mpl_connect('button_press_event', lambda event,x=ii,canvas=figs[ii].canvas: cubeExplorer__onMouseClick(event,x,canvas))
		figs[ii].canvas.mpl_connect('button_release_event', lambda event,x=ii,canvas=figs[ii].canvas: cubeExplorer__onMouseRelease(event,x,canvas))
		figs[ii].canvas.mpl_connect('motion_notify_event', lambda event,x=ii: cubeExplorer__onMouseDrag(event,x))

	def cubeExplorer__tab_eventhandler():
		global CurrentlySelectedTab

		if tab.selected_index==0 and CurrentlySelectedTab==1: #Changing to Main tab
			panel[0]['val'].value=second_diff_panel[0]['val'].value
			panel[1]['val'].value=second_diff_panel[1]['val'].value
			panel[2]['val'].value=second_diff_panel[2]['val'].value
			panel[0]['integration'].value=second_diff_panel[0]['integration'].value+0.0001 # change something insignficant by an insignificant amount to trigger the redraw
			CurrentlySelectedTab=0

		elif tab.selected_index==1 and CurrentlySelectedTab==0: #Coming to second derivative tab from the main tab

			second_diff_panel[0]['val'].value=panel[0]['val'].value
			second_diff_panel[1]['val'].value=panel[1]['val'].value
			second_diff_panel[2]['val'].value=panel[2]['val'].value
			second_diff_panel[0]['integration'].value=panel[0]['integration'].value+0.0001
			CurrentlySelectedTab=1


	tab.on_trait_change(cubeExplorer__tab_eventhandler)
	tab.selected_index=0

	
	val = panel[0]['integration'].value
	panel[0]['integration'].value=val+0.0001 # change something insignficant by an insignificant amount to trigger the redraw
	return tab











def imageExplorer(spectrum,hv=0):
	try:
		if spectrum.endswith(".ibw") or spectrum.endswith(".txt"): spectrum=pesto.loadSpectrum(spectrum,beQuiet=True)
	except AttributeError: pass

	try:
		ipython = get_ipython()
		ipython.magic("matplotlib widget")
	except:
		pass
	assert any(ii in matplotlib.get_backend() for ii in ['ipympl','widget']), f"[Pesto Error]\nInteractive data viewers require the 'widget' backend. Execute '%matplotlib widget' to set this.\n (You are currently using '{matplotlib.get_backend()}'"

	#--------------------------------

	def imageExplorer__reloadInput(self):
		
		try:

			colorSliderMaxRelativePosition = mainPlot__colorSlider.value[1]/mainPlot__colorSlider.max
			colorSliderMinRelativePosition = mainPlot__colorSlider.value[0]/mainPlot__colorSlider.max
			
			newSpectrum = pesto.loadSpectrum(spectrum['Metadata']['CurrentFilePath'])
			spectrum['data'] = newSpectrum['data']
			
			mainPlot__colorSlider.max=np.max(spectrum['data'])*1.4
			mainPlot__colorSlider.value=[colorSliderMinRelativePosition*mainPlot__colorSlider.max,colorSliderMaxRelativePosition*mainPlot__colorSlider.max]
			#

			val = EDC__xintegration.value
			EDC__xintegration.value=val+0.01
			EDC__xintegration.value=val

			val = MDC__xcenter.value
			MDC__xcenter.value=val+0.01
			MDC__xcenter.value=val

			val = secondDerivative__colorSlider.value
			secondDerivative__colorSlider.value=val+0.01
			secondDerivative__colorSlider.value=val		
			

		except Exception as e:
			print("Something went wrong with imageExplorer__reloadInput:",e)
			pass
		
		


	def imageExplorer__updateOutput(spectrum,figures,cmaprange,cmap):
		figures['main'][2].set(array=spectrum['data'],clim=cmaprange,cmap=cmap)
		
	def imageExplorer__MDCUpdateOutput(spectrum,mainPlot__overlays,figures,position,integration,x_range,x_center):
		profile = pesto.getProfile(spectrum,samplingAxis='x',yAxisRange=[position-integration/2,position+integration/2],
			xAxisRange=[x_center-x_range/2,x_center+x_range/2],beQuiet=True)
		
		mainPlot__overlays['MDC'].set_xy((x_center-x_range/2, position-integration/2))
		mainPlot__overlays['MDC'].set_height(integration)
		mainPlot__overlays['MDC'].set_width(x_range)
		mainPlot__overlays['MDC'].set_visible(True)
		mainPlot__overlays['EDC'].set_visible(False)
		figures['MDC'][2][0].set_ydata(profile['data'])
		figures['MDC'][2][0].set_xdata(profile['Axis'])
		figures['MDC'][1].set_xlim(profile['Axis'][0],profile['Axis'][-1])
		figures['MDC'][1].set_ylim([min(profile['data']),min(profile['data'])+(max(profile['data'])-min(profile['data']))*1.1])

	def imageExplorer__EDCUpdateOutput(spectrum,mainPlot__overlays,figures,position,integration,y_range,y_center):	
		profile = pesto.getProfile(spectrum,samplingAxis='y',xAxisRange=[position-integration/2,position+integration/2],
			yAxisRange=[y_center-y_range/2,y_center+y_range/2],beQuiet=True)		

		mainPlot__overlays['EDC'].set_xy((position-integration/2,y_center-y_range/2))
		mainPlot__overlays['EDC'].set_width(integration)
		mainPlot__overlays['EDC'].set_height(y_range)
		mainPlot__overlays['MDC'].set_visible(False)
		mainPlot__overlays['EDC'].set_visible(True)

		figures['EDC'][2][0].set_ydata(profile['data'])
		figures['EDC'][2][0].set_xdata(profile['Axis'])
		figures['EDC'][1].set_xlim(profile['Axis'][0],profile['Axis'][-1])
		figures['EDC'][1].set_ylim([min(profile['data']),min(profile['data'])+(max(profile['data'])-min(profile['data']))*1.1])


	def imageExplorer__curvature_2D(data, x, y, smoothingX=1,smoothingY=1, Cx=0.001, Cy=0.001):
		# Based on: Zhang et al, https://doi.org/10.1063/1.3585113
		if smoothingX!=0 and smoothingY!=0:
			data_smth = convolve(data, Gaussian2DKernel(smoothingX,smoothingY), boundary='extend')
		else:
			data_smth=data
		dx = np.gradient(data_smth, axis=1)
		dy = np.gradient(data_smth, axis=0)
		d2x = np.gradient(np.gradient(data_smth, x, axis=1), x, axis=1)
		d2y = np.gradient(np.gradient(data_smth, y, axis=0), y, axis=0)
		dxdy = np.gradient(np.gradient(data_smth, y, axis=0), x, axis=1)

		curvature_2D = ((1 + Cx*dx**2)*Cy*d2y - 2*Cx*Cy*dx*dy*dxdy + (1 + Cy*dy**2)*Cx*d2x) / (1 + Cx*dx**2 + Cy*dy**2)**1.5

		return curvature_2D

	def imageExplorer__secondDerivativeUpdateOutput(spectrum,figures,whichAxis,derivativeOrder,presmoothing,postsmoothing,cmaprange):
		if derivativeOrder=="First": derivativeOrder = 1
		else: derivativeOrder = 2

		if whichAxis=="Energy":whichAxis=0
		else:whichAxis=1

		spectrumCopy=copy.deepcopy(spectrum)
		spectrumCopy['data']=scipy.ndimage.uniform_filter1d(spectrumCopy['data'], int(presmoothing), whichAxis)
		spectrumCopy['data'] = np.diff(spectrumCopy['data'], n=derivativeOrder,axis=whichAxis)
		spectrumCopy['data']=scipy.ndimage.uniform_filter1d(spectrumCopy['data'], int(postsmoothing), whichAxis)
		figures['secondDerivative'][2].set(array=spectrumCopy['data'],clim=[-cmaprange,cmaprange],cmap='gray_r')



	def imageExplorer__curvatureUpdateOutput(spectrum,figures,presmoothingX,presmoothingY,Cx,Cy,cmaprange):
		spectrumCopy=copy.deepcopy(spectrum)

		spectrumCopy['data']=imageExplorer__curvature_2D(spectrumCopy['data'],spectrumCopy['Axis'][1],spectrumCopy['Axis'][0],smoothingX=presmoothingX,smoothingY=presmoothingY,Cx=Cx,Cy=Cy)

		figures['curvature'][2].set(array=spectrumCopy['data'],clim=[-cmaprange,cmaprange],cmap='Greys')


	def imageExplorer__pasteMDCcode(self):
		templateCode="spectrum=[FILL THIS IN]\n"
		templateCode+="energy,integration = {},{}\n".format(MDC__yslider.value,MDC__yintegration.value)
		templateCode+="angleCenter,angleRange = {},{}\n".format(MDC__xcenter.value,MDC__xrange.value)
		templateCode+="\nfig,axes=matplotlib.pyplot.subplots(figsize=(9,4),ncols=2)\n\n"
		templateCode+="ax=axes[0]\n"
		templateCode+="pesto.quickPlot(spectrum,axis=ax,cmin={},cmax={},cmap='{}')\n".format(mainPlot__colorSlider.value[0],mainPlot__colorSlider.value[1],mainPlot__colorMapSelector.value)
		templateCode+="ax.add_patch(matplotlib.patches.Rectangle((angleCenter-angleRange/2, energy-integration/2),width=angleRange,height=integration, color='tab:red',fill=False,lw=1))\n"
		templateCode+="\nax=axes[1]\n"
		templateCode+="MDC = pesto.getProfile(spectrum=spectrum,samplingAxis='x',xAxisRange=[angleCenter-angleRange/2,angleCenter+angleRange/2],yAxisRange=[energy-integration/2,energy+integration/2],beQuiet=True)\n"
		templateCode+="pesto.quickPlot(MDC,axis=ax)\n"
		templateCode+="\nplt.tight_layout()\nplt.show()"
		pyperclip.copy(templateCode)

	def imageExplorer__pasteEDCcode(self):
		templateCode="spectrum=[FILL THIS IN]\n"
		templateCode+="angle,integration = {},{}\n".format(xslider.value,EDC__xintegration.value)
		templateCode+="energyCenter,energyRange = {},{}\n".format(EDC_ycenter.value,EDC_yrange.value)
		templateCode+="\nfig,axes=matplotlib.pyplot.subplots(figsize=(9,4),ncols=2)\n\n"
		templateCode+="ax=axes[0]\n"
		templateCode+="pesto.quickPlot(spectrum,axis=ax,cmin={},cmax={},cmap='{}')\n".format(mainPlot__colorSlider.value[0],mainPlot__colorSlider.value[1],mainPlot__colorMapSelector.value)
		templateCode+="ax.add_patch(matplotlib.patches.Rectangle((angle-integration/2, energyCenter-energyRange/2),width=integration,height=energyRange, color='tab:red',fill=False,lw=1))\n"
		templateCode+="\nax=axes[1]\n"
		templateCode+="EDC = pesto.getProfile(spectrum=spectrum,samplingAxis='y',xAxisRange=[angle-integration/2,angle+integration/2],yAxisRange=[energyCenter-energyRange/2,energyCenter+energyRange/2],beQuiet=True)\n"
		templateCode+="pesto.quickPlot(EDC,axis=ax)\n"
		templateCode+="\nplt.tight_layout()\nplt.show()"
		pyperclip.copy(templateCode)

	def imageExplorer__pastederivativecode(self):
		templateCode="import copy,scipy\nimport numpy as np\n"
		templateCode+="\nspectrum=[FILL THIS IN]\n"
		templateCode+="presmoothing,postsmoothing = {},{}\n".format(secondDerivative__preSmoothingSlider.value,secondDerivative__postSmoothingSlider.value)
		if secondDerivative__derivativeOrder.value=='First':derivativeOrder=1
		else:derivativeOrder=2
		if secondDerivative__whichAxisToggle.value=='Energy':whichAxis=0
		else:whichAxis=1
		templateCode+="derivativeOrder,whichAxis = {},{}\n".format(derivativeOrder,whichAxis)
		templateCode+="\nfig,ax=matplotlib.pyplot.subplots(figsize=(5,6))\n\n"	
		templateCode+="spectrumCopy=copy.deepcopy(spectrum)\n"
		templateCode+="spectrumCopy['data']=scipy.ndimage.uniform_filter1d(spectrumCopy['data'], presmoothing, whichAxis)\n"
		templateCode+="spectrumCopy['data']=scipy.ndimage.uniform_filter1d(spectrumCopy['data'], presmoothing, whichAxis)\n"
		templateCode+="spectrumCopy['data'] = np.diff(spectrumCopy['data'], n=derivativeOrder,axis=whichAxis)\n"
		templateCode+="spectrumCopy['data']=scipy.ndimage.uniform_filter1d(spectrumCopy['data'], postsmoothing, whichAxis)\n"
		templateCode+="pesto.quickPlot(spectrumCopy,axis=ax,cmin={},cmax={},cmap='gray_r')\n".format(-secondDerivative__colorSlider.value,secondDerivative__colorSlider.value)
		templateCode+="plt.show()"
		pyperclip.copy(templateCode)

	def imageExplorer__pastecurvaturecode(self):
		templateCode="import copy,scipy\nimport numpy as np\n"
		templateCode+="from astropy.convolution import convolve, Box2DKernel,Gaussian2DKernel"
		templateCode+="\nspectrum=[FILL THIS IN]\n"
		templateCode+="spectrumCopy=copy.deepcopy(spectrum)\n"

		
		templateCode+="smoothingX,smoothingY = {},{}\n".format(curvature__preSmoothingX.value,curvature__preSmoothingY.value)
		templateCode+="x,y = spectrumCopy['Axis'][1],spectrumCopy['Axis'][0]\n"

		templateCode+="Cx,Cy = {},{}\n".format(curvature__Cx.value,curvature__Cy.value)

		templateCode+="\nfig,ax=plt.subplots(figsize=(5,6))\n\n"	
		templateCode+="data_smth = convolve(spectrumCopy['data'], Gaussian2DKernel(smoothingX,smoothingY), boundary='extend')\n"

		templateCode+="dx = np.gradient(data_smth, axis=1)\n"
		templateCode+="dy = np.gradient(data_smth, axis=0)\n"
		templateCode+="d2x = np.gradient(np.gradient(data_smth, x, axis=1), x, axis=1)\n"
		templateCode+="d2y = np.gradient(np.gradient(data_smth, y, axis=0), y, axis=0)\n"
		templateCode+="dxdy = np.gradient(np.gradient(data_smth, y, axis=0), x, axis=1)\n"
		templateCode+="spectrumCopy['data'] = ((1 + Cx*dx**2)*Cy*d2y - 2*Cx*Cy*dx*dy*dxdy + (1 + Cy*dy**2)*Cx*d2x) / (1 + Cx*dx**2 + Cy*dy**2)**1.5\n"
		templateCode+="pesto.quickPlot(spectrumCopy,axis=ax,cmin={},cmax={},cmap='gray_r')\n".format(-curvature__colorSlider.value,curvature__colorSlider.value)
		templateCode+="plt.show()"
		pyperclip.copy(templateCode)

	figures={}

	# Prepare the main image plot
	matplotlib.pyplot.ioff()
	fig,ax=matplotlib.pyplot.subplots(figsize=(5,5)) 
	matplotlib.pyplot.ion()
	fig.canvas.toolbar_visible = 'fade-in-fade-out'
	fig.canvas.header_visible = False
	fig.canvas.footer_visible = True
	fig.canvas.resizable = False
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
	im=pesto.quickPlot(spectrum,axis=ax,returnIm=True)
	figures['main']=[fig,ax,im]

	mainPlot__overlays={}
	mainPlot__overlays['MDC']=matplotlib.patches.Rectangle(
		(spectrum['Axis'][1][0], spectrum['Axis'][0][0]), 
		width=abs(spectrum['Axis'][1][0]-spectrum['Axis'][1][-1]), 
		height=abs(spectrum['Axis'][0][0]-spectrum['Axis'][0][1]), 
		color='tab:red',fill=False,lw=1)
	mainPlot__overlays['EDC']=matplotlib.patches.Rectangle(
		(spectrum['Axis'][1][0], spectrum['Axis'][0][0]), 
		width=abs(spectrum['Axis'][1][0]-spectrum['Axis'][1][1]), 
		height=abs(spectrum['Axis'][0][0]-spectrum['Axis'][0][-1]), 
		color='tab:red',fill=False,lw=1)

	ax.add_patch(mainPlot__overlays['MDC'])
	ax.add_patch(mainPlot__overlays['EDC'])

	# Prepare the MDC plot
	matplotlib.pyplot.ioff()
	fig,ax=matplotlib.pyplot.subplots(figsize=(3.5,2)) 
	matplotlib.pyplot.ion()
	fig.canvas.toolbar_visible = 'fade-in-fade-out'
	fig.canvas.header_visible = False
	fig.canvas.footer_visible = True
	fig.canvas.resizable = False
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
	MDC=pesto.getProfile(spectrum,samplingAxis='x',beQuiet=True)
	im=pesto.quickPlot(MDC,axis=ax,returnIm=True)
	figures['MDC']=[fig,ax,im]

	# Prepare the EDC plot
	matplotlib.pyplot.ioff()
	fig,ax=matplotlib.pyplot.subplots(figsize=(3.5,2)) 
	matplotlib.pyplot.ion()
	fig.canvas.toolbar_visible = 'fade-in-fade-out'
	fig.canvas.header_visible = False
	fig.canvas.footer_visible = True
	fig.canvas.resizable = False
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
	EDC=pesto.getProfile(spectrum,samplingAxis='y',beQuiet=True)
	im=pesto.quickPlot(EDC,axis=ax,returnIm=True)
	figures['EDC']=[fig,ax,im]

	# Prepare the second derivative plot
	matplotlib.pyplot.ioff()
	fig,ax=matplotlib.pyplot.subplots(figsize=(5,5)) 
	matplotlib.pyplot.ion()
	fig.canvas.toolbar_visible = 'fade-in-fade-out'
	fig.canvas.header_visible = False
	fig.canvas.footer_visible = True
	fig.canvas.resizable = False
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
	spectrumCopy=copy.deepcopy(spectrum)
	spectrumCopy['data']=scipy.ndimage.uniform_filter1d(spectrumCopy['data'], 5, 0)
	spectrumCopy['data'] = np.diff(spectrumCopy['data'], n=1,axis=0)
	im=pesto.quickPlot(spectrumCopy,axis=ax,returnIm=True)
	figures['secondDerivative']=[fig,ax,im]

	# Prepare the curvature plot

	matplotlib.pyplot.ioff()
	fig,ax=matplotlib.pyplot.subplots(figsize=(5,5)) 
	matplotlib.pyplot.ion()
	fig.canvas.toolbar_visible = 'fade-in-fade-out'
	fig.canvas.header_visible = False
	fig.canvas.footer_visible = True
	fig.canvas.resizable = False
	spectrumCopy=copy.deepcopy(spectrum)
	spectrumCopy['data'] = imageExplorer__curvature_2D(spectrumCopy['data'],spectrumCopy['Axis'][1],spectrumCopy['Axis'][0],Cx=0.001,Cy=0.001)
	im=pesto.quickPlot(spectrumCopy,axis=ax,returnIm=True,cmap='Greys')
	figures['curvature']=[fig,ax,im]


	# ----- Main plot controls ----------
	style = {'description_width': 'initial'}

	mainPlot__colorSlider=ipywidgets.widgets.FloatRangeSlider(
		value=[np.min(spectrum['data']),np.max(spectrum['data'])],
		min=np.min(spectrum['data']),
		max=np.max(spectrum['data'])*1.4,
		step=(np.max(spectrum['data'])*2-np.min(spectrum['data']))/200,
		description='Colormap range:',
		continuous_update=True,
		readout_format='.1f',
		layout=ipywidgets.Layout(width='450px'),
		style=style)	

	mainPlot__colorMapSelector = ipywidgets.widgets.Dropdown(
		options=['bone_r', 'inferno', 'viridis','plasma', 'cividis','gray','OrRd','PuBuGn','coolwarm','bwr'],
		value='bone_r',
		description='Colormap:',)

	mainPlot__colorscalePanel = ipywidgets.widgets.VBox(
		[mainPlot__colorSlider,mainPlot__colorMapSelector],
		layout=ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',padding='5px 5px 5px 5px',width='480px'))

	mainPlot__Output = ipywidgets.widgets.interactive_output(imageExplorer__updateOutput,{
		'spectrum':ipywidgets.fixed(spectrum),
		'figures':ipywidgets.fixed(figures),
		'cmaprange':mainPlot__colorSlider,
		'cmap':mainPlot__colorMapSelector,
		})

	reloadButton = ipywidgets.Button(description='Reload source file',layout=ipywidgets.Layout(width='350px') )	
	reloadButton.on_click(imageExplorer__reloadInput) 

	mainPlot__panel = ipywidgets.widgets.VBox([figures['main'][0].canvas,mainPlot__colorscalePanel,reloadButton],
		layout=ipywidgets.Layout(width='650px'))

	# ----- MDC controls ----------

	ymin, ymax = spectrum['Axis'][0][0], spectrum['Axis'][0][-1]
	if ymax<ymin: ymax,ymin=ymin,ymax
	yrange=abs(spectrum['Axis'][0][-1]-spectrum['Axis'][0][0])
	ystep=abs(spectrum['Axis'][0][1]-spectrum['Axis'][0][0])
	
	xmin, xmax = spectrum['Axis'][1][0], spectrum['Axis'][1][-1]
	if xmax<xmin: xmax,xmin=xmin,xmax
	xrange=abs(spectrum['Axis'][1][-1]-spectrum['Axis'][1][0])
	xstep=abs(spectrum['Axis'][1][1]-spectrum['Axis'][1][0])

	MDC__yslider=ipywidgets.widgets.FloatSlider(
		value=ymin+(yrange/2),min=ymin,max=ymax,step=ystep,description="",continuous_update=True,
		layout=ipywidgets.Layout(width='340px'),style=style)  
	MDC__yintegration=ipywidgets.widgets.FloatSlider(
		value=0,min=0,max=yrange,step=ystep,description="{} integration".format(spectrum['AxisLabel'][0]),continuous_update=True,
		layout=ipywidgets.Layout(width='340px'),style=style)  
	MDC__xcenter=ipywidgets.widgets.FloatSlider(
		value=xmin+(xmax-xmin)/2,min=xmin,max=xmax,step=xstep,description="",continuous_update=True,
		layout=ipywidgets.Layout(width='340px'),style=style)  
	MDC__xrange=ipywidgets.widgets.FloatSlider(
		value=xrange/2,min=0,max=xrange,step=xstep,description="{} range".format(spectrum['AxisLabel'][1]),continuous_update=True,
		layout=ipywidgets.Layout(width='340px'),style=style)    

	MDC__Output = ipywidgets.widgets.interactive_output(imageExplorer__MDCUpdateOutput,{
		'spectrum':ipywidgets.fixed(spectrum),
		'figures':ipywidgets.fixed(figures),
		'mainPlot__overlays': ipywidgets.fixed(mainPlot__overlays),
		'position': MDC__yslider,
		'integration':MDC__yintegration,
		'x_center': MDC__xcenter,
		'x_range': MDC__xrange})

	MDC__copyToClipBoardButton = ipywidgets.Button(description='Copy template code to clipboard',layout=ipywidgets.Layout(width='350px') )	
	MDC__copyToClipBoardButton.on_click(imageExplorer__pasteMDCcode) 

	MDC__panel = ipywidgets.widgets.VBox(
		[MDC__yintegration,MDC__xrange,figures['MDC'][0].canvas,MDC__copyToClipBoardButton],
		layout=ipywidgets.Layout(width='550px'))


	# ----- EDC controls ----------

	xmin, xmax = spectrum['Axis'][1][0], spectrum['Axis'][1][-1]
	if xmax<xmin: xmax,xmin=xmin,xmax
	x_range=abs(spectrum['Axis'][1][-1]-spectrum['Axis'][1][0])
	xstep=abs(spectrum['Axis'][1][1]-spectrum['Axis'][1][0])

	xslider=ipywidgets.widgets.FloatSlider(
		value=xmin+(x_range/2),min=xmin,max=xmax,step=xstep,description="",continuous_update=True,
		layout=ipywidgets.Layout(width='340px'),style=style)    
	EDC__xintegration=ipywidgets.widgets.FloatSlider(
		value=0,min=0,max=x_range,step=xstep,description="{} integration".format(spectrum['AxisLabel'][1]),
		continuous_update=True,layout=ipywidgets.Layout(width='340px'),style=style)  
	EDC_ycenter=ipywidgets.widgets.FloatSlider(
		value=ymin+(ymax-ymin)/2,min=ymin,max=ymax,step=ystep,description="",continuous_update=True,
		layout=ipywidgets.Layout(width='340px'),style=style) 
	EDC_yrange=ipywidgets.widgets.FloatSlider(
		value=(ymax-ymin)/2,min=0,max=ymax-ymin,step=ystep,description="{} range".format(spectrum['AxisLabel'][0]),
		continuous_update=True,layout=ipywidgets.Layout(width='340px'),style=style) 

	EDCOutput = ipywidgets.widgets.interactive_output(imageExplorer__EDCUpdateOutput,{
		'spectrum':ipywidgets.fixed(spectrum),
		'figures':ipywidgets.fixed(figures),
		'mainPlot__overlays': ipywidgets.fixed(mainPlot__overlays),
		'position': xslider,
		'integration':EDC__xintegration,
		'y_center': EDC_ycenter,
		'y_range': EDC_yrange})

	EDC__copyToClipBoardButton = ipywidgets.Button(description='Copy template code to clipboard',layout=ipywidgets.Layout(width='350px') )	
	EDC__copyToClipBoardButton.on_click(imageExplorer__pasteEDCcode) 
	
	EDC_panel = ipywidgets.widgets.VBox(
		[EDC__xintegration,EDC_yrange,figures['EDC'][0].canvas,EDC__copyToClipBoardButton],
		layout=ipywidgets.Layout(width='550px'))

	profilesTab = ipywidgets.Tab(children = [MDC__panel,EDC_panel])
	[profilesTab.set_title(i, title) for i, title in enumerate(["MDC","EDC"])]

	mainTab=ipywidgets.widgets.HBox([mainPlot__panel,profilesTab],layout=ipywidgets.Layout(width='1100px'))



	# ------------ Next tab: second derivative ------------------

	secondDerivative__derivativeOrder=ipywidgets.widgets.RadioButtons(
		options=['First', 'Second'],description='Derivative order:',
		value='Second',style=style)

	secondDerivative__whichAxisToggle=ipywidgets.widgets.RadioButtons(
		options=['Energy', 'Angle'],description='Which axis:',
		value='Energy',style=style)

	secondDerivative__preSmoothingSlider=ipywidgets.widgets.IntSlider(
		value=8,min=1,max=36,step=1,description='Pre-derivative smoothing:',
		continuous_update=True,style=style)  

	secondDerivative__postSmoothingSlider=ipywidgets.widgets.IntSlider(
		value=8,min=1,max=36,step=1,description='Post-derivative smoothing:',
		continuous_update=True,style=style)  

	secondDerivative__colorSlider=ipywidgets.widgets.FloatSlider(
		value=10,min=0,max=50,step=0.1,description='Color range:',
		continuous_update=True,style=style) 

	secondDerivative__panel = ipywidgets.widgets.VBox(
		[secondDerivative__whichAxisToggle,secondDerivative__derivativeOrder,secondDerivative__preSmoothingSlider,secondDerivative__postSmoothingSlider],
		layout=ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',padding='5px 5px 5px 5px',width='350px'))

	secondDerivative__colorscalePanel = ipywidgets.widgets.VBox([secondDerivative__colorSlider],
		layout=ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',padding='5px 5px 5px 5px',width='350px'))


	secondDerivative__Output = ipywidgets.widgets.interactive_output(imageExplorer__secondDerivativeUpdateOutput,{
		'spectrum':ipywidgets.fixed(spectrum),
		'figures':ipywidgets.fixed(figures),
		'derivativeOrder': secondDerivative__derivativeOrder,
		'whichAxis':secondDerivative__whichAxisToggle,
		'presmoothing':secondDerivative__preSmoothingSlider,
		'postsmoothing':secondDerivative__postSmoothingSlider,
		'cmaprange':secondDerivative__colorSlider,
		})

	secondDerivative__copyToClipBoardButton = ipywidgets.Button(description='Copy template code to clipboard',layout=ipywidgets.Layout(width='350px') )	
	secondDerivative__copyToClipBoardButton.on_click(imageExplorer__pastederivativecode) 

	vbox1 = ipywidgets.widgets.VBox([figures['secondDerivative'][0].canvas,secondDerivative__colorscalePanel,reloadButton],layout=ipywidgets.Layout(width='550px'))
	vbox2 = ipywidgets.widgets.VBox([secondDerivative__panel,secondDerivative__copyToClipBoardButton],layout=ipywidgets.Layout(width='550px'))

	secondDerivativeTab=ipywidgets.widgets.HBox([vbox1,vbox2],layout=ipywidgets.Layout(width='1000px'))



	# ------------ Next tab: curvature ------------------


	curvature__preSmoothingX=ipywidgets.widgets.BoundedFloatText(
		value=2,min=0,max=30,step=1,description='Pre-smoothing X',
		continuous_update=True,style=style)  

	curvature__preSmoothingY=ipywidgets.widgets.BoundedFloatText(
		value=2,min=0,max=30,step=1,description='Pre-smoothing Y',
		continuous_update=True,style=style)  

	curvature__Cx=ipywidgets.widgets.BoundedFloatText(
		value=1e-3,min=1e-12,max=1e12,description='Cx',
		continuous_update=True,style=style)  

	curvature__Cy=ipywidgets.widgets.BoundedFloatText(
		value=1e-3,min=1e-12,max=1e12,description='Cy',
		continuous_update=True,style=style)  

	curvature__colorSlider=ipywidgets.widgets.FloatSlider(
		value=5,min=0,max=500,step=0.01,description='Color range:',
		continuous_update=True,style=style)  

	curvatureControlPanel = ipywidgets.widgets.VBox(
		[curvature__preSmoothingX,curvature__preSmoothingY,curvature__Cx,curvature__Cy,curvature__colorSlider],
		layout=ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',padding='5px 5px 5px 5px',width='350px'))

	curvatureTabOutput = ipywidgets.widgets.interactive_output(imageExplorer__curvatureUpdateOutput,{
		'spectrum':ipywidgets.fixed(spectrum),
		'figures':ipywidgets.fixed(figures),
		'presmoothingX':curvature__preSmoothingX,
		'presmoothingY':curvature__preSmoothingY,
		'Cx':curvature__Cx,
		'Cy':curvature__Cy,
		'cmaprange':curvature__colorSlider,
		})

	curvature__copyToClipBoardButton = ipywidgets.Button(description='Copy template code to clipboard',layout=ipywidgets.Layout(width='350px') )	
	curvature__copyToClipBoardButton.on_click(imageExplorer__pastecurvaturecode) 


	vbox1 = ipywidgets.widgets.VBox([figures['curvature'][0].canvas],layout=ipywidgets.Layout(width='550px'))
	vbox2 = ipywidgets.widgets.VBox([curvatureControlPanel,curvature__copyToClipBoardButton],layout=ipywidgets.Layout(width='550px'))

	curvatureTab=ipywidgets.widgets.HBox([vbox1,vbox2],layout=ipywidgets.Layout(width='1000px'))


	tab = ipywidgets.Tab(children = [mainTab,secondDerivativeTab,curvatureTab])
	[tab.set_title(i, title) for i, title in enumerate(["Main","Second derivative","Curvature"])]

	#tab = ipywidgets.Tab(children = [mainTab,secondDerivativeTab])
	#[tab.set_title(i, title) for i, title in enumerate(["Main","Second derivative"])]


	global mouseState
	mouseState=0

	def imageExplorer__onClick(event,canvas):
		print("HAHAHAH")
		global mouseState
		state = canvas.toolbar.mode
		if state=="":
			if mouseState==0: mouseState=1
			if profilesTab.selected_index==0: #MDC
				MDC__yslider.value=event.ydata
				MDC__xcenter.value=event.xdata
			if profilesTab.selected_index==1: #EDC
				xslider.value=event.xdata
				EDC_ycenter.value=event.ydata

	def imageExplorer__onRelease(event):
		global mouseState
		mouseState=0

	def imageExplorer__clickDrag(event):
		global mouseState
		if mouseState==1: 
			try:
				if profilesTab.selected_index==0: #MDC
					MDC__yslider.value=event.ydata
					MDC__xcenter.value=event.xdata
				if profilesTab.selected_index==1: #EDC
					xslider.value=event.xdata
					EDC_ycenter.value=event.ydata
			except:
				pass
	
	figures['main'][0].canvas.mpl_connect('button_press_event', lambda event: imageExplorer__onClick(event,figures['main'][0].canvas))
	figures['main'][0].canvas.mpl_connect('button_release_event', imageExplorer__onRelease)
	figures['main'][0].canvas.mpl_connect('motion_notify_event', imageExplorer__clickDrag)

	def imageExplorer__tab_eventhandler(change):
		if profilesTab.selected_index==0: #MDC
			imageExplorer__MDCUpdateOutput(
				spectrum=spectrum,
				figures=figures,
				mainPlot__overlays=mainPlot__overlays,
				position=MDC__yslider.value,
				integration=MDC__yintegration.value,
				x_center=MDC__xcenter.value,
				x_range=MDC__xrange.value)
		if profilesTab.selected_index==1: #EDC
			imageExplorer__EDCUpdateOutput(
				spectrum=spectrum,
				figures=figures,
				mainPlot__overlays=mainPlot__overlays,
				position=xslider.value,
				integration=EDC__xintegration.value,
				y_center=EDC_ycenter.value,
				y_range=EDC_yrange.value)

	
	profilesTab.on_trait_change(imageExplorer__tab_eventhandler)

	profilesTab.selected_index=1


	display(tab)





def spatialMapExplorer(spectrum):

	style = {'description_width': 'initial'}

	flip_x_axis = False
	flip_y_axis = False

	def spatialMapExplorer__updateRelativeIntensityOutput(spectrum,figures,frame_overlays,ROI_Angle,ROI_AngleIntegration,ROI_Energy,ROI_EnergyIntegration,ROI2_Angle,ROI2_AngleIntegration,ROI2_Energy,ROI2_EnergyIntegration):
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

		figures['XY_map'][2].set(array=image)

		#	figures['XY_map'][2].set(array=image)
		for ii in frame_overlays:
			frame_overlays[ii].set_visible(False)

		frame_overlays['IntensityRelative_SignalROI'].set_visible(True)
		frame_overlays['IntensityRelative_SignalROI'].set_xy((ROI_AngleStart, ROI_EnergyStart))
		frame_overlays['IntensityRelative_SignalROI'].set_width(ROI_AngleIntegration)
		frame_overlays['IntensityRelative_SignalROI'].set_height(ROI_EnergyIntegration)
		frame_overlays['IntensityRelative_BackgroundROI'].set_visible(True)
		frame_overlays['IntensityRelative_BackgroundROI'].set_xy((ROI2_AngleStart, ROI2_EnergyStart))
		frame_overlays['IntensityRelative_BackgroundROI'].set_width(ROI2_AngleIntegration)
		frame_overlays['IntensityRelative_BackgroundROI'].set_height(ROI2_EnergyIntegration)

	def spatialMapExplorer__updateRelativeIntensityXPSOutput(spectrum,figures,frame_overlays,ROI_Energy,ROI_EnergyIntegration,ROI2_Energy,ROI2_EnergyIntegration):
		ROI_EnergyStart,ROI_EnergyStop=ROI_Energy-ROI_EnergyIntegration/2,ROI_Energy+ROI_EnergyIntegration/2		
		ROI2_EnergyStart,ROI2_EnergyStop=ROI2_Energy-ROI2_EnergyIntegration/2,ROI2_Energy+ROI2_EnergyIntegration/2		
	
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
		#if flip_x_axis == True: image=np.flip(image,axis=1)
		#if flip_y_axis == True: image=np.flip(image,axis=0)

		figures['XY_map'][2].set(array=image)

		for ii in frame_overlays:
			frame_overlays[ii].set_visible(False)

		frame_overlays['IntensityRelativeXPS_signalROI'].set_visible(True)
		frame_overlays['IntensityRelativeXPS_signalROI'].set_xy((ROI_EnergyStart, 0))
		frame_overlays['IntensityRelativeXPS_signalROI'].set_width(ROI_EnergyIntegration)
		frame_overlays['IntensityRelativeXPS_signalROI'].set_height(1e12)
		frame_overlays['IntensityRelativeXPS_BackgroundROI'].set_visible(True)
		frame_overlays['IntensityRelativeXPS_BackgroundROI'].set_xy((ROI2_EnergyStart, 0))
		frame_overlays['IntensityRelativeXPS_BackgroundROI'].set_width(ROI2_EnergyIntegration)
		frame_overlays['IntensityRelativeXPS_BackgroundROI'].set_height(1e12)

	def spatialMapExplorer__updateIntensityOutput(spectrum,figures,frame_overlays,ROI_Angle,ROI_AngleIntegration,ROI_Energy,ROI_EnergyIntegration):

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

		figures['XY_map'][2].set(array=image)

		for ii in frame_overlays:
			frame_overlays[ii].set_visible(False)

		frame_overlays['IntensityROI'].set_visible(True)
		frame_overlays['IntensityROI'].set_xy((ROI_AngleStart, ROI_EnergyStart))
		frame_overlays['IntensityROI'].set_width(ROI_AngleIntegration)
		frame_overlays['IntensityROI'].set_height(ROI_EnergyIntegration)

	def spatialMapExplorer__updateMDCSharpnessOutput(spectrum,figures,frame_overlays,profileAngle,profileAngleIntegration,profileEnergy,profileEnergyIntegration,smoothing):
		profileAngleStart,profileAngleStop=profileAngle-profileAngleIntegration/2,profileAngle+profileAngleIntegration/2
		profileEnergyStart,profileEnergyStop=profileEnergy-profileEnergyIntegration/2,profileEnergy+profileEnergyIntegration/2

		yStartIndex = (np.abs(spectrum['Axis'][0] - profileEnergyStart)).argmin()
		yStopIndex = (np.abs(spectrum['Axis'][0] - profileEnergyStop)).argmin()
		if yStartIndex>yStopIndex: yStartIndex,yStopIndex=yStopIndex,yStartIndex
		xStartIndex = (np.abs(spectrum['Axis'][1] - profileAngleStart)).argmin()
		xStopIndex = (np.abs(spectrum['Axis'][1] - profileAngleStop)).argmin()
		if xStartIndex>xStopIndex: xStartIndex,xStopIndex=xStopIndex,xStartIndex

		# np.sum is a bit strange sometimes. It's 10x slower than the equivalent call in the EDC function. 
		# Giving it a copy of the input matrix rather than a reference makes this twice as fast, but for the
		# EDC function the copy.deepcopy() addition makes it twice as slow

		data_subset = np.sum(copy.deepcopy(spectrum['data'][yStartIndex:yStopIndex+1,xStartIndex:xStopIndex+1,:,:]),axis=(0))

		smoothed=scipy.ndimage.uniform_filter1d(data_subset, smoothing, 0)	
		derivative = np.diff(smoothed, n=1, axis=0)
		derivative_smoothed = scipy.ndimage.uniform_filter1d(derivative, smoothing, 0)
		maximum = np.max(np.absolute(derivative_smoothed),axis=0)
		image=maximum.T

		if np.max(image)>0:image=image/np.max(image)

		figures['XY_map'][2].set(array=image)

		for ii in frame_overlays:
			frame_overlays[ii].set_visible(False)

		frame_overlays['MDC'].set_visible(True)
		frame_overlays['MDC'].set_xy((profileAngleStart, profileEnergyStart))
		frame_overlays['MDC'].set_width(profileAngleIntegration)
		frame_overlays['MDC'].set_height(profileEnergyIntegration)



	def spatialMapExplorer__updateEDCSharpnessOutput(spectrum,figures,frame_overlays,profileAngle,profileAngleIntegration,profileEnergy,profileEnergyIntegration,smoothing):
		profileAngleStart,profileAngleStop=profileAngle-profileAngleIntegration/2,profileAngle+profileAngleIntegration/2
		profileEnergyStart,profileEnergyStop=profileEnergy-profileEnergyIntegration/2,profileEnergy+profileEnergyIntegration/2

		yStartIndex = (np.abs(spectrum['Axis'][0] - profileEnergyStart)).argmin()
		yStopIndex = (np.abs(spectrum['Axis'][0] - profileEnergyStop)).argmin()
		if yStartIndex>yStopIndex: yStartIndex,yStopIndex=yStopIndex,yStartIndex
		xStartIndex = (np.abs(spectrum['Axis'][1] - profileAngleStart)).argmin()
		xStopIndex = (np.abs(spectrum['Axis'][1] - profileAngleStop)).argmin()
		if xStartIndex>xStopIndex: xStartIndex,xStopIndex=xStopIndex,xStartIndex

		data_subset = np.sum(spectrum['data'][yStartIndex:yStopIndex+1,xStartIndex:xStopIndex+1,:,:],axis=(1))

		smoothed=scipy.ndimage.uniform_filter1d(data_subset, smoothing, 0)	
		derivative = np.diff(smoothed, n=1, axis=0)
		derivative_smoothed = scipy.ndimage.uniform_filter1d(derivative, smoothing, 0)
		maximum = np.max(np.absolute(derivative_smoothed),axis=0)
		image=maximum.T
		if np.max(image)>0:image=image/np.max(image)
		figures['XY_map'][2].set(array=image)

		for ii in frame_overlays:
			frame_overlays[ii].set_visible(False)

		frame_overlays['EDC'].set_visible(True)
		frame_overlays['EDC'].set_xy((profileAngleStart, profileEnergyStart))
		frame_overlays['EDC'].set_width(profileAngleIntegration)
		frame_overlays['EDC'].set_height(profileEnergyIntegration)

	def spatialMapExplorer__updateCoordinates(spectrum,figures,map_overlays,majorVal,minorVal):
	
		try: majorAxis,minorAxis = spectrum['majorAxis'],spectrum['minorAxis']
		except: majorAxis,minorAxis = spectrum['Axis'][3],spectrum['Axis'][2]

		majorAxisStep=abs(majorAxis[1]-majorAxis[0])
		minorAxisStep=abs(minorAxis[1]-minorAxis[0])

		map_overlays['Crosshair_hline'].set_ydata(majorVal)
		map_overlays['Crosshair_vline'].set_xdata(minorVal)
		map_overlays['Crosshair_box'].set_xy((minorVal-minorAxisStep/2,majorVal-majorAxisStep/2 ))

		try: majorAxisLabel,minorAxisLabel = spectrum['majorAxisLabel'],spectrum['minorAxisLabel']
		except: majorAxisLabel,minorAxisLabel = spectrum['AxisLabel'][3],spectrum['AxisLabel'][2]
		spectrumSlice=pesto.getFrameFrom4DScan(spectrum=spectrum,axes=[minorAxisLabel,majorAxisLabel],axisValues=[minorVal,majorVal],beQuiet=True)

		if tab.selected_index==4: #XPS relative
			EDC=pesto.getProfile(spectrum=spectrumSlice,samplingAxis='y',beQuiet=True)
			figures['DetectorImageCollapsed'][2][0].set_ydata(EDC['data'])
			figures['DetectorImageCollapsed'][1].set_ylim([min(EDC['data']),max(EDC['data'])*1.1])
			figures['DetectorImageCollapsed'][1].set_title("X,Y = ({:.3f},{:.3f})".format(minorVal,majorVal))
		else:
			figures['DetectorImage'][2].set(array=spectrumSlice['data'])
			figures['DetectorImage'][1].set_title("X,Y = ({:.3f},{:.3f})".format(minorVal,majorVal))

	def spatialMapExplorer__updateMap_cmap(figures,mapcrange,cmap):
		mapcmin,mapcmax=mapcrange[0],mapcrange[1]
		figures['XY_map'][2].set(clim=[mapcmin,mapcmax],cmap=cmap)

	def spatialMapExplorer__updateDetectorImage_cmap(figures,mapcrange,cmap):
		mapcmin,mapcmax=mapcrange[0],mapcrange[1]
		figures['DetectorImage'][2].set(clim=[mapcmin,mapcmax],cmap=cmap)

	try:
		ipython = get_ipython()
		ipython.magic("matplotlib widget")
	except:
		pass
	assert any(ii in matplotlib.get_backend() for ii in ['ipympl','widget']), f"[Pesto Error]\nInteractive data viewers require the 'widget' backend. Execute '%matplotlib widget' to set this.\n (You are currently using '{matplotlib.get_backend()}'"


	# ----------------- Assets common to all tabs---------------------------------------------------------
	tab = ipywidgets.Tab()
	
	figure={}
	map_overlays={}
	frame_overlays={}
	matplotlib.pyplot.ioff()

	# Define the detector frame plot
	fig,ax=matplotlib.pyplot.subplots(figsize=(4.5,4.5)) 
	fig.canvas.header_visible = False
	fig.canvas.resizable = False
	spectrumSlice=pesto.getFrameFrom4DScan(spectrum=spectrum,axes=['X','Y'],axisValues=[0,0],beQuiet=True)
	im=pesto.quickPlot(spectrumSlice,axis=ax,returnIm=True)
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
	figure['DetectorImage']=[fig,ax,im]

	# Define the collapsed detector frame plot (for XPS mode)

	fig,ax=matplotlib.pyplot.subplots(figsize=(5,5)) 

	fig.canvas.header_visible = False
	fig.canvas.resizable = False
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]
	EDC=pesto.getProfile(spectrum=spectrumSlice,samplingAxis='y',beQuiet=True)
	im=pesto.quickPlot(EDC,axis=ax,returnIm=True)
	figure['DetectorImageCollapsed']=[fig,ax,im]


	# Define the contrast map plot, AND controls for its colormapping

	fig,ax=matplotlib.pyplot.subplots(figsize=(5,5)) 
	matplotlib.pyplot.ion()
	map_overlays['Crosshair_hline']=ax.axhline(color='tab:blue',ls='--')
	map_overlays['Crosshair_vline']=ax.axvline(color='tab:blue',ls='--')
	try: majorAxis,minorAxis = spectrum['majorAxis'],spectrum['minorAxis']
	except: majorAxis,minorAxis = spectrum['Axis'][3],spectrum['Axis'][2]
	majorAxisStep=abs(majorAxis[1]-majorAxis[0])
	minorAxisStep=abs(minorAxis[1]-minorAxis[0])

	map_overlays['Crosshair_box']=matplotlib.patches.Rectangle((0,0), height=majorAxisStep, width=minorAxisStep,linestyle='-',color='tab:red',fill=False,lw=2)
	ax.add_patch(map_overlays['Crosshair_box']) 

	fig.canvas.toolbar_visible = 'fade-in-fade-out'
	fig.canvas.header_visible = False
	fig.canvas.resizable = False
	fig.canvas.toolbar.toolitems = [ii for ii in fig.canvas.toolbar.toolitems if ii[0] not in ('Back','Forward','Pan','Download')]


	spectrumSlice=pesto.getFrameFrom4DScan(spectrum=spectrum,axes=[spectrum['AxisLabel'][0],spectrum['AxisLabel'][1]],axisValues=[0,0],beQuiet=True)
	spectrumSlice['data']=spectrumSlice['data'].T
	spectrumSlice['Axis'][0],spectrumSlice['Axis'][1]=spectrumSlice['Axis'][1],spectrumSlice['Axis'][0]

	#if spectrumSlice['Axis'][1][0]>spectrumSlice['Axis'][1][1]:
	#	spectrumSlice['data']=np.flip(spectrumSlice['data'],axis=0)
	#	#spectrumSlice['Axis'][1]=np.flip(spectrumSlice['Axis'][1])
	#	spectrumSlice['Axis'][1]=np.flip(spectrumSlice['Axis'][1])


	spectrumSlice['AxisLabel'][0],spectrumSlice['AxisLabel'][1]=spectrumSlice['AxisLabel'][1],spectrumSlice['AxisLabel'][0]
	spectrumSlice['AxisUnits'][0],spectrumSlice['AxisUnits'][1]=spectrumSlice['AxisUnits'][1],spectrumSlice['AxisUnits'][0]
	im=pesto.quickPlot(spectrumSlice,axis=ax,returnIm=True)
	figure['XY_map']=[fig,ax,im]
	fig.colorbar(im,ax=ax)



	frame_overlays['MDC']=matplotlib.patches.Rectangle(
		(spectrum['Axis'][0][0], spectrum['Axis'][0][0]), 
		width=abs(spectrum['Axis'][1][0]-spectrum['Axis'][1][-1]), 
		height=abs(spectrum['Axis'][0][0]-spectrum['Axis'][0][1]), 
		color='tab:red',fill=False,lw=1,ls='--')
	figure['DetectorImage'][1].add_patch(frame_overlays['MDC'])

	frame_overlays['EDC']=matplotlib.patches.Rectangle(
		(spectrum['Axis'][1][0], spectrum['Axis'][0][0]), 
		width=abs(spectrum['Axis'][1][0]-spectrum['Axis'][1][1]), 
		height=abs(spectrum['Axis'][0][0]-spectrum['Axis'][0][-1]), 
		color='tab:red',fill=False,lw=1,ls='--')
	figure['DetectorImage'][1].add_patch(frame_overlays['EDC'])

	frame_overlays['IntensityROI']=matplotlib.patches.Rectangle(
		(spectrum['Axis'][1][0], spectrum['Axis'][0][0]), 
		width=abs(spectrum['Axis'][1][0]-spectrum['Axis'][1][1]), 
		height=abs(spectrum['Axis'][0][0]-spectrum['Axis'][0][-1]), 
		color='tab:red',fill=False,lw=1)
	figure['DetectorImage'][1].add_patch(frame_overlays['IntensityROI'])

	frame_overlays['IntensityRelative_SignalROI']=matplotlib.patches.Rectangle(
		(spectrum['Axis'][1][0], spectrum['Axis'][0][0]), 
		width=abs(spectrum['Axis'][1][0]-spectrum['Axis'][1][1]), 
		height=abs(spectrum['Axis'][0][0]-spectrum['Axis'][0][-1]), 
		color='tab:red',fill=False,lw=3)
	figure['DetectorImage'][1].add_patch(frame_overlays['IntensityRelative_SignalROI'])

	frame_overlays['IntensityRelative_BackgroundROI']=matplotlib.patches.Rectangle(
		(spectrum['Axis'][1][0], spectrum['Axis'][0][0]), 
		width=abs(spectrum['Axis'][1][0]-spectrum['Axis'][1][1]), 
		height=abs(spectrum['Axis'][0][0]-spectrum['Axis'][0][-1]), 
		color='black',fill=False,lw=1)
	figure['DetectorImage'][1].add_patch(frame_overlays['IntensityRelative_BackgroundROI'])

	frame_overlays['IntensityRelativeXPS_signalROI']=matplotlib.patches.Rectangle(
		(spectrum['Axis'][0][0], 0), 
		width=0.1, 
		height=999, 
		color='red',fill=True,lw=1,alpha=0.2)
	figure['DetectorImageCollapsed'][1].add_patch(frame_overlays['IntensityRelativeXPS_signalROI'])
	frame_overlays['IntensityRelativeXPS_BackgroundROI']=matplotlib.patches.Rectangle(
		(spectrum['Axis'][0][0], 0), 
		width=0.1, 
		height=999, 
		color='black',fill=True,lw=1,alpha=0.2)
	figure['DetectorImageCollapsed'][1].add_patch(frame_overlays['IntensityRelativeXPS_BackgroundROI'])


	maxVal = np.max(spectrum['data'])
	mapcolorSlider=ipywidgets.widgets.FloatRangeSlider(value=[0,1],max=10,step=0.01,description='Map colorscale',continuous_update=True,layout=ipywidgets.Layout(width='600px'),readout_format='.1f',style=style)
	colorMapSelector = ipywidgets.widgets.Dropdown(options=['bone_r', 'inferno', 'viridis','plasma', 'cividis','gray','OrRd','PuBuGn','coolwarm','bwr'],value='cividis',description='Colormap:',)

	cmap_update = ipywidgets.widgets.interactive_output(spatialMapExplorer__updateMap_cmap,{
		'figures':		ipywidgets.fixed(figure),
		'mapcrange':		mapcolorSlider,
		'cmap':	colorMapSelector,
		})	

	framecolorSlider=ipywidgets.widgets.FloatRangeSlider(value=[0,maxVal/2],max=maxVal*1.3,step=maxVal*1.3/500,description='Frame colorscale',continuous_update=True,layout=ipywidgets.Layout(width='600px'),readout_format='.1f',style=style)
	framecolorMapSelector = ipywidgets.widgets.Dropdown(options=['bone_r', 'inferno', 'viridis','plasma', 'cividis','gray','OrRd','PuBuGn','coolwarm','bwr'],value='bone_r',description='Colormap:',)

	DetectorImage_cmap_update = ipywidgets.widgets.interactive_output(spatialMapExplorer__updateDetectorImage_cmap,{
		'figures':		ipywidgets.fixed(figure),
		'mapcrange':		framecolorSlider,
		'cmap':	framecolorMapSelector,
		})	



	#---------------------------------------------------------------------------------------------------------


	#---- Controls for selecting the (X,Y) coordinate to show a detector frame from, and the frame colorscale
	# (Can be updated without having to recompute the contrast map)


	if majorAxis[0]>majorAxis[1]: majorAxis=reversed(majorAxis)
	if minorAxis[0]>minorAxis[1]: minorAxis=reversed(minorAxis)
	
	try: majorAxisLabel,minorAxisLabel = spectrum['majorAxisLabel'],spectrum['minorAxisLabel']
	except: majorAxisLabel,minorAxisLabel = spectrum['AxisLabel'][3],spectrum['AxisLabel'][2]
	majorSlider=ipywidgets.widgets.SelectionSlider(options=[(i) for i in majorAxis],description=majorAxisLabel,continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)
	minorSlider=ipywidgets.widgets.SelectionSlider(options=[(i) for i in minorAxis],description=minorAxisLabel,continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)

	coordinate_update = ipywidgets.widgets.interactive_output(spatialMapExplorer__updateCoordinates,{
		'figures':		ipywidgets.fixed(figure),
		'map_overlays':		ipywidgets.fixed(map_overlays),
		'spectrum':		ipywidgets.fixed(spectrum),
		'majorVal':		majorSlider,
		'minorVal':		minorSlider,
		})		

	#---------------------------------------------------------------------------------------------------------

	box_layout = ipywidgets.widgets.Layout(
		border='dashed 1px gray',
		margin='0px 10px 10px 0px',
		padding='5px 5px 5px 5px',
		width='700px')

	#---------------------------------------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------
	# Specific to ROI intensity panels



	ax=list(spectrum['Axis'][1])
	ax_midpoint = ax[int(len(ax)/2)]
	Intensity_AngleSlider=ipywidgets.widgets.FloatSlider(
		value=ax[int(len(ax)*(1/2))],max=max(ax),min=min(ax),step=abs(ax[1]-ax[0]),
		description="Angle",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)
	ROI_AngleIntegrationSlider=ipywidgets.widgets.FloatSlider(
		value=(max(ax)-min(ax))*0.05,max=max(ax)-min(ax),min=0.0,step=abs(ax[1]-ax[0]),
		description="Angle integration",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	ax=list(spectrum['Axis'][0])

	Intensity_EnergySlider=ipywidgets.widgets.FloatSlider(
		value=ax[int(len(ax)*(1/2))],max=max(ax),min=min(ax),step=abs(ax[1]-ax[0]),
		description="Energy",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	ROI_EnergyIntegrationSlider=ipywidgets.widgets.FloatSlider(
		value=(max(ax)-min(ax))*0.05,max=max(ax)-min(ax),min=0.0,step=abs(ax[1]-ax[0]),
		description="Energy integration",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)
	


	ROI_intensity = ipywidgets.widgets.interactive_output(spatialMapExplorer__updateIntensityOutput,{
		'figures':				ipywidgets.fixed(figure),
		'frame_overlays':		ipywidgets.fixed(frame_overlays),
		'spectrum':				ipywidgets.fixed(spectrum),
		'ROI_Angle':			Intensity_AngleSlider,
		'ROI_AngleIntegration':	ROI_AngleIntegrationSlider,
		'ROI_Energy':			Intensity_EnergySlider,
		'ROI_EnergyIntegration':ROI_EnergyIntegrationSlider,
	})
	ROI_intensity_control_panel=ipywidgets.widgets.VBox([
		ROI_AngleIntegrationSlider,ROI_EnergyIntegrationSlider],
		layout=box_layout)

	#---------------------------------------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------

	ax=list(spectrum['Axis'][1])
	ax_midpoint = ax[int(len(ax)/2)]
	IntensityRelative_Signal_AngleSlider=ipywidgets.widgets.FloatSlider(
		value=ax[int(len(ax)*(1/2))],max=max(ax),min=min(ax),step=ax[1]-ax[0],
		description="Signal angle",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)
	IntensityRelative_Signal_AngleIntegrationSlider=ipywidgets.widgets.FloatSlider(
		value=(max(ax)-min(ax))*0.05,max=max(ax)-min(ax),min=0.0,step=ax[1]-ax[0],
		description="Signal angle integration",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)
	
	IntensityRelative_BG_AngleSlider=ipywidgets.widgets.FloatSlider(
		value=ax[int(len(ax)*(1/2))],max=max(ax),min=min(ax),step=ax[1]-ax[0],
		description="Background angle",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)	
	IntensityRelative_BG_AngleIntegrationSlider=ipywidgets.widgets.FloatSlider(
		value=(max(ax)-min(ax))*0.05,max=max(ax)-min(ax),min=0.0,step=ax[1]-ax[0],
		description="Background angle integration",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	ax=list(spectrum['Axis'][0])

	IntensityRelative_Signal_EnergySlider=ipywidgets.widgets.FloatSlider(
		value=ax[int(len(ax)*(4/7))],max=max(ax),min=min(ax),step=ax[1]-ax[0],
		description="Signal energy",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)
	IntensityRelative_Signal_EnergyIntegrationSlider=ipywidgets.widgets.FloatSlider(
		value=(max(ax)-min(ax))*0.05,max=max(ax)-min(ax),min=0.0,step=ax[1]-ax[0],
		description="Signal energy integration",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)
	IntensityRelative_BG_EnergySlider=ipywidgets.widgets.FloatSlider(
		value=ax[int(len(ax)*(3/7))],max=max(ax),min=min(ax),step=ax[1]-ax[0],
		description="Background energy",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)
	IntensityRelative_BG_EnergyIntegrationSlider=ipywidgets.widgets.FloatSlider(
		value=(max(ax)-min(ax))*0.05,max=max(ax)-min(ax),min=0.0,step=ax[1]-ax[0],
		description="Background energy integration",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	ROI_intensity_relative = ipywidgets.widgets.interactive_output(spatialMapExplorer__updateRelativeIntensityOutput,{
		'figures':				ipywidgets.fixed(figure),
		'frame_overlays':		ipywidgets.fixed(frame_overlays),
		'spectrum':				ipywidgets.fixed(spectrum),
		'ROI_Angle':			IntensityRelative_Signal_AngleSlider,
		'ROI_AngleIntegration':	IntensityRelative_Signal_AngleIntegrationSlider,
		'ROI_Energy':			IntensityRelative_Signal_EnergySlider,
		'ROI_EnergyIntegration':IntensityRelative_Signal_EnergyIntegrationSlider,
		'ROI2_Angle':			IntensityRelative_BG_AngleSlider,
		'ROI2_AngleIntegration':	IntensityRelative_BG_AngleIntegrationSlider,
		'ROI2_Energy':			IntensityRelative_BG_EnergySlider,
		'ROI2_EnergyIntegration':IntensityRelative_BG_EnergyIntegrationSlider,

	})

	ROI_intensity_relative_control_panel=ipywidgets.widgets.VBox([
		IntensityRelative_Signal_AngleIntegrationSlider,
		IntensityRelative_Signal_EnergyIntegrationSlider,
		IntensityRelative_BG_AngleIntegrationSlider,
		IntensityRelative_BG_EnergyIntegrationSlider],
		layout=box_layout)





	ax=list(spectrum['Axis'][0])

	IntensityRelative_XPS_Signal_EnergySlider=ipywidgets.widgets.FloatSlider(
		value=ax[int(len(ax)*(4/7))],max=max(ax),min=min(ax),step=abs(ax[1]-ax[0]),
		description="Signal energy",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)
	IntensityRelative_XPS_Signal_EnergyIntegrationSlider=ipywidgets.widgets.FloatSlider(
		value=(max(ax)-min(ax))*0.05,max=max(ax)-min(ax),min=0.0,step=abs(ax[1]-ax[0]),
		description="Signal energy integration",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)
	IntensityRelative_XPS_BG_EnergySlider=ipywidgets.widgets.FloatSlider(
		value=ax[int(len(ax)*(3/7))],max=max(ax),min=min(ax),step=abs(ax[1]-ax[0]),
		description="Background energy",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)
	IntensityRelative_XPS_BG_EnergyIntegrationSlider=ipywidgets.widgets.FloatSlider(
		value=(max(ax)-min(ax))*0.05,max=max(ax)-min(ax),min=0.0,step=abs(ax[1]-ax[0]),
		description="Background energy integration",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	ROI_intensity_relative_XPS = ipywidgets.widgets.interactive_output(spatialMapExplorer__updateRelativeIntensityXPSOutput,{
		'figures':				ipywidgets.fixed(figure),
		'frame_overlays':		ipywidgets.fixed(frame_overlays),
		'spectrum':				ipywidgets.fixed(spectrum),
		'ROI_Energy':			IntensityRelative_XPS_Signal_EnergySlider,
		'ROI_EnergyIntegration':IntensityRelative_XPS_Signal_EnergyIntegrationSlider,
		'ROI2_Energy':			IntensityRelative_XPS_BG_EnergySlider,
		'ROI2_EnergyIntegration':IntensityRelative_XPS_BG_EnergyIntegrationSlider,

	})

	ROI_intensity_relative_XPS_control_panel=ipywidgets.widgets.VBox([
		IntensityRelative_XPS_Signal_EnergyIntegrationSlider,
		IntensityRelative_XPS_BG_EnergyIntegrationSlider],
		layout=box_layout)

	#---------------------------------------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------

	ax=list(spectrum['Axis'][1])
	MDC_profileAngleSlider=ipywidgets.widgets.FloatSlider(value=0,max=max(ax),min=min(ax),step=ax[1]-ax[0],description="Angle",continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)
	MDC_profileAngleIntegrationSlider=ipywidgets.widgets.FloatSlider(value=(max(ax)-min(ax))*4/5,max=max(ax)-min(ax),min=0.0,step=ax[1]-ax[0],description="Angle range",continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)
	ax=list(spectrum['Axis'][0])
	MDC_profileEnergySlider=ipywidgets.widgets.FloatSlider(value=ax[int(len(ax)*(5/7))],max=max(ax),min=min(ax),step=ax[1]-ax[0],description="Energy",continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)
	MDC_profileEnergyIntegrationSlider=ipywidgets.widgets.FloatSlider(value=0.1,max=max(ax)-min(ax),min=0.0,step=ax[1]-ax[0],description="Energy range",continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)

	MDC_smoothingSlider=ipywidgets.widgets.IntSlider(value=10,max=50,min=0,step=1,description="Smoothing",continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)

	MDC_sharpness = ipywidgets.widgets.interactive_output(spatialMapExplorer__updateMDCSharpnessOutput,{
		'figures':		ipywidgets.fixed(figure),
		'frame_overlays':		ipywidgets.fixed(frame_overlays),
		'spectrum':		ipywidgets.fixed(spectrum),
		'profileAngle':	MDC_profileAngleSlider,
		'profileAngleIntegration':	MDC_profileAngleIntegrationSlider,
		'profileEnergy':	MDC_profileEnergySlider,
		'profileEnergyIntegration':	MDC_profileEnergyIntegrationSlider,
		'smoothing':	MDC_smoothingSlider,
	})

	MDC_sharpness_control_panel=ipywidgets.widgets.VBox([
		MDC_profileAngleIntegrationSlider,
		MDC_profileEnergyIntegrationSlider,
		MDC_smoothingSlider],
		layout=box_layout)
	#---------------------------------------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------

	ax=list(spectrum['Axis'][1])
	EDC_profileAngleSlider=ipywidgets.widgets.FloatSlider(value=ax[int(len(ax)*(1/2))],max=max(ax),min=min(ax),step=abs(ax[1]-ax[0]),description="Angle",continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)
	EDC_profileAngleIntegrationSlider=ipywidgets.widgets.FloatSlider(value=0.5,max=max(ax)-min(ax),min=0.0,step=abs(ax[1]-ax[0]),description="Angle range",continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)		   
	ax=list(spectrum['Axis'][0])
	EDC_profileEnergySlider=ipywidgets.widgets.FloatSlider(value=ax[int(len(ax)*(1/2))],max=max(ax),min=min(ax),step=abs(ax[1]-ax[0]),description="Energy",continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)
	EDC_profileEnergyIntegrationSlider=ipywidgets.widgets.FloatSlider(value=(max(ax)-min(ax))*3/5,max=max(ax)-min(ax),min=0.0,step=abs(ax[1]-ax[0]),description="Energy range",continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)

	EDC_smoothingSlider=ipywidgets.widgets.IntSlider(value=10,max=50,min=0,step=1,description="Smoothing",continuous_update=True,layout=ipywidgets.Layout(width='600px'),style=style)
	
	EDC_sharpness = ipywidgets.widgets.interactive_output(spatialMapExplorer__updateEDCSharpnessOutput,{
		'figures':		ipywidgets.fixed(figure),
		'frame_overlays':		ipywidgets.fixed(frame_overlays),
		'spectrum':		ipywidgets.fixed(spectrum),
		'profileAngle':	EDC_profileAngleSlider,
		'profileAngleIntegration':	EDC_profileAngleIntegrationSlider,
		'profileEnergy':	EDC_profileEnergySlider,
		'profileEnergyIntegration':	EDC_profileEnergyIntegrationSlider,
		'smoothing':	EDC_smoothingSlider,
	})
	EDC_sharpness_control_panel=ipywidgets.widgets.VBox([
		EDC_profileAngleIntegrationSlider,
		EDC_profileEnergyIntegrationSlider,
		EDC_smoothingSlider],
		layout=box_layout)
	#---------------------------------------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------


	def spatialMapExplorer__pasteCodeCell(self):

		templateCode=""
		templateCode+="from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar\n"
		templateCode+="\nspectrum=[FILL THIS IN]\n"
		templateCode+="scaleBarLength_um=30\n"
		templateCode+="point = [{},{}]\n".format(minorSlider.value,majorSlider.value)

		templateCode+="fig,axes=matplotlib.pyplot.subplots(figsize=(9,4),ncols=2)\n"
		templateCode+="ax=axes[1]\n"

		if tab.selected_index==0: #Intensity
			templateCode+="ROI_Angle,ROI_AngleIntegration = {:.3f},{:.2f}\n".format(Intensity_AngleSlider.value,ROI_AngleIntegrationSlider.value)
			templateCode+="ROI_Energy,ROI_EnergyIntegration = {:.3f},{:.2f}\n".format(Intensity_EnergySlider.value,ROI_EnergyIntegrationSlider.value)
			templateCode+="ROI_AngleStart,ROI_AngleStop=ROI_Angle-ROI_AngleIntegration/2,ROI_Angle+ROI_AngleIntegration/2\n"
			templateCode+="ROI_EnergyStart,ROI_EnergyStop=ROI_Energy-ROI_EnergyIntegration/2,ROI_Energy+ROI_EnergyIntegration/2\n"
			templateCode+="image = pesto.getFrameFrom4DScan(spectrum=spectrum,axes=['X','Y'],axisValues=point)\n"
			templateCode+="pesto.quickPlot(image,axis=ax,cmin={:.3f},cmax={:.3f},cmap='{}')\n".format(framecolorSlider.value[0],framecolorSlider.value[1],framecolorMapSelector.value)
			templateCode+="ROI=matplotlib.patches.Rectangle((ROI_AngleStart,ROI_EnergyStart), height=ROI_EnergyIntegration, width=ROI_AngleIntegration,linestyle='-',color='tab:red',fill=False)\n"
			templateCode+="ax.add_patch(ROI) \n"
			templateCode+="axes[0].set_title('Intensity in ROI')\n"
			templateCode+="map = pesto.spatialMap__IntensityContrastImage(spectrum,ROI_Angle,ROI_AngleIntegration,ROI_Energy,ROI_EnergyIntegration)\n"

		if tab.selected_index==1: #Relative intensity
			templateCode+="ROI_Angle,ROI_AngleIntegration = {:.3f},{:.2f}\n".format(IntensityRelative_Signal_AngleSlider.value,IntensityRelative_Signal_AngleIntegrationSlider.value)
			templateCode+="ROI_Energy,ROI_EnergyIntegration = {:.3f},{:.2f}\n".format(IntensityRelative_Signal_EnergySlider.value,IntensityRelative_Signal_EnergyIntegrationSlider.value)
			templateCode+="ROI_AngleStart,ROI_AngleStop=ROI_Angle-ROI_AngleIntegration/2,ROI_Angle+ROI_AngleIntegration/2\n"
			templateCode+="ROI_EnergyStart,ROI_EnergyStop=ROI_Energy-ROI_EnergyIntegration/2,ROI_Energy+ROI_EnergyIntegration/2\n"
			templateCode+="ROI2_Angle,ROI2_AngleIntegration = {:.3f},{:.2f}\n".format(IntensityRelative_BG_AngleSlider.value,IntensityRelative_BG_AngleIntegrationSlider.value)
			templateCode+="ROI2_Energy,ROI2_EnergyIntegration = {:.3f},{:.2f}\n".format(IntensityRelative_BG_EnergySlider.value,IntensityRelative_BG_EnergyIntegrationSlider.value)
			templateCode+="ROI2_AngleStart,ROI2_AngleStop=ROI2_Angle-ROI2_AngleIntegration/2,ROI2_Angle+ROI2_AngleIntegration/2\n"
			templateCode+="ROI2_EnergyStart,ROI2_EnergyStop=ROI2_Energy-ROI2_EnergyIntegration/2,ROI2_Energy+ROI2_EnergyIntegration/2\n"
			templateCode+="image = pesto.getFrameFrom4DScan(spectrum=spectrum,axes=['X','Y'],axisValues=point)\n"
			templateCode+="pesto.quickPlot(image,axis=ax,cmin={:.3f},cmax={:.3f},cmap='{}')\n".format(framecolorSlider.value[0],framecolorSlider.value[1],framecolorMapSelector.value)
			templateCode+="ROI=matplotlib.patches.Rectangle((ROI_AngleStart,ROI_EnergyStart), height=ROI_EnergyIntegration, width=ROI_AngleIntegration,linestyle='-',color='tab:red',fill=False)\n"
			templateCode+="ax.add_patch(ROI) \n"
			templateCode+="ROI2=matplotlib.patches.Rectangle((ROI2_AngleStart,ROI2_EnergyStart), height=ROI2_EnergyIntegration, width=ROI2_AngleIntegration,linestyle='-',color='black',fill=False)\n"
			templateCode+="ax.add_patch(ROI2) \n"
			templateCode+="axes[0].set_title('Relative intensity (red/black ROI)')\n"
			templateCode+="map = pesto.spatialMap__RelativeIntensityContrastImage(spectrum,ROI_Angle,ROI_AngleIntegration,ROI_Energy,ROI_EnergyIntegration,ROI2_Angle,ROI2_AngleIntegration,ROI2_Energy,ROI2_EnergyIntegration)\n"

		if tab.selected_index==2: #MDC sharpness
			templateCode+="profileAngle,profileAngleIntegration = {:.3f},{:.2f}\n".format(MDC_profileAngleSlider.value,MDC_profileAngleIntegrationSlider.value)
			templateCode+="profileEnergy,profileEnergyIntegration = {:.3f},{:.2f}\n".format(MDC_profileEnergySlider.value,MDC_profileEnergyIntegrationSlider.value)
			templateCode+="profileAngleStart,profileAngleStop=profileAngle-profileAngleIntegration/2,profileAngle+profileAngleIntegration/2\n"
			templateCode+="profileEnergyStart,profileEnergyStop=profileEnergy-profileEnergyIntegration/2,profileEnergy+profileEnergyIntegration/2\n"
			templateCode+="smoothing = {}\n".format(MDC_smoothingSlider.value)
			templateCode+="image = pesto.getFrameFrom4DScan(spectrum=spectrum,axes=['X','Y'],axisValues=point)\n"
			templateCode+="pesto.quickPlot(image,axis=ax,cmin={:.3f},cmax={:.3f},cmap='{}')\n".format(framecolorSlider.value[0],framecolorSlider.value[1],framecolorMapSelector.value)
			templateCode+="ROI=matplotlib.patches.Rectangle((profileAngleStart,profileEnergyStart), height=abs(profileEnergyStart-profileEnergyStop), width=abs(profileAngleStart-profileAngleStop),linestyle='-',color='tab:red',fill=False)\n"
			templateCode+="ax.add_patch(ROI) \n"
			templateCode+="axes[0].set_title('MDC sharpness')\n"
			templateCode+="map = pesto.spatialMap__SharpnessContrastImage(spectrum,'MDC',profileAngle,profileAngleIntegration,profileEnergy,profileEnergyIntegration,smoothing)\n"

		if tab.selected_index==3: #EDC sharpness
			templateCode+="profileAngle,profileAngleIntegration = {:.3f},{:.2f}\n".format(EDC_profileAngleSlider.value,EDC_profileAngleIntegrationSlider.value)
			templateCode+="profileEnergy,profileEnergyIntegration = {:.3f},{:.2f}\n".format(EDC_profileEnergySlider.value,EDC_profileEnergyIntegrationSlider.value)
			templateCode+="profileAngleStart,profileAngleStop=profileAngle-profileAngleIntegration/2,profileAngle+profileAngleIntegration/2\n"
			templateCode+="profileEnergyStart,profileEnergyStop=profileEnergy-profileEnergyIntegration/2,profileEnergy+profileEnergyIntegration/2\n"
			templateCode+="smoothing = {}\n".format(EDC_smoothingSlider.value)
			templateCode+="image = pesto.getFrameFrom4DScan(spectrum=spectrum,axes=['X','Y'],axisValues=point)\n"
			templateCode+="pesto.quickPlot(image,axis=ax,cmin={:.3f},cmax={:.3f},cmap='{}')\n".format(framecolorSlider.value[0],framecolorSlider.value[1],framecolorMapSelector.value)
			templateCode+="ROI=matplotlib.patches.Rectangle((profileAngleStart,profileEnergyStart), height=abs(profileEnergyStart-profileEnergyStop), width=abs(profileAngleStart-profileAngleStop),linestyle='-',color='tab:red',fill=False)\n"
			templateCode+="ax.add_patch(ROI) \n"
			templateCode+="axes[0].set_title('EDC sharpness')\n"
			templateCode+="map = pesto.spatialMap__SharpnessContrastImage(spectrum,'EDC',profileAngle,profileAngleIntegration,profileEnergy,profileEnergyIntegration,smoothing)\n"
	
		if tab.selected_index==4: #XPS relative
			templateCode+="signalEnergy,signalIntegration = {:.3f},{:.2f}\n".format(IntensityRelative_XPS_Signal_EnergySlider.value,IntensityRelative_XPS_Signal_EnergyIntegrationSlider.value)
			templateCode+="backgroundEnergy,backgroundIntegration = {:.3f},{:.2f}\n".format(IntensityRelative_XPS_BG_EnergySlider.value,IntensityRelative_XPS_BG_EnergyIntegrationSlider.value)
			templateCode+="image = pesto.getFrameFrom4DScan(spectrum=spectrum,axes=['X','Y'],axisValues=point)\n"
			templateCode+="pesto.quickPlot(image,axis=ax,color='black',XPS=True)\n"
			templateCode+="ax.axvline(x=signalEnergy-(signalIntegration/2),color='tab:red',ls='--')\n"
			templateCode+="ax.axvline(x=signalEnergy+(signalIntegration/2),color='tab:red',ls='--')\n"
			templateCode+="ax.axvline(x=backgroundEnergy-(backgroundIntegration/2),color='black',ls='--')\n"
			templateCode+="ax.axvline(x=backgroundEnergy+(backgroundIntegration/2),color='black',ls='--')\n"
			templateCode+="axes[0].set_title('Relative intensity')\n"
			templateCode+="map = pesto.spatialMap__XPSContrastImage(spectrum,signalEnergy,signalIntegration,backgroundEnergy,backgroundIntegration)\n"
		
		templateCode+="ax=axes[0]\n"
		templateCode+="image=pesto.quickPlot(map,axis=ax,returnIm=True,cmin={:.3f},cmax={:.3f},cmap='{}')\n".format(mapcolorSlider.value[0],mapcolorSlider.value[1],colorMapSelector.value)

		templateCode+="fig.colorbar(image,ax=ax)\n"
		templateCode+="x,y=point[0],point[1]\n"
		templateCode+="dx=abs(spectrum['Axis'][2][1]-spectrum['Axis'][2][0])\n"
		templateCode+="dy=abs(spectrum['Axis'][3][1]-spectrum['Axis'][3][0])\n"
		templateCode+="ax.axvline(x=x,ls='--')\n"
		templateCode+="ax.axhline(y=y,ls='--')\n"
		templateCode+="ROI=matplotlib.patches.Rectangle((x-(dx/2),y-(dy/2)), height=dy, width=dx,linestyle='-',color='tab:red',fill=False,lw=2)\n"
		templateCode+="ax.add_patch(ROI)\n"
		templateCode+="\n"
		templateCode+="scalebar = AnchoredSizeBar(ax.transData,scaleBarLength_um/1000, '{}um'.format(scaleBarLength_um), 'lower right',pad=0.3,color='white',frameon=False,size_vertical=0.005)\n"
		templateCode+="ax.add_artist(scalebar)\n"

		templateCode+="plt.tight_layout()\n"
		templateCode+="plt.show()\n"

		pyperclip.copy(templateCode)



	map_cmap_control_panel=ipywidgets.widgets.VBox([mapcolorSlider,colorMapSelector],layout=box_layout,width='auto')
	frame_cmap_control_panel=ipywidgets.widgets.VBox([framecolorSlider,framecolorMapSelector],layout=box_layout,width='auto')

	frame_vbox=ipywidgets.widgets.VBox([figure['DetectorImage'][0].canvas,frame_cmap_control_panel],width='auto')
	map_vbox=ipywidgets.widgets.VBox([figure['XY_map'][0].canvas,map_cmap_control_panel],width='auto')

	hbox=ipywidgets.widgets.HBox([map_vbox,frame_vbox],width='auto')
	panels={}

	panels['Intensity']  = 	ipywidgets.widgets.VBox([ROI_intensity_control_panel,hbox],width='auto')
	panels['Intensity relative']= 	ipywidgets.widgets.VBox([ROI_intensity_relative_control_panel,hbox],width='auto')
	panels['MDC sharpness'] =	ipywidgets.widgets.VBox([MDC_sharpness_control_panel,hbox],width='auto')
	panels['EDC sharpness'] =	ipywidgets.widgets.VBox([EDC_sharpness_control_panel,hbox],width='auto')

	frame_vbox=ipywidgets.widgets.VBox([figure['DetectorImageCollapsed'][0].canvas,frame_cmap_control_panel],width='auto')
	hbox=ipywidgets.widgets.HBox([map_vbox,frame_vbox],width='auto')
	panels['Intensity relative XPS']= 	ipywidgets.widgets.VBox([ROI_intensity_relative_XPS_control_panel,hbox],width='auto')


		
	tab.children = [panels[key] for key in panels]
	[tab.set_title(ii, key) for ii, key in enumerate(panels)]

	global tab_selected
	tab_selected=0
	spatialMapExplorer__updateIntensityOutput(
		spectrum=spectrum,
		figures=figure,
		frame_overlays=frame_overlays,
		ROI_Angle=Intensity_AngleSlider.value,
		ROI_AngleIntegration=ROI_AngleIntegrationSlider.value,
		ROI_Energy=Intensity_EnergySlider.value,
		ROI_EnergyIntegration=ROI_EnergyIntegrationSlider.value)


	copyToClipBoardButton = ipywidgets.Button(description='Copy template code to clipboard',layout=ipywidgets.Layout(width='auto') )	
	copyToClipBoardButton.on_click(spatialMapExplorer__pasteCodeCell) 


	# ---- This exists solely so that everything is re-drawn immediately when you change tabs. Otherwise the display is incorrect until the controls are adjusted
	def spatialMapExplorer__tab_eventhandler():
		global tab_selected
		if tab.selected_index==0 and tab_selected!=tab.selected_index: #Coming to intensity from something else

			tab_selected=tab.selected_index
			spatialMapExplorer__updateIntensityOutput(
				spectrum=spectrum,
				figures=figure,
				frame_overlays=frame_overlays,
				ROI_Angle=Intensity_AngleSlider.value,
				ROI_AngleIntegration=ROI_AngleIntegrationSlider.value,
				ROI_Energy=Intensity_EnergySlider.value,
				ROI_EnergyIntegration=ROI_EnergyIntegrationSlider.value)

		if tab.selected_index==1 and tab_selected!=tab.selected_index: #Intensity relative
			tab_selected=tab.selected_index
			spatialMapExplorer__updateRelativeIntensityOutput(
				spectrum=spectrum,
				figures=figure,
				frame_overlays=frame_overlays,
				ROI_Angle=IntensityRelative_Signal_AngleSlider.value,
				ROI_AngleIntegration=IntensityRelative_Signal_AngleIntegrationSlider.value,
				ROI_Energy=IntensityRelative_Signal_EnergySlider.value,
				ROI_EnergyIntegration=IntensityRelative_Signal_EnergyIntegrationSlider.value,
				ROI2_Angle=IntensityRelative_BG_AngleSlider.value,
				ROI2_AngleIntegration=IntensityRelative_BG_AngleIntegrationSlider.value,
				ROI2_Energy=IntensityRelative_BG_EnergySlider.value,
				ROI2_EnergyIntegration=IntensityRelative_BG_EnergyIntegrationSlider.value)

		if tab.selected_index==2 and tab_selected!=tab.selected_index: #MDC sharpness	
			tab_selected=tab.selected_index
			spatialMapExplorer__updateMDCSharpnessOutput(
				spectrum=spectrum,
				figures=figure,
				frame_overlays=frame_overlays,
				profileAngle=MDC_profileAngleSlider.value,
				profileAngleIntegration=MDC_profileAngleIntegrationSlider.value,
				profileEnergy=MDC_profileEnergySlider.value,
				profileEnergyIntegration=MDC_profileEnergyIntegrationSlider.value,
				smoothing=MDC_smoothingSlider.value)

		if tab.selected_index==3 and tab_selected!=tab.selected_index: #EDC sharpness	
			tab_selected=tab.selected_index
			spatialMapExplorer__updateEDCSharpnessOutput(
				spectrum=spectrum,
				figures=figure,
				frame_overlays=frame_overlays,
				profileAngle=EDC_profileAngleSlider.value,
				profileAngleIntegration=EDC_profileAngleIntegrationSlider.value,
				profileEnergy=EDC_profileEnergySlider.value,
				profileEnergyIntegration=EDC_profileEnergyIntegrationSlider.value,
				smoothing=EDC_smoothingSlider.value)

		if tab.selected_index==4 and tab_selected!=tab.selected_index: #XPS relative

			tab_selected=tab.selected_index
			spatialMapExplorer__updateRelativeIntensityXPSOutput(
				spectrum=spectrum,
				figures=figure,
				frame_overlays=frame_overlays,
				ROI_Energy=IntensityRelative_XPS_Signal_EnergySlider.value,
				ROI_EnergyIntegration=IntensityRelative_XPS_Signal_EnergyIntegrationSlider.value,
				ROI2_Energy=IntensityRelative_XPS_BG_EnergySlider.value,
				ROI2_EnergyIntegration=IntensityRelative_XPS_BG_EnergyIntegrationSlider.value)

	
	tab.on_trait_change(spatialMapExplorer__tab_eventhandler)

	global mouseState
	global ROI_selected


	ROI_selected='signal'
	mouseState=0

	def spatialMapExplorer__map_onClick(event,canvas):
		state = canvas.toolbar.mode
		if state=="":
			global mouseState
			if mouseState==0: 
				mouseState=1

				try: majorAxis,minorAxis = spectrum['majorAxis'],spectrum['minorAxis']
				except: majorAxis,minorAxis = spectrum['Axis'][3],spectrum['Axis'][2]


				majorValue = min(list(majorAxis), key=lambda x:abs(x-event.ydata))
				minorValue = min(list(minorAxis), key=lambda x:abs(x-event.xdata))

				minorSlider.value, majorSlider.value = minorValue, majorValue

	def spatialMapExplorer__map_onRelease(event):
		global mouseState
		if mouseState==1: mouseState=0

	def spatialMapExplorer__map_clickDrag(event):
		global mouseState
		if mouseState==1: 
			try:
				try: majorAxis,minorAxis = spectrum['majorAxis'],spectrum['minorAxis']
				except: majorAxis,minorAxis = spectrum['Axis'][3],spectrum['Axis'][2]
				majorValue = min(list(majorAxis), key=lambda x:abs(x-event.ydata))
				minorValue = min(list(minorAxis), key=lambda x:abs(x-event.xdata))
				majorSlider.value=majorValue
				minorSlider.value=minorValue
			except:
				pass

	def spatialMapExplorer__point_is_in_ROI(whichROI,coordinates):
		if tab.selected_index==1:
			if whichROI == 'signal':
				ROI_Angle=IntensityRelative_Signal_AngleSlider.value
				ROI_Energy=IntensityRelative_Signal_EnergySlider.value
				ROI_AngleIntegration=IntensityRelative_Signal_AngleIntegrationSlider.value
				ROI_EnergyIntegration=IntensityRelative_Signal_EnergyIntegrationSlider.value
			else:
				ROI_Angle=IntensityRelative_BG_AngleSlider.value
				ROI_Energy=IntensityRelative_BG_EnergySlider.value
				ROI_AngleIntegration=IntensityRelative_BG_AngleIntegrationSlider.value
				ROI_EnergyIntegration=IntensityRelative_BG_EnergyIntegrationSlider.value

			ROI_AngleStart,ROI_AngleStop=ROI_Angle-ROI_AngleIntegration/2,ROI_Angle+ROI_AngleIntegration/2
			ROI_EnergyStart,ROI_EnergyStop=ROI_Energy-ROI_EnergyIntegration/2,ROI_Energy+ROI_EnergyIntegration/2		

			x=coordinates[0]
			y=coordinates[1]

			if x>=ROI_AngleStart and x<=ROI_AngleStop and y>=ROI_EnergyStart and y<=ROI_EnergyStop: return True
			else: return False

		if tab.selected_index==4:
			if whichROI == 'signal':
				ROI_Energy=IntensityRelative_XPS_Signal_EnergySlider.value
				ROI_EnergyIntegration=IntensityRelative_XPS_Signal_EnergyIntegrationSlider.value
			else:
				ROI_Energy=IntensityRelative_XPS_BG_EnergySlider.value
				ROI_EnergyIntegration=IntensityRelative_XPS_BG_EnergyIntegrationSlider.value

			ROI_EnergyStart,ROI_EnergyStop=ROI_Energy-ROI_EnergyIntegration/2,ROI_Energy+ROI_EnergyIntegration/2		
			x=coordinates[0]


			if x>=ROI_EnergyStart and x<=ROI_EnergyStop: return True
			else: return False
				
	def spatialMapExplorer__frame_onClick(event,canvas):
		global mouseState
		global ROI_selected
		state = canvas.toolbar.mode
		if state=="":
			if mouseState==0: mouseState=1
			try:
				if tab.selected_index==0: #Intensity
					Intensity_EnergySlider.value=event.ydata
					Intensity_AngleSlider.value=event.xdata

				if tab.selected_index==1: #Intensity relative
					if ROI_selected=='signal' and spatialMapExplorer__point_is_in_ROI('background',[event.xdata,event.ydata]):
						ROI_selected='background'
						frame_overlays['IntensityRelative_BackgroundROI'].set(linewidth=3)
						frame_overlays['IntensityRelative_SignalROI'].set(linewidth=1)
					elif ROI_selected=='background' and spatialMapExplorer__point_is_in_ROI('signal',[event.xdata,event.ydata]):
						ROI_selected='signal'
						frame_overlays['IntensityRelative_BackgroundROI'].set(linewidth=1)
						frame_overlays['IntensityRelative_SignalROI'].set(linewidth=3)
					elif ROI_selected=='signal':			
						IntensityRelative_Signal_EnergySlider.value=event.ydata
						IntensityRelative_Signal_AngleSlider.value=event.xdata
					elif ROI_selected=='background':			
						IntensityRelative_BG_EnergySlider.value=event.ydata
						IntensityRelative_BG_AngleSlider.value=event.xdata

				if tab.selected_index==2: # MDC sharpness
					MDC_profileEnergySlider.value=event.ydata
					MDC_profileAngleSlider.value=event.xdata

				if tab.selected_index==3: # EDC sharpness
					EDC_profileEnergySlider.value=event.ydata
					EDC_profileAngleSlider.value=event.xdata


				if tab.selected_index==4: #XPS relative
					if ROI_selected=='signal' and spatialMapExplorer__point_is_in_ROI('background',[event.xdata,event.ydata]):
						ROI_selected='background'
						frame_overlays['IntensityRelativeXPS_BackgroundROI'].set(lw=3)
						frame_overlays['IntensityRelativeXPS_signalROI'].set(lw=1)
					elif ROI_selected=='background' and spatialMapExplorer__point_is_in_ROI('signal',[event.xdata,event.ydata]):
						ROI_selected='signal'
						frame_overlays['IntensityRelativeXPS_BackgroundROI'].set(lw=1)
						frame_overlays['IntensityRelativeXPS_signalROI'].set(lw=3)
					elif ROI_selected=='signal':			
						IntensityRelative_XPS_Signal_EnergySlider.value=event.xdata
					elif ROI_selected=='background':			
						IntensityRelative_XPS_BG_EnergySlider.value=event.xdata

			except:
				pass

	def spatialMapExplorer__frame_onRelease(event):
		global mouseState
		if mouseState==1: mouseState=0

	def spatialMapExplorer__frame_clickDrag(event):
		global mouseState
		global ROI_selected
		if mouseState==1: 
			try:
				if tab.selected_index==0: #Intensity
					Intensity_EnergySlider.value=event.ydata
					Intensity_AngleSlider.value=event.xdata
				if tab.selected_index==1: #Intensity relative
					if ROI_selected=='signal':			
						IntensityRelative_Signal_EnergySlider.value=event.ydata
						IntensityRelative_Signal_AngleSlider.value=event.xdata
					elif ROI_selected=='background':			
						IntensityRelative_BG_EnergySlider.value=event.ydata
						IntensityRelative_BG_AngleSlider.value=event.xdata
				if tab.selected_index==2: # MDC sharpness
					MDC_profileEnergySlider.value=event.ydata
					MDC_profileAngleSlider.value=event.xdata

				if tab.selected_index==3: # EDC sharpness
					EDC_profileEnergySlider.value=event.ydata
					EDC_profileAngleSlider.value=event.xdata

				if tab.selected_index==4: #Intensity XPS relative
					if ROI_selected=='signal':			
						IntensityRelative_XPS_Signal_EnergySlider.value=event.xdata
					elif ROI_selected=='background':			
						IntensityRelative_XPS_BG_EnergySlider.value=event.xdata
			except:
				pass

	figure['XY_map'][0].canvas.mpl_connect('button_press_event', lambda event: spatialMapExplorer__map_onClick(event,figure['XY_map'][0].canvas))
	figure['XY_map'][0].canvas.mpl_connect('button_release_event', spatialMapExplorer__map_onRelease)
	figure['XY_map'][0].canvas.mpl_connect('motion_notify_event', spatialMapExplorer__map_clickDrag)

	figure['DetectorImage'][0].canvas.mpl_connect('button_press_event', lambda event: spatialMapExplorer__frame_onClick(event,figure['DetectorImage'][0].canvas))
	figure['DetectorImage'][0].canvas.mpl_connect('button_release_event', spatialMapExplorer__frame_onRelease)
	figure['DetectorImage'][0].canvas.mpl_connect('motion_notify_event', spatialMapExplorer__frame_clickDrag)

	figure['DetectorImageCollapsed'][0].canvas.mpl_connect('button_press_event', lambda event: spatialMapExplorer__frame_onClick(event,figure['DetectorImageCollapsed'][0].canvas))
	figure['DetectorImageCollapsed'][0].canvas.mpl_connect('button_release_event', spatialMapExplorer__frame_onRelease)
	figure['DetectorImageCollapsed'][0].canvas.mpl_connect('motion_notify_event', spatialMapExplorer__frame_clickDrag)

	display(ipywidgets.widgets.VBox([tab,copyToClipBoardButton],width='auto'))



