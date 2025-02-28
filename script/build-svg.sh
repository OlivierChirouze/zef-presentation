#!/bin/bash

# Replace "gitGraph TB:" with "gitGraph LR:" and pass the result to mmdc
sed 's/gitGraph TB:/gitGraph LR:/' timeline.mmd | mmdc -i /dev/stdin -o timeline-presentation/timeline.svg