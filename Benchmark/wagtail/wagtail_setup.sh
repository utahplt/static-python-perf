# requirements for cinder
sudo apt install libsqlite3-dev

# download and build cinder
git clone https://github.com/mrigankpawagi/cinder && cd cinder
./configure --enable-loadable-sqlite-extensions && make -j
cd ..

# create (and activate) venv with static-python
cinder/python -m venv testsite/env
source ./testsite/env/bin/activate

# install wagtail
python -m pip install wagtail

# create a new wagtail site
wagtail start TestSite testsite

# Django setup
cd testsite
pip install -r requirements.txt
python manage.py migrate
DJANGO_SUPERUSER_PASSWORD=sudo1234 python manage.py createsuperuser --email=su@su.com --username=su --noinput
python manage.py runserver
