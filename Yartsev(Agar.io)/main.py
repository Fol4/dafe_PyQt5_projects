from background import *
from player import *
from yummy import *
from enemy import *
from map import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("agar.io")
clock = pygame.time.Clock()

player = Player()
background = Background()
map = Map()

enemies = []
for i in range(EnemyQuantity):
    enemy = Enemy(background)
    enemies.append(enemy)

food = []
for i in range(FoodQuantity):
    yummy = Yummy(background)
    food.append(yummy)

is_running = True
while is_running:
    clock.tick(FPS)

    screen.fill(WHITE)

    background.update(player)
    background.draw(screen)

    for dot in food:
        dot.update(background, player, enemies)
        dot.draw(screen, background)

    player.draw(screen)
    is_running = player.checking_for_death(enemies, background)

    for enemy in enemies:
        enemy.update(enemies, food, player, background)
        enemy.checking_for_death(enemies, background, player)
        enemy.draw(screen, background)

    map.draw(screen, background, player, enemies, food)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    pygame.display.flip()

pygame.quit()