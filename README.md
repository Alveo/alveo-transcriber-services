# alveo-transcriber-services
Repository to provide additional services to the alveo-transcriber web application. Provides transcription storage and automatic audio segmentation.

## Config
1. If deploying this outside of a local address, you will need to generate an SSL certificate to avoid mixed content browser errors
2. Build the transcriber with an `environment.ts` that points towards this as the `ALVEO_SERVICES_URL` 

## Running
1. Install requirements with pip, recommended you use a python virtual environment
2. Optionally enable debug `export FLASK_DEBUG=1`, else you will have to set a `DATABASE_URI` environment variable (see `application/config.py`)
3. If it hasn't be generated yet, initialise the database and tables `python utility.py init_db`
4. `export FLASK_APP=application && python -m flask run`

## Unit tests
Set up environment variables for relevant modules (unconfigured ones will be skipped!)
   
When ready, run the unit tests with `python tests.py`
- Alveo: `export ALVEO_API_KEY=<YOUR ALVEO API KEY>`

## Examples
See [examples](docs/examples/).

## Writing a module
The transcriber-services is intended to be as modular as possible. To achieve that, handlers are written for the service of your choosing. The Alveo module is included which demonstrates how to register the authentication, storage and segmentation handlers. Module integration can be set up and disabled by editing the entry in `DOMAIN_HANDLERS` in the config file. 

## Deployment with Dokku
The application is deployed using dokku, the following configuration is required on the dokku host:

```bash
$ dokku apps:create segmenter
```
Be sure to set up a database so that Dokku provides the `DATABASE_URL` environment variable. Supported type are sqlite3, Postgres, MariaDB and MySQL.    
Now you can push the repository to the dokku host using git:
```bash
$ git remote add dokku dokku@apps.alveo.edu.au:segmenter
$ git push dokku master
```
You could then add and set a domain if you wanted to. You should do this before creating an SSL certificate. Here is an example:
```bash
$ dokku domains:add segmenter segmenter.apps.alveo.edu.au
$ dokku domains:set segmenter segmenter.apps.alveo.edu.au
```
This should build the environment and start the application. We then need to set up an SSL certificate
on the dokku host:
```bash
$ dokku letsencrypt segmenter
```
Finally, build the database if it hasn't been built already.
```bash
$ dokku run segmenter python utility.py init_db
```
