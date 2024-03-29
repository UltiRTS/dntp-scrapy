from multiprocessing.sharedctypes import Value
from PIL import Image
import ctypes
import os
from difflib import SequenceMatcher


class UnitSync:
	def __init__(self, startdir,libunitsync_path,username='unknown'):
		self.so = ctypes.CDLL(libunitsync_path)
		self.init = self.so.Init(0, 0)
		self.write_dir = self.so.GetWritableDataDirectory()
		self.username=username
		self.startdir=startdir
		os.chdir(self.startdir)
		# Some Dynamic functions
		self._getMapCount = self.so.GetMapCount
		self._getMapName = self.so.GetMapName
		self._getMapFileName = self.so.GetMapFileName
		self._getMapArchiveName = self.so.GetMapArchiveName
		self._getMinimap = self.so.GetMinimap
		# output settings
		self._getMapCount.restype = ctypes.c_int
		self._getMapName.restype = ctypes.c_char_p
		self._getMapFileName.restype = ctypes.c_char_p
		self._getMapArchiveName.restype = ctypes.c_char_p

		self.mapNames = []

	def reinit(self):
		self.init = self.so.Init(0, 0)
		


	def mapList(self):
		mapList = []
		mapCount = self._getMapCount()
		for i in range(mapCount):
			mapList.append(self._getMapName(i).decode('utf8'))
		os.chdir(self.startdir)

		self.mapNames = mapList

		return mapList

	def _getImg(self, mapname, reduction=0):
		width = height = 1024 // 2**reduction
		self._getMinimap.restype = ctypes.POINTER(ctypes.c_ubyte * (width * height * 2))
		try:
			minimapData = self._getMinimap(mapname.encode('utf8'), reduction).contents
			mapname.replace(' ', '_')
			img = Image.frombytes('RGB', (width, height), minimapData, 'raw', 'BGR;16' )

			return img
		except ValueError:
			img = Image.new('RGB', (width, height), (0, 0, 0))
			return img
		
#		have, need = len(minimapData), width*height*2
#		print(have, need)
#		if have < need:
#			print("No much data fixing.")
#			emptyFix = bytes(need-have)
#			minimapData += emptyFix


	def storeMinimap(self, mapname):
		minimapStorePath = os.path.join('/tmp', mapname + '.png')
		img = self._getImg(mapname, 0)
		for reduction in range(0,9):
			try:
				img = self._getImg(mapname, reduction)
				break
			except:
				#print(colored("ERROR", 'red'), "No much data reduce width and height.")
				pass

		img.save(minimapStorePath)
		return minimapStorePath
		
		
	def getMapName(self):
		self._getMapCount()
		#print('totalmap count '+ str())
		return self._getMapName(0).decode('utf8')



if __name__ == '__main__':
	cur = os.getcwd()
	print(cur + '/engine/libunitsync.so')
	us = UnitSync(cur,cur + '/engine/libunitsync.so')

	import os
	import requests

	testMapUrl = 'https://springfiles.springrts.com/files/maps/supercoreprimecorridor-v1.5.sd7'
	resp = requests.get(testMapUrl)
	with open(os.path.join(cur, 'engine/maps', 'supercoreprimecorridor-v1.5.sd7'), 'wb') as f:
		f.write(resp.content)
	
	us.reinit()
	mapname = us.getMapName()
	us.storeMinimap(mapname)
