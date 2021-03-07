from objects import *


class Game:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("Invader using pygame")

        self.running = True
        self.game_state = START  # starting screen state

        # sprite group
        self.all_objects = pygame.sprite.RenderUpdates()
        self.e_bullets = pygame.sprite.Group()   # enemy bullets
        self.enemies, self.bullet = pygame.sprite.Group(), pygame.sprite.Group()

        # sprite group of each class
        Player.grouping = self.all_objects
        Enemy.grouping = self.all_objects, self.enemies
        Bullet.grouping = self.all_objects, self.bullet
        Beam.grouping = self.all_objects, self.e_bullets
        Explosion.grouping = self.all_objects

        # create player ship
        self.player = Player()

        # create 50 enemies
        for i in range(0, 50):
            x, y = 20 + (i % 10) * 40, 20 + (i // 10) * 40
            Enemy((x, y))

        # game main loop
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handling()

    def update(self):
        """update game state"""
        if self.game_state == PLAY:
            self.all_objects.update()
            # enemy and bullet collide
            self.check_collision()
            # if no enemy left, then games done
            if len(self.enemies.sprites()) == 0:
                self.game_state = GAME_OVER

    def draw(self, screen):
        """display on window"""
        # background wall paper
        screen.blit(load_image('background.png'), (0, 0))

        # this is for start screen
        if self.game_state == START:  # starting game
            title = pygame.font.SysFont("Times New Roman", 80).render(
                "INVADER GAME", False, (255, 100, 100))
            screen.blit(title,
                        ((SCR_RECT.width - title.get_width()) / 2, 100))
            # draw enemy
            enemy_image = split_image(load_image("enemy.png"), 2)[0]
            screen.blit(enemy_image,
                        ((SCR_RECT.width - enemy_image.get_width()) / 2, 200))
            # Start instruction
            push_space = pygame.font.SysFont("Times New Roman", 40).render(
                "PUSH SPACE KEY TO START", False, (255, 255, 255))
            screen.blit(push_space,
                        ((SCR_RECT.width - push_space.get_width()) / 2, 300))
            # Display my name
            credit = pygame.font.SysFont("Times New Roman", 40).render(
                'Created by Satoshi', False, (255, 255, 255))
            screen.blit(credit,
                        ((SCR_RECT.width - credit.get_width()) / 2, 380))

        # playing screen
        elif self.game_state == PLAY:
            self.all_objects.draw(screen)

        # game over screen
        elif self.game_state == GAME_OVER:
            # print GAME OVER
            game_over = pygame.font.SysFont("Times New Roman", 80).render(
                "GAME OVER", False, (255, 100, 100))
            screen.blit(game_over,
                        ((SCR_RECT.width - game_over.get_width()) / 2, 100))
            # draw enemy
            enemy_image = split_image(load_image("enemy.png"), 2)[0]
            screen.blit(enemy_image,
                        ((SCR_RECT.width - enemy_image.get_width()) / 2, 200))
            # Game over, push space button
            push_space = pygame.font.SysFont("Times New Roman", 40).render(
                "PUSH SPACE KEY TO START", False, (255, 255, 255))
            screen.blit(push_space,
                        ((SCR_RECT.width - push_space.get_width()) / 2, 300))

    def key_handling(self):
        """handle key inputs and make an action"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if self.game_state == START:  # start game
                    self.game_state = PLAY
                elif self.game_state == GAME_OVER:  # game over to start
                    self.__init__()  # start game again
                    self.game_state = PLAY

    def check_collision(self):
        """check collision"""
        collision = pygame.sprite.groupcollide(self.enemies, self.bullet,
                                               True, True)
        for enemy in collision.keys():
            # player's bullet and enemy collide
            load_sound("kill.wav").play()
            Explosion(enemy.rect.center)

        if pygame.sprite.spritecollide(self.player, self.e_bullets, True):
            # if player and enemy's bullet collide
            load_sound("bomb.wav").play()
            self.game_state = GAME_OVER


if __name__ == "__main__":
    Game()
