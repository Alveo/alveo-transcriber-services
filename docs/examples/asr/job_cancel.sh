#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au/alveo
#
# Attempts to authenticate and cancel the specified job.
# Example usage:
#   ./job_cancel.sh <job_number>
#   ./job_cancel.sh 5302

job_id=$1

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
  $ATS_URL/asr/jobs/cancel?job_id=job_id
