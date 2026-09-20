# RoboMind

An AI agent simulation that combines classical search, logical inference, and probabilistic reasoning to navigate uncertain grid-world environments.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-GPL--2.0-blue.svg)](LICENSE)

## Overview

RoboMind explores how an autonomous agent can make decisions in a changing environment. The system models a 2D grid world containing obstacles, goals, and uncertain sensor information. It evaluates multiple AI strategies and combines them into a hybrid agent capable of planning, reasoning, and acting under uncertainty.

The project is designed to demonstrate practical understanding of:

- Path planning and graph search
- Knowledge representation and rule-based inference
- Bayesian reasoning and belief updates
- Agent architecture and decision-making
- Algorithm evaluation and performance analysis

## Key Capabilities

### Search and Path Planning

Implements and compares classical search strategies including:

- Breadth-First Search (BFS)
- Uniform-Cost Search (UCS)
- A* search with configurable heuristics
- Local-search approaches such as simulated annealing

### Logical Reasoning

Uses a knowledge base to represent known facts and derive additional information through rules. This enables the agent to identify safe moves and reason about partially observed areas of the environment.

### Probabilistic Decision-Making

Models noisy sensor readings and updates the agent's beliefs using Bayesian reasoning. This allows the agent to make useful decisions even when the environment cannot be observed perfectly.

### Hybrid Agent Architecture

The hybrid agent combines planning, logic, and probability:

1. Perceive the current environment
2. Update beliefs from sensor observations
3. Infer safe or unsafe actions
4. Plan a route toward the goal
5. Execute the next action and repeat

## Project Structure

```text
.
├── course-project/
│   └── RoboMind/
│       ├── main.py                  # Simulation and experiment entry point
│       ├── environment.py           # Grid-world environment
│       ├── agents/                  # Search, logic, probabilistic, and hybrid agents
│       ├── ai_core/                 # Search, knowledge-base, and Bayesian components
│       ├── utils/                   # Visualization and metrics utilities
│       ├── maps/                    # Example environments
│       └── requirements.txt         # Python dependencies
├── lectures/                        # Supporting technical notes and examples
└── README.md
```

## Getting Started

### Requirements

- Python 3.8 or later
- pip
- Jupyter Notebook, if you want to explore the notebooks and experiments

### Installation

```bash
git clone https://github.com/MADm10d/Robomind-proj.git
cd Robomind-proj/course-project/RoboMind
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

### Run the Simulation

```bash
python main.py --demo
```

Run the available algorithm tests or the complete experiment suite:

```bash
python main.py --test-search
python main.py --test-logic
python main.py --test-probability
python main.py --test-hybrid
python main.py --experiment all
```

## Evaluation

The project supports comparing agents using measurable performance indicators:

| Metric | Purpose |
|---|---|
| Path cost | Measures the cost of reaching the goal |
| Nodes expanded | Indicates search efficiency |
| Success rate | Measures how often an agent completes its objective |
| Execution time | Captures computational performance |
| Belief accuracy | Evaluates probabilistic state estimates |

These metrics make it possible to compare solution quality, computational efficiency, and decision-making reliability across different agent designs.

## Technical Highlights

- Modular separation between environment, agent, reasoning, and evaluation layers
- Reusable search and inference components
- Support for deterministic and uncertain environments
- Visual simulation of agent behavior
- Experiment-oriented design for algorithm comparison
- Python-based implementation with notebook support for analysis

## Why This Project Matters

RoboMind demonstrates how foundational AI techniques can be combined into an end-to-end autonomous system. Rather than treating an algorithm in isolation, the project focuses on the engineering challenge of integrating perception, reasoning, planning, and action into a single decision loop.

This makes the project relevant to work involving:

- Robotics and autonomous systems
- Route planning and optimization
- Decision-support systems
- Simulation and experimentation
- Intelligent software agents
- Applied machine learning and AI research

## Documentation

- [RoboMind project documentation](course-project/RoboMind/README.md)
- [Lecture notes and technical material](lectures/)
- [Course policies](syllabus/policies.md)

## Future Improvements

Potential extensions include:

- Dynamic obstacles and changing goals
- More advanced localization and particle filtering
- Multi-agent coordination
- Learning-based action selection
- Additional benchmark environments
- Automated experiment reports and dashboards

## Author

**MADm10d**

If you are interested in the implementation or would like to discuss the design decisions, feel free to explore the source code and open an issue.
