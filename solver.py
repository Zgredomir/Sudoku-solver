def read_from_file(filename: str) -> list:
    '''
    Read Sudoku table from file.
    '''
    with open(filename, 'rt') as f:
        sudoku = []
        for _ in range(9):
            line = f.readline().strip()
            row = [char if char.isdigit() else '' for char in line]
            sudoku.append(row)
    return sudoku

def square(tab:list, i:int, j:int) -> list:
    '''
    Return elements of square in one dimensional list.
    '''
    r = i // 3 * 3
    c = j // 3 * 3
    sq = [tab[row][col] for row in range(r, r+3) for col in range(c, c+3)]
    return sq

def column(tab:list, j:int) -> list:
    '''
    Return elements of column.
    '''
    col = [tab[row][j] for row in range(9)]
    return col

def row(tab:list, i:int) -> list:
    '''
    Return single row of Sudoku.
    '''
    r = tab[i]
    return r

def compress(tab: list) -> str:
    '''
    Compress list of strings to the one string.
    '''
    out = ''
    for elem in tab:
        out += elem
    return out

def remove_element(possibility: str, val: str) -> str:
    '''
    Remove digit from the string.
    e.g.: remove_element('1346','3') = '146'
    '''
    result = possibility.replace(val, '')
    return result

def save_to_file(solution: list, filename: str):
    '''
    Save Sudoku to the file.
    '''
    with open(filename, 'wt') as f:
        for row in solution:
            line = ""
            for elem in row:
                line += elem if elem.isdigit() else "x"
            line += "\n"
            f.write(line)
    return

def check(table: list) -> bool:
    '''
    Check if table is correct Sudoku.
    '''
    for r in range(9):
        for c in range(9):
            elem = table[r][c]
            if not elem.isdigit():
                return False
            if row(table, r).count(elem) > 1:
                return False
            if column(table, c).count(elem) > 1:
                return False
            if square(table, r, c).count(elem) > 1:
                return False
    return True

def constraint(sudoku, guess_table: list) -> list:
    '''
    Constraint Propagation
    Find squares that can only be one possible number.
    '''
    end = False
    changed = False
    while not end:
        end = True
        for r in range(9):
            for c in range(9):
                if sudoku[r][c].isdigit():
                    guess_table[r][c] = sudoku[r][c]
                    continue
                sq = square(sudoku, r, c)
                co = column(sudoku, c)
                ro = row(sudoku, r)
                for guess in guess_table[r][c]:
                    if guess in sq or guess in co or guess in ro:
                        guess_table[r][c] = remove_element(guess_table[r][c], guess)
                        changed = True
                        end = False
                        if len(guess_table[r][c]) == 1:
                            sudoku[r][c] = guess_table[r][c]
    return changed

def only_one(sudoku, guess_table: list) -> bool:
    '''
    Look for possible solutions to squares where the number is only 
    in a single square in a box, row, or column
    '''
    end = False
    changed = False
    while not end:
        end = True
        for r in range(9):
            for c in range(9):
                if sudoku[r][c].isdigit():
                    guess_table[r][c] = sudoku[r][c]
                    continue
                sq_str = compress(square(guess_table, r, c))
                co_str = compress(column(guess_table, c))
                ro_str = compress(row(guess_table, r))
                for guess in guess_table[r][c]:
                    count_sq = sq_str.count(guess)
                    count_ro = ro_str.count(guess)
                    count_co = co_str.count(guess)
                    if count_sq == 1 or count_ro == 1 or count_co == 1:
                        guess_table[r][c] = guess
                        sudoku[r][c] = guess
                        changed = True
                        end = False
    return changed

def empty_pos(sudoku: list, pos: list) -> bool:
    '''
    Find the first empty field in a board. Return True and its position.
    Return False if all fields are fulfilled.
    '''
    for r in range(9):
        for c in range(9):
            if not sudoku[r][c].isdigit():
                pos[:] = [r, c]
                return True
    return False

def backtracking(sudoku: list) -> bool: 
    '''
    Backtracking algorithm
    Return True if successful, False otherwise
    '''
    pos = [0, 0]
    if not empty_pos(sudoku, pos):
        return True
    
    r, c = pos
    ro = row(sudoku, r)
    co = column(sudoku, c)
    sq = square(sudoku, r, c)

    for num in range(1,10): 
        guess = str(num)
        if not(guess in sq or guess in co or guess in ro):
            sudoku[r][c] = guess
            if backtracking(sudoku): 
                return True
            sudoku[r][c] = ''
    return False

def solve(sudoku: list) -> bool:
    '''
    Complete solver that uses all available methods
    '''
    guess_table = [['123456789' for r in range(9)] for c in range(9)]

    changed_1, changed_2 = True, True
    while changed_1 or changed_2:
        changed_1 = constraint(sudoku, guess_table)
        changed_2 = only_one(sudoku, guess_table)
        if check(sudoku): 
            return True
    if backtracking(sudoku):
        return True
    else:
        return False

if __name__ == "__main__":
    sourcefname = "test.txt"
    destfname = "test_solution.txt"
    sudoku = read_from_file(sourcefname)
    if solve(sudoku):
        print("You did it!")
    else:
        print("Mission impossible :(")
    save_to_file(sudoku, destfname)
