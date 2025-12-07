"""
Logic Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

Implemented by: Abdulaziz Altamimi 230714
Phase 2 of the project (Week 3-4)
"""

from environment import GridWorld
from ai_core.knowledge_base import KnowledgeBase
import random

class LogicAgent:
    """
    An agent that uses propositional logic to reason about the world.
    """
    
    def __init__(self, environment: GridWorld):
        """Initialize the logic agent."""
        self.env = environment
        self.kb = KnowledgeBase()

        for x in range(self.env.width): # loops through all the x's in the grid 
            for y in range(self.env.height): # loops through all the y's in the grid
                self.kb.add_rule([f"Safe({x},{y})", f"Free({x},{y})"], f"CanMove({x},{y})") # forms the rule using each x and y combination
                self.kb.add_rule([f"At({x},{y})", f"Safe({x},{y})"], f"Visited({x},{y})") # adding the visited fact of the agent's position to the knowledge base
        
    def perceive(self):
        """Perceive the environment and update knowledge base."""

        pos_x, pos_y = self.env.agent_pos # storing the x and y values of the agent's position 
          
        if self.env.is_valid((pos_x,pos_y)): # checking if position is valid
            self.kb.tell(f"At({pos_x},{pos_y})") # adding the at fact of the agent's position to the knowledge base
            self.kb.tell(f"Safe({pos_x},{pos_y})") # adding the safe fact of the agent's position to the knowledge base
            if not self.env.is_goal((pos_x,pos_y)): # if the agent is not at goal position it adds the agent's neighbors facts to the knowledge base
                for i in self.env.get_neighbors((pos_x,pos_y)): # looping through the neighbors of the agent's position
                    neighbor_x = i[0] # neighbor's x position
                    neighbor_y = i[1] # neighbor's y position
                    self.kb.tell(f"Safe({neighbor_x},{neighbor_y})") # adding the safe fact of the agent's neighbor's position to the knowledge base
                    self.kb.tell(f"Free({neighbor_x},{neighbor_y})") # adding the free fact of the agent's neighbor's position to the knowledge base
                    #self.kb.tell(f"Adjacent({pos_x},{pos_y},{neighbor_x},{neighbor_y})") # adding the adjacent fact between the agent's position and its neighbor's position to the knowledge base    
            return
    
    def reason(self):
        """Use logic inference to make decisions."""

        self.kb.infer() # calling the infer method from kb to make the reasoning 
    
    def act(self):
        """Decide and execute next action."""

        if not self.env.is_goal(self.env.agent_pos): # checking if the agent is not at goal state

            possible_moves = self.env.get_neighbors(self.env.agent_pos) # storing all valid neighbors of the agent

            for move in possible_moves: # looping through all the valid neighbors
                neighbor_x, neighbor_y = move # storing the x and y values of the agent's valid neighbor's position
                

                if self.env.is_goal(move): # if agent has the goal as a neighbor it immediately goes to it 
                    self.env.agent_pos = move
                    print("goal achieved")
                    return
            
            for move in possible_moves: # looping through all the valid neighbors
                neighbor_x, neighbor_y = move # storing the x and y values of the agent's valid neighbor's position
                
                if not self.kb.ask(f"Visited({neighbor_x},{neighbor_y})"): # if the agent hasn't visited the neighbor it moves there 
                    self.kb.tell(f"Previous({neighbor_x},{neighbor_y},{self.env.agent_pos[0]},{self.env.agent_pos[1]})")
                    self.env.agent_pos = move
                    return
            
            for move in possible_moves: # looping through all the valid neighbors
                neighbor_x, neighbor_y = move # storing the x and y values of the agent's valid neighbor's position
                
                if self.kb.ask(f"Previous({self.env.agent_pos[0]},{self.env.agent_pos[1]},{neighbor_x},{neighbor_y})"): # if the agent has valid neighbors and has visited them and they aren't the goal it backtracks to the previous move
                    print("Backtracking")
                    self.env.agent_pos = move
                    return