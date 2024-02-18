mkdir backend
python3 -m venv env
source env/bin/activate
mkdir if req
git clone https://github.com/dishant-yadav/deduct-ai-backend-api 
cd deduct-ai-backend-api
pip install -r requirements.txt
python3 manage.py makemigartions
python3 manage.py migarte
python3 manage.py runserver localhost:8000
