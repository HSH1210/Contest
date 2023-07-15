import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, name, image, flipped, pos, speed, maxspeed, collisionmap):
        super(Player, self).__init__()
        self.name = name
        self.image = image
        self.flipped = flipped
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.maxspeed = maxspeed
        self.velocity = pygame.math.Vector2(0, 0)
        self.collisionmap = collisionmap

    def update(self, keyInput):
        
        if keyInput[pygame.K_a]:
            self.velocity.x -= self.speed
        if keyInput[pygame.K_d]:
            self.velocity.x += self.speed
        if keyInput[pygame.K_w]:
            self.velocity.y -= self.speed
        if keyInput[pygame.K_s]:
            self.velocity.y += self.speed

        self.velocity.x = max(-self.maxspeed, min(self.maxspeed, self.velocity.x))
        self.velocity.y = max(-self.maxspeed, min(self.maxspeed, self.velocity.y))

        if self.velocity.x < 0:
            self.velocity.x += self.speed / 2
        elif self.velocity.x > 0:
            self.velocity.x -= self.speed / 2
        if self.velocity.y < 0:
            self.velocity.y += self.speed / 2
        elif self.velocity.y > 0:
            self.velocity.y -= self.speed / 2
            
        
        new_left = pygame.Rect(self.rect.left + self.velocity.x, self.rect.top, 1, self.rect.height)
        new_right = pygame.Rect(self.rect.right + self.velocity.x, self.rect.top, 1, self.rect.height)
        new_top = pygame.Rect(self.rect.left, self.rect.top + self.velocity.y, self.rect.width, 1)
        new_bottom = pygame.Rect(self.rect.left, self.rect.bottom + self.velocity.y, self.rect.width, 1)
        
        for rect in self.collisionmap.rectlist:
            if new_left.colliderect(rect):
                self.velocity.x = 0
                self.rect.left = rect.right
            if new_right.colliderect(rect):
                self.velocity.x = 0
                self.rect.right = rect.left
            if new_top.colliderect(rect):
                self.velocity.y = 0
                self.rect.top = rect.bottom
            if new_bottom.colliderect(rect):
                self.velocity.y = 0
                self.rect.bottom = rect.top
                
                
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        
        
    def draw(self, surface):
        cursorx = pygame.mouse.get_pos()[0]
        if cursorx >= self.rect.centerx:
            surface.blit(self.image, self.rect)
        else:
            surface.blit(self.flipped, self.rect)