#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au
#
# Attempts to authenticate and retrieve a list of your
#  personally stored objects.
#
# This will return a list of storage IDs of anything that
#  matches your query.
#
# You can narrow down a query by altering the URL:
#  /datastore/list/<key_id>
#  /datastore/list/<key_id>/<revision>
#
# Example usage:
#   sh store-list

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
$ATS_URL/datastore/list/
