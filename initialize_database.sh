python3 -m venv myvenv
source myvenv/bin/activate
pip install django~=1.11.0
pip install django-widget-tweaks
python manage.py migrate
