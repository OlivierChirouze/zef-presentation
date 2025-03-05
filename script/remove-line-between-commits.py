import xml.etree.ElementTree as ET
import sys
import math

def get_circle_coordinates(circle):
    cx = float(circle.get('cx'))
    cy = float(circle.get('cy'))
    return cx, cy

def is_within_distance(x1, y1, x2, y2, distance):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) <= distance

def find_parent(root, child):
    for parent in root.iter():
        if child in parent:
            return parent
    return None

def remove_path_between_circles(svg_file, required_class1, required_class2, output_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Register the SVG namespace with an empty prefix
    ET.register_namespace('', "http://www.w3.org/2000/svg")

    # Find the two circles based on their class attribute patterns
    circles = root.findall(".//{http://www.w3.org/2000/svg}circle[@class]")
    circle1 = None
    circle2 = None

    for circle in circles:
        classes = circle.get('class')
        if required_class1 in classes:
            circle1 = circle
        if required_class2 in classes:
            circle2 = circle

    if circle1 is None or circle2 is None:
        print(f"Circles with classes containing '{required_class1}' and '{required_class2}' not found.")
        return

    # Get the coordinates of the circles
    cx1, cy1 = get_circle_coordinates(circle1)
    cx2, cy2 = get_circle_coordinates(circle2)

    # Find the path element that goes from one circle to the other based on coordinates
    paths = root.findall(".//{http://www.w3.org/2000/svg}path")
    path_to_remove = None

    for path in paths:
        d = path.get('d')
        coords = d.split()

        x1, y1 = map(float, coords[1:3])
        x2, y2 = map(float, coords[4:6])

        if (is_within_distance(cx1, cy1, x1, y1, 5) and is_within_distance(cx2, cy2, x2, y2, 5)) or \
           (is_within_distance(cx1, cy1, x2, y2, 5) and is_within_distance(cx2, cy2, x1, y1, 5)):
            path_to_remove = path
            break

    if path_to_remove is not None:
        parent = find_parent(root, path_to_remove)
        if parent is not None:
            parent.remove(path_to_remove)
            tree.write(output_file)
            print(f"Path removed and saved to {output_file}")
        else:
            print("Parent of the path to remove not found.")
    else:
        print("Path not found.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python remove-line-between-commits.py <svg_file> <required_class1> <required_class2> <output_file>")
    else:
        svg_file = sys.argv[1]
        required_class1 = sys.argv[2]
        required_class2 = sys.argv[3]
        output_file = sys.argv[4]
        remove_path_between_circles(svg_file, required_class1, required_class2, output_file)