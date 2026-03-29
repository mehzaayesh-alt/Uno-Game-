# UNO AI Game (Minimax vs Expectimax)

## Overview

This project is a simplified UNO game implemented in Python for an AI assignment.
It compares two algorithms: **Minimax (defensive)** and **Expectimax (offensive)**.

## Game Rules

* Match card by **color or number**
* **Skip card** skips next player
* If no move then **draw a card**
* First player to finish cards wins

## AI Approach

* **Minimax**: assumes worst-case, plays safely
* **Expectimax**: uses probability, plays aggressively

## Evaluation Function

Based on:

* own cards (less is better)
* opponents' cards
* skip cards


## Conclusion

Expectimax performs better due to handling randomness, while Minimax is more defensive.

## Author

Mehza Ayesh
FAST NUCES Islamabad
