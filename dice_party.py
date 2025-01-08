#Importando bibliotecas
import pygame
import sys
from random import randint

pygame.init()

screen = pygame.display.set_mode((1280, 720))

#Lista para as casas do tabuleiro
casas_tabuleiro = [(20,560),(50,460),(68,324),(190,230),(330,160),(487,100),(660,60),(822,85),(993,110),(1130,180),(1090,330),(960,427),(760,438),(544,430),(346,461),(185,540)]

#Carregando as imagens
imp = pygame.image.load('Tabuleiro.jpg')
size = pygame.transform.scale(imp, (1280,720))
start = pygame.image.load('start_btn.png').convert_alpha()
exit = pygame.image.load('exit_btn.png').convert_alpha()
main_menu_img = pygame.image.load('Main_menu.jpg')
main_menu_img2 = pygame.transform.scale(main_menu_img, (1280,720))
cat_player = pygame.image.load('cat.png').convert_alpha()
duck_player = pygame.image.load('duck.png').convert_alpha()
cat_scaled = pygame.transform.scale(cat_player, (70, 70))
duck_scaled = pygame.transform.scale(duck_player, (70,70))

#Fonte para exibir mensagens
font_msg = pygame.font.Font('Fonte_Fofa.ttf', 50)

#Variáveis de pontuação
font_points = pygame.font.Font('Fonte_Fofa.ttf', 25)
coins_duck_1 = 10
coins_cat_1 = 10
star_duck_1 = 0
star_cat_1 = 0
round_counter_c = 0
round_counter_d = 0

  

#Contador 
contagem_duck = 0
contagem_cat = 0 

#Função para mostrar mensagens temporária
def exibir_mensagem(tela, mensagem, tempo=2000, x=1280, y=720):
    font = pygame.font.Font('Fonte_Fofa.ttf', 50)
    texto = font.render(mensagem, True, (0,0,0))
    texto_rect = texto.get_rect(center=(x // 2, y // 2))
    tela.blit(texto, texto_rect)  # Desenha a mensagem na tela
    pygame.display.flip()  # Atualiza a tela
    pygame.time.wait(tempo)

#Criando uma classe pra ser de base
class TelaBase:
    def __init__(self):
        self.next = self

    def eventos(self, events):
        pass

    def atualizar(self):
        pass

    def desenhar(self, screen):
        pass

#Classe dos botões 
class Button():
    def __init__(self, x, y, image, scale):
        #Diminuindo a escala dos botões
        width_img = image.get_width()
        height_img = image.get_height()

        self.image = pygame.transform.scale(image, (int(width_img * scale), int(height_img * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        #Fazendo o botão ser clicado apenas 1 vez
        self.clicked = False

    def draw(self):
        #desenhar o botão na tela
        screen.blit(self.image, (self.rect.x, self.rect.y) )
    
        #Posição do mouse
        pos = pygame.mouse.get_pos()

        #Dando Funcionalidade pros botões
        action = False 

        #Checando se o mouse tá em cima do botão ou clicando
        if self.rect.collidepoint(pos):
           if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
           if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action
                
#Classe pra tela de menu
class MenuScreen(TelaBase):
    def processar_eventos(self, eventos):

        #Evento para passar para a tela do jogo 
        for event in eventos:
            start_button = Button(0,0, start, 1)
            if event.type == start_button.draw():
                self.next = TelaJogo()

            #Evento para sair do jogo     
            exit_button = Button(600,500, exit, 1)
            if event.type == exit_button.draw():
                pygame.quit()
                sys.exit()

    def desenhar(self, screen):
        
        #Customização da tela inicial
        screen.fill((199, 215, 255))
        screen.blit(main_menu_img2, (0,0))
        
        #Colocando os botões na tela de menu
        start_button = Button(200,300, start, 0.8)
        if start_button.draw():
            self.next = TelaJogo()
        exit_button = Button(700,300, exit, 0.8)
        if exit_button.draw():
            pygame.quit()
            sys.exit()

class TelaJogo(TelaBase):

            
    def processar_eventos(self, eventos):
        global contagem_duck, contagem_cat, coins_duck_1, coins_cat_1, star_duck_1, star_cat_1, round_counter_d, round_counter_c
        for event in eventos:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                dado = randint(1,6)
                contagem_duck += dado
                round_counter_d += 1
                dado_msg = exibir_mensagem(screen, f'Duck rolled a {dado}!', 1000)
                
                casa_anterior_d = contagem_duck - dado
                if casa_anterior_d <= 10 < contagem_duck or casa_anterior_d == 10 and contagem_duck == 1:
                    exibir_mensagem(screen, f"Want to buy a star?", 2000, 1280, 500)
                
                    if event.type == pygame.KEYDOWN and coins_duck_1 >= 20:
                        exibir_mensagem(screen,f'You bought a star! ★', 2000, 1280, 820)
                        star_duck_1 += 1
                        coins_duck_1 = coins_duck_1 - 20
                    else:
                        exibir_mensagem(screen,f'You cant buy a star!', 2000, 1280, 820)

                if contagem_duck == 14 or contagem_duck == 11:
                    lucky_msg = exibir_mensagem(screen, f'Lucky Space +5 coins', 2000, 1280, 600)
                    coins_duck_1 += 5
                if contagem_duck == 2 or contagem_duck == 9:
                    exibir_mensagem(screen, f'Event! Cat go back!', 2000, 1280, 600)
                    contagem_cat -= 3
                if contagem_duck > 15:
                   resto = contagem_duck - 15
                   contagem_duck = resto

                if contagem_duck in {3,5,6,8,10,12,15}:
                    coins_duck_1 += 2
                    exibir_mensagem(screen, f'Gain +2 coins!', 2000, 1280, 600)
                
                if contagem_duck in {1,4,7,13}:
                    coins_duck_1 -= 2
                    exibir_mensagem(screen, f'Loose -2 coins!', 2000, 1280, 600)
                
                if coins_duck_1 < 0:
                    coins_duck_1 = 0

                   
            if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                dado = randint(1,6)
                contagem_cat += dado
                exibir_mensagem(screen, f'Cat rolled a {dado}!', 2000)
                casa_anterior_c = contagem_cat - dado
                round_counter_c += 1
                if casa_anterior_c <= 10 < contagem_cat or casa_anterior_c == 10 and contagem_cat == 1:
                    exibir_mensagem(screen, f"Want to buy a star?", 2000, 1280, 500)
                
                    if event.type == pygame.KEYDOWN and coins_cat_1 >= 20:
                        exibir_mensagem(screen,f'You bought a star! ★', 2000, 1280, 820)
                        star_cat_1 += 1
                        coins_cat_1 = coins_cat_1 - 20
                    else:
                        exibir_mensagem(screen,f'You cant buy a star!', 2000, 1280, 820)

                if contagem_cat == 14 or contagem_cat == 11:
                    lucky_msg = exibir_mensagem(screen, f'Lucky Space +5 coins!', 2000, 1280, 600)
                    coins_cat_1 += 5

                if contagem_cat == 2 or contagem_cat == 9 and contagem_duck != 0:
                    exibir_mensagem(screen, f'Event! Duck go back!', 2000, 1280, 600)
                    contagem_duck -= 3

                if contagem_cat > 15:
                   resto = contagem_cat - 15
                   contagem_cat = resto  
                
                if contagem_cat in {3,5,6,8,10,12,15}:
                    exibir_mensagem(screen, f'Gain +2 coins!', 2000, 1280, 600)
                    coins_cat_1 += 2
                
                if contagem_cat in {1,4,7,13}:
                    coins_cat_1 = coins_cat_1 - 2
                    exibir_mensagem(screen, f'Loose -2 coins!', 2000, 1280, 600)
                
                if coins_cat_1 < 0:
                    coins_cat_1 = 0
                if round_counter_d == 15 and round_counter_c == 15:
                    if star_duck_1 > star_cat_1:
                        exibir_mensagem(screen, f'The Duck Wins!!!', 2000, 1280, 600)
                    if star_cat_1 > star_duck_1:
                        self.next = MenuScreen()
                        exibir_mensagem(screen, f'The Cat Wins!!!', 2000, 1280, 600)
                        self.next = MenuScreen()        
                    if star_duck_1 == star_cat_1:
                        exibir_mensagem(screen, f'We have a Tie!!!', 2000, 1280, 400)
                        self.next = MenuScreen()

                
    def desenhar(self, screen):
        screen.fill((0,0,0))
        star_duck_formatado = font_points.render(f'{star_cat_1}', True, (0,0,0))
        star_cat_formatado = font_points.render(f'{star_duck_1}', True, (0,0,0))
        duck_formatado = font_points.render(f'{coins_cat_1}', True, (0,0,0))
        cat_formatado = font_points.render(f'{coins_duck_1}', True, (0,0,0),)
        screen.blit(size, (0,0))
        screen.blit(star_duck_formatado, (180, 38))
        screen.blit(star_cat_formatado, (1210, 38))
        screen.blit(duck_formatado, (180, 76))
        screen.blit(cat_formatado, (1210, 72))
        screen.blit(duck_scaled, (casas_tabuleiro[contagem_duck]))
        screen.blit(cat_scaled, (casas_tabuleiro[contagem_cat]))

def main():
    pygame.init()
    
    pygame.display.set_caption("Dice Party")

    tela_atual = MenuScreen()
    
    while True:
        eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela_atual.processar_eventos(eventos)
        tela_atual.atualizar()

        tela_atual.desenhar(screen)
        pygame.display.flip()

        tela_atual = tela_atual.next

main()
