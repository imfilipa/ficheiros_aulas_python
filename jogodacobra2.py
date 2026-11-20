import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Cores (Paleta Retro / Python Theme)
BLACK = (15, 15, 20)
WHITE = (255, 255, 255)
DARK_GREEN = (34, 139, 34)
LIGHT_GREEN = (50, 205, 50)
EYE_COLOR = (255, 255, 255)
PUPIL_COLOR = (0, 0, 0)

# Cores do logotipo do Python para a comida
PYTHON_BLUE = (53, 114, 165)
PYTHON_YELLOW = (255, 211, 66)

# Configuração da grelha e janela
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Cobrinha - Python Edition")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)

def reset_game():
    global snake, direction, next_direction, food, score, game_over
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = "RIGHT"
    next_direction = "RIGHT"
    food = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
    score = 0
    game_over = False

reset_game()

# Loop principal do jogo
while True:
    # 1. Tratamento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_SPACE:
                    reset_game()
            else:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "DOWN":
                    next_direction = "UP"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "UP":
                    next_direction = "DOWN"
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "RIGHT":
                    next_direction = "LEFT"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != "LEFT":
                    next_direction = "RIGHT"

    if not game_over:
        direction = next_direction

        # 2. Movimento da cobrinha
        head = list(snake[0])
        if direction == "UP":
            head[1] -= BLOCK_SIZE
        elif direction == "DOWN":
            head[1] += BLOCK_SIZE
        elif direction == "LEFT":
            head[0] -= BLOCK_SIZE
        elif direction == "RIGHT":
            head[0] += BLOCK_SIZE

        # 3. Travessia de paredes (Teletransporte)
        if head[0] < 0:
            head[0] = WIDTH - BLOCK_SIZE
        elif head[0] >= WIDTH:
            head[0] = 0
        
        if head[1] < 0:
            head[1] = HEIGHT - BLOCK_SIZE
        elif head[1] >= HEIGHT:
            head[1] = 0

        # 4. Colisão com o próprio corpo (Game Over)
        if head in snake:
            game_over = True
        else:
            snake.insert(0, head)

            # 5. Comer a comida
            if head == food:
                score += 1
                food = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                        random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
            else:
                snake.pop()

    # 6. Desenhar elementos no ecrã
    screen.fill(BLACK)

    if not game_over:
        # Desenhar a comida (Símbolo Python estilizado)
        fx, fy = food[0], food[1]
        pygame.draw.rect(screen, PYTHON_BLUE, pygame.Rect(fx + 2, fy + 2, BLOCK_SIZE - 4, BLOCK_SIZE // 2 - 1), border_radius=3)
        pygame.draw.rect(screen, PYTHON_YELLOW, pygame.Rect(fx + 2, fy + BLOCK_SIZE // 2, BLOCK_SIZE - 4, BLOCK_SIZE // 2 - 1), border_radius=3)

        # Desenhar a cobrinha
        for index, block in enumerate(snake):
            bx, by = block[0], block[1]
            if index == 0:
                pygame.draw.rect(screen, LIGHT_GREEN, pygame.Rect(bx + 1, by + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2), border_radius=4)
                # Olhos
                if direction == "RIGHT":
                    pygame.draw.circle(screen, EYE_COLOR, (bx + 15, by + 6), 3)
                    pygame.draw.circle(screen, PUPIL_COLOR, (bx + 16, by + 6), 1)
                    pygame.draw.circle(screen, EYE_COLOR, (bx + 15, by + 14), 3)
                    pygame.draw.circle(screen, PUPIL_COLOR, (bx + 16, by + 14), 1)
                elif direction == "LEFT":
                    pygame.draw.circle(screen, EYE_COLOR, (bx + 5, by + 6), 3)
                    pygame.draw.circle(screen, PUPIL_COLOR, (bx + 4, by + 6), 1)
                    pygame.draw.circle(screen, EYE_COLOR, (bx + 5, by + 14), 3)
                    pygame.draw.circle(screen, PUPIL_COLOR, (bx + 4, by + 14), 1)
                elif direction == "UP":
                    pygame.draw.circle(screen, EYE_COLOR, (bx + 6, by + 5), 3)
                    pygame.draw.circle(screen, PUPIL_COLOR, (bx + 6, by + 4), 1)
                    pygame.draw.circle(screen, EYE_COLOR, (bx + 14, by + 5), 3)
                    pygame.draw.circle(screen, PUPIL_COLOR, (bx + 14, by + 4), 1)
                elif direction == "DOWN":
                    pygame.draw.circle(screen, EYE_COLOR, (bx + 6, by + 15), 3)
                    pygame.draw.circle(screen, PUPIL_COLOR, (bx + 6, by + 16), 1)
                    pygame.draw.circle(screen, EYE_COLOR, (bx + 14, by + 15), 3)
                    pygame.draw.circle(screen, PUPIL_COLOR, (bx + 14, by + 16), 1)
            else:
                pygame.draw.rect(screen, DARK_GREEN, pygame.Rect(bx + 2, by + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=3)

        # Mostrar pontuação durante o jogo
        score_text = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(score_text, (15, 15))
    else:
        # Ecrã de Game Over
        game_over_text = large_font.render("GAME OVER", True, (255, 80, 80))
        final_score_text = font.render(f"Pontuação Final: {score}", True, WHITE)
        restart_text = font.render("Pressiona ESPAÇO para Recomeçar", True, PYTHON_YELLOW)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT * 2 // 3))

    # Atualizar ecrã
    pygame.display.flip()
    clock.tick(10)
    