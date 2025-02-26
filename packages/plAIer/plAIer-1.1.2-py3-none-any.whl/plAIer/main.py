import json
import threading
import os

lock = threading.Lock()

class game():
    jsonDataFile = None
    data = None
    outcomesRating = None
    gameStates = None
    isFinished = None
    
    def __init__(self, jsonDataFile, outcomesRating):
        if not os.path.exists(jsonDataFile): # If the database file doesn't exist
            raise FileNotFoundError("Database file not found !")
        
        try:
            self.jsonDataFile = jsonDataFile
        except json.decoder.JSONDecodeError:
            raise json.decoder.JSONDecodeError("The JSON file is malformed !")
        
        self.data = eval(str(json.load(open(jsonDataFile))))
        
        if not list(outcomesRating.keys()) == self.data["outcomes"]:
            raise ValueError("The outcomes model is not properly filled out.")
        for outcome in self.data["outcomes"]:
            if type(outcomesRating[outcome]) != int and type(outcomesRating[outcome]) != float:
                raise ValueError("The outcomes model is not properly filled out.")
        self.outcomesRating = outcomesRating
        self.gameStates = []
        self.isFinished = False


    def findBestMove(self, possibleMoves):
        """Find the best move based on the game state."""
        
        if self.isFinished: # If the game is already finished
            raise RuntimeError("This game is already finished !")
        
        if possibleMoves == []: # If there are no possible moves
            raise ReferenceError("No possible move has been proposed.")

        # If the AI does not recognize one of the proposed moves, create an empty model
        emptyJson = {}
        for outcome in self.data["outcomes"]:
            emptyJson[outcome] = 0
        for possibleMove in possibleMoves:
            if not possibleMove["stateAfterMove"] in self.data["moves"]:
                self.data["moves"][possibleMove["stateAfterMove"]] = dict(emptyJson)

        # Find the common characters among all the boards
        commonCharIndexes = []
        try:
            for i in range(len(possibleMoves[0]["stateAfterMove"])):
                char = possibleMoves[0]["stateAfterMove"][i]
                matchingChar = True
                for move in possibleMoves:
                    if move["stateAfterMove"][i] != char:
                        matchingChar = False
                if matchingChar:
                    commonCharIndexes.append(i)
        except IndexError:
            pass
        
        # Determine the best move
        expectation = None
        plannedMove = None
        for possibleMove in possibleMoves:
            possibleMoveWithoutCommonCharacters = generateBoardWithoutCommonCharacters(possibleMove["stateAfterMove"], commonCharIndexes)
            moveStatistics = self.data["moves"][possibleMove["stateAfterMove"]]
            moveExpectation = 0
            
            for i in range(len(moveStatistics)):
                moveExpectation += self.outcomesRating[list(moveStatistics.keys())[i]] * list(moveStatistics.values())[i]
            try:
                moveExpectation = moveExpectation/sum(list(moveStatistics.values()))
            except ZeroDivisionError:
                pass

            # Calculate the similarity with the different game boards already encountered
            for possibleMove1, possibleMove1outcomes in self.data["moves"].items():
                possibleMove1WithoutCommonCharacters = generateBoardWithoutCommonCharacters(possibleMove1, commonCharIndexes)
                for outcomeName, outcomeValue in self.outcomesRating.items():
                    moveExpectation += difference(possibleMoveWithoutCommonCharacters, possibleMove1WithoutCommonCharacters) * outcomeValue * possibleMove1outcomes[outcomeName]
            
            if expectation == None or expectation < moveExpectation:
                expectation = moveExpectation
                plannedMove = possibleMove
        
        self.gameStates.append(plannedMove["stateAfterMove"]) # Save the move to know if it was a successful move
        return plannedMove["move"]


    def setOutcome(self, outcome):
        """Tell the AI what the outcome of the game is."""
        
        if not outcome in self.outcomesRating.keys(): # If the provided outcome doesn't exist
            raise ValueError(f"The item '{outcome}' is not in the expected outcomes list.")
        
        lock.acquire() # In case the file is used by two different instances of the program
        self.isFinished = True
        importedJson = eval(str(json.load(open(self.jsonDataFile)))) # Import the data from the original file

        # If the AI made a move not known to the database
        emptyJson = {}
        for outcome1 in self.data["outcomes"]:
            emptyJson[outcome1] = 0
            
        for gameState in self.gameStates: # Save the outcome of the game
            if not gameState in importedJson["moves"]:
                importedJson["moves"][gameState] = dict(emptyJson)
            importedJson["moves"][gameState][outcome] += 1
        json.dump(importedJson, open(self.jsonDataFile, 'w'))
        lock.release()



def generateBoardWithoutCommonCharacters(board, commonCharactersIndexes):
    """Remove identical characters from all game boards."""
    boardGameWithoutCommonCharacters = ""
    for characterIndex in range(len(board)):
        if not characterIndex in commonCharactersIndexes:
            boardGameWithoutCommonCharacters += board[characterIndex]
    return boardGameWithoutCommonCharacters


def difference(s1, s2):
    "Obtain a coefficient between 0 and 1 as follows: the closer the coefficient is to 1, the more similar s1 and s2 are."
    if len(s1) < len(s2):
        return difference(s2, s1)
    elif len(s2) == 0:
        return 0

    previousRow = [n for n in range(max(0, len(s2) + 1))]
    for indexS1, c1 in enumerate(s1):
        currentRow = [0] * (len(s2) + 1)
        currentRow[0] = indexS1 + 1
        for indexS2, c2 in enumerate(s2):
            currentRow[indexS2 + 1] = min(previousRow[indexS2 + 1] + 1,
                                          currentRow[indexS2] + 1,
                                          previousRow[indexS2] + (c1 != c2))
        previousRow = currentRow

    distance = currentRow[-1]
    maxLen = max(len(s1), len(s2))
    return 1 - distance / maxLen


def createDatabase(filename, name, description, outcomes):
    """Create a new database."""
    
    if os.path.exists(filename): # If the file already exists
        raise FileExistsError(f"The file '{filename}' already exists")

    # Create a new database
    databaseContent = {"name": name, "description": description, "outcomes": outcomes, "moves":{}}
    database = json.dump(databaseContent, open(filename, 'w'))

