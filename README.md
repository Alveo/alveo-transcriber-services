# alveo-transcriber-services
Repository to provide additional services to the alveo-transcriber web application. Provides transcription storage and automatic audio segmentation.

## Config
1. Copy `config-sample` to `config` and edit it accordingly
2. If deploying this outside of a local address, you will need to generate an SSL certificate to avoid mixed content browser errors
3. Build the transcriber with an `environment.ts` that points towards this as the `ALVEO_SERVICES_URL` 

## Running
1. Install requirements with pip, recommended you use a python virtual environment
2. Optionally enable debug `export FLASK_DEBUG=1`
3. If not done so already, build database `python utility.py init_db`
4. `export FLASK_APP=application && python -m flask run`

## Unit tests
1. The unit tests are currently done through the Alveo API. Make sure requirements installed and config file set (see above)
2. `export ALVEO_API_KEY=<YOUR ALVEO API KEY>` must be valid to test authentication
3. `python tests.py`

## Example usage
### Segment a remote URL
```bash
$ curl https://localhost:5000/segment?remote_url=https://<URI to file> \
  --header "X-Api-Domain: <handler to use e.g alveo >" \
  --header "X-Api-Key: <api key for remote auth>"
```

### Transcribe via a POST
```bash
$ curl -F "file=@test.wav" https://localhost:5000/segment \
  --header "X-Api-Domain: <handler to use e.g alveo >" \
  --header "X-Api-Key: <api key for remote auth, remote auth required even for POST>"
```

### Store data
```bash
$ curl \
  --header "X-Api-Domain: domain" \
  --header "X-Api-Key: apikey" \
  -d '
  {
    "storage_key": "example",
    "storage_value": [
      {
        "start": "0",
        "end": "3.22",
        "text": "This is an example"
      },
      {
        "start": "5.3",
        "end": "11.71",
        "text": "Of how to store some data"
      },
    ]
  }
  ' \
  -H "Content-Type: application/json" \
  -X POST https://localhost:5000/storage
```

### Retrieve data
``` bash
$ curl \
  --header "X-Api-Domain: domain" \
  --header "X-Api-Key: apikey" \
  https://localhost:5000/storage?storage_key=example
```

## Writing a module
The transcriber-services is intended to be as modular as possible. To achieve that, handlers are written for the service of your choosing. The Alveo module is included which demonstrates how to register the authentication, storage and segmentation handlers. Module integration can be set up and disabled by editing the entry in `DOMAIN_HANDLERS` in the config file. 

## Deployment with Dokku
The application is deployed using dokku, the following configuration is required on the dokku host:

```bash
$ dokku apps:create segmenter
$ dokku config:set segmenter ATS_CONFIG_PATH=../config-sample
```
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
