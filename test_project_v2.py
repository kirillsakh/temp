import rasterio
import numpy as np
import json
import pandas as pd


def main():

	'''to load Json'''
	json_file = 'class_description.json'
	class_labels = load_description(json_file)

	'''just to see what it looks like'''
	print('\nclass_description.json\n')
	[print('{}   {}'.format(i, k)) for i, k in
	                 zip(class_labels.label_ids, class_labels.label_colors)]

	'''to load ~landcover.tif'''
	tiff_file = 'benatky-nad-jizerou-landcover.tif'
	landcover = load_rasterio(tiff_file)
	
	'''to check dimensions'''
	landcover.shape

	'''to calculate number of pixels per each Class label'''
	unique, counts = np.unique(landcover[:,:,0], return_counts=True)
	pixels_per_class = dict(zip(unique,counts))

	'''to create DataFrame with Class labels and RGB_code'''
	legend = ['Class labels', 'RGB_code']
	df = pd.DataFrame([[label, rgb_code] for (label, rgb_code) in
	                  zip(class_labels.label_ids, class_labels.label_colors)],
	                  columns=legend)

	'''to create Series with Pixels per Class'''
	s = pd.Series(pixels_per_class)

	'''to merge'''
	df = df.join(s.to_frame(name='Pixels per Class'))

	'''to check data types'''
	df.dtypes

	'''to convert to Int'''
	df['Pixels per Class'] = df['Pixels per Class'].fillna(0).astype(int)

	'''to compare number of pixels in DataFrame with loaded file'''
	print('\nPixels in Landcover: {}\n\nPixels in DataFrame: {}\n'
		.format(landcover.shape[0]*landcover.shape[1], df['Pixels per Class'].sum()))

	'''to select Pixels per Class "vehicle"'''
	pixs_per_vehicle = int(df['Pixels per Class'].loc[df['Class labels'] == 'vehicle'])
	print('Num of pixels per Class "vehicle": {}\n'.format(pixs_per_vehicle))

	'''to calculate area of a pixel in m^2'''
	pix_area = get_pixel_square_area(tiff_file)
	print('Area of a pixel in m^2: {}\n'.format(pix_area))

	'''to calculate approximate vehicle size in m^2'''
	# http://www.skoda-auto.cz/modely/octavia/octavia/octavia-rozmery
	octavia_length = 4.670 
	octavia_width = 1.814
	octavia_area = octavia_length * octavia_width
	print('Approximate area of a vehicle in m^2: {}\n'.format(octavia_area))

	'''to calculate approximate number of vehicles'''
	number_of_vehicles = int((pixs_per_vehicle * pix_area) / octavia_area)
	print('Approximate number of vehicles: {}\n'.format(number_of_vehicles))

# df = pd.DataFrame([[label, rgb_code] for (label, rgb_code) in zip(class_labels.label_ids, class_labels.label_colors)], columns=legend)

def load_rasterio(file_path, window=None):

	with rasterio.open(file_path, 'r') as r:
		return np.transpose(r.read(window=window), axes=[1, 2, 0])


class Description:

	def __init__(self, settings):
		self.label_ids = settings['label_ids']
		self.label_colors = settings['label_colors']
		self.nb_labels = len(self.label_ids)

		if self.nb_labels != len(self.label_colors):
			print("Wrong number of label colors.")


def load_description(file_path):

	with open(file_path) as description_file:
		description_dict = json.load(description_file)
		description = Description(description_dict)
		return description

def get_pixel_square_area(file_path):
	'''calculates area of a pixel in m^2'''
	with rasterio.open(file_path, 'r') as raster:
		geo_transform = raster.transform
		pixelSizeX = geo_transform[0]
		pixelSizeY = -geo_transform[4]
		return pixelSizeX * pixelSizeY



if __name__ == '__main__':
	main()