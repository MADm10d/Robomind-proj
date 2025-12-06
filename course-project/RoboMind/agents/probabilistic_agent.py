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
        
        # Initialize Beliefs (Prior = 20%)
        self.beliefs = {}
        for r in range(self.rows):
            for c in range(self.cols):
                self.beliefs[(r, c)] = 0.2
                
        # Start is safe
        start_pos = environment.agent_pos
        self.beliefs[start_pos] = 0.0
        
        self.visited = set()
        self.visited.add(start_pos)

        # Track how many times we visit each cell to break loops
        self.visit_counts = {}

    # --- SENSOR METHOD (Crucial for Phase 3) ---
    def sense_breeze(self, pos):
        """
        Simulate a Breeze Sensor by looking at the grid directly.
        Returns True if any neighbor is a Pit (Obstacle).
        """
        r, c = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check boundaries
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                # Check for Pit/Obstacle (Value 1)
                # We access the environment's grid data directly here
                if self.env.grid[nr][nc] == 1: 
                    return True
        return False
    # -------------------------------------------
        
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
        Decision Loop: Sense -> Think -> Act
        """
        curr_pos = self.env.agent_pos     
        
        # 1. Sense (Using our internal sensor)
        is_breeze = self.sense_breeze(curr_pos)
        
        # 2. Update Beliefs
        self.update_beliefs(is_breeze, curr_pos)
        
        # 3. Get Neighbors
        possible_moves = self._get_valid_neighbors(curr_pos)
        random.shuffle(possible_moves) 
        
        # 4. Filter Moves by Risk
        # "Safe" means less than 40% chance of being a pit.
        SAFE_THRESHOLD = 0.4
        
        safe_moves = []
        risky_moves = []
        
        for move in possible_moves:
            prob = self.beliefs.get(move, 0.2)
            
            # Categorize
            if prob < SAFE_THRESHOLD:
                safe_moves.append(move)
            else:
                risky_moves.append((move, prob))
        
        # 5. Make Decision
        best_move = None
        
        if safe_moves:
            # --- "BOREDOM" LOGIC ---
            # Score = Distance + (Number of times we visited it * 5)
            # This makes visited squares look "expensive" so we don't loop forever.
            
            def calculate_score(move):
                dist = self.get_distance_to_goal(move)
                visits = self.visit_counts.get(move, 0)
                return dist + (visits * 5)

            best_move = min(safe_moves, key=calculate_score)

        elif risky_moves:
            # Desperation: Pick lowest risk
            best_move = min(risky_moves, key=lambda x: x[1])[0]
            
        # Execute
        if best_move:
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
