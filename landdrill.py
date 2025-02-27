import cv2
import numpy as np
import networkx as nx
from random import randint
import time

# Parameters
grid_size = (10, 10)
cell_width = 50
cell_height = 50

# Load rock and grass images
rock_image = cv2.imread("C:\\Users\\Lithu\\Downloads\\driller machine\\driller machine\\rock_icon.jpg", cv2.IMREAD_UNCHANGED)  # Load rock icon with transparency
grass_image = cv2.imread("C:\\Users\\Lithu\\Downloads\\driller machine\\driller machine\\grass_icon.jpg", cv2.IMREAD_UNCHANGED)  # Load grass icon with transparency

# Resize images to fit into the grid cells
rock_image = cv2.resize(rock_image, (cell_width, cell_height))
grass_image = cv2.resize(grass_image, (cell_width, cell_height))

# Create a blank image (grid)
image = np.ones((grid_size[0] * cell_height, grid_size[1] * cell_width, 3), dtype=np.uint8) * 255

# Define colors
start_color = (0, 0, 255)  # Blue for start
goal_color = (0, 255, 0)  # Green for goal
path_color = (255, 0, 0)  # Red for the path
human_color = (255, 255, 0)  # Yellow for human icon

# Define start and end positions
start = (0, 0)  # Start at the top-left corner
goal = (grid_size[0] - 1, grid_size[1] - 1)  # Goal at the bottom-right corner

# Add rocks at random locations
rocks = set()
while len(rocks) < 25:  # Place 25 rocks randomly
    r = randint(1, grid_size[0] - 1)  # Avoid placing a rock at the start or goal
    c = randint(1, grid_size[1] - 1)
    if (r, c) != start and (r, c) != goal:  # Ensure rocks don't overlap start or goal
        rocks.add((r, c))

# Create the graph and set obstacles (rocks)
graph = nx.grid_2d_graph(grid_size[0], grid_size[1])

# Remove the rocks from the graph to set them as obstacles
for rock in rocks:
    if rock in graph:
        graph.remove_node(rock)

# Function to find the shortest path using Dijkstra's algorithm
def find_shortest_path(graph, start, goal):
    try:
        return nx.shortest_path(graph, source=start, target=goal)
    except nx.NetworkXNoPath:
        return None

# Calculate the shortest path
shortest_path = find_shortest_path(graph, start, goal)

# Function to place images of rocks and grass
def place_icons(image, rocks, grass_image, rock_image):
    for y in range(grid_size[0]):
        for x in range(grid_size[1]):
            if (y, x) in rocks:
                image[y * cell_height:(y + 1) * cell_height, x * cell_width:(x + 1) * cell_width] = rock_image[:, :, :3]  # Place rock
            else:
                image[y * cell_height:(y + 1) * cell_height, x * cell_width:(x + 1) * cell_width] = grass_image[:, :, :3]  # Place grass

# Draw start and goal
def draw_start_goal(image, start, goal):
    # Draw start and goal with icons
    cv2.putText(image, "Start", (start[1] * cell_width + 10, start[0] * cell_height + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, start_color, 2)
    cv2.putText(image, "Goal", (goal[1] * cell_width + 10, goal[0] * cell_height + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, goal_color, 2)

    # Draw human icon at goal
    cv2.circle(image, (goal[1] * cell_width + cell_width // 2, goal[0] * cell_height + cell_height // 2), 15, human_color, -1)

# Place icons for the grid
place_icons(image, rocks, grass_image, rock_image)

# Draw start and goal on the image
draw_start_goal(image, start, goal)

# Show the initial grid
cv2.imshow("Grid with Obstacles", image)
cv2.waitKey(0)

# Path Animation: animate the path
if shortest_path:
    # Start animation: Animate the path from start to goal
    for i in range(1, len(shortest_path)):
        # Copy the initial image
        animation_image = image.copy()

        # Draw the path incrementally
        start_node = shortest_path[i - 1]
        end_node = shortest_path[i]

        # Draw a line from the start node to the end node
        cv2.line(animation_image, (start_node[1] * cell_width + cell_width // 2, start_node[0] * cell_height + cell_height // 2),
                 (end_node[1] * cell_width + cell_width // 2, end_node[0] * cell_height + cell_height // 2),
                 path_color, 3)

        # Show the animated path
        cv2.imshow("Path Animation", animation_image)
        cv2.waitKey(500)  # Wait for 500 ms before showing the next step

    print("Path found:", shortest_path)
else:
    print("No path found.")

# Close windows
cv2.destroyAllWindows()
