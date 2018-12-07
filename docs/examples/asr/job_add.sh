#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au/alveo

# Attempts to authenticate and queue an ASR job for an Alveo URL.
# Example usage:
#   ./job_add.sh https://app.alveo.edu.au/catalog/austalk/1_1274_2_7_001/document/1_1274_2_7_001-ch6-speaker16.wav
# Returns job ID if successful.

url=$1

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
  $ATS_URL/asr/jobs/add?remote_url=$url
