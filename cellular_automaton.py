import math
import random
from time import sleep
import sys
import subprocess
import os
#avoiding the prints of pygame library
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

#downloading the required packages(numpy and pygame) if they aren't installed
try:
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'numpy'], stdout=subprocess.DEVNULL)
    print("Installed numpy")
    import numpy as np

try:
    import pygame as pg
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pygame'], stdout=subprocess.DEVNULL)
    print("Installed pygame")
    import pygame as pg


#this class represents an organism in the simulation
class Organism:
    # ctor
    def __init__(self, state, speed, X):
        self.state = state
        self.speed = speed
        self.sick_time = X

    # setting the state of the organism
    def set_state(self, new_state):
        self.state = new_state

    # returns true if the organism is healthy, else - false
    def is_healthy(self):
        if self.state == 1:
            return True
        return False

    # returns true if the organism is sick, else - false
    def is_sick(self):
        if self.state == 2:
            return True
        return False

    #checking if the organism still has time to be sick
    def is_still_sick(self):
        if self.sick_time > 0:
            return True
        return False

    #updating the number of generations that the organism has to be sick
    def update_sick_time(self):
        self.sick_time -= 1
        return self.sick_time


#the board size - size*size
size = 200


#moving an organism randomly - setting the selected new location in "update_positions"
#parameters: the board, a list with the selected locations for all the organisms,
# the row and column of the organism's current location, the speed of the organism, the id of the organism
def move(board, update_positions, row, col, steps, id):
    new_position = []
    options_list = [1,2,3,4,5,6,7,8,9]
    valid_position = False

    #untill the selected new location doesn't collide with other organism's location - selecting a new location
    while valid_position == False:
        #selecting the movement of the organism randomly
        x = random.choice(options_list)

        # Stay in the same place
        if x == 1:
            new_position = [row, col]
        # Up + Left
        elif x == 2:
            new_position = [((row - steps) + size) % size, ((col - steps) + size) % size]
        # Up
        elif x == 3:
            new_position = [((row - steps) + size) % size, col]
        # Up + Right
        elif x == 4:
            new_position = [((row - steps) + size) % size, ((col + steps) + size) % size]
        # Left
        elif x == 5:
            new_position = [row, ((col - steps) + size) % size]
        # Right
        elif x == 6:
            new_position = [row, ((col + steps) + size) % size]
        # Down + Left
        elif x == 7:
            new_position = [((row + steps) + size) % size, ((col - steps) + size) % size]
        # Down
        elif x == 8:
            new_position = [((row + steps) + size) % size, col]
        # Down + Right
        elif x == 9:
            new_position = [((row + steps) + size) % size, ((col + steps) + size) % size]

        #checking if the position is valid - not colliding with other organism's position
        if board[new_position[0], new_position[1]] == 0 or board[new_position[0], new_position[1]] == id:
            valid_position = True
        #if invalid - removing the selected movement from the possible movements array
        else:
            options_list.remove(x)

    #checks if the selected new location collides with a new location of a previous organism
    #if there is a collision - the current organism will stay in the same place
    for i in range(id - 1):
        if update_positions[i + 1][0] == new_position[0] and update_positions[i + 1][1] == new_position[1]:
            new_position = [row, col]

    #updates the new position of the current organism
    update_positions[id] = new_position


#initializing the board of the simulation
def initialize_board(N, init_positions):
    # Create an empty 2D numpy array by the size(0 - an empty position)
    an_array = np.full([size, size], 0)

    #adding the organisms to the board
    for i in range(N):
        #finds a position that is empty
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)

        while an_array[row, col] != 0:
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)

        #setting the current organism in the empty position
        an_array[row, col] = i + 1
        init_positions[i] = [row , col]

    return an_array


#initializing dictionary that holds information about every organism
def initialize_dict(N, init_positions, D, R, X):
    org_dict = {}
    #the initial states of the organisms
    states = np.full(N, 1)
    #selecting randomly by D the sick organisms
    sick_indexes = random.sample(range(0, N), D)
    #setting the state of the sick organisms(2)
    for index in sick_indexes:
        states[index] = 2

    #the initial speeds of the organisms
    speeds = np.full(N, 1)
    # selecting randomly by R the fast organisms
    fast_indexes = random.sample(range(0, N), R)
    # setting the speed of the sick organisms(10)
    for index in fast_indexes:
        speeds[index] = 10

    #adding the organisms to the dictionary
    for i in range(N):
        org_dict[i + 1] = (init_positions[i], Organism(states[i], speeds[i], X))

    return org_dict


#checking if there is a neighbor near the input position. if there is - returning it's id
def get_neighbors_ids(array, row, col):
    ids = []
    if array[((row - 1) + size) % size, ((col - 1) + size) % size] != 0:
        ids.append(array[((row - 1) + size) % size, ((col - 1) + size) % size])
    if array[((row - 1) + size) % size, col] != 0:
        ids.append(array[((row - 1) + size) % size, col])
    if array[((row - 1) + size) % size, ((col + 1) + size) % size] != 0:
        ids.append(array[((row - 1) + size) % size, ((col + 1) + size) % size])
    if array[row, ((col - 1) + size) % size] != 0:
        ids.append(array[row, ((col - 1) + size) % size])
    if array[row, ((col + 1) + size) % size] != 0:
        ids.append(array[row, ((col + 1) + size) % size])
    if array[((row + 1) + size) % size, ((col - 1) + size) % size] != 0:
        ids.append(array[((row + 1) + size) % size, ((col - 1) + size) % size])
    if array[((row + 1) + size) % size, col] != 0:
        ids.append(array[((row + 1) + size) % size, col])
    if array[((row + 1) + size) % size, ((col + 1) + size) % size] != 0:
        ids.append(array[((row + 1) + size) % size, ((col + 1) + size) % size])

    return ids


#randomly selecting sick or healthy by P
def random_sick(P):
    state = ["sick", "healthy"]
    if np.random.choice(state, p=[P, 1 - P]) == "sick":
        return True
    return False


#setting P by the sick organisms rate and T
def initialize_p(T, P_low, P_high, sick_rate):
    if sick_rate <= T:
        return P_high
    elif sick_rate > T:
        return P_low

#printing the information about the organisms
def print_organisms(organisms_list, N):
    for i in range(N):
        print('id:', i + 1)
        print('position:', organisms_list[i + 1][0])
        print('data:', organisms_list[i + 1][1].state, organisms_list[i + 1][1].sick_time, organisms_list[i + 1][1].speed)


#checks if the input parameters are valid
def are_parameters_valid(N, D, R, X, P_low, P_high, T):
    valid_parameters = True
    if N >= size*size:
        print("Too Many Organisms - N Needs To Be Smaller Than The Size Of The Board.")
        valid_parameters = False
    if N < 1:
        print("N Needs To Be At Least 1.")
        valid_parameters = False
    if not isinstance(N, int):
        print("N Needs To Be An Integer.")
        valid_parameters = False
    if D > 1 or D < 0:
        print("D Needs To Be Between 0 And 1.")
        valid_parameters = False
    if R > 1 or R < 0:
        print("R Needs To Be Between 0 And 1.")
        valid_parameters = False
    if X < 0:
        print("X Needs To Be At Least 0.")
        valid_parameters = False
    if not isinstance(X, int):
        print("X Needs To Be An Integer.")
        valid_parameters = False
    if P_low > 1 or P_low < 0:
        print("P_low Needs To Be Between 0 And 1.")
        valid_parameters = False
    if P_high > 1 or P_high < 0:
        print("P_high Needs To Be Between 0 And 1.")
        valid_parameters = False
    if P_low > P_high:
        print("P_low Needs To Be Lower Or Equal To P_high.")
        valid_parameters = False
    if T > 1 or T < 0:
        print("T Needs To Be Between 0 And 1.")
        valid_parameters = False

    return valid_parameters


#main function
if __name__ == '__main__':
    if len(sys.argv) < 8:
        print("Not Enough Parameters!")
    else:
        # initializing the parameters by the input of the user
        N = int(sys.argv[1])
        D = float(sys.argv[2])
        R = float(sys.argv[3])
        X = int(sys.argv[4])
        P_low = float(sys.argv[5])
        P_high = float(sys.argv[6])
        T = float(sys.argv[7])

        #if the parameters are valid - proceeding
        if are_parameters_valid(N, D, R, X, P_low, P_high, T):
            num_of_fast_organisms = math.ceil(N*R)
            sick_organisms = math.ceil(N*D)
            print("Number Of Organisms:", N, ", Initial Number Of Sick Organisms:", sick_organisms,
                  " ,Number Of Fast Organisms: ", num_of_fast_organisms)
            #initializing the board and the starting positions of the organisms
            init_positions = [None] * N
            arr = initialize_board(N, init_positions)

            #initializing the properties for every organism
            organisms_dict = initialize_dict(N, init_positions, sick_organisms, num_of_fast_organisms, X)

            #the colors on the board
            colors = np.array([[255, 255, 255], [120, 250, 90], [250, 90, 120], [80, 128, 255]])

            isLastGeneration = False

            #generations loop
            generation = 0
            while not isLastGeneration:
                #if there are not anymore sick organisms - the simulation will stop
                if sick_organisms == 0:
                    isLastGeneration = True
                sick_rate = float(sick_organisms/N)
                # check for updating p
                P = initialize_p(T, P_low, P_high, sick_rate)

                print("Generation: ", generation, " Sick Rate: ", sick_rate)

                #creating a board with the organism's states instead of the organism's ids
                states_board = np.empty((size, size))
                for i in range(size):
                    for j in range(size):
                        if arr[i][j] != 0:
                            states_board[i][j] = organisms_dict[arr[i][j]][1].state
                        else:
                            states_board[i][j] = 0

                #presenting the visual board
                states_board = states_board.astype(int)
                pg.init()
                screen = pg.display.set_mode((700, 700))

                print_array = np.transpose(states_board)
                colors_arr = colors[print_array]
                surface = pg.surfarray.make_surface(colors_arr)
                surface = pg.transform.scale(surface, (600, 600))  # Scaled a bit.

                pg.font.init()
                my_font = pg.font.SysFont('Comic Sans MS', 30)
                text_surface = my_font.render(
                    'Generation: ' + str(generation) + ", Sick Organisms Rate: " + str(sick_rate*100) + "%",
                    False, (255, 255, 255))

                screen.fill((30, 30, 30))
                screen.blit(surface, (60, 60))
                screen.blit(text_surface, (10, 10))
                pg.display.flip()
                sleep(3)

                #scans the array for the sick organisms
                update_states = {}
                for i in range(N):
                    #if the current organism is still sick
                    if organisms_dict[i + 1][1].is_sick():
                        #if the current organism has no time left to be sick - updating it's state and the sick counter
                        if not organisms_dict[i + 1][1].is_still_sick():
                            update_states[i + 1] = 3
                            sick_organisms -= 1

                        #if the current organism if still sick
                        else:
                            #getting the organism's neighbors and randomizing by P if the healthy neighbors will be sick
                            for neighbor_id in get_neighbors_ids(arr, organisms_dict[i + 1][0][0], organisms_dict[i + 1][0][1]):
                                #if the neighbor is healthy
                                if organisms_dict[neighbor_id][1].is_healthy():
                                    #randomize if sick
                                    if random_sick(P):
                                        #means that no other organism already got the current neighbor sick
                                        if neighbor_id not in update_states:
                                            #updating the neighbor's state and the sick counter
                                            update_states[neighbor_id] = 2
                                            sick_organisms += 1

                            organisms_dict[i + 1][1].update_sick_time()

                #updating the states for the next generation
                for update_index in update_states:
                    organisms_dict[update_index][1].set_state(update_states[update_index])

                #scans the array and for every organism's randomizing it's new position
                update_positions = {}
                for i in range(N):
                    move(arr, update_positions, organisms_dict[i + 1][0][0], organisms_dict[i + 1][0][1], organisms_dict[i + 1][1].speed, i + 1)

                #update the positions on the dictionary and on the board
                for i in range(N):
                    # updates the new position for the organism on the board
                    arr[update_positions[i + 1][0], update_positions[i + 1][1]] = i + 1
                    # setting the old position as empty if no previous organism moves to this location
                    if arr[organisms_dict[i + 1][0][0], organisms_dict[i + 1][0][1]] == i + 1 and organisms_dict[i + 1][0] != update_positions[i + 1]:
                        arr[organisms_dict[i + 1][0][0], organisms_dict[i + 1][0][1]] = 0

                    # updates the new position for the organism in the dictionary
                    organisms_dict[i + 1][0][0] = update_positions[i + 1][0]
                    organisms_dict[i + 1][0][1] = update_positions[i + 1][1]

                #updates the generation number
                generation += 1
