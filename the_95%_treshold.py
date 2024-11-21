import pygame
import math
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("The 95% Threshold")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Propiedades del jugador
player_x, player_y = screen_width // 2, screen_height // 2
player_angle = 0
player_speed = 4
player_alive = True

# Probabilidad de bala atascada
shooting_probability = 100  # Comienza en 100%

# Propiedades de las balas
bullets = []  # Cada bala es una lista: [x, y, angle]
bullet_speed = 7
bullet_cooldown = 15  # Tiempo de enfriamiento entre disparos
bullet_timer = 0

# Propiedades de los enemigos
enemies = []
enemy_speed = 4
enemy_spawn_timer = 0
enemy_spawn_delay = 105  # Cada segundo aparece un enemigo

#Propiedades de los puntos
points = []
player_points = 0
points_spawn_timer = 0
points_spawn_delay = 200
points_radius = 15
points_in_screen = 0

# Radio del área de juego
arena_radius = 350

#Fuente
font = pygame.font.SysFont(None, 70)

# Función para dibujar la arena
def draw_arena():
    pygame.draw.circle(screen, WHITE, (screen_width // 2, screen_height // 2), arena_radius, 2)

# Función para dibujar al jugador como un triángulo rotado
def draw_rotated_triangle(surface, x, y, angle, size=20, color=WHITE):
    front = (x + math.cos(angle) * size, y - math.sin(angle) * size)
    left = (x + math.cos(angle + 2 * math.pi / 3) * size, y - math.sin(angle + 2 * math.pi / 3) * size)
    right = (x + math.cos(angle - 2 * math.pi / 3) * size, y - math.sin(angle - 2 * math.pi / 3) * size)
    pygame.draw.polygon(surface, color, [front, left, right])

# Función para generar un enemigo en un lugar aleatorio fuera del círculo
def spawn_enemy():
    angle = random.uniform(0, 2 * math.pi)
    x = screen_width // 2 + math.cos(angle) * (arena_radius + 50)
    y = screen_height // 2 + math.sin(angle) * (arena_radius + 50)
    enemies.append([x, y])

def spawn_point():
    global points_in_screen
    angle = random.uniform(0, 2 *math.pi)
    distance = random.uniform(arena_radius , 0)
    x = screen_width // 2 + math.cos(angle) * distance
    y = screen_height // 2 + math.sin(angle) * distance 
    points.append([x, y])   
    points_in_screen += 1

# Función para reiniciar el juego
def reset_game():
    global player_x, player_y, player_alive, bullets, enemies, points, shooting_probability, player_points, points_in_screen
    player_x, player_y = screen_width // 2, screen_height // 2
    player_alive = True
    bullets = []
    enemies = []
    points = []
    shooting_probability = 100
    player_points = 0
    points_in_screen = 0

def check_points_player_collisions():
    global player_points, shooting_probability, points_in_screen
    for point in points[:]:
        if math.hypot(player_x - point[0], player_y - point[1]) < points_radius:
            points.remove(point)  # Eliminar el punto recogido
            player_points += 1  # Aumentar los puntos del jugador
            points_in_screen -= 1
            shooting_probability = 100  # Restablecer probabilidad de disparo
            if player_points >= 11:  # Si el jugador llega a 11 puntos
                return True  # El jugador ha ganado 

# Función para detectar colisiones entre balas y enemigos
def check_bullet_enemy_collisions():
    global enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            # Comprobar si la bala está cerca de un enemigo
            if math.hypot(bullet[0] - enemy[0], bullet[1] - enemy[1]) < 15:
                enemies.remove(enemy)  # Eliminar enemigo
                bullets.remove(bullet)  # Eliminar bala
                break  # No es necesario comprobar más colisiones para esta bala

def draw_text(text, x, y, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))

# Función principal
running = True
while running:
    screen.fill(BLACK)
    draw_arena()

    # Eventos
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not player_alive:
        font = pygame.font.Font(None, 74)
        text = font.render("¡Has muerto!", True, RED)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        reset_game()
        continue

    if player_points >= 11:  # Si el jugador ha ganado
        font = pygame.font.Font(None, 74)
        text = font.render("¡Ganaste!", True, GREEN)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        reset_game()
        continue
    

    # Movimiento del jugador con clic derecho
    if mouse_buttons[2]:  # Click derecho
        dx = mouse_x - player_x
        dy = mouse_y - player_y
        dist = math.hypot(dx, dy)
        if dist > player_speed:
            player_x += dx / dist * player_speed
            player_y += dy / dist * player_speed

    # Asegurarse de que el jugador no salga del área de juego
    dx = player_x - screen_width // 2
    dy = player_y - screen_height // 2
    dist_from_center = math.hypot(dx, dy)
    if dist_from_center > arena_radius:
        player_x = screen_width // 2 + dx / dist_from_center * arena_radius
        player_y = screen_height // 2 + dy / dist_from_center * arena_radius

    # Rotación del jugador hacia el cursor
    player_angle = math.atan2(player_y - mouse_y, mouse_x - player_x)

    # Dibujar al jugador
    draw_rotated_triangle(screen, player_x, player_y, player_angle)

    # Disparar balas con clic izquierdo
    bullet_timer += 1
    if mouse_buttons[0] and bullet_timer >= bullet_cooldown:  # Click izquierdo
        bullet_timer = 0
        if random.uniform(0, 100) <= shooting_probability:
            bullet_start_x = player_x + math.cos(player_angle) * 20
            bullet_start_y = player_y - math.sin(player_angle) * 20
            bullets.append([bullet_start_x, bullet_start_y, player_angle])
            shooting_probability = max(0, shooting_probability - 1)  # Reducir probabilidad en 1%
        else:
            player_alive = False  # Autodaño: el jugador muere

    # Mover y dibujar balas
    for bullet in bullets:
        bullet[0] += math.cos(bullet[2]) * bullet_speed
        bullet[1] -= math.sin(bullet[2]) * bullet_speed
        pygame.draw.circle(screen, RED, (int(bullet[0]), int(bullet[1])), 5)

    # Eliminar balas fuera de la pantalla
    bullets = [b for b in bullets if 0 <= b[0] <= screen_width and 0 <= b[1] <= screen_height]

    # Spawnear enemigos
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_delay:
        spawn_enemy()
        enemy_spawn_timer = 0

    if points_in_screen == 0:
        points_spawn_timer += 1
        if points_spawn_timer >= points_spawn_delay:
            spawn_point()
            points_spawn_timer = 0

    # Mover enemigos hacia el jugador y dibujarlos
    for enemy in enemies:
        ex, ey = enemy
        angle_to_player = math.atan2(player_y - ey, player_x - ex)
        enemy[0] += math.cos(angle_to_player) * enemy_speed
        enemy[1] += math.sin(angle_to_player) * enemy_speed
        pygame.draw.circle(screen, WHITE, (int(enemy[0]), int(enemy[1])), 10)

        # Detectar colisión con el jugador
        if math.hypot(player_x - enemy[0], player_y - enemy[1]) < 15:
            player_alive = False

    # Comprobar colisiones del jugador con los puntos
    if check_points_player_collisions():
        font = pygame.font.Font(None, 74)
        text = font.render("¡Ganaste!", True, GREEN)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        reset_game()

    # Dibujar los puntos
    for point in points:
        pygame.draw.circle(screen, GREEN, (int(point[0]), int(point[1])), points_radius)

    draw_text(f"{shooting_probability}", (screen_width // 2)-50, (screen_height // 2)-20)

    # Comprobar colisiones entre balas y enemigos
    check_bullet_enemy_collisions()

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

pygame.quit()
