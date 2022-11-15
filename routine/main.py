from automated_routine import automated_routine
from manual_routine import manual_routine

if __name__ == '__main__':
    while True:
        routine = input('"Manual" or "Automated" routine: ')
        if routine == 'Manual':
            manual_routine()
        elif routine == 'Automated':
            automated_routine()
        else:
            print('Exiting program.')
            # Should have a way to "e-stop" the arms from the code (throuh modbus?) to stop arms without hitting the e-stop which damages the arms? On the teach pendant theres some function that stops it in a better way
            break


    