import xml.etree.ElementTree as ET
import sys

def inject_rect_with_gradient(svg_file, output_file):
    # Parse the SVG file
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Register the SVG namespace
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    ET.register_namespace('inkscape', "http://www.inkscape.org/namespaces/inkscape")

    # Add the inkscape namespace to the root element
    root.set('xmlns:inkscape', "http://www.inkscape.org/namespaces/inkscape")

    # Get the viewBox attribute to determine the origin
    viewbox = root.attrib.get('viewBox', '0 0 100 100').split()
    x_origin, y_origin = viewbox[0], viewbox[1]

    # Define the gradient
    defs = ET.Element('defs')
    linear_gradient = ET.SubElement(defs, 'linearGradient', {
        'id': 'gradient-opacity',
        'x1': '0%', 'y1': '0%', 'x2': '100%', 'y2': '0%'
    })
    ET.SubElement(linear_gradient, 'stop', {
        'offset': '0%', 'style': 'stop-color:white;stop-opacity:0'
    })
    ET.SubElement(linear_gradient, 'stop', {
        'offset': '2%', 'style': 'stop-color:white;stop-opacity:1'
    })
    root.append(defs)  # Add defs at the end

    # Create the <g> element
    g_element = ET.Element('g', {
        'inkscape:label': 'Mask',
        'id': 'mask',
        'inkscape:groupmode': 'layer'
    })

    # Add the rectangle inside the <g> element
    rect = ET.Element('rect', {
        'x': x_origin, 'y': y_origin,
        'width': '100%', 'height': '100%',
        'fill': 'url(#gradient-opacity)'
    })
    g_element.append(rect)

    # Append the <g> element to the root
    root.append(g_element)

    # Write the modified SVG to the output file
    tree.write(output_file)
    print(f"Injected rect with gradient inside <g> into {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add-layers.py <input_svg_file> <output_svg_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    inject_rect_with_gradient(input_file, output_file)