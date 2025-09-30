### Execution
clone this repo
go to latest branch 
```
git checkout latest
```
go to
```
https://platform.openai.com/api-keys
```
create new secret api key
go to main.py
on line 12 replace this line 
```
OPENAI_API_KEY = "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"
```
by 
```
OPENAI_API_KEY = "your personal api key"
```

install docker
```
sudo apt-get install docker-compose 
```
```
sudo docker-compose build --no-cache
```

after the docker image is built, enter the docker env
```
docker-compose run --rm ai_interview_app
```