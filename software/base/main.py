import multiprocessing as mp
from multiprocessing.managers import SyncManager
import time

# Librerías Propias
from clases import Robot, Controlable_Robot, Ball
from Field_process import Get_Field_Data
from Server_process import server_process
from State_process import StateMachine
from Keyboard_process import keyboard_process

# Configuramos el Manager para exponer los métodos
class SoccerManager(SyncManager): pass

# Registramos indicando qué métodos queremos que sean accesibles (incluyendo los nuevos getters)
SoccerManager.register('Robot', Robot)
SoccerManager.register('Controlable_Robot', Controlable_Robot)
SoccerManager.register('Ball', Ball)

if __name__ == "__main__":
    # Necesario en Windows para evitar bucles infinitos de procesos
    mp.freeze_support()
    
    with SoccerManager() as manager:
        # Creamos los objetos dentro del manager
        robots_shared = manager.dict({
            0: manager.Controlable_Robot(0, True),
            1: manager.Robot(1, False)
        })
        ball_shared = manager.Ball()

        # Control (Manual o Autónomo) -> que velocidades enviar
        # controller_p = mp.Process(target=StateMachine, args=(robots_shared, ball_shared,))    
        controller_p = mp.Process(target=keyboard_process, args=(robots_shared,))
        controller_p.start()

        # Redes -> coneccion entre robots y pc
        server_p = mp.Process(target=server_process, args=(robots_shared,))
        server_p.start()
        
        # Percepción -> obtener posiciones de robots y pelota
        vision_p = mp.Process(target=Get_Field_Data, args=(robots_shared, ball_shared,))
        vision_p.start()

        print("--- Monitor de Datos Iniciado ---")
        try:
            while vision_p.is_alive():
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("Finalizando...")
            vision_p.terminate()
            controller_p.terminate()
            server_p.terminate()