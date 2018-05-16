#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au
#
# Attempts to authenticate and retrieve a list of objects
#  stored by the target user.
#
# This will return a list of storage IDs of anything that
#  matches your query.
#
# You can narrow down a query by altering the URL:
#  /datastore/user/<user_id>/list/<key_id>
#  /datastore/user/<user_id>/list/<key_id>/<revision>
#
# You can also change the URL 'list' to 'export' to receive a zip
#  that also includes all the data rather than the ID only.
#
# Example usage:
#   sh store-list
user_id=$1

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
$ATS_URL/datastore/user/$user_id/list/
