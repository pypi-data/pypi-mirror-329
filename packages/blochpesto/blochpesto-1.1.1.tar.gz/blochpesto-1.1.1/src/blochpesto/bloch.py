import os,time,copy,math

import blochpesto as pesto

try:	import numpy as np
except ImportError: print("\t(ERROR): Couldn't import the numpy module. This is required for basic functionality. Install it with the command 'pip install numpy'")

try:	import matplotlib
except ImportError: print("\t(ERROR): Couldn't import the matplotlib module. This is required for basic functionality. Install it with the command 'pip install matplotlib'")

try:	import scipy
except ImportError: print("\t(Warning): Couldn't import the scipy module. This is required for basic functionality. Install it with the command 'pip install scipy'")

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

try:	import ipywidgets
except ImportError: print("\t(Warning): Couldn't import the ipywidgets module. You will not be able to use any interactive functions")


print("Taking A-branch analyzer workfunction = {}eV, calibrated 2023.08.28".format(pesto.getAnalyzerWorkFunction()))
print("Call pesto.setAnalyzerWorkFunction(value_in_eV) if you wish to change this")


def temperatureCalculator(startT,endT):

	def settlingTime(tau,deltaT,tolerance):
		return tau * math.log(deltaT/tolerance)

	def getTau(temperature): #Specific to the Carving on the Bloch A-station
		if temperature<20: 
			temperature=20
		if temperature>300:
			temperature=300
		c=[]
		c.append(0.36018952400947457)
		c.append(0.04165986305230357)
		c.append(-0.0065425111458743725)
		c.append(0.00025357122275147906)
		c.append(-3.448604172402499e-06)
		c.append(2.3601021440995724e-08)
		c.append(-8.801008328766784e-11)
		c.append(1.7099889968656564e-13)
		c.append(-1.3573855205337025e-16)
		order=len(c)
		tau=0
		for ii in range(order):
			tau+=c[ii]* temperature**ii

		return tau

	tau=getTau(endT)
	timeElapsed = np.linspace(-2,tau*5,num=100)
	predictedTemperature=[]
	for ii,time in enumerate(timeElapsed):
		if time<0: predictedTemperature.append(startT)
		else: predictedTemperature.append(startT + (endT-startT)*(1-math.exp(-(time)/tau)))

	fig,ax=matplotlib.pyplot.subplots(figsize=[10,6])
	ax.plot(timeElapsed,predictedTemperature,label="Predicted",lw=5)
	ax.axhline(y=endT,ls='--')
	tolerances=[1,2.5,5]
	for tolerance in tolerances:
		if endT-startT>tolerance:
			T=endT-tolerance
			timeTaken=settlingTime(tau,(endT-startT),tolerance)
			ax.plot([-3,timeTaken,timeTaken],[T,T,startT],ls='--',label='Within {}K in {:.1f} mins'.format(tolerance,timeTaken))
	
	matplotlib.pyplot.legend(loc='lower right')
	ax.set_xlim(-2,5*tau)
	ax.set_xlabel("Time elapsed (mins)")
	ax.set_ylabel("Sample temperature (K)")
	ax.set_title("Predicted sample temperature for a step change in setpoint\nTime constant at {}K = {:.1f} minutes".format(endT,tau))
	matplotlib.pyplot.show()   


def resolutionCalculator():

	tab = ipywidgets.Tab()

	dirname=os.path.dirname(__file__)
	coefficientsLoaded=False
	try:
		with open(os.path.join(dirname,"assets/gr800_2.25_resolution.txt")) as f: fileContents=f.readlines()
		fit_coefficients_800 = [float(line.split()[-1]) for line in fileContents]
		with open(os.path.join(dirname,"assets/gr2400_2.25_resolution.txt")) as f: fileContents=f.readlines()
		fit_coefficients_2400 = [float(line.split()[-1]) for line in fileContents]	
		with open(os.path.join(dirname,"assets/gr92_2.25_resolution.txt")) as f: fileContents=f.readlines()
		fit_coefficients_92 = [float(line.split()[-1]) for line in fileContents]
		coefficientsLoaded=True
	except:
		coefficientsLoaded=False
	
	assert(coefficientsLoaded==True), "[Pesto Error]\nUnable to load beamline resolution coefficient files (e.g. gr800_2.25_resolution.txt)"


	def resolutionCalculator__guessDeltaE(fit_coefficients,hv,hgap):
		ci=0
		enres=0
		for order in range(6+1):
			for ii in range(order+1):
				enres+=fit_coefficients[ci] * hgap**ii * hv **(order-ii)
				ci+=1 
		return enres

	def resolutionCalculator__B_update(grating,hv,hgap,Ep,anaSlit,noise,spinAperture):
		ana = analyzer_resolution(hemisphereRadius_mm=150,passEnergy_eV = Ep,slit_mm = anaSlit,beQuiet=True)
		
		if grating=='92': bl = resolutionCalculator__guessDeltaE(fit_coefficients_92,hv,hgap)
		if grating=='800': bl = resolutionCalculator__guessDeltaE(fit_coefficients_800,hv,hgap)
		if grating=='2400': bl = resolutionCalculator__guessDeltaE(fit_coefficients_2400,hv,hgap)

		spin = (Ep*1000*0.1*spinAperture)/35
		totalCCD = math.sqrt(ana**2 + bl**2 + noise**2)
		totalspin = math.sqrt(ana**2 + bl**2 + noise**2 + spin**2)
		print("Analyzer CCD resolution:\t{:.2f} meV".format(ana))
		print("Analyzer spin resolution:\t{:.2f} meV".format(spin))
		print("Beamline resolution:\t\t{:.2f} meV".format(bl))
		print("Noise floor:\t\t\t{:.2f} meV".format(noise))
		print("\nTotal resolution (CCD):\t\t{:.2f} meV".format(totalCCD))
		print("Total resolution (spin):\t{:.2f} meV".format(totalspin))


	def resolutionCalculator__A_update(grating,hv,hgap,Ep,anaSlit,noise):
		ana = analyzer_resolution(hemisphereRadius_mm=200,passEnergy_eV = Ep,slit_mm = anaSlit,beQuiet=True)
		if grating=='92': bl = resolutionCalculator__guessDeltaE(fit_coefficients_92,hv,hgap)
		if grating=='800': bl = resolutionCalculator__guessDeltaE(fit_coefficients_800,hv,hgap)
		if grating=='2400': bl = resolutionCalculator__guessDeltaE(fit_coefficients_2400,hv,hgap)
		total = math.sqrt(ana**2 + bl**2 + noise**2)
		
		print("Analyzer resolution:\t{:.2f} meV".format(ana))
		print("Beamline resolution:\t{:.2f} meV".format(bl))
		print("Noise floor:\t\t{:.2f} meV".format(noise))
		print("\nTotal resolution:\t{:.2f} meV".format(total))


	style = {'description_width': 'initial'}

	grating=ipywidgets.widgets.Dropdown(
		options=['92','800','2400'],value='800',description="Grating density (l/mm)",
		layout=ipywidgets.Layout(width='600px'),style=style)

	hv=ipywidgets.widgets.FloatSlider(
		value=80,min=10,max=1000,step=1,description='Photon energy (eV)',continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	hgap=ipywidgets.widgets.FloatSlider(
		value=100,min=10,max=200,step=1,description='Exitslit hgap (\u00b5m)',continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	noise=ipywidgets.widgets.FloatSlider(
		value=6,min=0,max=20,step=1,description='Electrical noise (meV)',continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	A_anaSlit=ipywidgets.widgets.SelectionSlider(
		options=[0.1,0.2,0.3,0.5,0.8,1.5],value=0.2,description="Analyer slit  (mm)",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	A_Ep=ipywidgets.widgets.SelectionSlider(
		options=[2,5,10,20,50,100,200],value=20,description="Pass energy   (eV)",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	B_anaSlit=ipywidgets.widgets.SelectionSlider(
		options=[0.05,0.1,0.2,0.5,0.8],value=0.2,description="Analyer slit  (mm)",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	B_Ep=ipywidgets.widgets.FloatSlider(
		value=20,min=2,max=60,step=1,description="Pass energy   (eV)",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	B_spinAperture=ipywidgets.widgets.SelectionSlider(
		options=[0.5,1,3,7],value=1,description="Spin aperture  (mm)",continuous_update=True,
		layout=ipywidgets.Layout(width='600px'),style=style)

	outputPanelA=ipywidgets.widgets.interactive_output(resolutionCalculator__A_update,{
		'grating':grating,
		'hv':hv,
		'hgap':hgap,
		'Ep':A_Ep,
		'anaSlit':A_anaSlit,
		'noise':noise,
	})

	outputPanelB=ipywidgets.widgets.interactive_output(resolutionCalculator__B_update,{
		'grating':grating,
		'hv':hv,
		'hgap':hgap,
		'Ep':B_Ep,
		'anaSlit':B_anaSlit,
		'spinAperture':B_spinAperture,
		'noise':noise,
	})

	controlPanelA = ipywidgets.widgets.VBox(
		[grating,hv,hgap,A_Ep,A_anaSlit,noise,outputPanelA],
		layout=ipywidgets.Layout(width='750px'))

	controlPanelB = ipywidgets.widgets.VBox(
		[grating,hv,hgap,B_Ep,B_anaSlit,B_spinAperture,noise,outputPanelB],
		layout=ipywidgets.Layout(width='750px'))

	tab.children = [controlPanelA,controlPanelB]
	tab.set_title(0, 'A endstation')
	tab.set_title(1, 'B endstation')
	display(tab)



def spotSize(hgap,vgap,beQuiet=False):
	# Simple model to match data measured 2022.09.23 on spot size sample at 100eV
	# That analysis was NOT deconvolved with the 5um feature size, so these values are likely an overestimate.

	if vgap<100: h=10
	else: h=10 + (vgap-100)*0.04

	if hgap<50: v=5
	else: v=5 + (hgap-50)*0.07
		
	if beQuiet==False:
		print("Approximate spot size at normal incidence (sample facing beam) = {:.1f}um (H) X {:.1f}um (V)".format(h,v))
		print("At normal emission (sample facing analyzer): {:.1f}um (H) X {:.1f}um (V)".format(h/math.sin(math.radians(51)),v))


	return h,v


# in meV
def analyzer_resolution(hemisphereRadius_mm,passEnergy_eV,slit_mm,beQuiet=False):
	if beQuiet==False:
		print("Theoretical analyzer resolution = {:.1f}meV".format(1000*passEnergy_eV*slit_mm/((2*hemisphereRadius_mm))))
	return 1000*passEnergy_eV*slit_mm/(2*hemisphereRadius_mm)
