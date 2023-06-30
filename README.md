# Findner
This is a back end project that works with `Partner`s; creating, loading, and finding their nearest given a coordinations.
It uses FastAPI and PostgreSQL.

Find + Partner -> 🔥Findner🔥 (I know it sounds like a dating app... But it's not...)

# Installation
0. Open your terminal (I used `bash`)
1. Clone the project
```
git clone https://github.com/sananqsh/Findner.git
```
3. Change directory to the project root
```
cd Findner
```
5. Run docker-compose (see [this](https://docs.docker.com/engine/install/) and [this](https://docs.docker.com.zh.xy2401.com/v17.12/compose/install/) if not installed)
> The `--build` is only for first time docker-composing.
```
docker-compose up -d --build
```
6. You can call APIs from your local!
See the `/docs` route for Swagger documentations of APIs (for example if the project is on local: `http://127.0.0.1:8000/docs`)

# Tests
*Under construction*

# Deployment
The `docker-compose.yml` is provided in a way that we can deploy a new version of the web application without downtime.

> There are other ways to achieve zero-downtime deployment, including the use of `Docker Swarm` or `Kubernetes`. However, these methods can be complex and may require additional resources.

The docker-compose creates two instances of the web app with a load balancer (NGINX) in front of them (the number of instances can increase based on our need).

A new version of the application could be deployed to one instance at a time, ensuring that at least one instance is always available to handle incoming requests.
My approach for introducing new version of the code is to build the application's Docker image with the new version of the code, 
then use `docker-compose up --no-deps --build web1` to update `web1` and `docker-compose up --no-deps --build web2` to update `web2`, ensuring that at least one of them is always running.
