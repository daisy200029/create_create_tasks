import sys
from PIL import Image
import os

class photo_merge():
	def __init__(self,file_path=os.path.join(os.environ["HOME"], "Desktop/"),photoNames=[],output='OUT.PNG'):
		self.photoNames=photoNames
		self.file_path=file_path
		self.output=output
		self.create_path_names()
		self.merge_photo()
		self.check_file_exist()

	def create_path_names(self):
		print self.photoNames
		self.path_names=[self.file_path+photo for photo in self.photoNames]

	def merge_photo(self):
		images = map(Image.open, self.path_names)
		widths, heights = zip(*(i.size for i in images))
		total_width = sum(widths)
		max_height = max(heights)
		new_im = Image.new('RGB', (total_width, max_height))
		x_offset = 0
		for im in images:
			new_im.paste(im, (x_offset,0))
			x_offset += im.size[0]
		self.new_im=new_im

	def check_file_exist(self):
		outputfile=self.file_path+self.output
		if (os.path.isfile(outputfile)):
			number=1;
			name,filetype=self.output.split('.')
			print name+" + "+filetype
			while (os.path.isfile(self.file_path+name+'-'+str(number)+'.'+filetype)):
				number=number+1
			self.final_photo=self.file_path+name+'-'+str(number)+'.'+filetype
			self.new_im.save(self.final_photo)
			print "success get new naming merged photo"+self.final_photo
		else:
			self.final_photo=outputfile
			self.new_im.save(self.final_photo)
			print "success get merged photo"+self.final_photo

if __name__ == "__main__":
	photo_merge(photoNames=['TEST1.PNG','TEST3.PNG'])
