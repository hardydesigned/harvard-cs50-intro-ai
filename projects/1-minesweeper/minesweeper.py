import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        if len(self.cells) == self.count and self.count != 0:
            mines = self.cells

        return mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes = set()
        if self.count == 0:
            safes = self.cells

        return safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        # 1) Mark the cell as a move made
        self.moves_made.add(cell)

        # 2) Mark the cell as safe
        self.mark_safe(cell)

        # 3) Add a new sentence to the knowledge base
        neighbors = set()
        row, col = cell
        for i in range(max(0, row - 1), min(self.height, row + 2)):
            for j in range(max(0, col - 1), min(self.width, col + 2)):
                neighbor = (i, j)
                if neighbor != cell and neighbor not in self.moves_made:
                    if neighbor not in self.mines and neighbor not in self.safes:
                        neighbors.add(neighbor)
                    elif neighbor in self.mines:
                        count -= 1  # Decrement count for known mines

        if neighbors:
            new_sentence = Sentence(neighbors, count)
            self.knowledge.append(new_sentence)

        # 4) Mark any additional cells as safe or as mines
        while True:
            updated = False

            for sentence in self.knowledge.copy():
                known_mines = sentence.known_mines()
                known_safes = sentence.known_safes()

                if known_mines:
                    updated = True
                    for mine in known_mines.copy():
                        self.mark_mine(mine)

                if known_safes:
                    updated = True
                    for safe in known_safes.copy():
                        self.mark_safe(safe)

                # Clean up sentences that are now empty or trivially true
                if not sentence.cells:
                    self.knowledge.remove(sentence)

            # Stop if no new updates were made
            if not updated:
                break

        # 5) Infer new sentences
        inferred_sentences = []
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count
                    inferred_sentence = Sentence(new_cells, new_count)
                    if inferred_sentence not in self.knowledge and inferred_sentence not in inferred_sentences:
                        inferred_sentences.append(inferred_sentence)

        # Add inferred sentences to the knowledge base
        self.knowledge.extend(inferred_sentences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        if len(self.moves_made) == self.height * self.width:
            return None
        
        random_height = random.randint(0, self.height - 1)
        random_width = random.randint(0, self.width - 1)

        while (random_height, random_width) in self.moves_made or (random_height, random_width) in self.mines:
            random_height = random.randint(0, self.height - 1)
            random_width = random.randint(0, self.width - 1)

        return (random_height, random_width)
    


# board = Minesweeper(4, 4, 15)
# print(board.print())
# # ai = MinesweeperAI(4, 4)
# # print(ai.make_safe_move())
# s = Sentence({(1, 1), (1, 2), (2, 1), (2, 2)}, 4)
# print(s.known_mines())

def print_ai_status(ai):
    print(f'\nAfter move:{move} with nearby_count:{nearby_count}')
    if ai.knowledge:
        print('Sentences in Knowledge Base:')
        for cnt, s in enumerate(ai.knowledge):
            print(f'{cnt}: {s}')
    else:
        print('NO Sentences in Knowledge Base.')       
    # print(f'Safe Cells: {sorted(list(ai.safes))}')
    # print(f'Mine Cells: {sorted(list(ai.mines))}')    
    print(f'Safe Cells: {ai.safes}')
    print(f'Mine Cells: {ai.mines}')    

    
# Create AI agent
HEIGHT, WIDTH, MINES = 8, 8, 8
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Test new sentence logic (3rd requirement)
move, nearby_count = (1,1), 0
ai.add_knowledge(move,nearby_count)
print_ai_status(ai)

move, nearby_count = (2,2), 2
ai.add_knowledge(move,nearby_count)
print_ai_status(ai)

# Test inference logic for new safes or mines (4th requirement)
move, nearby_count = (3,3), 0
ai.add_knowledge(move,nearby_count)
print_ai_status(ai)




# Expected output:
# After move:(1, 1) with nearby_count:0
# NO Sentences in Knowledge Base.
# Safe Cells: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
# Mine Cells: []

# After move:(2, 2) with nearby_count:2
# Sentences in Knowledge Base:
# 0: {(3, 2), (1, 3), (2, 3), (3, 3), (3, 1)} = 2
# Safe Cells: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
# Mine Cells: []

# After move:(3, 3) with nearby_count:0
# NO Sentences in Knowledge Base.
# Safe Cells: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4)]
# Mine Cells: [(1, 3), (3, 1)]



# Setup for new sentence inference logic test
move, nearby_count = (4,2), 1
ai.add_knowledge(move,nearby_count)
print_ai_status(ai)

# Tests subset inference logic for new sentences (5th requirement)
move, nearby_count = (7,2), 2
ai.add_knowledge(move,nearby_count)
print_ai_status(ai)

move, nearby_count = (5,2), 1
ai.add_knowledge(move,nearby_count)
print_ai_status(ai)

# Here is the output after the last move:
# After move:(5, 2) with nearby_count:1
# Sentences in Knowledge Base:
# 0: {(7, 3), (7, 1)} = 1
# 1: {(6, 3), (6, 1), (6, 2)} = 1
# Safe Cells: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3), (4, 4), (5, 1), (5, 2), (5, 3), (7, 2)]
# Mine Cells: [(1, 3), (3, 1)]
