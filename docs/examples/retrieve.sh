#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au
# 
# The docuemntation below describes how the Alveo module handles this route.
#
# Attempts to authenticate and query the backend for data.
#  Either (or both) the storage_key or user_id must be provided
# 
# `user_id` can be `self` as a shortcut if you don't know your user_id
#  It will get matched to the authenticated user.
#
# If storage_key is null, a list of all matches for the user_id will be
#  returned.
#
# If download_type is zip, a zip archive will be returned including the data
#  of every value found.
#
# If there is more than one result, only a list will be returned summarizing them.
# No data will be returned if there is more than one
#
# Example usage:
#   sh retrieve-store.sh transcription1 self
#   sh retrieve-store.sh transcription1 449
#   sh retrieve-store.sh transcription1 449 zip
#
if [ ! -z "$1"]
then
storage_key="storage_key=$1"
fi
if [ ! -z "$2"]
then
  user_id="user_id=$2"
fi
if [ ! -z "$3"]
then
download_type="download_type=$3"
fi

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
  $ATS_URL/storage?"$storage_key&$user_id&$download_type"
