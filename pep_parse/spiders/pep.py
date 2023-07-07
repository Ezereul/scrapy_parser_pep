import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        tables = response.css('table.pep-zero-table')

        for table in tables:
            table_links = table.css('tr td + td a::attr(href)').getall()
            for pep_link in table_links:
                yield response.follow(pep_link + '/', callback=self.parse_pep)

    def parse_pep(self, response):
        pattern = r'PEP (?P<number>\d+) – (?P<name>.*)'
        title = response.css('h1.page-title::text').get()
        text_match = re.search(pattern, title)

        if text_match is None:
            self.logger.warning(f'Error parsing {title} in {response.url}')
            return

        number, name = text_match.groups()
        data = {
            'number': number,
            'name': name,
            'status': response.css('dt:contains("Status") + '
                                   'dd abbr::text').get()
        }

        yield PepParseItem(data)
