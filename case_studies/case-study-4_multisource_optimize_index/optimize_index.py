"""
	In this file: a function to optimize a vegetation index 
	that takes an image as a input and returns a
	named array (implemented as a dictionary) as output. Typically 
	they are doing image-wide computation.
	Function signature is:
		def function(img, channels) -> dictionary (each value should be a scalar), or np.nan if not appliable
	
	With:
	 - img: numpy ndarray, axis are row, columns, channels
	 - channels: list of string, channel names
"""

import datetime
from scipy.optimize import minimize
import csv
import numpy as np
import pandas as pd
import pathlib
from d2r.task import Task
import os.path

class optimize_index(Task):
	def parse_config(self, config):
		"""parsing config parameters specific to this subclass"""
		res = super().parse_config(config)
		return(res)

	def _set_x0(self, nchan, logfile):
		"""
		   If logfile exists, loads the initial weights from the last row
		   from there. Otherwise picks (2*nchan+2) random weights
		"""		
		x0 = None
		if os.path.isfile(logfile):
			#loading the values from the last run
			with open(logfile, newline='') as csvfile:
				re = csv.reader(csvfile)
				for row in re:
					#each row contains: timestamp, correlation, <parameters>
					#we just need to remove the first two elements
					x0 = row[2:]
			print('Loaded x0 from previous run')
		else:
			#no previous file existing, we set x0 at a random point
			print('Random x0')
			x0 = np.random.normal(0, 1, 2*nchan + 2)
		
		#done
		return(x0)
	
	def run(self, dataset):
		#making sure the output subfolder do exists
		path = pathlib.Path(self.config['outfolder'], dataset.get_title())
		path.mkdir(parents=True, exist_ok=True)
		
		outfile = str(path) + '/' + self.config['outfile']
		print('we are saving here:' + outfile)
		
		#let's optimize the index, in the form:
		#
		#  linear_combination(channels) + constant
		#  -----------------------------------------------
		#  another_linear_combination(channels) + constant
		
		#Starting point:
		ch = dataset.get_channels()
		x0 = self._set_x0(len(ch), outfile)

		#names, interface
		weight_names = ['num_' + s for s in ch] + ['num_const']  + ['den_' + s for s in ch] + ['den_const'] 
		print(dict(zip(weight_names, x0)))
		
		#initializing the log, if needed
		if not os.path.isfile(outfile):
			new_row = {'time' : None, 'correlation' : None}
			for i in range(len(weight_names)):
				new_row[weight_names[i]] = None
			with open(outfile, "w", newline="") as f:
				w = csv.DictWriter(f, new_row.keys())
				w.writeheader()

		#reading target phenos, it should contain two columns, named
		# - self.config['id_col']   (e.g. "gid")
		# - self.config['target_col'] (e.g. "lodging")
		true_phenos = pd.read_csv(self.config['phenofile'])
		
		#packing all the extra config in a single global dict. We
		#could pass it to the evaluation function via the args parameter,
		#but we still need to use it as a global variable for the callback
		#function, so...
		global extraconf
		extraconf = {
			'dataset' : dataset,
			'id_col'  : self.config['id_col'],
			'target_col' : self.config['target_col'], 
			'phenotypes' : true_phenos,
			'outfile' : outfile
		}
		
		#ready to optimize
		res = minimize(compute_index, x0, method = 'Nelder-Mead', callback = mycallback)
		
		#finished, final interface		
		print(res)
		print('iterations: ' + str(res.nit))
		print('evaluations: ' + str(res.nfev))

def mycallback(xk):
	"""
		callback function to store optimization progress. Depending on
		the python/scipy version this functioun could receive a more 
		advanced intermediate_result:OptimizeResult object. In this 
		implementation it receives only the current solution xt.
		Moreover, to actually obtain the current function value we need
		to evaluate again.
		This function need access to the global	variable "extraconf" for
		all the params needed for evaluation and saving
	"""
	#a bit of interface
	print('invoked mycallback')
	
	#local pointers for easier syntax
	dataset = extraconf['dataset']
	id_col = extraconf['id_col']
	target_col = extraconf['target_col']
	phenotypes = extraconf['phenotypes']
	outfile = extraconf['outfile']
	
	#evaluating the funcion at the current solution
	sol = compute_index(xk)
	
	#taking notes
	new_row = {
		'time' : str(datetime.datetime.now()), 
		'correlation' : -sol #saving the actual correlation, not it's negative
	}
	for i in range(len(xk)):
		new_row['param_' + str(i)] = xk[i]

	with open(outfile, "a", newline="") as f:
		w = csv.DictWriter(f, new_row.keys())
		w.writerow(new_row)

def compute_index(current_weights):
	#a bit of interface
	print(' - invoked compute_index')
	
	#local pointers for easier syntax
	dataset = extraconf['dataset']
	id_col = extraconf['id_col']
	target_col = extraconf['target_col']
	phenotypes = extraconf['phenotypes']
	
	#the field that is used to index geometries in the shape file
	fields = dataset.get_geom_index()
	geometry_columns = dataset.get_geom_field(fields)
	
	#the channel list, lenght
	channels = dataset.get_channels()
	nchan = len(channels)
	
	#separating the weights by use. They are: 
	#    <channels> + const
	#   --------------------
	#    <channels> + const
	#and packed as:
	# [[num coeffs], num_const, [den_coeffs], den_const]
	num_coeff  = current_weights[:nchan]
	num_const = current_weights[nchan]
	den_coeff  = current_weights[(nchan+1):(2*nchan+1)]
	den_const = current_weights[2*nchan+1]

	#room for results
	res = {}
	
	#for each shape in the dataset
	for i in range(len(geometry_columns)): #this could be parallelized
		#selecting the current geometry
		cg = geometry_columns.iloc[i,:]
		d = {key : cg[key] for key in fields}

		#a raster block
		rb = dataset.get_geom_raster(d, normalize_if_possible=True)
		
		#computing the index: (numerator + const) / (denominator + const)
		numerator   = num_coeff[None, None, :] * rb 
		denumerator = den_coeff[None, None, :] * rb 
		numerator   = np.sum(numerator, axis = 2) + num_const
		denumerator = np.sum(denumerator, axis = 2) + den_const
		myindex = numerator / denumerator

		#extracting the mean by plot, storing
		res[cg[id_col]] = np.ma.mean(myindex)

	#ensuring the correct order
	desired_order = phenotypes[id_col].apply(str)
	ordered_values = [res[k] for k in desired_order]
	
	#computing correlation, penalized for big absolute values
	final_cor = np.corrcoef(ordered_values, phenotypes[target_col])[0,1]

	#done: we minimize negative correlation
	return -final_cor  

