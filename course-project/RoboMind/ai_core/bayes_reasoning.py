"""
Bayesian Reasoning Module
SE444 - Artificial Intelligence Course Project

Implemented by: Amr Issa/230265
Phase 3 (Week 5-6)
"""

from typing import Dict, Tuple

def bayes_update(prior: float, likelihood: float, total_prob: float) -> float:
    """
    Standard Bayes rule implementation.
    P(H|E) = (P(E|H) * P(H)) / P(E)
    """
    # avoid division by zero if evidence is impossible
    if total_prob == 0:
        return 0.0
        
    return (likelihood * prior) / total_prob


def compute_evidence(prior: float, prob_if_true: float, prob_if_false: float) -> float:
    """
    Calculates the total probability of the evidence (normalization factor).
    P(E) = P(E|H)P(H) + P(E|~H)P(~H)
    """
    prior_false = 1.0 - prior
    
    # weighted sum of probabilities
    evidence = (prob_if_true * prior) + (prob_if_false * prior_false)
    return evidence


def sensor_model(has_pit: bool, accuracy: float = 0.9) -> Tuple[float, float]:
    """
    Returns the probability of the sensor beeping (True) vs silent (False)
    given the actual state of the cell.
    """
    if has_pit:
        # If there is a pit: accuracy= (0.9), error =(0.1) 
        return accuracy, 1.0 - accuracy
    else:
        # If there is no pit:
        # Chance of false alarm = error (0.1) which is false positive
        # Chance of silence (correct) = accuracy (0.9)
        return 1.0 - accuracy, accuracy


def update_belief_map(belief_map: Dict[Tuple[int, int], float],
                      is_breeze: bool,
                      current_pos: Tuple[int, int], 
                      sensor_accuracy: float = 0.9) -> Dict[Tuple[int, int], float]:
    """
    Updates the probability grid based on the sensor reading.
    NOTE: Only updates neighbors of the current position!
    """
    new_grid = belief_map.copy()
    
    # Get neighbors (Up, Down, Left, Right)
    r, c = current_pos
    neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
    
    # Iterate through neighbors and apply Bayes' rule
    for nx, ny in neighbors:
        
        # Make sure neighbor is actually in our grid
        if (nx, ny) in belief_map:
            prior_belief = belief_map[(nx, ny)]
            
            # Get the likelihoods from the sensor model
            # we need: P(Breeze | Pit) and P(Breeze | No Pit)
            
            p_breeze_if_pit, p_no_breeze_if_pit = sensor_model(True, sensor_accuracy)
            p_breeze_if_safe, p_no_breeze_if_safe = sensor_model(False, sensor_accuracy)
            
            if is_breeze:
                # we felt a breeze, so we use the "Detection" probabilities
                likelihood = p_breeze_if_pit      # 0.9
                likelihood_false = p_breeze_if_safe # 0.1
            else:
                # No breeze, use the "Miss/Correct" probabilities
                likelihood = p_no_breeze_if_pit      # 0.1
                likelihood_false = p_no_breeze_if_safe # 0.9

            # 1. Compute Normalization (Total Evidence)
            total_prob = compute_evidence(prior_belief, likelihood, likelihood_false)
            
            # 2. Compute Posterior (New Belief)
            posterior = bayes_update(prior_belief, likelihood, total_prob)
            
            # 3. Update the grid
            new_grid[(nx, ny)] = posterior

    return new_grid


# ============================================================================
# Testing Code 
# ============================================================================

if __name__ == "__main__":
    print("--- Testing Math Functions ---")
    
    # Test 1: Simple Bayes
    # Disease example (Standard test case)
    p_sick = 0.01
    p_pos_if_sick = 0.95
    p_pos_if_healthy = 0.10
    
    ev = compute_evidence(p_sick, p_pos_if_sick, p_pos_if_healthy)
    post = bayes_update(p_sick, p_pos_if_sick, ev)
    
    print(f"Medical Test: P(Disease|Positive) should be ~8.7%. Calculated: {post*100:.2f}%")

    # Test 2: Grid Update
    print("\n--- Testing Grid Update ---")
    
    # Fake map with 3 cells
    # (0,1) is the neighbor of (0,0)
    test_grid = {(0,0): 0.0, (0,1): 0.2, (1,0): 0.2}
    
    print(f"Prior at (0,1): {test_grid[(0,1)]}")
    print("Agent at (0,0) feels BREEZE.")
    
    # NOTE: We must pass agent position (0,0) now
    updated = update_belief_map(test_grid, is_breeze=True, current_pos=(0,0))
    
    print(f"Posterior at (0,1): {updated[(0,1)]:.4f}")
    
    if updated[(0,1)] > 0.2:
        print("Success: Probability increased!")
    else:
        print("Fail: Probability did not increase.")
