#!/bin/bash
# Set environment variables for:
#  ATS_API_DOMAIN, e.g app.alveo.edu.au
#  ATS_API_KEY, e.g a valid Alveo API key
#  ATS_URL, e.g https://segmenter.apps.alveo.edu.au

# Attempts to authenticate and store some data
# Example usage:
#   sh store-key.sh

curl \
  --header "X-Api-Domain: $ATS_API_DOMAIN" \
  --header "X-Api-Key: $ATS_API_KEY" \
  -d '
  {
    "key": "test-transcription2",
    "value": [
      {
        "start": 1.00,
        "end": 3.71,
        "annotation": "Example"
      },
      {
        "start": 5.21,
        "end": 8.33,
        "speaker": "B",
        "annotation": "Example 2"
      }
    ]
  }
  ' \
  -H "Content-Type: application/json" \
  -X POST \
  $ATS_URL/datastore/
