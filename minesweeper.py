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
        if self.count == len(self.cells):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #first check to see if cell is one of the cells included in the sentence
        if cell in self.cells:
        #If cell is in the sentence, the function should update the sentence so that cell is no longer in the sentence, but still represents a logically correct sentence given that cell is known to be a mine.
            self.cells.remove(cell)
        #If cell is not in the sentence, then no action is necessary.

        
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #first check to see if cell is one of the cells included in the sentence.
        if cell in self.cells:
        #If cell is in the sentence, the function should update the sentence so that cell is no longer in the sentence, but still represents a logically correct sentence given that cell is known to be safe.
            self.cells.remove(cell)
        #If cell is not in the sentence, then no action is necessary.
      


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
        print('added cell to mines')
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
          
        """
        self.safes.add(cell)
        ('added cell to  safe')
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        """
        print(f"adding knowledge for move: cell= {cell} count= {count}")
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        print('moves made', self.moves_made)

        # 2) mark the cell as safe
        self.safes.add(cell)
        print('safes', self.safes)

        # 3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        cells=set()
        
        print('cell=', cell)
        for k in range(cell[0]-1, cell[0]+2):
            for l in range(cell[1]-1,cell[1]+2):
                if (k,l) != cell:
                    # if cell in bounds 
                    if 0 <= k < self.height and 0 <= l < self.width:
                        cells.add((k,l))
        sentence = Sentence(cells, count)
        print('sentence=', sentence)
        self.knowledge.append(sentence)

        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base.


        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)
            # iimplies safes? add to safes list
            if sentence.count == 0:
                print('count==0 so adding cells to  safes')
                self.safes.update(sentence.cells)
            # implies mines?  add to mine list
            if len(sentence.cells) == sentence.count:
                self.mines.update(cells)
        




            

        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        myknowledge = self.knowledge
        print('len(self.knowledge)=', len(self.knowledge))

        print('>>>len knowlege=', len(self.knowledge))

        def findsubsetsinknowledge(myknowledge,  newsentence, i=0):
            print('R: len(myknowledge) beg rec=', len(myknowledge))
            # base case
            if i == len(myknowledge)-1:
                print('R: len(myknowledge) at end rec=', len(myknowledge))
                return myknowledge

            # check if sentence is a subset of the next knowledge item
            if newsentence.cells.issubset(myknowledge[i].cells):
                print('R: is subset')
                # get remainder cells
                newcells = myknowledge[i].cells.difference(newsentence.cells)
                print('R: newcells', newcells)
                # get remainder count
                newcount = myknowledge[i].count - newsentence.count
                print('R: newcount', newcount)
                # make new sentence + add to knowledge
                newsentence = Sentence(newcells, newcount)
                if newsentence not in myknowledge:
                    myknowledge.append(newsentence)
                    i+=1
            else:
                print('R: no subsets found')

            i+=1
            # run check on new sentence
            return findsubsetsinknowledge(myknowledge, newsentence, i)
  
        
        self.knowledge = findsubsetsinknowledge(myknowledge, sentence)



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print('\nin safemove fn')
        unplayedsafes=self.safes-self.moves_made
        if len(unplayedsafes) != 0:
            print('unplayedsafes= ',unplayedsafes)
            (print('returninf safe move'))
            return random.choice(list(unplayedsafes))
        else:
            print('return no safes')
            return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        alloptions =set()
        print('in randommove fn')
        for i in range(self.height-1):
            for j in range(self.width-1):
                alloptions.add((i,j))
        # print('alloptions', alloptions)
        randomoptions = alloptions.difference(self.moves_made, self.mines)
        # print('randomoptions', randomoptions)
        print('return randommove')
        return random.choice(list(randomoptions))
        
