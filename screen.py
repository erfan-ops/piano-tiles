import pygame
from settings import *
    

class Screen():
    def __init__(self) -> None:
        super().__init__()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("piano tiles by erfan :D")
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))
        
        self.bg_colors = SETTINGS["colors"]["bg_colors"]
        self.rainbow_color_speed = SETTINGS["colors"]["rainbow_color_speed"]
        
        self.r, self.g, self.b = self.bg_colors[0][0], self.bg_colors[0][1], self.bg_colors[0][2]
        self.nextr, self.nextg, self.nextb = self.bg_colors[1][0], self.bg_colors[1][1], self.bg_colors[1][2]
        self.ri, self.gi, self.bi = self.nextr-self.r, self.nextg-self.g, self.nextb-self.b
        self.enum = 0
        self.len_colors = len(self.bg_colors)
        self.speed = 1
    
    
    def reset(self):
        enum2 = (self.enum+1) % self.len_colors
        self.r, self.g, self.b = self.bg_colors[self.enum]
        self.nextr, self.nextg, self.nextb = self.bg_colors[enum2]
        self.ri, self.gi, self.bi = self.nextr-self.r, self.nextg-self.g, self.nextb-self.b
        self.nextr = self.bg_colors[enum2][0]
    
    
    def fill(self, surface: pygame.Surface):
        surface.fill((self.r, self.g, self.b))
        
        self.r += self.ri*self.dt*self.rainbow_color_speed
        self.g += self.gi*self.dt*self.rainbow_color_speed
        self.b += self.bi*self.dt*self.rainbow_color_speed
        
        if self.r > 255:
            self.r = 255
        elif self.r < 0:
            self.r = 0
        
        if self.g > 255:
            self.g = 255
        elif self.g < 0:
            self.g = 0
        
        if self.b > 255:
            self.b = 255
        elif self.b < 0:
            self.b = 0
        
        if int(self.r) == self.nextr and int(self.g) == self.nextg and int(self.b) == self.nextb:
            self.enum = (self.enum+1) % self.len_colors
            self.reset()
    
    
    def fill_surface(self, surface: pygame.Surface, color_group="bg_colors"):
        colors = SETTINGS["colors"][color_group]
        l_colors_1 = len(SETTINGS["colors"][color_group]) - 1
        
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