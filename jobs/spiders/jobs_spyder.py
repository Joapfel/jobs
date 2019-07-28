from scrapy import Spider
import datetime


class JobsSpyder(Spider):
    name = 'jobs'
    start_urls = [
        'https://jobs.apple.com/en-us/search?sort=relevance'
    ]

    def parse(self, response):
        for job_page in response.xpath("//div[@class='results']"
                                       "/div[@id='active-search-results']"
                                       "/div[@class='results__table']"
                                       "/table/tbody/tr/td[1]/a/@href").getall():
            yield response.follow(job_page, callback=self.parse_job_description)

        next_page = response.xpath("//ul/li[@class='pagination__next']"
                                   "/span/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_job_description(self, response):
        posted = response.xpath("//div[@class='sum-info']/div[1]/span/strong/text()").get()
        posted = str(datetime.datetime.strptime(posted, '%b %d, %Y').date())
        yield {
            'company': 'Apple',
            'url': response.request.url,
            'job-title': response.xpath("//div[@class='job-details']//h1/text()").get(),
            'job-location': response.xpath("//div[@class='job-details']"
                                           "//div[@id='job-location-name']/text()").get(),
            'job-team': response.xpath("//div[@class='job-details']//div[@id='job-team-name']/text()").get(),
            'job-summary': response.xpath("//div[@id='jd-job-summary']/span/text()").get(),
            'posted': posted,
            'weekly-hours': response.xpath("//div[@class='sum-info']/div[2]/span/strong/text()").get(),
            'role-number': response.xpath("//div[@class='sum-info']/div[3]/strong/text()").get(),
            'key-qualifications': response.xpath("//div[@id='jd-key-qualifications']/ul/li/span/text()").getall(),
            'description': response.xpath("//div[@id='jd-description']/span/text()").get(),
            'education-experience': response.xpath("//div[@id='jd-education-experience']/span/text()").get(),
            'additional-requirements': response.xpath("//div[@id='jd-additional-requirements']"
                                                      "/ul/li/span/text()").getall()
        }


if __name__ == '__main__':
    from settings.logging_initializer import init_logger
    logger = init_logger('crawler_loggs')
    logger.info('Starting crawle process.')

    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl('jobs')
    process.start()
