"""
Pipelines per site are stored in their own folder for minumum chaos
"""

from utils import utils
from scrapy import log
import datetime
from cosme.pipes.default import AbstractSite

class MagazineLuizaSite(AbstractSite):
    
    #Do all default processing here before going on to site specific processing.
    def process(self, item,spider,matcher):
    
    
        if item['name']:
            temp = item['name']
            item['name'] = temp[0].lower()
    
        #if there isn't a price make it very expensive 
        if item['price']:
            temp = float(utils.getFirst(item['price']).replace(',','.'))
            item['price'] = temp
        if item['name']:
            temp = item['name']
        if item['brand']:
	    temp = item['brand'][0]
	    item['brand'] = temp    
		# item['brand'] = matcher.listMatch(temp)
        if item['url']:
            item['url'] = item['url'].lower()
        
	if item['category']:
		temp = item['category']
		item['category'] = temp[0]
	
	item['date_crawled'] = utils.convertDateClass(datetime.datetime.today().isoformat())
         
        #is this a gay video?
            
            
        return item
             
        #except:
        #    log.msg("Error parsing results", level=log.WARNING)
        #   raise DropItem("Something whent wrong parsing dropping item %s " % item['url'])
        
