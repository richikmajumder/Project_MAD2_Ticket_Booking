python -m venv environment;
source environment/bin/activate;
pip install -r requirements.txt;
npm install;
python api.py & npm run serve & redis-server & celery -A api.celery worker --loglevel=info & celery -A api.celery beat --max-interval 1 -l info;