from cc import import_file
cwd = '/bin/'
lib = '/lib/'
turtle = import_file(lib + 'turtle_api.py')

# start bottom fron left
def quarry(width = 4, depth = 4, height = 4):
        # axis one direction changes
        directions = [turtle.left, turtle.right]
        directionIndex = 1
        turtle.forward()
        for i in range(height):
                for j in range(width):
                        for k in range(depth - 1):
                                turtle.dig()
                                turtle.forward()

                        # finished diggin one row
                        # reposition to dig second row
                        if j != (width - 1):
                                # choose direction
                                changeDirection = directions[directionIndex] 

                                # turn to next row
                                changeDirection()
                                turtle.dig()
                                turtle.forward()
                                changeDirection()

                                # change direction
                                directionIndex = (directionIndex + 1) % 2
                
                # reset in next level
                if i != (hieght - 1):
                        turtle.digDown()
                        turtle.down()
                        turtle.left()
                        turtle.left()
