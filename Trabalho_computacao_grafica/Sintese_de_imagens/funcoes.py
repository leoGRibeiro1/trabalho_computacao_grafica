import pygame
import math

pygame.init()

# Janela
menu_width = 200
screen_width = 1000 + menu_width  # A largura total inclui o menu
screen_height = 670
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sintese de imagens")
grid_size = 25  
num_cells = 11  

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Cohen-Sutherland
INSIDE = 0  
LEFT = 1    
RIGHT = 2   
BOTTOM = 4  
TOP = 8 

# Referências para Cohen-Sutherland
def compute_code(x, y):
    code = INSIDE
    if x < -num_cells:
        code |= LEFT
    elif x > num_cells:
        code |= RIGHT
    if y < -num_cells:
        code |= BOTTOM
    elif y > num_cells:
        code |= TOP
    return code

# Função para converter coordenadas do sistema para a tela
def to_screen_coordinates(x, y):
    return (menu_width + (screen_width - menu_width) // 2 + int(x * grid_size), 
            screen_height // 2 - int(y * grid_size))

# Função para desenhar pixel
def draw_pixel(x, y, color=RED):
    screen_x, screen_y = to_screen_coordinates(x, y)
    pygame.draw.rect(screen, color, (screen_x, screen_y, grid_size, grid_size))

# Algoritmo de Bresenham
def bresenham(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points

# Bresenham com recorte
def bresenham_with_clipping(x1, y1, x2, y2):
    full_line = bresenham(x1, y1, x2, y2)
    
    clipped = cohen_sutherland_clip(x1, y1, x2, y2)
    
    if clipped:
        inside_points = []
        outside_points = []
        
        for point in full_line:
            if -num_cells <= point[0] <= num_cells and -num_cells <= point[1] <= num_cells:
                inside_points.append(point)
            else:
                outside_points.append(point)
        
        return inside_points, outside_points
    else:
        return [], full_line

# Função do recorte
def cohen_sutherland_clip(x1, y1, x2, y2):
    xmin, xmax = -num_cells, num_cells
    ymin, ymax = -num_cells, num_cells
    
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)
    accept = False
    
    while True:
        if code1 == 0 and code2 == 0:
            accept = True
            break
        
        elif code1 & code2 != 0:
            break
        
        code = code1 if code1 != 0 else code2
        
        if code & TOP:
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
            y = ymax
        elif code & BOTTOM:
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            y = ymin
        elif code & RIGHT:
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            x = xmax
        elif code & LEFT:
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            x = xmin
            
        if code == code1:
            x1, y1 = x, y
            code1 = compute_code(x1, y1)
        else:
            x2, y2 = x, y
            code2 = compute_code(x2, y2)
    
    return (x1, y1, x2, y2) if accept else None

# Função de desenhar círculo/elipse
def draw_ellipse_midpoint(x_center, y_center, rx, ry):
    points = []
    border_points = []
    
    x = 0
    y = ry
    rx_sq = rx ** 2
    ry_sq = ry ** 2
    p1 = ry_sq - (rx_sq * ry) + (0.25 * rx_sq)
    
    first_quadrant = []
    while (2 * ry_sq * x) < (2 * rx_sq * y):
        first_quadrant.append((x, y))
        points.extend([
            (x_center + x, y_center + y), (x_center - x, y_center + y),
            (x_center + x, y_center - y), (x_center - x, y_center - y)
        ])
        x += 1
        if p1 < 0:
            p1 += 2 * ry_sq * x + ry_sq
        else:
            y -= 1
            p1 += 2 * ry_sq * x - 2 * rx_sq * y + ry_sq

    p2 = (ry_sq * ((x + 0.5) ** 2)) + (rx_sq * ((y - 1) ** 2)) - (rx_sq * ry_sq)
    second_quadrant = []
    while y >= 0:
        second_quadrant.append((x, y))
        points.extend([
            (x_center + x, y_center + y), (x_center - x, y_center + y),
            (x_center + x, y_center - y), (x_center - x, y_center - y)
        ])
        y -= 1
        if p2 > 0:
            p2 -= 2 * rx_sq * y + rx_sq
        else:
            x += 1
            p2 += 2 * ry_sq * x - 2 * rx_sq * y + rx_sq

    border_points = []
    border_points.extend([(x_center + x, y_center - y) for x, y in reversed(first_quadrant)])
    border_points.extend([(x_center + x, y_center - y) for x, y in second_quadrant])

    border_points.extend([(x_center + x, y_center + y) for x, y in second_quadrant])
    border_points.extend([(x_center + x, y_center + y) for x, y in reversed(first_quadrant)])

    border_points.extend([(x_center - x, y_center + y) for x, y in first_quadrant])
    border_points.extend([(x_center - x, y_center + y) for x, y in reversed(second_quadrant)])

    border_points.extend([(x_center - x, y_center - y) for x, y in reversed(second_quadrant)])
    border_points.extend([(x_center - x, y_center - y) for x, y in first_quadrant])

    return points, border_points

# Calcular pontos de controle
def calculate_bezier_point(t, points):
    n = len(points) - 1  
    result_x = 0
    result_y = 0
    
    for i in range(n + 1):
        coef = 1
        if i > 0:
            for j in range(i):
                coef *= (n - j)
                coef //= (j + 1)
        
        term = coef * (1 - t)**(n - i) * t**i
        result_x += points[i][0] * term
        result_y += points[i][1] * term
    
    return round(result_x), round(result_y)

# Função que desenha as curvas
def bezier_curve(control_points):
    if len(control_points) not in [3, 4]:
        raise ValueError("Número inválido de pontos de controle. Use 3 para quadrática ou 4 para cúbica.")
    
    points = []
    last_point = None
    
    num_steps = 100
    
    for i in range(num_steps + 1):
        t = i / num_steps
        current_point = calculate_bezier_point(t, control_points)
        
        if last_point is not None:
            line_points = bresenham(last_point[0], last_point[1], 
                                  current_point[0], current_point[1])
            points.extend(line_points)
        
        last_point = current_point
    
    return points

# Função que cria as curvas
def create_bezier_curve(input_points):
    try:
        curve_points = bezier_curve(input_points)
        inside_points = []
        outside_points = []
        
        for point in curve_points:
            if -num_cells <= point[0] <= num_cells and -num_cells <= point[1] <= num_cells:
                inside_points.append(point)
            else:
                outside_points.append(point)
        
        return inside_points, outside_points, input_points
        
    except Exception as e:
        print(f"Erro ao criar curva de Bézier: {str(e)}")
        return [], [], []

# Função de criar polígono
def create_polygon(vertices):
    points = []
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        line_points = bresenham(x1, y1, x2, y2)
        points.extend(line_points)
    
    return points, vertices

def draw_polyline(points):
    if len(points) < 2:
        return []
        
    all_points = []
    
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]

        line_points = bresenham(p1[0], p1[1], p2[0], p2[1])
        all_points.extend(line_points)
    
    return all_points

# Função de preenchimento recursivo
def flood_fill_recursive(x, y, border_points, filled_points=None):
   
    if filled_points is None:
        filled_points = set()
    
    if x < -num_cells or x > num_cells or y < -num_cells or y > num_cells:
        return filled_points
    
    current = (x, y)
    
    if current in filled_points or current in border_points:
        return filled_points
    
    filled_points.add(current)
    
    flood_fill_recursive(x + 1, y, border_points, filled_points)  
    flood_fill_recursive(x - 1, y, border_points, filled_points)  
    flood_fill_recursive(x, y + 1, border_points, filled_points)  
    flood_fill_recursive(x, y - 1, border_points, filled_points)  
    
    return filled_points

# Função de preenchimento por varredura
def scan_line_fill(polygon_points):
   
    if not polygon_points:
        return []
    
    y_min = min(point[1] for point in polygon_points)
    y_max = max(point[1] for point in polygon_points)
    
    fill_points = []
    
    for y in range(y_min, y_max + 1):
        intersections = []
        
        for i in range(len(polygon_points)):
            p1 = polygon_points[i]
            p2 = polygon_points[(i + 1) % len(polygon_points)]
            
            if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                if p1[1] != p2[1]: 
                    x = int(p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]))
                    intersections.append(x)
        
        intersections.sort()
        
        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                for x in range(intersections[i], intersections[i + 1] + 1):
                    fill_points.append((x, y))
    
    return fill_points

# Recorte de polígono 
def clip_polygon(vertices):
    if len(vertices) < 3:
        return [], [], []  

    clipped_points = []
    outside_points = []
    clipped_vertices = []
    
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        
        clipped = cohen_sutherland_clip(x1, y1, x2, y2)
        
        if clipped:
            x1_clip, y1_clip, x2_clip, y2_clip = clipped
            
            original_line = bresenham(x1, y1, x2, y2)
            
            for point in original_line:
                if -num_cells <= point[0] <= num_cells and -num_cells <= point[1] <= num_cells:
                    if point not in clipped_points:
                        clipped_points.append(point)
                else:
                    if point not in outside_points:
                        outside_points.append(point)
            
            if len(clipped_vertices) == 0 or clipped_vertices[-1] != (x1_clip, y1_clip):
                clipped_vertices.append((x1_clip, y1_clip))
            if len(clipped_vertices) == 0 or clipped_vertices[-1] != (x2_clip, y2_clip):
                clipped_vertices.append((x2_clip, y2_clip))
        else:
            line_points = bresenham(x1, y1, x2, y2)
            outside_points.extend(line_points)

    return clipped_points, outside_points, clipped_vertices

# Retorna os pontos do polígono recortado
def create_polygon_with_clipping(vertices):
    clipped_points, outside_points, clipped_vertices = clip_polygon(vertices)
    return clipped_points, outside_points, clipped_vertices

# Rotacionar polígono
def rotate_polygon(vertices, angle_degrees, pivot_x=0, pivot_y=0):
    angle_rad = math.radians(angle_degrees)
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    
    new_vertices = []
    
    for x, y in vertices:
        translated_x = x - pivot_x
        translated_y = y - pivot_y
        
        rotated_x = translated_x * cos_angle - translated_y * sin_angle
        rotated_y = translated_x * sin_angle + translated_y * cos_angle
        
        final_x = rotated_x + pivot_x
        final_y = rotated_y + pivot_y
        
        new_vertices.append((round(final_x), round(final_y)))
    
    return new_vertices

# Translação do polígono
def translate_polygon(vertices, dx, dy):
    return [(x + dx, y + dy) for x, y in vertices]

# Aplicar escala no polígono
def scale_polygon(vertices, sx, sy, fixed_point_x=0, fixed_point_y=0):
    new_vertices = []
    
    for x, y in vertices:
        translated_x = x - fixed_point_x
        translated_y = y - fixed_point_y
        
        scaled_x = translated_x * sx
        scaled_y = translated_y * sy
        
        final_x = scaled_x + fixed_point_x
        final_y = scaled_y + fixed_point_y
        
        new_vertices.append((round(final_x), round(final_y)))
    
    return new_vertices

# Chama a transformação correta
def transform_and_clip_polygon(vertices, transformation_type, *args):
    if transformation_type == 'rotate':
        angle, pivot_x, pivot_y = args
        transformed_vertices = rotate_polygon(vertices, angle, pivot_x, pivot_y)
    elif transformation_type == 'translate':
        dx, dy = args
        transformed_vertices = translate_polygon(vertices, dx, dy)
    elif transformation_type == 'scale':
        sx, sy, fixed_x, fixed_y = args
        transformed_vertices = scale_polygon(vertices, sx, sy, fixed_x, fixed_y)
    else:
        return [], [], vertices
    
    return create_polygon_with_clipping(transformed_vertices)

# Projeção ortogonal
def orthographic_projection(vertices_3d):
    return [(x, y) for x, y, z in vertices_3d]

# Projeção oblíqua
def oblique_projection(vertices_3d, alpha=45, beta=45):
    alpha_rad = math.radians(alpha)
    beta_rad = math.radians(beta)
    
    l = math.cos(alpha_rad) 
    m = math.cos(beta_rad)   
    
    projected_vertices = []
    for x, y, z in vertices_3d:
        x_proj = x + l * z
        y_proj = y + m * z
        projected_vertices.append((round(x_proj), round(y_proj)))
    
    return projected_vertices

# Projeção perspectiva
def perspective_projection(vertices_3d, d=100):
    projected_vertices = []
    for x, y, z in vertices_3d:
        if z != d:  
            scale = d / (d - z)
            x_proj = x * scale
            y_proj = y * scale
            projected_vertices.append((round(x_proj), round(y_proj)))
        else:
            projected_vertices.append((round(x), round(y)))
    
    return projected_vertices

# Criar objeto 3d
def create_cube(size):
    half = size / 2
    vertices = [
        (0 - half, 0 - half, 0 - half),  
        (0 + half, 0 - half, 0 - half),  
        (0 + half, 0 + half, 0 - half),  
        (0 - half, 0 + half, 0 - half),  

        (0 - half, 0 - half, 0 + half), 
        (0 + half, 0 - half, 0 + half),  
        (0 + half, 0 + half, 0 + half),
        (0 - half, 0 + half, 0 + half),  
    ]
    
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  
        (4, 5), (5, 6), (6, 7), (7, 4),  
        (0, 4), (1, 5), (2, 6), (3, 7)   
    ]
    
    return vertices, edges

# Desenha linhas do objeto 3d
def draw_3d_object(vertices_2d, edges,):
    points = []
    for start_idx, end_idx in edges:
        start = vertices_2d[start_idx]
        end = vertices_2d[end_idx]
        line_points = bresenham(int(start[0]), int(start[1]), 
                              int(end[0]), int(end[1]))
        points.extend(line_points)
    
    return points

# Função para desenhar a grade
def draw_grid():
    for i in range(-num_cells, num_cells + 2):
        pygame.draw.line(screen, GRAY, 
                        to_screen_coordinates(i, -(num_cells + 1)), 
                        to_screen_coordinates(i, num_cells))
        
    for i in range(-(num_cells + 1), num_cells + 1):  
        pygame.draw.line(screen, GRAY, 
                        to_screen_coordinates(-num_cells, i),
                        to_screen_coordinates(num_cells + 1, i))