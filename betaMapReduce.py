from pymongo import Connection
import os,sys,urllib2
import time
import json
import logging
from fuzzywuzzy import fuzz
import hashlib
import logging

#secondCon = secondConnection('outDb')
logging.basicConfig(filename='matchLog.log', level=logging.DEBUG)

MAINDB = 'matching'
NAME_RATIO = 92
FULLPROC = False
ADD_TOP_SCORE_DUPLICATE	= False			
BATCHSIZE = 150

def singleMatch(key1, key2):
	comments_db = 'comments_db'
        collection = 'scratchDb'
	connection = Connection()
	db = connection[comments_db]
	db = db[collection]
		
	item1 = list(db.find( {'key' : key1} )) 
	item2 = list(db.find( {'key' : key2} )) 
	item1 = item1[0]
	item2 = item2[0]
	ratio = fuzzyNameMatch(item1['name'] , item2['name'])
	print 'name Ratio is: %s' % ratio

	if objectMatch(item1, item2):
		print 'has match'	

def isFullProcess(first):
	if FULLPROC:
		return False
	else:
		
		out=  hasGroupKey(first)
		return out

def  matchVolumized(db):
   start = time.time()
   quarter = 0.01
   size =  db.find().count()-1 
   hasMatch = False
   print size
 #  try :  
   for cursor, first in  enumerate(db.find(timeout= False)):
		if not isFullProcess(first):
			for idx,second in enumerate(db.find(timeout = False)):
				if first['key'] != second['key'] and objectMatch(first,second):
					insertOrUpdate(first, second, db)
					hasMatch = True
					logging.debug('%s, %s, %s' % (second['matchscore'], first['key'], second['groupid']))
					print 'FULL MATCH %s' %second['groupid']

				if  idx == size and hasMatch:
					print 'Parent Updated'					
					first['matchscore'] = 100
					first['rank'] = '1'	
					first['groupid'] = hashlib.md5(first['key']).hexdigest() 
					updateInDb(first,db)
					hasMatch = False 	
		print cursor
		if cursor > size*quarter and cursor < (size+30)*quarter:
			quarter = quarter +quarter
			print "percantage done : %s" % quarter						
   #except Exception, e:
#		print 'CRASH %s' % e
#		logging.debug('crash occured at cursor %s with exception %s' % (cursor, e))
					
   end = time.time()
   print "feeding finisehd in %s ms"%(end-start)
def insertOrUpdate(first,second, db):
	
	second['groupid'] = hashlib.md5(first['key']).hexdigest()
	second['matchscore'] = fuzzyNameMatch(first['name'], second['name'])	
	
	if hasExistingMatch(second, db):
		validateSiteMatch(second, db)
	else:
		updateInDb(second,db)	

def validateSiteMatch(item, db):
	
	find = list(db.find( { 'groupid' : item['groupid'] }))
	for savedItem in find:
		if item['site'] == savedItem['site']:
			if checkScore(savedItem['matchscore'], item['matchscore']):
				key = savedItem['key']
				db.update( {'key': key}, {'$unset' : { 'groupid' : 1 } })
				
				updateInDb(item, db)
				print 'Replacing %s with %s' % (savedItem['key'], item['key'])
			else:
				pass		 			
		else:
			updateInDb(item, db)			

def hasExistingMatch(item, db):
  if 'groupid' in item:
	  find = list(db.find( { 'groupid' : item['groupid'] }))
	  if find:
		for savedItem in find: 
			if savedItem:
				if item['site'] == savedItem['site']:
					if not 'rank' in savedItem:
						return True
					else:
						return False
				else:
					return False
			else:
				print 'check exists returns False'
				return False
	  else:
		return False
  else:
	return False

def checkScore(score1, score2):
	if score1 < score2:
		return True
	elif score1 > score2:
		return False
	elif score1 == score2:
		return ADD_TOP_SCORE_DUPLICATE				

def objectMatch(first, second):
	if not isFullProcess(second):
		try:
			if first['site'] != second['site']:
				if matchVolume(first['volume'], second['volume']):		
					if fuzzyMatchBrand(first['brand'], second['brand']):
						if matchName(first['name'], second['name']):
							return True
						else:
							return False	
		except Exception, e:
			logging.debug(e)		


def fuzzyMatchBrand(first, second): 
	first = first.lower().strip()
	#first = fuzz.asciidammit(first)
	second = second.lower().strip()
	#second = fuzz.asciidammit(second)
	ratio = fuzz.ratio(first, second)
	
	if ratio >= 98:
		return True
	else:
		return False

def fuzzyNameMatch(name1, name2):
	name1 = name1.lower()
	name2 = name2.lower()
	name1 = fuzz.asciidammit(name1)
	name2 = fuzz.asciidammit(name2)
	ratio = fuzz.token_set_ratio(name1,name2)	
	return ratio 

def matchName(name1, name2):
	ratio = fuzz.token_set_ratio(name1,name2)	
	#ratio = fuzzyNameMatch(name1,name2)	
	if ratio > NAME_RATIO:
		return True
	else:
		return False
		
def checkVolume(vol1, vol2):
	if vol1 =='NA':
		return False
	else:
		if vol2 == 'NA':
			return False
		else:
			return True

def matchVolume(vol1, vol2):

  if checkVolume(vol1,vol2): 

	ratio = fuzz.ratio(vol1, vol2)
	if ratio == 100:
		return True
	else:
		return False

def hasGroupKey(item):
	if 'groupkey' in item:
		return True
	else:
		return False

def secondConnection(secondCollection):
	con = Connection()
	con = con[MAINDB]	
	con = con[secondCollection]
	return con

def outputDb(item, collection):
        
        groupDb = collection

	try:
		groupDb.insert(item)
	
	except Exception, e:
		print 'mongo exception'
 
def updateInDb(item, collection):
        groupDb = collection
	try:
		groupDb.update( {'key': item['key']}, item, safe = True)
	
	except Exception, e:
		print 'mongo exception'

	
def main(collection):
        connection = Connection()
	db = connection[MAINDB]
	db = db[collection]
	print 'collection in use %s' %db
	matchVolumized(db)

if __name__ == "__main__":

    #first argument: batch size
    #second argument: dmp or feed
    #third argument : filename
    main(str(sys.argv[1]))
