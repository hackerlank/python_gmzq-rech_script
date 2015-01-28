#!/usr/bin/python

import sys, time, re, ConfigParser

class Datetime:
	
	datetimeFormat = []
	datetimePattern = []

	def __init__(self):
		self.datetimeFormat.append("%Y-%m-%d")
		self.datetimePattern.append(re.compile(r"^[1-9]{1}[0-9]{3}-[0-9]{1,2}-[0-9]{1,2}$"))
		
		self.datetimeFormat.append("%Y%m%d")
		self.datetimePattern.append(re.compile(r"^[1-9]{1}[0-9]{3}[0-9]{2}[0-9]{2}$"))
		
		self.datetimeFormat.append("%Y-%m-%d %H:%M:%S")
		self.datetimePattern.append(re.compile(r"^[1-9]{1}[0-9]{3}-[0-9]{1,2}-[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}$"))
		
		self.datetimeFormat.append("%Y%m%d %H:%M:%S")
		self.datetimePattern.append(re.compile(r"^[1-9]{1}[0-9]{3}[0-9]{2}-[0-9]{2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}$"))
		
	
	def str2ts(self, string, fmt = '%Y-%m-%d'):
		timeArray = time.strptime(string, fmt)
		return int(time.mktime(timeArray))
		
	def ts2str(self, ts, fmt = '%Y-%m-%d %H:%M:%S'):
		timeArray = time.localtime(ts)
		return time.strftime(fmt, timeArray)
		
	def autoStr2ts(self, string):
		genFormat = self.__selectFormat(string)
		if (genFormat):
			timeArray = time.strptime(string, genFormat)
			return int(time.mktime(timeArray))
		else:
			return False

	def autoStrReformat(self, string, formatOld2New = '%Y_%m_%d'):
		genFormat = self.__selectFormat(string)
		if (genFormat):
			timeArray = time.strptime(string, genFormat)
			return time.strftime(formatOld2New, timeArray)
		else:
			print 'There\'s no datetime pattern matched for given string!'
			return False

	def getTodayStr(self, fmt = '%Y-%m-%d'):
		now = int(time.time())
		timeArray = time.localtime(now)
		return time.strftime(fmt, timeArray)
			
	def GmzqAutoStrReformat(self, string):
		genFormat = self.__selectFormat(string)
		if (genFormat):
			timeArray = time.strptime(string, genFormat)
			genStr = time.strftime('%Y_%m_%d', timeArray)
			genStrList = genStr.split('_')
			month = int(genStrList[1])
			day = int(genStrList[2])
			return genStrList[0] + '_' + str(month) + '_' + str(day)
		else:
			print 'There\'s no datetime pattern matched for given string!'
			return False

			
			
	def __selectFormat(self, string):
		#for (i = 0; i < len(self.datetimePattern); i++):
		for curPtn in self.datetimePattern:
			key = self.datetimePattern.index(curPtn)
			match = curPtn.match(string)
			if (match):
				return self.datetimeFormat[key]
		else:
			print 'There\'s no datetime pattern matched for given string!'
			return False
		


class configUtil:
	def __init__(self, cfgPath = 'config.ini'):
		self.cf = ConfigParser.ConfigParser()
		self.cfgPath = cfgPath
		self.cf.read(self.cfgPath)
		
	def test(self):
		print self.cf.get('logname', 'test')
		
	def getSections(self):
		return self.cf.sections()
		
	def getOptions(self, section = 'logname'):
		return self.cf.options(section)
		
	def getItems(self, section = 'logname'):
		return self.cf.items(section)
		
	def getSpecCfg(self, key, section = 'logname'):
		return self.cf.get(section, key)
		
	
		
if __name__ == '__main__':
	sys.exit();