import scrapy as scrapy

from ..servicies.get_values import get_values


class ProxiesSpider(scrapy.Spider):
    name = 'proxies'
    allowed_domains = ['www.nntime.com']
    start_urls = ['http://www.nntime.com/']

    def parse(self, response, **kwargs):
        script_key_list = response.xpath('/html/head/script[2]/text()').get().strip()[:-1].split(';')
        script_key_dict = dict(elem.split('=') for elem in script_key_list)

        ports_list = response.xpath('//tr//script/text()').extract()
        cropped_ports_list = [elem[19:-1] for elem in ports_list]
        split_ports_list = [elem.split('+') for elem in cropped_ports_list]
        ports = [''.join(get_values(script_key_dict, elem)) for elem in split_ports_list]

        ip_addresses = response.xpath('//tr//td[2]/text()').extract()

        row_data = zip(ip_addresses, ports)
        for item in row_data:
            scraped_info = {
                'ip_address': item[0],
                'port': item[1]
            }
            yield scraped_info
