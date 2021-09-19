import scrapy

class DistroSpider(scrapy.Spider):
  name = 'DistroSpider'
  start_url = 'https://distrowatch.com/'
  start_urls = [start_url + '/?language=PT']
  user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

  def parse(self, response):
    distros = response.xpath("*//table[@class='News'][@style='direction: ltr']/tr/td/a/@href").getall()   # obtendo o link para cada distro
    for distro in distros:     
      complete_url = self.start_url + 'table.php?distribution=' + distro    # concatenando url com nome de cada distro 
      yield scrapy.Request(url=complete_url, callback=self.parse_detail)    # consultando a página de cada distro para obter informações específicas

  def parse_detail(self, response):
    distro = response.xpath("*//ul")[1] 

    yield { 
      'name': response.xpath("*//td/h1/text()").get(),
      'ranking': response.xpath(".//td/b/text()")[2].get(),
      'based_on': distro.xpath(".//li")[1].xpath('.//a/text()').getall(), 
      'architecture': distro.xpath(".//li")[3].xpath('.//a/text()').getall(), 
      'graphicalEnv': distro.xpath(".//li")[4].xpath('.//a/text()').getall(), 
      'tags': distro.xpath(".//li")[5].xpath('.//a/text()').getall(), 
      'popularity': distro.xpath(".//li")[7].xpath('.//a/text()').get(),
      'rating': response.xpath(".//td/b/text()")[6].get()
    }