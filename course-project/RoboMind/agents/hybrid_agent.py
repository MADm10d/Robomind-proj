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



class HybridAgent:
    """
    A rational agent that integrates search, logic, and probabilistic reasoning.
    """
    
    def __init__(self, environment: GridWorld):
        """Initialize the hybrid agent."""
        self.env = environment
        
        # Search component
        self.search_agent = SearchAgent(environment)
        
        # Logic component
        self.kb = KnowledgeBase()
        # Add rules using function in knowledge_base file, for reasoning
        for x in range(self.env.width): # loops through all the x's in the grid 
            for y in range(self.env.height): # loops through all the y's in the grid
                self.kb.add_rule([f"Safe({x},{y})", f"Free({x},{y})"], f"CanMove({x},{y})") # forms the rule using each x and y combination
                
        

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
        curr = self.env.agent_pos # getting the current position of the agent
        percepts = self.perceive() # start the perception
        self.update_beliefs(percepts["breeze"]) # update the beliefs
        self.reason() # reason by the logic 
        path, cost, expanded = self.plan() # planning with the search 

    


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

