import sys
import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da Janela
LARGURA, ALTURA = 600, 700  # 600x600 para o tabuleiro + 100px para o painel inferior
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Velha Moderno - Python & Pygame")

# Paleta de Cores Moderna (Dark Theme)
COR_FUNDO = (18, 18, 24)          # Azul escuro/quase preto muito elegante
COR_LINHAS = (45, 55, 72)         # Cinza azulado suave
COR_PAINEL = (26, 32, 44)         # Fundo da barra inferior
COR_X = (245, 101, 101)           # Vermelho coral moderno
COR_O = (72, 187, 120)            # Verde menta moderno
COR_HOVER = (35, 43, 56)          # Cor ao passar o mouse nas casas vazias
COR_TEXTO = (237, 242, 247)       # Branco suave para textos

# Fontes
FONTE_STATUS = pygame.font.SysFont("Segoe UI", 28, bold=True)
FONTE_FIM = pygame.font.SysFont("Segoe UI", 24, bold=True)

# Estado inicial do tabuleiro (3x3)
tabuleiro = [["", "", ""], 
             ["", "", ""], 
             ["", "", ""]]
jogador_atual = "X"
jogo_acabou = False
vencedor = None

def desenhar_tabuleiro(mouse_pos):
    TELA.fill(COR_FUNDO)
    
    # Desenha o efeito de Hover (mouse em cima da casa) se o jogo estiver rolando
    if not jogo_acabou:
        x, y = mouse_pos
        if y < 600:  # Apenas na área do tabuleiro
            coluna = x // 200
            linha = y // 200
            if tabuleiro[linha][coluna] == "":
                # Desenha um retângulo suave na casa onde o mouse está
                pygame.draw.rect(TELA, COR_HOVER, (coluna * 200 + 10, linha * 200 + 10, 180, 180), border_radius=15)

    # Linhas do Tabuleiro (com bordas arredondadas estéticas)
    espessura = 8
    # Verticais
    pygame.draw.line(TELA, COR_LINHAS, (200, 20), (200, 580), espessura)
    pygame.draw.line(TELA, COR_LINHAS, (400, 20), (400, 580), espessura)
    # Horizontais
    pygame.draw.line(TELA, COR_LINHAS, (20, 200), (580, 200), espessura)
    pygame.draw.line(TELA, COR_LINHAS, (20, 400), (580, 400), espessura)

def desenhar_pecas():
    for linha in range(3):
        for coluna in range(3):
            # Centro da célula
            centro_x = coluna * 200 + 100
            centro_y = linha * 200 + 100
            
            if tabuleiro[linha][coluna] == "X":
                # Desenha um X moderno usando linhas grossas cruzadas
                offset = 50
                pygame.draw.line(TELA, COR_X, (centro_x - offset, centro_y - offset), (centro_x + offset, centro_y + offset), 12)
                pygame.draw.line(TELA, COR_X, (centro_x + offset, centro_y - offset), (centro_x - offset, centro_y + offset), 12)
                
            elif tabuleiro[linha][coluna] == "O":
                # Desenha um Círculo (O) moderno vazado no centro
                pygame.draw.circle(TELA, COR_O, (centro_x, centro_y), 50, 12)

def desenhar_painel():
    # Painel inferior
    pygame.draw.rect(TELA, COR_PAINEL, (0, 600, 600, 100))
    pygame.draw.line(TELA, COR_LINHAS, (0, 600), (600, 600), 4)
    
    if not jogo_acabou:
        # Texto indicando de quem é a vez
        texto_vez = f"Vez do Jogador: {jogador_atual}"
        texto_renderizado = FONTE_STATUS.render(texto_vez, True, COR_X if jogador_atual == "X" else COR_O)
        ret_texto = texto_renderizado.get_rect(center=(300, 650))
        TELA.blit(texto_renderizado, ret_texto)
    else:
        # Mensagem de fim de jogo
        if vencedor == "Empate":
            msg = "Deu Velha! Pressione [ESPAÇO] para reiniciar"
        else:
            msg = f"Jogador {vencedor} Venceu! Pressione [ESPAÇO] para reiniciar"
            
        texto_renderizado = FONTE_FIM.render(msg, True, COR_TEXTO)
        ret_texto = texto_renderizado.get_rect(center=(300, 650))
        TELA.blit(texto_renderizado, ret_texto)

def verificar_vencedor():
    global tabuleiro
    # Linhas e Colunas
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] != "":
            return tabuleiro[i][0]
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] != "":
            return tabuleiro[0][i]
            
    # Diagonais
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != "":
        return tabuleiro[0][0]
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != "":
        return tabuleiro[0][2]
        
    # Empate
    if all(celula != "" for linha in tabuleiro for celula in linha):
        return "Empate"
        
    return None

def reiniciar_jogo():
    global tabuleiro, jogador_atual, jogo_acabou, vencedor
    tabuleiro = [["", "", ""], ["", "", ""], ["", "", ""]]
    jogador_atual = "X"
    jogo_acabou = False
    vencedor = None

# Loop Principal do Jogo
while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN and not jogo_acabou:
            x, y = evento.pos
            # Garante que o clique foi apenas na área do tabuleiro (acima de y=600)
            if y < 600:
                coluna = x // 200
                linha = y // 200
                
                if tabuleiro[linha][coluna] == "":
                    tabuleiro[linha][coluna] = jogador_atual
                    
                    vencedor = verificar_vencedor()
                    if vencedor:
                        jogo_acabou = True
                    else:
                        jogador_atual = "O" if jogador_atual == "X" else "X"
                        
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            if jogo_acabou:
                reiniciar_jogo()

    # Renderização Gráfica Completa
    desenhar_tabuleiro(mouse_pos)
    desenhar_pecas()
    desenhar_painel()

    pygame.display.update()