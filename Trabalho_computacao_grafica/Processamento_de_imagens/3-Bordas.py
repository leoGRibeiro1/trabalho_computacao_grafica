# Alunos: Leandro Marcos Pinheiro Souza - 201911140007 / Leonardo Gouvêa Ribeiro - 202111140015

import cv2
import matplotlib.pyplot as plt
import numpy as np

# Inserir imagem
imagem = cv2.imread(r"C:\\Users\\leand\\Desktop\\Processamento de Imagem\\imagem.jpg", cv2.IMREAD_GRAYSCALE) # Alterar caminho da imagem

# Filtro Sobel
sobel_x = cv2.Sobel(imagem, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(imagem, cv2.CV_64F, 0, 1, ksize=3)
sobel = cv2.magnitude(sobel_x, sobel_y)

# Filtro Prewitt
filtro_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=int)
filtro_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
prewitt_x = cv2.filter2D(imagem, cv2.CV_32F, filtro_x)
prewitt_y = cv2.filter2D(imagem, cv2.CV_32F, filtro_y)
prewitt = cv2.magnitude(prewitt_x, prewitt_y)

# Filtro Canny
bordas_canny = cv2.Canny(imagem, 100, 200)

# Exibir imagens
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.imshow(imagem, cmap='gray')
plt.title('Imagem Original')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(sobel, cmap='gray')
plt.title('Sobel')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(prewitt, cmap='gray')
plt.title('Prewitt')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(bordas_canny, cmap='gray')
plt.title('Canny')
plt.axis('off')

plt.show()
