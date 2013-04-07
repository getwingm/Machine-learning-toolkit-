from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class LaffayetteXPath(AbstractXPath):
    META = {
    
    "image" : "//img[@id=\'imgProd0\']/@src",
    "name" :  "//li[@class=\'nomeProd_g\']/text()",
    "brand" : "//li[@class=\'marca\']/text()",
    "price" : "//span[@class=\'precoItem\']/b/text()",
    "start" : "//null",
    "description" : "//div[@id=\'itensProd\']/ul/li[3]/p/text()",
    "category" : "//div[@class=\'tituloPag\']/ul/li[5]/a/text()",
    "sku" : "//ul/li[@class=\'marca\']/span/i/text()",
    }

    def get_meta(self):
        return self.META

    COMMENTS = {
       "commentList":  "//div[@id=\'comentarios\']/ul",
       "commenterName": ".//li[@id=\'star\']/div[@class=\'dados\']/span/text()",
       "commentText": ".//li[2]/text()",
       "commentDate": ".//li[@id=\'star\']/div[@class=\'dados\']/text()",
       "commentStar": ".//li[@id=\'star\']/div[1]/@class"
    }

    
    def get_comments(self):
        return self.COMMENTS
