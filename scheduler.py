### load settings and apps ###
import django               ##
django.setup()              ##
##############################

import os
import redis
from rq_scheduler import Scheduler

from scheduled_jobs import master_jobs

conn = redis.from_url(os.getenv('BROKER_URL'))

if __name__ == '__main__':
	scheduler = Scheduler(connection=conn)

	# remove existing master scheduler job
	for job in scheduler.get_jobs():
		if job.description == 'master':
			scheduler.cancel(job)

	###### add cron jobs here #######
	# scheduler.cron(               #
	# 	cron_string,                #=> A cron string (e.g. "0 0 * * 0")
	# 	func=func,                  #=> Function to be queued
	# 	args=[arg1, arg2],          #=> Arguments passed into function when executed
	# 	kwargs={'foo': 'bar'},      #=> Keyword arguments passed into function when executed
	# 	repeat=10                   #=> Repeat this number of times (None means repeat forever)
	# 	queue_name=queue_name       #=> In which queue the job should be put in
	# )                             #
	#################################

	scheduler.cron(
		"0 */2 * * *",
		func=master_jobs.run_article_scores,
		queue_name='default',
		description='master'
	)

	scheduler.run()

