"""
Probabilistic Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

Implemented by: Amr Issa/230265
Phase 3 (Week 5-6)
"""

import random
from environment import GridWorld
from ai_core.bayes_reasoning import update_belief_map

class ProbabilisticAgent:
    """
    An agent that uses Bayesian reasoning to navigate safely 
    and reach the goal.
    """
    
    def __init__(self, environment: GridWorld):
        self.env = environment
        self.rows = environment.height
        self.cols = environment.width
        self.goal = environment.goal 
        
        # Starting beleifs (prior = 20%)
        self.beliefs = {}
        for r in range(self.rows):
            for c in range(self.cols):
                self.beliefs[(r, c)] = 0.2
                
        # Start is safe
        start_pos = environment.agent_pos
        self.beliefs[start_pos] = 0.0
        
        self.visited = set()
        self.visited.add(start_pos)

        # track how many times we visit each cell to break loops
        self.visit_counts = {}
        
    def update_beliefs(self, is_breeze, pos):
        """Update probability grid based on sensor."""
        self.beliefs = update_belief_map(
            self.beliefs, 
            is_breeze, 
            pos,
            sensor_accuracy=0.9
        )
        
    def get_distance_to_goal(self, pos):
        """Simple Manhattan distance to the Red Square."""
        r, c = pos
        gr, gc = self.goal
        return abs(r - gr) + abs(c - gc)
    
    def act(self):
        """
        Decision Loop with Loop-Breaking Logic
        """
        curr_pos = self.env.agent_pos     
        
        # 1. Sense & Update
        is_breeze = self.env.has_breeze(curr_pos)
        self.update_beliefs(is_breeze, curr_pos)
        
        # 2. Get neighbors
        possible_moves = self._get_valid_neighbors(curr_pos)
        random.shuffle(possible_moves) 
        
        # 3. Filter moves by risk
        # "safe" means less than 40% chance of being a pit.
        SAFE_THRESHOLD = 0.4
        
        safe_moves = []
        risky_moves = []
        
        for move in possible_moves:
            prob = self.beliefs.get(move, 0.2)
            
            # categorize
            if prob < SAFE_THRESHOLD:
                safe_moves.append(move)
            else:
                risky_moves.append((move, prob))
        
        # 4. Make decisionn here
        best_move = None
        
        if safe_moves:
            # "BOREDOM LOGIC ": Choose the move that minimizes the loop risk:
            # the score = distance + (# of times we visited it * 5)
            # this makes visited squares look "expensive" to the agent
            
            def calculate_score(move):
                dist = self.get_distance_to_goal(move)
                # this counts how many times we have been there (the default is 0)
                visits = self.visit_counts.get(move, 0)
                # we put a penalty where each visit adds 5 "fake distance" points
                return dist + (visits * 5)

            best_move = min(safe_moves, key=calculate_score)

        elif risky_moves:
            # Desperation: pick the lowest risk
            best_move = min(risky_moves, key=lambda x: x[1])[0]
            
        # Execute
        if best_move:
            # increment visit count for the chosen move
            self.visit_counts[best_move] = self.visit_counts.get(best_move, 0) + 1
            self.visited.add(best_move)
            return best_move
        else:
            return curr_pos

    def _get_valid_neighbors(self, pos):
        r, c = pos
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        valid = []
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                valid.append((nr, nc))
        return valid
