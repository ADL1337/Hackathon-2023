import pygame

from game_data import GRAVITY
from projectile import PlayerProjectile


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale_by(pygame.image.load("img/player/idle/player_idle_0.png").convert_alpha(), 0.5)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 20
        self.is_alive = True
        self.dx = 0
        self.dy = 0

        self.gravity = GRAVITY
        self.facing = "right"
        self.last_shot = pygame.time.get_ticks()
        self.shot_timer = 500
        self.image_ratio = 0.5
        self.animation_index = 0
        self.current_animation = "idle"

        self.animations = {"idle": self.create_image_list("img/player/idle/player_idle_", 2),
                           "run": self.create_image_list("img/player/run/player_run_", 11),
                           "shoot": self.create_image_list("img/player/shoot/player_shoot_", 16), }

    def run(self, direction=None):
        self.current_animation = "run"
        if direction == "left":
            self.facing = "left"
            self.dx = -self.speed
        elif direction == "right":
            self.facing = "right"
            self.dx = self.speed
        self.image = self.animations["idle"][self.facing][0]

    def shoot(self):
        self.current_animation = "shoot"
        if pygame.time.get_ticks() - self.last_shot >= self.shot_timer:
            self.last_shot = pygame.time.get_ticks()
        return PlayerProjectile(getattr(self.rect, f"mid{self.facing}"), 1 if self.facing == "right" else -1)

    def jump(self):
        self.dy = -20

    def _collision(self, obstacles):
        collision_list = pygame.sprite.spritecollide(self, obstacles, False)
        if collision_list:
            for entity in collision_list:
                if self.dy > 0 and self.rect.bottom > entity.rect.top:
                    self.rect.bottom = entity.rect.top
                    self.dy = 0
                elif self.dy < 0 and self.rect.top < entity.rect.bottom:
                    self.rect.top = entity.rect.bottom
                    self.dy = 0
                elif self.dx > 0 and self.rect.right > entity.rect.left:
                    self.rect.right = entity.rect.left
                elif self.dx < 0 and self.rect.left < entity.rect.right:
                    self.rect.left = entity.rect.right

    def _move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def _apply_gravity(self):
        self.dy += self.gravity

    def die(self):
        self.is_alive = False

    def update(self, obstacles):
        self._move()
        self._apply_gravity()
        self.run()
        self._animate()
        self._collision(obstacles)

    def _animate(self):
        self.image = self.animations[self.current_animation][self.facing][self.animation_index]
        self.animation_index += 1
        self.animation_index %= len(self.animations[self.current_animation][self.facing])

    def create_image_list(self, path, count):
        res = {}
        res["right"] = [pygame.transform.scale_by(img, self.image_ratio) for img in
                        [pygame.image.load(f"{path}{i}.png").convert_alpha() for i in range(count)]]
        res["left"] = [pygame.transform.flip(img, True, False) for img in res["right"]]
        return res