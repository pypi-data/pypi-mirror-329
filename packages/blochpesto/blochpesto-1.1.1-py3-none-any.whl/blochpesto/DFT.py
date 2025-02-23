import blochpesto as pesto
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import os


def quickPlot(spectrum,**kwargs):
	defaultKwargs = {'spinProjection':None,'axis':None,'filled':True,'lw':None,'alpha':None,'color':None,
	'kPath':None,'drawHighSymmetryLabels':None,'bandIndicesToPlot':None}
	kwargs = { **defaultKwargs, **kwargs }	


	if kwargs['filled']==None: kwargs['filled']=True
	if kwargs['lw']==None: kwargs['lw']=1
	if kwargs['alpha']==None: kwargs['alpha']=1
	if kwargs['drawHighSymmetryLabels']==None: kwargs['drawHighSymmetryLabels']=False
	if kwargs['drawHighSymmetryLabels']==True and kwargs['kPath']==None:
		kwargs['drawHighSymmetryLabels']=False
	if kwargs['color']==None: kwargs['color']='lightsteelblue'

	numBands=np.shape(spectrum['data'])[0]

	if 'isProjectedBulkBands' in spectrum['Metadata']:

		Ef = spectrum['Metadata']['Ef']
		nkpnts=spectrum['Metadata']['nkpnts']
		if kwargs['axis']==None: fig,ax=matplotlib.pyplot.subplots(figsize=(7,5))
		else: ax = kwargs['axis']

		if kwargs['kPath']==None:
			kAxis=spectrum['Axis']
		else:
			kPath = kwargs['kPath']
			k,kAxis=0,[]

			for ii,segment in enumerate(kPath):
				if ii==len(kPath)-1: 
					endpoint,num=True,nkpnts+1
				else: endpoint,num=False,nkpnts

				if ii>0:
					for kpoint in np.linspace(start=kPath[ii-1][1],stop=kPath[ii][1],num=num,endpoint=endpoint):
						kAxis.append(kpoint)	

		

		if kwargs['filled']==False:
			for bandIndex in range(numBands): 
				for kzIndex in range(np.shape(spectrum['data'])[1]): 
					ax.plot(kAxis,spectrum['data'][bandIndex][kzIndex],color=kwargs['color'],alpha=kwargs['alpha'])

		if kwargs['filled']==True:
			# At each kparr value, there are (kz_pt) number of evals for each band
			# We are trying to trace out the 'envelope' of the bulk band projection by finding
			# the minimum and maximum eval at each kparr, for each band

			num_kz_points = np.shape(spectrum['data'])[1]
			for bandIndex in range(numBands): 
				solidUpper =[]
				solidLower =[]
				
				for kindex,kval in enumerate(spectrum['Axis']):
					eBs =[spectrum['data'][bandIndex][kzIndex][kindex] for kzIndex in range(num_kz_points)]
					solidUpper.append(((max(eBs))))
					solidLower.append(((min(eBs))))

				ax.fill_between(kAxis, solidUpper, solidLower,color=kwargs['color'],alpha=kwargs['alpha'])

		if kwargs['drawHighSymmetryLabels']==True:
			pesto.drawHighSymmetryLabels(points=kPath,axis=ax)

		ax.set_xlim([kAxis[0],kAxis[-1]])  

		
	else:

		nkpnts=spectrum['Metadata']['nkpnts']

		if kwargs['axis']==None: fig,ax=matplotlib.pyplot.subplots(figsize=(7,5))
		else: ax = kwargs['axis']

		if kwargs['kPath']==None:
			#print(spectrum['Axis'])
			kAxis=spectrum['Axis']
		else:
			kPath = kwargs['kPath']
			k,kAxis=0,[]

			for ii,segment in enumerate(kPath):
				if ii==len(kPath)-1: 
					endpoint,num=True,nkpnts+1
				else: endpoint,num=False,nkpnts

				if ii>0:
					for kpoint in np.linspace(start=kPath[ii-1][1],stop=kPath[ii][1],num=num,endpoint=endpoint):
						kAxis.append(kpoint)	

		for ii,band in enumerate(spectrum['data']):
			if kwargs['bandIndicesToPlot']!=None and not (ii in kwargs['bandIndicesToPlot']):
				pass
			else:
				ax.plot(kAxis,band,color=kwargs['color'],alpha=kwargs['alpha'])

		if kwargs.get('drawHighSymmetryLabels'):
			pesto.drawHighSymmetryLabels(points=kPath,axis=ax)

		ax.set_xlim([kAxis[0],kAxis[-1]])  

		if kwargs['spinProjection'] in [0,1,2]:
			for ii,band in enumerate(spectrum['data']):
				if kwargs['bandIndicesToPlot']!=None and not (ii in kwargs['bandIndicesToPlot']):
					pass
				else:
					spinvals = spectrum['spinProjection'][kwargs['spinProjection']][ii]
					ax.scatter(kAxis,band,c=spinvals, s=abs(spinvals*500),cmap='bwr',alpha=kwargs['alpha'],vmin=-0.5,vmax=0.5)


def loadProjectedBulkBands(folderPath,bandsOutputPrefix="",scfOutputFileName="scf.out",nscfInputFileName="bands.in",nscfOutputFileName="bands.out",invertEnergyAxis=False,beQuiet=False):
	

	loadedSpectrum={}
	loadedSpectrum['Metadata']={}
	loadedSpectrum['Metadata']['isDFT']=True
	loadedSpectrum['Metadata']['isProjectedBulkBands']=True

	loadedSpectrum['Axis']=[]
	loadedSpectrum['AxisLabel']=["",""]
	loadedSpectrum['AxisUnits']=["",""]
	loadedSpectrum['data']=[]

	Ef=0

	nscfInputFilePath=folderPath+"/"+nscfInputFileName
	try:
		with open(nscfInputFilePath,'r') as f:	
			inputFile=f.readlines()

			card="control"
			for line in inputFile:
				if line.startswith("&SYSTEM"): 
					card="system"
					loadedSpectrum['Metadata']['&SYSTEM']={}
				if line.startswith("&ELECTRONS"): 
					card="electrons"
					loadedSpectrum['Metadata']['&ELECTRONS']={}
				if line.startswith("ATOMIC_SPECIES"): 
					card="atomic_species"
					loadedSpectrum['Metadata']['ATOMIC_SPECIES']={}
				if line.startswith("ATOMIC_POSITIONS"): 
					card="atomic_positions"
					loadedSpectrum['Metadata']['ATOMIC_POSITIONS']={}
				if line.startswith("K_POINTS"): 
					card="kpoints"
					loadedSpectrum['Metadata']['K_POINTS']={}

				if card=="system":
					data=line.split()
					# sometimes exponentials are missing the 'e', which breaks pythons float conversion (e.g. 1.322+02 instead of 1.322e+02)
					# This inserts missing 'e's in exponential numbers
					if len(data)>1 and not 'e' in data[-1] and '+' in data[-1]:
						substrings=data[-1].split('+')
						data[-1]=substrings[0]+'e'+substrings[1]

					if len(data)>1:
						if data[0]=="a": loadedSpectrum['Metadata']['&SYSTEM']['a']=float(data[-1])
						if data[0]=="c": loadedSpectrum['Metadata']['&SYSTEM']['c']=float(data[-1])
						if data[0]=="ibrav": loadedSpectrum['Metadata']['&SYSTEM']['ibrav']=float(data[-1])
						if data[0]=="degauss": loadedSpectrum['Metadata']['&SYSTEM']['degauss']=float(data[-1])
						if data[0]=="eutrho": loadedSpectrum['Metadata']['&SYSTEM']['ecutrho']=float(data[-1])
						if data[0]=="ecutwfc": loadedSpectrum['Metadata']['&SYSTEM']['ecutwfc']=float(data[-1])
						if data[0]=="nat": loadedSpectrum['Metadata']['&SYSTEM']['nat']=float(data[-1])
						if data[0]=="ntyp": loadedSpectrum['Metadata']['&SYSTEM']['ntyp']=float(data[-1])
						if data[0]=="occupations": loadedSpectrum['Metadata']['&SYSTEM']['']=data[-1]
						if data[0]=="smearing": loadedSpectrum['Metadata']['&SYSTEM']['']=data[-1]
				
				if card=="kpoints":
					data=line.split()
					if len(data)>3:
						loadedSpectrum['Metadata']['nkpnts']=int(data[-1])
	except FileNotFoundError:
		print("Could not find the nscf input file (guessed location was {})".format(nscfInputFilePath))
		return

	nscfOutputFilePath=folderPath+"/"+nscfOutputFileName
	try:
		with open(nscfOutputFilePath,'r') as f:	
			outputFile=f.readlines()
			loadedSpectrum['Metadata']['StartTime']=outputFile[1].split("starts on ")[-1]
			if beQuiet==False: print("Calculation performed: ",loadedSpectrum['Metadata']['StartTime'])
	except FileNotFoundError:
		print("Could not find the nscf output file (guessed location was {})".format(nscfInputFilePath))

	scfFilePath=folderPath+"/"+scfOutputFileName
	try:
		with open(scfFilePath,'r') as f:	
			scfFile=f.readlines()
			for line in scfFile:
				if line.startswith("     the Fermi energy is"):
					temp = line.split("     the Fermi energy is")[1].lstrip("  ")
					Ef = float(temp.split(" ")[0])
					loadedSpectrum['Metadata']['Ef']=Ef
	except FileNotFoundError:
		print("Could not find the scf output file (guessed location was {})".format(bandInputFilePath))
		return


	numBands=0
	num_kz_points = len([name for name in os.listdir(folderPath) if name.endswith(".out.gnu")])
	with open(folderPath+"/"+bandsOutputPrefix+"00.out.gnu",'r') as f:
		for line in f:
			vals=line.rstrip('\n').lstrip(' ').split("  ")
			if len(vals)==1: numBands+=1

	for bandIndex in range(numBands):
		loadedSpectrum['data'].append([])
		for index in range(num_kz_points):
			loadedSpectrum['data'][-1].append([]) 


	for kz in range(num_kz_points):
		with open(folderPath+"/"+bandsOutputPrefix+"{:02d}.out.gnu".format(kz),'r') as f:
			# Format is (k,E), chunked per band. Bands are separated by lines with no entries
			bandIndex=0
			evals,kvals=[],[]
			for line in f:
				vals=line.rstrip('\n').lstrip(' ').split("  ")
				if len(vals)>1: 
					kvals.append(float(vals[0]))
					evals.append(float(vals[-1]))
				elif len(vals)==1: #End of this band
					if invertEnergyAxis==True: loadedSpectrum['data'][bandIndex][kz]=[-(ii-Ef) for ii in evals]
					else: loadedSpectrum['data'][bandIndex][kz]=[(ii-Ef) for ii in evals]

					loadedSpectrum['Axis']=kvals
					evals,kvals=[],[]
					bandIndex+=1

	

	return loadedSpectrum






def loadBands(folderPath,bandsOutputFileName="bandstructure.out.gnu",nscfInputFileName="bands.in",nscfOutputFileName="bands.out",scfOutputFileName="scf.out",invertEnergyAxis=False,beQuiet=False):
	loadedSpectrum={}
	loadedSpectrum['Metadata']={}
	loadedSpectrum['Metadata']['isDFT']=True

	loadedSpectrum['Axis']=[]
	loadedSpectrum['AxisLabel']=["",""]
	loadedSpectrum['AxisUnits']=["",""]
	loadedSpectrum['data']=[]

	Ef = 0

	nscfInputFilePath=folderPath+"/"+nscfInputFileName
	try:
		if beQuiet==False: print("loading {} to find calculation parameters:".format(nscfInputFileName))
		with open(nscfInputFilePath,'r') as f:	
			inputFile=f.readlines()

			card="control"
			for line in inputFile:
				if line.startswith("&SYSTEM"): 
					card="system"
					loadedSpectrum['Metadata']['&SYSTEM']={}
				if line.startswith("&ELECTRONS"): 
					card="electrons"
					loadedSpectrum['Metadata']['&ELECTRONS']={}
				if line.startswith("ATOMIC_SPECIES"): 
					card="atomic_species"
					loadedSpectrum['Metadata']['ATOMIC_SPECIES']={}
				if line.startswith("ATOMIC_POSITIONS"): 
					card="atomic_positions"
					loadedSpectrum['Metadata']['ATOMIC_POSITIONS']=[]
				if line.startswith("K_POINTS"): 
					card="kpoints"
					loadedSpectrum['Metadata']['K_POINTS']={}

				if card=="system":
					data=line.split()
					# sometimes exponentials are missing the 'e', which breaks pythons float conversion (e.g. 1.322+02 instead of 1.322e+02)
					# This inserts missing 'e's in exponential numbers
					if len(data)>1 and not 'e' in data[-1] and '+' in data[-1]:
						substrings=data[-1].split('+')
						data[-1]=substrings[0]+'e'+substrings[1]
					if len(data)>1:
						if data[0]=="a": loadedSpectrum['Metadata']['&SYSTEM']['a']=float(data[-1])
						if data[0]=="c": loadedSpectrum['Metadata']['&SYSTEM']['c']=float(data[-1])
						if data[0]=="ibrav": loadedSpectrum['Metadata']['&SYSTEM']['ibrav']=float(data[-1])
						if data[0]=="degauss": loadedSpectrum['Metadata']['&SYSTEM']['degauss']=float(data[-1])
						if data[0]=="eutrho": loadedSpectrum['Metadata']['&SYSTEM']['ecutrho']=float(data[-1])
						if data[0]=="ecutwfc": loadedSpectrum['Metadata']['&SYSTEM']['ecutwfc']=float(data[-1])
						if data[0]=="nat": loadedSpectrum['Metadata']['&SYSTEM']['nat']=float(data[-1])
						if data[0]=="ntyp": loadedSpectrum['Metadata']['&SYSTEM']['ntyp']=float(data[-1])
						if data[0]=="occupations": loadedSpectrum['Metadata']['&SYSTEM']['']=data[-1]
						if data[0]=="smearing": loadedSpectrum['Metadata']['&SYSTEM']['']=data[-1]
				
				if card=="kpoints":
					data=line.split()
					if len(data)>3:
						loadedSpectrum['Metadata']['nkpnts']=int(data[3])

				if card=="atomic_positions":
					loadedSpectrum['Metadata']['ATOMIC_POSITIONS'].append(line.rstrip("\n"))
					if beQuiet==False:
						print(line.rstrip("\n"))

	except FileNotFoundError:
		print("Could not find the nscf input file (guessed location was {})".format(nscfInputFileName))
		return

	nscfOutputFilePath=folderPath+"/"+nscfOutputFileName
	try:
		if beQuiet==False: print("loading {} to find calculation date:".format(nscfOutputFileName))
		with open(nscfOutputFilePath,'r') as f:	
			nscfOutputFile=f.readlines()
			loadedSpectrum['Metadata']['StartTime']=nscfOutputFile[1].split("starts on ")[-1]
			if beQuiet==False: print("Calculation performed: ",loadedSpectrum['Metadata']['StartTime'])
	except FileNotFoundError:
		print("Could not find the nscf output file (guessed location was {}). \nThis is not critical, and only results in the loss of some trivial metadata".format(nscfInputFilePath))

	scfOutputFilePath=folderPath+"/"+scfOutputFileName
	try:
		if beQuiet==False: print("loading {} to find Fermi energy:".format(scfOutputFileName))
		with open(scfOutputFilePath,'r') as f:	
			scfFile=f.readlines()
			for line in scfFile:
				if line.startswith("     the Fermi energy is"):
					temp = line.split("     the Fermi energy is")[1].lstrip("  ")
					Ef = float(temp.split(" ")[0])
					loadedSpectrum['Metadata']['Ef']=Ef	
	except FileNotFoundError:
		print("Could not find the scf output file (guessed location was {})".format(scfOutputFilePath))
		return

	bandsOutputFilePath =folderPath+"/"+bandsOutputFileName

	numBands=0
	try:
		if beQuiet==False: print("loading {} to get evals:".format(bandsOutputFileName))
		with open(bandsOutputFilePath,'r') as f:
			data = f.readlines()

			for line in data:
				vals=line.rstrip('\n').lstrip(' ').split("  ")
				if len(vals)==1:
					numBands+=1

			evals,kvals=[],[]
			for line in data:

				vals=line.rstrip('\n').lstrip(' ').split("  ")
				if len(vals)<2: #If you've finished this band and are about to start on a new one (band eigenvalues are separated by empty lines)
					if invertEnergyAxis==True: loadedSpectrum['data'].append([-(ii-Ef) for ii in evals])
					else: loadedSpectrum['data'].append([(ii-Ef) for ii in evals])
					loadedSpectrum['Axis']=kvals
					evals,kvals=[],[]
				else:
					evals.append(float(vals[-1]))
					kvals.append(float(vals[0]))
	except FileNotFoundError:
		print("Could not find the bandstructure output file (guessed location was {})".format(bandsOutputFilePath))
		return

	loadedSpectrum['AxisLabel'][0]="Energy"
	loadedSpectrum['AxisLabel'][0]="k"
	loadedSpectrum['AxisUnits'][0]="eV"
	loadedSpectrum['AxisUnits'][1]="??"


	try:
		numBands = np.shape(loadedSpectrum['data'])[0]
		numkpnts = np.shape(loadedSpectrum['data'])[1]

		spin=[]
		for spinIndex in [1,2,3]:
			guessed_filePath=bandsOutputFilePath.replace(".gnu",".{}".format(spinIndex))
			if beQuiet==False: print("Attempting to load spin information from ",guessed_filePath)

			with open(guessed_filePath) as f: 
				print("opened it OK")
				spinFile = f.readlines()
			spin.append(np.zeros([numBands,numkpnts]))	

			readingkval=False
			data=[]
			kIndex=-1

			# The layout of these output files is:
			# (3 element k point)
			# A bloch of n rows * 10 columns, where every entry is the spin projection on that band at that kpoint
			for line in spinFile[1:]:
				#print(line)
				if len(line.split())==3: #We've reached a new kpoint. Save our data from the last kpoint if we have any
					readingkval=True
					if len(data)>0:
						#print("Saving data to array position",spinIndex-1)
						for bandIndex,datapoint in enumerate(data):
							spin[spinIndex-1][bandIndex,kIndex]=datapoint
						data=[]
					kIndex=kIndex+1
					
				elif readingkval==True: #We're still recording data from the current k-point
					lineVals=line.split()
					[data.append(float(ii)) for ii in line.split()]

		loadedSpectrum['spinProjection']=spin		
	except:
		pass

	return loadedSpectrum
