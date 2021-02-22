import tkinter as tk
from tkinter import *
import random


def end_game(event):
    exit()


def draw_sheet():
    for i in range(18):
        field = Button(col1, width=15, height=2, fg='black')
        paper[0].append(field)
        field.pack()
    for i in range(18):
        field = Button(col2, width=15, height=2, fg='black', command=lambda j=i: write_score(1, j))
        paper[1].append(field)
        field.pack()
    for i in range(18):
        field = tk.Button(col3, width=15, height=2, fg='black', command=lambda j=i: write_score(2, j))
        paper[2].append(field)
        field.pack()
    for i in range(18):
        field = tk.Button(col4, width=15, height=2, fg='black', command=lambda j=i: write_score(3, j))
        paper[3].append(field)
        field.pack()

    for i in range(1, 7):
        paper[0][i]['text'] = str(i)

    paper[0][7]['text'] = 'Total Upper'
    paper[0][8]['text'] = 'Bonus'
    paper[0][9]['text'] = 'Total + Bonus'
    paper[0][10]['text'] = 'Trilling'
    paper[0][11]['text'] = 'Poker'
    paper[0][12]['text'] = 'Full'
    paper[0][13]['text'] = 'Small Str'
    paper[0][14]['text'] = 'Large Str'
    paper[0][15]['text'] = 'YAHTZEE'
    paper[0][16]['text'] = 'Total Lower'
    paper[0][17]['text'] = 'TOTAL'
    paper[1][0]['text'] = 'Down'
    paper[2][0]['text'] = 'Up'
    paper[3][0]['text'] = 'Down / Up'
    paper[0][0]['fg'] = 'black'
    paper[0][0]['text'] = 'YAHTZEE'

    col1.pack(side=LEFT, fill=BOTH)
    col2.pack(side=LEFT, fill=BOTH)
    col3.pack(side=LEFT, fill=BOTH)
    col4.pack(side=LEFT, fill=BOTH)

    return paper


def roll(n):
    for x in range(n):
        score = random.randint(1, 6)
        result.append(score)
    result.sort()
    return result


def roll_button(event):
    global play_counter
    global result
    play_counter += 1
    if play_counter < 3:
        num = 5 - len(keep_dices)
        result.clear()
        result = keep_dices + roll(num)
        result.sort()
        keep_dices.clear()
        draw_dices(result)
    elif play_counter >= 3:
        result_counter(result)

    return result


def select_dices(event):
    item = sheet.find_closest(event.x, event.y)
    num = sheet.itemcget(item, 'tag')
    current_color = sheet.itemcget(item, 'fill')

    if current_color == 'red':
        keep_dices.append(result[int(num[0])-1])
        sheet.itemconfig(item, fill='brown')
    else:
        index = int(num[0]) - 1
        keep_dices.remove(result[int(num[0])-1])
        sheet.itemconfig(item, fill='red')
    return keep_dices


def result_counter(result):
    counter = []
    combinations = set()
    for dice_val in range(1, 7):
        counter.append(result.count(dice_val))
    straight_check = set(result)
    straight_check = list(straight_check)
    # small straight
    if len(straight_check) > 3 and straight_check[0] == straight_check[1] - 1 == straight_check[2] - 2 == \
            straight_check[3] - 3:
        combinations.add('Small Straight')
    # large straight
    if result == [1, 2, 3, 4, 5] or result == [2, 3, 4, 5, 6]:
        combinations.add('Large Straight')
    pair = False
    trilling = False
    for amount in counter:
        if amount == 2:
            pair = True
        if amount > 2:
            combinations.add('Trilling')
            trilling = True
        if amount > 3:
            combinations.add('Poker')
        if amount > 4:
            combinations.add('YAHTZEE')
    if pair is True and trilling is True:
        combinations.add('Full')
        full = True

    return [counter, combinations]


def write_score(col, row):
    # column write rules
    if col == 1:
        write[0] += 1
        if write[0] == 7:  # skip total and bonus rows
            write[0] += 3
        elif write[0] == 16:  # column full
            write[0] -= 1
        row = write[0]
    elif col == 2:
        write[1] -= 1
        if write[1] == 9:  # skip total and bonus rows
            write[1] -= 3
        row = write[1]
    elif col == 3:
        if write[2] < 8:
            write[2] -= 1
        if write[2] == 0:
            write[2] += 9
        if write[2] > 8:
            write[2] += 1
        row = write[2]
    # upper side
    if 0 < row < 7:
        upper_score = result_counter(result)[0][row - 1] * row
        paper[col][row]['text'] = upper_score  # write score
        # total up
        total_up[col - 1] += upper_score
        paper[col][7]['text'] = str(total_up[col - 1])
        # total + bonus
        paper[col][9]['text'] = int(paper[col][7]['text'])
        global game_counter
        game_counter += 1

        if int(paper[col][7]['text']) > 62:  # bonus
            paper[col][8]['text'] = 35
            paper[col][9]['text'] = int(paper[col][7]['text']) + 35
            total[col - 1] = int(paper[col][7]['text']) + 35
            paper[col][-1]['text'] = str(total[col - 1])
        # total
        else:
            total[col - 1] += upper_score
            paper[col][-1]['text'] = str(total[col - 1])

        play(player=1)

    if 9 < row < 16:
        lower_section_score(col, row)


def lower_section_score(col, row):
    selection = ''
    if row == 10:
        selection = 'Trilling'
    elif row == 11:
        selection = 'Poker'
    elif row == 12:
        selection = 'Full'
    elif row == 13:
        selection = 'Small Straight'
    elif row == 14:
        selection = 'Large Straight'
    elif row == 15:
        selection = 'YAHTZEE'
    combinations = result_counter(result)[1]

    if selection in combinations:
        if selection == 'Trilling':
            score = sum(result)
        elif selection == 'Poker':
            score = sum(result)
        elif selection == 'Full':
            score = 25
        elif selection == 'YAHTZEE':
            score = 50
        elif selection == 'Small Straight':
            score = 30
        elif selection == 'Large Straight':
            score = 40
    else:
        score = 0
    paper[col][row]['text'] = score  # write score
    # total lower section
    total_low[col - 1] += score
    paper[col][-2]['text'] = total_low[col-1]
    # total
    total[col - 1] += score
    paper[col][-1]['text'] = str(total[col - 1])

    global game_counter
    game_counter += 1

    play(player=1)


def draw_dices(result):
    cx = 10
    cy = 60
    cx1 = 110
    cy1 = 160
    cube_pos = []
    q = 0
    for i in result:
        cube = sheet.create_rectangle(cx, cy, cx1, cy1, fill='red', width='5', tag=q+1)
        cube_pos.append([cx])
        cx += 110
        cx1 += 110
        x = cube_pos[q][0]
        sheet.tag_bind(cube, '<Button-1>', select_dices)

        if result[q] == 1:
            sheet.create_oval(x+40, cy + 40, x + 60, cy + 60, fill='white', width='5')
        elif result[q] == 2:
            sheet.create_oval(x + 20, cy + 20, x + 40, cy + 40, fill='white', width='5') + \
            sheet.create_oval(x + 60, cy + 60, x + 80, cy + 80, fill='white', width='5')
        elif result[q] == 3:
            sheet.create_oval(x + 10, cy + 10, x + 30, cy + 30, fill='white', width='5') + \
            sheet.create_oval(x + 70, cy + 70, x + 90, cy + 90, fill='white', width='5') + \
            sheet.create_oval(x + 40, cy + 40, x + 60, cy + 60, fill='white', width='5')
        elif result[q] == 4:
            sheet.create_oval(x + 10, cy + 10, x + 30, cy + 30, fill='white', width='5') + \
            sheet.create_oval(x + 70, cy + 70, x + 90, cy + 90, fill='white', width='5') + \
            sheet.create_oval(x + 70, cy + 10, x + 90, cy + 30, fill='white', width='5') + \
            sheet.create_oval(x + 10, cy + 70, x + 30, cy + 90, fill='white', width='5')
        elif result[q] == 5:
            sheet.create_oval(x + 40, cy + 40, x + 60, cy + 60, fill='white', width='5') + \
            sheet.create_oval(x + 10, cy + 10, x + 30, cy + 30, fill='white', width='5') + \
            sheet.create_oval(x + 70, cy + 70, x + 90, cy + 90, fill='white', width='5') + \
            sheet.create_oval(x + 70, cy + 10, x + 90, cy + 30, fill='white', width='5') + \
            sheet.create_oval(x + 10, cy + 70, x + 30, cy + 90, fill='white', width='5')
        elif result[q] == 6:
            sheet.create_oval(x + 10, cy + 10, x + 30, cy + 30, fill='white', width='5') + \
            sheet.create_oval(x + 70, cy + 70, x + 90, cy + 90, fill='white', width='5') + \
            sheet.create_oval(x + 70, cy + 10, x + 90, cy + 30, fill='white', width='5') + \
            sheet.create_oval(x + 10, cy + 70, x + 30, cy + 90, fill='white', width='5') + \
            sheet.create_oval(x + 10, cy + 40, x + 30, cy + 60, fill='white', width='5') + \
            sheet.create_oval(x + 70, cy + 40, x + 90, cy + 60, fill='white', width='5')

        q += 1

    # draw roll dices button
    _roll_button = sheet.create_rectangle(230, 15, 330, 45, fill='green',outline='white', width='4', tag='roll')
    text = sheet.create_text(280, 30, text='Roll Dices', font=('Arial', 20), fill='white')
    sheet.tag_bind(text, '<Button-1>', roll_button)
    # quit game
    main.bind('<Escape>', end_game)

    mainloop()


def play(player):
    global result
    result = []
    global play_counter
    play_counter = 0
    global keep_dices
    keep_dices = []
    global game_counter
    if game_counter < 36:
        roll(5)
        draw_dices(result)
    else:
        print('Total:', sum(total))
        print('Game Over')
        exit()


main = tk.Tk()
main.title('YAHTZEE')
main.geometry('560x860')
paper = [[], [], [], []]

col1 = Frame(main)
col2 = Frame(main)
col3 = Frame(main)
col4 = Frame(main)

sheet = Canvas(main, bg='green', width=555, height=205)
sheet.place(x=0, y=860, anchor=SW)

play_counter = 0  # counts 3 dice rolls
game_counter = 0  # counts write events, after 36 game over
result = []
keep_dices = []
total_up = [0, 0, 0]
total_plus_bonus = [0, 0, 0]
total_low = [0, 0, 0]
total = [0, 0, 0]
write = [0, 16, 7]


draw_sheet()
play(player=1)
