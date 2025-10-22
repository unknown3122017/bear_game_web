import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐻 Bear and Balloon 🎈")

# Load images (web-friendly paths)
background_img = pygame.image.load("assets/background.png").convert()
bear_img = pygame.image.load("assets/bear.png").convert_alpha()
balloon_img = pygame.image.load("assets/balloon.png").convert_alpha()
enemy_img = pygame.image.load("assets/enemy.png").convert_alpha()  # replaced .gif with .png
arrow_img = pygame.image.load("assets/arrow.png").convert_alpha()
heart_img = pygame.image.load("assets/heart.png").convert_alpha()

# Resize images
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bear_img = pygame.transform.scale(bear_img, (140, 140))
balloon_img = pygame.transform.scale(balloon_img, (70, 100))
enemy_img = pygame.transform.scale(enemy_img, (80, 80))
arrow_img = pygame.transform.scale(arrow_img, (30, 50))
heart_img = pygame.transform.scale(heart_img, (40, 40))

# Fonts
font = pygame.font.SysFont("Arial", 30)
large_font = pygame.font.SysFont("Arial", 72)

# Draw centered text
def draw_center_text(text, font, color, y):
    label = font.render(text, True, color)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, y))

# Game Over screen
def game_over_screen(score):
    screen.fill((15, 15, 25))
    draw_center_text("GAME OVER 💀", large_font, (255, 255, 255), HEIGHT // 2 - 120)
    draw_center_text(f"Your Score: {score}", font, (200, 200, 200), HEIGHT // 2 - 40)
    draw_center_text("Press ENTER to restart or ESC to quit", font, (255, 255, 0), HEIGHT // 2 + 40)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Start screen
def show_start_screen():
    screen.blit(background_img, (0, 0))
    draw_center_text("🐻 Bear and Balloon 🎈", large_font, (255, 255, 255), HEIGHT // 2 - 100)
    draw_center_text("← → to move | SPACE to shoot", font, (255, 255, 255), HEIGHT // 2)
    draw_center_text("Press ENTER to start", font, (255, 255, 0), HEIGHT // 2 + 60)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# Main game function
def play_game():
    bear_x, bear_y = WIDTH // 2 - 60, HEIGHT - 160
    enemy_list = []
    arrows = []
    enemy_speed = 3
    arrow_speed = 10
    score = 0
    level = 1
    lives = 3  # ❤️ Hearts

    ENEMY_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, 1200)

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == ENEMY_SPAWN_EVENT:
                x = random.choice([-80, WIDTH + 80])
                y = random.randint(100, HEIGHT - 250)
                direction = 1 if x < 0 else -1
                enemy_list.append([x, y, direction])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    arrow_x = bear_x + bear_img.get_width() // 2 - arrow_img.get_width() // 2
                    arrow_y = bear_y + 10
                    arrows.append([arrow_x, arrow_y])

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bear_x > 0:
            bear_x -= 6
        if keys[pygame.K_RIGHT] and bear_x < WIDTH - bear_img.get_width():
            bear_x += 6

        # Balloon position
        balloon_x = bear_x + (bear_img.get_width() // 2 - balloon_img.get_width() // 2)
        balloon_y = bear_y - balloon_img.get_height() + 10

        # More accurate collision area
        balloon_rect = pygame.Rect(balloon_x + 10, balloon_y + 10, balloon_img.get_width() - 20, balloon_img.get_height() - 20)

        # Move enemies and check collisions
        for enemy in enemy_list[:]:
            enemy[0] += enemy_speed * enemy[2]
            enemy_rect = pygame.Rect(enemy[0] + 20, enemy[1] + 20, enemy_img.get_width() - 40, enemy_img.get_height() - 40)

            if enemy_rect.colliderect(balloon_rect):
                enemy_list.remove(enemy)
                lives -= 1
                if lives <= 0:
                    running = False

            if enemy[0] < -120 or enemy[0] > WIDTH + 120:
                enemy_list.remove(enemy)
                score += 5

        # Move arrows
        for arrow in arrows[:]:
            arrow[1] -= arrow_speed
            arrow_rect = pygame.Rect(arrow[0], arrow[1], arrow_img.get_width(), arrow_img.get_height())

            for enemy in enemy_list[:]:
                enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_img.get_width(), enemy_img.get_height())
                if arrow_rect.colliderect(enemy_rect):
                    enemy_list.remove(enemy)
                    arrows.remove(arrow)
                    score += 15
                    break

            if arrow[1] < 0:
                arrows.remove(arrow)

        # Level up every 100 points
        if score >= level * 100:
            level += 1
            enemy_speed += 0.5

        # Draw everything
        screen.blit(background_img, (0, 0))
        screen.blit(bear_img, (bear_x, bear_y))
        screen.blit(balloon_img, (balloon_x, balloon_y))
        for enemy in enemy_list:
            screen.blit(enemy_img, (enemy[0], enemy[1]))
        for arrow in arrows:
            screen.blit(arrow_img, (arrow[0], arrow[1]))

        # Score and level
        text = font.render(f"Score: {score}   Level: {level}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # Draw hearts
        for i in range(lives):
            screen.blit(heart_img, (WIDTH - (i + 1) * 50 - 10, 10))

        pygame.display.flip()

    game_over_screen(score)


# Run the game
show_start_screen()
while True:
    play_game()
