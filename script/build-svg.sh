#!/bin/bash

# Check if the input file is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <input-file>"
  exit 1
fi

INPUT_FILE="$1"

# Replace "gitGraph TB:" with "gitGraph LR:" and pass the result to mmdc
sed 's/gitGraph TB:/gitGraph LR:/' "$INPUT_FILE" | mmdc -i /dev/stdin -o time-diagram-presentation/time-diagram.svg