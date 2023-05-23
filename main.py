import pygame

root_path = '/data/data/org.nrunner.nightrunner/files/app/'

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 359))
pygame.display.set_caption('Game')
icon = pygame.image.load(root_path + 'images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load(root_path + 'images/bg.png').convert_alpha()
bg_sound = pygame.mixer.Sound(root_path + 'sounds/bg.mp3')
player = pygame.image.load(root_path + 'images/player_right/player_right1.png').convert_alpha()
ghost = pygame.image.load(root_path + 'images/ghost.png').convert_alpha()
bullet = pygame.image.load(root_path + 'images/bullet.png').convert_alpha()

walk_right = [
    pygame.image.load(root_path + 'images/player_right/player_right1.png').convert_alpha(),
    pygame.image.load(root_path + 'images/player_right/player_right2.png').convert_alpha(),
    pygame.image.load(root_path + 'images/player_right/player_right3.png').convert_alpha(),
    pygame.image.load(root_path + 'images/player_right/player_right4.png').convert_alpha()
]

walk_left = [
    pygame.image.load(root_path + 'images/player_left/player_left1.png').convert_alpha(),
    pygame.image.load(root_path + 'images/player_left/player_left2.png').convert_alpha(),
    pygame.image.load(root_path + 'images/player_left/player_left3.png').convert_alpha(),
    pygame.image.load(root_path + 'images/player_left/player_left4.png').convert_alpha()
]

ghost_list = []

bullets_capacity = 6
bullets = []

FPS = 20
player_anim_count = 0
bg_x = 0
bg_sound.play(loops=-1)
player_speed = 6
player_x = 130
player_y = 263
score = 0
kills = 0
is_jump = False
jump_height = 7
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

label_40 = pygame.font.Font(root_path + 'fonts/Roboto-Black.ttf', 40)
label_24 = pygame.font.Font(root_path + 'fonts/Roboto-Black.ttf', 24)
label_16 = pygame.font.Font(root_path + 'fonts/Roboto-Black.ttf', 16)
lose_label = label_40.render('Вы проиграли!', False, (193, 196, 199))
restart_label = label_24.render('Играть заново', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(225, 180))

gameplay = True
running = True

while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 618, 0)) 

    if gameplay:
        bg_sound.set_volume(1)
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        ghost_rect = ghost.get_rect(topleft=(620, 263))
        
        score += 1
        if score % 100 == 0:
            FPS += 1
        if score % 500 == 0:
            bullets_capacity += 1
        
        if ghost_list:
            for (i, el) in enumerate(ghost_list):
                screen.blit(ghost, el)
                el.x -= 10
                
                if el.x < -10:
                    ghost_list.pop(i)
                
                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 400:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_height >= -7:
                if jump_height > 0:
                    player_y -= (jump_height ** 2) / 2
                else:
                    player_y += (jump_height ** 2) / 2
                jump_height -= 1
            else:
                is_jump = False
                jump_height = 7

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x <= -618:
            bg_x = 0
        
        if bullets:
            for (i, bullet_el) in enumerate(bullets):
                screen.blit(bullet, (bullet_el.x, bullet_el.y))
                bullet_el.x += 5

                if bullet_el.x > 630:
                    bullets.pop(i)
                
                if ghost_list:
                    for (index, ghost_el) in enumerate(ghost_list):
                        if bullet_el.colliderect(ghost_el):
                            ghost_list.pop(index)
                            bullets.pop(i)
                            kills += 1

        score_label = label_16.render(f'Score: {score}', 1, 'White')
        screen.blit(score_label, (12, 5))
        ammo_label = label_16.render(f'Ammo: {bullets_capacity}', 1, 'White')
        screen.blit(ammo_label, (440, 5))
        kills_label = label_16.render(f'Kills: {kills}', 1, 'White')
        screen.blit(kills_label, (540, 5))
        
    else:
        bg_sound.set_volume(0)
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (170, 120))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_focused():
            restart_label = label_24.render('Играть заново', False, (125, 100, 148))
        else:
            restart_label = label_24.render('Играть заново', False, (115, 132, 148))
        
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 130
            ghost_list.clear()
            bullets.clear()
            bullets_capacity = 6
            kills = 0
            score = 0
            FPS = 20
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list.append(ghost.get_rect(topleft=(620, 263)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT and bullets_capacity > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 20, player_y + 5)))
            bullets_capacity -= 1

    clock.tick(FPS)