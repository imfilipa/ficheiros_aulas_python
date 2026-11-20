import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Definir cores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Configuração da grelha e janela
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Cobrinha - Passagem nas Paredes")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def reset_game():
    global snake, direction, next_direction, food, score
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = "RIGHT"
    next_direction = "RIGHT"
    food = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
    score = 0

reset_game()

# Loop principal do jogo
running = True
while running:
    # 1. Tratamento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "DOWN":
                next_direction = "UP"
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "UP":
                next_direction = "DOWN"
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "RIGHT":
                next_direction = "LEFT"
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != "LEFT":
                next_direction = "RIGHT"

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

    # 3. Travessia de paredes (Teletransporte para o lado oposto)
    if head[0] < 0:
        head[0] = WIDTH - BLOCK_SIZE
    elif head[0] >= WIDTH:
        head[0] = 0
    
    if head[1] < 0:
        head[1] = HEIGHT - BLOCK_SIZE
    elif head[1] >= HEIGHT:
        head[1] = 0

    # 4. Condição de derrota (Apenas se bater no próprio corpo)
    if head in snake:
        reset_game()
        continue

    snake.insert(0, head)

    # 5. Comer a comida
    if head == food:
        score += 1
        food = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
    else:
        snake.pop() # Remove a cauda se não comer

    # 6. Desenhar elementos no ecrã
    screen.fill(BLACK)

    # Desenhar a comida
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

    # Desenhar a cobrinha
    for block in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

    # Mostrar pontuação
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Atualizar ecrã (Velocidade do jogo regulada para 10 FPS)
    pygame.display.flip()
    clock.tick(10)