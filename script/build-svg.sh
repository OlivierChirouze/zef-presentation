#!/bin/bash

# Replace "gitGraph TB:" with "gitGraph LR:" and pass the result to mmdc
sed 's/gitGraph TB:/gitGraph LR:/' timeline.mmd | mmdc -i /dev/stdin -o timeline-presentation/timeline.svg

# Clean up: remove lines that need to be removed
# Initialize variables
start_id=""
end_id=""

# Read the file line by line
while IFS= read -r line; do
  # Check for "%% remove-end" and extract the commit id
  if [[ $line == *"%% remove-end"* ]]; then
    end_id=$(echo $line | sed -n 's/.*id:"\([^"]*\)".*/\1/p')
    # Print the pair of commit ids
    echo "($start_id, $end_id)"
    # Remove the lines between the two commit ids
    python3 script/remove-line-between-commits.py timeline-presentation/timeline.svg "$start_id" "$end_id" timeline-presentation/timeline.svg
  fi

  # Check for "%% remove-start" and extract the commit id
  if [[ $line == *"%% remove-start"* ]]; then
    start_id=$(echo $line | sed -n 's/.*id:"\([^"]*\)".*/\1/p')
  fi
done < timeline.mmd