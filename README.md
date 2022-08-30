# Why EAZYLABS ?

Hello world !

[After Heroku being acquired by salesforce, the free offer is not more available](https://blog.heroku.com/next-chapter). This will take effect on November 28, 2022.

unfortunately our gitlab-ci and jenkins courses were based on the Dynos offer that enable us to deploy container and host them (550-1,000 dyno hours per month).

we haven't found a credible alternative as easy as heroku that provide us a container hosting for free. We decide to build a very simple tool that help our student to deploy container through pipeline using simple curl (POST) request.

So our student can provision temporary infrastructure and use them as infrastructure deployment more easily than ever.

## Prerequisites
To use the application you need a ***virtual machine*** (`in the cloud, on-prem, in play-with-docker, in killercoda`) with ***docker installed***
**Caution**: This API must not be used in production invironment
## Installation
### From Scratch
Make sure that
 - **python3** and **pip3** are alredy installed on your virtual machine
 - your **current user** have sufficient permisison to run docker command

Ensure that 
If you want to deploy the API directly on the VM host please run the following commands

    git clone https://github.com/diranetafen/eazylabs.git
    cd eazylabs
    pip3  install  -r  requirements.txt
   
   And then you can run the API 

       python3 src/main.py

Something like this will be shown

![image](https://user-images.githubusercontent.com/18481009/187277175-d8604dfe-e5fa-457c-a9b1-92fa711e705e.png)


### Using docker (also easy to install)
#### Use Eazytraining Image
A docker image is available on [eazytraining/eazylabs](https://hub.docker.com/repository/docker/eazytraining/eazylabs). You can use it directly by running this command for example : 
    
    docker run -d --name eazylabs --privileged -v /var/run/docker.sock:/var/run/docker.sock -p 1993:1993 eazytraining/eazylabs:v1.0.0
    
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

The follwing command will deploy nginx image in staging environnement

    curl -X POST http://< server address>:1993/staging -H 'Content-Type: application/json' -d '{"your_name":"dirane","container_image":"nginx", "external_port":"80", "internal_port":"80"}'
    
The follwing command will deploy dirane/alpinehelloworld image in production environnement

    curl -X POST http://< server address>:1993/prod -H 'Content-Type: application/json' -d '{"your_name":"dirane","container_image":"dirane/alpinehelloworld", "external_port":"80", "internal_port":"5000"}'

### Some rules

 - The API can be used to deploy multiple container on the same docker host but ensure that you provide different **your_name** and **external_port** parameters
 - to simulate prod and staging env, you can create another VM or directly the same host (used for prod deployment). If you use the same host for both deployment, provide a different **external_port** but the **your_name** can be the same for production and staging env
 
### Temporary infrastructure
If you are using temporary infrastructure like [killercoda](https://killercoda.com/), [play with docker](https://labs.play-with-docker.com/) or [play with eazytraining](http://docker.labs.eazytraining.fr/) don't forget that the port is content in the URL.

**Example For the API URL:**

http://ip10-0-1-3-cc6f19ssrdn0fvnms2og-***1993***.direct.docker.labs.eazytraining.fr/

**Example For App deployed with external_port = 80:**

http://ip10-0-1-4-cc6f19ssrdn0fvnms2og-***80***.direct.docker.labs.eazytraining.fr/