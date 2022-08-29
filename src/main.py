from flask import Flask
from flask import request
import docker

app = Flask(__name__)

# install library with pip3 install docker==6.0.0 flask==2.2.2
# PROD curl -X POST http://ip10-0-0-3-cc54afviqhe0g95rin70-1993.direct.docker.labs.eazytraining.fr/prod -H 'Content-Type: application/json' -d '{"your_name":"dirane","container_image":"dirane/alpinehelloworld", "external_port":"80", "internal_port":"5000"}'
# STAGING curl -X POST http://ip10-0-0-3-cc54afviqhe0g95rin70-1993.direct.docker.labs.eazytraining.fr/staging -H 'Content-Type: application/json' -d '{"your_name":"dirane","container_image":"dirane/alpinehelloworld", "external_port":"80", "internal_port":"5000"}'


def deploy(container_name, container_image, external_port, internal_port):
    client=docker.from_env()
    image = client.images.pull(container_image)
    try: 
      webapp=client.containers.get(container_name)
      webapp.remove(v=True, force=True)
      client.containers.run(container_image, detach=True, name=container_name, ports={internal_port:external_port}, environment=["PORT=5000"])
      return "container created in production"
    except docker.errors.NotFound:
      print(container_name+" does not exist")
      client.containers.run(container_image, detach=True, name=container_name, ports={internal_port:external_port}, environment=["PORT=5000"])
      return "container created in production"
    except docker.errors.APIError:
      return "ERROR please contact administrator"


@app.route('/prod', methods = ['POST'])
def prod():
    content=request.get_json()
    container_name="prod-"+content['your_name']
    container_image=content['container_image']
    external_port=content['external_port']
    internal_port=content['internal_port']
    if(container_name and container_image and external_port and internal_port):
      #print("good paramater")
      #print(container_name, container_image, external_port, internal_port)
      deploy(container_name, container_image, external_port, internal_port)
      return "container created in production"
          
    else:
      print("please review you parameter")
      return "Application is ready"

@app.route('/staging', methods = ['POST'])
def staging():
    content=request.get_json()
    container_name="preprod-"+content['your_name']
    container_image=content['container_image']
    external_port=content['external_port']
    internal_port=content['internal_port']
    if(container_name and container_image and external_port and internal_port):
      #print("good paramater")
      #print(container_name, container_image, external_port, internal_port)
      deploy(container_name, container_image, external_port, internal_port)
      return "Application is ready"
    else:
      print("please review you parameter")
      return "Please review your parameter"

@app.route('/', methods = ['GET'])
def welcome():
  app_url=(request.base_url).replace("1993","80")
  return "Welcome to EAZYTraining deployment API \n your application URL is available at ''"+ app_url +"'' if external_port=80"


app.run(host="0.0.0.0", port=1993)