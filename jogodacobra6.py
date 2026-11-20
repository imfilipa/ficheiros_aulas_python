import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Cores gerais e do fundo de computador
DARK_GRAY = (35, 35, 42)      # Fundo cinzento do monitor
GRID_GRAY = (48, 48, 58)      # Linhas da grelha do computador
WHITE = (255, 255, 255)
EYE_COLOR = (255, 255, 255)
PUPIL_COLOR = (0, 0, 0)
MESSAGE_BG = (20, 20, 25, 200) # Fundo semi-transparente para o pop-up
GOLD = (255, 215, 0)

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

# Bancos de mensagens aleatórias por marcos de pontuação
MESSAGES_5 = [
    "Boa! Já aqueceste as escamas!",
    "5 pontos! O pequeno réptil cresce!",
    "Continua assim, estás a ir bem!"
]

MESSAGES_10 = [
    "10 pontos! Respeito pela cobra!",
    "Já pareces uma jibóia profissional!",
    "Cuidado para não dares um nó!"
]

MESSAGES_20 = [
    "20 pontos! És um mestre da cobrinha!",
    "Impressionante! Alguém que pare este animal!",
    "Velocidade e reflexos de aço!"
]

MESSAGES_30 = [
    "30 PONTOS?! És uma lenda viva do Arcade!",
    "Nível Divino atingido com sucesso!",
    "O criador do jogo estaria orgulhoso!"
]

# Estados do jogo: 'SELECT_SNAKE', 'PLAYING', 'GAME_OVER'
game_state = "SELECT_SNAKE"
selected_snake_idx = 0

# Variáveis para controlar os pop-ups de mensagem temporários
active_message = ""
message_timer = 0

def reset_game():
    global snake, direction, next_direction, food, score, active_message, message_timer
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = "RIGHT"
    next_direction = "RIGHT"
    food = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
    score = 0
    active_message = ""
    message_timer = 0

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
                    
            elif game_state == "PLAYING":
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
        # Reduzir o temporizador da mensagem a cada frame se estiver ativa
        if message_timer > 0:
            message_timer -= 1
            if message_timer == 0:
                active_message = ""

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
                
                # Gatilhos de mensagens por pontuação (5, 10, 20, 30)
                if score == 5:
                    active_message = random.choice(MESSAGES_5)
                    message_timer = 20  # Fica visível durante 20 frames (~2 segundos a 10 FPS)
                elif score == 10:
                    active_message = random.choice(MESSAGES_10)
                    message_timer = 20
                elif score == 20:
                    active_message = random.choice(MESSAGES_20)
                    message_timer = 20
                elif score == 30:
                    active_message = random.choice(MESSAGES_30)
                    message_timer = 20

                food = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                        random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
            else:
                snake.pop()

    # 2. Desenhar elementos no ecrã (Com o fundo cinzento de computador)
    draw_computer_background()

    if game_state == "SELECT_SNAKE":
        # Ecrã de Seleção de Cobras
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

        # Se houver uma mensagem ativa, desenhar o pop-up no centro do ecrã
        if active_message:
            msg_render = font.render(active_message, True, GOLD)
            # Criar uma caixa de fundo para destacar a mensagem
            box_width = msg_render.get_width() + 40
            box_height = 50
            box_x = WIDTH // 2 - box_width // 2
            box_y = HEIGHT // 2 - box_height // 2 - 50
            
            # Desenhar retângulo de fundo e contorno
            pygame.draw.rect(screen, DARK_GRAY, (box_x, box_y, box_width, box_height), border_radius=8)
            pygame.draw.rect(screen, GOLD, (box_x, box_y, box_width, box_height), 2, border_radius=8)
            
            # Desenhar o texto lá dentro
            screen.blit(msg_render, (box_x + 20, box_y + 12))

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