__author__ = 'xiao-data'

'''
00,01,02,03,04,05,06,07
08,09,10,11,12,13,14,15
16,17,18,19,20,21,22,23
24,25,26,27,28,29,30,31
32,33,34,35,36,37,38,39
40,41,42,43,44,45,46,47
48,49,50,51,52,53,54,55
56,57,58,59,60,61,62,63
'''
import numpy as np
from math import sqrt, log
import random
import time
# from tqdm import trange
class Othello(object):
    def __init__(self, color=1):
        tmp = np.zeros(64)
        tmp[27] = tmp[36] = -1
        tmp[28] = tmp[35] = +1
        self.state = tmp
        self.color = color
    def Clone(self):
        st = Othello(self.color)
        st.state = self.state.copy()
        return st
    
    def quick_find(self, move, color = 0):
        if color == 0: color = self.color
        x, y = self.num2tuple(move)
        dirs = []
        for (dx, dy) in [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]:
            near = self.tuple2num((x+dx, y+dy))
            if self.is_on_board(x+dx, y+dy) and self.state[near] == -color:
                dirs.append((dx, dy))
        return dirs
    
    def search(self, move, dirrection, color = 0):
        if color == 0: color = self.color
        x, y = self.num2tuple(move)
        dx, dy = dirrection
        x += dx
        y += dy
        reversible = []
        while self.is_on_board(x, y) and self.state[self.tuple2num((x, y))] == -color:
            reversible.append(self.tuple2num((x,y)))
            x += dx
            y += dy
            
        if self.is_on_board(x,y) and self.state[self.tuple2num((x, y))] == color:
            return reversible
        else:
            return []

    def get_reversible(self, move, color = 0):
        if color == 0: color = self.color
        dirs = self.quick_find(move, color)
        reversible = []
        for d in dirs:
            reversible.extend(self.search(move, d, color))
        return reversible
    
    def downable(self, move, color = 0):
        if color == 0: color = self.color
        if self.state[move] != 0.: return False
        dirs = self.quick_find(move, color)
        if dirs == []: return False
        for d in dirs:
            if(self.search(move, d, color) != []): return True
        return False
    def tuple2num(self, move):
        return 8*move[0]+move[1]
    def num2tuple(self, move):
        return (move//8, move%8)
    def is_on_board(self, x, y):
        return (x >= 0 and x < 8 and y >= 0 and y < 8)
    def do_move(self, move, color = 0):
        if color == 0: color = self.color
        reversible = self.get_reversible(move, color)
        self.state[move] = color
        for i in reversible:
            self.state[i] = color
        self.chg_color()
        return reversible
    def get_all_possible_moves(self, color = 0):
        if color == 0: color = self.color
        return [i for i in range(64) if self.downable(i, color)]
    def count(self):
        return np.sum(self.state == 1), np.sum(self.state == -1)
    def get_result(self, color = 0):
            if color == 0: color = self.color
            count_jm = np.sum(self.state == color)
            count_njm = np.sum(self.state == -color)
            if count_jm > count_njm: return 1.0
            elif count_njm > count_jm: return 0.0
            else: return 0.5
    def chg_color(self):
        self.color = -self.color
    def __repr__(self):
        s = ''
        for i in range(64):
            s += 'X.O'[int(self.state[i])+1]
            if i % 8 == 7:
                s += '\n'
        return s
class Node:

    def __init__(self, move = None, parent = None, state = None):
        self.move = move
        self.parent_node = parent # root node is None
        self.child_nodes = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.get_all_possible_moves() 
        self.color = state.color 

    def UCT_select_child(self, rootcolor):
        if self.color == rootcolor:
            return sorted(self.child_nodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return sorted(self.child_nodes, key = lambda c: 1-c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]

    def add_child(self, m, s):
        n = Node(move = m, parent = self, state = s)
        self.untried_moves.remove(m)
        self.child_nodes.append(n)
        return n

    def update(self, result):
        self.visits += 1
        self.wins += result
# 
#     def __repr__(self):
#         return '[M:' + str(self.move) + ' W/V:' + str(self.wins) + '/' + str(self.visits) + ' U:' + str(self.untried_moves) + ']'
#     def children_to_string(self):
#         s = ''
#         for c in self.child_nodes:
#             s += str(c) + '\n'
#         return s
def UCT(rootstate, itermax): #Upper Confidence Bounds for Tree

    rootnode = Node(state = rootstate)
    rootcolor = rootstate.color
    for _ in range(itermax):
        node = rootnode
        state = rootstate.Clone()
        # Select
        while node.untried_moves == [] and node.child_nodes != []:
            node = node.UCT_select_child(rootcolor)
            state.do_move(node.move)
        # Expand
        if node.untried_moves != []:
            m = random.choice(node.untried_moves) 
            state.do_move(m)
            node = node.add_child(m,state)
        # Rollout
        while True:
            all_possible_moves = state.get_all_possible_moves()
            if  all_possible_moves != []:
                for corner in [0,7,56,63]:
                    if corner in all_possible_moves:
                        state.do_move(corner)
                        continue
                state.do_move(random.choice(all_possible_moves))
                continue
            state.chg_color()
            all_possible_moves = state.get_all_possible_moves()
            if all_possible_moves != []:
                for corner in [0,7,56,63]:
                    if corner in all_possible_moves:
                        state.do_move(corner)
                        continue
                state.do_move(random.choice(all_possible_moves))
                continue
            break
        # Backpropagate
        while node != None: 
            node.update(state.get_result(rootcolor)) 
            node = node.parent_node
#     print (rootnode.children_to_string())

    return sorted(rootnode.child_nodes, key = lambda c: c.visits)[-1].move

if __name__ == '__main__':
    def xo(color):
        return 'x.o'[color+1]
    R = Othello()
    print(R)
    i = 100
    difficulty = 1000 # Generally, x will win if difficulty is set to a number bigger than 100
    while (R.get_all_possible_moves() != []):
 
        if R.color == 1:
            Tsta = time.time()
            m = UCT(rootstate = R, itermax = 100)
            Tend = time.time()
            print('player o\ntime consuming:'+str(Tend-Tsta))
        else:
            Tsta = time.time()
            m = UCT(rootstate = R, itermax = i)
            Tend = time.time()
            print('player x\ntime consuming:'+str(Tend-Tsta))
        print ('Move: ' + str(R.num2tuple(m)) + '\n')
        R.do_move(m)
        i += 100
        if i >= difficulty: i = difficulty
        print(R)
    if R.get_result(R.color) == 1.0:
        print ('Player ' + xo(R.color) + ' wins!')
    elif R.get_result(R.color) == 0.0:
        print ('Player ' + xo(-R.color) + ' wins!')
    else: print ('Nobody wins!')
#*****
#*****
#*****
#     n = 0
#     for _ in trange(100):
#         R = Othello()
#         while (R.get_all_possible_moves() != []):
#             if R.color == 1:
#                 m = UCT(rootstate = R, itermax = 50)
#             else:
#                 m = UCT(rootstate = R, itermax = 100)
#             R.do_move(m)
#         if R.get_result(-1) == 1.0: n+=1
#     print('winrate:'+str(n)+'%') #70%
#*****
#     n = 0
#     for _ in trange(50):
#         R = Othello()
#         while (R.get_all_possible_moves() != []):
#             if R.color == 1:
#                 m = UCT(rootstate = R, itermax = 50)
#             else:
#                 m = UCT(rootstate = R, itermax = 50)
#             R.do_move(m)
#         if R.get_result(-1) == 1.0: n+=1
#     print('winrate:'+str(n*2)+'%') #50%
#*****
#     n = 0
#     for _ in trange(50):
#         R = Othello()
#         while (R.get_all_possible_moves() != []):
#             if R.color == 1:
#                 m = UCT(rootstate = R, itermax = 50)
#             else:
#                 m = UCT(rootstate = R, itermax = 500)
#             R.do_move(m)
#         if R.get_result(-1) == 1.0: n+=1
#     print('winrate:'+str(n*2)+'%') #98%
