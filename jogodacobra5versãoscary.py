import pygame
import random
import sys
import time

# Inicialização do Pygame
pygame.init()

# Cores gerais e do fundo de computador
DARK_GRAY = (35, 35, 42)      # Fundo cinzento do monitor
GRID_GRAY = (48, 48, 58)      # Linhas da grelha do computador
WHITE = (255, 255, 255)
EYE_COLOR = (255, 255, 255)
PUPIL_COLOR = (0, 0, 0)

# Definição das 5 opções de cobras (Cabeça e Corpo)
SNAKE_OPTIONS = [
    {"name": "Verde", "head": (50, 205, 50), "body": (34, 139, 34)},
    {"name": "Azul", "head": (0, 191, 255), "body": (0, 102, 204)},
    {"name": "Vermelho", "head": (255, 69, 0), "body": (178, 34, 34)},
    {"name": "Roxo", "head": (186, 85, 211), "body": (128, 0, 128)},
    {"name": "Amarelo", "head": (255, 215, 0), "body": (218, 165, 32)}
]

# Configuração da grelha e janela
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Cobra")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

# Tentar carregar a imagem assustadora (substitui 'assustadora.png' pelo nome do teu ficheiro de imagem)
scary_image = None
try:
    loaded_img = pygame.image.load("assustadora.png")
    scary_image = pygame.transform.scale(loaded_img, (WIDTH, HEIGHT))
except Exception:
    pass  # Se não encontrar a imagem, o jogo continua sem ela para não dar erro

# Estados do jogo: 'SELECT_SNAKE', 'PLAYING', 'GAME_OVER'
game_state = "SELECT_SNAKE"
selected_snake_idx = 0

# Variáveis para o susto aos 3 pontos
scary_active = False
scary_timer = 0
scary_triggered_at_3 = False  # Garante que só acontece uma vez por jogo

def reset_game():
    global snake, direction, next_direction, food, score, scary_triggered_at_3
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = "RIGHT"
    next_direction = "RIGHT"
    food = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
    score = 0
    scary_triggered_at_3 = False

def draw_computer_background():
    """Desenha o fundo em cinzento com linhas de grelha estilo computador"""
    screen.fill(DARK_GRAY)
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_GRAY, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_GRAY, (0, y), (WIDTH, y), 1)

# Loop principal do jogo
while True:
    # 1. Tratamento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            if game_state == "SELECT_SNAKE":
                if event.key == pygame.K_1:
                    selected_snake_idx = 0
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_2:
                    selected_snake_idx = 1
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_3:
                    selected_snake_idx = 2
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_4:
                    selected_snake_idx = 3
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_5:
                    selected_snake_idx = 4
                    reset_game()
                    game_state = "PLAYING"
                    
            elif game_state == "PLAYING" and not scary_active:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "DOWN":
                    next_direction = "UP"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "UP":
                    next_direction = "DOWN"
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "RIGHT":
                    next_direction = "LEFT"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != "LEFT":
                    next_direction = "RIGHT"
                    
            elif game_state == "GAME_OVER":
                if event.key == pygame.K_SPACE:
                    game_state = "SELECT_SNAKE"

    if game_state == "PLAYING":
        # Se o susto estiver ativo, decrementa o temporizador e congela o jogo por 3 segundos (30 frames a 10 FPS)
        if scary_active:
            scary_timer -= 1
            if scary_timer <= 0:
                scary_active = False
        else:
            direction = next_direction

            # Movimento da cobrinha
            head = list(snake[0])
            if direction == "UP":
                head[1] -= BLOCK_SIZE
            elif direction == "DOWN":
                head[1] += BLOCK_SIZE
            elif direction == "LEFT":
                head[0] -= BLOCK_SIZE
            elif direction == "RIGHT":
                head[0] += BLOCK_SIZE

            # Travessia de paredes (Teletransporte)
            if head[0] < 0:
                head[0] = WIDTH - BLOCK_SIZE
            elif head[0] >= WIDTH:
                head[0] = 0
            
            if head[1] < 0:
                head[1] = HEIGHT - BLOCK_SIZE
            elif head[1] >= HEIGHT:
                head[1] = 0

            # Colisão com o próprio corpo (Game Over)
            if head in snake:
                game_state = "GAME_OVER"
            else:
                snake.insert(0, head)

                # Comer a comida
                if head == food:
                    score += 1
                    # Ativar o susto se for a primeira vez que atinge os 3 pontos
                    if score == 3 and not scary_triggered_at_3:
                        scary_active = True
                        scary_timer = 30  # 30 frames = 3 segundos (a 10 FPS)
                        scary_triggered_at_3 = True

                    food = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
                else:
                    snake.pop()

    # 2. Desenhar elementos no ecrã
    draw_computer_background()

    if game_state == "SELECT_SNAKE":
        title_text = large_font.render("ESCOLHE A TUA COBRA", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 40))

        for idx, s_info in enumerate(SNAKE_OPTIONS):
            y_pos = 110 + (idx * 50)
            pygame.draw.rect(screen, s_info["head"], pygame.Rect(120, y_pos + 5, 20, 20), border_radius=4)
            option_text = font.render(f"[{idx + 1}] {s_info['name']}", True, WHITE)
            screen.blit(option_text, (160, y_pos))

        instruction_text = small_font.render("Pressiona a tecla de 1 a 5 para começar", True, (200, 200, 200))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 350))

    elif game_state == "PLAYING":
        # Desenhar a comida (Bola branca simples)
        fx, fy = food[0], food[1]
        pygame.draw.circle(screen, WHITE, (fx + BLOCK_SIZE // 2, fy + BLOCK_SIZE // 2), BLOCK_SIZE // 2 - 3)

        # Obter as cores da cobra escolhida com segurança
        active_skin = SNAKE_OPTIONS[selected_snake_idx]
        head_color = active_skin["head"]
        body_color = active_skin["body"]

        # Desenhar a cobrinha detalhada
        for index, block in enumerate(snake):
            bx, by = block[0], block[1]
            if index == 0:
                pygame.draw.rect(screen, head_color, pygame.Rect(bx + 1, by + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2), border_radius=4)
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
                pygame.draw.rect(screen, body_color, pygame.Rect(bx + 2, by + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=3)

        # Mostrar pontuação
        score_text = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(score_text, (15, 15))

        # Se o susto estiver ativo, desenha a imagem por cima do ecrã
        if scary_active:
            if scary_image:
                screen.blit(scary_image, (0, 0))
            else:
                # Fallback caso não encontrem a imagem: Mostra um aviso gigante a vermelho
                warning_text = large_font.render("BOO!", True, (255, 0, 0))
                screen.blit(warning_text, (WIDTH // 2 - warning_text.get_width() // 2, HEIGHT // 2 - warning_text.get_height() // 2))

    elif game_state == "GAME_OVER":
        game_over_text = large_font.render("GAME OVER", True, (255, 80, 80))
        final_score_text = font.render(f"Pontuação Final: {score}", True, WHITE)
        restart_text = font.render("Pressiona ESPAÇO para Voltar ao Menu", True, WHITE)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT * 2 // 3))

    # Atualizar ecrã
    pygame.display.flip()
    clock.tick(10)