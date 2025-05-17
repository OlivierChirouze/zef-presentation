from lxml import etree
import json
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate Sozi frames from an SVG file.")
parser.add_argument("svg_file", help="Path to the input SVG file.")
parser.add_argument("json_file", help="Path to the Sozi JSON configuration file.")
args = parser.parse_args()

# File paths
svg_file = args.svg_file
json_file = args.json_file

movement_x_layer = 16  # Movement increment in x direction

# Load the SVG file
tree = etree.parse(svg_file)
root = tree.getroot()

# Load the JSON file
with open(json_file, "r") as f:
    sozi_config = json.load(f)

# Extract <rect> elements with class="commit-label-bkg" and the following <text> elements
namespace = {"svg": "http://www.w3.org/2000/svg"}
commit_labels = [
    {
        "label": text_element.text,
        "x": float(rect_element.attrib["x"]) + float(rect_element.attrib["width"]) / 2
    }
    for rect_element in root.findall(".//svg:rect[@class='commit-label-bkg']", namespace)
    if (text_element := rect_element.getnext()) is not None and text_element.tag.endswith("text")
]

# Consider the first frame has been set manually and use it as a template
commit_labels = commit_labels[1:] # Ignore the first commit_label
sozi_config["frames"] = sozi_config["frames"][:2]  # Keep only "overview" and the first element after "overview"

# Use the first frame after "overview" as a template
first_frame = sozi_config["frames"][1]

# Initial positions
original_mask_x = first_frame["cameraStates"]["mask"]["cx"]

# Add frames for each commit label
for commit_label in commit_labels:
    label = commit_label["label"]
    x = commit_label["x"]
    # Create a new frame by copying the first frame
    new_frame = json.loads(json.dumps(first_frame))  # Deep copy of the first frame

    print(f"Adding frame for {label} at x={x}")

    # Update the frame properties
    new_frame["frameId"] = label
    new_frame["title"] = label
    new_frame["cameraStates"]["__sozi_auto__"]["cx"] += x
    new_frame["cameraStates"]["mask"]["cx"] = original_mask_x

    # Append the new frame to the frames list
    sozi_config["frames"].append(new_frame)

# Save the updated JSON file
with open(json_file, "w") as f:
    json.dump(sozi_config, f, indent=4)