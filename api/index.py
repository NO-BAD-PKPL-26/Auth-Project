import os

from auth_project.wsgi import application

is_vercel_runtime = bool(os.getenv('VERCEL') or os.getenv('VERCEL_URL') or os.getenv('VERCEL_ENV'))

if is_vercel_runtime and os.getenv('PRODUCTION', 'false').lower() != 'true':
	from django.core.management import call_command

	# Ensure sqlite demo database has required tables on cold start.
	call_command('migrate', interactive=False, run_syncdb=True, verbosity=0)

app = application