# Staple Internal Storage Server



For some on-premise deployments, Staple is offering in-cluster storage as an alternative to S3. This is implemented by storing the documents in a PostgreSQL database, with a thin server layer for our other applications to interact with. 

This codebase is responsible for:

1. Database setup.
2. Interactive server layer.

To see how to connect from the client side, please refer to [this walkthrough](https://hebehh.github.io/things/2021/02/01/ClusterStorage/).



#### Techstack:

* `python3` - primary language
* `sqlalchemy` - database ORM (database is PostgreSQL)
* `flask` - server web framework
* `docker` - build, run and deploy
* `makefile` - abstract some of the more complicated commands (only verified for Mac)



#### Build Docker Image:

The same image is used for both setup and server. This can be created with either of:

* `make build` , or
* `docker build -t storage .`



### Environment Variables:

You will need an `env/` folder containing `env/staging_env` in the same directory as this README to run any of the images on local. Please ask @Hebe Hilhorst for this. Update the contents with whichever database you want to run this against.



## Database Structure

There are two tables, with ORM representation:

* `documents`/`Structure` - the filesystem structure, contains both folder and file elements
  * `folder`: folder the element is in
  * `name`: name of the element
  * `kind`: is a `folder` or a `file`?
  * `blob_id`: if is `file`, link to `Blob`
*  `blobs`/`Blob` -  the file contents
  * `id`: for reference by associated `Structures`
  * `kind`: type of document, eg `JPEG`. 
  * `hashval`: hash of document
  * `blob`: binary blob of document

The name, location and other metadata info of filesystem elements are stored as a `Structure` in the `documents` database. Actual files are then stored as a `Blob` in the `blobs` database.

Notably, the `hashval` is used to ensure each file is only stored once, even if it exists in many parts of the filesystem structure.





## Database Setup

The files responsible for setting up the database are, in order of reverse dependency:

1. `Server/Code/db_classes.py`: defines the tables to be built
2. `Server/Code/generate_db.py`: connect to database and create all from (1)
3.  `Server/db_migration.py`: run (2) and then create root folder



#### Running Image

To run the Docker image in database setup mode, please use any of:

* `make migrate_db`, or

* ```bash
  docker run -it --rm \
  	--env-file $PWD/env/staging_env/config.env \
  	--env-file $PWD/env/staging_env/urls.env \
  	--env-file $PWD/env/staging_env/secrets.env \
  	--name storage \
  	storage python3 db_migration.py
  ```

* (Windows: ) 
  ```bash
  docker run -it --rm \
  	--env-file %cd%/env/staging_env/config.env \
  	--env-file %cd%/env/staging_env/urls.env \
  	--env-file %cd%/env/staging_env/secrets.env \
  	--name storage \
  	storage python3 db_migration.py
  ```
  





## Server

The files responsible for running the server are, in order of reverse dependency:

1. `Server/Code/db_classes.py`: defines the object representation mapping of the tables
2. `Server/Code/interaction.py`: database interaction functions to provide capability to insert, retreive and delete files and  folders from the database representation.
3. `Server/Code/routes.py`: retreive paramaters from incoming requests and pass them to (2). Error catching and wrapping.
4. `Server/server.py`: flask skin of (3)



#### Running Server

To run the Docker image in database setup mode, please use any of:

* `make run`, or

* ```bash
  docker run -it --rm \
  	--env-file $PWD/env/staging_env/config.env \
  	--env-file $PWD/env/staging_env/urls.env \
  	--env-file $PWD/env/staging_env/secrets.env \
  	--name storage \
  	storage 
  ```

* (Windows: ) 

  ```bash
  docker run -it --rm \
  	--env-file %cd%/env/staging_env/config.env \
  	--env-file %cd%/env/staging_env/urls.env \
  	--env-file %cd%/env/staging_env/secrets.env \
  	--name storage \
  	storage
  ```





