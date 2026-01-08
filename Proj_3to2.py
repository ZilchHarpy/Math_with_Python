'''
Aprendendo a lógica por trás do código de conversão de 3D para 2D
Este código converte coordenadas tridimensionais (x, y, z) em coordenadas bidimensionais (x', y')
Assim, um cubo 3D pode ser representado em um plano 2D, por exemplo

Aqui eu uso para visualização a biblioteca turtle do Python, simulando uma tela OLED de 128x64 pixels
'''

import turtle # Biblioteca para desenhos 2D
from math import * # Biblioteca matemática para cálculos trigonométricos
import time # Biblioteca para controle de tempo para animações
import numpy as np # Biblioteca para manipulação de arrays e operações matemáticas avançadas

running = [True]

# Função para sair do programa
def quit_program(screen):
        running[0] = False
        screen.bye()

# Função de configuração inicial da tela
def setup_screen(t: turtle.Turtle, screen: turtle.Screen = turtle.Screen()):
    screen.bgcolor("black")
    screen.title("Projeção 3D para 2D - Cubo")
    screen.setup(width=128, height=64)
    screen.delay(0)
    t.speed(0)
    t.pencolor("white")
    t.hideturtle()
    turtle.tracer(0, 0)
    t.penup()
    screen.onkey(lambda: quit_program(screen), "q")

# Função para conectar os pontos do cubo
def connect_points(t: turtle.Turtle, i: int, j: int, points: list):
    t.penup()
    t.goto(points[i][0], points[i][1])
    t.pendown()
    t.goto(points[j][0], points[j][1])
    t.penup()



# Declarando os vértices do cubo em 3D
points = []
points.append(np.matrix([1, 1, 1])) #0
points.append(np.matrix([1, 1, -1])) #1
points.append(np.matrix([1, -1, -1])) #2
points.append(np.matrix([1, -1, 1])) #3
points.append(np.matrix([-1, 1, 1])) #4
points.append(np.matrix([-1, 1, -1])) #5
points.append(np.matrix([-1, -1, -1])) #6
points.append(np.matrix([-1, -1, 1])) #7


# Definindo as matrizes de projeção
projmatrix = np.matrix(
    [
        [1, 0, 0],
        [0, 1, 0]
    ]
)

def main():
    t = turtle.Turtle()
    setup_screen(t) # Configura a tela de desenho
    turtle.listen() 

    angle = 0.0 # Ângulo inicial para rotação
    var = 0.2
    scale = 10 # Fator de escala para ajustar o tamanho da projeção na tela
    frame_time = 1.0 / 120.0  # ~120 FPS
    last_time = time.time()

    proj_points = [
         [n, n] for n in range(len(points))
    ]

    # Loop para manter a janela aberta até apertar 'Q'
    while running[0]:
        current_time = time.time()
        elapsed = current_time - last_time
        
        # Aguarda o tempo necessário para manter 60 FPS
        if elapsed < frame_time:
            time.sleep(frame_time - elapsed)
        
        last_time = time.time()
        
        t.clear() # Limpa a tela para redesenhar

        #matriz de rotação em torno do eixo Z
        rot_z = np.matrix(
        [
            [cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [0, 0, 1]
        ])
        rot_y = np.matrix(
        [
            [cos(angle), 0, sin(angle)],
            [0, 1, 0],
            [-sin(angle), 0, cos(angle)]
        ])
        rot_x = np.matrix(
        [
            [1, 0, 0],
            [0, cos(angle), -sin(angle)],
            [0, sin(angle), cos(angle)]
        ])

        if angle > 2 * pi:
            angle -= 2*pi

        if scale >= 50 or scale <= 5:
            var = -var

        angle += 0.01
        scale += var

        i = 0
        for point in points:
            rot2d = np.dot(rot_x, point.reshape((3, 1))) # Aplica a rotação em x no ponto 3D
            rot2d = np.dot(rot_y, rot2d) # Aplica a rotação em y no ponto 3D
            rot2d = np.dot(rot_z, rot2d) # Aplica a rotação em z no ponto 3D
            proj2d = np.dot(projmatrix, rot2d) # Aplica a matriz de projeção e obtém o ponto 2D
            
            x = int(proj2d[0, 0].item() * scale) # Centraliza na tela (128/2)
            y = int(proj2d[1, 0].item() * scale)  # Centraliza na tela (64/2)
            t.goto(x, y)
            proj_points[i] = [x, y]
            #t.dot(2)

            i += 1


        for p in range(4):
            connect_points(t, p, (p+1)%4, proj_points)
            connect_points(t, p+4, ((p+5)%4)+4, proj_points)
            connect_points(t, p, ((p+4)%4)+4, proj_points)
        
        turtle.update()


if __name__ == "__main__":
    main()