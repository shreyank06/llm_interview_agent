### Execution
clone this repo and go to latest branch 
```
git checkout latest
```
go to
```
https://platform.openai.com/api-keys
```
create new secret api key and
go to main.py and 
on line 12 replace this line 
```
OPENAI_API_KEY = ""
```
by 
```
OPENAI_API_KEY = "your personal api key"
```

install docker
```
sudo apt-get install docker-compose 
```
build docker image
```
sudo docker-compose build --no-cache
```

after the docker image is built, enter the docker env
```
docker-compose run --rm ai_interview_app
```
