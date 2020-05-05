from tkinter import *
from tkinter import messagebox
import copy
from itertools import chain
import collections

saved = [0]*81

def limit(arg):
    arg = int(arg[6:])
    value = vals[arg].get()
    try:
        value = int(value[-1])
    except:
        if len(value) == 2:
            vals[arg].set(value[0])
        else:
            vals[arg].set('')
    else:
        vals[arg].set(value)
        
def clear():
    for i in range(0, len(boxes)):
        for j in boxes[i]:
            j.delete(0, 'end')
            
def save():
    global saved
    saved = [vals[i].get() for i in range(81)]

def load():
    for i in range(0, len(boxes)):
        for j in boxes[i]:
            j.delete(0, 'end')

    for i in range(81):
        if saved[i] == 0:
            vals[i].set('')
        else:
            vals[i].set(saved[i])
            
def solve():
    rows = []
    cols = []
    squares = []
    
    for i in range(9):
        rows.append(vals[(9*i):(9+9*i)])
        cols.append([vals[9*j + i] for j in range(9)])
        for j in range(9):
            if rows[i][j].get() == '':
                rows[i][j] = 0
            else:
                rows[i][j] = int(rows[i][j].get())
            if cols[i][j].get() == '':
                cols[i][j] = 0
            else:
                cols[i][j] = int(cols[i][j].get())
            
    for i in range(9):
        square = []
        for j in range(3):
            for k in range(3):
                if i < 3:
                    square.append(rows[j][k + 3*i])
                elif i < 6:
                    square.append(rows[3 + j][k + 3*i - 9])
                else:
                    square.append(rows[6 + j][k + 3*i - 18])      
        squares.append(square)
        
    if not checkValidity(squares, rows, cols):
        messagebox.showinfo("ERROR", "Invalid Sudoku Puzzle")
        return
        
    change = True
    while change:
        change = False
        for i in range(9):
            for j in range(1,10):
                if j in squares[i]:
                    continue
                
                if i < 3:
                    row0 = 0
                    col0 = 3*i
                elif i < 6:
                    row0 = 3
                    col0 = 3*i - 9
                else:
                    row0 = 6
                    col0 = 3*i - 18
                    
                sq = copy.deepcopy(squares[i])
                
                for k in range(3):
                    if j in rows[row0 + k]:
                        sq[3*k] = -1
                        sq[3*k+1] = -1
                        sq[3*k+2] = -1
                    if j in cols[col0 + k]:
                        sq[k] = -1
                        sq[k+3] = -1
                        sq[k+6] = -1
                        
                placement = -1
                for k in range(9):
                    if sq[k] == 0 and placement == -1:
                        placement = k
                    elif sq[k] == 0 and not placement == -1:
                        placement = -1
                        break
                
                if not placement == -1:
                    squares[i][placement] = j
                    y = (i%3)*3 + placement%3
                    if i < 3:
                        x = int(placement/3)
                        rows[x][3*i + placement%3] = j
                        cols[y][x] = j
                    elif i < 6:
                        x = int(placement/3) + 3
                        rows[x][3*i - 9 + placement%3] = j
                        cols[y][x] = j
                    else:
                        x = int(placement/3) + 6
                        rows[x][3*i - 18 + placement%3] = j
                        cols[y][x] = j
                    change = True
            
            for j in range(9):
                if squares[i][j] == 0:
                    y = (i%3)*3 + j%3
                    if i < 3:
                        x = int(j/3)
                    elif i < 6:
                        x = int(j/3) + 3
                    else:
                        x = int(j/3) + 6
                    
                    placement = -1
                    for k in range(1,10):
                        if k in squares[i] or k in cols[y] or k in rows[x]:
                            continue
                        elif placement == -1:
                            placement = k
                        else:
                            placement = -1
                            break
                            
                    if not placement == -1:
                        squares[i][j] = placement
                        if i < 3:
                            rows[x][3*i + j%3] = placement
                            cols[y][x] = placement
                        elif i < 6:
                            rows[x][3*i - 9 + j%3] = placement
                            cols[y][x] = placement
                        else:
                            rows[x][3*i - 18 + j%3] = placement
                            cols[y][x] = placement
                        change = True
            
    if updateBoard(rows):
        bruteForce(squares, rows, cols)
    else:
        messagebox.showinfo("Success!", "Solved successfully")
        
def bruteForce(squares, rows, cols):
    options = []
    keys = []
    indices = []
    for i in range(9):
        for j in range(9):
            if squares[i][j] == 0:
                y = (i%3)*3 + j%3
                if i < 3:
                    x = int(j/3)
                elif i < 6:
                    x = int(j/3) + 3
                else:
                    x = int(j/3) + 6
                
                possible = []
                for k in range(1,10):
                    if k in squares[i] or k in cols[y] or k in rows[x]:
                        continue
                    else:
                        possible.append(k)
                if possible:
                    if i == 0:
                        key = '0' + str(j)
                    else:
                        key = str(10*i + j)
                    options.append(possible)
                    keys.append(key)
    limit = len(keys)
    indices = [0] * limit
    index = 0
    while index < limit:

        i = int(keys[index][0])
        j = int(keys[index][1])
        
        y = (i%3)*3 + j%3
        if i < 3:
            x = int(j/3)
        elif i < 6:
            x = int(j/3) + 3
        else:
            x = int(j/3) + 6
        
        placement = options[index][indices[index]]
        indices[index] = indices[index] + 1
        squares[i][j] = placement
        if i < 3:
            rows[x][3*i + j%3] = placement
            cols[y][x] = placement
        elif i < 6:
            rows[x][3*i - 9 + j%3] = placement
            cols[y][x] = placement
        else:
            rows[x][3*i - 18 + j%3] = placement
            cols[y][x] = placement
        
        if not checkValidity(squares, rows, cols):
            while True:
            
                i = int(keys[index][0])
                j = int(keys[index][1])
        
                y = (i%3)*3 + j%3
                if i < 3:
                    x = int(j/3)
                elif i < 6:
                    x = int(j/3) + 3
                else:
                    x = int(j/3) + 6
            
                squares[i][j] = 0
                if i < 3:
                    rows[x][3*i + j%3] = 0
                    cols[y][x] = 0
                elif i < 6:
                    rows[x][3*i - 9 + j%3] = 0
                    cols[y][x] = 0
                else:
                    rows[x][3*i - 18 + j%3] = 0
                    cols[y][x] = 0
            
                if indices[index] >= len(options[index]):
                    indices[index] = 0
                    index = index - 1
                    
                    if index < 0:
                        messagebox.showinfo("ERROR", "No Solution Found")
                        return
                else:
                    break
        else:
            index = index + 1
    updateBoard(rows)
    messagebox.showinfo("Success!", "Solved successfully")
        
def checkValidity(squares, rows, cols):
    for i in range(9):
        zeros = [0,0,0]
        for j in range(9):
            if rows[i][j] == 0:
                zeros[0] = zeros[0] + 1
            if cols[i][j] == 0:
                zeros[1] = zeros[1] + 1
            if squares[i][j] == 0:
                zeros[2] = zeros[2] + 1
        if (zeros[0] and not len(set(rows[i])) + zeros[0] == 10) or (not zeros[0] and not len(set(rows[i])) == 9):
            return False
        if (zeros[1] and not len(set(cols[i])) + zeros[1] == 10) or (not zeros[1] and not len(set(cols[i])) == 9):
            return False    
        if (zeros[2] and not len(set(squares[i])) + zeros[2] == 10) or (not zeros[2] and not len(set(squares[i])) == 9):
            return False
    return True
    
def updateBoard(rows):
    flatRows = list(chain.from_iterable(rows))
    partial = False
    for i in range(81):
        if flatRows[i] == 0:
            vals[i].set('')
            partial = True
        else:
            vals[i].set(flatRows[i])
    return partial
            
            
   
window = Tk()
window.title("Sudoku Solver")
window.geometry("800x732")
window.resizable(False, False)

#Create the canvas and pack it
w = Canvas(window, width=732, height=732)
w.configure(background = 'white')
w.pack(side = "right")

#These will automatically be drawn on the already packed canvas
w.create_line(80, 0, 80, 732)
w.create_line(161, 0, 161, 732)
w.create_line(242, 0, 242, 732, width = 3)
w.create_line(325, 0, 325, 732)
w.create_line(406, 0, 406, 732)
w.create_line(487, 0, 487, 732, width = 3)
w.create_line(570, 0, 570, 732)
w.create_line(651, 0, 651, 732)
w.create_line(0, 80, 732, 80)
w.create_line(0, 161, 732, 161)
w.create_line(0, 242, 732, 242, width = 3)
w.create_line(0, 325, 732, 325)
w.create_line(0, 406, 732, 406)
w.create_line(0, 487, 732, 487, width = 3)
w.create_line(0, 570, 732, 570)
w.create_line(0, 651, 732, 651)

boxes = []
vals = []
for i in range(0,9):
    row = []
    for j in range(0,9):
        val = StringVar()
        val.trace('w', lambda *args: limit(args[0]))
        txt = Entry(window, font = "Helvetica 40 bold", width = 1, borderwidth = 0, textvariable = val)
        row.append(txt)
        w.create_window(40 + 81*j, 40 + 81*i, window=txt)
        vals.append(val)
    boxes.append(row)
    
solve = Button(window, text = 'Solve', bg = "green", fg = "black", command = solve)
solve.pack()
save = Button(window, text = 'Save', bg = "blue", fg = "black", command = save)
save.pack()
load = Button(window, text = 'Load', bg = "yellow", fg = "black", command = load)
load.pack()
clear = Button(window, text = 'Clear All', bg = "red", fg = "black", command = clear)
clear.pack()

window.mainloop()
