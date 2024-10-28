# Alunos: Leandro Marcos Pinheiro Souza - 201911140007 / Leonardo Gouvêa Ribeiro - 202111140015

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Converter imagem RGB para tons de cinza
def rgb_para_cinza(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

# Converter imagem tons de cinza para binária
def cinza_para_binaria(imagem, limite=127):
    _, imagem_binaria = cv2.threshold(imagem, limite, 255, cv2.THRESH_BINARY)
    return imagem_binaria

# Converter uma imagem binária para tons de cinza
def binaria_para_cinza(imagem):
    imagem_cinza = (imagem / 255) * 127  
    return imagem_cinza.astype(np.uint8)

# Converter imagem em tons de cinza para RGB
def cinza_para_rgb(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_GRAY2RGB)

# Converter imagem RGB para binária
def rgb_para_binaria(imagem, limite=127):
    imagem_cinza = rgb_para_cinza(imagem)
    return cinza_para_binaria(imagem_cinza, limite)

# Filtro média
def aplicar_filtro_media(imagem, tamanho_kernel=5):
    return cv2.blur(imagem, (tamanho_kernel, tamanho_kernel))

# Filtro mediana
def aplicar_filtro_mediana(imagem, tamanho_kernel=5):
    return cv2.medianBlur(imagem, tamanho_kernel)

# Filtro gaussiano
def aplicar_filtro_gaussiano(imagem, tamanho_kernel=5, sigma=1):
    return cv2.GaussianBlur(imagem, (tamanho_kernel, tamanho_kernel), sigma)

# Definir caminho da imagem
caminho_imagem = r"C:\Users\leand\Desktop\Processamento de Imagem\imagem.jpg"  # Alterar caminho da imagem
imagem = cv2.imread(caminho_imagem)
imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)  

# Conversão
imagem_cinza = rgb_para_cinza(imagem_rgb)
imagem_binaria = cinza_para_binaria(imagem_cinza)
imagem_cinza_convertida = binaria_para_cinza(imagem_binaria)
imagem_rgb_cinza = cinza_para_rgb(imagem_cinza)

# Exemplo de filtros
imagem_filtro_media = aplicar_filtro_media(imagem_cinza)
imagem_filtro_mediana = aplicar_filtro_mediana(imagem_cinza)
imagem_filtro_gaussiano = aplicar_filtro_gaussiano(imagem_cinza)

# Exibir imagens
plt.figure(figsize=(12, 8))

# Exibir imagem original
plt.subplot(2, 4, 1)
plt.imshow(imagem_rgb)
plt.title("Original")
plt.axis("off")

# Conversões
plt.subplot(2, 4, 2)
plt.imshow(imagem_cinza, cmap='gray')
plt.title("Cinza")
plt.axis("off")

plt.subplot(2, 4, 3)
plt.imshow(imagem_binaria, cmap='gray')
plt.title("Binária")
plt.axis("off")

plt.subplot(2, 4, 4)
plt.imshow(imagem_rgb_cinza)
plt.title("Cinza para RGB")
plt.axis("off")

# Filtros
plt.subplot(2, 4, 5)
plt.imshow(imagem_filtro_media, cmap='gray')
plt.title("Filtro Média")
plt.axis("off")

plt.subplot(2, 4, 6)
plt.imshow(imagem_filtro_mediana, cmap='gray')
plt.title("Filtro Mediana")
plt.axis("off")

plt.subplot(2, 4, 7)
plt.imshow(imagem_filtro_gaussiano, cmap='gray')
plt.title("Filtro Gaussiano")
plt.axis("off")

# Exibição
plt.tight_layout()
plt.show()
