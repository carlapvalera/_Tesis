from fireworks import Firework, Workflow, LaunchPad

# Configura tu API Key
api_key = "fw_3ZXb6WWaLuUNnJZnvXWTwEY2"
launchpad = LaunchPad()

# Define una tarea simple (puedes reemplazar esto con una tarea real)
def simple_task():
    print("Esta es una tarea simple.")

# Crea un Firework
fw = Firework(simple_task, name="Simple Task")

# Agrega el Firework al LaunchPad
launchpad.add_fw(fw)

print("Firework agregado con éxito.")