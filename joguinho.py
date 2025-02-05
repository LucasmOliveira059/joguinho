import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo dos Quadrados")


# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Configurações dos quadrados
INITIAL_SIZE = 70  # Tamanho inicial dos quadrados
MIN_SIZE = 30      # Tamanho mínimo dos quadrados
INITIAL_SPEED = 5  # Velocidade inicial dos quadrados
MAX_SPEED = 10     # Velocidade máxima dos quadrados

# Fonte para o texto
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Classe para os quadrados
class Square:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.size = INITIAL_SIZE
        self.spikes = False
        self.health = 10
        self.speed = INITIAL_SPEED

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        if self.spikes:
            pygame.draw.circle(screen, WHITE, (self.x + self.size // 2, self.y + self.size // 2), self.size // 4)

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Verifica colisão com as paredes
        new_x = max(0, min(new_x, WIDTH - self.size))
        new_y = max(0, min(new_y, HEIGHT - self.size))

        # Atualiza a posição
        self.x = new_x
        self.y = new_y

    def update_size_and_speed(self):
        # Reduz o tamanho e aumenta a velocidade com base na vida perdida
        self.size = INITIAL_SIZE - (10 - self.health) * 4
        self.size = max(self.size, MIN_SIZE)
        self.speed = INITIAL_SPEED + (10 - self.health)
        self.speed = min(self.speed, MAX_SPEED)

# Função para gerar pontos brancos
def create_point():
    return pygame.Rect(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 10), 10, 10)

# Função para gerar pontos verdes
def create_green_point():
    return pygame.Rect(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 10), 10, 10)

# Função para desenhar o cabeçalho com a vida dos quadrados
def draw_header(square1, square2):
    header = pygame.Rect(0, 0, WIDTH, 50)
    pygame.draw.rect(screen, GRAY, header)
    life_text1 = font.render(f"Vida Vermelho: {square1.health}", True, RED)
    life_text2 = font.render(f"Vida Azul: {square2.health}", True, BLUE)
    screen.blit(life_text1, (10, 10))
    screen.blit(life_text2, (WIDTH - 200, 10))

# Função para exibir a tela de vitória
def show_winner(winner):
    screen.fill(BLACK)
    winner_text = large_font.render(f"Vencedor: {winner}", True, RED if winner == "Vermelho" else BLUE)
    instruction_text = font.render("Pressione R para reiniciar ou Q para sair", True, WHITE)
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

# Função para reiniciar o jogo
def reset_game():
    global square1, square2, points, green_points, last_point_time, last_green_point_time
    square1 = Square(RED, 100, 100)
    square2 = Square(BLUE, 400, 400)
    points = []
    green_points = []
    last_point_time = pygame.time.get_ticks()
    last_green_point_time = pygame.time.get_ticks()

# Loop principal do jogo
def main():
    global square1, square2, points, green_points, last_point_time, last_green_point_time

    reset_game()
    clock = pygame.time.Clock()
    running = True
    game_over = False
    winner = ""

    while running:
        if not game_over:
            screen.fill(BLACK)

            # Verifica eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Movimentação dos quadrados
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                square1.move(0, -1)
            if keys[pygame.K_s]:
                square1.move(0, 1)
            if keys[pygame.K_a]:
                square1.move(-1, 0)
            if keys[pygame.K_d]:
                square1.move(1, 0)

            if keys[pygame.K_UP]:
                square2.move(0, -1)
            if keys[pygame.K_DOWN]:
                square2.move(0, 1)
            if keys[pygame.K_LEFT]:
                square2.move(-1, 0)
            if keys[pygame.K_RIGHT]:
                square2.move(1, 0)

            # Verifica colisão entre os quadrados
            rect1 = pygame.Rect(square1.x, square1.y, square1.size, square1.size)
            rect2 = pygame.Rect(square2.x, square2.y, square2.size, square2.size)
            if rect1.colliderect(rect2):
                # Colisão sólida: impede que os quadrados se sobreponham
                if square1.x < square2.x:
                    square1.x = min(square1.x, square2.x - square1.size)
                    square2.x = max(square2.x, square1.x + square1.size)
                else:
                    square2.x = min(square2.x, square1.x - square2.size)
                    square1.x = max(square1.x, square2.x + square2.size)

                if square1.y < square2.y:
                    square1.y = min(square1.y, square2.y - square1.size)
                    square2.y = max(square2.y, square1.y + square1.size)
                else:
                    square2.y = min(square2.y, square1.y - square2.size)
                    square1.y = max(square1.y, square2.y + square2.size)

                # Verifica se um quadrado causa dano ao outro
                if square1.spikes and not square2.spikes:
                    square2.health -= 2
                    square1.spikes = False
                elif square2.spikes and not square1.spikes:
                    square1.health -= 2
                    square2.spikes = False
                elif square1.spikes and square2.spikes:
                    # Ambos têm espinhos: perdem os espinhos, mas não perdem vida
                    square1.spikes = False
                    square2.spikes = False

            # Verifica se um quadrado pegou um ponto branco
            for point in points[:]:
                if rect1.colliderect(point):
                    square1.spikes = True
                    points.remove(point)
                elif rect2.colliderect(point):
                    square2.spikes = True
                    points.remove(point)

            # Verifica se um quadrado pegou um ponto verde
            for green_point in green_points[:]:
                if rect1.colliderect(green_point):
                    square1.health = min(square1.health + 1, 10)
                    green_points.remove(green_point)
                elif rect2.colliderect(green_point):
                    square2.health = min(square2.health + 1, 10)
                    green_points.remove(green_point)

            # Gera pontos brancos a cada 3 segundos
            current_time = pygame.time.get_ticks()
            if current_time - last_point_time > 3000:
                points.append(create_point())
                last_point_time = current_time

            # Gera pontos verdes a cada 5 segundos
            if current_time - last_green_point_time > 5000:
                green_points.append(create_green_point())
                last_green_point_time = current_time

            # Remove pontos verdes após 3 segundos
            for green_point in green_points[:]:
                if current_time - last_green_point_time > 3000:
                    green_points.remove(green_point)

            # Atualiza o tamanho e a velocidade dos quadrados
            square1.update_size_and_speed()
            square2.update_size_and_speed()

            # Desenha os pontos brancos
            for point in points:
                pygame.draw.rect(screen, WHITE, point)

            # Desenha os pontos verdes
            for green_point in green_points:
                pygame.draw.rect(screen, GREEN, green_point)

            # Desenha os quadrados
            square1.draw()
            square2.draw()

            # Desenha o cabeçalho com a vida dos quadrados
            draw_header(square1, square2)

            # Verifica se o jogo acabou
            if square1.health <= 0 or square2.health <= 0:
                winner = "Vermelho" if square2.health <= 0 else "Azul"
                game_over = True
                show_winner(winner)

            # Atualiza a tela
            pygame.display.flip()
            clock.tick(60)

        else:
            # Tela de vitória
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reinicia o jogo
                        reset_game()
                        game_over = False
                    elif event.key == pygame.K_q:  # Fecha o jogo
                        running = False

# Executa o jogo
if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
