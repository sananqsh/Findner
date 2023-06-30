# Findner
This is a back end project that works with `Partner`s; creating, loading, and finding their nearest given a coordinations.
It uses FastAPI and PostgreSQL.

Find + Partner -> 🔥Findner🔥 (I know it sounds like a dating app... But it's not...)

# Installation
0. Open your terminal (I used `bash`)
1. Clone the project
```bash
git clone https://github.com/sananqsh/Findner.git
```
3. Change directory to the project root
```bash
cd Findner
```
4. Make `.env` file (`.env` file should contain the necessary environment variables for the PostgreSQL database connection)
```bash
cp .env.example .env
```


<details>
<summary>Create PostgreSQL user and database</summary>

  
  First, you need to create a PostgreSQL user that you can use to interact with your database. You can do this from the PostgreSQL shell. The following steps are for a Linux-based system:
  
  - Log into PostgreSQL shell
  
  ```bash
  sudo -u postgres psql
  ```
  
  - Create a new PostgreSQL user
  
  ```sql
  CREATE USER yourusername WITH PASSWORD 'yourpassword';
  ```
  
  - Create a new database
  
  ```sql
  CREATE DATABASE yourdbname;
  ```
  
  - Grant privileges to your user for the new database
  
  ```sql
  GRANT ALL PRIVILEGES ON DATABASE yourdbname TO yourusername;
  ```
  
  - Optional: Sometimes PostgreSQL is configured to disallow non-superusers from creating databases or schema, and you might need to modify these configurations to suit your needs, or alter your user role to super user:
  
  ```sql
  ALTER USER yourusername WITH SUPERUSER
  
  # if you want to remove superuser privileges, you can do it with:
  # ALTER USER yourusername WITH NOSUPERUSER;
  ```
  
  - Exit the PostgreSQL shell
  
  ```sql
  \q
  ```
  
  > For the tutorial we went through, the `.env` should look like this (based on our docker-compose, the host would be *`db`*):
  ```
  DATABASE_USER=yourusername
  DATABASE_PASSWORD=yourpassword
  DATABASE_NAME=yourdbname
  DATABASE_HOST=db
  ```

</details>

<br>

5. Run docker-compose (see [this](https://docs.docker.com/engine/install/) and [this](https://docs.docker.com.zh.xy2401.com/v17.12/compose/install/) if not installed)
> The `--build` is only for first time docker-composing.
```bash
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
