#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au/alveo
#
# Attempts to authenticate and download (as a zip) all stored data associated
#  to the user.
#
# You can narrow down a query by altering the URL:
#  /datastore/export/<key_id>
#  /datastore/export/<key_id>/<revision>
# 
# Exporting by a user is also possible.
#  /datastore/user/<user_id>/export/<key_id>
#  /datastore/user/<user_id>/export/<key_id>/<revision>
#
# Example usage:
#   sh store-export.sh

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
$ATS_URL/datastore/export/
