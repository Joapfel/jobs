import logging
import re
from scrapy import Spider
import datetime

logger = logging.getLogger('main.jobs-spyder')


class JobsSpyderGoogle(Spider):
    name = 'jobs_google'
    start_urls = [
        "https://careers.google.com/jobs/results/?company=Chronicle&company=Google&company=Google"
        "%20Fiber&company=Loon&company=Verily%20Life%20Sciences&company=Waymo&company=Wing&company="
        "X&company=YouTube&employment_type=FULL_TIME&employment_type=INTERN&employment_type=PART_TIME"
        "&employment_type=TEMPORARY&hl=en_US&jlo=en_US&q=&sort_by=relevance"
    ]

    def parse(self, response):
        for job_page in response.xpath().getall():
            yield response.follow(job_page, callback=self.parse_job_description)

        next_page = response.xpath().get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_job_description(self, response):
        posted = response.xpath().get()
        try:
            posted_tmp = str(datetime.datetime.strptime(posted, '%b %d, %Y').date())
        except ValueError:
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

        yield {
            'company': 'Google',
            'url': response.request.url,
            'job-title': response.xpath("").get(),
            'job-location': response.xpath("").get(),
            'job-team': response.xpath("").get(),
            'job-summary': response.xpath("").get(),
            'posted': posted,
            'weekly-hours': response.xpath("").get(),
            'role-number': response.xpath("").get(),
            'key-qualifications': response.xpath("").getall(),
            'description': response.xpath("").get(),
            'education-experience': response.xpath("").get(),
            'additional-requirements': response.xpath("").getall()
        }


if __name__ == '__main__':
    from settings.logging_initializer import init_logger
    logger = init_logger('crawler_loggs')
    logger.info('Starting crawle process.')

    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl('jobs_google')
    process.start()