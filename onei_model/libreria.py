import jpype

# Inicia la JVM
jpype.startJVM()

print("JPype se ha instalado y la JVM se ha iniciado correctamente.")

# Detén la JVM
jpype.shutdownJVM()
