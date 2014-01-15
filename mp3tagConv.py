#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
created by YK,Yong Ki Kim
when:	2011. 12. 10
version: 0.2
changeLog
- directory 변수로 받으면 해당 디렉토리내의 mp3 태그 수정
- 'getTagName' is modified with easyid3 module
- first release dec 09, 2011
"""

import os,sys
from mutagen.easyid3 import EasyID3
#from mutagen.mp3 import MP3

def genFileName(fileName):
	'''
	replace file name space to '_' and lower the Capitals.
	'''
	nFileName = fileName.replace(' ', '_').lower()
	return nFileName

def getTagName(songName):
	'''
	get the mp3 tag about title, artist, album name.
	'''
	oTags = {}
	try:
		oSongInfo = EasyID3(songName)
		for i in oSongInfo.keys():
			oTags[i] = oSongInfo[i][0].encode('latin1')
	except:
		print "To get %s tag info is failed" % songName
		print "Maybe %s is already UTF" % songName
#		oTags = oSongInfo
	return oTags

def setTagName(nSongName, oTags):
	'''
	set the new mp3 tag about title, artist, album name.
	'''
	try:
		songInfo = EasyID3(nSongName)
		for i in songInfo.keys():
			if ( oTags[i] != "" ): 
				songInfo[i] = unicode( oTags[i], 'cp949' )
		songInfo.save()
		print "%s is changed successfully" % nSongName
	except:
		print "cp949 unicode capsulizing is not worked"
		print ""
	try:
		songInfo = EasyID3(nSongName)
		for j in songInfo.keys():
			if ( oTags[j] != "" ): 
				songInfo[j] = unicode( oTags[j], 'utf8' )
		songInfo.save()
		print "%s is changed successfully" % nSongName
	except:
		print "utf8 unicode capsulizing is not worked"
		print ""

def rmTagName(nSongName):
	'''
	remove the new mp3 tag 
	'''
	try:
		songInfo = EasyID3(nSongName)
		for i in songInfo.keys():
			songInfo[i] = ""
		songInfo.save()
	except:
		print "rmTagName is not worked"
#### Main ####
if ( len(sys.argv) == 1 ):
	print "%s Usage: [whole|rmtag|{file}|{dir $dirname}]" % sys.argv[0]

elif (sys.argv[1] == "whole"):
	for root, dirs, files in os.walk('./'):
		for fileName in files:
			if fileName[-3:].lower() == 'mp3':
				nFileName = genFileName(fileName)
				oFullPathFile  = os.path.join(root, fileName)
				nFullPathFile  = os.path.join(root, nFileName)
				os.rename(oFullPathFile, nFullPathFile)
				orgTags = getTagName(nFullPathFile)	
				setTagName(nFullPathFile, orgTags)

elif (sys.argv[1] == "rmtag"):
	answer = input()
	if ( answer == "Y" ):
		for root, dirs, files in os.walk('./'):
			for fileName in files:
				if fileName[-3:].lower() == 'mp3':
					nFileName = genFileName(fileName)
					oFullPathFile  = os.path.join(root, fileName)
					nFullPathFile  = os.path.join(root, nFileName)
					os.rename(oFullPathFile, nFullPathFile)
					rmTagName(nFullPathFile)
	else:
		print "Removing Tag is canceled"
	
elif (sys.argv[1][-3:].lower() == "mp3"):
	fileName = sys.argv[1]
	nFileName = genFileName(fileName)
	os.rename(fileName, nFileName)
	orgTags = getTagName(nFileName)
	setTagName(nFileName, orgTags)

elif (sys.argv[1] == "dir"):
	dName = sys.argv[2]
	for root, dirs, files in os.walk(dName):
		for fileName in files:
			if fileName[-3:].lower() == 'mp3':
				nFileName = genFileName(fileName)
				oFullPathFile  = os.path.join(root, fileName)
				nFullPathFile  = os.path.join(root, nFileName)
				os.rename(oFullPathFile, nFullPathFile)
				orgTags = getTagName(nFullPathFile)	
				setTagName(nFullPathFile, orgTags)
		
else:
	print "%s Usage: [whole|rmtag|{file}|{dir $dirname}]" % sys.argv[0]
