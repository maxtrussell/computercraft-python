from cc import import_file
turtle = import_file('/lib/turtle_api.py')

# start bottom front left
def quarry(width, depth, height):
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
                if i != (height - 1):
                        turtle.digDown()
                        turtle.down()
                        turtle.left()
                        turtle.left()
