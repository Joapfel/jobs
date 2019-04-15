from datetime import datetime
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from email_service.email_service import EmailService

mongo_client = MongoClient('localhost', 27017)
subscribers = mongo_client.jobs.subscribers

for subscriber in subscribers.find():
    subscriber = dict(subscriber)
    email = subscriber['email']
    company = subscriber['company']
    timestamp_last = subscriber['timestamp_last']
    keywords_must = ' '.join(subscriber['keywords_must'])
    # keywords_can = ' '.join(subscriber['keywords_can'])

    # TODO: add more fields to match for
    search = {
        'query': {
            'bool': {
                'must': [
                    {
                        'bool': {
                            'should': [
                                {'match': {'job-title': keywords_must}},
                                {'match': {'job-team': keywords_must}},
                            ]
                        }
                    },
                    {
                        'range': {
                            'posted': {
                                'gte': timestamp_last
                            }
                        }
                    }
                ],
                #'should': [
                #    {'match': {'job-title': keywords_can}},
                #    {'match': {'job-team': keywords_can}}
                #]
            }
        }
    }

    # search with the filter
    es = Elasticsearch()
    results = es.search(index='jobs', body=search)

    # prepare email client
    email = EmailService(host='smtp.gmail.com', port=465,
                         sender='jojokr94@gmail.com', receivers=[email])
    email.login(pw='jJWyERH88E6%Em^5i^!8CmXrG$@QiM2')

    date_structure = '%Y-%m-%d'
    timestamp_update = datetime.strptime(timestamp_last, date_structure)
    for res in results['hits']['hits']:
        job_title = res['_source']['job-title']
        job_team = res['_source']['job-team']
        url = res['_source']['url']
        job_posted = datetime.strptime(res['_source']['posted'], date_structure)

        message = f"""From: Jobs
            Subject: New Job at Apple

            Job-Title: {job_title}\n
            Job-Team: {job_team}\n
            {url}
        """

        email.send_message(message)

        # get the newest job timestamp
        if job_posted > timestamp_update:
            timestamp_update = job_posted

    # update the timestamp in mongo
    subscribers.update_one(subscriber,
                           {'$set': {'timestamp_last': datetime.strftime(timestamp_update, date_structure)}})

