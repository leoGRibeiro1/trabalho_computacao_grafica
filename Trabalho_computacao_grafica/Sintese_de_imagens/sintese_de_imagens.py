# Alunos: Leonardo Gouvêa Ribeiro - 202111140015 / Leandro Marcos Pinheiro Souza - 201911140007

from funcoes import *

# Guia para resolução de questões
# Primeiramente é preciso instalar a biblioteca pygame pelo comando: 'pip install pygame'
#
# 1 - Bresenham: escolher a opção 1 e inserir dois pontos no formato: x1 y1 x2 y2
#
# 2 - Círculos e elipses: escolher opção 2 e inserir: x1 y1 rx ry, sendo x1 y1 o centro
# e rx o raio na horizontal, e ry o raio na vertical, inserir raios iguais caso deseje 
# ver círculos e raios diferentes em caso de elipse
#
# 3 - Curvas de Bezier: escolher a opção 3, e primeiramente escolher se que retornar
# a curva de grau 2 ou 3, inserindo 'q' ou 'c', após isso, inserir os 3 ou 4 pontos x y 
#
# 4 - Polilinha: escolher a opção 5 e inserir um de cada vez, no mínimo 3 pontos xN yN,
# digitar 'done' quando desejar não inserir mais pontos
# 
# 5 - Preenchimentos recursivo e de varredura: primeiramente criar um polígono na opção 4,
# inserir um de cada vez, no mínimo 3 pontos xN yN, digitar 'done' quando desejar não 
# inserir mais pontos, após isso escolher uma das opções 6 ou 7 de preenchimento, no 
# caso de Recursivo inserir um ponto x1 y1 para iniciar a varedura
#
# 6 - Recorte de linha: Basta usar a opção 1 do algoritimo de bresenham, e inserir 
# pontos x1 y1 x2 y2, sendo eles fora dos pontos -11 < x < 11 e/ou -11 < y < 11
# 
# 7 - Recorte de polígono: Basta usar a opção 4 para criação de polígono, e inserir 
# um de cada vez pontos xN yN, e inserir 'done' quando quiser parar, 
# sendo eles fora dos pontos -11 < x < 11 e/ou -11 < y < 11
#
# 8 - Transformações: Primeiramente usar a opção 4 para criar um polígono, e após isso
# escolher uma das opções de transformação desejada com as seguintes instruções:
#     - Rotação: primeiro inserir em graus a rotação, depois inserir os coordenadas X e Y
#       para definir o pivô
#     - Translação: primeiro definir o deslocamento em X e depois em Y
#     - Escala: primeiro definir o fator da escala em X e depois em Y, depois inserir os
#       coordenadas X e Y para definir o pivô
# 
# 9 - Projeções: selecionar uma das opções de projeção
#     - Ortográfica: Basta inserir o tamanho do cubo
#     - Oblíqua: Primeiramente inserir o tamanho do cubo, e depois inserir os valores
#       dos angulos para o cálculo
#     - Perspectiva: Primeiramente inserir o tamanho do cubo, e depois inserir a distância
#       do cubo

# Função para exibir o menu na lateral esquerda
def display_menu(selected_option):
    font = pygame.font.Font(None, 28)
    options = [
        "1: Desenhar Linha Bresenham/Recorte",
        "2: Desenhar Círculo/Elipse",
        "3: Curva Bezier",
        "4: Criar polígono",
        "5: Polilinha",
        "6: Preenchimento Recursivo",
        "7: Preenchimento por Varredura",
        "8: Rotação de Polígono",
        "9: Translação de Polígono",
        "10: Escala de Polígono",
        "11: Projeção Ortográfica",
        "12: Projeção Oblíqua",
        "13: Projeção Perspectiva",
        "Pressione 'Esc' para sair"
    ]

    # Preenche o fundo do menu
    pygame.draw.rect(screen, BLACK, (0, 0, menu_width, screen_height))
    for index, option in enumerate(options):
        color = WHITE if index == selected_option else GRAY
        text = font.render(option, True, color)
        screen.blit(text, (20, 20 + index * 40))

# Função principal
def main():
    running = True
    selected_option = 0
    points = []
    outside_points = []  
    border_points = []
    polygon_vertices = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = selected_option + 1 
                elif event.key == pygame.K_UP:
                    selected_option = selected_option - 1 

                elif event.key == pygame.K_RETURN: 
                    # Desenhar linha bresenam
                    if selected_option == 0:
                        input_str = input("Digite as coordenadas da linha (x1 y1 x2 y2): ")
                        try:
                            x1, y1, x2, y2 = map(int, input_str.split())
                            points, outside_points = bresenham_with_clipping(x1, y1, x2, y2)
                            border_points = [(x1, y1), (x2, y2)]
                        except ValueError:
                            print("Entrada inválida!")

                    # Círculo
                    elif selected_option == 1:
                        input_str = input("Digite o centro e os raios (x y rx ry): ")
                        try:
                            x, y, rx, ry = map(int, input_str.split())
                            points, border_points = draw_ellipse_midpoint(x, y, rx, ry)
                        except ValueError:
                            print("Entrada inválida!") 
                    
                    # Curva de Bézier de grau 2 e 3
                    elif  selected_option == 2:  
                        print("\nDigite as coordenadas dos pontos de controle")
                        print("Para curva quadrática: 3 pontos (inicial, controle, final)")
                        print("Para curva cúbica: 4 pontos (inicial, controle1, controle2, final)")
                        print("Digite 'q' para quadrática ou 'c' para cúbica")
                        
                        curve_type = input("> ").lower()
                        if curve_type not in ['q', 'c']:
                            print("Tipo de curva inválido!")
                            continue
                        
                        num_points = 3 if curve_type == 'q' else 4
                        control_points = []
                        
                        print(f"\nDigite as coordenadas dos {num_points} pontos:")
                        for i in range(num_points):
                            point_type = "inicial" if i == 0 else "final" if i == num_points-1 else f"controle{i}"
                            while True:
                                try:
                                    input_str = input(f"Ponto {point_type} (x y): ")
                                    x, y = map(int, input_str.split())
                                    control_points.append((x, y))
                                    break
                                except ValueError:
                                    print("Formato inválido! Use: x y")
                        
                        points, outside_points, border_points = create_bezier_curve(control_points)

                    # Polígono
                    elif selected_option == 3: 
                        print("\nDigite as coordenadas dos vértices do polígono (mínimo 3 pontos)")
                        print("Formato: x y (um vértice por linha)")
                        print("Digite 'done' quando terminar")
                        
                        vertices = []
                        while True:
                            input_str = input("> ").strip()
                            if input_str.lower() == 'done':
                                if len(vertices) < 3:
                                    print("Por favor, insira pelo menos 3 vértices.")
                                    vertices = []
                                    continue
                                break
                                
                            try:
                                x, y = map(int, input_str.split())
                                vertices.append((x, y))
                                print(f"Vértice ({x}, {y}) adicionado. Total: {len(vertices)}")
                            except ValueError:
                                print("Formato inválido. Use: x y")
                                continue
                        
                        if len(vertices) >= 3:
                            points, outside_points, border_points = create_polygon_with_clipping(vertices)
                            polygon_vertices = vertices

                    # Atualizar grade no menu
                    for point in outside_points:
                        draw_pixel(point[0], point[1], GRAY)
                    for point in points:
                        draw_pixel(point[0], point[1])

                    # Polilinha
                    if selected_option == 4:                
                        print("\nDigite as coordenadas dos pontos da polilinha (mínimo 3 pontos)")
                        print("Formato: x1 y1 x2 y2 x3 y3 ... xn yn")
                        print("Digite 'done' quando terminar de inserir os pontos")
                        
                        polyline_points = []
                        while True:
                            input_str = input("> ").strip()
                            if input_str.lower() == 'done':
                                if len(polyline_points) < 3:
                                    print("Por favor, insira pelo menos 3 pontos.")
                                    polyline_points = []
                                    continue
                                break
                                
                            try:
                                x, y = map(int, input_str.split())
                                polyline_points.append((x, y))
                                print(f"Ponto ({x}, {y}) adicionado. Total de pontos: {len(polyline_points)}")
                            except ValueError:
                                print("Formato inválido. Use: x y")
                                continue
                        
                        if len(polyline_points) >= 3:
                            points = draw_polyline(polyline_points)
                            border_points = set(points)

                    # Preenchimento Recursivo
                    elif selected_option == 5:  
                        if not border_points:
                            print("Primeiro crie um polígono ou forma fechada")
                            continue
                            
                        input_str = input("Digite as coordenadas do ponto inicial (x y): ")
                        try:
                            start_x, start_y = map(int, input_str.split())
                            border_set = set(points) 
                            filled = flood_fill_recursive(start_x, start_y, border_set)
                            points.extend(list(filled))
                        except ValueError:
                            print("Coordenadas inválidas!")

                    # Preenchimento por Varredura
                    elif selected_option == 6:  
                        if not border_points:
                            print("Primeiro crie um polígono ou forma fechada")
                            continue
                        
                        fill_points = scan_line_fill(border_points)
                        points.extend(fill_points)
                    
                    # Rotação
                    elif selected_option == 7:  
                        if not polygon_vertices:
                            print("Primeiro crie um polígono!")
                            continue
                            
                        try:
                            angle = float(input("Digite o ângulo de rotação em graus: "))
                            pivot_x = int(input("Digite a coordenada X do ponto de pivô: "))
                            pivot_y = int(input("Digite a coordenada Y do ponto de pivô: "))
                            
                            points, outside_points, border_points = transform_and_clip_polygon(
                                polygon_vertices, 'rotate', angle, pivot_x, pivot_y)
                            polygon_vertices = border_points
                            
                        except ValueError:
                            print("Entrada inválida!")
                    
                    # Translação
                    elif selected_option == 8:  
                        if not polygon_vertices:
                            print("Primeiro crie um polígono!")
                            continue
                            
                        try:
                            dx = int(input("Digite o deslocamento em X: "))
                            dy = int(input("Digite o deslocamento em Y: "))
                            
                            points, outside_points, border_points = transform_and_clip_polygon(
                                polygon_vertices, 'translate', dx, dy)
                            polygon_vertices = border_points
                            
                        except ValueError:
                            print("Entrada inválida!")
                
                    # Escala
                    elif selected_option == 9:  
                        if not polygon_vertices:
                            print("Primeiro crie um polígono!")
                            continue
                        
                        try:
                            sx = float(input("Digite o fator de escala em X: "))
                            sy = float(input("Digite o fator de escala em Y: "))
                            fixed_x = int(input("Digite a coordenada X do ponto fixo: "))
                            fixed_y = int(input("Digite a coordenada Y do ponto fixo: "))
                            
                            points, outside_points, border_points = transform_and_clip_polygon(
                                polygon_vertices, 'scale', sx, sy, fixed_x, fixed_y)
                            polygon_vertices = border_points
                            
                        except ValueError:
                            print("Entrada inválida!")

                    # Projeção Ortográfica
                    elif selected_option == 10:  
                        try:
                            size = int(input("Digite o tamanho do cubo: "))
                            
                            vertices_3d, edges = create_cube(size)
                            vertices_2d = orthographic_projection(vertices_3d)
                            points = draw_3d_object(vertices_2d, edges)
                        except ValueError:
                            print("Entrada inválida!")

                    # Projeção Oblíqua
                    elif selected_option == 11:  
                        try:
                            size = int(input("Digite o tamanho do cubo: "))
                            alpha = float(input("Digite o ângulo alpha (em graus): "))
                            beta = float(input("Digite o ângulo beta (em graus): "))
                            
                            vertices_3d, edges = create_cube(size)
                            vertices_2d = oblique_projection(vertices_3d, alpha, beta)
                            points = draw_3d_object(vertices_2d, edges)
                            
                        except ValueError:
                            print("Entrada inválida!")

                    # Projeção Perspectiva
                    elif selected_option == 12:  
                        try:
                           
                            size = int(input("Digite o tamanho do cubo: "))
                            d = float(input("Digite a distância do centro de projeção: "))
                            
                            vertices_3d, edges = create_cube(size)
                            vertices_2d = perspective_projection(vertices_3d, d)
                            points = draw_3d_object(vertices_2d, edges)
                            
                        except ValueError:
                            print("Entrada inválida!")
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Preenche a área de desenho com preto
        screen.fill(BLACK)

        # Desenha o menu na lateral esquerda
        display_menu(selected_option)

        # Desenha a grade e os pontos na área principal
        draw_grid()

        for point in outside_points:
            draw_pixel(point[0], point[1], GRAY)

        for point in points:
            draw_pixel(point[0], point[1])

        # Atualiza a tela
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
