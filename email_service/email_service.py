from elasticsearch import Elasticsearch
from email_sender import EmailService
import jmespath

search = {
    'query': {
        'bool': {
            'must': [
                {'match': {'job-title': 'Machine Learning'}},
                {'match': {'job-team': 'Software and Services'}}
            ]
        }
    }
}

es = Elasticsearch()
results = es.search(index='jobs', body=search)

email = EmailService(host='smtp.gmail.com', port=465,
                     sender='jojokr94@gmail.com', receivers=['kraemer.johannes.p@gmail.com'])
email.login(pw='jJWyERH88E6%Em^5i^!8CmXrG$@QiM2')

for res in results['hits']['hits']:
    job_title = res['_source']['job-title']
    job_team = res['_source']['job-team']
    url = res['_source']['url']

    message = f"""From: Jobs\n
        Subject: New Job at Apple\n

        Job-Title: {job_title}\n
        Job-Team: {job_team}\n
        {url}
    """

    email.send_message(message)

