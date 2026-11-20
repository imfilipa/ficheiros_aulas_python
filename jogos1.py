import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configuração da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Simples")

# Relógio para controlar os FPS
clock = pygame.time.Clock()

# Jogador (Raquete da Esquerda)
player = pygame.Rect(50, HEIGHT // 2 - 50, 15, 100)
player_speed = 7

# Computador / Oponente (Raquete da Direita)
opponent = pygame.Rect(WIDTH - 65, HEIGHT // 2 - 50, 15, 100)
opponent_speed = 6

# Bola
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
ball_speed_x = 5 * pygame.math.Vector2(1, 1).normalize().x
ball_speed_y = 5 * pygame.math.Vector2(1, 1).normalize().y

# Pontuação
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 74)

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1

# Loop principal do jogo
running = True
while running:
    # 1. Tratamento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 2. Movimento do Jogador (Teclas W e S ou Setas Cima e Baixo)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.y += player_speed

    # Limitar o jogador dentro do ecrã
    if player.top < 0:
        player.top = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT

    # Movimento automático simples do oponente
    if opponent.centery < ball.centery:
        opponent.y += opponent_speed
    if opponent.centery > ball.centery:
        opponent.y -= opponent_speed

    if opponent.top < 0:
        opponent.top = 0
    if opponent.bottom > HEIGHT:
        opponent.bottom = HEIGHT

    # 3. Movimento da bola
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Colisão com as paredes superior e inferior
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Pontuação (Saída lateral)
    if ball.left <= 0:
        opponent_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        player_score += 1
        reset_ball()

    # Colisão com as raquetes
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    # 4. Desenhar os elementos no ecrã
    screen.fill(BLACK)
    
    # Desenhar raquetes e bola
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)
    
    # Linha divisória central
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Mostrar pontuação
    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (WIDTH // 4, 20))
    
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(opponent_text, (WIDTH * 3 // 4, 20))

    # Atualizar o ecrã
    pygame.display.flip()
    clock.tick(60)