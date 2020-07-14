'''
ChemistryGym Demo

:title: demo_chemistrygym.py

:author: Chris Beeler and Mitchell Shahen

:history: 2020-07-03
'''

# import all the required external modules
import gym
import numpy as np
import os
import pickle
import sys
from time import sleep

# ensure all necessary modules can be found
sys.path.append("../") # to access chemistrylab
sys.path.append("../chemistrylab/reactions") # to access all reactions

# import all local modules
import chemistrylab

# -------------------- # REACTION BENCH DEMO # -------------------- #
__ = input("PRESS ENTER TO START REACTION BENCH.")

# Use a perfect policy
perfect = False

# Initialize the environment
r_env = gym.make('WurtzReact-v0')
render_mode = "human"

# Reset the environment to get initial state
# State [0] is seconds since the start of reaction
# State [1] is the thermostat temperature of the system
# State [2 and beyond] is the remaining amounts of each reactant
__ = r_env.reset()
r_env.render(mode=render_mode)

__ = input('PRESS ENTER TO CONTINUE REACTION BENCH.')

done = False
i = 0

# Game will play until: 20 steps are reached
total_reward = 0.0

while not done:
    # Select random actions
    # Actions:
    #   a[0] changes the temperature between -dT (a[0] = 0.0) and +dT (a[0] = 1.0)
    #   a[1] changes the Volume between -dV (a[1] = 0.0) and +dV (a[1] = 1.0)
    #   a[2:] adds between none (a[2:] = 0.0) and all (a[2:] = 1.0) of each reactant
    if perfect:
        if i == 0:
            action = np.ones(r_env.action_space.shape)
            action[1] = 0.0
        else:
            action = np.zeros(r_env.action_space.shape)
            action[0] = 1.0
    else:
        action = r_env.action_space.sample()

    # perform the action and update the reward
    state, reward, done, __ = r_env.step(action)
    total_reward += reward

    # render the plot and wait before continuing
    r_env.render(mode=render_mode)
    sleep(2)

    i += 1

# open and check the material dict
vessel_path = os.path.join(os.getcwd(), "vessel_experiment_0.pickle")
with open(vessel_path, 'rb') as open_file:
    v = pickle.load(open_file)
print(v._material_dict)
__ = input("PRESS ENTER TO CONTINUE")

# -------------------- # EXTRACT BENCH DEMO # -------------------- #
__ = input('PRESS ENTER TO START EXTRACT BENCH.')

# create a registered environment
e_env = gym.make('WurtzExtract-v1')
e_env.reset()

# render the initial state
e_env.render(model=render_mode)

# queue and perform the Extraction Vessel's pour by volume action with a multiplier of 0.5 (2/4)
action = np.array([4, 2])
__, __, __, __ = e_env.step(action)

# render the resulting state
e_env.render()

__ = input('PRESS ENTER TO CONTINUE EXTRACT BENCH')

done = False
step_num = 0
total_reward = 0.0

while not done:
    # select and perform a random action
    # actions consist of arrays of two elements
    #   action[0] is a number indicating the event to take place
    #   action[1] is a number representing a multiplier for the event
    # Actions and multipliers are included below:
    #   0: Valve (Speed multiplier, relative to max_valve_speed)
    #   1: Mix ExV (mixing coefficient, *-1 when passed into mix function)
    #   2: Pour B1 into ExV (Volume multiplier, relative to max_vessel_volume)
    #   3: Pour B2 into ExV (Volume multiplier, relative to max_vessel_volume)
    #   4: Pour ExV into B2 (Volume multiplier, relative to default vessel volume)
    #   5: Pour S1 into ExV (Volume multiplier, relative to max_vessel_volume)
    #   6: Pour S2 into ExV (Volume multiplier, relative to max_vessel_volume)
    #   7: Done (Multiplier doesn't matter)
    action_space = e_env.action_space
    action = action_space.sample()

    # perform the random action and update the reward
    state, reward, done, __ = e_env.step(action)
    total_reward += reward

    # render each of the three plots
    e_env.render()
    sleep(2)

    step_num += 1

__ = input("PRESS ENTER TO EXIT.")
