"""
Hybrid Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

Implemented by: Abdulrahman Salameh 230326
Phase 4 of the project (Week 7-8) - Final Integration
"""

from environment import GridWorld
from agents.search_agent import SearchAgent
from ai_core.knowledge_base import KnowledgeBase
from ai_core.bayes_reasoning import update_belief_map
import random



class HybridAgent:
    """
    A rational agent that integrates search, logic, and probabilistic reasoning.
    """
    
    def __init__(self, environment: GridWorld):
        """Initialize the hybrid agent."""
        self.env = environment
        
        # Search component
        self.search_agent = SearchAgent(environment)
        self.search_agent.verbose = False
        
        # Logic component
        self.kb = KnowledgeBase()
        # Add rules using function in knowledge_base file, for reasoning
        for x in range(self.env.width): # loops through all the x's in the grid 
            for y in range(self.env.height): # loops through all the y's in the grid
                self.kb.add_rule([f"Safe({x},{y})", f"Free({x},{y})"], f"CanMove({x},{y})") # forms the rule using each x and y combination
                self.kb.add_rule([f"At({x},{y})", f"Safe({x},{y})"], f"Visited({x},{y})")
                
        

        # Probabilistic component
        self.beliefs = {}
        # initialize the beliefs using the logic used in Probability agent
        # Initialize Beliefs (Prior = 20%)
        for r in range(self.env.height):
            for c in range(self.env.width):
                self.beliefs[(r, c)] = 0.2
                
        # Start is safe
        start_pos = environment.agent_pos
        self.beliefs[start_pos] = 0.0
        
        self.visited = set()
        self.visited.add(start_pos)

        # Track how many times we visit each cell to break loops
        self.visit_counts = {}


    def perceive(self):
        """
        Get sensor readings from environment.
        May be noisy - need probability!
        """
        curr_pos = self.env.agent_pos # getting the current position of the agent
        is_breeze = self.sense_breeze(curr_pos) # calling the sense_breeze method to get the breeze sensor reading
        return {"breeze": is_breeze} 
    
    def plan(self):
        """
        Use A* search algorithm to plan path to goal.
        We chose A* because it is complete, optimal, and efficient.
        Based on our tests, A* performed the best in terms of path length and time complexity.
        """
        path, cost, expanded = self.search_agent.search(algorithm='astar', heuristic='manhattan')
        self.env.path = path or []
        return path, cost, expanded
    
    def reason(self):
        """
        Use logic to infer safe moves and update knowledge base.
        """
        # Convert beliefs into logical facts
        for (x, y), prob in self.beliefs.items(): #using the beliefs found by probability agent
            if prob <= 0.1:  # High confidence that the cell is safe
                self.kb.tell(f"Safe({x},{y})")
                self.kb.tell(f"Free({x},{y})")
            elif 0.1 < prob < 0.7:  # Medium confidence that the cell is free
                self.kb.tell(f"Free({x},{y})")
            else:  # High confidence that the cell is an obstacle
                self.kb.tell(f"Obstacle({x},{y})")

        # Rules for CanMove were pre added in init
        
        # Perform inference using the infer function implemented before, to derive new facts
        self.kb.infer()
        

    def update_beliefs(self,is_breeze):
        """
        Use Bayesian inference to handle uncertain sensor readings.
        """
        curr_pos = self.env.agent_pos # getting the current position of the agent
        # Update beliefs using the update_belief_map function implemented before
        self.beliefs = update_belief_map(
            self.beliefs, 
            is_breeze, # getting the breeze sensor reading
            curr_pos,
            sensor_accuracy=0.9  # Same accuracy as ProbabilisticAgent
    )
    
    def act(self):
        """
        Integrate all reasoning techniques to decide next action.
        
        Strategy:
            1. If goal is visible and path is clear → use search
            2. If uncertain about obstacles → use probability
            3. If need to infer hidden info → use logic
        """
        # 1) Sense → Update Beliefs → Reason
        curr = self.env.agent_pos # getting the current position of the agent
        percepts = self.perceive() # start the perception
        self.update_beliefs(percepts["breeze"]) # update the beliefs using Bayes
        self.reason() # reason by the logic (facts + rules → inference)
        self.kb.tell(f"At({curr[0]},{curr[1]})") # track current location as a fact
        path, cost, expanded = self.plan() # planning with the search (A*)

        # 2) Try using the planned path if the next step is safe 
        # We gate following A* by a safety threshold derived from beliefs.
        SAFE_THRESHOLD = 0.4
        next_step = None
        if path:
            # If path exists, take the immediate next cell (or current if single node)
            next_step = path[1] if len(path) > 1 else path[0]
        # Move by search only if it's a real progress, valid, and sufficiently safe
        if next_step and next_step != curr and self.env.is_valid(next_step) and self.beliefs.get(next_step, 0.2) < SAFE_THRESHOLD:
            self.env.agent_pos = next_step
            self.visit_counts[next_step] = self.visit_counts.get(next_step, 0) + 1
            self.visited.add(next_step)
            self.kb.tell(f"At({next_step[0]},{next_step[1]})")
            print(f"[Search Agent] move->{next_step} p={self.beliefs.get(next_step, 0.2):.2f}")
            print("")
            return

        # If search could not proceed, record the reason and fall back to probability
        failure_reason = None
        if not path:
            failure_reason = "no path"
        elif not next_step or next_step == curr:
            failure_reason = "no progress"
        elif not self.env.is_valid(next_step):
            failure_reason = "blocked"
        elif self.beliefs.get(next_step, 0.2) >= SAFE_THRESHOLD:
            failure_reason = f"unsafe p={self.beliefs.get(next_step, 0.2):.2f}≥{SAFE_THRESHOLD}"
        if failure_reason:
            print(f"[Search Agent] fail: {failure_reason}; trying probability")
        
        # 3) Probabilistic fallback 
        # Consider only unvisited neighbors to avoid loops and choose the best
        # according to risk + proximity + revisit penalty.
        neighbors = [n for n in self.env.get_neighbors(curr) if n not in self.visited]
        random.shuffle(neighbors)
        safe_moves = []
        risky_moves = []
        for n in neighbors:
            p = self.beliefs.get(n, 0.2)
            if p < SAFE_THRESHOLD:
                safe_moves.append(n)
            else:
                risky_moves.append((n, p))

        def manhattan(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        goal = self.env.goal

        # Score combines distance to goal and revisit penalty; lower is better
        def score(move):
            return manhattan(move, goal) + (self.visit_counts.get(move, 0) * 5)

        best_move = None
        if safe_moves:
            best_move = min(safe_moves, key=score)
        elif risky_moves:
            best_move = min(risky_moves, key=lambda x: x[1])[0]

        # If probability suggests a real move, perform it and update KB
        if best_move and best_move != curr:
            self.visit_counts[best_move] = self.visit_counts.get(best_move, 0) + 1
            self.visited.add(best_move)
            self.kb.tell(f"Previous({best_move[0]},{best_move[1]},{curr[0]},{curr[1]})")
            self.env.agent_pos = best_move
            self.kb.tell(f"At({best_move[0]},{best_move[1]})")
            print(f"[Probabilistic Agent] move->{best_move} prob={self.beliefs.get(best_move, 0.2):.2f} dist={manhattan(best_move, goal)} visits={self.visit_counts.get(best_move, 0)}")
            print("")
            return

        # If probability cannot help, use logic for goal, inferred safe moves, or backtracking
        if not safe_moves and not risky_moves:
            print("[Probabilistic Agent] fail: no unvisited neighbors; trying logic")
        possible_moves = self.env.get_neighbors(self.env.agent_pos)
        for move in possible_moves:
            if self.env.is_goal(move):
                self.kb.tell(f"Previous({move[0]},{move[1]},{self.env.agent_pos[0]},{self.env.agent_pos[1]})")
                self.env.agent_pos = move
                print(f"[Logic] goal->{move}")
                print("")
                return

        for move in possible_moves:
            nx, ny = move
            if not self.kb.ask(f"Visited({nx},{ny})") and self.kb.ask(f"CanMove({nx},{ny})"):
                self.kb.tell(f"Previous({nx},{ny},{self.env.agent_pos[0]},{self.env.agent_pos[1]})")
                self.env.agent_pos = move
                print(f"[Logical Agent] infer->{(nx, ny)}")
                print("")
                return

        for move in possible_moves:
            nx, ny = move
            if self.kb.ask(f"Previous({self.env.agent_pos[0]},{self.env.agent_pos[1]},{nx},{ny})"):
                self.env.agent_pos = move
                print(f"[Logical Agent] backtrack->{(nx, ny)}")
                print("")
                return

    # helper method
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
            if 0 <= nr < self.env.height and 0 <= nc < self.env.width:
                # Check for Pit/Obstacle (Value 1)
                # We access the environment's grid data directly here
                if self.env.grid[nr][nc] == 1: 
                    return True
        return False

# Example usage
if __name__ == "__main__":
    print("Hybrid Agent - combines Search + Logic + Probability")
    print("This is the final phase - integrate everything!")
