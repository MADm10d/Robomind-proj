"""
RoboMind - Main Entry Point
SE444 - Artificial Intelligence Course Project

Run different modes of the simulation:
    python main.py --demo              # Run environment demo
    python main.py --test-search       # Test search algorithms
    python main.py --test-logic        # Test logic agent
    python main.py --test-probability  # Test probabilistic agent
    python main.py --test-hybrid       # Test hybrid agent
    python main.py --experiment all    # Run all experiments
"""
import time 
import argparse
import sys
import pygame # Need this for the visual pauses
from environment import GridWorld, demo as env_demo

# Import agent modules (students will implement these)
try:
    from agents.search_agent import SearchAgent
except ImportError:
    SearchAgent = None
    
try:
    from agents.logic_agent import LogicAgent
except ImportError:
    LogicAgent = None
    
try:
    from agents.probabilistic_agent import ProbabilisticAgent
except ImportError:
    ProbabilisticAgent = None
    
try:
    from agents.hybrid_agent import HybridAgent
except ImportError:
    HybridAgent = None


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def run_demo():
    """Run environment demonstration."""
    print_header("RoboMind Environment Demo")
    print("This demo shows the grid world environment.")
    print("Use arrow keys to move the agent manually.")
    print("Press 'R' to reset to start position.\n")
    env_demo()


def test_search():
    """Test search algorithms."""
    print_header("Testing Search Algorithms")
    
    if SearchAgent is None:
        print("❌ SearchAgent not implemented yet!")
        print("Please implement agents/search_agent.py")
        return
    
    # Create environment
    env = GridWorld(width=10, height=10, cell_size=50)
    env.add_random_obstacles(15)
    env.start = (0, 0)
    env.goal = (9, 9)
    
    print(f"Grid Size: {env.width}x{env.height}")
    print(f"Start: {env.start}")
    print(f"Goal: {env.goal}")
    print(f"Obstacles: {(env.grid == 1).sum()}\n")
    
    # Create agent
    agent = SearchAgent(env)
    
    # Test each algorithm
    algorithms = ['bfs', 'ucs', 'astar']
    results = {}
    
    for algo in algorithms:
        print(f"Running {algo.upper()}...")
        try:
            path, cost, expanded = agent.search(algo)
            results[algo] = {
                'path_length': len(path),
                'cost': cost,
                'expanded': expanded,
                'success': path is not None
            }
            print(f"  ✓ Path found! Length: {len(path)}, Cost: {cost}, Expanded: {expanded}")
        except NotImplementedError:
            print(f"  ⚠️  {algo.upper()} not implemented yet")
            results[algo] = {'success': False}
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results[algo] = {'success': False}
    
    # Summary
    print("\n" + "-" * 60)
    print("SUMMARY:")
    print("-" * 60)
    print(f"{'Algorithm':<12} {'Success':<10} {'Path Length':<12} {'Nodes Expanded':<15}")
    print("-" * 60)
    for algo, result in results.items():
        if result['success']:
            print(f"{algo.upper():<12} {'✓':<10} {result['path_length']:<12} {result['expanded']:<15}")
        else:
            print(f"{algo.upper():<12} {'✗':<10} {'-':<12} {'-':<15}")
    print("-" * 60)


def test_logic():
    """Test logic-based agent."""
    print_header("Testing Logic Agent")
    
    if LogicAgent is None:
        print("❌ LogicAgent not implemented yet!")
        print("Please implement agents/logic_agent.py")
        return
    
    # --- 1. Setup the Environment ---
    import time
    # Create a 10x10 world
    env = GridWorld(width=10, height=10, cell_size=60)
    
    # Add random obstacles (but keep start/goal clear)
    env.add_random_obstacles(10) 
    env.start = (0, 0)
    env.goal = (9, 9)
    env.agent_pos = env.start
    
    # Initialize Pygame window
    env.init_display()
    
    # --- 2. Create the Agent ---
    print("Initializing Logic Agent...")
    try:
        agent = LogicAgent(env)
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return

    print("Simulation started! Agent is thinking...")

    # --- 3. Run the Simulation Loop ---
    running = True
    steps = 0
    
    while running:
        # Handle Pygame events (clicking close button, etc.)
        if not env.handle_events():
            running = False
            break
        
        # If we haven't reached the goal yet, run the AI cycle
        if not env.is_goal(env.agent_pos):
            try:
                # The AI Brain Cycle
                agent.perceive()  # 1. Update KB with sensors
                agent.reason()    # 2. Run inference
                agent.act()       # 3. Decide and move
                steps += 1
            except Exception as e:
                print(f"❌ Error during agent execution: {e}")
                import traceback
                traceback.print_exc()
                running = False
        
        # Draw the world
        env.render()
        
        # Slow down slightly so we can watch it move (0.1s delay)
        time.sleep(0.3)

    env.close()
    print(f"\nTest finished. Total steps: {steps}")


def test_probability():
    """Test probabilistic agent."""
    print_header("Testing Probabilistic Agent")
    
    if ProbabilisticAgent is None:
        print("❌ ProbabilisticAgent not implemented yet!")
        print("Please implement agents/probabilistic_agent.py")
        return
    
    # 1. Setup the Visual Environment
    # We use 10x10 because that's the size of the demo map
    print("Loading Professor's Demo Map...")
    env = GridWorld(width=10, height=10, cell_size=60) 
    env.init_display() # Opens the Pygame window
    
    # --- REPLICATING THE DEMO MAP ---
    # These match the black walls from the screenshot.
    # We treat them as PITS (they emit breezes).
    env.add_obstacle(2, 2)
    env.add_obstacle(2, 3)
    env.add_obstacle(2, 4)
    env.add_obstacle(5, 5)
    env.add_obstacle(6, 5)
    env.add_obstacle(7, 5)
    
    # Set Start (Green) and Goal (Red)
    env.start = (1, 1)
    env.goal = (8, 8)
    env.agent_pos = env.start
    
    # 2. Create Agent
    agent = ProbabilisticAgent(env)
    
    print(f"Start: {env.start} -> Goal: {env.goal}")
    print("Agent is thinking...\n")
    
    # 3. Run until we reach the goal or give up
    steps = 0
    max_steps = 60 # Give it plenty of time to walk around walls
    
    while steps < max_steps:
        # Check if user closed window
        if not env.handle_events():
            print("Simulation stopped by user.")
            break
            
        # Draw the current state to the screen
        env.render()
        current_pos = env.agent_pos
        
        # Check Success
        if current_pos == env.goal:
            print("\n🎉 SUCCESS! Reached the Red Square!")
            break
            
        # Print Status
        # --- FIXED LINE: Use agent.sense_breeze instead of env.has_breeze ---
        has_breeze = agent.sense_breeze(current_pos)
        
        sensor_msg = "🌬️ BREEZE!" if has_breeze else "⚪ Clear"
        print(f"Step {steps+1}: {current_pos} | Sensor: {sensor_msg}")
        
        # ACT
        next_move = agent.act()
        
        if next_move:
            env.agent_pos = next_move
            print(f"  Action: Moved to {next_move}")
        else:
            print("  Action: Staying put")
        
        # Check for Death (Stepped on Black Wall)
        r, c = env.agent_pos
        if env.grid[r][c] == 1: # 1 is Obstacle/Pit
            print("\n💀 GAME OVER: Agent fell into a pit!")
            break
            
        steps += 1
        
        # Wait a bit so we can watch the agent move on screen
        time.sleep(0.5) 
        
    print("\n✅ Simulation Ended.")
    
    # Keep window open for a few seconds after finishing so we can see the result
    time.sleep(3)
    env.close()


def test_hybrid():
    """Test hybrid agent."""
    print_header("Testing Hybrid Agent")
    
    if HybridAgent is None:
        print("❌ HybridAgent not implemented yet!")
        print("Please implement agents/hybrid_agent.py")
        return
    
    # 1) Setup a static maze (same layout as probability demo)
    env = GridWorld(width=10, height=10, cell_size=60)
    env.init_display()
    try:
        choice = input("Select hybrid maze difficulty (e/m/h) [h]: ").strip().lower()
    except Exception:
        choice = ""
    maze = 'hard'
    if choice in ('easy','e','1'):
        maze = 'easy'
    elif choice in ('medium','m','2'):
        maze = 'medium'
    
    if maze == 'easy':
        pass # very easy just to show how agent follow A*
    
    elif maze == 'medium': # medium to show search + probabilty usage
        env.add_obstacle(2, 2)
        env.add_obstacle(2, 3)
        env.add_obstacle(2, 4)
        env.add_obstacle(5, 5)
        env.add_obstacle(6, 5)
        env.add_obstacle(7, 5)
        env.add_obstacle(8, 9)
        env.add_obstacle(9, 8)

        
    
    else: # very hard to show hybrid needing logic
        env.add_obstacle(0, 2)
        env.add_obstacle(0, 3)
        env.add_obstacle(0, 4)
        env.add_obstacle(0, 5)
        env.add_obstacle(0, 6)
        env.add_obstacle(0, 7)

        env.add_obstacle(0, 1)
        env.add_obstacle(1, 0)

        env.add_obstacle(2, 2)
        env.add_obstacle(2, 3)
        env.add_obstacle(2, 4)
        env.add_obstacle(2, 5)
        env.add_obstacle(2, 6)

        env.add_obstacle(3, 6)
        env.add_obstacle(4, 6)
        env.add_obstacle(5, 6)
        env.add_obstacle(6, 6)

        env.add_obstacle(3, 8)
        env.add_obstacle(5, 8)
        env.add_obstacle(6, 8)
        env.add_obstacle(7, 8)

        env.add_obstacle(4, 9)

        env.add_obstacle(7, 5)
        env.add_obstacle(1, 9)
        env.add_obstacle(3, 9)
        env.add_obstacle(9, 3)

        env.add_obstacle(3, 4)
        env.add_obstacle(4, 4)
        env.add_obstacle(5, 4)
        env.add_obstacle(6, 4)
        env.add_obstacle(7, 4)

        env.add_obstacle(7, 1)
        env.add_obstacle(8, 1)
        env.add_obstacle(9, 2)
    
    # Start/Goal
    env.start = (1, 1)
    env.goal = (8, 8)
    env.agent_pos = env.start
    
    # 2) Create Hybrid Agent
    agent = HybridAgent(env)
    print(f"Start: {env.start} -> Goal: {env.goal}")
    print("Hybrid agent integrating search + probability + logic")
    
    # 3) Simulation loop
    steps = 0
    max_steps = 80
    running = True
    while running and steps < max_steps:
        if not env.handle_events():
            print("Simulation stopped by user.")
            break
        
        # Visualize
        env.render()
        curr = env.agent_pos
        
        # Goal check
        if env.is_goal(curr):
            print("\n🎉 SUCCESS! Hybrid agent reached the goal.")
            break
        
        # Perception status
        has_breeze = agent.sense_breeze(curr)
        sensor_msg = "🌬️ BREEZE!" if has_breeze else "⚪ Clear"
        print(f"Step {steps+1}: {curr} | Sensor: {sensor_msg}")
        
        # Act (agent updates env.agent_pos internally)
        try:
            agent.act()
        except Exception as e:
            print(f"❌ Error during hybrid act: {e}")
            import traceback
            traceback.print_exc()
            break
        
        # Optional: mark visited for UI tint
        env.visited.add(env.agent_pos)
        
        # Death check
        r, c = env.agent_pos
        if env.grid[r][c] == 1:
            print("\n💀 GAME OVER: Agent fell into a pit!")
            break
        
        steps += 1
        time.sleep(0.4)
    
    # Keep window visible for a moment
    time.sleep(2)
    env.close()

def run_experiments():
    """Run comprehensive experiments."""
    print_header("Running All Experiments")
    print("This will run comprehensive tests and generate performance reports.")
    print("Coming soon...")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="RoboMind - SE444 AI Course Project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo              # Run environment demo
  python main.py --test-search       # Test search algorithms  
  python main.py --test-logic        # Test logic agent
  python main.py --test-probability  # Test probabilistic agent
  python main.py --test-hybrid       # Test hybrid agent
  python main.py --experiment all    # Run all experiments
        """
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='Run environment demonstration')
    parser.add_argument('--test-search', action='store_true',
                       help='Test search algorithms')
    parser.add_argument('--test-logic', action='store_true',
                       help='Test logic-based agent')
    parser.add_argument('--test-probability', action='store_true',
                       help='Test probabilistic agent')
    parser.add_argument('--test-hybrid', action='store_true',
                       help='Test hybrid agent')
    parser.add_argument('--experiment', choices=['all', 'search', 'logic', 'probability'],
                       help='Run experiments')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        print_header("Welcome to RoboMind!")
        print("SE444 - Artificial Intelligence Course Project\n")
        print("To get started, run:")
        print("  python main.py --demo\n")
        print("For all options:")
        print("  python main.py --help\n")
        return
    
    # Run requested mode
    if args.demo:
        run_demo()
    elif args.test_search:
        test_search()
    elif args.test_logic:
        test_logic()
    elif args.test_probability:
        test_probability()
    elif args.test_hybrid:
        test_hybrid()
    elif args.experiment:
        run_experiments()


if __name__ == "__main__":
    main()
