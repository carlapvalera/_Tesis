import numpy as np

def centered_kernel(X):
    """Calcula el kernel centrado para una matriz de embeddings X."""
    n = X.shape[0]
    # Calcular la matriz de similitud (producto interno)
    K = np.dot(X, X.T)
    
    # Centrar la matriz
    one_n = np.ones((n, n)) / n
    K_centered = K - one_n @ K - K @ one_n + one_n @ K @ one_n
    
    return K_centered

def hsic(K, L):
    """Calcula el Hilbert-Schmidt Independence Criterion (HSIC) entre dos matrices de kernel."""
    n = K.shape[0]
    
    # Calcular el producto de las matrices centradas
    return np.trace(np.dot(K, L)) / (n * n)

def cka(X, Y):
    """Calcula el Centered Kernel Alignment (CKA) entre dos conjuntos de embeddings X e Y."""
    # Calcular los kernels centrados
    K_X = centered_kernel(X)
    K_Y = centered_kernel(Y)
    
    # Calcular HSIC
    hsic_value = hsic(K_X, K_Y)
    
    # Normalizar con HSIC de cada conjunto
    norm_X = np.sqrt(hsic(K_X, K_X))
    norm_Y = np.sqrt(hsic(K_Y, K_Y))
    
    # CKA
    cka_value = hsic_value / (norm_X * norm_Y)
    
    return cka_value

# Ejemplo de uso
if __name__ == "__main__":
    # Crear dos conjuntos de embeddings aleatorios
    np.random.seed(0)
    embeddings_A = np.random.rand(10, 5)  # 10 muestras, 5 dimensiones
    embeddings_B = np.random.rand(10, 5)  # 10 muestras, 5 dimensiones

    # Calcular CKA entre los dos conjuntos
    cka_score = cka(embeddings_A, embeddings_B)
    
    print(f"CKA Score: {cka_score}")

