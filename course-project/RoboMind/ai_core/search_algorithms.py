
from typing import Tuple, List, Optional
from collections import deque
import heapq


    # Breadth-First Search - Find shortest path in terms of number of steps.
def bfs(env, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List], float, int]:
    
    
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    expanded = 0
    
    while queue:
        current = queue.popleft()
        expanded += 1
        
        if current == goal:
            path = reconstruct_path(parent, start, goal)
            cost = len(path) - 1  
            return path, cost, expanded
        
        for neighbor in env.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None, float('inf'), expanded
    
    raise NotImplementedError("BFS not implemented yet - this is your task!")
    
   
# Uniform Cost Search - Find path with lowest total cost.
def ucs(env, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List], float, int]:
    
    frontier = [(0, start)]
    explored = set()
    cost_so_far = {start: 0}
    parent = {start: None}
    expanded = 0

    while frontier: 
        current_cost, current = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.add(current)
        expanded += 1

        if current == goal:
            path = reconstruct_path(parent, start, goal)
            return path, current_cost, expanded
        
        for neighbor in env.get_neighbors(current):
            new_cost = current_cost + env.get_cost(current, neighbor)

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(frontier, (new_cost, neighbor))

    return None, float('inf'), expanded

    raise NotImplementedError("UCS not implemented yet - this is your task!")
    
# A* Search - Find optimal path using cost + heuristic.
def astar(env, start: Tuple[int, int], goal: Tuple[int, int], 
          heuristic='manhattan') -> Tuple[Optional[List], float, int]:
    
    if heuristic == 'manhattan':
        h = lambda pos: env.manhattan_distance(pos, goal)
    elif heuristic == 'euclidean':
        h = lambda pos: env.euclidean_distance(pos, goal)
    else:
        raise ValueError(f"Unknown heuristic: {heuristic}")
    
    g_score = {start: 0}
    f_score = {start: h(start)}
    frontier = [(f_score[start], start)]
    explored = set()
    parent = {start: None}
    expanded = 0

    while frontier:
        current_f, current = heapq.heappop(frontier)
        
        if current in explored:
            continue
        
        explored.add(current)
        expanded += 1
        
        if current == goal:
            path = reconstruct_path(parent, start, goal)
            return path, g_score[current], expanded
        
        for neighbor in env.get_neighbors(current):
            if neighbor in explored:
                continue
            
            tentative_g = g_score[current] + env.get_cost(current, neighbor)
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h(neighbor)
                parent[neighbor] = current
                heapq.heappush(frontier, (f_score[neighbor], neighbor))
    
    return None, float('inf'), expanded
   
    
    raise NotImplementedError("A* not implemented yet - this is your task!")
    
# Reconstructing path from parent pointers
def reconstruct_path(parent: dict, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
   
    path = []
    current = goal 

    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()

    if path and path[0] == start:
        return path
    else:
        return[]
    
    raise NotImplementedError("Path reconstruction not implemented yet!")


if __name__ == "__main__":
    from environment import GridWorld
    
    print("=" * 60)
    print("  Testing Search Algorithms")
    print("=" * 60 + "\n")
    
    # Create a test environment
    env = GridWorld(width=10, height=10)
    
    # Add obstacles
    for i in range(3, 8):
        env.add_obstacle(i, 5)
    
    start = (0, 0)
    goal = (9, 9)
    
    print(f"Grid: {env.width}x{env.height}")
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    print(f"Obstacles: {(env.grid == 1).sum()}\n")
    
    # Test each algorithm
    algorithms = [
        ('BFS', lambda: bfs(env, start, goal)),
        ('UCS', lambda: ucs(env, start, goal)),
        ('A* (Manhattan)', lambda: astar(env, start, goal, 'manhattan')),
        ('A* (Euclidean)', lambda: astar(env, start, goal, 'euclidean')),
    ]
    
    results = []
    
    for name, algo_func in algorithms:
        print(f"\nTesting {name}...")
        print("-" * 40)
        try:
            path, cost, expanded = algo_func()
            if path:
                print(f"✓ Success!")
                print(f"  Path length: {len(path)} steps")
                print(f"  Path cost: {cost:.2f}")
                print(f"  Nodes expanded: {expanded}")
                results.append((name, True, len(path), cost, expanded))
            else:
                print(f"✗ No path found")
                results.append((name, False, 0, 0, 0))
        except NotImplementedError:
            print(f"⚠️  Not implemented yet")
            results.append((name, False, 0, 0, 0))
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append((name, False, 0, 0, 0))
    
    # Summary table
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"{'Algorithm':<20} {'Status':<10} {'Length':<8} {'Cost':<8} {'Expanded':<10}")
    print("-" * 60)
    
    for name, success, length, cost, expanded in results:
        status = "✓" if success else "✗"
        length_str = str(length) if success else "-"
        cost_str = f"{cost:.2f}" if success else "-"
        expanded_str = str(expanded) if success else "-"
        print(f"{name:<20} {status:<10} {length_str:<8} {cost_str:<8} {expanded_str:<10}")
    
    print("-" * 60)
    print("\n💡 Tip: Implement the algorithms one at a time and test each one!")
    print("   Start with BFS (simplest), then UCS, then A*\n")

