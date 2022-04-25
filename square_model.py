import numpy as np
np.set_printoptions(precision=2)

# all temps in centigrade
brownie_target = 85
room_temp = 18.333
side_length = 20
pan_temp = room_temp
oven_temp = 162.778

h = 9.14
A = 0.0001 # 0.01m ^2

brownie_density = 500
brownie_specific_heat = 2550
brownie_conductivity = 0.15
brownie_alpha = brownie_conductivity / (brownie_density * brownie_specific_heat)

steel_density = 7832
steel_specific_heat = 434
steel_conductivity = 59
steel_alpha = steel_conductivity / (steel_density * steel_specific_heat)

print(brownie_alpha)
print(steel_alpha)
print(A)

def initialize_brownie_pan(side_length, room_temp):
    return np.full((side_length, side_length), room_temp)


def heat_transfer_over_increment(brownie_pan: np.array, pan_temp, dx, dt):
    # heat transfer from oven to pan
    d_pan_temp = h * A * (oven_temp - pan_temp)
    pan_temp += dt * d_pan_temp 

    # heat transfer from pan to brownie
    time_derivative = np.zeros(brownie_pan.shape)
    for x in range(side_length):
        for y in range(side_length):
            # edge
            if (x == 0 and y == 0): # top left corner
                outside_squares = 2 * pan_temp 
                surrounding_squares = brownie_pan[x][y+1] + brownie_pan[x+1][y] + outside_squares
                curr_square = 4 * brownie_pan[x][y]
            elif (x == 0 and y == (side_length - 1)): # bottom left corner
                outside_squares = 2 * pan_temp 
                surrounding_squares = brownie_pan[x][y-1] + brownie_pan[x+1][y] + outside_squares
                curr_square = 4 * brownie_pan[x][y]
            elif (x == (side_length - 1) and y == 0): # top right corner
                outside_squares = 2 * pan_temp 
                surrounding_squares = brownie_pan[x][y+1] + brownie_pan[x-1][y] + outside_squares
                curr_square = 4 * brownie_pan[x][y]
            elif (x == (side_length - 1) and y == (side_length - 1)): # bottom right corner
                outside_squares = 2 * pan_temp 
                surrounding_squares = brownie_pan[x][y-1] + brownie_pan[x-1][y] + outside_squares
                curr_square = 4 * brownie_pan[x][y]
            elif x == 0: # left edge
                surrounding_squares = brownie_pan[x][y+1] + brownie_pan[x][y-1] + brownie_pan[x+1][y] + pan_temp
                curr_square = 4 * brownie_pan[x][y]
            elif y == 0: # top edge
                surrounding_squares = brownie_pan[x+1][y] + brownie_pan[x-1][y] + brownie_pan[x][y+1] + pan_temp
                curr_square = 4 * brownie_pan[x][y]
            elif x == (side_length - 1): # right edge
                surrounding_squares = brownie_pan[x][y+1] + brownie_pan[x][y-1] + brownie_pan[x-1][y] + pan_temp
                curr_square = 4 * brownie_pan[x][y]
            elif y == (side_length - 1): # bottom edge
                surrounding_squares = brownie_pan[x+1][y] + brownie_pan[x-1][y] + brownie_pan[x][y-1] + pan_temp
                curr_square = 4 * brownie_pan[x][y]
            else:
                surrounding_squares = brownie_pan[x + 1][y] + brownie_pan[x - 1][y] + brownie_pan[x][y + 1] + brownie_pan[x][y - 1]
                curr_square = 4 * brownie_pan[x][y]

            time_derivative[x][y] = (brownie_alpha / (dx ** 2)) * (surrounding_squares - curr_square + pan_temp)

    brownie_pan += (time_derivative * dt)
    return brownie_pan, pan_temp

brownie_pan = initialize_brownie_pan(side_length, room_temp)
counter = 0
while True:
    brownie_pan, pan_temp = heat_transfer_over_increment(brownie_pan, pan_temp, dx=0.01, dt=0.01) # 0.01 meters (1cm), 0.01 seconds
    # if counter % 10000 == 0:
    #     print(brownie_pan)
    counter += 1
    if brownie_pan[int(side_length/2)][int(side_length/2)] >= brownie_target:
        print(f"{counter / 100 / 60} minutes of cooking")
        print(pan_temp)
        break

print(brownie_pan)