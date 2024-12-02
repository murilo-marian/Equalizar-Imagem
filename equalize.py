import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

def obterBits(img):
    modos_bits = {
        "1": 1,        # 1 bit por pixel
        "L": 8,        # 8 bits (escala de cinza)
        "P": 8,        # 8 bits (paleta)
        "RGB": 24,     # 3 canais * 8 bits (24 bits)            "RGBA": 32,    # 4 canais * 8 bits (32 bits)
        "CMYK": 32     # 4 canais * 8 bits (32 bits)
    }
    bits_por_pixel = modos_bits.get(img.mode, None)
    if bits_por_pixel is None:
        return f"Modo não reconhecido: {img.mode}"
    return bits_por_pixel

def calcularHistograma(bits, img):
    print(len(img))
    histograma = [0] * bits  
    for linha in img:
        for pixel in linha:
            histograma[pixel] += 1  #cada ocorrência aumenta a frequência
    return histograma

def calcularProbabilidade(histograma, totalPixels):
    return [freq / totalPixels for freq in histograma]

def calcularAcumulado(probabilidades):
    acumulado = [0] * len(probabilidades)
    acumulado[0] = probabilidades[0]
    for i in range(1, len(probabilidades)):
        acumulado[i] = acumulado[i - 1] + probabilidades[i]
    return acumulado

def calcularTransformação(acumulado, bits):
    return [round((bits - 1) * valor) for valor in acumulado]
    
def aplicarTransformacao(img, transformacao):
    nova_img = []
    for linha in img:
        nova_linha = [transformacao[pixel] for pixel in linha]
        nova_img.append(nova_linha)
    return nova_img

def equalizar_histograma(img, nomeImagem):
    imgArray = np.array(img)
    largura, altura = img.size
    total_pixels = largura * altura  # Total de pixels na imagem
    bits = 2 ** obterBits(img)
    histograma = calcularHistograma(bits, imgArray)
    probabilidades = calcularProbabilidade(histograma, total_pixels)
    acumulado = calcularAcumulado(probabilidades)
    transformacao = calcularTransformação(acumulado, bits)
    nova_img = aplicarTransformacao(imgArray, transformacao)
    salvarImagem(nova_img, nomeImagem)

def salvarImagem(array, nomeArquivo):
    arraynp = np.array(array, dtype=np.uint8)
    img = Image.fromarray(arraynp, mode="L")
    img.save(nomeArquivo)
    
    
img1 = Image.open('Fig0316(1)(top_left).tif')
img2 = Image.open('Fig0316(2)(2nd_from_top).tif')
img3 = Image.open('Fig0316(3)(third_from_top).tif')
img4 = Image.open('Fig0316(4)(bottom_left).tif')
img1Array = np.array(img1)
img2Array = np.array(img2)
img3Array = np.array(img3)
img4Array = np.array(img4)

equalizar_histograma(img1, "1.tif")
equalizar_histograma(img2, "2.tif")
equalizar_histograma(img3, "3.tif")
equalizar_histograma(img4, "4.tif")