import os

from auth_project.wsgi import application

if os.getenv('VERCEL') and os.getenv('PRODUCTION', 'false').lower() != 'true':
	from django.core.management import call_command

	# Ensure sqlite demo database has required tables on cold start.
	call_command('migrate', interactive=False, run_syncdb=True, verbosity=0)

app = application