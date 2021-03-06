from BeautifulSoup import BeautifulSoup
from utils import utils
import re
from scrapy import log
from scrapy.exceptions import DropItem
import datetime
from  cosme.pipes.default import AbstractSite
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.pipes.utils.utils import get_http_response, cleanNumberArray2,multiStateVolume, cleanChars, extractSku,extractFloat,cleanSpaces
import sys
import traceback
import logging
import pipeMethods

logger = logging.getLogger(__name__)
logging.basicConfig(filename='branddrop.log', filemode = 'w',level=logging.DEBUG)
class Dafiti(AbstractSite):
	
	def __init__(self):
		self.siteModule = XPathRegistry().getXPath('submarino')
		
	def process(self, item, spider, matcher):
		if item['url']:
			item['url'] = item['url'].lower()					
		if item['price']: 
			if item['price'] != 'NA':
				temp = item['price']
				temp = extractFloat(temp)
				#pipeline expects price inside list
				arr = [temp]
				clean = cleanNumberArray2(arr, 'float')
				item['price'] = clean

		if item['brand']:
			temp = item['brand'][0]
			temp = matcher.dualMatch(temp)
			item['brand'] = temp
			if not item['brand']:
				logging.info(item['url'])
                                raise DropItem("**** **** **** Missing brand in %s . Dropping" % item)

		if item['category']:
			tempCat = item['category']
			item['category'] = ''
		if item['description']:
			temp = item['description'][0]	
			temp = cleanSpaces(temp)
			item['description'] = temp

		if item['image']:
			temp = item['image'] 
			temp = temp[0]
			item['image'] = temp
		if item['volume']: 
			temp = item['name']
			item['volume'] = multiStateVolume(temp)
		if item['product_id']:
			item['product_id'] = ''
					
		if item['sku']: 
			item['sku'] = '' 

		return item
