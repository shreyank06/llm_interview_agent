### Execution
start docker env
```
docker-compose up -d
```
if after this you get no module named disutils found, do this
```
python3 -m venv myenv
source myenv/bin/activate
pip install setuptools
deactivate
```
and execute this again
```
docker-compose up -d
```
after the docker image is built, enter the docker env
```
docker-compose run --rm ai_interview /bin/bash
```