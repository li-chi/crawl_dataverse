import scrapy
import os

class QuotesSpider(scrapy.Spider):
    name = "dataverse"

    def start_requests(self):
        total = int(self.settings['TOTAL_RECORD'])
        pages = range(1,int(total/10)+1)
        url = self.settings['MAIN_URL']
        for page in pages:
            yield scrapy.Request(url=url+str(page), callback=self.parse)

    def parse(self, response):
        for div in response.css('div.card-title-icon-block'):
            link = div.css('a::attr(href)').get()
            doi = link.split('=')[-1]
            path = self.settings['DIR'] + '/' + doi.replace('/','-')
            
            os.mkdir(path)
            yield scrapy.Request(self.settings['BASE_URL']+link, callback=self.parse2, meta={'path': path})

    def parse2(self, response):
        #page = response.url.split("/")[-1]
        #filename = '%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % persist_id)
        for div in response.css('div.file-metadata-block'):
            full_link = div.css('a::attr(href)').get()
            filename = div.css('a::text').get().strip()
            filepath = response.meta['path'] + '/' + filename
            persist_id = full_link.split('?')[1].split('&')[0]
            yield scrapy.Request(url='https://dataverse.harvard.edu/api/access/datafile/:persistentId?'+persist_id, callback=self.parse3, meta={'filename': filepath})

    def parse3(self, response):
        #page = response.url.split("/")[-1]
        with open(response.meta['filename'], 'wb') as f:
            f.write(response.body)