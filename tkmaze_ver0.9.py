"""
冥土で冥土探索。それは終わりなき旅。ゴールは無くて、敵を避けつつひたすら階段を降りていく。
1歩ごとにスコアカウント。階段を降りるとプラス。ハイスコアを目指そう！
"""
import tkinter
import maze_maker
from PIL import Image,ImageTk
import random

#キー入力
key = ''
koff = False
def key_down(e):
    global key,koff
    key = e.keysym
    koff = False

def key_up(e):
    global koff
    koff = True

CHIP_SIZE = 32
DIR_UP = 3
DIR_DOWN = 0
DIR_LEFT = 1
DIR_RIGHT = 2
chara_x = chara_y = 146
chara_d = chara_a = 0
obj_a = 0
emy_num = 4
emy_list_x = [0]*emy_num
emy_list_y = [0]*emy_num
emy_list_d = [0]*emy_num
emy_list_a = [0]*emy_num
ANIMATION = [1,0,1,2]
#素材は「ぴぽや http://blog.pipoya.net/」様より
imgplayer_pass = 'image/charachip01.png'
emy_img_pass = 'image/pipo-charachip019.png'
emy2_img_pass = 'image/hone.png'
emy3_img_pass = 'image/majo.png'
emy3_kageimg_pass = 'image/majo_kage.png'
takara_img_pass = 'image/pipoya_mcset1_obj01.png'
obj_pass = 'image/pipoya_mcset1_obj02.png'
obj2_pass = 'image/pipo-hikarimono005.png'
yuka_pass = 'image/pipoya_mcset1_at_gravel1.png'
kebe_pass = 'image/pipoya_mcset1_bridge01.png'

map_data = maze_maker.maze_maker(11,7)
map_data.make_dungeon()
map_data.put_event()

tmr = 0
idx = 1
floor_count = 0
item_count = 0
pl_life=150
pl_stamina = 150
pl_damage = 0

def move_player():
    global chara_x,chara_y,chara_a,chara_d,pl_stamina,pl_life
    if key == 'Up':
        chara_d = DIR_UP
        check_wall()
    if key == 'Down':
        chara_d = DIR_DOWN
        check_wall()
    if key == 'Left':
        chara_d = DIR_LEFT
        check_wall()
    if key == 'Right':
        chara_d = DIR_RIGHT
        check_wall()
    check_event()
    if tmr%4 == 0:
        if pl_stamina > 0:
            pl_stamina -= 1
        else:
            pl_life -= 1
            if pl_life <= 0:
                pl_life = 0
                idx = 2
    chara_a = chara_d*3 + ANIMATION[tmr%4]


def emy_set(emy_num):
    while True:
        x = random.randint(3,map_data.DUNGEON_W-4)
        y = random.randint(3,map_data.DUNGEON_H-4)
        if map_data.dungeon[y][x] == 0:
            emy_list_x[emy_num] = x*CHIP_SIZE+(CHIP_SIZE//2)
            emy_list_y[emy_num] = y*CHIP_SIZE+(CHIP_SIZE//2)
            break


def draw_text(txt):
    st_fnt = ('Times New Roman',60)
    canvas.create_text(200,200,text=txt,font=st_fnt,fill='red',tag='SCREEN')


def damage_cal(pl_damage):
    global pl_life,idx
    if pl_life <= pl_damage:
        pl_life = 0
        idx = 2
    else:
        pl_life -= pl_damage


def move_emy(emy_num):
    cy = int(emy_list_y[emy_num]//CHIP_SIZE)
    cx = int(emy_list_x[emy_num]//CHIP_SIZE)
    emy_list_d[emy_num] = random.randint(0,3)
    if emy_list_d[emy_num] == DIR_UP:
        if map_data.dungeon[cy-1][cx] != 9:
            emy_list_y[emy_num] -= 32
    if emy_list_d[emy_num] == DIR_DOWN:
        if map_data.dungeon[cy+1][cx] != 9:
            emy_list_y[emy_num] += 32
    if emy_list_d[emy_num] == DIR_LEFT:
        if map_data.dungeon[cy][cx-1] != 9:
            emy_list_x[emy_num] -= 32
    if emy_list_d[emy_num] == DIR_RIGHT:
        if map_data.dungeon[cy][cx+1] != 9:
            emy_list_x[emy_num] += 32
    emy_list_a[emy_num] = emy_list_d[emy_num]*3 + ANIMATION[tmr%4]
    if abs(emy_list_x[emy_num]-chara_x) <= 30 and abs(emy_list_y[emy_num]-chara_y) <= 30:
        pl_damage = 10*random.choice([1,2,2,3,3])
        damage_cal(pl_damage)


def obj_animation():
    global obj_a
    obj_a = ANIMATION[tmr%4]


def check_wall():
    global chara_x,chara_y,chara_a,chara_d
    cy = int(chara_y//CHIP_SIZE)
    cx = int(chara_x//CHIP_SIZE)
    if chara_d == DIR_UP:
        if map_data.dungeon[cy-1][cx] != 9:
            chara_y -= 32
    if chara_d == DIR_DOWN:
        if map_data.dungeon[cy+1][cx] != 9:
            chara_y += 32
    if chara_d == DIR_LEFT:
        if map_data.dungeon[cy][cx-1] != 9:
            chara_x -= 32
    if chara_d == DIR_RIGHT:
        if map_data.dungeon[cy][cx+1] != 9:
            chara_x += 32

def check_event():
    global chara_x,chara_y,chara_a,chara_d,idx,pl_damage
    global floor_count,emy_count,item_count,pl_life,pl_stamina
    cy = int(chara_y//CHIP_SIZE)
    cx = int(chara_x//CHIP_SIZE)
    if map_data.dungeon[cy][cx] == 1:
        #ワープの魔法陣にのった
        map_data.make_dungeon()
        map_data.put_event()
        emy_set(0)
        emy_set(1)
        emy_set(2)
        floor_count += 1
        chara_x = chara_y = 146
    if map_data.dungeon[cy][cx] == 2:
        #トラップの魔法陣に乗った
        if item_count > 0:
            item_count -= 1
            map_data.dungeon[cy][cx] = 0
        else:
            pl_damage = 5*random.choice([1,2,2,3,4,3])
            damage_cal(pl_damage)
            map_data.dungeon[cy][cx] = 0
    if map_data.dungeon[cy][cx] == 3:
        #アイテムに接触
        item_count += 1
        map_data.dungeon[cy][cx] = 0
    if map_data.dungeon[cy][cx] == 4:
        #食料に接触
        pl_stamina_recover = 5*random.choice([1,2,2,3,4,3])
        if pl_stamina + pl_stamina_recover > 150:
            pl_stamina = 150
        else:
            pl_stamina += pl_stamina_recover
        map_data.dungeon[cy][cx] = 0


def split_chip(chip_pass,chip_img_x,chip_img_y):
    '''
    複数のチップを１単位のチップに分割する
    '''
    chip_list = []
    for cy in range(0,chip_img_y,CHIP_SIZE):
        for cx in range(0,chip_img_x,CHIP_SIZE):
            chip_list.append(ImageTk.PhotoImage(Image.open(chip_pass).crop((cx,cy,cx+CHIP_SIZE,cy+CHIP_SIZE))))
    return chip_list


def draw_screen():
    st_fnt = ('Times New Roman',30)
    canvas.delete('SCREEN')
    for my in range(len(map_data.dungeon)):
        for mx in range(len(map_data.dungeon[0])):
            if map_data.dungeon[my][mx] != 9:
                canvas.create_image(mx*CHIP_SIZE+(CHIP_SIZE//2),my*CHIP_SIZE+(CHIP_SIZE//2),image=yuka_img[8],tag='SCREEN')
            if map_data.dungeon[my][mx] == 1:
                canvas.create_image(mx*CHIP_SIZE+(CHIP_SIZE//2),my*CHIP_SIZE+(CHIP_SIZE//2),image=obj2_img[obj_a],tag='SCREEN')
            if map_data.dungeon[my][mx] == 2:
                canvas.create_image(mx*CHIP_SIZE+(CHIP_SIZE//2),my*CHIP_SIZE+(CHIP_SIZE//2),image=obj2_img[6+obj_a],tag='SCREEN')
            if map_data.dungeon[my][mx] == 3:
                canvas.create_image(mx*CHIP_SIZE+(CHIP_SIZE//2),my*CHIP_SIZE+(CHIP_SIZE//2),image=takara_img[5],tag='SCREEN')
            if map_data.dungeon[my][mx] == 4:
                canvas.create_image(mx*CHIP_SIZE+(CHIP_SIZE//2),my*CHIP_SIZE+(CHIP_SIZE//2),image=obj_img[25],tag='SCREEN')
            if map_data.dungeon[my][mx] == 9:
                canvas.create_image(mx*CHIP_SIZE+(CHIP_SIZE//2),my*CHIP_SIZE+(CHIP_SIZE//2),image=kabe_img[28],tag='SCREEN')
    canvas.create_image(chara_x,chara_y,image=imgplayer[chara_a],tag='SCREEN')
    canvas.create_image(emy_list_x[0],emy_list_y[0],image=emy_img[emy_list_a[0]],tag='SCREEN')
    canvas.create_image(emy_list_x[1],emy_list_y[1],image=emy2_img[emy_list_a[1]],tag='SCREEN')
    canvas.create_image(emy_list_x[2],emy_list_y[2],image=emy3_img[emy_list_a[2]],tag='SCREEN')
    canvas.create_image(emy_list_x[2],emy_list_y[2],image=emy3_kageimg[emy_list_a[2]],tag='SCREEN')
    canvas.create_text(1110,50,text='{} 階'.format(floor_count),font=st_fnt,fill='black',tag='SCREEN')
    canvas.create_text(1110,100,text='{} 個'.format(item_count),font=st_fnt,fill='black',tag='SCREEN')
    canvas.create_rectangle(1060,135,1210,160,fill='black',tag='SCREEN')
    canvas.create_rectangle(1060,135,1060+pl_life,160,fill='limegreen',tag='SCREEN')
    canvas.create_text(1130,148,text='LIFE',font=('Times New Roman',15),fill='white',tag='SCREEN')
    canvas.create_rectangle(1060,165,1210,190,fill='black',tag='SCREEN')
    canvas.create_rectangle(1060,165,1060+pl_stamina,190,fill='blue',tag='SCREEN')
    canvas.create_text(1130,178,text='STAMINA',font=('Times New Roman',15),fill='white',tag='SCREEN')
    canvas.create_text(1155,210,text='{}のダメージを受けた！'.format(pl_damage),font=('Times New Roman',15),fill='black',tag='SCREEN')


def main():
    global tmr,koff,key,idx
    tmr += 1
    draw_screen()
    if idx == 1:
        if tmr == 1:
            for emy in range(0,emy_num):
                emy_set(emy)
        move_player()
        obj_animation()
        if tmr%2 == 0:
            for emy in range(0,emy_num):
                move_emy(emy)
        if pl_life == 0:
            idx = 2
    if idx == 2:
        draw_text('You Died')
        if tmr == 20:
            idx = 1
            print('hiu')

    if koff == True:
        key = ''
        koff = False

    root.after(130,main)



root = tkinter.Tk()
root.title('メイドで冥土探検！')
root.bind('<KeyPress>',key_down)
root.bind('<KeyRelease>',key_up)
canvas = tkinter.Canvas(width=1256,height=864)
imgplayer = split_chip(imgplayer_pass,96,128)
emy_img = split_chip(emy_img_pass,96,128)
emy2_img = split_chip(emy2_img_pass,96,128)
emy3_img = split_chip(emy3_img_pass,96,128)
emy3_kageimg = split_chip(emy3_kageimg_pass,96,128)
takara_img = split_chip(takara_img_pass,256,64)
obj_img = split_chip(obj_pass,256,224)
obj2_img = split_chip(obj2_pass,96,128)
yuka_img = split_chip(yuka_pass,64,160)
kabe_img = split_chip(kebe_pass,256,192)
canvas.pack()
main()
root.mainloop()
