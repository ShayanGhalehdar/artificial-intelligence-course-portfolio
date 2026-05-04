# Artificial Intelligence Course Portfolio

Cleaned portfolio repository for selected implementations from my undergraduate Artificial Intelligence course at Sharif University of Technology.

The course introduced AI from both theoretical and practical perspectives, including intelligent agents, state-space search, knowledge representation and inference, and machine learning. The official syllabus also lists topics such as informed search, local search, CSPs, adversarial search, MDPs, reinforcement learning, Bayesian networks, temporal probability models, decision trees, logistic regression, perceptron, neural networks, robustness, and applications in RL/NLP/CV.

## Repository Contents

```text
01-search-and-optimization/
  a_star_elevator.ipynb
  simulated_annealing_knapsack.ipynb
  drawer.py
  assets/

02-csp-and-adversarial-search/
  cryptarithmetic_csp.ipynb
  adversarial_search_game.ipynb
  player_minimax.py

03-reinforcement-learning/
  rl_sentence_generator.ipynb

04-probabilistic-reasoning/
  bayesian_network_inference.ipynb

05-machine-learning/
  decision_tree_from_scratch.ipynb
  logistic_regression_from_scratch.ipynb
```

## Topics Covered

- Intelligent agents and state-space problem formulation
- Uninformed and informed search, including DFS and A*
- Local search and simulated annealing
- Constraint satisfaction and backtracking search
- Adversarial search and heuristic game-playing agents
- Markov decision processes and reinforcement learning
- Bayesian networks, factor operations, enumeration, and variable elimination
- Decision trees and logistic regression implemented from scratch

## Academic Integrity / Copyright Note

This repository is designed as a portfolio-style archive of my own implementations and learning outcomes. Official assignment PDFs, textbook PDFs, instructor solution manuals, grading instructions, test files, and copyrighted course material are intentionally excluded.

If this repository is made public, it should remain a cleaned portfolio version rather than a full dump of course submissions. For private archival use, keep any official course material outside the public repository.

## Setup

Create an environment and install the common dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Some notebooks were originally written for Google Colab or a course-provided environment and may need small path/import adjustments before running locally.
