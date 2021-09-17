import pygame
import copy
from random import *

import text

pygame.init()
V = pygame.Vector2
# coordinate positions for tetris pieces in a 4x4 area


FIGURES = {
    "I":{"name":"I","coordinates":[V(1,0),V(1,1),V(1,2),V(1,3)],"center":None,"2rotate":True,"colour":(0, 255, 255)},
    "T":{"name":"T","coordinates":[V(1,0),V(1,1),V(0,1),V(1,2)],"center":V(1,1),"2rotate":False,"colour":(128, 0, 128)},
    "O":{"name":"O","coordinates":[V(1,1),V(2,2),V(1,2),V(2,1)],"center":None,"2rotate":True,"colour":(255, 255, 0)},
    "L":{"name":"L","coordinates":[V(0,1),V(1,1),V(2,1),V(2,0)],"center":V(1,1),"2rotate":False,"colour":(255, 127, 0)},
    "J":{"name":"J","coordinates":[V(0,1),V(1,1),V(2,1),V(0,0)],"center":V(1,1),"2rotate":False,"colour":(127, 127, 127)},
    "S":{"name":"S","coordinates":[V(0,1),V(1,1),V(1,0),V(2,0)],"center":V(1,1),"2rotate":True,"colour":(0, 255, 0)},
    "Z":{"name":"Z","coordinates":[V(0,0),V(1,1),V(1,0),V(2,1)],"center":V(1,1),"2rotate":True,"colour":(255, 0, 0)}
}

"""WALL_KICKS = (
    ((-1, 0), (-1, 1), (0, -2), (-1, -2)),
    ((1, 0), (1, -1), (0, 2), (1, 2)),
    ((1, 0), (1, 1), (0, -2), (1, -2)),
    ((-1, 0), (-1, -1), (0, 2), (-1, 2))
)

WALL_KICKS_I = (
    ((-2, 0), (1, 0), (-2,-1), (1,2)),
    ((-1,0), (2, 0), (-1,2), (2,-1)),
    ((2, 0), (-1, 0), (2,1), (-1,-2)),
    ((1,0), (-2, 0), (1,-2), (-2,1)),
)"""


def reverse_signs(l,x,y):
    new = []
    for v in l:
        if x:
            v = V(-v[0],v[1])
        if y:
            v = V(v[0],-v[1])
        new.append(v)
    return new

wall_temps = [[V(-1,0),V(-1,1),V(0,-2),V(-1,-2)],
              [V(-2,0),V(1,0),V(-2,-1),V(1,2)],
              [V(-1,0),V(2,0),V(-1,2),V(2,-1)]
              ]
WALL_KICKS = {
    "0>R":wall_temps[0],
    "R>0":reverse_signs(wall_temps[0],True,True),
    "R>2":reverse_signs(wall_temps[0],True,True),
    "2>R":wall_temps[0],
    "2>L":reverse_signs(wall_temps[0],True,False),
    "L>2":reverse_signs(wall_temps[0],False,True),
    "L>0":reverse_signs(wall_temps[0],False,True),
    "0>L":reverse_signs(wall_temps[0],True,False)
}
for k in WALL_KICKS:
    print(k,":",WALL_KICKS[k])
WALL_KICKS_I = {
    "0>R":wall_temps[1],
    "R>0":reverse_signs(wall_temps[1],True,True),
    "R>2":wall_temps[2],
    "2>R":reverse_signs(wall_temps[2],True,True),
    "2>L":wall_temps[1],
    "L>2":reverse_signs(wall_temps[1],True,True),
    "L>0":reverse_signs(wall_temps[2],True,True),
    "0>L":wall_temps[2]
}


def int_tuple(vector):
    return int(vector[0]), int(vector[1])


# returns rotated coordinates from a figure dictionary
def rotate_figure(figure1,rotations):
    # use deepcopy to avoid making changes to constant
    coordinates = copy.deepcopy(figure1["coordinates"])
    center = figure1["center"]
    rotate_2 = figure1["2rotate"]

    # get the minimum num of rotations needed to get the new shape
    rotation = rotations % 4
    if rotate_2:
        rotation = rotations % 2

    new_coordinates = []
    # if center is None, rotate the tetrimino by the center of a 4x4 grid
    if center is None:
        if rotation == 0:
            new_coordinates = coordinates
        else:
            # add new coordinates to list
            for coord in coordinates:
                new_coordinates.append(V(coord[1],coord[0]))
    else:
        # get a copy of the original coordinates of the tetrimino
        prev_coordinates = copy.deepcopy(coordinates)
        # repeat for num of rotations
        for _ in range(abs(rotation)):
            # do for all coordinates
            for coord in prev_coordinates:
                # move coord to allow pivot from 0,0
                coord -= center
                # pivot clockwise(+) or anticlockwise(-)
                coord = V(-coord[1],coord[0])
                if rotation < 0:
                    coord = V(coord[1],-coord[0])
                coord += center
                # add coords to new list
                new_coordinates.append(coord)
            # move the new coords to previous coords to allow more rotations
            prev_coordinates = copy.deepcopy(new_coordinates)
            new_coordinates = []
        new_coordinates = prev_coordinates
    return new_coordinates


# apply rotations for correct tetrimino spawning
FIGURES["I"]["coordinates"] = rotate_figure(FIGURES["I"],1)
FIGURES["T"]["coordinates"] = rotate_figure(FIGURES["T"],-1)
FIGURES["J"]["coordinates"] = rotate_figure(FIGURES["J"],2)
FIGURES["L"]["coordinates"] = rotate_figure(FIGURES["L"],2)


# prints all the pieces and their rotation to the console
def print_tetriminos():
    for key in FIGURES:
        figure = FIGURES[key]
        print("piece:",figure["name"])
        for i in range(4):
            print("rotation:",i)
            coords = rotate_figure(figure,i)
            for y in range(4):
                string = ""
                for x in range(4):
                    if V(x,y) in coords:
                        string += "⬛"
                    else:
                        string += "⬜"
                    string += " "
                print(string)
        print("--")


class Timers:
    def __init__(self):
        self.timers = {}

    def check_timer(self,tag,max_time):
        if tag not in self.timers:
            self.timers[tag] = {"max_time":max_time,"time":0}
        else:
            if self.timers[tag]["time"] >= self.timers[tag]["max_time"]:
                return True
        return False

    def reset_timer(self,tag):
        if tag in self.timers:
            self.timers[tag]["time"] = 0

    def just_set(self,tag):
        if tag in self.timers:
            if self.timers[tag]["time"] == 0:
                return True
        return False

    def just_finished(self,tag):
        if "finished" not in self.timers[tag] and self.check_timer(tag,self.timers[tag]["max_time"]):
            self.timers[tag]["finished"] = True
            return True
        return False

    def lerp(self,tag):
        return self.timers[tag]["time"]/self.timers[tag]["max_time"]

    def update(self,screen):
        for k in self.timers:
            timer = self.timers[k]
            if timer["time"] < timer["max_time"]:
                timer["time"] += dt

    def exists(self,tag):
        return tag in self.timers


class Tetrimino:
    def __init__(self,name=None):
        self.offset = V(3,-2)

        self.down_timer_max = 0.5
        self.down_timer_max_fast = 0.05
        self.set_timer_max = 1

        timers.reset_timer("tetrimino:down_timer")
        timers.reset_timer("tetrimino:down_timer_fast")
        timers.reset_timer("tetrimino:set_timer")

        self.rotation = 0

        self.delete = False
        if name is None:
            name = choice("I T O L J S Z".split(" "))

        self.figure = copy.deepcopy(FIGURES[name])
        self.coordinates = copy.deepcopy(self.figure["coordinates"])

        self.images = []
        for _ in range(4):
            self.images.append(choice([4]))

        self.get_rect()

        self.inbetween = 0

    def reset_pos(self):
        self.offset = V(3, -2)

    def reset_rotation(self):
        self.coordinates = copy.deepcopy(self.figure["coordinates"])

    def draw(self,screen,play_offset=V(0,0),width=1):
        for i in range(4):
            coord = self.coordinates[i]
            c_scale = width

            # pygame.draw.rect(self,screen.figure["colour"],pygame.Rect(((coord+self.offset)*c_scale)+play_offset,V(c_scale,c_scale)))
            screen.blit(block_images[self.images[i]],((coord+self.offset)*c_scale)+play_offset+self.inbetween)

    def draw_preview(self,screen,play_offset,width=1):
        for i in range(4):
            coord = self.coordinates[i]
            c_scale = width
            if width == 9:
                screen.blit(block_images[self.images[i]], (coord * c_scale) + play_offset)
            else:
                screen.blit(small_block_images[self.images[i]], (coord * c_scale) + play_offset)

    def to_blocks(self):
        blocks = []
        for i in range(4):
            coord = self.coordinates[i]
            blocks.append(Block(self.figure["colour"],coord+self.offset,self.images[i]))
        return blocks

    def get_rect(self):
        max_x = 0
        max_y = 0
        for coord in self.coordinates:
            max_x = max(max_x,coord[0])
            max_y = max(max_y,coord[1])
        min_x = 4
        min_y = 4
        for coord in self.coordinates:
            min_x = min(min_x,coord[0])
            min_y = min(min_y,coord[1])
        self.rect = pygame.Rect(V(min_x,min_y),V(max_x-min_x,max_y-max_y))
        return self.rect

    def update(self,screen,blocks):
        left = controls["left"] in keys_pressed
        right = controls["right"] in keys_pressed
        turn_l = controls["rotate left"] in keys_pressed
        turn_r = controls["rotate right"] in keys_pressed
        drop = controls["hard drop"] in keys_pressed

        if not (controls["left"] in keys_held and controls["right"] in keys_held):
            if left:
                self.move(V(-1,0),blocks)
            elif right:
                self.move(V(1, 0),blocks)

        if turn_l:
            self.rotate(1,blocks)
        if turn_r:
            self.rotate(-1,blocks)

        if (timers.check_timer("tetrimino:down_timer",self.down_timer_max) and not controls["soft drop"] in keys_held) or \
                (timers.check_timer("tetrimino:down_timer_fast",self.down_timer_max_fast) and controls["soft drop"] in keys_held):
            timers.reset_timer("tetrimino:down_timer")
            timers.reset_timer("tetrimino:down_timer_fast")
            self.move(V(0,1),blocks)

        if right or left or turn_r or turn_l:
            timers.reset_timer("tetrimino:set_timer")

        if not self.try_move(V(0,1),blocks):
            if timers.check_timer("tetrimino:set_timer",self.set_timer_max):
                timers.reset_timer("tetrimino:set_timer")
                self.delete = True
        else:
            timers.reset_timer("tetrimino:set_timer")

        if drop:
            check = True
            while check:
                check = self.move(V(0,1),blocks)
            self.delete = True

        self.inbetween = V(0, 0)
        if timers.exists("tetrimino:down_timer") and self.try_move(V(0, 1), blocks):
            self.inbetween = V(0, timers.lerp("tetrimino:down_timer") * 9)

    def rotate(self,rotation,blocks):
        temp_rotation = copy.deepcopy(self.rotation)
        self.rotation += rotation
        self.rotation = self.rotation % 4
        rotated_coordinates = rotate_figure(self.figure,self.rotation)

        m = ["0","L","2","R"]

        r1 = m[temp_rotation]
        r2 = m[self.rotation]
        translation_key = r1 + ">" + r2

        if not self.try_move(V(0,0),blocks,rotated_coordinates):

            if self.figure["name"] == "I":
                translations = WALL_KICKS_I[translation_key]
            else:
                translations = WALL_KICKS[translation_key]
            translation = None
            for t in translations:
                t = V(t[0],t[1])
                if self.try_move(t,blocks,rotated_coordinates):
                    translation = t
                    break
            if translation is not None:
                self.move(translation,blocks)
                self.coordinates = rotated_coordinates
            else:
                self.rotation -= rotation
        else:
            self.coordinates = rotated_coordinates

    def move(self,displacement,blocks):
        new_coords = []
        for coord in self.coordinates:
            new_coords.append(coord+displacement+self.offset)
        if self.is_valid(new_coords,blocks):
            self.offset += displacement
            return True
        return False

    def try_move(self,displacement,blocks,coordinates=None):
        if coordinates is None:
            coordinates = self.coordinates
        new_coords = []
        for coord in coordinates:
            new_coords.append(coord + displacement + self.offset)
        if self.is_valid(new_coords, blocks):
            return True
        return False

    def is_valid(self,coordinates,blocks):
        for coord in coordinates:
            if coord in blocks or coord[0] < 0 or coord[0] > 9 or coord[1] > tetris_height-1:
                return False
        return True

    def apply_offset(self,coordinates,offset):
        new_coordinates = []
        for coord in coordinates:
            new_coordinates.append(coord+offset)
        return new_coordinates

    def get_image(self,width=9):
        minx = 4
        miny = 4
        maxx = 0
        maxy = 0
        for i in range(4):
            coord = self.coordinates[i]
            minx = min(coord[0], minx)
            maxx = max(coord[0], maxx)
            miny = min(coord[1], miny)
            maxy = max(coord[1], maxy)
        new_coords = []
        for coord in self.coordinates:
            new_coords.append(coord-V(minx,miny))

        surf = pygame.Surface(V(maxx-minx+1,maxy-miny+1)*width,pygame.SRCALPHA)
        for i in range(4):
            coord = new_coords[i]
            if width == 9:
                surf.blit(block_images[self.images[i]], coord * width)
            else:
                surf.blit(small_block_images[self.images[i]], coord * width)
        return surf





class Block:
    def __init__(self,colour,pos,image=None):
        self.pos = pos
        self.colour = colour
        self.image = image

    def update(self,screen,offset,width):
        c_scale = width
        if self.image is None:
            pygame.draw.rect(screen, self.colour, pygame.Rect((self.pos * c_scale)+offset, V(c_scale,c_scale)))
        else:
            screen.blit(block_images[self.image], (self.pos * c_scale)+offset)




class PlayField:
    def __init__(self):
        self.playfield_image = pygame.image.load("images/UI.png").convert_alpha()
        self.grid_image = pygame.image.load("images/grid.png").convert_alpha()
        self.grid_rect = pygame.Rect(V(45,9),V(90,180))

        self.held_rect = pygame.Rect(V(4, 29), V(36, 27))
        self.next_rect = pygame.Rect(V(140, 29), V(36, 27))

        self.preview_rect = pygame.Rect(V(139, 75), V(20, 70))

        self.achievement_rect = pygame.Rect(V(18,67),V(23,23))

        self.blocks_offset = V(self.grid_rect.topleft)
        self.block_width = 9
        self.block_width_small = 5

        self.init()

    def init(self):
        self.blocks = []
        self.current = Tetrimino()
        self.held = None
        self.held_once = False
        self.next = None
        self.preview_num = 4
        self.previews = []
        self.bag_template = []
        for c in "I T L J O S Z".split(" "):
            self.bag_template.append(Tetrimino(c))
        self.bag = copy.deepcopy(self.bag_template)

        self.refill_previews()
        self.get_next()
        self.refill_previews()

    def refill_previews(self):
        if self.preview_num>1:
            while len(self.previews) < self.preview_num-1:
                if not self.bag:
                    self.bag = copy.deepcopy(self.bag_template)
                shuffle(self.bag)
                self.previews.append(self.bag.pop(0))

    def get_next(self):
        next_current = copy.deepcopy(self.next)
        self.next = self.previews.pop(0)
        return next_current

    def draw_previews(self,screen):
        next_image = self.next.get_image()
        next_rect_image = next_image.get_rect()
        next_rect_image.center = self.next_rect.center
        screen.blit(next_image,next_rect_image)

        if self.held is not None:
            held_image = self.held.get_image()
            held_rect_image = held_image.get_rect()
            held_rect_image.center = self.held_rect.center
            screen.blit(held_image,held_rect_image)

        ypointer = 0
        for i in self.previews:
            preview_image = i.get_image(self.block_width_small)
            preview_rect_image = preview_image.get_rect()
            preview_rect_image.centerx = self.preview_rect.centerx
            preview_rect_image.top = self.preview_rect.top+ypointer
            screen.blit(preview_image,preview_rect_image)

            ypointer += (self.block_width_small*2)+2

    def draw(self,screen):
        screen.blit(self.playfield_image,V(0,0))

    def update(self,screen):
        screen.blit(self.grid_image, self.blocks_offset)

        self.current.update(screen,self.get_block_coords())
        self.current.draw(screen,self.blocks_offset,self.block_width)

        if self.current.delete:
            self.held_once = False
            blocks = self.current.to_blocks()
            for block in blocks:
                self.blocks.append(block)
            self.current = self.get_next()
            self.refill_previews()
            self.clear_lines(blocks)

        for block in self.blocks:
            block.update(screen,self.blocks_offset,self.block_width)

        if controls["hold/swap"] in keys_pressed and not self.held_once:
            if self.held is None:
                self.held = copy.deepcopy(self.current)
                self.current = self.get_next()
                self.refill_previews()
            else:
                self.held_once = True
                held_temp = copy.deepcopy(self.held)
                self.held = copy.deepcopy(self.current)
                self.held.reset_rotation()
                self.current = held_temp
                self.current.reset_pos()
                self.held.reset_pos()

        self.draw_previews(screen)

        self.draw(screen)

        if controls["restart"] in keys_pressed:
            self.init()

    def get_block_coords(self):
        coords = []
        for block in self.blocks:
            coords.append(block.pos)
        return coords

    def clear_lines(self,blocks_new):
        """
        lines = []
        for block in blocks_new:
            if block.pos[1] not in lines:
                lines.append(block.pos[1])
        to_remove = []

        for y in lines:
            line_blocks = []
            for b in self.blocks:
                if b.pos[1] == y:
                    line_blocks.append(b)
            if len(line_blocks) >= 10:
                for b in self.blocks:
                    if b.pos[1]<y:
                        b.pos[1] += 1
                for b in line_blocks:
                    to_remove.append(b)

        for b in to_remove:
            self.blocks.remove(b)"""

        lines = {}
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            ypos = block.pos[1]
            if str(ypos) not in lines:
                lines[str(ypos)] = []

            lines[str(ypos)].append(i)

        move_down = []
        print(lines)
        for ypos in lines:
            line = lines[ypos]
            print(line)
            if len(line) >= 10:
                for i in range(-1,int(ypos)+1):
                    move_down.append(i)
                for block in line:
                    self.blocks.pop(block)

        for line in move_down:
            pass





clock = pygame.time.Clock()

tetris_height = 20
scale = 4

game_dims = V(180,190)
game_screen = pygame.Surface(int_tuple(game_dims),pygame.HWSURFACE)
window_dims = V(180,190)
window = pygame.display.set_mode(int_tuple(game_dims),pygame.RESIZABLE)

block_images = []
img = pygame.image.load("images/blocks.png")
for y in range(4):
    for x in range(4):
        rect = pygame.Rect(V(9*x,9*y),V(9,9))
        surf = img.subsurface(rect)
        surf.convert()
        block_images.append(surf)
small_block_images = []
for i in block_images:
    smaller = pygame.transform.scale(i,(5,5))
    smaller.convert()
    small_block_images.append(smaller)

ach_images = []
img = pygame.image.load("images/achievements.png")
for y in range(4):
    rect = pygame.Rect(V(0,23*y),V(23,23))
    surf = img.subsurface(rect)
    surf.convert()
    ach_images.append(surf)

keys_held = []
keys_pressed = []
controls = {"hard drop":"w",
            "soft drop":"s",
            "left":"a",
            "right":"d",
            "rotate left":"j",
            "rotate right":"k",
            "hold/swap":"l",
            "restart":"r",
            }
keys_allow_hold = {controls["left"]:(0.1,0.05),
                   controls["right"]:(0.1,0.05)}


timers = Timers()

game = PlayField()

while True:
    keys_pressed = []
    game_screen.fill((0, 0, 0))
    window.fill((0, 0, 0))
    dt = clock.tick(60)/1000
    pygame.display.set_caption(str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            window_dims = V(event.w,event.h)
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            key = event.key
            name = pygame.key.name(key)
            if event.type == pygame.KEYDOWN:
                if name not in keys_held:
                    keys_pressed.append(name)
                    keys_held.append(name)
                if name in keys_held:
                    tag1 = "key:" + name + ":first"
                    timers.reset_timer(tag1)
            if event.type == pygame.KEYUP:
                if name in keys_held:
                    keys_held.remove(name)

    for name in keys_held:
        if name in keys_allow_hold:
            tag1 = "key:" + name + ":first"
            tag2 = "key:" + name + ":second"
            if timers.check_timer(tag1, keys_allow_hold[name][0]):
                """if not timers.check_timer(tag2, keys_allow_hold[name][0]) and timers.just_set(tag2):
                    keys_pressed.append(name)
                    timers.reset_timer(tag)
                elif timers.check_timer(tag2, keys_allow_hold[name][0]):
                    keys_pressed.append(name)"""
                if timers.just_finished(tag1):
                    keys_pressed.append(name)
                else:
                    if timers.check_timer(tag2, keys_allow_hold[name][0]):
                        timers.reset_timer(tag2)
                        keys_pressed.append(name)

    timers.update(game_screen)
    game.update(game_screen)

    # str_img = text.generate_text("Badtris",(255,255,255),(0,0,0))
    # game_screen.blit(str_img,(0,0))

    xdiv = window_dims[0]//game_dims[0]
    ydiv = window_dims[1] // game_dims[1]
    scale = min(xdiv,ydiv)

    scaled_game_dims = game_dims*scale
    scaled_game_screen = pygame.transform.scale(game_screen,int_tuple(scaled_game_dims))
    scaled_rect = scaled_game_screen.get_rect()
    scaled_rect.center = pygame.Rect((0,0),window_dims).center
    window.blit(scaled_game_screen,scaled_rect.topleft)


    pygame.display.flip()


