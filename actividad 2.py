from experta import*

# Definimos los hechos (Facts)
class Ruta(Fact):
    """Representa una ruta entre dos puntos."""
    pass

class Solicitud(Fact):
    """Representa una solicitud de ruta óptima."""
    pass

# Definimos el motor de inferencia
class SistemaRutas(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.mejor_ruta = None

    # Regla para buscar rutas directas
    @Rule(Solicitud(origen=MATCH.origen, destino=MATCH.destino),
          Ruta(origen=MATCH.origen, destino=MATCH.destino, tiempo=MATCH.tiempo))
    def ruta_directa(self, origen, destino, tiempo):
        self.mejor_ruta = f"La mejor ruta es directa desde {origen} hasta {destino}. Tiempo estimado: {tiempo} minutos."

    # Regla para buscar rutas con transbordo
    @Rule(Solicitud(origen=MATCH.origen, destino=MATCH.destino),
          Ruta(origen=MATCH.origen, destino=MATCH.transbordo, tiempo=MATCH.tiempo1),
          Ruta(origen=MATCH.transbordo, destino=MATCH.destino, tiempo=MATCH.tiempo2))
    def ruta_con_transbordo(self, origen, destino, transbordo, tiempo1, tiempo2):
        tiempo_total = tiempo1 + tiempo2
        self.mejor_ruta = (f"La mejor ruta incluye un transbordo en {transbordo}. "
                           f"Tiempo total estimado: {tiempo_total} minutos.")

    # Regla para manejar casos sin rutas disponibles
    @Rule(Solicitud(origen=MATCH.origen, destino=MATCH.destino),
          NOT(Ruta(origen=MATCH.origen, destino=MATCH.destino)))
    def sin_ruta(self, origen, destino):
        self.mejor_ruta = f"No hay rutas disponibles desde {origen} hasta {destino}."

# Configuración de datos
def cargar_rutas(engine):
    """Carga las rutas en la base de conocimiento."""
    engine.declare(Ruta(origen="A", destino="B", tiempo=10))
    engine.declare(Ruta(origen="B", destino="C", tiempo=15))
    engine.declare(Ruta(origen="A", destino="D", tiempo=20))
    engine.declare(Ruta(origen="D", destino="C", tiempo=10))
    # Agrega más rutas según sea necesario

# Ejecución del sistema
def main():
    sistema = SistemaRutas()
    sistema.reset()  # Resetea el motor de inferencia
    cargar_rutas(sistema)

    # Solicita una ruta al sistema
    origen = input("Ingrese el punto de origen: ")
    destino = input("Ingrese el punto de destino: ")
    sistema.declare(Solicitud(origen=origen, destino=destino))
    sistema.run()  # Ejecuta las reglas

    if sistema.mejor_ruta:
        print(sistema.mejor_ruta)
    else:
        print("No se pudo determinar una ruta.")

if __name__ == "__main__":
    main()
