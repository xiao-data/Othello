__author__ = 'xiao-data'
import Othello
import tkinter as tk
from tkinter import ttk
from collections import deque
def turn(var):
    if var.get() == '黑方下子':
        var.set('白方下子')
        return
    var.set('黑方下子')
def choose_iter(i):
    if i <= 500:
        return 100
    if i < diffmap[Pdifficulty.get()]:
        return i
    return diffmap[Pdifficulty.get()]
def draw_board(R, img):
    img.clear()
    for i in range(64):
        img.append(tk.PhotoImage(file='./'+img_file[int(R.state[i])+1]+'.png'))
#         Cboard[i].delete('all')
        Cboard[i].create_image(0,0,anchor='nw',image=img[i])
def chg_img(color, img, move, reversible):
    img[move] = tk.PhotoImage(file='./'+img_file[color+1]+'.png')
#     Cboard[move].delete('all')
    Cboard[move].create_image(0,0,anchor='nw', image=img[move])
    for r in reversible:
        img[r] = tk.PhotoImage(file='./'+img_file[color+1]+'.png')
        Cboard[r].create_image(0,0,anchor='nw', image=img[r])
def player_move(event, move):
    if flag_start == 0: return
    color = int(R.color)
    if color != playermap[Pcolor.get()]: return
    if not R.downable(move): return
    Vtips.set('')
    global img
    retract_moves.append(R.Clone())
    reversible = R.do_move(move)
    chg_img(color, img, move, reversible)
    turn(Vcolor)
    
def player_move_Adaptor(fun, **kwds):  
    return lambda event,fun=fun, kwds=kwds: fun(event, **kwds)
def AI_move(event):
#     if flag_start == 0: return
    color = int(R.color)
    if color == playermap[Pcolor.get()]: return
    if R.get_all_possible_moves() == []:
        R.chg_color()
        if R.get_all_possible_moves() == []:
            end_game()
            return
        Vtips.set('黑.白'[-R.color+1]+'方无棋可下,'+'黑.白'[R.color+1]+'继续')
        turn(Vcolor)
        return
    global img, iterI
    j = choose_iter(iterI)
    iterI += 100
    move = Othello.UCT(rootstate = R, itermax = j)
    reversible = R.do_move(move)
    chg_img(color, img, move, reversible)
    turn(Vcolor)
    tmp_R = R.Clone()
    if tmp_R.get_all_possible_moves() == []:
        tmp_R.chg_color()
        if tmp_R.get_all_possible_moves() == []:
            end_game()
            return
        Vtips.set('黑.白'[R.color+1]+'方无棋可下,'+'黑.白'[-R.color+1]+'继续')
        R.chg_color()
        AI_move(0)
        turn(Vcolor)
def start_game():
    global flag_start
    CBcolor.place_forget()
    CBpriority.place_forget()
    CBdifficulty.place_forget()
    Plcp.set('执'+Pcolor.get()+Ppriority.get())
    Vtips.set('')
    Lcp.place(x=94*8, y=100)
    Ldifficulty.place(x=94*8, y=150)
    flag_start = 1
    if Pcolor.get() == '黑' and Ppriority.get() == '后手': 
        R.chg_color()
        Vcolor.set('白方下子')
        AI_move(0)
    elif Pcolor.get() == '白' and Ppriority.get() == '后手':
        Vcolor.set('黑方下子')
        AI_move(0)
    elif Pcolor.get() == '白':
        R.chg_color()
        Vcolor.set('白方下子')
    else:
        Vcolor.set('黑方下子')
    Bstart.place_forget()
def retract_move():
    Vtips.set('')
    if retract_moves == deque():
        Vtips.set('不能再悔棋啦')
        return
    global R
    R = retract_moves.pop()
    draw_board(R, img)
def restart_game():
    global R, iterI
    Vtips.set('')
    R = Othello.Othello()
    iterI = 100
    draw_board(R, img)
    Lcp.place_forget()
    Ldifficulty.place_forget()
    CBcolor.place(x=94*8, y=100)
    CBpriority.place(x=94*8, y=150)
    CBdifficulty.place(x=94*8, y=200)
    Bstart.place(x=94*8, y=250)
def end_game():
    count = R.count()
    if R.get_result(1) == 1.0:
        Vtips.set('白:'+str(count[1])+'黑:'+str(count[0])+ '---黑方胜!')
    elif R.get_result(R.color) == 0.0:
        Vtips.set('白:'+str(count[1])+'黑:'+str(count[0])+ '---白方胜!')
    else: Vtips.set("平局!")
    return
R = Othello.Othello()
root = tk.Tk()
root.title('黑白棋')
root.geometry('1000x1000')
Pcolor = tk.StringVar()
Ppriority = tk.StringVar()
Pdifficulty = tk.StringVar()
Plcp = tk.StringVar()
retract_moves = deque(maxlen=5)
playermap = {'黑':1, '白':-1}
diffmap = {'简单':100, '容易':1000, '困难':2000}
flag_start = 0
img_file = ['w','s','b']
Vcolor = tk.StringVar()
Vcolor.set('')
Vtips = tk.StringVar()
Vtips.set('')
Cboard = []
img = []
iterI = 100
Lcolor = tk.Label(root, textvariable=Vcolor, width=20, height=1)
Lcolor.place(x=94*8, y=0)
Ltips = tk.Label(root, textvariable=Vtips, width=20, height=1)
Ltips.place(x=94*8, y=50)
Lcp = tk.Label(root, textvariable=Plcp, width=20, height=1)
Ldifficulty = tk.Label(root, textvariable=Pdifficulty, width=20, height=1)
Ltips.place(x=94*8, y=50)
CBcolor = ttk.Combobox(root, textvariable=Pcolor, values = ('黑', '白'))
CBpriority = ttk.Combobox(root, textvariable=Ppriority, values = ('先手', '后手'))
CBdifficulty = ttk.Combobox(root, textvariable=Pdifficulty, values = ('简单', '容易', '困难'))
CBcolor.place(x=94*8, y=100)
CBcolor.current(0)
CBpriority.place(x=94*8, y=150)
CBpriority.current(0)
CBdifficulty.place(x=94*8, y=200)
CBdifficulty.current(0)
Bstart = tk.Button(root, text='开始', command = start_game)
Bstart.place(x=94*8, y=250)
Bretract = tk.Button(root, text='悔棋', command = retract_move)
Bretract.place(x=94*8, y=300)
Brestart = tk.Button(root, text='重新开始', command = restart_game)
Brestart.place(x=94*8, y=350)
for _ in range(64):
    Cboard.append(tk.Canvas(root, width=93, height=93))
draw_board(R, img)
for i in range(64):
    x, y = R.num2tuple(i)
    Cboard[i].place(x=y*94, y=x*94)
    Cboard[i].bind("<Button-1>", player_move_Adaptor(player_move, move=i))
    Cboard[i].bind("<ButtonRelease-1>", AI_move)


root.mainloop()
