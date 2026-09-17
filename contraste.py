import cv2
import numpy as np
import random

def cambiar_contraste_aleatorio(ruta_imagen, ruta_salida, rango_contraste=(0.7, 1.3), rango_brillo=(-20, 20)):
    """
    Aplica un cambio de contraste y brillo aleatorio a una imagen.
    
    Parámetros:
    - ruta_imagen: Ruta de la imagen de entrada.
    - ruta_salida: Ruta donde se guardará la imagen modificada.
    - rango_contraste: Tupla (min, max) para el factor de contraste. 
                       1.0 es el original. <1.0 disminuye, >1.0 aumenta.
    - rango_brillo: Tupla (min, max) para el valor de brillo a sumar/restar.
                    Valores negativos oscurecen, positivos aclaran.
    """
    
    # 1. Leer la imagen
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen en {ruta_imagen}")
        return

    # 2. Generar valores aleatorios
    # alpha controla el contraste (1.0 = sin cambios)
    alpha = random.uniform(rango_contraste[0], rango_contraste[1])
    # beta controla el brillo (0 = sin cambios)
    beta = random.uniform(rango_brillo[0], rango_brillo[1])
    
    print(f"Factor de contraste (alpha): {alpha:.2f}")
    print(f"Valor de brillo (beta): {beta:.2f}")

    # 3. Aplicar la transformación
    # La fórmula es: nueva_imagen = alpha * imagen_original + beta
    # cv2.convertScaleAbs se asegura de que los valores se mantengan en el rango 0-255
    # y convierte el resultado a valores absolutos de 8 bits.
    imagen_ajustada = cv2.convertScaleAbs(imagen, alpha=alpha, beta=beta)

    # 4. Guardar el resultado
    cv2.imwrite(ruta_salida, imagen_ajustada)
    print(f"Imagen guardada en: {ruta_salida}")

    # Opcional: Mostrar comparación
    # cv2.imshow('Original', imagen)
    # cv2.imshow('Contraste Aleatorio', imagen_ajustada)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# --- Ejecución ---
if __name__ == "__main__":
    # Reemplaza estos nombres con los de tu archivo real
    archivo_entrada = "word.png" 
    archivo_salida = "word_contraste.png"
    
    # Llamar a la función
    # Un rango de contraste de 0.7 a 1.3 significa que puede reducir el contraste un 30% o aumentarlo un 30%
    cambiar_contraste_aleatorio(archivo_entrada, archivo_salida, rango_contraste=(0.7, 1.3), rango_brillo=(-15, 15))