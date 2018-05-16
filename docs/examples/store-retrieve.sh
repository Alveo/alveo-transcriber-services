#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au

# Attempts to authenticate and retrieve a stored object
# Example usage:
#   sh store-retrieve.sh store_id
id=$1

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
$ATS_URL/datastore/?store_id=$id
