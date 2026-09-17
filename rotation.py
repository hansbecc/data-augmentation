import cv2
import numpy as np
import random
import math

def rotar_imagen_aleatoria(ruta_imagen, ruta_salida, angulo_min=-3.0, angulo_max=3.0):
    """
    Rota una imagen un ángulo aleatorio entre angulo_min y angulo_max.
    Ajusta el lienzo para que no se corten las esquinas y rellena con blanco.
    """
    
    # 1. Leer la imagen
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen en {ruta_imagen}")
        return

    # Obtener dimensiones
    alto, ancho = imagen.shape[:2]
    
    # 2. Generar ángulo aleatorio
    angulo = random.uniform(angulo_min, angulo_max)
    print(f"Ángulo de rotación aplicado: {angulo:.2f}°")

    # 3. Calcular el centro de la imagen
    centro = (ancho // 2, alto // 2)

    # 4. Obtener la matriz de rotación
    matriz_rotacion = cv2.getRotationMatrix2D(centro, angulo, 1.0)

    # 5. Calcular las nuevas dimensiones del lienzo para que no se corten las esquinas
    coseno = abs(matriz_rotacion[0, 0])
    seno = abs(matriz_rotacion[0, 1])
    
    nuevo_ancho = int((alto * seno) + (ancho * coseno))
    nuevo_alto = int((alto * coseno) + (ancho * seno))

    # 6. Ajustar la matriz de rotación para centrar la imagen en el nuevo lienzo
    matriz_rotacion[0, 2] += (nuevo_ancho / 2) - centro[0]
    matriz_rotacion[1, 2] += (nuevo_alto / 2) - centro[1]

    # 7. Aplicar la rotación
    # borderMode=cv2.BORDER_CONSTANT y borderValue=(255, 255, 255) rellena con blanco
    # Si tu documento es oscuro, cambia el borderValue a (0, 0, 0)
    imagen_rotada = cv2.warpAffine(
        imagen, 
        matriz_rotacion, 
        (nuevo_ancho, nuevo_alto), 
        flags=cv2.INTER_CUBIC, 
        borderMode=cv2.BORDER_CONSTANT, 
        borderValue=(255, 255, 255)
    )

    # 8. Guardar y/o mostrar el resultado
    cv2.imwrite(ruta_salida, imagen_rotada)
    print(f"Imagen guardada en: {ruta_salida}")

    # Opcional: Mostrar la imagen (presiona cualquier tecla para cerrar)
    # cv2.imshow('Imagen Original', imagen)
    # cv2.imshow('Imagen Rotada', imagen_rotada)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# --- Ejecución ---
if __name__ == "__main__":
    # Reemplaza estos nombres con los de tu archivo real
    archivo_entrada = "word.png" 
    archivo_salida = "word_rotado.png"
    
    # Llamar a la función
    rotar_imagen_aleatoria(archivo_entrada, archivo_salida)