#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au

# Attempts to authenticate and retrieve a summary of stored data with
#  the given key, from all users in thhe domain.

# Example usage:
#   sh retrieve-store-all.sh
key=$1

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
  $ATS_URL/userstore/all?storage_key=$key
