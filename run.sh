# Create environment if doesn't exist
#python3 -m venv venv
. venv/bin/activate
#pip install -e .
export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
flask run