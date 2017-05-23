Setup Local Environment
=============

1. Install requirements
  - `pip install -r requirements.txt` to install python dependencies
2. Run migrations
  - use `ENV=local` for development environment
  - `./manage.py makemigrations <module_name>`
  - `./manage.py migrate <module_name>`
3. Start all processes at once using `forego` (auto asset recompile, local server, etc.)
	- Install `forego`
  - `forego start -f Procfile.dev`