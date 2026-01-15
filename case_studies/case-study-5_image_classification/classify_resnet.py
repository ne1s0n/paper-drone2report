from d2r.task import Task
import d2r.misc
import tensorflow as tf
import numpy as np
import pprint
import csv 
import os

class classify_resnet(Task):
	def _prepare_image(self, dataset):
		"""prepare the image for the neural network"""
		img = dataset.get_raster_data(
			selected_channels = dataset.get_channels(), 
			output_width = self.config['input_size_width'],
			output_height = self.config['input_size_height'], 
			rescale_to_255=False,
			normalize_if_possible=False
		)
		
		#standard preprocessing for resnet
		img = tf.keras.applications.resnet.preprocess_input(img)

		#add batch dimension
		img = np.expand_dims(img, axis=0)  # (1, H, W, 3)
		
		#done
		return img 
	
	def run(self, dataset):
		"""Load the deep learning model and applies it to the current image"""
		
		#should we load the model? It's time consuming so we do it only once
		if not hasattr(self, 'model'):
			print(' - loading the model')
			self.model = tf.keras.models.load_model(self.config['model'])
		
		#load one image
		img = self._prepare_image(dataset)
		
		#predict
		pred = self.model.predict(img)

		#extract printable values
		predicted_class = np.argmax(pred, axis=1)[0]
		confidence = np.max(pred)
		
		#collecting the results in a dict
		(ortho, shapes) = dataset.get_files()
		res = {}
		res['image_file'] = ' '.join(ortho)
		res['predicted_class_number'] = predicted_class
		res['predicted_class_label']  = self.config['labels'][predicted_class]
		res['confidence']              = confidence
		res['raw_predictions']        = pred
		
		#saving to file, new or appending
		os.makedirs(os.path.dirname(self.config['outfile']), exist_ok=True)
		newfile = not os.path.isfile(self.config['outfile'])
		with open(self.config['outfile'], 'a', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=res.keys())
			if newfile:
				writer.writeheader()
			writer.writerow(res)
		
		#interface, if required
		if self.config['verbose']:
			pprint.pp(res)

	def parse_config(self, config):
		"""parsing config parameters specific to this subclass"""
		res = super().parse_config(config)
		
		for key in res:
			#input size should be integers
			if key in ['input_size_width', 'input_size_height']:
				res[key] = int(res[key])
			if key == 'labels':
				res[key] = d2r.misc.parse_python(res[key])

		return(res)
