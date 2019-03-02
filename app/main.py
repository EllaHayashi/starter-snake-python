import json
import os
import random
import bottle
import numpy as np
import math

from api import ping_response, start_response, move_response, end_response

# A Star Implementation from: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
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

#Returns the maze filled with zeros
def returnMaze(data):
    boardx = data['board']['height']
    boardy = data['board']['width']
    maze = np.zeros((boardx,boardy),dtype=int)
    return maze

#Gives the (int) x and y position of our OWN snake in two lists (x, y)
def getSelfPos(data):
    snake = data['you']['body']
    x = [snakePos['x'] for snakePos in snake]
    y = [snakePos['y'] for snakePos in snake]
    return x,y

# return the current head postion of OWN snake in (int) as a tuple
def getSelfHeadPos(data):
    xself,yself = getSelfPos(data)
    x = xself[0]
    y = yself[0]
    return (x,y)

#Gives the (int) x and y position of all enemies in a two lists (xx, yy)
def enemyAllPos(data):
    numEnemies = enemyCount(data)
    xx = [] #initializing
    yy = [] #initializing
    #looping to find an appended list of x and y coordinates of all enemy snakes
    
    
    
    for s in range(numEnemies):
        x,y = enemy1Pos(data,s)
        xx += x
        yy += y
        
#    for i in len(numEnemies):
#        snakeHead = data['board']['snakes'][i][0]

    
    return xx,yy

def determineNextCoordinate(direction, Head):
    newDirectionX = Head[0]
    newDirectionY = Head[1]
    if direction == 'right':    
       newDirectionX += 1	
    if direction == 'left':    
       newDirectionX -= 1   
    if direction == 'up':    
       newDirectionY -=1 
    if direction == 'down':    
       newDirectionY += 1
    return (newDirectionX, newDirectionY)
	
	
def enemyCoordinate(coordinate, data):
    for i in range(len(data['board']['snakes'])):
        for j in range(len(data['board']['snakes'][i]['body'])):
            enemyCoord = data['board']['snakes'][i]['body'][j]
            if(coordinate[0] == enemyCoord[0] and coordinate[1] == enemyCoord[1]):
               return true
               
    return false
    
def ourCoordinate(coordinate, data):
    for i in range(len(data['you']['body'])):
        bodyCoord = data['you']['body'][i][0]
        if(coordinate[0] == bodyCoord[0] and coordinate[1] == bodyCoord[1]):
            return true
               
    return false
	
def directionValid(newDirection, data):
	
	#not a wall
    if(newDirection[0]<0 or newDirection[0]>=data['board']['width']):
        return false
    elif(newDirection[1]<0 or newDirection[1]>=data['board']['height']):
        return false
	
	
	#not a snake
    elif enemyCoordinate(newDirection, data) is true:
        return false
	
	
	#not its body
    elif ourCoordinate(newDirection, data) is true:
        return false
	
	#not future snake


def directionFromCoordinate(coordinate, Head):
    Headx = Head[0]
    Heady = Head[1]
    direction = ''
    
    if coordinate[0] == Headx + 1:
       direction = 'right'
    elif coordinate[0] == Headx - 1:
       direction = 'left'
    elif coordinate[1] == Heady + 1:
       direction = 'down'
    elif coordinate[1] == Heady - 1:
       direction = 'up'
    
    return direction
    
#Gives the x,y as a list of int values of the a snake given 'numSnake' which starts at 0  
def enemy1Pos(data,numSnake):
    snake = data['board']['snakes'][numSnake]['body']
    x = [snakePos['x'] for snakePos in snake]
    y = [snakePos['y'] for snakePos in snake]
    return x,y
    
#Gives the number of enemies still alive
def enemyCount(data):
    numEnemies = sum(1 for enemies in data['board']['snakes'])
    return numEnemies

#Finding location of fruits
def fruitLoc(data):
    snake = data['board']['food']
    x = [snakePos['x'] for snakePos in snake]
    y = [snakePos['y'] for snakePos in snake]
    return x,y
    
#Finding nearest fruit to head. Returns position as a tuple (int) x,y
def closestFruit(data):
    fx,fy = fruitLoc(data) #getting x,y of all fruits
    hx,hy = getSelfHeadPos(data) #getting position of head
    distx = np.array(fx) - hx
    disty = np.array(fy) - hy
    distx *= distx #calculating the square
    disty *= disty #calculating the square
    dist = distx+disty #calculating distance (without taking sqrt)
    indexMin = np.argmin(dist) #checked: only returns one index which is good
    
    print("Closest fruit")
    print(str(fx[indexMin]) + " " + str(fy[indexMin]))
    
    return (fx[indexMin],fy[indexMin])
    
 #provides the string direction: 'up','down','left','right' from the path
def returnDirection(path):
    arrayDirection = np.subtract(path[1],path[0])
    
    if (arrayDirection== ([0,-1])).all():
        direction = 'up'
    elif (arrayDirection== ([0,1])).all():
        direction = 'down'
    elif (arrayDirection== ([-1,0])).all():
        direction = 'left'
    elif (arrayDirection== ([1,0])).all():
        direction = 'right'
    else:
        direction = 'right'
    return direction   
    
#A* Algorithm
def astar(maze, start, end, data):
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
    i=0
    # Loop until you find the end
    while len(open_list) > 0:
 #       i=i+1
  #      if i>200:
  #      	break
#        else:
 #           print(str(len(open_list)))
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
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        
        
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
			
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            #if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

			# Make sure not enemy snake
            enemyXLoc, enemyYLoc = enemyAllPos(data)
            if node_position[0] not in enemyXLoc and node_position[1] not in enemyYLoc:
                continue
			
#            if node_position[0]>-1 and node_position[0]<len(maze) or node_position[1]>-1 and node_position[1]<len(maze):
#                continue


            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

			# See if found another food node
			


            # Create new node
            new_node = Node(current_node, node_position)
#            print("**********")
 #           print(str(node_position[0]) + " " + str(node_position[1]))
            # Append
            children.append(new_node)

        # Loop through children
        
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


from api import ping_response, start_response, move_response, end_response



# A Star Implementation from: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
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

    
#A* Algorithm    
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
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
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
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
    
    
    
#Returns the maze filled with zeros
def returnMaze(data):
    boardx = data['board']['height']
    boardy = data['board']['width']
    maze = np.zeros((boardx,boardy),dtype=int)
    return maze

#Gives the (int) x and y position of our OWN snake in two lists (x, y)
def getSelfPos(data):
    snake = data['you']['body']
    x = [snakePos['x'] for snakePos in snake]
    y = [snakePos['y'] for snakePos in snake]
    return x,y

# return the current head postion of OWN snake in (int) as a tuple
def getSelfHeadPos(data):
    xself,yself = getSelfPos(data)
    x = xself[0]
    y = yself[0]
    return (x,y)

#Gives the entire position of snakes 
def enemyAllPos(data):
    numEnemies = enemyCount(data)
    xx = [] #initializing
    yy = [] #initializing
    if numEnemies > 0:
        #looping to find an appended list of x and y coordinates of all enemy snakes
        for s in range(numEnemies):
            x,y = enemy1Pos(data,s+1)
            xx += x
            yy += y
    return xx,yy

#Gives the x,y as a list of int values of the a snake given 'numSnake' which starts at 0  
def enemy1Pos(data,numSnake):
    snake = data['board']['snakes'][numSnake]['body']
    x = [snakePos['x'] for snakePos in snake]
    y = [snakePos['y'] for snakePos in snake]
    return x,y

#Gives the position of surrounding position of enemies heads and their potential 'next step'
def enemySurroundHeadPos(data):
    numEnemies = enemyCount(data)
    xx = [] #initializing
    yy = [] #initializing
    direction_x = [0, 0, -1, 1] # referring to up, down, left, right
    direction_y = [-1, 1, 0, 0] # referring to up, down, left, right
    
    if numEnemies > 0:
        #looping to find the 4 locations surrounding the head
        for s in range(numEnemies+1):
            x,y = enemy1Pos(data,s)
        
            headx = x[0]
            heady = y[0]
#            print('head of enemy')
#            print((headx,heady))
#            print('head of  own')
#            print(getSelfHeadPos(data))
            if not((headx,heady) == getSelfHeadPos(data)):
#                print('got that the heads are different')
                #looping through the directions
                for rr in range(4):
                    dir = [(headx)+direction_x[rr],(heady+direction_y[rr])] #find the 4 locations an enemie's head can move into in the next step
                    if (int(dir[0]) in range(0,(data['board']['height']-1)) and int(dir[1]) in range(0,(data['board']['width']-1))): #making sure the ranges are not out of bounds for x or y
                        xx+= [dir[0]]
                        yy+= [dir[1]]
    
#    print('surrounding head:')
#    print(xx,yy)
    return xx,yy

#Gives the number of enemies still alive
def enemyCount(data):
    numEnemies = sum(1 for enemies in data['board']['snakes']) -1 # minus one because the board counts itself in "snakes"
    return numEnemies

#Finding location of fruits
def fruitLoc(data):
    snake = data['board']['food']
    x = [snakePos['x'] for snakePos in snake]
    y = [snakePos['y'] for snakePos in snake]
    return x,y

#Finding nearest fruit to head. Returns position as a tuple (int) x,y
def closestFruit(data):
    fx,fy = fruitLoc(data) #getting x,y of all fruits
    hx,hy = getSelfHeadPos(data) #getting position of head
    distx = np.array(fx) - hx
    disty = np.array(fy) - hy
    distx *= distx #calculating the square
    disty *= disty #calculating the square
    dist = distx+disty #calculating distance (without taking sqrt)
    indexMin = np.argmin(dist) #checked: only returns one index which is good
    return (fx[indexMin],fy[indexMin])

#provides the string direction: 'up','down','left','right' from the path
def returnDirection(path):
    arrayDirection = np.subtract(path[1],path[0])
    if (arrayDirection == ([0,-1])).all():
        direction = 'up'
    elif (arrayDirection == ([0,1])).all():
        direction = 'down'
    elif (arrayDirection == ([-1,0])).all():
        direction = 'left'
    elif (arrayDirection == ([1,0])).all():
        direction = 'right'
    else:
        direction = 'right'
        print('random direction chosen!')
    return direction 
>>>>>>> 8ddeffa6f5904453b94dfc497b9287a638833910


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json
    print(" ")
    print("---------------------")
    print("New Game")
    print(data)
    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
#    print(json.dumps(data))

    # Obtaining board height and width!
    boardx = data['board']['height'] 
    boardy = data['board']['width']
    print(boardx)
    print(boardy)


    color = "#00FF00"

    return start_response(color)


#def getBoardWidth(data)
#	return data['board']['width']

#def getBoardHeight(data)
#	return data['board']['height']


@bottle.post('/move')
def move():
    data = bottle.request.json
    print(" ")
    print("Next Step:")
    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    #print(data)
    #print(data['board']['food'])
    print('--')
    numEnemies = enemyCount(data)
    print(numEnemies)
    print(data['you'])
    
    

    directions = ['up', 'down', 'left', 'right']
    
    #obtaining 'maze' for astar
    maze = returnMaze(data) #obtaining maze (size)
    

    enemyXLoc, enemyYLoc = enemyAllPos(data) #obtaing locations of enemies on maze
    ownXLoc, ownYLoc = getSelfPos(data) #obtaining own snake location on maze
    maze[enemyXLoc, enemyYLoc] = 1 #marking locations of other snakes on maze
    maze[ownXLoc, ownYLoc] = 1 #marking self location on maze
    

  
    #obtaining 'start' for astar 
    start = getSelfHeadPos(data) #using current head location as 'start'
    

    #obtaining 'end' for astar 
    end = closestFruit(data)
    

    #calculating astar for the shortest path
    path = astar(maze, start, end, data)
    print('path:')
    print(path)
    
    

    
    #determining direction
    direction = (returnDirection(path))
    
    #find out cordonate of next direction 
#    newDirection = determineNextCoordinate(direction, getSelfHeadPos(data))  
    
    
    
    print('direction:')
    
    print(direction)
    
    return move_response(direction)
    
    #determine weather or now the new Direction is valid
"""    
    if directionValid(newDirection, data) is true:
    
        print("it was valid af")
        return move_response(direction)
=======

@bottle.post('/move')
def move():
    data = bottle.request.json
    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
#    print('--')
    numEnemies = enemyCount(data)
    #print(numEnemies)
#    print(data['turn'])
    

    #obtaining 'maze' for astar
    maze = returnMaze(data) #obtaining maze (size)
    
    enemyXLoc, enemyYLoc = enemyAllPos(data) #obtaing locations of enemies on maze
    ownXLoc, ownYLoc = getSelfPos(data) #obtaining own snake location on maze
    enemyHeadMoveX, enemyHeadMoveY = enemySurroundHeadPos(data) #obtaining locations of the potential location of future enemy heads 
#    print('enemy head 4 locss')
    print(enemyHeadMoveX, enemyHeadMoveY)
    
    maze[enemyXLoc, enemyYLoc] = 1 #marking locations of other snakes on maze
    maze[ownXLoc, ownYLoc] = 1 #marking self location on maze
    maze[enemyHeadMoveX, enemyHeadMoveY] = 1 #marking locations of potential enemy sneakhead movements on maze

    #obtaining 'start' for astar 
    start = getSelfHeadPos(data) #using current head location as 'start'
#    print(start)
    
    #obtaining 'end' for astar 
    end = closestFruit(data)
#    print(end)
    
    #calculating astar for the shortest path
    path = astar(maze, start, end)
#    print('path:')
#    print(path)
    
    #determining direction
    direction = (returnDirection(path))
#    print('direction:')
#    print(direction)
#    print(data)
    
    return move_response(direction)
>>>>>>> 8ddeffa6f5904453b94dfc497b9287a638833910

    else:
        print("it was not valid boo")
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
        	# Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if directionValid(node_position, data) is true:
    			direction2 = directionFromCoordinate(node_position, getSelfHeadPos(data))
    			return move_response(direction2)
    		
    
        #pick a clear direction
"""
#     return move_response(direction)   
    

@bottle.post('/end')
def end():
    data = bottle.request.json

    print(data)


    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
#    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
   

