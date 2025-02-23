from blochpesto import indexOfClosestValue,getAnalyzerWorkFunction
import blochpesto as pesto
import numpy as np
import scipy
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time
from lmfit import minimize, Parameters,fit_report
import time

try:	import matplotlib
except ImportError: print("\t(ERROR): Couldn't import the matplotlib module. This is required for basic functionality. Install it with the command 'pip install matplotlib'")
from packaging.version import Version
if Version(matplotlib.__version__) < Version("3.9.0"): pass
else: print("\n(warning): You have version {} of matplotlib installed, which currently breaks certain interactive functionality. The most recent fully supported version is 3.8.4. Regress with 'pip uninstall matplotlib' followed by 'pip install matplotlib=3.8.4' \n".format(matplotlib.__version__))


try:	import ipywidgets
except ImportError: print("\tWarning: Couldn't import the ipywidgets module. You will not be able to use any interactive functions")

def gaussConvolve(x,y,gauss_width):

	# Make a new x array associated with the convolution Gaussian
	# It should have the same delta as the input x-array, but be much 
	# wider in range to avoid edge effects.
	# Centered on zero
	x=np.array(x)
	y=np.array(y)
	x_range=x[-1]-x[0]
	x_delta=x[1]-x[0]
	conv_x=np.arange((-5*x_range), (5*x_range), x_delta)
	convolutionGaussian=np.exp(  -4*np.log(2)*np.power(conv_x/gauss_width,2)  )
	
	# Also make an extended x-wave associated with our convolved model. Same center as the input data
	conv_x=np.arange((x[0]-(5*x_range)), x[-1]+(5*x_range), x_delta)
	
	unconvolvedModel = y
	convolutionOutput = scipy.signal.convolve(unconvolvedModel,convolutionGaussian,mode="full")

	# The convolution output has the same xdelta and central x as our input wave, but the range is still extended.
	# So we need to trim from both ends until it matches the x-range of our input wave
	amountToTrim=int((len(convolutionOutput)-len(x))/2)
	convolvedModel=[]
	for ii in range(amountToTrim,amountToTrim+len(x)):
		convolvedModel.append(convolutionOutput[ii])

	v_max=max(convolvedModel)
	convolvedModel = (convolvedModel/v_max) #Normalize
	return convolvedModel

def fit_function_linearBG(offset,slope,x):
	x=np.array(x)
	model = offset+(slope*(x-x[-1]))
	return model  

def fit_function_lorentzian_doublet(amplitude,position,width,splitting,ratio,x):
	x=np.array(x)
	model = amplitude*(1/(1+ 4*((x-position)/width)**2)) + ratio*amplitude*(1/(1+ 4*((x-splitting-position)/width)**2))
	return model  
	
def fit_function_lorentzian(amplitude,position,width,x):
	x=np.array(x)
	model = amplitude*(1/(1+ 4*((x-position)/width)**2))
	return model  

def fit_function_gauss(amplitude,position,width,x):
	x=np.array(x)
	model = amplitude*np.exp(-4*np.log(2)*((x-position)/width)**2)
	return model  

def fit_function_gauss_doublet(amplitude,position,width,splitting,ratio,x):
	x=np.array(x)
	model = amplitude*np.exp(-4*np.log(2)*((x-position)/width)**2) + ratio*amplitude*np.exp(-4*np.log(2)*((x-splitting-position)/width)**2)
	return model  




class parameter():
	def __init__(self):
		self.unlocked=True
		self.value=None
		self.label=None
		self.lmfit_label=None
		self.parameterID = None
		self.trackOtherParameter=False
		self.minimum=None
		self.maximum=None


class feature():
	def __init__(self):
		self.type=""
		self.label=""
		self.parameters=[]

	def getParameterByLabel(self,label):
		for p in self.parameters:
			if p.label==label:
				return p

	def compose(self,x):
		y=np.array(x)

		if self.type == "Constant_background":
			for p in self.parameters:
				if p.label=="offset": offset = p.value   
			y.fill(offset)

		if self.type == "Linear_background":
			for p in self.parameters:
				if p.label=="offset": offset = p.value
				if p.label=="slope": slope = p.value 

			y=fit_function_linearBG(offset,slope,x) 

		if self.type == "Voigt_singlet":
			for p in self.parameters:
				if p.label=="amplitude": amplitude = p.value
				if p.label=="position": position = p.value 
				if p.label=="gauss_width": gauss_width = p.value 
				if p.label=="lorentz_width": lorentz_width = p.value 

			unconvolvedPeak = np.array(x)
			unconvolvedPeak = fit_function_lorentzian(amplitude,position,lorentz_width,x)
			y=amplitude*gaussConvolve(x,unconvolvedPeak,gauss_width) 

		if self.type == "Voigt_doublet":
			for p in self.parameters:
				if p.label=="amplitude": amplitude = p.value
				if p.label=="position": position = p.value 
				if p.label=="gauss_width": gauss_width = p.value 
				if p.label=="lorentz_width": lorentz_width = p.value 
				if p.label=="splitting": splitting = p.value 
				if p.label=="ratio": ratio = p.value 

			unconvolvedPeak = np.array(x)
			unconvolvedPeak = fit_function_lorentzian_doublet(amplitude,position,lorentz_width,splitting,ratio,x)
			y=amplitude*gaussConvolve(x,unconvolvedPeak,gauss_width) 

		if self.type == "Lorentzian_singlet":
			for p in self.parameters:
				if p.label=="amplitude": amplitude = p.value
				if p.label=="position": position = p.value 
				if p.label=="width": width = p.value 

			y=fit_function_lorentzian(amplitude,position,width,x)

		if self.type == "Lorentzian_doublet":
			for p in self.parameters:
				if p.label=="amplitude": amplitude = p.value
				if p.label=="position": position = p.value 
				if p.label=="width": width = p.value 
				if p.label=="splitting": splitting = p.value 
				if p.label=="ratio": ratio = p.value 

			y=fit_function_lorentzian_doublet(amplitude,position,width,x)

		if self.type == "Gaussian_singlet":
			for p in self.parameters:
				if p.label=="amplitude": amplitude = p.value
				if p.label=="position": position = p.value 
				if p.label=="width": width = p.value 

			y=fit_function_gauss(amplitude,position,width,x)

		if self.type == "Gaussian_doublet":
			for p in self.parameters:
				if p.label=="amplitude": amplitude = p.value
				if p.label=="position": position = p.value 
				if p.label=="width": width = p.value 
				if p.label=="splitting": splitting = p.value 
				if p.label=="ratio": ratio = p.value 

			y=fit_function_gauss_doublet(amplitude,position,width,splitting,ratio,x)


		return y


class peakFit():
	def __init__(self):
		self.numberOfParameters =  0
		self.numberOfFeatures = 0
		self.features = []
		self.lmfit_Parameters = Parameters()

	def appendLorentzian(self,amplitude,position,width,label=None):
		f=feature()
		f.type = "Lorentzian_singlet"
		if label==None: f.label=f.type
		else: f.label=label    

		f.parameters=[]

		p=parameter()
		p.label="amplitude"
		p.lmfit_label="p{}_{}__Lorentzian_amplitude".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=amplitude
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked) 
		f.parameters.append(p)

		p=parameter()
		p.label="position"
		p.lmfit_label="p{}_{}__Lorentzian_position".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=position
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="width"
		p.lmfit_label="p{}_{}__Lorentzian_width".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=width
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)
		
		self.features.append(f)

	def appendLorentzianDoublet(self,amplitude,position,width,splitting,ratio,label=None):
		f=feature()
		f.type = "Lorentzian_doublet"
		if label==None: f.label=f.type
		else: f.label=label    

		f.parameters=[]

		p=parameter()
		p.label="amplitude"
		p.lmfit_label="p{}_{}__Lorentzian_amplitude".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=amplitude
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked) 
		f.parameters.append(p)

		p=parameter()
		p.label="position"
		p.lmfit_label="p{}_{}__Lorentzian_position".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=position
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="width"
		p.lmfit_label="p{}_{}__Lorentzian_width".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=width
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="splitting"
		p.lmfit_label="p{}_{}__Lorentzian_splitting".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=splitting
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="ratio"
		p.lmfit_label="p{}_{}__Lorentzian_ratio".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=ratio
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		self.features.append(f)

	def appendGaussian(self,amplitude,position,width,label=None):
		f=feature()
		f.type = "Gaussian_singlet"
		if label==None: f.label=f.type
		else: f.label=label    

		f.parameters=[]

		p=parameter()
		p.label="amplitude"
		p.lmfit_label="p{}_{}__Gaussian_amplitude".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=amplitude
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked) 
		f.parameters.append(p)

		p=parameter()
		p.label="position"
		p.lmfit_label="p{}_{}__Gaussian_position".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=position
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="width"
		p.lmfit_label="p{}_{}__Gaussian_width".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=width
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)
 
		self.features.append(f)

	def appendGaussianDoublet(self,amplitude,position,width,splitting,ratio,label=None):
		f=feature()
		f.type = "Gaussian_doublet"
		if label==None: f.label=f.type
		else: f.label=label    

		f.parameters=[]

		p=parameter()
		p.label="amplitude"
		p.lmfit_label="p{}_{}__Gaussian_amplitude".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=amplitude
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked) 
		f.parameters.append(p)

		p=parameter()
		p.label="position"
		p.lmfit_label="p{}_{}__Gaussian_position".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=position
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="width"
		p.lmfit_label="p{}_{}__Gaussian_width".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=width
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="splitting"
		p.lmfit_label="p{}_{}__Gaussian_splitting".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=splitting
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="ratio"
		p.lmfit_label="p{}_{}__Gaussian_ratio".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=ratio
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		self.features.append(f)

	def appendVoigt(self,amplitude,position,gauss_width,lorentz_width,label=None):
		f=feature()
		f.type = "Voigt_singlet"
		if label==None: f.label=f.type
		else: f.label=label    

		f.parameters=[]

		p=parameter()
		p.label="amplitude"
		p.lmfit_label="p{}_{}__Voigt_amplitude".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=amplitude
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked) 
		f.parameters.append(p)

		p=parameter()
		p.label="position"
		p.lmfit_label="p{}_{}__Voigt_position".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=position
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="gauss_width"
		p.lmfit_label="p{}_{}__Voigt_gausswidth".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=gauss_width
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="lorentz_width"
		p.lmfit_label="p{}_{}__Voigt_lorentzwidth".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=lorentz_width
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		self.features.append(f)

	def appendVoigtDoublet(self,amplitude,position,gauss_width,lorentz_width,splitting,ratio,label=None):
		f=feature()
		f.type = "Voigt_doublet"
		if label==None: f.label=f.type
		else: f.label=label    

		f.parameters=[]

		p=parameter()
		p.label="amplitude"
		p.lmfit_label="p{}_{}__Voigt_amplitude".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=amplitude
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked) 
		f.parameters.append(p)

		p=parameter()
		p.label="position"
		p.lmfit_label="p{}_{}__Voigt_position".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=position
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="gauss_width"
		p.lmfit_label="p{}_{}__Voigt_gausswidth".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=gauss_width
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="lorentz_width"
		p.lmfit_label="p{}_{}__Voigt_lorentzwidth".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=lorentz_width
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="splitting"
		p.lmfit_label="p{}_{}__Voigt_splitting".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=splitting
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		p=parameter()
		p.label="ratio"
		p.lmfit_label="p{}_{}__Voigt_ratio".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=ratio
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		self.features.append(f)

	def append_BG_offset(self,offset):
		f=feature()
		f.type = "Constant_background"
		f.label=f.type  

		f.parameters=[]

		p=parameter()
		p.label="offset"
		p.lmfit_label="p{}_{}__BG_offset".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=offset
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p) 
 
		self.features.append(f)

	def append_BG_linear(self,offset,slope):
		f=feature()
		f.type = "Linear_background"
		f.label=f.type 

		f.parameters=[]

		p=parameter()
		p.label="offset"
		p.lmfit_label="p{}_{}__BG_offset".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=offset
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked) 
		f.parameters.append(p)

		p=parameter()
		p.label="slope"
		p.lmfit_label="p{}_{}__BG_slope".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=slope
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked)
		f.parameters.append(p)

		self.features.append(f)

	def append_BG_shirley(self,shirleyfactor):
		f=feature()
		f.type = "Shirley_background"
		f.label=f.type  

		f.parameters=[]

		p=parameter()
		p.label="shirleyfactor"
		p.lmfit_label="p{}_{}__shirley_factor".format(self.numberOfParameters,f.label)
		p.unlocked=True
		p.value=shirleyfactor
		p.trackOtherParameter=False
		p.parameterID = self.numberOfParameters
		self.numberOfParameters+=1
		self.lmfit_Parameters.add(p.lmfit_label, value=p.value, vary=p.unlocked) 
		f.parameters.append(p)
 
		self.features.append(f)

	def compose(self,x):
		x=np.array(x)
		y=np.array(x)
		y_bg=np.array(x)
		y,y_bg=0,0
		doShirley=False

		for f in self.features:
			if f.type in ["Voigt_singlet","Voigt_doublet","Lorentzian_singlet","Lorentzian_doublet","Gaussian_singlet","Gaussian_doublet"]:
				y+=f.compose(x)
			
			elif f.type in ["Linear_background","Constant_background"]:
				y_bg+=f.compose(x)
			
			elif f.type == "Shirley_background":
				shirleyfactor = f.parameters[0].value
				doShirley=True
			else:
				print("ERROR: Unknown feature type ('{}') passed to peakFit.compose()".format(f.type))

		if doShirley==True: y_bg+=np.flip(shirleyfactor*np.cumsum(y))
		
		return y+y_bg,y_bg

	def getParameterByID(self,parameterID):
		for f in self.features:
			for p in f.parameters:
				if p.parameterID==parameterID:
					return p

	def getFeatureByLabel(self,label):
		for f in self.features:
			if f.label==label:
				return f

	def composeAllFeatures(self,x):
		x=np.array(x)
		ys=[]
		labels=[]
		for f in self.features:
			if f.type in ["Voigt_singlet","Voigt_doublet","Lorentzian_singlet","Lorentzian_doublet","Gaussian_singlet","Gaussian_doublet"]:
				ys.append(f.compose(x))
				labels.append(f.label)
		return ys,labels

	def trackParameters(self,master,slave):
		slave.trackOtherParameter=master.parameterID

	def updateCoefficients(self,lmfit_output):
		
		for param in lmfit_output:
			name = str(param)
			value = lmfit_output[name].value
			for f in self.features:
				for p in f.parameters:
					if p.lmfit_label==name: p.value=value

		# Enact tracking
		for f in self.features:
			for p in f.parameters:
				if p.trackOtherParameter!=False:
					p0 = self.getParameterByID(p.trackOtherParameter)
					p.value=p0.value
					# UPDATE THE LMFIT VALUE ALSO!!!

		
	def residual(self,params,x, y):
		self.updateCoefficients(params)
		y_fit,bg_fit = self.compose(x)
		return (y-y_fit)

	def doFit(self,x,y,beQuiet=False):
		t0=time.time()

		# Lock any features that are supposed to track with another parameter, and configure max/min parameter values
		for f in self.features:
			for p in f.parameters:
				if p.trackOtherParameter!=False: p.unlocked=False
				if p.minimum!=None: self.lmfit_Parameters[p.lmfit_label].min = p.minimum
				if p.maximum!=None: self.lmfit_Parameters[p.lmfit_label].max = p.maximum

				if p.unlocked==False: self.lmfit_Parameters[p.lmfit_label].vary = False
				if p.unlocked==True: self.lmfit_Parameters[p.lmfit_label].vary = True

		out = minimize(fcn=self.residual, params=self.lmfit_Parameters,args=(x, y),method='leastsq')
		if beQuiet==False:
			print("scipy Fit completed in {:.3f}s".format(time.time()-t0))
			print(fit_report(out,show_correl=False))
		self.updateCoefficients(out.params)


	def fitSummary(self,x,y):
		fit,bg=self.compose(x)
		residual = y-fit 
		fig,axes=matplotlib.pyplot.subplots(figsize=[12,5],ncols=2)
		ax=axes[0]
		divider = make_axes_locatable(ax)
		ax.plot(x,y,label="Data")
		ax.plot(x,fit,label="Fit")
		ax.legend()
		ax2 = divider.append_axes("bottom", size="20%", pad=0)
		ax.figure.add_axes(ax2)
		ax2.plot(x,residual)
		ax.set_xticks([])
		ax.invert_xaxis()
		ax2.axhline(y=0,ls='--',color='black')
		ax2.set_ylim([-0.1*max(fit),0.1*max(fit)])
		ax2.set_xlabel("Binding energy (eV)")
		ax2.invert_xaxis()

		ax=axes[1]
		ax.plot(x,y,label="Data")
		ax.invert_xaxis()
		#ax.plot(x,fit,label="Fit")
		ax.plot(x,bg,label="Fit background")

		ys,labels=self.composeAllFeatures(x)
		for y,label in zip(ys,labels):
			ax.plot(x,y+bg,label=label)
	 
		ax.legend()
		matplotlib.pyplot.tight_layout()
		matplotlib.pyplot.show()
	


def addPeakLabel(axis,spectrum,hv=None,xrange=[None,None],label=''):

	if len(np.shape(spectrum['data']))>1:
		EDC = pesto.getProfile(spectrum=spectrum,samplingAxis='y',yAxisRange=[0,9999],xAxisRange=[-99,99],beQuiet=True)
	else:
		EDC = spectrum
		
	y = list(EDC['data'])
	yrange = max(y)-min(y)
	
	if hv is not None and EDC['AxisLabel'].startswith("Kinetic"): 
		x = [hv - getAnalyzerWorkFunction() - ii for ii in EDC['Axis']]
	else:
		x=EDC['Axis']

	peakIndexStart = indexOfClosestValue(x,xrange[0])
	peakIndexEnd = indexOfClosestValue(x,xrange[1])
	if peakIndexEnd<peakIndexStart: peakIndexStart,peakIndexEnd = peakIndexEnd,peakIndexStart
	subRegion = y[peakIndexStart:peakIndexEnd] 
	peakMax=max(subRegion) 
	peakIndex = indexOfClosestValue(y,peakMax)
	peakPosition = x[peakIndex]
	axis.annotate(label+"\n{:.1f}eV".format(peakPosition), xy=(peakPosition, peakMax), xytext=(peakPosition, peakMax+yrange*0.04),			ha='center')   



def searchByElement():
	def build_panel(element,input_hv):
		_searchByElement_ni(element,input_hv)

	style = {'description_width': 'initial'}

	elementNames=[]
	for element in elements:
		if element[1] not in elementNames:
			elementNames.append(element[1])

	elementSelector=ipywidgets.widgets.Dropdown(
	options=sorted(elementNames),
	value='Ge',
	description='Element:',
	disabled=False,
	style=style
	)

	hv=ipywidgets.widgets.FloatText(
	value=100,
	description='Photon energy',
	disabled=False,
	style=style
	)

	w = ipywidgets.interactive(
		build_panel,
		element=elementSelector,
		input_hv=hv
	)
	return w 

def _searchByElement_ni(elementName,hv=0): #non-interactive
	matches=[]
	for index,element in enumerate(elements):
		if element[1]==elementName:
			matches.append(element)
			
	if len(matches)==0:
		print("No matches")
	else:
		if hv>0:
			print("Core level\tBinding energy\tEk at hv={0}\tEk (2nd order)\tEk (3rd order)\tEk (4th order)".format(hv))
			print("---------------------------------------------------------------------------------------------")
			for element in matches:
				name = element[1]
				level = element[2]
				orbital = element[3]
				spin = element[4]
				literatureBindingEnergy = float(element[5])
				inaccessible=False
				Ek_1st_order = hv-getAnalyzerWorkFunction()-literatureBindingEnergy
				if Ek_1st_order<0:	
					Ek_1st_order=float('nan')
					inaccessible=True


				Ek_2nd_order = (hv*2)-getAnalyzerWorkFunction()-literatureBindingEnergy
				if Ek_2nd_order<0:	Ek_2nd_order=float('nan')

				Ek_3rd_order = (hv*3)-getAnalyzerWorkFunction()-literatureBindingEnergy
				if Ek_3rd_order<0:	Ek_3rd_order=float('nan')

				Ek_4th_order = (hv*4)-getAnalyzerWorkFunction()-literatureBindingEnergy
				if Ek_4th_order<0:	Ek_4th_order=float('nan')

				if spin=="0":
					if inaccessible: print("\033[91m{} {}{}\t\t{:.6}\t\t{:.6}\t\t{:.6}\t\t{:.6}\t\t{:.6}\x1b[0m".format(name,level,orbital,literatureBindingEnergy,Ek_1st_order,Ek_2nd_order,Ek_3rd_order,Ek_4th_order))
					else: print("\033[92m{} {}{}\t\t{:.6}\t\t{:.6}\t\t{:.6}\t\t{:.6}\t\t{:.6}\x1b[0m".format(name,level,orbital,literatureBindingEnergy,Ek_1st_order,Ek_2nd_order,Ek_3rd_order,Ek_4th_order))
				
				else:
					if inaccessible: print("\033[91m{} {}{} {}\t{:.6}\t\t{:.6}\t\t{:.6}\t\t{:.6}\t\t{:.6}\x1b[0m".format(name,level,orbital,spin,literatureBindingEnergy,Ek_1st_order,Ek_2nd_order,Ek_3rd_order,Ek_4th_order))
					else: print("\033[92m{} {}{} {}\t{:.6}\t\t{:.6}\t\t{:.6}\t\t{:.6}\t\t{:.6}\x1b[0m".format(name,level,orbital,spin,literatureBindingEnergy,Ek_1st_order,Ek_2nd_order,Ek_3rd_order,Ek_4th_order))
		else:
			print("Core level\tBinding energy")
			print("--------------------------------")
			for element in matches:
				name = element[1]
				level = element[2]
				orbital = element[3]
				spin = element[4]
				literatureBindingEnergy = float(element[5])
				
				if spin=="0": print("{0} {1}{2}\t\t{3:.6}".format(name,level,orbital,literatureBindingEnergy))
				else: print("{0} {1}{2} {3}\t{4:.6}".format(name,level,orbital,spin,literatureBindingEnergy))


def searchBySplitting():
	def build_panel(splitting,tolerance):
		_searchBySplitting_ni(splitting,tolerance)

	style = {'description_width': 'initial'}


	splitting=ipywidgets.widgets.FloatSlider(
	value=1,
	min = 0.05,
	max = 50,
	step=0.05,
	description='Splitting (eV)',
	disabled=False,
	layout=ipywidgets.Layout(width='600px'),
	style=style
	)

	tolerance=ipywidgets.widgets.FloatSlider(
	value=1,
	min=0,
	max=7,
	step=0.5,
	description='Tolerance (eV)',
	disabled=False,
	layout=ipywidgets.Layout(width='400px'),
	style=style
	)

	w = ipywidgets.interactive(
		build_panel,
		splitting=splitting,
		tolerance=tolerance
	)
	return w 

def _searchBySplitting_ni(splitting,tolerance):
	
	splittingList=[]
		
	for index,element in enumerate(elements):
		
		atomicNumber = element[0]
		name = element[1]
		level = element[2]
		orbital = element[3]
		spin = element[4]
		bindingEnergy = float(element[5])
		

		
		if ('p' or 'd' or 'f') in orbital:
			for subindex,subelement in enumerate(elements[index:]):
				atomicNumber2 = subelement[0]
				name2 = subelement[1]
				level2 = subelement[2]
				orbital2 = subelement[3]
				spin2 = subelement[4]
				bindingEnergy2 = subelement[5]
				
				if (name == name2) and (level == level2) and (orbital == orbital2) and (spin !=spin2 ):
					splittingList.append([name,level,orbital,float(abs(bindingEnergy-bindingEnergy2))])
	
	matches=[]                   
	for index,element in enumerate(splittingList):
		
		if element[3] > (splitting-tolerance) and element[3] < (splitting+tolerance):
			matches.append([element[0],element[1],element[2],element[3],splitting-element[3]])
		
	matches_sorted=sorted(matches,key=lambda x: x[4],reverse=True)
			
	if len(matches)==0:
		print("No matches")
	else:
		print("Doublet\t\tSplitting\tError")
		print("-------------------------------------------")
		for element in matches_sorted:
			print("{0} {1}{2}\t\t{3:.4}\t\t{4:.4}".format(element[0],element[1],element[2],element[3],splitting-element[3]))


def searchByEnergy():
	def build_panel(hv,energy,tolerance,mode,orders):
		if orders=='Only first order':orders=[1]
		else: orders=[1,2,3,4,5]
		if mode=='Kinetic': _search_by_Ek(energy,hv,tolerance,orders)
		else: _search_by_Eb(energy,tolerance,orders)

	style = {'description_width': 'initial'}

	hv=ipywidgets.widgets.FloatText(
	value=100,
	description='Photon energy (eV)',
	disabled=False,
	layout=ipywidgets.Layout(width='400px'),
	style=style
	)

	energy=ipywidgets.widgets.FloatSlider(
	value=30,
	min = 0.05,
	max = 1000,
	step=0.05,
	description='Energy of peak (eV)',
	disabled=False,
	layout=ipywidgets.Layout(width='600px'),
	style=style
	)

	mode=ipywidgets.widgets.RadioButtons(
	options=['Kinetic', 'Binding'],
	description=' ',
	value='Kinetic',
	)

	orders=ipywidgets.widgets.RadioButtons(
	options=['Only first order', 'All orders'],
	value='Only first order',
	description=' ',
	)

	tolerance=ipywidgets.widgets.FloatSlider(
	value=2.5,
	min=0,
	max=10,
	step=0.5,
	description='Tolerance (eV)',
	layout=ipywidgets.Layout(width='400px'),
	style=style
	)



	w = ipywidgets.interactive(
		build_panel,
		energy=energy,
		tolerance=tolerance,
		mode=mode,
		orders=orders,
		hv=hv
	)
	return w 

def _search_by_Eb(bindingEnergy,tolerance,orders):

	matches=[]
	for index,element in enumerate(elements):
		
		atomicNumber = element[0]
		name = element[1]
		level = element[2]
		orbital = element[3]
		spin = element[4]
		literatureBindingEnergy = float(element[5])
		
		if literatureBindingEnergy > (bindingEnergy-tolerance) and literatureBindingEnergy < (bindingEnergy+tolerance):
			matches.append([name,level,orbital,spin,literatureBindingEnergy,abs(bindingEnergy-literatureBindingEnergy)])

	matches_sorted=sorted(matches,key=lambda x: x[5])
			
	if len(matches)==0:
		print("No matches")
	else:
		print("Peak\t\tBinding energy\tError")
		print("----------------------------------------------")
		for element in matches_sorted:
			name = element[0]
			level = element[1]
			orbital = element[2]
			spin = element[3]
			literatureBindingEnergy = element[4]
			difference = element[5]
			
			if spin=="0":
				print("{0} {1}{2}\t\t{3:.4}\t\t{4:.4}".format(name,level,orbital,literatureBindingEnergy,difference))
			else:
				print("{0} {1}{2} {3}\t{4:.4}\t\t{5:.4}".format(name,level,orbital,spin,literatureBindingEnergy,difference))
	


def _search_by_Ek(Ek,hv,tolerance,orders):
	analyzerWorkFunction = 4.43

	matches=[]
	for index,element in enumerate(elements):
		
		atomicNumber = element[0]
		name = element[1]
		level = element[2]
		orbital = element[3]
		spin = element[4]
		literatureBindingEnergy = float(element[5])

		for order in orders:
			bindingEnergy = (hv*order)-analyzerWorkFunction-Ek
			literatureEk = (hv*order) - analyzerWorkFunction - literatureBindingEnergy
			if literatureBindingEnergy > ((bindingEnergy)-tolerance) and literatureBindingEnergy < (bindingEnergy+tolerance):
				matches.append([name,level,orbital,spin,literatureBindingEnergy,literatureEk,abs(bindingEnergy-literatureBindingEnergy),order])

	matches_sorted=sorted(matches,key=lambda x: x[6])
			
	if len(matches)==0:
		print("No matches")
	else:
		print("Peak\t\tEb\t\tEk\t\tOrder\t\tError")
		print("----------------------------------------------------------------------------")
		for element in matches_sorted:
			name = element[0]
			level = element[1]
			orbital = element[2]
			spin = element[3]
			literatureBindingEnergy = element[4]
			literatureEk = element[5]
			difference = element[6]
			order = element[7]

			if spin=="0":
				print("{0} {1}{2:5}\t{3:.1f}\t\t{4:.4}\t\t{5}\t\t{6:.4}".format(name,level,orbital,literatureBindingEnergy,literatureEk,order,difference))

			else:
				print("{0} {1}{2} {3}{2:5}\t{4:.1f}\t\t{5:.4}\t\t{6}\t\t{7:.4}".format(name,level,orbital,spin,literatureBindingEnergy,literatureEk,order,difference))

	
"""
Source: webelements.com, which references mostly Cardona and Ley, 
Photoemission in Solids I (1978)

Contains all non-radioactive elements (up to Bi)
"""


elements=[]

#Row 2
elements.append([3,"Li","1","s","0",54.7])
elements.append([4,"Be","1","s","0",111.5])
elements.append([5,"B","1","s","0",188])
elements.append([6,"C","1","s","0",284.2])
elements.append([7,"N","1","s","0",409.9])
elements.append([7,"N","2","s","0",37.3])
elements.append([8,"O","1","s","0",543.1])
elements.append([8,"O","2","s","0",41.6])
elements.append([9,"F","1","s","0",696.7])
elements.append([10,"Ne","1","s","0",870.2])
elements.append([10,"Ne","2","s","0",48.5])
elements.append([10,"Ne","2","p","1/2",21.7])
elements.append([10,"Ne","2","p","3/2",21.6])


#Row 3
elements.append([11,"Na","1","s","0",1070.8])
elements.append([11,"Na","2","s","0",63.5])
elements.append([11,"Na","2","p","1/2",30.4])
elements.append([11,"Na","2","p","3/2",30.5])
elements.append([12,"Mg","1","s","0",1303.0])
elements.append([12,"Mg","2","s","0",88.6])
elements.append([12,"Mg","2","p","1/2",49.6])
elements.append([12,"Mg","2","p","3/2",49.2])
elements.append([13,"Al","1","s","0",1559.0])
elements.append([13,"Al","2","s","0",117.8])
elements.append([13,"Al","2","p","1/2",72.9])
elements.append([13,"Al","2","p","3/2",72.5])
elements.append([14,"Si","1","s","0",1839.0])
elements.append([14,"Si","2","s","0",149.7])
elements.append([14,"Si","2","p","1/2",99.8])
elements.append([14,"Si","2","p","3/2",99.2])
elements.append([15,"P","1","s","0",2145.5])
elements.append([15,"P","2","s","0",189.0])
elements.append([15,"P","2","p","1/2",136.0])
elements.append([15,"P","2","p","3/2",135.0])
elements.append([16,"S","1","s","0",2472.0])
elements.append([16,"S","2","s","0",230.9])
elements.append([16,"S","2","p","1/2",163.6])
elements.append([16,"S","2","p","3/2",162.5])
elements.append([17,"Cl","1","s","0",2822])
elements.append([17,"Cl","2","s","0",270])
elements.append([17,"Cl","2","p","1/2",202])
elements.append([17,"Cl","2","p","3/2",200])
elements.append([18,"Ar","1","s","0",3205.9])
elements.append([18,"Ar","2","s","0",326.3])
elements.append([18,"Ar","2","p","1/2",250.6])
elements.append([18,"Ar","2","p","3/2",248.4])
elements.append([18,"Ar","3","s","0",29.3])
elements.append([18,"Ar","3","p","1/2",15.9])
elements.append([18,"Ar","3","p","3/2",15.7])

#Row 4
elements.append([19,"K","1","s","0",3608.4])
elements.append([19,"K","2","s","0",378.6])
elements.append([19,"K","2","p","1/2",297.3])
elements.append([19,"K","2","p","3/2",294.6])
elements.append([19,"K","3","s","0",34.8])
elements.append([19,"K","3","p","1/2",18.3])
elements.append([19,"K","3","p","3/2",18.3])
elements.append([20,"Ca","1","s","0",4038.5])
elements.append([20,"Ca","2","s","0",438.4])
elements.append([20,"Ca","2","p","1/2",349.7])
elements.append([20,"Ca","2","p","3/2",346.2])
elements.append([20,"Ca","3","s","0",44.3])
elements.append([20,"Ca","3","p","1/2",25.4])
elements.append([20,"Ca","3","p","3/2",25.4])
elements.append([21,"Sc","1","s","0",4492])
elements.append([21,"Sc","2","s","0",498])
elements.append([21,"Sc","2","p","1/2",403.6])
elements.append([21,"Sc","2","p","3/2",398.7])
elements.append([21,"Sc","3","s","0",51.1])
elements.append([21,"Sc","3","p","1/2",28.3])
elements.append([21,"Sc","3","p","3/2",28.3])
elements.append([22,"Ti","1","s","0",4966])
elements.append([22,"Ti","2","s","0",560.9])
elements.append([22,"Ti","2","p","1/2",460.2])
elements.append([22,"Ti","2","p","3/2",453.8])
elements.append([22,"Ti","3","s","0",58.7])
elements.append([22,"Ti","3","p","1/2",32.6])
elements.append([22,"Ti","3","p","3/2",32.6])
elements.append([23,"V","1","s","0",5465])
elements.append([23,"V","2","s","0",626.7])
elements.append([23,"V","2","p","1/2",519.8])
elements.append([23,"V","2","p","3/2",512.1])
elements.append([23,"V","3","s","0",66.3])
elements.append([23,"V","3","p","1/2",37.2])
elements.append([23,"V","3","p","3/2",37.2])
elements.append([24,"Cr","1","s","0",5989])
elements.append([24,"Cr","2","s","0",696])
elements.append([24,"Cr","2","p","1/2",583.8])
elements.append([24,"Cr","2","p","3/2",574.1])
elements.append([24,"Cr","3","s","0",74.1])
elements.append([24,"Cr","3","p","1/2",42.2])
elements.append([24,"Cr","3","p","3/2",42.2])
elements.append([25,"Mn","1","s","0",6539])
elements.append([25,"Mn","2","s","0",769.1])
elements.append([25,"Mn","2","p","1/2",649.9])
elements.append([25,"Mn","2","p","3/2",638.7])
elements.append([25,"Mn","3","s","0",82.3])
elements.append([25,"Mn","3","p","1/2",47.2])
elements.append([25,"Mn","3","p","3/2",47.2])
elements.append([26,"Fe","1","s","0",7112])
elements.append([26,"Fe","2","s","0",844.6])
elements.append([26,"Fe","2","p","1/2",719.9])
elements.append([26,"Fe","2","p","3/2",706.8])
elements.append([26,"Fe","3","s","0",91.3])
elements.append([26,"Fe","3","p","1/2",52.7])
elements.append([26,"Fe","3","p","3/2",52.7])
elements.append([27,"Co","1","s","0",7709])
elements.append([27,"Co","2","s","0",925.1])
elements.append([27,"Co","2","p","1/2",793.2])
elements.append([27,"Co","2","p","3/2",778.1])
elements.append([27,"Co","3","s","0",101])
elements.append([27,"Co","3","p","1/2",58.9])
elements.append([27,"Co","3","p","3/2",59.9])
elements.append([28,"Ni","1","s","0",8333])
elements.append([28,"Ni","2","s","0",1008.6])
elements.append([28,"Ni","2","p","1/2",870])
elements.append([28,"Ni","2","p","3/2",852.7])
elements.append([28,"Ni","3","s","0",110.8])
elements.append([28,"Ni","3","p","1/2",68])
elements.append([28,"Ni","3","p","3/2",66.2])
elements.append([29,"Cu","1","s","0",8979])
elements.append([29,"Cu","2","s","0",1096.7])
elements.append([29,"Cu","2","p","1/2",952.3])
elements.append([29,"Cu","2","p","3/2",932.7])
elements.append([29,"Cu","3","s","0",122.5])
elements.append([29,"Cu","3","p","1/2",77.3])
elements.append([29,"Cu","3","p","3/2",75.1])
elements.append([30,"Zn","1","s","0",9659])
elements.append([30,"Zn","2","s","0",1196.2])
elements.append([30,"Zn","2","p","1/2",1044.9])
elements.append([30,"Zn","2","p","3/2",1021.8])
elements.append([30,"Zn","3","s","0",139.8])
elements.append([30,"Zn","3","p","1/2",91.4])
elements.append([30,"Zn","3","p","3/2",88.6])
elements.append([30,"Zn","3","d","3/2",10.2])
elements.append([30,"Zn","3","d","5/2",10.1])
elements.append([31,"Ga","1","s","0",10367])
elements.append([31,"Ga","2","s","0",1299])
elements.append([31,"Ga","2","p","1/2",1143.2])
elements.append([31,"Ga","2","p","3/2",1116.4])
elements.append([31,"Ga","3","s","0",159.5])
elements.append([31,"Ga","3","p","1/2",103.5])
elements.append([31,"Ga","3","p","3/2",100])
elements.append([31,"Ga","3","d","3/2",18.7])
elements.append([31,"Ga","3","d","5/2",18.7])
elements.append([32,"Ge","1","s","0",11103])
elements.append([32,"Ge","2","s","0",1414.6])
elements.append([32,"Ge","2","p","1/2",1248.1])
elements.append([32,"Ge","2","p","3/2",1217])
elements.append([32,"Ge","3","s","0",180.1])
elements.append([32,"Ge","3","p","1/2",124.9])
elements.append([32,"Ge","3","p","3/2",120.8])
elements.append([32,"Ge","3","d","3/2",29.8])
elements.append([32,"Ge","3","d","5/2",29.2])
elements.append([33,"As","1","s","0",11867])
elements.append([33,"As","2","s","0",1527])
elements.append([33,"As","2","p","1/2",1359.1])
elements.append([33,"As","2","p","3/2",1323.6])
elements.append([33,"As","3","s","0",204.7])
elements.append([33,"As","3","p","1/2",146.2])
elements.append([33,"As","3","p","3/2",141.2])
elements.append([33,"As","3","d","3/2",41.7])
elements.append([33,"As","3","d","5/2",41.7])
elements.append([34,"Se","1","s","0",12658])
elements.append([34,"Se","2","s","0",1652])
elements.append([34,"Se","2","p","1/2",1474.3])
elements.append([34,"Se","2","p","3/2",1433.9])
elements.append([34,"Se","3","s","0",229.6])
elements.append([34,"Se","3","p","1/2",166.5])
elements.append([34,"Se","3","p","3/2",160.7])
elements.append([34,"Se","3","d","3/2",55.5])
elements.append([34,"Se","3","d","5/2",54.6])
elements.append([35,"Br","1","s","0",13474])
elements.append([35,"Br","2","s","0",1782])
elements.append([35,"Br","2","p","1/2",1596])
elements.append([35,"Br","2","p","3/2",1550])
elements.append([35,"Br","3","s","0",257])
elements.append([35,"Br","3","p","1/2",189])
elements.append([35,"Br","3","p","3/2",182])
elements.append([35,"Br","3","d","3/2",70])
elements.append([35,"Br","3","d","5/2",69])
elements.append([36,"Kr","1","s","0",14326])
elements.append([36,"Kr","2","s","0",1921])
elements.append([36,"Kr","2","p","1/2",1730.9])
elements.append([36,"Kr","2","p","3/2",1678.4])
elements.append([36,"Kr","3","s","0",292.8])
elements.append([36,"Kr","3","p","1/2",222.2])
elements.append([36,"Kr","3","p","3/2",214.4])
elements.append([36,"Kr","3","d","3/2",95])
elements.append([36,"Kr","3","d","5/2",93.8])
elements.append([36,"Kr","4","s","0",27.5])
elements.append([36,"Kr","4","p","1/2",14.1])
elements.append([36,"Kr","4","p","3/2",14.1])

#Row 5
elements.append([37,"Rb","1","s","0",15200])
elements.append([37,"Rb","2","s","0",2065])
elements.append([37,"Rb","2","p","1/2",1864])
elements.append([37,"Rb","2","p","3/2",1804])
elements.append([37,"Rb","3","s","0",326.7])
elements.append([37,"Rb","3","p","1/2",248.7])
elements.append([37,"Rb","3","p","3/2",239.1])
elements.append([37,"Rb","3","d","3/2",113])
elements.append([37,"Rb","3","d","5/2",112])
elements.append([37,"Rb","4","s","0",30.5])
elements.append([37,"Rb","4","p","1/2",16.3])
elements.append([37,"Rb","4","p","3/2",15.3])

elements.append([38,"Sr","1","s","0",16105])
elements.append([38,"Sr","2","s","0",2216])
elements.append([38,"Sr","2","p","1/2",2007])
elements.append([38,"Sr","2","p","3/2",1940])
elements.append([38,"Sr","3","s","0",358.7])
elements.append([38,"Sr","3","p","1/2",280.3])
elements.append([38,"Sr","3","p","3/2",270])
elements.append([38,"Sr","3","d","3/2",136])
elements.append([38,"Sr","3","d","5/2",134.2])
elements.append([38,"Sr","4","s","0",38.9])
elements.append([38,"Sr","4","p","1/2",21.6])
elements.append([38,"Sr","4","p","3/2",20.1])

elements.append([39,"Y","1","s","0",17038])
elements.append([39,"Y","2","s","0",2373])
elements.append([39,"Y","2","p","1/2",2156])
elements.append([39,"Y","2","p","3/2",2080])
elements.append([39,"Y","3","s","0",392])
elements.append([39,"Y","3","p","1/2",310.6])
elements.append([39,"Y","3","p","3/2",298.8])
elements.append([39,"Y","3","d","3/2",157.7])
elements.append([39,"Y","3","d","5/2",155.8])
elements.append([39,"Y","4","s","0",43.8])
elements.append([39,"Y","4","p","1/2",24.4])
elements.append([39,"Y","4","p","3/2",23.1])

elements.append([40,"Zr","1","s","0",17998])
elements.append([40,"Zr","2","s","0",2532])
elements.append([40,"Zr","2","p","1/2",2307])
elements.append([40,"Zr","2","p","3/2",2223])
elements.append([40,"Zr","3","s","0",430.3])
elements.append([40,"Zr","3","p","1/2",343.5])
elements.append([40,"Zr","3","p","3/2",329.8])
elements.append([40,"Zr","3","d","3/2",181.1])
elements.append([40,"Zr","3","d","5/2",178.8])
elements.append([40,"Zr","4","s","0",50.6])
elements.append([40,"Zr","4","p","1/2",28.5])
elements.append([40,"Zr","4","p","3/2",27.1])

elements.append([41,"Nb","1","s","0",18986])
elements.append([41,"Nb","2","s","0",2698])
elements.append([41,"Nb","2","p","1/2",2465])
elements.append([41,"Nb","2","p","3/2",2371])
elements.append([41,"Nb","3","s","0",466.6])
elements.append([41,"Nb","3","p","1/2",376.1])
elements.append([41,"Nb","3","p","3/2",360.6])
elements.append([41,"Nb","3","d","3/2",205])
elements.append([41,"Nb","3","d","5/2",202.3])
elements.append([41,"Nb","4","s","0",56.4])
elements.append([41,"Nb","4","p","1/2",32.6])
elements.append([41,"Nb","4","p","3/2",30.8])

elements.append([42,"Mo","1","s","0",20000])
elements.append([42,"Mo","2","s","0",2866])
elements.append([42,"Mo","2","p","1/2",2625])
elements.append([42,"Mo","2","p","3/2",2520])
elements.append([42,"Mo","3","s","0",506.3])
elements.append([42,"Mo","3","p","1/2",411.6])
elements.append([42,"Mo","3","p","3/2",394])
elements.append([42,"Mo","3","d","3/2",231.1])
elements.append([42,"Mo","3","d","5/2",227.9])
elements.append([42,"Mo","4","s","0",63.2])
elements.append([42,"Mo","4","p","1/2",37.6])
elements.append([42,"Mo","4","p","3/2",35.5])

elements.append([43,"Tc","1","s","0",21044])
elements.append([43,"Tc","2","s","0",3043])
elements.append([43,"Tc","2","p","1/2",2793])
elements.append([43,"Tc","2","p","3/2",2677])
elements.append([43,"Tc","3","s","0",544])
elements.append([43,"Tc","3","p","1/2",447.6])
elements.append([43,"Tc","3","p","3/2",417.7])
elements.append([43,"Tc","3","d","3/2",257.6])
elements.append([43,"Tc","3","d","5/2",253.9])
elements.append([43,"Tc","4","s","0",69.5])
elements.append([43,"Tc","4","p","1/2",42.3])
elements.append([43,"Tc","4","p","3/2",39.9])

elements.append([44,"Ru","1","s","0",22117])
elements.append([44,"Ru","2","s","0",3224])
elements.append([44,"Ru","2","p","1/2",2967])
elements.append([44,"Ru","2","p","3/2",2838])
elements.append([44,"Ru","3","s","0",586.1])
elements.append([44,"Ru","3","p","1/2",483.3])
elements.append([44,"Ru","3","p","3/2",461.5])
elements.append([44,"Ru","3","d","3/2",284.2])
elements.append([44,"Ru","3","d","5/2",280])
elements.append([44,"Ru","4","s","0",75])
elements.append([44,"Ru","4","p","1/2",46.3])
elements.append([44,"Ru","4","p","3/2",43.2])

elements.append([45,"Rh","1","s","0",23220])
elements.append([45,"Rh","2","s","0",3412])
elements.append([45,"Rh","2","p","1/2",3146])
elements.append([45,"Rh","2","p","3/2",3004])
elements.append([45,"Rh","3","s","0",628.1])
elements.append([45,"Rh","3","p","1/2",521.3])
elements.append([45,"Rh","3","p","3/2",496.5])
elements.append([45,"Rh","3","d","3/2",311.9])
elements.append([45,"Rh","3","d","5/2",307.2])
elements.append([45,"Rh","4","s","0",81.4])
elements.append([45,"Rh","4","p","1/2",50.5])
elements.append([45,"Rh","4","p","3/2",47.3])

elements.append([46,"Pd","1","s","0",24350])
elements.append([46,"Pd","2","s","0",3604])
elements.append([46,"Pd","2","p","1/2",3330])
elements.append([46,"Pd","2","p","3/2",3173])
elements.append([46,"Pd","3","s","0",671.6])
elements.append([46,"Pd","3","p","1/2",559.9])
elements.append([46,"Pd","3","p","3/2",532.3])
elements.append([46,"Pd","3","d","3/2",340.5])
elements.append([46,"Pd","3","d","5/2",335.2])
elements.append([46,"Pd","4","s","0",87.1])
elements.append([46,"Pd","4","p","1/2",55.7])
elements.append([46,"Pd","4","p","3/2",50.9])

elements.append([47,"Ag","1","s","0",25514])
elements.append([47,"Ag","2","s","0",3806])
elements.append([47,"Ag","2","p","1/2",3524])
elements.append([47,"Ag","2","p","3/2",3351])
elements.append([47,"Ag","3","s","0",719])
elements.append([47,"Ag","3","p","1/2",603.8])
elements.append([47,"Ag","3","p","3/2",573])
elements.append([47,"Ag","3","d","3/2",374])
elements.append([47,"Ag","3","d","5/2",368.3])
elements.append([47,"Ag","4","s","0",97])
elements.append([47,"Ag","4","p","1/2",63.7])
elements.append([47,"Ag","4","p","3/2",58.3])

elements.append([48,"Cd","1","s","0",26711])
elements.append([48,"Cd","2","s","0",4018])
elements.append([48,"Cd","2","p","1/2",3727])
elements.append([48,"Cd","2","p","3/2",3538])
elements.append([48,"Cd","3","s","0",772])
elements.append([48,"Cd","3","p","1/2",652.6])
elements.append([48,"Cd","3","p","3/2",618.4])
elements.append([48,"Cd","3","d","3/2",411.9])
elements.append([48,"Cd","3","d","5/2",405.2])
elements.append([48,"Cd","4","s","0",109.8])
elements.append([48,"Cd","4","p","1/2",63.9])
elements.append([48,"Cd","4","p","3/2",63.9])
elements.append([48,"Cd","4","d","3/2",11.7])
elements.append([48,"Cd","4","d","5/2",10.7])

elements.append([49,"In","1","s","0",27940])
elements.append([49,"In","2","s","0",4238])
elements.append([49,"In","2","p","1/2",3938])
elements.append([49,"In","2","p","3/2",3730])
elements.append([49,"In","3","s","0",827.2])
elements.append([49,"In","3","p","1/2",703.2])
elements.append([49,"In","3","p","3/2",665.3])
elements.append([49,"In","3","d","3/2",451.4])
elements.append([49,"In","3","d","5/2",443.9])
elements.append([49,"In","4","s","0",122.9])
elements.append([49,"In","4","p","1/2",73.5])
elements.append([49,"In","4","p","3/2",73.5])
elements.append([49,"In","4","d","3/2",17.7])
elements.append([49,"In","4","d","5/2",16.9])

elements.append([50,"Sn","1","s","0",29200])
elements.append([50,"Sn","2","s","0",4465])
elements.append([50,"Sn","2","p","1/2",4156])
elements.append([50,"Sn","2","p","3/2",3929])
elements.append([50,"Sn","3","s","0",884.7])
elements.append([50,"Sn","3","p","1/2",756.5])
elements.append([50,"Sn","3","p","3/2",714.6])
elements.append([50,"Sn","3","d","3/2",493.2])
elements.append([50,"Sn","3","d","5/2",484.9])
elements.append([50,"Sn","4","s","0",137.1])
elements.append([50,"Sn","4","p","1/2",83.6])
elements.append([50,"Sn","4","p","3/2",83.6])
elements.append([50,"Sn","4","d","3/2",24.9])
elements.append([50,"Sn","4","d","5/2",23.9])

elements.append([51,"Sb","1","s","0",30491])
elements.append([51,"Sb","2","s","0",4698])
elements.append([51,"Sb","2","p","1/2",4380])
elements.append([51,"Sb","2","p","3/2",4132])
elements.append([51,"Sb","3","s","0",940])
elements.append([51,"Sb","3","p","1/2",812.7])
elements.append([51,"Sb","3","p","3/2",766.4])
elements.append([51,"Sb","3","d","3/2",537.5])
elements.append([51,"Sb","3","d","5/2",528.2])
elements.append([51,"Sb","4","s","0",153.2])
elements.append([51,"Sb","4","p","1/2",95.6])
elements.append([51,"Sb","4","p","3/2",95.6])
elements.append([51,"Sb","4","d","3/2",33.3])
elements.append([51,"Sb","4","d","5/2",32.1])

elements.append([52,"Te","1","s","0",31814])
elements.append([52,"Te","2","s","0",4939])
elements.append([52,"Te","2","p","1/2",4612])
elements.append([52,"Te","2","p","3/2",4341])
elements.append([52,"Te","3","s","0",1006])
elements.append([52,"Te","3","p","1/2",870.8])
elements.append([52,"Te","3","p","3/2",820.8])
elements.append([52,"Te","3","d","3/2",583.4])
elements.append([52,"Te","3","d","5/2",573])
elements.append([52,"Te","4","s","0",169.4])
elements.append([52,"Te","4","p","1/2",103.3])
elements.append([52,"Te","4","p","3/2",103.3])
elements.append([52,"Te","4","d","3/2",41.9])
elements.append([52,"Te","4","d","5/2",40.4])

elements.append([53,"I","1","s","0",33169])
elements.append([53,"I","2","s","0",5188])
elements.append([53,"I","2","p","1/2",4852])
elements.append([53,"I","2","p","3/2",4557])
elements.append([53,"I","3","s","0",1072])
elements.append([53,"I","3","p","1/2",931])
elements.append([53,"I","3","p","3/2",875])
elements.append([53,"I","3","d","3/2",630.8])
elements.append([53,"I","3","d","5/2",619.3])
elements.append([53,"I","4","s","0",186])
elements.append([53,"I","4","p","1/2",123])
elements.append([53,"I","4","p","3/2",123])
elements.append([53,"I","4","d","3/2",50.6])
elements.append([53,"I","4","d","5/2",48.9])

elements.append([54,"Xe","1","s","0",34561])
elements.append([54,"Xe","2","s","0",5453])
elements.append([54,"Xe","2","p","1/2",5107])
elements.append([54,"Xe","2","p","3/2",4786])
elements.append([54,"Xe","3","s","0",1148.7])
elements.append([54,"Xe","3","p","1/2",1002.1])
elements.append([54,"Xe","3","p","3/2",940.6])
elements.append([54,"Xe","3","d","3/2",689])
elements.append([54,"Xe","3","d","5/2",676.4])
elements.append([54,"Xe","4","s","0",213.2])
elements.append([54,"Xe","4","p","1/2",146.7])
elements.append([54,"Xe","4","p","3/2",145.5])
elements.append([54,"Xe","4","d","3/2",69.5])
elements.append([54,"Xe","4","d","5/2",67.5])
elements.append([54,"Xe","5","s","0",23.3])
elements.append([54,"Xe","5","p","1/2",13.4])
elements.append([54,"Xe","5","p","3/2",12.1])

####Row 6

elements.append([55,"Cs","1","s","0",35985])
elements.append([55,"Cs","2","s","0",5714])
elements.append([55,"Cs","2","p","1/2",5359])
elements.append([55,"Cs","2","p","3/2",5012])
elements.append([55,"Cs","3","s","0",1211])
elements.append([55,"Cs","3","p","1/2",1071])
elements.append([55,"Cs","3","p","3/2",1003])
elements.append([55,"Cs","3","d","3/2",740.5])
elements.append([55,"Cs","3","d","5/2",726.6])
elements.append([55,"Cs","4","s","0",232.3])
elements.append([55,"Cs","4","p","1/2",172.4])
elements.append([55,"Cs","4","p","3/2",161.3])
elements.append([55,"Cs","4","d","3/2",79.8])
elements.append([55,"Cs","4","d","5/2",77.5])
elements.append([55,"Cs","5","s","0",22.7])
elements.append([55,"Cs","5","p","1/2",14.2])
elements.append([55,"Cs","5","p","3/2",12.1])

elements.append([56,"Ba","1","s","0",37441])
elements.append([56,"Ba","2","s","0",5989])
elements.append([56,"Ba","2","p","1/2",5624])
elements.append([56,"Ba","2","p","3/2",5247])
elements.append([56,"Ba","3","s","0",1293])
elements.append([56,"Ba","3","p","1/2",1137])
elements.append([56,"Ba","3","p","3/2",1063])
elements.append([56,"Ba","3","d","3/2",795.7])
elements.append([56,"Ba","3","d","5/2",780.5])
elements.append([56,"Ba","4","s","0",253.5])
elements.append([56,"Ba","4","p","1/2",192])
elements.append([56,"Ba","4","p","3/2",178.6])
elements.append([56,"Ba","4","d","3/2",92.6])
elements.append([56,"Ba","4","d","5/2",89.9])
elements.append([56,"Ba","5","s","0",30.3])
elements.append([56,"Ba","5","p","1/2",17])
elements.append([56,"Ba","5","p","3/2",14.8])

elements.append([57,"La","1","s","0",38925])
elements.append([57,"La","2","s","0",6266])
elements.append([57,"La","2","p","1/2",5891])
elements.append([57,"La","2","p","3/2",5483])
elements.append([57,"La","3","s","0",1362])
elements.append([57,"La","3","p","1/2",1209])
elements.append([57,"La","3","p","3/2",1128])
elements.append([57,"La","3","d","3/2",853])
elements.append([57,"La","3","d","5/2",836])
elements.append([57,"La","4","s","0",274.7])
elements.append([57,"La","4","p","1/2",205.8])
elements.append([57,"La","4","p","3/2",196])
elements.append([57,"La","4","d","3/2",105.3])
elements.append([57,"La","4","d","5/2",102.5])
elements.append([57,"La","5","s","0",34.3])
elements.append([57,"La","5","p","1/2",19.3])
elements.append([57,"La","5","p","3/2",16.8])

elements.append([58,"Ce","1","s","0",40443])
elements.append([58,"Ce","2","s","0",6548])
elements.append([58,"Ce","2","p","1/2",6164])
elements.append([58,"Ce","2","p","3/2",5723])
elements.append([58,"Ce","3","s","0",1436])
elements.append([58,"Ce","3","p","1/2",1274])
elements.append([58,"Ce","3","p","3/2",1187])
elements.append([58,"Ce","3","d","3/2",902.4])
elements.append([58,"Ce","3","d","5/2",883.8])
elements.append([58,"Ce","4","s","0",291])
elements.append([58,"Ce","4","p","1/2",223.2])
elements.append([58,"Ce","4","p","3/2",206.5])
elements.append([58,"Ce","4","d","3/2",109])
elements.append([58,"Ce","4","f","5/2",0.1])
elements.append([58,"Ce","4","f","7/2",0.1])
elements.append([58,"Ce","5","s","0",37.8])
elements.append([58,"Ce","5","p","1/2",19.8])
elements.append([58,"Ce","5","p","3/2",17])

elements.append([59,"Pr","1","s","0",41991])
elements.append([59,"Pr","2","s","0",6835])
elements.append([59,"Pr","2","p","1/2",6440])
elements.append([59,"Pr","2","p","3/2",5964])
elements.append([59,"Pr","3","s","0",1511])
elements.append([59,"Pr","3","p","1/2",1337])
elements.append([59,"Pr","3","p","3/2",1242])
elements.append([59,"Pr","3","d","3/2",948.3])
elements.append([59,"Pr","3","d","5/2",928.8])
elements.append([59,"Pr","4","s","0",304.5])
elements.append([59,"Pr","4","p","1/2",236.3])
elements.append([59,"Pr","4","p","3/2",217.6])
elements.append([59,"Pr","4","d","3/2",115.1])
elements.append([59,"Pr","4","d","5/2",115.1])
elements.append([59,"Pr","4","f","5/2",2])
elements.append([59,"Pr","4","f","7/2",2])
elements.append([59,"Pr","5","s","0",37.4])
elements.append([59,"Pr","5","p","1/2",22.3])
elements.append([59,"Pr","5","p","3/2",22.3])

elements.append([60,"Nd","1","s","0",43569])
elements.append([60,"Nd","2","s","0",7126])
elements.append([60,"Nd","2","p","1/2",6722])
elements.append([60,"Nd","2","p","3/2",6208])
elements.append([60,"Nd","3","s","0",1575])
elements.append([60,"Nd","3","p","1/2",1403])
elements.append([60,"Nd","3","p","3/2",1297])
elements.append([60,"Nd","3","d","3/2",1003.3])
elements.append([60,"Nd","3","d","5/2",980.4])
elements.append([60,"Nd","4","s","0",319.2])
elements.append([60,"Nd","4","p","1/2",243.3])
elements.append([60,"Nd","4","p","3/2",224.6])
elements.append([60,"Nd","4","d","3/2",120.5])
elements.append([60,"Nd","4","d","5/2",120.5])
elements.append([60,"Nd","4","f","5/2",1.5])
elements.append([60,"Nd","4","f","7/2",1.5])
elements.append([60,"Nd","5","s","0",37.5])
elements.append([60,"Nd","5","p","1/2",21.1])
elements.append([60,"Nd","5","p","3/2",21.1])

elements.append([61,"Pm","1","s","0",45184])
elements.append([61,"Pm","2","s","0",7428])
elements.append([61,"Pm","2","p","1/2",7013])
elements.append([61,"Pm","2","p","3/2",6459])
elements.append([61,"Pm","3","p","1/2",1471.4])
elements.append([61,"Pm","3","p","3/2",1357])
elements.append([61,"Pm","3","d","3/2",1052])
elements.append([61,"Pm","3","d","5/2",1027])
elements.append([61,"Pm","4","p","1/2",242])
elements.append([61,"Pm","4","p","3/2",242])
elements.append([61,"Pm","4","d","3/2",120])
elements.append([61,"Pm","4","d","5/2",120])


elements.append([62,"Sm","1","s","0",46834])
elements.append([62,"Sm","2","s","0",7737])
elements.append([62,"Sm","2","p","1/2",7312])
elements.append([62,"Sm","2","p","3/2",6716])
elements.append([62,"Sm","3","s","0",1723])
elements.append([62,"Sm","3","p","1/2",1541])
elements.append([62,"Sm","3","p","3/2",1419.8])
elements.append([62,"Sm","3","d","3/2",1110.9])
elements.append([62,"Sm","3","d","5/2",1083.4])
elements.append([62,"Sm","4","s","0",347.2])
elements.append([62,"Sm","4","p","1/2",265.6])
elements.append([62,"Sm","4","p","3/2",247.4])
elements.append([62,"Sm","4","d","3/2",129])
elements.append([62,"Sm","4","d","5/2",129])
elements.append([62,"Sm","4","f","5/2",5.2])
elements.append([62,"Sm","4","f","7/2",5.2])
elements.append([62,"Sm","5","s","0",37.4])
elements.append([62,"Sm","5","p","1/2",21.3])
elements.append([62,"Sm","5","p","3/2",21.3])

elements.append([63,"Eu","1","s","0",48519])
elements.append([63,"Eu","2","s","0",8052])
elements.append([63,"Eu","2","p","1/2",7617])
elements.append([63,"Eu","2","p","3/2",6977])
elements.append([63,"Eu","3","s","0",1800])
elements.append([63,"Eu","3","p","1/2",1614])
elements.append([63,"Eu","3","p","3/2",1481])
elements.append([63,"Eu","3","d","3/2",1158.6])
elements.append([63,"Eu","3","d","5/2",1127.5])
elements.append([63,"Eu","4","s","0",360])
elements.append([63,"Eu","4","p","1/2",284])
elements.append([63,"Eu","4","p","3/2",257])
elements.append([63,"Eu","4","d","3/2",133])
elements.append([63,"Eu","4","d","5/2",127.7])
elements.append([63,"Eu","4","f","5/2",0])
elements.append([63,"Eu","4","f","7/2",0])
elements.append([63,"Eu","5","s","0",32])
elements.append([63,"Eu","5","p","1/2",22])
elements.append([63,"Eu","5","p","3/2",22])

elements.append([64,"Gd","1","s","0",50239])
elements.append([64,"Gd","2","s","0",8376])
elements.append([64,"Gd","2","p","1/2",7930])
elements.append([64,"Gd","2","p","3/2",7243])
elements.append([64,"Gd","3","s","0",1881])
elements.append([64,"Gd","3","p","1/2",1688])
elements.append([64,"Gd","3","p","3/2",1544])
elements.append([64,"Gd","3","d","3/2",1221.9])
elements.append([64,"Gd","3","d","5/2",1189.6])
elements.append([64,"Gd","4","s","0",378.6])
elements.append([64,"Gd","4","p","1/2",286])
elements.append([64,"Gd","4","p","3/2",271])
elements.append([64,"Gd","4","d","5/2",142.6])
elements.append([64,"Gd","4","f","5/2",8.6])
elements.append([64,"Gd","4","f","7/2",8.6])
elements.append([64,"Gd","5","s","0",36])
elements.append([64,"Gd","5","p","1/2",20])
elements.append([64,"Gd","5","p","3/2",20])

elements.append([65,"Tb","1","s","0",51996])
elements.append([65,"Tb","2","s","0",8708])
elements.append([65,"Tb","2","p","1/2",8252])
elements.append([65,"Tb","2","p","3/2",7514])
elements.append([65,"Tb","3","s","0",1968])
elements.append([65,"Tb","3","p","1/2",1768])
elements.append([65,"Tb","3","p","3/2",1611])
elements.append([65,"Tb","3","d","3/2",1276.9])
elements.append([65,"Tb","3","d","5/2",1241.1])
elements.append([65,"Tb","4","s","0",396])
elements.append([65,"Tb","4","p","1/2",322.4])
elements.append([65,"Tb","4","p","3/2",284.1])
elements.append([65,"Tb","4","d","3/2",150.5])
elements.append([65,"Tb","4","d","5/2",150.5])
elements.append([65,"Tb","4","f","5/2",7.7])
elements.append([65,"Tb","4","f","7/2",2.4])
elements.append([65,"Tb","5","s","0",45.6])
elements.append([65,"Tb","5","p","1/2",28.7])
elements.append([65,"Tb","5","p","3/2",22.6])

elements.append([66,"Dy","1","s","0",53789])
elements.append([66,"Dy","2","s","0",9046])
elements.append([66,"Dy","2","p","1/2",8581])
elements.append([66,"Dy","2","p","3/2",7790])
elements.append([66,"Dy","3","s","0",2047])
elements.append([66,"Dy","3","p","1/2",1842])
elements.append([66,"Dy","3","p","3/2",1676])
elements.append([66,"Dy","3","d","3/2",1333])
elements.append([66,"Dy","3","d","5/2",1292])
elements.append([66,"Dy","4","s","0",414.2])
elements.append([66,"Dy","4","p","1/2",333.5])
elements.append([66,"Dy","4","p","3/2",293.2])
elements.append([66,"Dy","4","d","3/2",153.6])
elements.append([66,"Dy","4","d","5/2",153.6])
elements.append([66,"Dy","4","f","5/2",8])
elements.append([66,"Dy","4","f","7/2",4.3])
elements.append([66,"Dy","5","s","0",49.9])
elements.append([66,"Dy","5","p","1/2",26.3])
elements.append([66,"Dy","5","p","3/2",26.3])

elements.append([67,"Ho","1","s","0",55618])
elements.append([67,"Ho","2","s","0",9394])
elements.append([67,"Ho","2","p","1/2",8918])
elements.append([67,"Ho","2","p","3/2",8071])
elements.append([67,"Ho","3","s","0",2128])
elements.append([67,"Ho","3","p","1/2",1923])
elements.append([67,"Ho","3","p","3/2",1741])
elements.append([67,"Ho","3","d","3/2",1392])
elements.append([67,"Ho","3","d","5/2",1351])
elements.append([67,"Ho","4","s","0",432.4])
elements.append([67,"Ho","4","p","1/2",343.5])
elements.append([67,"Ho","4","p","3/2",308.2])
elements.append([67,"Ho","4","d","3/2",160])
elements.append([67,"Ho","4","d","5/2",160])
elements.append([67,"Ho","4","f","5/2",8.6])
elements.append([67,"Ho","4","f","7/2",5.2])
elements.append([67,"Ho","5","s","0",49.3])
elements.append([67,"Ho","5","p","1/2",30.8])
elements.append([67,"Ho","5","p","3/2",24.1])

elements.append([68,"Er","1","s","0",57486])
elements.append([68,"Er","2","s","0",9751])
elements.append([68,"Er","2","p","1/2",9264])
elements.append([68,"Er","2","p","3/2",8358])
elements.append([68,"Er","3","s","0",2206])
elements.append([68,"Er","3","p","1/2",2006])
elements.append([68,"Er","3","p","3/2",1812])
elements.append([68,"Er","3","d","3/2",1453])
elements.append([68,"Er","3","d","5/2",1409])
elements.append([68,"Er","4","s","0",449.8])
elements.append([68,"Er","4","p","1/2",366.2])
elements.append([68,"Er","4","p","3/2",320.2])
elements.append([68,"Er","4","d","3/2",167.6])
elements.append([68,"Er","4","d","5/2",167.6])
elements.append([68,"Er","4","f","7/2",4.7])
elements.append([68,"Er","5","s","0",50.6])
elements.append([68,"Er","5","p","1/2",31.4])
elements.append([68,"Er","5","p","3/2",24.7])

elements.append([69,"Tm","1","s","0",59390])
elements.append([69,"Tm","2","s","0",10116])
elements.append([69,"Tm","2","p","1/2",9617])
elements.append([69,"Tm","2","p","3/2",8648])
elements.append([69,"Tm","3","s","0",2307])
elements.append([69,"Tm","3","p","1/2",2090])
elements.append([69,"Tm","3","p","3/2",1885])
elements.append([69,"Tm","3","d","3/2",1515])
elements.append([69,"Tm","3","d","5/2",1468])
elements.append([69,"Tm","4","s","0",470.9])
elements.append([69,"Tm","4","p","1/2",385.9])
elements.append([69,"Tm","4","p","3/2",332.6])
elements.append([69,"Tm","4","d","3/2",175.5])
elements.append([69,"Tm","4","d","5/2",175.5])
elements.append([69,"Tm","4","f","7/2",4.6])
elements.append([69,"Tm","5","s","0",54.7])
elements.append([69,"Tm","5","p","1/2",31.8])
elements.append([69,"Tm","5","p","3/2",25])

elements.append([70,"Yb","1","s","0",61332])
elements.append([70,"Yb","2","s","0",10486])
elements.append([70,"Yb","2","p","1/2",9978])
elements.append([70,"Yb","2","p","3/2",8944])
elements.append([70,"Yb","3","s","0",2398])
elements.append([70,"Yb","3","p","1/2",2173])
elements.append([70,"Yb","3","p","3/2",1950])
elements.append([70,"Yb","3","d","3/2",1576])
elements.append([70,"Yb","3","d","5/2",1528])
elements.append([70,"Yb","4","s","0",480.5])
elements.append([70,"Yb","4","p","1/2",388.7])
elements.append([70,"Yb","4","p","3/2",339.7])
elements.append([70,"Yb","4","d","3/2",191.2])
elements.append([70,"Yb","4","d","5/2",182.4])
elements.append([70,"Yb","4","f","5/2",2.5])
elements.append([70,"Yb","4","f","7/2",1.3])
elements.append([70,"Yb","5","s","0",52])
elements.append([70,"Yb","5","p","1/2",30.3])
elements.append([70,"Yb","5","p","3/2",24.1])

elements.append([71,"Lu","1","s","0",63314])
elements.append([71,"Lu","2","s","0",10870])
elements.append([71,"Lu","2","p","1/2",10349])
elements.append([71,"Lu","2","p","3/2",9244])
elements.append([71,"Lu","3","s","0",2491])
elements.append([71,"Lu","3","p","1/2",2264])
elements.append([71,"Lu","3","p","3/2",2024])
elements.append([71,"Lu","3","d","3/2",1639])
elements.append([71,"Lu","3","d","5/2",1589])
elements.append([71,"Lu","4","s","0",506.8])
elements.append([71,"Lu","4","p","1/2",412.4])
elements.append([71,"Lu","4","p","3/2",359.2])
elements.append([71,"Lu","4","d","3/2",206.1])
elements.append([71,"Lu","4","d","5/2",196.3])
elements.append([71,"Lu","4","f","5/2",8.9])
elements.append([71,"Lu","4","f","7/2",7.5])
elements.append([71,"Lu","5","s","0",57.3])
elements.append([71,"Lu","5","p","1/2",33.6])
elements.append([71,"Lu","5","p","3/2",26.7])

elements.append([72,"Hf","1","s","0",65351])
elements.append([72,"Hf","2","s","0",11271])
elements.append([72,"Hf","2","p","1/2",10739])
elements.append([72,"Hf","2","p","3/2",9561])
elements.append([72,"Hf","3","s","0",2601])
elements.append([72,"Hf","3","p","1/2",2365])
elements.append([72,"Hf","3","p","3/2",2107])
elements.append([72,"Hf","3","d","3/2",1716])
elements.append([72,"Hf","3","d","5/2",1662])
elements.append([72,"Hf","4","s","0",538])
elements.append([72,"Hf","4","p","1/2",438.2])
elements.append([72,"Hf","4","p","3/2",380.7])
elements.append([72,"Hf","4","d","3/2",220])
elements.append([72,"Hf","4","d","5/2",211.5])
elements.append([72,"Hf","4","f","5/2",15.9])
elements.append([72,"Hf","4","f","7/2",14.2])
elements.append([72,"Hf","5","s","0",64.2])
elements.append([72,"Hf","5","p","1/2",38])
elements.append([72,"Hf","5","p","3/2",29.9])

elements.append([73,"Ta","1","s","0",67416])
elements.append([73,"Ta","2","s","0",11682])
elements.append([73,"Ta","2","p","1/2",11136])
elements.append([73,"Ta","2","p","3/2",9881])
elements.append([73,"Ta","3","s","0",2708])
elements.append([73,"Ta","3","p","1/2",2469])
elements.append([73,"Ta","3","p","3/2",2194])
elements.append([73,"Ta","3","d","3/2",1793])
elements.append([73,"Ta","3","d","5/2",1735])
elements.append([73,"Ta","4","s","0",563.4])
elements.append([73,"Ta","4","p","1/2",463.4])
elements.append([73,"Ta","4","p","3/2",400.9])
elements.append([73,"Ta","4","d","3/2",237.9])
elements.append([73,"Ta","4","d","5/2",226.4])
elements.append([73,"Ta","4","f","5/2",23.5])
elements.append([73,"Ta","4","f","7/2",21.6])
elements.append([73,"Ta","5","s","0",69.7])
elements.append([73,"Ta","5","p","1/2",42.2])
elements.append([73,"Ta","5","p","3/2",32.7])

elements.append([74,"W","1","s","0",69525])
elements.append([74,"W","2","s","0",12100])
elements.append([74,"W","2","p","1/2",11544])
elements.append([74,"W","2","p","3/2",10207])
elements.append([74,"W","3","s","0",2820])
elements.append([74,"W","3","p","1/2",2575])
elements.append([74,"W","3","p","3/2",2281])
elements.append([74,"W","3","d","3/2",1949])
elements.append([74,"W","3","d","5/2",1809])
elements.append([74,"W","4","s","0",594.1])
elements.append([74,"W","4","p","1/2",490.4])
elements.append([74,"W","4","p","3/2",423.6])
elements.append([74,"W","4","d","3/2",255.9])
elements.append([74,"W","4","d","5/2",243.5])
elements.append([74,"W","4","f","5/2",33.6])
elements.append([74,"W","4","f","7/2",31.4])
elements.append([74,"W","5","s","0",75.6])
elements.append([74,"W","5","p","1/2",45.3])
elements.append([74,"W","5","p","3/2",36.8])

elements.append([75,"Re","1","s","0",71676])
elements.append([75,"Re","2","s","0",12527])
elements.append([75,"Re","2","p","1/2",11959])
elements.append([75,"Re","2","p","3/2",10535])
elements.append([75,"Re","3","s","0",2932])
elements.append([75,"Re","3","p","1/2",2682])
elements.append([75,"Re","3","p","3/2",2367])
elements.append([75,"Re","3","d","3/2",1949])
elements.append([75,"Re","3","d","5/2",1883])
elements.append([75,"Re","4","s","0",625.4])
elements.append([75,"Re","4","p","1/2",518.7])
elements.append([75,"Re","4","p","3/2",446.8])
elements.append([75,"Re","4","d","3/2",273.9])
elements.append([75,"Re","4","d","5/2",260.5])
elements.append([75,"Re","4","f","5/2",42.9])
elements.append([75,"Re","4","f","7/2",40.5])
elements.append([75,"Re","5","s","0",83])
elements.append([75,"Re","5","p","1/2",45.6])
elements.append([75,"Re","5","p","3/2",34.6])

elements.append([76,"Os","1","s","0",73871])
elements.append([76,"Os","2","s","0",12968])
elements.append([76,"Os","2","p","1/2",12385])
elements.append([76,"Os","2","p","3/2",10871])
elements.append([76,"Os","3","s","0",3049])
elements.append([76,"Os","3","p","1/2",2792])
elements.append([76,"Os","3","p","3/2",2457])
elements.append([76,"Os","3","d","3/2",2031])
elements.append([76,"Os","3","d","5/2",1960])
elements.append([76,"Os","4","s","0",658.2])
elements.append([76,"Os","4","p","1/2",549.1])
elements.append([76,"Os","4","p","3/2",470.7])
elements.append([76,"Os","4","d","3/2",293.1])
elements.append([76,"Os","4","d","5/2",278.5])
elements.append([76,"Os","4","f","5/2",53.4])
elements.append([76,"Os","4","f","7/2",50.7])
elements.append([76,"Os","5","s","0",84])
elements.append([76,"Os","5","p","1/2",58])
elements.append([76,"Os","5","p","3/2",44.5])

elements.append([77,"Ir","1","s","0",76111])
elements.append([77,"Ir","2","s","0",13419])
elements.append([77,"Ir","2","p","1/2",12824])
elements.append([77,"Ir","2","p","3/2",11215])
elements.append([77,"Ir","3","s","0",3174])
elements.append([77,"Ir","3","p","1/2",2909])
elements.append([77,"Ir","3","p","3/2",2551])
elements.append([77,"Ir","3","d","3/2",2116])
elements.append([77,"Ir","3","d","5/2",2040])
elements.append([77,"Ir","4","s","0",691.1])
elements.append([77,"Ir","4","p","1/2",577.8])
elements.append([77,"Ir","4","p","3/2",495.8])
elements.append([77,"Ir","4","d","3/2",311.9])
elements.append([77,"Ir","4","d","5/2",296.3])
elements.append([77,"Ir","4","f","5/2",63.8])
elements.append([77,"Ir","4","f","7/2",60.8])
elements.append([77,"Ir","5","s","0",95.2])
elements.append([77,"Ir","5","p","1/2",63])
elements.append([77,"Ir","5","p","3/2",48])

elements.append([78,"Pt","1","s","0",78395])
elements.append([78,"Pt","2","s","0",13880])
elements.append([78,"Pt","2","p","1/2",13273])
elements.append([78,"Pt","2","p","3/2",11564])
elements.append([78,"Pt","3","s","0",3296])
elements.append([78,"Pt","3","p","1/2",3027])
elements.append([78,"Pt","3","p","3/2",2645])
elements.append([78,"Pt","3","d","3/2",2202])
elements.append([78,"Pt","3","d","5/2",2122])
elements.append([78,"Pt","4","s","0",725.4])
elements.append([78,"Pt","4","p","1/2",609.1])
elements.append([78,"Pt","4","p","3/2",519.4])
elements.append([78,"Pt","4","d","3/2",331.6])
elements.append([78,"Pt","4","d","5/2",314.6])
elements.append([78,"Pt","4","f","5/2",74.5])
elements.append([78,"Pt","4","f","7/2",71.2])
elements.append([78,"Pt","5","s","0",101.7])
elements.append([78,"Pt","5","p","1/2",65.3])
elements.append([78,"Pt","5","p","3/2",51.7])

elements.append([79,"Au","1","s","0",80725])
elements.append([79,"Au","2","s","0",14353])
elements.append([79,"Au","2","p","1/2",13734])
elements.append([79,"Au","2","p","3/2",11919])
elements.append([79,"Au","3","s","0",3425])
elements.append([79,"Au","3","p","1/2",3148])
elements.append([79,"Au","3","p","3/2",2743])
elements.append([79,"Au","3","d","3/2",2291])
elements.append([79,"Au","3","d","5/2",2206])
elements.append([79,"Au","4","s","0",762.1])
elements.append([79,"Au","4","p","1/2",642.7])
elements.append([79,"Au","4","p","3/2",546.3])
elements.append([79,"Au","4","d","3/2",353.2])
elements.append([79,"Au","4","d","5/2",335.1])
elements.append([79,"Au","4","f","5/2",87.6])
elements.append([79,"Au","4","f","7/2",83.9])
elements.append([79,"Au","5","s","0",107.2])
elements.append([79,"Au","5","p","1/2",74.2])
elements.append([79,"Au","5","p","3/2",57.2])

elements.append([80,"Hg","1","s","0",83102])
elements.append([80,"Hg","2","s","0",14839])
elements.append([80,"Hg","2","p","1/2",14209])
elements.append([80,"Hg","2","p","3/2",12284])
elements.append([80,"Hg","3","s","0",3562])
elements.append([80,"Hg","3","p","1/2",3279])
elements.append([80,"Hg","3","p","3/2",2847])
elements.append([80,"Hg","3","d","3/2",2385])
elements.append([80,"Hg","3","d","5/2",2295])
elements.append([80,"Hg","4","s","0",802.2])
elements.append([80,"Hg","4","p","1/2",680.2])
elements.append([80,"Hg","4","p","3/2",576.6])
elements.append([80,"Hg","4","d","3/2",378.2])
elements.append([80,"Hg","4","d","5/2",358.8])
elements.append([80,"Hg","4","f","5/2",104])
elements.append([80,"Hg","4","f","7/2",99.9])
elements.append([80,"Hg","5","s","0",127])
elements.append([80,"Hg","5","p","1/2",83.1])
elements.append([80,"Hg","5","p","3/2",64.5])
elements.append([80,"Hg","5","d","3/2",9.6])
elements.append([80,"Hg","5","d","5/2",7.8])

elements.append([81,"Tl","1","s","0",85530])
elements.append([81,"Tl","2","s","0",15347])
elements.append([81,"Tl","2","p","1/2",14698])
elements.append([81,"Tl","2","p","3/2",12658])
elements.append([81,"Tl","3","s","0",3704])
elements.append([81,"Tl","3","p","1/2",3416])
elements.append([81,"Tl","3","p","3/2",2957])
elements.append([81,"Tl","3","d","3/2",2485])
elements.append([81,"Tl","3","d","5/2",2389])
elements.append([81,"Tl","4","s","0",846.2])
elements.append([81,"Tl","4","p","1/2",720.5])
elements.append([81,"Tl","4","p","3/2",609.5])
elements.append([81,"Tl","4","d","3/2",405.7])
elements.append([81,"Tl","4","d","5/2",385])
elements.append([81,"Tl","4","f","5/2",122.2])
elements.append([81,"Tl","4","f","7/2",117.8])
elements.append([81,"Tl","5","s","0",136])
elements.append([81,"Tl","5","p","1/2",94.6])
elements.append([81,"Tl","5","p","3/2",73.5])
elements.append([81,"Tl","5","d","3/2",14.7])
elements.append([81,"Tl","5","d","5/2",12.5])

elements.append([82,"Pb","1","s","0",88005])
elements.append([82,"Pb","2","s","0",15861])
elements.append([82,"Pb","2","p","1/2",15200])
elements.append([82,"Pb","2","p","3/2",13035])
elements.append([82,"Pb","3","s","0",3851])
elements.append([82,"Pb","3","p","1/2",3554])
elements.append([82,"Pb","3","p","3/2",3066])
elements.append([82,"Pb","3","d","3/2",2586])
elements.append([82,"Pb","3","d","5/2",2484])
elements.append([82,"Pb","4","s","0",891.8])
elements.append([82,"Pb","4","p","1/2",761.9])
elements.append([82,"Pb","4","p","3/2",643.5])
elements.append([82,"Pb","4","d","3/2",434.3])
elements.append([82,"Pb","4","d","5/2",412.2])
elements.append([82,"Pb","4","f","5/2",141.7])
elements.append([82,"Pb","4","f","7/2",136.9])
elements.append([82,"Pb","5","s","0",147])
elements.append([82,"Pb","5","p","1/2",106.4])
elements.append([82,"Pb","5","p","3/2",83.3])
elements.append([82,"Pb","5","d","3/2",20.7])
elements.append([82,"Pb","5","d","5/2",18.1])

elements.append([83,"Bi","1","s","0",90526])
elements.append([83,"Bi","2","s","0",16388])
elements.append([83,"Bi","2","p","1/2",15711])
elements.append([83,"Bi","2","p","3/2",13419])
elements.append([83,"Bi","3","s","0",3999])
elements.append([83,"Bi","3","p","1/2",3696])
elements.append([83,"Bi","3","p","3/2",3177])
elements.append([83,"Bi","3","d","3/2",2688])
elements.append([83,"Bi","3","d","5/2",2580])
elements.append([83,"Bi","4","s","0",939])
elements.append([83,"Bi","4","p","1/2",805.2])
elements.append([83,"Bi","4","p","3/2",678.8])
elements.append([83,"Bi","4","d","3/2",464])
elements.append([83,"Bi","4","d","5/2",440.1])
elements.append([83,"Bi","4","f","5/2",162.3])
elements.append([83,"Bi","4","f","7/2",157])
elements.append([83,"Bi","5","s","0",159.3])
elements.append([83,"Bi","5","p","1/2",119])
elements.append([83,"Bi","5","p","3/2",92.6])
elements.append([83,"Bi","5","d","3/2",26.9])
elements.append([83,"Bi","5","d","5/2",23.8])
