from flask import Flask, request, make_response
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

def delete(container_name):
    client=docker.from_env()
    try: 
      webapp=client.containers.get(container_name)
      webapp.remove(v=True, force=True)
      return "container was deleted"
    except docker.errors.NotFound:
      print(container_name+" does not exist")
      return "Nothing to delete"
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
      deploy(container_name, container_image, external_port, internal_port)
      return "Container created in production\n", 200
          
    else:
      print("please review you parameter")
      return "Application is not ready", 402

@app.route('/staging', methods = ['POST'])
def staging():
    content=request.get_json()
    container_name="preprod-"+content['your_name']
    container_image=content['container_image']
    external_port=content['external_port']
    internal_port=content['internal_port']
    if(container_name and container_image and external_port and internal_port):
      deploy(container_name, container_image, external_port, internal_port)
      return "Container created in staging\n", 200
    else:
      print("please review you parameter\n")
      return "Please review your parameter, application is not ready\n", 402

@app.route('/review', methods = ['POST', 'DELETE'])
def review():
    content=request.get_json()
    container_name="review-"+content['your_name']
    if request.method == 'POST':
        container_image=content['container_image']
        external_port=content['external_port']
        internal_port=content['internal_port']
        if(container_name and container_image and external_port and internal_port):
          deploy(container_name, container_image, external_port, internal_port)
             
          return "Container created in review\n", 200
    if request.method == 'DELETE':
        if(container_name):
          delete(container_name)
          return "Application is deleted in review\n", 200
    else:
      print("please review your parameters\n")
      return "Please review your parameters, application is not ready\n", 402
  
    


@app.route('/', methods = ['GET'])
def welcome():
  app_url=(request.base_url).replace("1993","80")
  return "Welcome to EAZYTraining deployment API \n your application URL is available at ''"+ app_url +"'' if external_port=80"


app.run(host="0.0.0.0", port=1993)
