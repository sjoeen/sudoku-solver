from sudoku_reader import Sudoku_reader
import time


class Board:
    # It is your task to subclass this in order to make it more fit
    # to be a sudoku board

    def __init__(self,nums):
        # Nums parameter is a 2D list, like what the sudoku_reader returns
        self.n_rows = len(nums[0])
        self.n_cols = len(nums)
        self.nums = [[nums[i][j] for j in range(self.n_cols)] for i in range(self.n_rows)]
            #instead of implementing a seperate set up nums function i did it directly
            #with a simple list comprehension 


    def __str__(self):
        r = "Board with " + str(self.n_rows) + " rows and " + str(self.n_cols) + " columns:\n"
        r += "[["
        for num in self.nums:
            for elem in num:
                r += elem.__str__() + ", "
            r = r[:-2] + "]" + "\n ["
        r = r[:-3] + "]\n\n"
        return r




class Square:

    def __init__(self,row,column,num,board):
        """
        This function represents a single square and the necessary operations to 
        the square to solve the sudoku puzzle.

        it also stores the row number and column number.
        """

        self.row = row
        self.column = column
        self.num = num
        self.board = board


    def is_legal(self, new_num):
        """
        When playing sudoku, you can't have the same number in a row,column and 3x3 grid/box, 
        therefore the square needs to check if the new number is inside these parameters.
        A number needs to be in the range 1-9 also. 

        Chapt gpt helped me understand and break down the subgrid/box seperation.
        """

        row = self.board[self.row]
        col = [self.board[i][self.column] for i in range(9)]
            #the column is the same index postion on all nine lists.
        
        subgrid_start_row = (self.row // 3) * 3
        subgrid_start_col = (self.column // 3) * 3
            #to divide the boxes we do fulltime division so we only work with 0,3,6 instead
            # of 0-8.

        subgrid = [self.board[i][j] for i in range(subgrid_start_row, subgrid_start_row + 3)
                                for j in range(subgrid_start_col, subgrid_start_col + 3)]
            #Loops over the three next indexes in both row and column and saves them as as
            #new values. Chat gpt helped me with the list comprehension and the understanding
            #of what to do here. 

        if new_num in row or new_num in col or new_num in subgrid:
            return False
        elif new_num < 1 or new_num > 9:  
            # Corrected this line to ensure valid Sudoku numbers
            return False

        return True
            #return True if none of the conditons above is filled.

    
    def change_num(self,new_num):

        if self.is_legal(new_num):
            self.num = new_num


    def __str__(self):
        return f"\n\n\nrow:{self.row},\ncolumn{self.column}\nnum{self.num}"
            #Used in testing. 


class Element:
    """
    The element class represents a single row, column or box. it's based on the same
    code used in the is_legal method inside the Square class. 
    """

    def __init__(self, row, column,board):
        self.board = board
        self.row = row
        self.column = column


    def row_lists(self):
        row_list = self.board[self.row]
        return row_list


    def column_lists(self):

        col_list = [self.board[i][self.column] for i in range(9)]

        return col_list
    

    def box_lists(self):
        subgrid_start_row = (self.row // 3) * 3
        subgrid_start_col = (self.column // 3) * 3

        subgrid = [self.board[i][j] for i in range(subgrid_start_row, subgrid_start_row + 3)
                            for j in range(subgrid_start_col, subgrid_start_col + 3)]

        
        return subgrid




class Sudoku_board(Board):
    """"
    Sudoku board is a subclass of the board class. it uses the nums variable 
    which sets up the board. It has the ability to set up elements and solve
    equations. it also has a few help functions for the solving algoritm. 
    """  

    def _set_up_elements(self,row,column):
        """
        Return the row,column or box using the given row and column.
        """
        
        elements = Element(row,column,self.nums)
        row = (elements.row_lists())
        column = (elements.column_lists())
        box =(elements.box_lists())
        
        return row, column, box


    def solve(self):
        """
        A solving algoritm created using the brute-force method.
        I took inspiration from a github code linked below and 
        tried to implement the princepals using sudoku_board help functions 
        as well as the Square and Element classes:

        https://gist.github.com/syphh/62e6140361feb2d7196f2cb050c987b3

        The hidden singluar check is not necessary to solve the puzzle,
        but it saves a lot of time. 
        """

        empty_cell = self.find_empty_cell()

        if not empty_cell:
            # If there are no empty cells left, a solution is found
            print(self.__str__())
            return True
                #breaks the loop of the function.

        row, col = empty_cell
            #used to loop over to the next empty square.

        hidden_single_found, hidden_single_number = self.hidden_singular(row, col)

        if hidden_single_found:
            #it not necceray to check if the hidden single is legal, because it's the
            #only option left.

            self.nums[row][col] = hidden_single_number

            if self.solve():
                return True
            self.nums[row][col] = 0
                #backtrack if a combination does not work.

        else:
            for num in range(1, 10):
                #loops over and try all numbers from 1-9.

                square = Square(row, col, num, self.nums)

                if square.is_legal(num):
                    self.nums[row][col] = num

                    if self.solve():
                        return True

                    self.nums[row][col] = 0
                        #backtrack if a rule is broken. 

        return False


    def find_empty_cell(self):
        """
        This function is activly used to updating the rows and colums inside the 
        solve algoritm. if the function return None, then we know that the puzzle
        is completed.
        """

        for i in range(9):
            for j in range(9):
                if self.nums[i][j] == 0:
                    return i, j
        return None


    def hidden_singular(self,row,column):
        """
        This function check if there is one missing number inside a specific 
        square element. If only one number is missing in either row,column or 3x3 grid
        it then return True and that number.

        I did research on some humans techniques to solve sudoku puzzles 
        faster, I then found out about the hidden single method.
        """

        elements = self._set_up_elements(row, column)
        row, column, box = elements
    
        self._element_count(row)
        self._element_count(column)
        self._element_count(box)
        
        return False,None
            #return a tuple because the solving algoritm expects it.
    

    def _element_count(self,lists):
        """
        A help function for the hidden singular function.
        Check if a list contains one zero, if so: return the
        missing numeber 
        """

        if lists.count(0) == 1:
            #if there is only one zero we know the element is missing
            #one number.

            number = list(set(range(1, 10)) - set(lists))[0]
                #set function return a dictonary with one item
                # that i turned into a list and indexed 
                # it to get the number
            
            return True, number


def sudoku_loop(repetions):
    """
    with this function the program can run the solver function the amount of 
    times the user desires.
    """

    reader = Sudoku_reader("sudoku_1M.csv")

    for _ in range(repetions):
        
        sodoku_board = reader.next_board()
        sodoku_class = Sudoku_board(sodoku_board)
        sodoku_class.solve()
        print(_+1)
        
        
if __name__ == '__main__':

    repetions = input("\nselect how many iterations you would like to try the program for:")
    
    start_time = time.time()

    sudoku_loop(int(repetions))

    end_time = time.time()

    total_time = end_time - start_time

    print(f"The program used:\n{round(total_time,2)} seconds to solve {repetions} sudoku puzzles")