from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from scheduled_jobs import master_jobs

class Command(BaseCommand):
	help = 'Runs article scoring via CLI'

	def handle(self, *args, **options):
		master_jobs.run_article_scores()
