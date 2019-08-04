import logging
import re
from scrapy import Spider
import datetime

logger = logging.getLogger('main.jobs-spyder')


class JobsSpyderMicrosoft(Spider):
    name = 'jobs_microsoft'
    start_urls = [
        'https://careers.microsoft.com/us/en/search-results'
    ]

    def parse(self, response):
        for job_page in response.xpath("//span[@class='job-title']/parent::a/@href").getall():
            logger.info('Job found:' + job_page)
            yield response.follow(job_page, callback=self.parse_job_description)

        # next_page = response.xpath("//ul/li[@class='pagination__next']"
                                   # "/span/a/@href").get()
        # if next_page:
            # yield response.follow(next_page, callback=self.parse)

    def parse_job_description(self, response):
        logger.info('Getting job information...')
        logger.info(response.xpath('//h1').getall())
        job_details = response.xpath("//div[@data-ph-at-id='job-fields']//ul//li/span[@class='lable-text']"
                                     "//text()").getall()
        job_details_count = len(job_details)
        if not job_details or job_details_count not in [6, 7]:
            logger.warning('Job details are unusual:')
            logger.warning(response.url)
            logger.warning(job_details)
            # return

        continuation_idx = 4
        job_number, \
            posted, \
            travel = job_details[:3]

        # if no travel is necessary it says literally 'None'
        if travel != 'None':
            travel += job_details[3].strip()
        else:
            continuation_idx = 3

        profession, \
            role_type, \
            employment_type = job_details[continuation_idx:]

        job_title = response.xpath("//div[@class='jd-header-block']//h1/text()").get()

        logger.info(f'Job Title: {job_title}\n'
                    f'Job number: {job_number}\n'
                    f'Posted date: {posted}\n'
                    f'Travel: {travel}\n'
                    f'Profession: {profession}\n'
                    f'Role type: {role_type}\n'
                    f'Employment Type: {employment_type}')

        try:
            posted_tmp = str(datetime.datetime.strptime(posted, '%b %d, %Y').date())
            logger.info('Formated date: ' + posted_tmp)
            return
        except ValueError:
            logger.warning('Date is unusual: ' + posted)
            return
            try:
                posted_tmp = str(datetime.datetime.strptime(re.sub('[^0-9]\s*', ', ', posted),
                                                            '%m, %d, %Y').date())
            except ValueError:
                try:
                    posted_tmp = str(datetime.datetime.strptime(posted, '%B %d, %Y').date())
                except ValueError:
                    posted_tmp = str(datetime.datetime.now().date())
                    logger.warning('Actual "Posted"-time was overridden with current time.')
            logger.warning(f'Posted time not recognized: {posted}\n'
                           f'Formatted to: {posted_tmp}\n')
        if posted_tmp:
            posted = posted_tmp

        return
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
    process.crawl('jobs_microsoft')
    process.start()