"""
Search Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

Implemented by: Mohammed Al-deri 
Phase 1 of the project (Week 1-2)
"""

from environment import GridWorld
from typing import Tuple, List, Optional
from ai_core.search_algorithms import bfs, ucs, astar


class SearchAgent:

    # Initialize the search agent.
    def __init__(self, environment: GridWorld):
        
        self.env = environment
        self.path = []
        self.current_pos = environment.start
        self.verbose = True
    
    def search(self, algorithm='bfs', heuristic='manhattan') -> Tuple[Optional[List], float, int]:
        
        #Find a path from start to goal using the specified algorithm.
        
        if self.verbose:
            print(f"\n🔍 Running {algorithm.upper()} search...")
            print(f"   Start: {self.env.agent_pos}")
            print(f"   Goal: {self.env.goal}")
        
        current_start = self.env.agent_pos
        if algorithm == 'bfs':
            path, cost, expanded = bfs(self.env, current_start, self.env.goal)
        elif algorithm == 'ucs':
            path, cost, expanded = ucs(self.env, current_start, self.env.goal)
        elif algorithm == 'astar':
            path, cost, expanded = astar(self.env, current_start, self.env.goal, heuristic)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        if path is None:
            path = []
            
        self.path = path
        
        return path, cost, expanded
    
    def move_along_path(self):
        # Move the agent along the computed path (for visualization).
        if not self.path:
            print("No path to follow!")
            return
        
        print(f"\n🤖 Moving along path ({len(self.path)} steps)...")
        
        self.env.agent_pos = self.env.start
        self.env.render() 
        
        for i, pos in enumerate(self.path):
            self.env.agent_pos = pos
            self.env.visited.add(pos)
            self.env.render()
            
            pygame.event.pump() 
            
            time.sleep(0.3) 
            
            if self.env.is_goal(pos):
                print(f"✓ Goal reached at step {i+1}!")
                break

# Example usage and testing
if __name__ == "__main__":
    import pygame
    import time

    pygame.init()

    print("=== Search Agent Test ===\n")
    
    # Create a test environment
    env = GridWorld(width=8, height=8, cell_size=60)
    
    # Add some obstacles
    obstacles = [(2, 2), (2, 3), (2, 4), (4, 4), (5, 4), (6, 4)]
    for obs in obstacles:
        env.add_obstacle(*obs)
    
    env.start = (0, 0)
    env.goal = (7, 7)

    env.init_display()
    
    # Create agent
    agent = SearchAgent(env)

    algos = [
        ('bfs', 'Breadth-First Search'),
        ('ucs', 'Uniform Cost Search'),
        ('astar', 'A* Search')
    ]

    for algo, name in algos:
        env.reset()
        env.agent_pos = env.start
        env.visited = set()
        env.render()

        # Test search (will fail until you implement the algorithms!)
        try:
            path, cost, expanded = agent.search(algo)
            print(f"\n✓ {name} found path with {len(path)} steps, cost={cost}, expanded={expanded} nodes")
            agent.move_along_path()
            time.sleep(1)

        except NotImplementedError:
            print("\n⚠️  {name} not implemented yet - please implement in ai_core/search_algorithms.py")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

    time.sleep(2)
    pygame.quit()
