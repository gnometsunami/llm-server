#!/bin/bash

curl --request POST \
     --url http://localhost:9000/completion \
     --data '{"prompt": "What is the capitol of kazakstan?","n_predict": 128}'