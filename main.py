import pygame

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800
SCREEN_TITLE = "Cross The Road !"

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

CLOCK = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('comicsans', 100)


class Game:
    TICK_RATE = 60

    def __init__(self, image_path, title: str, width, height):
        self.title = title
        self.width = width
        self.height = height

        self.game_screen = pygame.display.set_mode((self.width, self.height))
        self.game_screen.fill(COLOR_WHITE)
        pygame.display.set_caption(SCREEN_TITLE)

        background_image = pygame.image.load(image_path)
        self.background = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level):
        is_game_over = False
        is_win = False
        direction = 0

        player_character = PlayerCharacter('resources/character.png', 375, 700, 42, 57)
        monster_character_1 = MonsterCharacter('resources/monster.png', 50, 600, 50, 50)
        monster_character_1.SPEED *= level
        monster_character_2 = MonsterCharacter('resources/monster.png', 50, 450, 50, 50)
        monster_character_2.SPEED *= level
        monster_character_3 = MonsterCharacter('resources/monster.png', 50, 200, 50, 50)
        monster_character_3.SPEED *= level

        treasure_character = GameObject('resources/chess.png', 375, 50, 50, 50)

        while not is_game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

            self.game_screen.fill(COLOR_WHITE)
            self.game_screen.blit(self.background, (0, 0))

            treasure_character.draw(self.game_screen)

            player_character.move(direction, self.height)
            player_character.draw(self.game_screen)

            monster_character_1.move(self.width)
            monster_character_1.draw(self.game_screen)

            if level > 1.5:
                monster_character_2.move(self.width)
                monster_character_2.draw(self.game_screen)

            if level > 3:
                monster_character_3.move(self.width)
                monster_character_3.draw(self.game_screen)

            if player_character.detect_collision(monster_character_1):
                is_game_over = True
                is_win = False
                text = FONT.render('Sorry, you failed !', True, COLOR_BLACK)
                self.game_screen.blit(text, (125, 350))
                pygame.display.update()
                CLOCK.tick(1)
                break

            elif player_character.detect_collision(treasure_character):
                is_game_over = True
                is_win = True
                text = FONT.render('Yes, you did it !', True, COLOR_BLACK)
                self.game_screen.blit(text, (125, 350))
                pygame.display.update()
                CLOCK.tick(1)
                break

            elif level > 4.5:
                is_game_over = True
                text = FONT.render('Congratulation !', True, COLOR_BLACK)
                self.game_screen.blit(text, (125, 350))
                pygame.display.update()
                CLOCK.tick(1)
                return


            pygame.display.update()
            CLOCK.tick(self.TICK_RATE)

        if is_win:
            self.run_game_loop(level + 0.5)
        else:
            return


class GameObject:
    def __init__(self, image_path: str, x, y, w, h):
        self.object = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.object, (w, h))

        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, background):
        background.blit(self.image, (self.x, self.y))


class PlayerCharacter(GameObject):
    SPEED = 5

    def __init__(self, image_path: str, x, y, w, h):
        super().__init__(image_path, x, y, w, h)

    def move(self, direction, h):
        if direction > 0:
            self.y -= self.SPEED
        elif direction < 0:
            self.y += self.SPEED

        if self.y >= h - 50:
            self.y = h - 50

    def detect_collision(self, other_body):
        if self.y > other_body.y + other_body.h:
            return False
        elif self.y + self.h < other_body.y:
            return False
        if self.x > other_body.x + other_body.w:
            return False
        elif self.x + self.w < other_body.x:
            return False
        return True


class MonsterCharacter(GameObject):
    SPEED = 3

    def __init__(self, image_path: str, x, y, w, h):
        super().__init__(image_path, x, y, w, h)

    def move(self, w):
        if self.x <= 50:
            self.SPEED = abs(self.SPEED)
        elif self.x >= w - 100:
            self.SPEED = -abs(self.SPEED)
        self.x += self.SPEED


def main():
    pygame.init()

    new_game = Game('resources/background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
    new_game.run_game_loop(1)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
