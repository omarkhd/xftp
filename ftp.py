# -*- encoding: UTF-8 -*-
from ftplib import FTP as _FTP
from os.path import basename

class FTP(_FTP):

	def ls(self, dirname = '.'):
		listing = []
		for filename in self.nlst('-a', dirname):
			if basename(filename) not in ('.', '..'):
				listing.append(filename)
		return listing
		

	def lsdirs(self, dirname = '.'):
		dirs = []
		for filename in self.ls(dirname):
			if self.isdir(filename):
				dirs.append(filename)
		return dirs
	
	def lsfiles(self, dirname = '.'):
		return list(set(self.ls(dirname)) - set(self.lsdirs(dirname)))

	def isdir(self, filename):
		try:
			current = self.pwd()
			self.cwd(filename)
			self.cwd(current)
			return True
		except:
			return False

	def lsr(self, dirname = '.', recursive_list = []):
		for entry in self.lsdirs(dirname):
			recursive_list.append(entry)
			self.lsr(entry, recursive_list)
		for entry in self.lsfiles(dirname):
			recursive_list.append(entry)
		return recursive_list

	def rmr(self, filename = '.', not_deleted = []):
		if(self.isdir(filename)):
			for nodename in self.ls(filename):
				self.rmr(nodename, not_deleted)
			self.rmdir(filename)
		else:
			self.rm(filename)
		return not_deleted

	def lsrtype(self, dirname = '.', lstype = None):
		if lstype == None:
			return self.lsr(dirname)
		if lstype not in ('FILE', 'DIR'):
			raise Exception('types: FILE|DIR')
		ls_rec = []
		for filename in self.lsr(dirname):
			isdir = self.isdir(filename)
			if isdir and lstype == 'DIR':
				ls_rec.append(filename)
			if not isdir and lstype == 'FILE':
				ls_rec.append(filename)
		return ls_rec

	def lsrdirs(self, dirname = '.'):
		return self.lsrtype(dirname, 'DIR')

	def lsrfiles(self, dirname = '.'):
		return self.lsrtype(dirname, 'FILE')
			
	def count(self, dirname = '.'):
		return len(self.lsr(dirname))

	def rm(self, filename):
		try:
			self.delete(filename)
			return True
		except:
			return False

	def rmdir(self, dirname):
		try:
			self.rmd(dirname)
			return True
		except:
			return False
