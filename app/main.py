import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

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

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))




    directions = ['up', 'down', 'left', 'right']
    #direction = random.choice(directions)
    boardheight = data['board']['height']
    boardwidth = data['board']['width']

    ourHead = data['you']['body'][0]
    
    rightTopCorner = ourHead['y']==0 and ourHead['x']==boardwidth-1
    origin = ourHead['y']==0 and ourHead['x']==0
    leftBottomCorner = ourHead['x']==0 and ourHead['y']==boardheight-1
    rightBottomCorner = ourHead['x']==boardwidth-1 and ourHead['y']==boardheight-1
    rightWall = ourHead['x']==boardwidth-1
    bottomWall = ourHead['y']==boardheight-1
    leftWall = ourHead['x']==0
    topWall = ourHead['y']==0
    
    if(rightTopCorner):
        direction = 'left'
    elif(origin):
        direction = 'down'
    elif(leftBottomCorner):
        direction = 'right'
    elif(rightBottomCorner):
        direction = 'up'
    elif (rightWall):
        direction = 'up'
    elif (bottomWall):
        direction = 'right'
    elif (leftWall):
        direction = 'down'
    elif (topWall):
        direction = 'left'
    else:
        direction = 'up'

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    
    # x=data['turn']
    

# print(x)
    
    print(json.dumps(data))

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

def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))

    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)

    return move_response(direction)



