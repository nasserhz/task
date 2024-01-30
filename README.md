# README

### Start project

set environment variables
```
cp .env.sample .env
```

project starts with docker-compose command, app will be available at: http://127.0.0.1:8000
``` 
docker-compose up -d --build
```


### Database migrations

run database migration with: 
``` 
docker-compose exec delay_report poetry run python manage.py migrate
```

### Load test data

add admin user and app data with django fixtures:
``` 
docker-compose exec delay_report poetry run python manage.py loaddata ./data/auth.json
```
``` 
docker-compose exec delay_report poetry run python manage.py loaddata ./data/app.json
```

### API document

Import ``` delay_report.postman_collection.json ``` postman collection 

```
POST http://127.0.0.1:8000/app/delay?order_id=1
GET http://127.0.0.1:8000/app/assign?agent_id=1
GET http://127.0.0.1:8000/app/report
```

### Admin dashboard

login to django admin at http://127.0.0.1:8000/admin
```
user: admin
pass: password
```
