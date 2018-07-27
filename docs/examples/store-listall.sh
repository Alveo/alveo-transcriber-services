#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au/alveo
#
# Attempts to authenticate and retrieve a list of objects
#  matching the specified object key.
#
# This will return a list of object IDs of anything that
#  matches your query.
#
# Example usage:
#   sh store-listall.sh alveo-120841
key=$1

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
$ATS_URL/datastore/listall/$key
