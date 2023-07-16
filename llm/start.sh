#!/bin/bash
[ -z "$PERSONALITY_NAME" ] && unset PERSONALITY_NAME || echo "Personality Name: $PERSONALITY_NAME"
[ -z "$PERSONALITY_DESCRIPTION" ] && unset PERSONALITY_DESCRIPTION|| echo "Personality Description: $PERSONALITY_DESCRIPTION"
/llama/server --port 8080 --host 0.0.0.0 -ngl "$GPU_LAYERS" -m /models/"$MODEL"