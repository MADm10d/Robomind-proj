"""
Knowledge Base - Logic Reasoning Module
SE444 - Artificial Intelligence Course Project

Implemented by: Abdulaziz Altamimi 230714
Phase 2 (Week 3-4)
"""

from typing import Set, List


class KnowledgeBase:
    """
    A simple knowledge base for propositional logic.
    
    Stores facts and rules, performs forward chaining inference.
    """
    
    def __init__(self):
        """Initialize empty knowledge base."""
        self.facts = set()   # Known facts: "Safe(2,3)", "Obstacle(4,5)"
        self.rules = []      # Rules: ("A", "B", "C") means "A AND B → C"
    
    def tell(self, fact: str):
        """
        Add a fact to the knowledge base.
        
        Args:
            fact: A proposition like "Safe(2,3)" or "Explored(5,6)"
        
        Example:
            >>> kb = KnowledgeBase()
            >>> kb.tell("Safe(2,3)")
            >>> kb.tell("Free(2,3)")
        """

        if (fact in self.facts): # If the fact already exists in the knowledge base, skip it
            return

        self.facts.add(fact) # Adding the fact into the  facts set for the knowledge base
        print(f"Added fact: {fact}")
    
    def add_rule(self, premises: List[str], conclusion: str):
        """
        Add an inference rule.
        
        Args:
            premises: List of propositions that must all be true
            conclusion: Proposition that follows from premises
        
        Example:
            >>> kb.add_rule(["Safe(X)", "Free(X)"], "CanMove(X)")
            This means: If Safe(X) AND Free(X) then CanMove(X)
        """

        self.rules.append((premises, conclusion)) # Adding the premises and conclusion from a rule into the rules array for the knowledge base 
        print(f"Added rule: {' AND '.join(premises)} → {conclusion}")
    
    def ask(self, query: str) -> bool:
        """
        Check if a query can be inferred from the knowledge base.
        
        Args:
            query: A proposition to check
        
        Returns:
            True if query is known or can be inferred, False otherwise
        
        Example:
            >>> kb.ask("Safe(2,3)")
            True
        """

        self.infer() # Perform inference to derive new facts from the rules before completing the query
        return query in self.facts # If query exists in the facts set, it will return true
    
    def infer(self):
        """
        Apply forward chaining to derive new facts from rules.
        
        Forward chaining:
            1. For each rule: check if all premises are satisfied
            2. If yes, add conclusion to facts
            3. Repeat until no new facts can be derived
        
        Example:
            >>> kb.tell("Safe(2,3)")
            >>> kb.tell("Free(2,3)")
            >>> kb.add_rule(["Safe(2,3)", "Free(2,3)"], "CanMove(2,3)")
            >>> kb.infer()
            >>> kb.ask("CanMove(2,3)")
            True
        """

        fact_added = True # A variable to track if new facts are being added 
        
        while fact_added: # Loop runs as long as new facts are being added to the knowledge base
            fact_added = False
            for premises, conclusion in self.rules: # Loop through premises and conclusions in the rules array
                if conclusion in self.facts: # Checking if conclusion is already infered and added to knowledge base
                    continue
                
                all_premises_exist = True 

                for i in premises: # Loop through each individual premise and checking if it any of them don't exist in the knowledge base
                    if(i not in self.facts):
                        all_premises_exist = False
                        break

                if all_premises_exist: # If all premises are in the knowledge base add the conclusion as a fact in the knowledge base    
                    self.facts.add(conclusion)
                    fact_added = True
    
    def __str__(self) -> str:
        """String representation of KB."""
        return f"KB with {len(self.facts)} facts and {len(self.rules)} rules"


# ============================================================================
# Testing Code
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Testing Knowledge Base")
    print("=" * 60 + "\n")
    
    # Create KB
    kb = KnowledgeBase()
    
    # Add some facts
    print("Adding facts...")
    kb.tell("Safe(2,3)")
    kb.tell("Free(2,3)")
    kb.tell("Adjacent(2,3,2,4)")
    
    # Add some rules
    print("\nAdding rules...")
    kb.add_rule(["Safe(2,3)", "Free(2,3)"], "CanMove(2,3)")
    kb.add_rule(["Safe(2,3)", "Adjacent(2,3,2,4)", "Free(2,4)"], "SafePath(2,3,2,4)")
    
    # Query
    print("\nQuerying...")
    print(f"Is Safe(2,3) known? {kb.ask('Safe(2,3)')}")
    print(f"Is Obstacle(2,3) known? {kb.ask('Obstacle(2,3)')}")
    
    # Try inference
    print("\nTrying inference...")
    try:
        kb.infer()
        print(f"After inference, is CanMove(2,3) known? {kb.ask('CanMove(2,3)')}")
    except NotImplementedError:
        print("⚠️  Forward chaining not implemented yet!")
    
    print(f"\n{kb}")
    print("\n💡 Tip: Implement forward chaining to automatically derive new facts!")