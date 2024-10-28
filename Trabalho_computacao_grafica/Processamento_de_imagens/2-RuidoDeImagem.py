# Alunos: Leandro Marcos Pinheiro Souza - 201911140007 / Leonardo Gouvêa Ribeiro - 202111140015

import cv2
import numpy as np
from matplotlib import pyplot as plt

# Imagem
imagem = cv2.imread(r'C:\\Users\\leand\\Desktop\\Processamento de Imagem\\imagem2.BMP', cv2.IMREAD_GRAYSCALE) # Alterar caminho da imagem

# Filtro de média
filtro_media = cv2.blur(imagem, (5, 5))

# Filtro de mediana
filtro_mediana = cv2.medianBlur(imagem, 5)

# Filtro Gaussiano
filtro_gaussiano = cv2.GaussianBlur(imagem, (5, 5), 0)

# Resultados
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.title("Imagem Original")
plt.imshow(imagem, cmap='gray')

plt.subplot(2, 2, 2)
plt.title("Filtro de Média")
plt.imshow(filtro_media, cmap='gray')

plt.subplot(2, 2, 3)
plt.title("Filtro de Mediana")
plt.imshow(filtro_mediana, cmap='gray')

plt.subplot(2, 2, 4)
plt.title("Filtro Gaussiano")
plt.imshow(filtro_gaussiano, cmap='gray')

plt.tight_layout()
plt.show()
