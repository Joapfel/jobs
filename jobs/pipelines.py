# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from elasticsearch import Elasticsearch
import redis
import hashlib


class CheckValuesPipeline(object):

    #TODO: more finegrade decision on missing values
    def process_item(self, item, spider):
        if not item['job-title']:
            item['job-title'] = ''
        if not item['job-location']:
            item['job-location'] = ''
        if not item['job-team']:
            item['job-team'] = ''
        if not item['job-summary']:
            item['job-summary'] = ''
        if not item['posted']:
            item['posted'] = ''
        if not item['weekly-hours']:
            item['weekly-hours'] = ''
        if not item['role-number']:
            item['role-number'] = ''
        if not item['key-qualifications']:
            item['key-qualifications'] = ''
        if not item['description']:
            item['description'] = ''
        if not item['education-experience']:
            item['education-experience'] = ''
        if not item['additional-requirements']:
            item['additional-requirements'] = ''
        return item


class AlreadyGotThatPipeline(object):

    def open_spider(self, spider):
        self.agt_client = redis.Redis()

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        to_hash = item['job-title'] \
                + item['job-location'] \
                + item['job-team'] \
                + item['job-summary'] \
                + str(item['posted']) \
                + item['weekly-hours'] \
                + item['role-number'] \
                + ' '.join(str(el) for el in item['key-qualifications']) \
                + item['description'] \
                + item['education-experience'] \
                + ' '.join(str(el) for el in item['additional-requirements'])
        hashed = hashlib.md5(bytes(to_hash, encoding='utf8')).hexdigest()
        if self.agt_client.exists(hashed):
            raise DropItem
        else:
            self.agt_client.set(name=hashed, value='seen')
            return item


class ElasticPipeline(object):

    """
    Look at example here when extending to another host
    https://docs.scrapy.org/en/latest/topics/item-pipeline.html
    """

    mapping = {
        'mappings': {
            'job': {
                'properties': {
                    'posted': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd'
                    }
                }
            }
        }
    }

    def process_item(self, item, spider):
        es = Elasticsearch()
        # ignore 400 cause by IndexAlreadyExistsException when creating an index
        es.indices.create(index='jobs', body=self.mapping, ignore=400)
        es.index(index='jobs', doc_type='job', body=item)
        raise DropItem
        #return item
