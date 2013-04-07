import unittest

import logging
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.lxmlsel import HtmlXPathSelector
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.spiders.Lafbot import Cosme
from test.test_comment_extractor import load_file

logging.debug('creating logger')
logger = logging.getLogger(__name__)

class TestLaffayetteCommentExtract(unittest.TestCase):
    

    xpathRegistry = XPathRegistry()
        
    def test_comment_extraction(self):
        cosme = Cosme()
        sephora_html = load_file('Laffayette.html')
        url = 'http://www.laffayette.com.br/produto/esmalte-revlon-scented-nail-enamel-14,7ml.html'
        request = Request(url=url)
        response = HtmlResponse(url=url,
                            request=request,
                            body=sephora_html,
                            encoding = 'utf-8')
        
        print 'About to parse item'
        item = self.my_parse_item(response, cosme)
        print '%s ' % item
        
        
    def my_parse_item(self, response, cosme):
        hxs = HtmlXPathSelector(response)
        #cosmeItem['url'] = response.url
        #siteModule = self.xpathRegistry.getXPath(cosmeItem['site'])
        '''
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()
        '''
        siteModule = self.xpathRegistry.getXPath('laffayette')        
        return cosme.get_comments(hxs, siteModule)
        