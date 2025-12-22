import multiprocessing as mp
from multiprocessing.managers import SyncManager
import time

# Librerías Propias
from clases import Robot, Controlable_Robot, Ball
from Field_process import Get_Field_Data
from Server_process import server_process
from State_process import StateMachine

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

        controller_p = mp.Process(target=StateMachine, args=(robots_shared, ball_shared,))
        controller_p.start()

        server_p = mp.Process(target=server_process, args=(robots_shared,))
        server_p.start()
        
        vision_p = mp.Process(target=Get_Field_Data, args=(robots_shared, ball_shared,))
        vision_p.start()

        print("--- Monitor de Datos Iniciado ---")
        try:
            while vision_p.is_alive():
                b_pos = ball_shared.get_position()
                
                if 0 in robots_shared:
                    r0 = robots_shared[0]
                    r0_pos = r0.get_pos()
                    r0_ang = r0.get_angle()
                    # print(f"Bola: {b_pos} | Robot 0: {r0_pos} @ {r0_ang}°")
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Finalizando...")
            vision_p.terminate()
            controller_p.terminate()
            server_p.terminate()