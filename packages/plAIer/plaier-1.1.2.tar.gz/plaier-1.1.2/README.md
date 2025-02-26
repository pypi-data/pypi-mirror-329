# plAIer

A Python library that uses a reinforcement learning AI to play board games such as Chess, Tic Tac Toe, and Reversi.

You can also find the project on [PyPI][]

[PyPI]: https://pypi.org/project/plAIer/

## Example of use
```python
# The current game state :
gameState = """
 X | O | 
---+---+---
 O | O | X
---+---+---
 X |   | O
"""

# Import the library :
import plAIer

# Create database if not exists :
plAIer.createDatabase("database_filename.json", "database_name", "description", ["outcomes", "list"])

# Initialize the AI :
outcomesRating = {"O won": 1, "tie": 0, "X won": -1} # The definition of outcomes allows us to determine what the goals of the AI are.
AI = plAIer.Game("database_filename.json", outcomesRating)

# Find the best move in the current game position :
bestMove = AI.findBestMove([
    {"move" : "[0, 2]",
        "stateAfterMove": "\n X | O | O\n---+---+---\n O | O | X\n---+---+---\n X |   | O\n"},
    {"move" : "[2, 1]",
        "stateAfterMove": "\n X | O | \n---+---+---\n O | O | X\n---+---+---\n X | O | O\n"}
])

print(eval(bestMove)) # Output : [2, 1]

# Tell the AI what the outcome of the game is :
AI.setOutcome("O won")
```
### Optimization
For better prediction of the best move to play, please ensure that the format of the given board is always the same. Example with tic-tac-toe :
- Board 1 : OXO|OXX|XOO ✅
- Board 2 : XXO|OOO|XOX ✅
- Board 3 : OOX XOO XXO ❌

### Database format
Databases are JSON files which follow this format :
```json
{
    "name": "name of the game",
    "description": "additional informations",
    "outcomes": ["list", "of", "outcomes"],
    "moves": {"gameState1": {"outcome1": 1234, "outcome2": 2345, "outcomeN": 4567},
             "gameState2": {"outcome1": 5678, "outcome2": 6789, "outcomeN": 7890},
             "gameStateN": {"outcome1": 8901, "outcome2": 9011, "outcomeN": 0}
    }
}
```

## How to get it
Write in your terminal (bash or Windows cmd/powershell) the following command :
```bash
pip install plAIer
```

## Contribute
Don't hesitate to contribute with pull requests :
1. Fork the repository
2. Do your commits
3. Add your pull request on the repository with a description of what your pull request does