from bs4 import BeautifulSoup
import plotly.graph_objects as go
from svgpathtools import parse_path
import numpy as np


def extractShapesFromSVG(location,parts):
    """Extracts all shapes from an svg file

    Inputs:
        @param: location: relative location of svg file
        @param: parts: list of names of defined parts that map to shapes (should be in order of values that correspond to color strength
        of each shape) Additionally the list of names must be the same as the list of named polygons on the svg file

    Returns:
        @param: elements: list of lists, each list is the ordered vertices in each polygon, each vertex
        is supplied as an index corresponding to the location of the vertex in points
        @param: points: List of (x,y) of each point
        @param: path_elements - list of raw path data from the svg for all shapes
        @param: partMappings - mapping of each shape to its  part (value is -1 if it is just a line)
        """
    
    # Load the SVG content
    with open(location, 'r') as file:
        svg_content = file.read()

    # Create a BeautifulSoup object and specify the lxml parser
    soup = BeautifulSoup(svg_content, 'html.parser')

    # Find all the path elements
    path_elements = soup.find_all('path')






    # Initialize lists for points and elements
    points = [] # holds all points
    elements = [] # holds each polygon

    # Function to add a point if it's not already in the list and return its index
    def add_point(point):
        if point not in points:
            points.append(point)
        return points.index(point)
    print(path_elements[0])
    partMappings = []
    # describes which polygon each rigid body is responsible, -1 indicates it is just a line

    # Iterate through each path (polygon) and update points / elements
    for pathRawData in path_elements:
        path_string = str(parse_path(pathRawData))
        truthList = [parts[i] in path_string for i in range(0,len(parts))]
        try:
            partMappings.append( truthList.index(1) )
        except:
            partMappings.append( -1 )
        
        path_data = parse_path(pathRawData.get('d'))
        # Iterate through each line in the path
        element_ =  []
        for i,line in enumerate(path_data):
            # Extract start and end points 
            start_point = (line.start.real, -line.start.imag)
            
            end_point = (line.end.real, -line.end.imag)

            # Get indices of start and end points
            start_index = add_point(start_point)
            if i == 0:
                element_.append(start_index)
            end_index = add_point(end_point)

            # Add element as indices of points
            element_.append(end_index)
        elements.append(element_)

    return elements, points, path_elements,partMappings



def drawObject(points,elements,colors,partMapping,savePath = "Composite image.png",lineColor = '#000000' ):
    """
    This function draws the polygons passed in elements to the screen
    requires import plotly.graph_objects as go
    and from bs4 import BeautifulSoup


    Inputs:
        @param points: list of all points (x,y) that polygon vertices form at
        @param elements: List of lists corresponding to list of vertices in each polygon, each vertex entry should be the index of the vertex from the list points 
        @param colors: List of colors for all defined shapes ( not including lines)
        @param partMapping: pointer to map each polygon to each color, if not a defined shape, the value is -1
        @param (optional) savePath: saves composite image color coded map to savePath location
        @param (optional) lineColor: color of any non defined shapes (lines) set as black
    """
    nodes=np.asarray(points).transpose()
    shapeIdx = 0
    polygons= []
    

    for i, element in enumerate(elements):
        if partMapping[i] != -1:
            # Fill shape
            colorIdx = partMapping[i]
            fillcolor = colors[colorIdx]
            shapeIdx += 1
        else:
            # Fill line
            fillcolor = lineColor

        polygons.append(go.Scatter(x=nodes[0][element],y=nodes[1][element],
            mode='lines',line=dict(color=lineColor, width=2), fill='toself',fillcolor=fillcolor))
        
    # Now plot data
        
    axis = dict(showline=False, zeroline=False, showgrid = False,ticks='', showticklabels=False)

    fig = go.Figure(polygons)

    fig.update_layout(width=600, height=900, showlegend=False,xaxis=axis, yaxis=axis,template="none")    
    fig.write_image(savePath)

def get_color_hex(value, light_color, dark_color):
    """Function returns hexadecimal color based on value between 0 and 1."""
    # Check value is bounded first
    value = max(0, min(1, value))

    # Interpolate between light and dark colors
    r = int(light_color[0] + value * (dark_color[0] - light_color[0]))
    g = int(light_color[1] + value * (dark_color[1] - light_color[1]))
    b = int(light_color[2] + value * (dark_color[2] - light_color[2]))

    # Return as hexadecimal
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    





