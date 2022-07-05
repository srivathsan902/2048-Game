import pygame
import random
import math

WIDTH = 700
background_color = (251,247,245)
grid_element_color = (0,0,0)
button_color = (52, 31, 151)
colour_2=(255,229,204)
colour_4=(255,204,153)
colour_8=(255, 153, 51)
colour_16=(255,153,153)
colour_32=(255,51,51)
colour_64=(205,0,0)
colour_128=(102,255,255)
colour_256=(0,128,255)
colour_512=(127,0,255)
colour_1024=(255,0,127)
colour_2048=(0,255,0)
colour=[(251,247,245),colour_2,colour_4,colour_8,colour_16,colour_32,colour_64,colour_128,colour_256,colour_512,colour_1024,colour_2048,(0,0,0)]
buffer = 2
rows, cols = (4, 4)
grid = [[0 for i in range(cols)] for j in range(rows)]

def empty_check():
    flag=0
    for i in range(4):
        for j in range(4):
            if grid[i][j]==0:
                flag=1
                break
    return flag

def win_check():
    for i in range(4):
        for j in range(4):
            if grid[i][j]==2048:
                return 1
    return 0

def random_pos():
    row_pos=[]
    col_pos=[]
    for i in range(4):
        for j in range(4):
            if grid[i][j]==0:
                row_pos.append(i)
                col_pos.append(j)
    size_empty=len(row_pos)
    pos=random.randint(0,size_empty-1)
    return row_pos[pos],col_pos[pos]

def check_move():
    changed=0
    for i in range(4):
        for j in range(1,4):
            if grid[i][j]!=0 and grid[i][j-1]==0:
                changed=1
    for i in range(4):
        if grid[i][0]==grid[i][1]:
            changed=1
        elif grid[i][1]==grid[i][2] and grid[i][1]!=0:
            changed=1
        elif grid[i][2]==grid[i][3] and grid[i][2]!=0:
            changed=1
    return changed

def check_over():
    over=check_move()
    if over ==0:
        transpose()
        over=check_move()
        transpose()
        if over==0:
            mirror()
            over=check_move()
            mirror()
            if over==0:
                transpose()
                mirror()
                over=check_move()
                mirror()
                transpose()
                if over==0:
                    return 0
    return 1
        
def left():
    changed=0
    for i in range(4):
        for j in range(1,4):
            if grid[i][j]!=0 and grid[i][j-1]==0:
                changed=1
    for i in range(4):
        for j in range(4):
            for l in range(4):
                if grid[i][j]==0:
                    for k in range(0,3-j):
                        grid[i][j+k]=grid[i][j+k+1]
                    grid[i][3]=0 
        if grid[i][0]==grid[i][1] and grid[i][0]!=0:
            changed=1
            grid[i][0]=2*grid[i][0]
            grid[i][1]=grid[i][2]
            grid[i][2]=grid[i][3]
            grid[i][3]=0
            if grid[i][1]==grid[i][2]:
                grid[i][1]=2*grid[i][1]
                grid[i][2]=0
        elif grid[i][1]==grid[i][2] and grid[i][1]!=0:
            changed=1
            grid[i][1]=2*grid[i][1]
            grid[i][2]=grid[i][3]
            grid[i][3]=0
        elif grid[i][2]==grid[i][3] and grid[i][2]!=0:
            changed=1
            grid[i][2]=2*grid[i][2]
            grid[i][3]=0
    if changed==1:
        row_new,col_new=random_pos()
        grid[row_new][col_new]=2
    changed=0

def transpose():
    rows, cols=(4,4)
    new_grid=[[0 for i in range(cols)] for j in range(rows)]
    for i in range(rows):
        for j in range(cols):
            new_grid[i][j]=grid[j][i]
    for i in range(rows):
        for j in range(cols):
            grid[i][j]=new_grid[i][j]

def mirror():
    rows,cols=(4,4)
    new_grid=[[0 for i in range(cols)] for j in range(rows)]
    for i in range(rows):
        for j in range(cols):
            new_grid[i][j]=grid[i][3-j]
    for i in range(rows):
        for j in range(cols):
            grid[i][j]=new_grid[i][j]

def play_move(win,move):
    myfont = pygame.font.SysFont('Comic Sans MS', 24)
    if move=='a':
        over=check_over()
        if over==1:
            left()
    if move=='w':
        transpose()
        over=check_over()
        if over==1:
            left()
        transpose()
    if move=='d':
        mirror()
        over=check_over()
        if over==1:
            left()
        mirror()
    if move=='s':
        transpose()
        mirror()
        over=check_over()
        if over==1:
            left()
        mirror()
        transpose()
    for i in range(4):
        for j in range(4):
            if grid[i][j]!=0:
                if int(math.log((grid[i][j]),2))<=11:
                    bgc=colour[int(math.log((grid[i][j]),2))]
                else:
                    bgc=colour[1]
            else:
                bgc=colour[0]
            pygame.draw.rect(win, bgc, ((j+1)*100-50 + buffer, (i+1)*100+ buffer-50,100 -buffer , 100 - buffer))
            if grid[i][j]==0:
                value = myfont.render(str(grid[i][j]), True, (251,247,245))
            else :
                value = myfont.render(str(grid[i][j]), True, (0,0,0))
            win.blit(value, ((j+1)*100 -15,(i+1)*100-20))
            pygame.display.update()
        
def main():    
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("2048")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 24)
    
    for i in range(0,5):
        pygame.draw.line(win, (0,0,0), (50 + 100*i, 50), (50 + 100*i ,450 ), 2 )
        pygame.draw.line(win, (0,0,0), (50, 50 + 100*i), (450, 50 + 100*i), 2 )
    value=myfont.render("U", True, button_color)
    win.blit(value, ((500,400)))
    value=myfont.render("D", True, button_color)
    win.blit(value, ((500,600)))
    value=myfont.render("L", True, button_color)
    win.blit(value, ((400,500)))
    value=myfont.render("R", True, button_color)
    win.blit(value, ((600,500)))
    pygame.display.update()
    start_row, start_col=random_pos()
    grid[start_row][start_col]=2
    for i in range(4):
        for j in range(4):
            if grid[i][j]!=0:
                if int(math.log((grid[i][j]),2))<=11:
                    bgc=colour[int(math.log((grid[i][j]),2))]
                else:
                    bgc=colour[1]
            else:
                bgc=colour[0]
            pygame.draw.rect(win, bgc, ((j+1)*100-50 + buffer, (i+1)*100+ buffer-50,100 -buffer , 100 - buffer))
            if grid[i][j]==0:
                value = myfont.render(str(grid[i][j]), True, (251,247,245))
            else :
                value = myfont.render(str(grid[i][j]), True, (0,0,0))
            win.blit(value, ((j+1)*100 -15,(i+1)*100-20))
            pygame.display.update()
    pygame.display.update()
    move='d'
    cnt=0
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                x=mouse_pos[0]
                y=mouse_pos[1]
                if x>=450 and x<=550 and y>=350 and y<=450:
                    move='w'
                elif x>=350 and x<450 and y>450 and y<550:
                    move='a'
                elif x>450 and x<550 and y>550 and y<=650:
                    move='s'
                elif x>550 and x<=650 and y>450 and y<550:
                    move='d'
                play_move(win,move)
                win_chk=win_check()
                if win_chk==1:
                    pygame.draw.rect(win, colour[0], (0, 0,700 , 700))
                    value = myfont.render("Congratulations! You won", True, (0,0,0))
                    win.blit(value,(50,225))
                    pygame.display.update()
                    pygame.time.delay(5000)
                    pygame.quit()
                chk1=check_over()
                chk2=empty_check()
                if chk1==0 and chk2==0:
                    pygame.draw.rect(win, colour[0], (0, 0,700 , 700))
                    value = myfont.render("Oops! You lose", True, (0,0,0))
                    win.blit(value,(50,225))
                    pygame.display.update()
                    pygame.time.delay(5000)
                    pygame.quit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                return
   
main()
