# alveo-transcriber-services
Repository to provide additional services to the alveo-transcriber webapp. Provides transcription storage and audio segmentation.

## Config
1. Copy `config-sample` to `config` and edit it accordingly
2. If deploying this outside of a local address, you will need to generate an SSL certificate to avoid mixed content browser errors
3. Build the transcriber with an `environment.ts` that points towards this as the `ALVEO_SERVICES_URL` 

## Running
1. Install requirements with pip, recommended you use a python virtual environment
2. Optionally enable debug `export FLASK_DEBUG=1`
3. Optionally rebuild database `python utility.py init_db`
4. `export FLASK_APP=application && python -m flask run`

## Unit tests
1. Make sure requirements installed and config file set (see above)
2. `export ALVEO_API_KEY=<YOUR ALVEO API KEY>` must be valid to test authentication
3. `python tests.py`
