
# Why EAZYLABS ?

Hello world !

[After Heroku being acquired by salesforce, the free offer is not more available](https://blog.heroku.com/next-chapter). This will take effect on November 28, 2022.

unfortunately our gitlab-ci and jenkins courses were based on the Dynos offer that enable us to deploy container and host them (550-1,000 dyno hours per month).

we haven't found a credible alternative as easy as heroku that provide us a container hosting for free. We decide to build a very simple tool that help our student to deploy container through pipeline using simple curl (POST) request.

So our student can provision temporary infrastructure and use them as infrastructure deployment more easily than ever.

## Prerequisites
To use the application you need a ***virtual machine*** (`in the cloud, on-prem, in play-with-docker, in killercoda`) with ***docker installed***

Also ensure that your docker image is **public** to prevent this issue (access deny)
![image (4)](https://user-images.githubusercontent.com/18481009/209438392-a1f14205-7fd3-4dc1-8706-38da131fd7a1.png)

**Caution**: This API must not be used in production invironment

## Installation
### From Scratch
Make sure that
 - **python3** and **pip3** are alredy installed on your virtual machine
 - your **current user** have sufficient permisison to run docker command

Ensure that 
If you want to deploy the API directly on the VM host please run the following commands

    git clone https://github.com/eazytraining/eazylabs.git
    cd eazylabs
    pip3  install  -r  requirements.txt
   
   And then you can run the API 

       python3 src/main.py

Something like this will be shown

![image](https://user-images.githubusercontent.com/18481009/187277175-d8604dfe-e5fa-457c-a9b1-92fa711e705e.png)


### Using docker (also easy to install)
#### Use Eazytraining Image
A docker image is available on [eazytraining/eazylabs](https://hub.docker.com/repository/docker/eazytraining/eazylabs). You can use it directly by running this command for example : 
    
    docker run -d --name eazylabs --privileged -v /var/run/docker.sock:/var/run/docker.sock -p 1993:1993 eazytraining/eazylabs:latest
    
#### Build your own image
You are free to build image by your own. Just make sure that your **current user** have sufficient permisison to run docker command :

     git clone https://github.com/diranetafen/eazylabs.git
     cd eazylabs
     docker build -t eazylabs .
     docker run -d --name eazylabs --privileged -v /var/run/docker.sock:/var/run/docker.sock -p 1993:1993 eazylabs

#### Check container is OK after running
Show the containers logs with docker logs command : 
     
    docker logs eazylabs

Something like this will be shown

![image](https://user-images.githubusercontent.com/18481009/187277175-d8604dfe-e5fa-457c-a9b1-92fa711e705e.png)


**Caution** : Options  "--privileged" and  "-v /var/run/docker.sock:/var/run/docker.sock" are very dangereous option that must no be used in production environment
### Verify everything looks good
To ensure that the application is up and running, please try to reach the api throught your browser or curl at http://< your server address >:1993
You would get a mesage started with : `Welcome to EAZYTraining deployment API`

![image](https://user-images.githubusercontent.com/18481009/187278171-4381969e-dcf5-45f1-aedc-d3d56eefa2a8.png)
Now you are ready for the deployment
## Container deployment
The deployment of container is very easy.
Simple send a POST request with curl for example with the following parameter

 - `environment` : PROD or STATING
 - `your_name` : used to define your container's name on the server where eazylabs API is hosted
 - `container_image` : docker image to used for deployment
 - `external_port` : to reach your application (webapp) you need to provide the external corresponding to "-p" docker option
 - `internal_port` : your internal contatiner port used by your image corresponding to "-p" docker option

**Example**:

- **Staging** : The follwing command will deploy nginx image in staging environnement

        curl -X POST http://< server address>:1993/staging -H 'Content-Type: application/json' -d '{"your_name":"dirane","container_image":"nginx", "external_port":"80", "internal_port":"80"}'
    
- **Production** : The follwing command will deploy dirane/alpinehelloworld image in production environnement

        curl -X POST http://< server address>:1993/prod -H 'Content-Type: application/json' -d '{"your_name":"dirane","container_image":"dirane/alpinehelloworld", "external_port":"80", "internal_port":"5000"}'
    
- **Review** : 
    - The follwing command will deploy dirane/alpinehelloworld image in Review environnement

            curl -X POST http://< server address>:1993/review -H 'Content-Type: application/json' -d '{"your_name":"dirane","container_image":"dirane/alpinehelloworld", "external_port":"80", "internal_port":"5000"}'
    - The follwing command will delete dirane/alpinehelloworld image in Review environnement

            curl -X DELETE http://< server address>:1993/review -H 'Content-Type: application/json' -d '{"your_name":"dirane"}'

### Some rules

 - The API can be used to deploy multiple container on the same docker host but ensure that you provide different **your_name** and **external_port** parameters
 - to simulate prod and staging env, you can create another VM or directly the same host (used for prod deployment). If you use the same host for both deployment, provide a different **external_port** but the **your_name** can be the same for production and staging env
 
### Temporary infrastructure
If you are using temporary infrastructure like [killercoda](https://killercoda.com/), [play with docker](https://labs.play-with-docker.com/) or [play with eazytraining](http://docker.labs.eazytraining.fr/) don't forget that the port is content in the URL.

**Example For the API URL:**

http://ip10-0-1-3-cc6f19ssrdn0fvnms2og-***1993***.direct.docker.labs.eazytraining.fr/

**Example For App deployed with external_port = 80:**

http://ip10-0-1-4-cc6f19ssrdn0fvnms2og-***80***.direct.docker.labs.eazytraining.fr/

## Debug your deployment issue
FOr many reason you will face a lot of issue and in this section we will provide to you a way the get log and debug your deployment.
### From scratch deployment
If you made a deployment from scratch (pyrhon3 src/main.py), you will get the log directly in the console

![image](https://user-images.githubusercontent.com/18481009/187277175-d8604dfe-e5fa-457c-a9b1-92fa711e705e.png)

### Using Docker
If you use the easiest way to deploy eazylabs (container), the log must be get through `docker logs -f eazylabs`
![image](https://user-images.githubusercontent.com/18481009/211189177-792d42c2-7726-4435-aecc-55d30a0a3748.png)

### Test your deployment
To test your deployment we recommend you to follow these steps:

 - Launch linux terminal with `curl` command line installed
 - Modify the deployment command with your own values :   `curl -X POST http://< server address>:1993/prod -H 'Content-Type: application/json' -d '{"your_name":"dirane","container_image":"dirane/alpinehelloworld", "external_port":"80", "internal_port":"5000"}'`
![image](https://user-images.githubusercontent.com/18481009/211189466-92dd30f4-8a87-4871-b17a-8332c8540d61.png)
 - Watch your logs to verify the result
![image](https://user-images.githubusercontent.com/18481009/211189513-ca09e338-6291-43b1-9c40-34b7c4ca2dee.png)

Another example with error (we remove "e" on image name to ensure that my image could not be download).

    curl -X POST http://ip10-0-0-3-cet8pma46q9gga880adg-1993.direct.docker.labs.eazytraining.fr/prod -H 'Content-Type: application/json' -d '{"your_name":"dirane","container_image":"diran/alpinehelloworld", "external_port":"80", "internal_port":"5000"}'

![image](https://user-images.githubusercontent.com/18481009/211189584-07dc253d-f880-41ae-994e-356d28075766.png)

Check the result

![image](https://user-images.githubusercontent.com/18481009/211189675-7dbb7139-d329-4722-9975-f611a88ad861.png)

    Traceback (most recent call last):
      File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 2525, in wsgi_app
        response = self.full_dispatch_request()
      File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1822, in full_dispatch_request
        rv = self.handle_user_exception(e)
      File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1820, in full_dispatch_request
        rv = self.dispatch_request()
      File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1796, in dispatch_request
        return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
      File "/app/src/main.py", line 48, in prod
        deploy(container_name, container_image, external_port, internal_port)
      File "/app/src/main.py", line 14, in deploy
        image = client.images.pull(container_image)
      File "/usr/local/lib/python3.10/site-packages/docker/models/images.py", line 465, in pull
        pull_log = self.client.api.pull(
      File "/usr/local/lib/python3.10/site-packages/docker/api/image.py", line 429, in pull
        self._raise_for_status(response)
      File "/usr/local/lib/python3.10/site-packages/docker/api/client.py", line 270, in _raise_for_status
        raise create_api_error_from_http_exception(e) from e
      File "/usr/local/lib/python3.10/site-packages/docker/errors.py", line 39, in create_api_error_from_http_exception
        raise cls(e, response=response, explanation=explanation) from e
    docker.errors.ImageNotFound: 404 Client Error for http+docker://localhost/v1.41/images/create?tag=latest&fromImage=diran%2Falpinehelloworld: Not Found ("pull access denied for diran/alpinehelloworld, repository does not exist or may require 'docker login': denied: requested access to the resource is denied")
    10.0.0.2 - - [08/Jan/2023 09:45:12] "POST /prod HTTP/1.1" 500 -
**ERROR** : *docker.errors.ImageNotFound: 404 Client Error for http+docker://localhost/v1.41/images/create?tag=latest&fromImage=diran%2Falpinehelloworld: Not Found ("pull access denied for diran/alpinehelloworld, repository does not exist or may require 'docker login': denied: requested access to the resource is denied")*

So i can review my request and fix image name
