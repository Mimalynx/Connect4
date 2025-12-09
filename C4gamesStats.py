class Node:
    def __init__(self):
        self.children = {}
        self.count = 0
        self.playerOnesTurn = True
        self.winCount = 0

root = Node()

movesInGames = []
whoWon = []
with open("ListOfAnalysisOfGames.txt", "r") as f:
    for line in f:
        parts = line.strip().split(",")
        movesInGames.append(parts[2])
        whoWon.append(int(parts[0]) % 2 != 0)

for i in range(len(movesInGames)):
    current = root
    current.count += 1
    current.playerOnesTurn = True
    if whoWon[i]:
        current.winCount += 1

    for move in movesInGames[i]:
        if move not in current.children:
            current.children[move] = Node()

        current.children[move].playerOnesTurn = not current.playerOnesTurn
        current = current.children[move]
        if whoWon[i] == current.playerOnesTurn:
            current.winCount += 1
        current.count += 1

for i in range(1,8):
    print(root.children["4"].children["3"].children[str(i)].count)
    print(root.children["4"].children["3"].children[str(i)].winCount)