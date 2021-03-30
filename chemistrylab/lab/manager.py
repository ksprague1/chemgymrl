import sys
from abc import ABC

import numpy as np
sys.path.append("../../") # to access `chemistrylab`
from chemistrylab.lab.lab import Lab
from chemistrylab.lab.agent import RandomAgent, Agent
import datetime as dt
import gym

"""
The manager class works as an interface for the agent to work with the lab environment and helps to automate the use of 
the entire lab
"""


class Manager:
    def __init__(self, mode='custom', agent=None):
        """

        Parameters
        ----------
        mode: str: ['human', 'random', 'custom']: describes the mode that the manager will be run in, human opens up a
        cli that can be used to run or by adding an agent to the agents
        agent: Agent: specifies a custom user made agent for the manager to use in solving the lab environment
        """

        self.mode = mode
        self.agents = {'random': RandomAgent}
        self.agent = agent
        self.lab = Lab()

    def register_agent(self, name: str, agent: Agent):
        """
        allows the user to add an agent to the manager environment which they can then use to perform actions in the lab
        environment
        Parameters
        ----------
        name: str: the name of the agent that will be stored
        agent: Agent: the agent that will run the environment

        Returns
        -------
        None
        """
        self.agents[name] = agent

    def register_bench_agent(self, bench: str, name: str, agent: Agent):
        """
        allows the user to add agents to the lab environment which can then be used in order to perform actions in a
        bench
        Parameters
        ----------
        bench: str: reaction, extraction, distillation specifies which bench the agent will be registered for
        name: str: the name of the agent
        agent: Agent: the agent itself of the type Agent

        Returns
        -------
        None
        """
        self.lab.register_agent(bench, name, agent)

    def run(self):
        """
        this function runs the lab environment based on the agent specified by the user, based on the run mode it loads
        the correct agent
        Returns
        -------
        None
        """
        if self.mode == 'human':
            self._human_run()
        elif self.mode in self.agents:
            self.agent = self.agents[self.mode]()
            self._agent_run()
        elif self.agent:
            self.agent = self.agent()
            self._agent_run()
        else:
            raise ValueError("agent specified does not exist")

    def _human_run(self):
        """
        Function for running the environment using a human agent
        the human agent picks an action from the list and is then prompted with options
        Returns
        -------
        None
        """
        done = False
        commands = ['load vessel from pickle',
                    'load distillation bench',
                    'load reaction bench',
                    'load extraction bench',
                    'load analysis bench',
                    'list vessels',
                    'create new vessel',
                    'save vessel',
                    'quit']
        while not done:
            print('Index: Action')
            for i, command in enumerate(commands):
                print(f'{i}: {command}')
            action = int(input('Please select an action: '))

            if action == 0:
                path = input('please specify the path of the vessel: ')
                self.load_vessel(path)
            elif action == 1:
                self._human_bench('distillation')
            elif action == 2:
                self._human_bench('reaction')
            elif action == 3:
                self._human_bench('extraction')
            elif action == 4:
                self._human_bench('analysis')
            elif action == 5:
                self.list_vessels()
            elif action == 6:
                self.create_new_vessel()
            elif action == 7:
                self.save_vessel()
            else:
                done = True

    def _human_bench(self, bench: str):
        """
        a method that loads a bench and provides cli instructions for a human agent
        Parameters
        ----------
        bench: str: either reaction, extraction, distillation or analysis then bench which the human
        agent wishes to load.

        Returns
        -------
        None
        """
        if bench == 'distillation':
            envs = self.lab.distillations
            agents = list(self.lab.distill_agents.keys())
        elif bench == 'reaction':
            envs = self.lab.reactions
            agents = list(self.lab.react_agents.keys())
        elif bench == 'extraction':
            envs = self.lab.extractions
            agents = list(self.lab.extract_agents.keys())
        elif bench == 'analysis':
            envs = ['analysis']
            agents = ['none']
        else:
            raise KeyError('bench not supported')
        print('index: env')
        for i, env in enumerate(envs):
            print(f'{i}: {env}')
        env = int(input('Please specify what environment you wish to use: '))
        self.list_vessels()
        vessel = int(input(
            'Please specify what vessel you wish to use (if you input -1 we will create a new vessel and use that) : '))
        if vessel == -1:
            self.create_new_vessel()
        for i, agent in enumerate(agents):
            print(f'{i}: {agent}')
        agent_ind = int(input('Please specify what agent you wish to use: '))
        start = dt.datetime.now()
        self.load_bench(bench, env, vessel, agent_ind)
        finish = dt.datetime.now()
        print(finish - start)

    def _agent_run(self):
        """
        a wrapper for the agent to run with the lab environment autonomously
        Returns
        -------

        """
        done = False
        self.lab.reset()
        total_reward = 0
        # if at any stage during the running of the environment, if the user selects an analysis technique the data will
        # be stored here
        analysis = np.array([])
        while not done:
            # agent selects actions based on the state of the environemnt and the chosen analysis of a vessel
            action = self.agent.run_step(self.lab, analysis)
            reward, analysis, done = self.lab.step(action)
            total_reward += reward

    def load_bench(self, bench: str, env_index: int, vessel_index: int, agent: int):
        """
        loads and runs a lab bench based on the bench, environment, vessel and agent specified
        Parameters
        ----------
        bench: str: either reaction, extraction, distillation or analysis
        env_index: which environment within each bench the agent wishes to use
        vessel_index: which vessel will provide the necessary materials
        agent: what agent within each bench that will perform the experiment

        Returns
        -------
        None
        """
        self.lab.run_bench(bench,  env_index, vessel_index, agent)

    def list_vessels(self):
        """
        for a human user this function lists all available vessels
        Returns
        -------
        None
        """
        for i, vessel in enumerate(self.lab.shelf.vessels):
            print(f'{i}: {vessel.label}')
            print(vessel.get_material_dict())
            print(vessel.get_solute_dict())

    def load_vessel(self, path: str):
        """
        for a human user, the user may specify a path to a vessel pickle file and load it using this function
        Parameters
        ----------
        path: str: the path to a vessel pickle that will be loaded into the shelf

        Returns
        -------
        None
        """
        self.lab.shelf.load_vessel(path)

    def create_new_vessel(self):
        """
        creates a new empty vessel which is stored in the shelf

        Returns
        -------

        """
        self.lab.shelf.create_new_vessel()

    def save_vessel(self):
        """
        for a human user to save a vessel to a pickle file
        Returns
        -------

        """

        self.list_vessels()
        vessel = int(input('What vessel do you wish to save: '))
        path = input('please specify the relative path for the vessel: ')
        self.lab.shelf.vessels[vessel].save_vessel(path)


if __name__ == "__main__":
    manager = Manager(mode='random')
    manager.run()
