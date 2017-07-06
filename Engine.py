#Original 'engine' for my previous games: Battle!, battle-with-pygame, tresure hunt, ai_plays_tresure_hunt
#Github 'dylan157' :)
#Empty 12*12 graphical map which can be navigated using w a s d.

from random import randint
from sys import platform
import os, pygame
import time

Map_Size_X_Y = 12 #Change this value to your needs!(12 max)

size = width, height = Map_Size_X_Y*80, Map_Size_X_Y*80
pygame.init()
screen = pygame.display.set_mode((size))

if platform == "linux" or platform == "linux2": #Clear cmd/terminal text screen
    clear = lambda: os.system('clear')
elif platform == "darwin":
    clear = lambda: os.system('clear')
elif platform == "win32":
    clear = lambda: os.system('cls')

#Icons. add as many as you want. just remember to add them in the print_board dict
land_icon = '@'
bandit_icon = 'X'
health_icon = '+'
player_icon = "h"

#Boards
object_board = [] #Static objects such as buttons, ground and walls.
memory_board = [] #Counts the steps each block has recieved for limited use items such as health packs
playerboard = [] #Front-end. Move your player around this board without affecting static objects.

#Map array writer 
for click in range(Map_Size_X_Y):
    object_board.append([land_icon] * Map_Size_X_Y)
    playerboard.append([land_icon] * Map_Size_X_Y)
    memory_board.append([0] * Map_Size_X_Y)

#vars
error_message = ""
player_xy = [(len(object_board)-2), 0, 0]

def print_board(board):
    #Change the contents of the icon dictionary to print the correct graphics..
    #Print_board will translate the 2d array icon board(playerboard) into a x*y graphical board.
    #Vars
    global icons, error_message
    x = 0
    y = 0
    size = 80
    #Recommend 80*80 pixel blocks
    icon = {
    '@': 'ground.jpg',
    'X':'bandit.jpg',
    '+':'health.jpg',
    'h':'player.jpg',}
    clear()
    #Text board printer
    for row in board[:]:
        for j in range(1):
            print " ".join(row)
    #Graphical board printer(Left to right, row by row)
    for row in board:
        cout = 0
        x = 0
        for square in row:
            cout +=1 
            try:
                img = pygame.image.load(icon[square])
            except: 
                img = pygame.image.load('ground.jpg')
                print "image failed", square
            screen.blit(img,(x,y))
            if x < width: x += size
            else: x = 0
        y += size
    pygame.display.update()
def board_transport(move_choice, em, who):
    #Board transport determins if the move it has been ordered to process is legal or not (valid input and on-map) 
    #Once the move has been validated, the players x_y is changed to the new location. 
    global error_message

    if len(move_choice) == 1 and move_choice[0] in ('w', 'a', 's', 'd'):#W.a.s.d movements. Add special keys above this if statement. eg if move_choice = 'x': playerstats()
        if move_choice[0] == "w":
            if who[0] - int(1) >= 0: #UP
                if playerboard[(who[0] - int(1))][who[1]] not in (): #add restricted icons here.
                    who[0] -= int(1) 
                else:
                    em = "You can't move there!"
            else:
                em = "You can't move there!"

        elif move_choice[0] == "s":
            if (who[0] + int(1)) <= (len(object_board)-1): #DOWN
                if playerboard[(who[0] + int(1))][who[1]] not in ():#add restricted icons here.
                    who[0] += int(1)
                else:
                    em = "You can't move there!"
            else:
                em = "You can't move there!"

        elif move_choice[0] == "d":
            if who[1] + int(1) <= (len(object_board)-1): #RIGHT
                if playerboard[who[0]][(who[1] + int(1))] not in ():#add restricted icons here.
                    who[1] += int(1)
                else:
                    em = "You can't move there!"
            else:
                em = "You can't move there!"

        elif move_choice[0] == "a":
            if who[1] - int(1) >= 0: #LEFT
                if playerboard[who[0]][(who[1] - int(1))] not in ():#add restricted icons here.
                    who[1] -= int(1)
                else:
                    em = "You can't move there!"
            else:
                em = "You can't move there!"
        else:
            em = "What?"
    else:
        em = "Controls: w,a,s,d + enter"
    error_message = em
    return who

playerboard[player_xy[0]][player_xy[1]] = player_icon

while True:
    #User input loop.
    print_board(playerboard)
    choice = False
    while choice == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    W = 'a'
                    choice = True
                if event.key == pygame.K_s:
                    W = 's'
                    choice = True
                if event.key == pygame.K_d:
                    W = 'd'
                    choice = True
                if event.key == pygame.K_w:
                    W = 'w'
                    choice = True

    old_pos = player_xy[:]
    player_xy = board_transport(W, '', player_xy)
    if player_xy != old_pos:
        playerboard[player_xy[0]][player_xy[1]] = player_icon
        playerboard[old_pos[0]][old_pos[1]] = object_board[old_pos[0]][old_pos[1]]
    else:
        playerboard[player_xy[0]][player_xy[1]] = player_icon

