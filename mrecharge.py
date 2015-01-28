#!/usr/bin/python

import glob
import sys
import os
import hashlib
import util
from subprocess import call

print '####################Script Starting######################'
print '#Usage: /path/to/script/file path/to/log/ [date] [hour]#'
print '#########################################################'

logtype = 'bill'

args = sys.argv
argsLen = len(args)

logAttach = '_*'


if argsLen < 2:
    print 'Arguments Length Error: at least 1 argument is required!'
    sys.exit()
elif 4 == argsLen:
	if False == args[3].isdigit() or int(args[3]) > 23:
		print '2nd Argument should be the hour of that specified day(1st argument)'
		sys.exit()
	else:
		logAttach = '_' + str(args[3])

logpath = str(args[1])
if not os.path.exists(logpath):
	print 'Log path(' + logpath + ') does not exist on this server!'
	sys.exit()


dtUtil = util.Datetime()
cfgUtil = util.configUtil()

dateStr = args[2] if argsLen >= 3 else dtUtil.getTodayStr()
dateStr = dtUtil.GmzqAutoStrReformat(dateStr)

logName = cfgUtil.getSpecCfg(logtype)
hashKey = cfgUtil.getSpecCfg('key', 'logkey')
cfgkwd = cfgUtil.getSpecCfg(logtype, 'keywords')
bkdb = cfgUtil.getSpecCfg('db', 'ftp')
ftpuser = cfgUtil.getSpecCfg('ftpuser', 'ftp')
ftppass = cfgUtil.getSpecCfg('ftppass', 'ftp')
ftpport = cfgUtil.getSpecCfg('ftpport', 'ftp')
ftphost = cfgUtil.getSpecCfg('ftphost', 'ftp')
ftppath = cfgUtil.getSpecCfg('ftppath', 'ftp')


usedbsql = 'USE %s;\n' % bkdb
inssqls = ''
resFileName = ''

for logfile in glob.glob(r''+os.path.join(logpath, logName+'_'+dateStr+logAttach+'.log')):
	fh = open(logfile, 'rb')
	while True:
		line = fh.readline()
		if not line: break

		logSegment = line.strip().split('|')

		if not len(logSegment) == 14:
			print 'Loop Error: log segment length is illegal! Should be 14!'
			continue

		(gameAbbr, platformId, serverId, token, ts, keyword, rechargeTs, orderId, amount, isk, uname, cname, ifSuccess,
		 level) = logSegment

		resFileName = 'startup1_' + platformId + '_' + serverId + '.sql'

		if cfgkwd == keyword:
			calcHash = hashlib.md5(gameAbbr + platformId + serverId + hashKey).hexdigest().lower()[5:10]

			if not calcHash == token:
				print 'Loop Error: hash calculation mismatch with the token!'
				continue
			else:
				inssqls += "INSERT INTO recharge_order (platform, server, datetime, order_id, status, account, cname, " \
						   "amount, isk, level) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');\n" % \
						   (platformId, serverId, rechargeTs, orderId, ifSuccess, uname, cname, amount, isk, level)
		else:
			print 'Loop Error: keyword mismatch with configuration!'
			continue

inssqls = usedbsql + inssqls
inssqls += "/*totally crap%^&$#@!*/"

sqlFile = open(resFileName, 'w')

sqlFile.write(inssqls)


ftpParam = "-t 120 -r 20 -u '%s' -p '%s' -P '%s' -m -R '%s' '%s/' %s" % (ftpuser, ftppass, ftpport, ftphost, ftppath,
																		 resFileName)
call(["ncftpput", ftpParam])