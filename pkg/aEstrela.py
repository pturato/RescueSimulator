from time import sleep


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def distance_childtocurrent(current_node,child):
    if current_node[0]!=child[0] and current_node[1]!=child[1]:
        #print(current_node, child)
        return 1.5
    return 1

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            #print("Found the goal")
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return [current_node.g, path[::-1]] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            if Node(current_node, node_position) in closed_list: 
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    break
            else:
                # Create the f, g, and h values
                child.g = current_node.g + 1
                # H: Manhattan distance to end point
                child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    # check if the new path to children is worst or equal 
                    # than one already in the open_list (by measuring g)
                    if child == open_node and child.g >= open_node.g:
                        break
                else:
                    # Add the child to the open list
                    open_list.append(child)


        # for child in children:
            
        #     # row_dif = child.position[0] - current_node.position[0]
        #     # col_dif = child.position[1] - current_node.position[1]

        #     # #não considerar as diagonais com parede
        #     # if ([child.position[0] + row_dif][current_node.position[1]] == 1 and
        #     #     [child.position[0]][current_node.position[1] + col_dif] == 1):
        #     #     continue
            
        #     #se for diagonal
            
        #     if(current_node.position[0]!=child.position[0] and current_node.position[1]!=child.position[1]):
        #         if(current_node.position[0]<child.position[0] and current_node.position[1]<child.position[1]):
        #             if(maze[current_node.position[0]+1][current_node.position[1]] == 1 and 
        #                maze[current_node.position[0]][current_node.position[1]+1] == 1):
        #                 continue
        #         elif(current_node.position[0]<child.position[0] and current_node.position[1]>child.position[1]):
        #             if(maze[current_node.position[0]+1][current_node.position[1]] == 1 and 
        #                maze[current_node.position[0]][current_node.position[1]-1] == 1):
        #                 continue
        #         elif(current_node.position[0]>child.position[0] and current_node.position[1]<child.position[1]):
        #             if(maze[current_node.position[0]-1][current_node.position[1]] == 1 and 
        #                maze[current_node.position[0]][current_node.position[1]+1] == 1):
        #                 continue
        #         elif(current_node.position[0]>child.position[0] and current_node.position[1]>child.position[1]):
        #             if(maze[current_node.position[0]-1][current_node.position[1]] == 1 and 
        #                maze[current_node.position[0]][current_node.position[1]-1] == 1):
        #                 continue

        #         #print()

        #     # Child is on the closed list
        #     for closed_child in closed_list:
        #         if child == closed_child:
        #             continue

        #     # Create the f, g, and h values
        #     child.g = current_node.g + distance_childtocurrent(current_node.position, child.position) #distance between child and current
        #     child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
        #     #print("g do filho = ",child.g)
        #     child.f = child.g + child.h

        #     # Child is already in the open list
        #     for open_node in open_list:
        #         if child == open_node and child.g > open_node.g:
        #             #print(len(open_list))
        #             #sleep(2)
        #             continue

        #     # Add the child to the open list
        #     open_list.append(child)