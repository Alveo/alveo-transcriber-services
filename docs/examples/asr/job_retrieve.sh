#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au/alveo
#
# Attempts to authenticate and retrieve the status of a job.
#  If the job has been completed, the result will be returned too.
# Example usage:
#   ./job_retrieve.sh <job_number>
#   ./job_retrieve.sh 5302

job_id=$1

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
  $ATS_URL/asr/jobs/add?remote_url=$url
