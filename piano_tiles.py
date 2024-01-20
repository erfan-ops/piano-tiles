import pygame
from pygame.locals import *
from settings import *
from sys import exit as sExit
from random import choice
from win32api import EnumDisplaySettings, EnumDisplayDevices
from keyboard import get_hotkey_name


class SongInfo:
    def __init__(self) -> None:
        song_file = open("settings.json")
        self._SETTINGS:dict = load(song_file)
        self.song_speed = self._SETTINGS["song_speed"] * self._SETTINGS["tile_height"] * H_RATIO


class Tile(SongInfo):
    def __init__(self, x, speed, w=WIDTH//LINES) -> None:
        super().__init__()
        self.tile_width = w
        self.tile_height = self._SETTINGS["tile_height"] * H_RATIO
        self.rect = pygame.Rect(x, -self.tile_height, self.tile_width, self.tile_height)
        
        self.img = pygame.surface.Surface((self.tile_width, self.tile_height))
        
        self.speed = speed * H_RATIO


class BG(SongInfo):
    def __init__(self) -> None:
        super().__init__()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("piano tiles by erfan :D")
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))
        
        self.colors = self._SETTINGS["colors"]["bg_colors"]
        self.colors_len = len(self.colors)
        self.main_r = self.colors[0][0]
        self.main_g = self.colors[0][1]
        self.main_b = self.colors[0][2]
        self.r = self.colors[0][0]
        self.g = self.colors[0][1]
        self.b = self.colors[0][2]
        self.enum = 1
        self.rainbow_color_speed = self._SETTINGS["colors"]["rainbow_color_speed"]
        self.rainbow_layers = self._SETTINGS["rainbow_bg_layers"]
        if self.rainbow_layers > self.colors_len:
            self.rainbow_layers = self.colors_len
        
        self.rainbow_layers_1 = self.rainbow_layers - 1
    
    
    def fill(self, surface: pygame.Surface, color_group="bg_colors"):
        h = surface.get_height()
        w = surface.get_width()
        ratio = self.rainbow_layers/h
        
        self.bg_colors = self._SETTINGS["colors"][color_group]
        en = int(self.enum)
        self.ri = (self.bg_colors[en][0]-self.r)*self.dt
        self.gi = (self.bg_colors[en][1]-self.g)*self.dt
        self.bi = (self.bg_colors[en][2]-self.b)*self.dt
        for i in range(self.rainbow_layers_1):
            r, g, b = self.bg_colors[i][0], self.bg_colors[i][1], self.bg_colors[i][2]
            r_interval = (self.bg_colors[i+1][0] - r) * ratio
            g_interval = (self.bg_colors[i+1][1] - g) * ratio
            b_interval = (self.bg_colors[i+1][2] - b) * ratio
            
            for height in range(h//self.rainbow_layers_1 * i, h//self.rainbow_layers_1 * (i+1)):
                r += r_interval + self.ri
                g += g_interval + self.gi
                b += b_interval + self.bi
                
                if r > 255:
                    r = 255
                elif r < 0:
                    r = 0
                
                if g > 255:
                    g = 255
                elif g < 0:
                    g = 0
                
                if b > 255:
                    b = 255
                elif b < 0:
                    b = 0
                
                pygame.draw.line(surface, (int(r), int(g), int(b)), (0, height), (w, height))
            
        
            self.enum += self.dt * self.rainbow_color_speed
            self.enum %= self.colors_len
        
        self.r, self.g, self.b, = r, g, b


class App(BG):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()

        self.screen = BG()
        
        self.running = True
        self.clock = pygame.time.Clock()
        
        self.repeat = self._SETTINGS["repeat"]
        
        self.line = (WIDTH//4) * choice(range(0, 4))
        
        self.go_font = pygame.font.Font(f"fonts/{self._SETTINGS['font']}", int(80 * W_RATIO * H_RATIO))
        self.reset_font = pygame.font.Font(f"fonts/{self._SETTINGS['font']}", int(40 * W_RATIO * H_RATIO))
        
        if self._SETTINGS["fps"] == "VSync":
            self._REFRESH_RATE: int = EnumDisplaySettings(EnumDisplayDevices().DeviceName, -1).DisplayFrequency
        else:
            self._REFRESH_RATE = self._SETTINGS["fps"]
        
        self.dt = 1/self._REFRESH_RATE
        
        self.score = 0
        self.score_text = self.go_font.render(str(self.score), 0, self._SETTINGS["colors"]["score_color"])
        self.score_text_rect = self.score_text.get_rect()
        
        self.speed_increase_rate = self._SETTINGS["speed_increase_rate"] * self._SETTINGS["tile_height"]
        self.colors = self._SETTINGS["colors"]
        
        for n in self._SETTINGS["keys"]:
            for v in self._SETTINGS["keys"][n]:
                if v == ";":
                    self._SETTINGS["keys"][n][self._SETTINGS["keys"][n].index(v)] = "COLON"
                elif v == "space":
                    self._SETTINGS["keys"][n][self._SETTINGS["keys"][n].index(v)] = "SPACE"
        
        match LINES:
            case 2:
                self.keys = [eval(f'K_{i}') for i in self._SETTINGS["keys"]["2"]]
            case 3:
                self.keys = [eval(f'K_{i}') for i in self._SETTINGS["keys"]["3"]]
            case 4:
                self.keys = [eval(f'K_{i}') for i in self._SETTINGS["keys"]["4"]]
            case 5:
                self.keys = [eval(f'K_{i}') for i in self._SETTINGS["keys"]["5"]]
            case 6:
                self.keys = [eval(f'K_{i}') for i in self._SETTINGS["keys"]["6"]]
            case 7:
                self.keys = [eval(f'K_{i}') for i in self._SETTINGS["keys"]["7"]]
            case 8:
                self.keys = [eval(f'K_{i}') for i in self._SETTINGS["keys"]["8"]]
            case 9:
                self.keys = [eval(f'K_{i}') for i in self._SETTINGS["keys"]["9"]]
        
        self.spawn_rates = []
        for s in range(LINES):
            for _ in range(self._SETTINGS["spawn_rates"][list(self._SETTINGS["spawn_rates"].keys())[s]]):
                self.spawn_rates.append(list(self._SETTINGS["spawn_rates"].keys())[s])
        
        if self._SETTINGS["show_score"] and self._SETTINGS["show_speed"]:
            self.render_ss = self.rss
        elif self._SETTINGS["show_score"]:
            self.render_ss = self.r_scr
        elif self._SETTINGS["show_speed"]:
            self.render_ss = self.r_spd
        else:
            self.render_ss = lambda: None
        
        if self._SETTINGS["show_fps"]:
            self.show_fps2 = self.show_fps
        
        pygame.mixer.music.load(self._SETTINGS["song"])
        
        if self._SETTINGS["rainbow_bg"]:
            self.fill_bg = self.fill
        else:
            self.fill_bg = self.fill_surface
    
    
    def generate_new_tile(self) -> Tile:
        l = choice(range(0, LINES))
        x = (WIDTH//LINES) * l
        t = Tile(x, self.song_speed)
        t.related_key = self.keys[l]
        remove_items = [l, ]
        
        note_type = choice(self.spawn_rates)
        if note_type == "single_note_spawn_rate" and LINES >= 1:
            l = choice(range(0, LINES))
            x = (WIDTH//LINES) * l
            
            while x == self.line and not self.repeat:
                l = choice(range(0, LINES))
                x = (WIDTH//LINES) * l
            
            if self.repeat:
                l = choice(range(0, LINES))
                x = (WIDTH//LINES) * l
            
            
            self.line = x
            
            t = Tile(x, self.d_song_speed*self._SETTINGS["tile_height"]*H_RATIO)
            t.related_key = self.keys[l]
            
            self.tiles.append(t)
        
        elif note_type == "double_note_spawn_rate" and LINES >= 2:
            self.tiles.append(t)
            
            l2 = list(range(0, LINES))
            l2.remove(l)
            l = choice(l2)
            x = (WIDTH//LINES) * l
            t = Tile(x, self.song_speed)
            t.related_key = self.keys[l]
            self.tiles.append(t)
        
        elif note_type == "triple_note_spawn_rate" and LINES >= 3:
            self.tiles.append(t)
            
            for _ in range(2):
                l2 = list(range(0, LINES))
                for item in remove_items:
                    l2.remove(item)
                l = choice(l2)
                x = (WIDTH//LINES) * l
                t = Tile(x, self.song_speed)
                t.related_key = self.keys[l]
                self.tiles.append(t)
                remove_items.append(l)
        
        elif note_type == "quad_note_spawn_rate" and LINES >= 4:
            self.tiles.append(t)
            for _ in range(3):
                l2 = list(range(0, LINES))
                for item in remove_items:
                    l2.remove(item)
                l = choice(l2)
                x = (WIDTH//LINES) * l
                t = Tile(x, self.song_speed)
                t.related_key = self.keys[l]
                self.tiles.append(t)
                remove_items.append(l)
    
    
    def quit(self) -> None:
        self.running = False
        pygame.quit()
        sExit()
    
    
    def check_for_quit(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            
            elif event.type == QUIT:
                self.quit()
    
    
    def update_score(self):
        self.score_text = self.go_font.render(str(self.score), 1, self._SETTINGS["colors"]["score_color"])
        self.score_text_rect = self.score_text.get_rect()
    
    
    def pop_tile(self, i=0):
        self.update_score()
        
        self.tiles.pop(i)
        if self.tiles:
            self.current_note_key = self.tiles[0].related_key
    
    
    def pop_rel_tile(self, t_type, key):
        for i in range(t_type):
            if self.tiles[i].related_key == key:
                self.tiles.pop(i)
                self.current_note_key = self.tiles[0].related_key
    
    
    def show_fps(self):
        fps_text: pygame.Surface = self.reset_font.render(f"{(self.clock.get_fps()):.2f}", 1, self._SETTINGS["colors"]["score_color"])
        fps_text_rect = fps_text.get_rect()
        self.screen.surface.blit(fps_text, (10*W_RATIO, 10*H_RATIO), fps_text_rect)
    
    
    def mouse_col_check(self, mouse_x, mouse_y, rect):
        if mouse_x > rect.left and mouse_x < rect.right and mouse_y > rect.top and mouse_y < rect.bottom:
            return True
    
    
    def game_over(self):
        pygame.mixer.music.stop()
        self.score = 0
        self.update_score()
        
        self.song_speed = self._SETTINGS["song_speed"] * self._SETTINGS["tile_height"]
        self.d_song_speed = self._SETTINGS["song_speed"]
        self.tile_spawn_rate = self._SETTINGS["tile_height"]/self.song_speed
        
        
        self.tiles = []
        
        go_text_color: tuple[int, int, int] = self._SETTINGS["colors"]["game_over_start_color"]
        r, g, b = go_text_color[0], go_text_color[1], go_text_color[2]
        r_interval = self._SETTINGS["colors"]["game_over_end_color"][0] - r
        g_interval = self._SETTINGS["colors"]["game_over_end_color"][1] - g
        b_interval = self._SETTINGS["colors"]["game_over_end_color"][2] - b
        
        go_text = self.go_font.render("GAME OVER", 0, go_text_color)
        go_text_rect = go_text.get_rect()
        
        reset = self.reset_font.render("press any key to continue", 0, self._SETTINGS["colors"]["game_over_end_color"])
        reset_rect = reset.get_rect()
        
        timer = 0
        while True:
            self.check_for_quit()
            self.fill_bg(self.screen.surface)
            self.screen.surface.blit(go_text, (WIDTH//2 - go_text_rect.width//2, 100), go_text_rect)
            
            r += self._SETTINGS["game_over_fade_in_time"] * r_interval * self.dt
            g += self._SETTINGS["game_over_fade_in_time"] * g_interval * self.dt
            b += self._SETTINGS["game_over_fade_in_time"] * b_interval * self.dt
            
            if r > 255:
                r = 255
            elif r < 0:
                r = 0
            
            if g > 255:
                g = 255
            elif g < 0:
                g = 0
            
            if b > 255:
                b = 255
            elif b < 0:
                b = 0
            
            go_text_color: tuple[int, int, int] = int(r), int(g), int(b)
            go_text = self.go_font.render("GAME OVER", 0, go_text_color)
            
            timer += self.dt
            
            if timer >= 1:
                self.screen.surface.blit(reset, (WIDTH//2 - reset_rect.w//2, HEIGHT//2 - reset_rect.h//2), reset_rect)
                if get_hotkey_name():
                    break
            
            pygame.display.flip()
            self.clock.tick(self._REFRESH_RATE)
        
        pygame.mixer.music.play()
    
    
    def rss(self):
        speed_text: pygame.Surface = self.go_font.render(f"{(self.d_song_speed):.2f}", 1, self._SETTINGS["colors"]["score_color"])
        speed_text_rect = speed_text.get_rect()
        self.screen.surface.blit(speed_text, (WIDTH//2 - speed_text_rect.w//2, 110*H_RATIO), speed_text_rect)
        self.r_scr()
    
    def r_spd(self):
        speed_text: pygame.Surface = self.go_font.render(f"{(self.d_song_speed):.2f}", 1, self._SETTINGS["colors"]["score_color"])
        speed_text_rect = speed_text.get_rect()
        self.screen.surface.blit(speed_text, (WIDTH//2 - speed_text_rect.w//2, 10*H_RATIO), speed_text_rect)
    
    def r_scr(self):
        self.screen.surface.blit(self.score_text, (WIDTH//2 - self.score_text_rect.w//2, 10*H_RATIO), self.score_text_rect)
    
    
    def fill_surface(self, surface: pygame.Surface, color_group="bg_colors"):
        colors = self._SETTINGS["colors"][color_group]
        l_colors = len(self._SETTINGS["colors"][color_group])
        l_colors_1 = l_colors-1
        
        h = surface.get_height()
        w = surface.get_width()
        for i in range(l_colors_1):
            r, g, b = colors[i][0], colors[i][1], colors[i][2]
            
            r_interval = (colors[i+1][0] - r) / h * l_colors_1
            g_interval = (colors[i+1][1] - g) / h * l_colors_1
            b_interval = (colors[i+1][2] - b) / h * l_colors_1
            
            for j in range(h//l_colors_1 * i, h//l_colors_1 * (i+1)):
                pygame.draw.line(surface, (r, g, b), (0, j), (w, j))
                r += r_interval
                g += g_interval
                b += b_interval
                
                if r > 255:
                    r = 255
                elif r < 0:
                    r = 0
                
                if g > 255:
                    g = 255
                elif g < 0:
                    g = 0
                
                if b > 255:
                    b = 255
                elif b < 0:
                    b = 0
    
    
    def run(self):
        self.timer = 0
        self.dt = 1/self._REFRESH_RATE
        
        self.song_speed = self._SETTINGS["song_speed"] * self._SETTINGS["tile_height"]
        self.d_song_speed = self._SETTINGS["song_speed"]
        self.tile_spawn_rate = self._SETTINGS["tile_height"]/self.song_speed
        self.tsr = self.tile_spawn_rate
        
        self.tiles: list[Tile] = []
        self.generate_new_tile()
        self.current_note_key = self.tiles[0].related_key
        
        pygame.event.set_blocked(MOUSEMOTION)
        pygame.mixer.music.play()
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quit()
                    
                    if len(self.tiles) >= 3 and self.tiles[0].rect.y == self.tiles[1].rect.y and self.tiles[0].rect.y == self.tiles[2].rect.y:
                        if event.key in [self.tiles[0].related_key, self.tiles[1].related_key, self.tiles[2].related_key]:
                            self.pop_rel_tile(3, event.key)
                            self.score += 1
                        
                        elif event.key in self.keys:
                            self.game_over()
                        break
                    
                    elif len(self.tiles) >= 2 and self.tiles[0].rect.y == self.tiles[1].rect.y:
                        if event.key in [self.tiles[0].related_key, self.tiles[1].related_key]:
                            self.pop_rel_tile(2, event.key)
                            self.score += 1
                        
                        elif event.key in self.keys:
                            self.game_over()
                        break
                    
                    elif len(self.tiles) >= 1:
                        if event.key == self.current_note_key:
                            self.pop_tile()
                            self.score += 1
                        
                        elif event.key in self.keys:
                            self.game_over()
                        break
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if len(self.tiles) >= 4 and self.tiles[0].rect.y == self.tiles[1].rect.y and self.tiles[0].rect.y == self.tiles[2].rect.y and self.tiles[0].rect.y == self.tiles[3].rect.y:
                        for i in range(4):
                            if self.mouse_col_check(*mouse_pos, self.tiles[i].rect):
                                self.pop_tile(i)
                                self.score += 1
                    
                    elif len(self.tiles) >= 3 and self.tiles[0].rect.y == self.tiles[1].rect.y and self.tiles[0].rect.y == self.tiles[2].rect.y:
                        for i in range(3):
                            if self.mouse_col_check(*mouse_pos, self.tiles[i].rect):
                                self.pop_tile(i)
                                self.score += 1
                    
                    elif len(self.tiles) >= 2 and self.tiles[0].rect.y == self.tiles[1].rect.y:
                        for i in range(2):
                            if self.mouse_col_check(*mouse_pos, self.tiles[i].rect):
                                self.pop_tile(i)
                                self.score += 1
                    
                    elif mouse_pos[0] > self.tiles[0].rect.left and mouse_pos[0] < self.tiles[0].rect.right and mouse_pos[1] > self.tiles[0].rect.top and mouse_pos[1] < self.tiles[0].rect.bottom:
                        self.pop_tile()
                        self.score += 1
                    else:
                        self.game_over()
                    break
                
                elif event.type == QUIT:
                    self.quit()
            
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            self.fill_bg(self.screen.surface)
            for l in range(1, LINES):
                pygame.draw.line(self.screen.surface, self._SETTINGS["colors"]["line_color"], (WIDTH//LINES*l, 0), (WIDTH//LINES*l, HEIGHT), 1)
            
            if self.clock.get_fps() != 0:
                self.dt = 1 / self.clock.get_fps() 
            
            self.timer += self.dt
            self.d_song_speed += self.dt * self._SETTINGS["speed_increase_rate"]
            self.tile_spawn_rate = 1/self.d_song_speed
            if self.timer >= self.tile_spawn_rate:
                self.generate_new_tile()
                if len(self.tiles):
                    self.current_note_key = self.tiles[0].related_key
                self.timer = 0
            
            for t in self.tiles:
                t.speed = self.d_song_speed*self._SETTINGS["tile_height"]*H_RATIO
                if t.rect.top >= HEIGHT:
                    self.pop_tile()
                    self.game_over()
                    break
                
                self.fill_surface(t.img, "tile_colors")
                self.screen.surface.blit(t.img, t.rect)
                t.rect.y += t.speed * self.dt
            
            
            self.render_ss()
            self.show_fps2()
                
            pygame.display.flip()
            self.clock.tick(self._REFRESH_RATE)


if __name__ == "__main__":
    app = App()
    app.run()
    app.quit()