import cv2
import numpy as np
from scipy.ndimage import gaussian_filter

def deformacion_elastica(ruta_imagen, ruta_salida, alpha=30, sigma=8, seed=None):
    """
    Aplica una deformación elástica suave a una imagen.
    
    Parámetros:
    - ruta_imagen: Ruta de la imagen de entrada.
    - ruta_salida: Ruta donde se guardará la imagen modificada.
    - alpha: Magnitud de la deformación (en píxeles). Valores típicos: 20-50.
             Valores muy altos distorsionan demasiado las letras.
    - sigma: Suavidad de la deformación (en píxeles). Valores típicos: 5-10.
             Valores altos = deformación muy suave y global.
             Valores bajos = deformación más local y ondulada.
    - seed: Semilla aleatoria para reproducibilidad (opcional).
    """
    
    # Establecer semilla si se proporciona (útil para reproducir resultados)
    if seed is not None:
        np.random.seed(seed)
    
    # 1. Leer la imagen
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen en {ruta_imagen}")
        return
    
    alto, ancho = imagen.shape[:2]
    print(f"Dimensiones de la imagen: {ancho}x{alto}")
    print(f"Parámetros: alpha={alpha}, sigma={sigma}")

    # 2. Generar campos de desplazamiento aleatorios
    # dx: desplazamiento en el eje X
    # dy: desplazamiento en el eje Y
    dx = np.random.uniform(-1, 1, (alto, ancho)).astype(np.float32) * alpha
    dy = np.random.uniform(-1, 1, (alto, ancho)).astype(np.float32) * alpha

    # 3. Suavizar los campos con un filtro gaussiano
    # Esto es lo que hace que la deformación sea "elástica" y no ruido puro
    dx = gaussian_filter(dx, sigma=sigma, mode="constant", cval=0)
    dy = gaussian_filter(dy, sigma=sigma, mode="constant", cval=0)

    # 4. Crear las mallas de coordenadas (grid) para el mapeo
    x, y = np.meshgrid(np.arange(ancho), np.arange(alto))
    
    # 5. Aplicar los desplazamientos a las coordenadas originales
    # map_x: coordenada X de origen para cada píxel del destino
    # map_y: coordenada Y de origen para cada píxel del destino
    map_x = (x + dx).astype(np.float32)
    map_y = (y + dy).astype(np.float32)

    # 6. Aplicar la transformación con cv2.remap
    # INTER_CUBIC mantiene buena calidad en texto
    # BORDER_REPLICATE rellena los bordes con el color del píxel más cercano
    imagen_deformada = cv2.remap(
        imagen,
        map_x,
        map_y,
        interpolation=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    # 7. Guardar el resultado
    cv2.imwrite(ruta_salida, imagen_deformada)
    print(f"Imagen guardada en: {ruta_salida}")

    # Opcional: Mostrar comparación
    # cv2.imshow('Original', imagen)
    # cv2.imshow('Deformacion Elastica', imagen_deformada)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


# --- Ejecución ---
if __name__ == "__main__":
    archivo_entrada = "word.png"
    archivo_salida = "word_elastico.png"
    
    # Llamar a la función con parámetros suaves
    # alpha=30: desplazamiento máximo de 30 píxeles
    # sigma=8: deformación muy suave (ideal para no romper las letras)
    deformacion_elastica(archivo_entrada, archivo_salida, alpha=30, sigma=8)