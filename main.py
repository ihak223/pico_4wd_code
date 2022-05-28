import pico_4wd as car
import time

STOP_PROX = 40   # Proximity to object needed to cause a halt
TURN_DIV  = 1000 # Divisor for the turn

def op_radar():
    '''
    Operates servo and proximity detector
    '''
    right_readings = [] # of readings from the right scan
    left_readings  = [] # collection of readings from the left scan
    
    angles = [0, 45]    # angles to scan at
    
    # right scan
    for angle in angles:
        left_readings.append(car.get_radar_distance_at(angle)*angle)     # gets angle at left (positive)
        time.sleep(0.25)
        right_readings.append(car.get_radar_distance_at(angle*-1)*angle) # gets angle at right (negative)
        time.sleep(0.25)
        
    front = car.get_radar_distance_at(0) # gets front stop
    
    # returns average
    return sum(left_readings)/len(left_readings), sum(right_readings)/len(right_readings), front
        
blocked = False
while not blocked:
    car.set_light_rear_color([0, 100, 100])
    l, r, f = op_radar()
    dif = abs(l-r)/TURN_DIV
    print(f'dif: {dif}')
    if f < STOP_PROX:
        blocked = True
        print(f)
    if l > r:
        print('l')
        car.set_motor_power(-20/dif, 20/dif, -20/dif, 20/dif)
        car.set_light_bottom_left_color([255, 0, 100])
        print('l')
    elif r > l:
        print('r')
        car.set_motor_power(20/dif, -20/dif, 20/dif, -20/dif)
        car.set_light_bottom_right_color([255, 0, 100])
        print('r')
    else:
        print('e')
    
    time.sleep(0.9)
    car.set_light_bottom_color([0, 100, 100])
    car.set_light_rear_color([255, 255, 0])
    car.set_motor_power(70, 70, 70, 70)
    
car.stop()
car.set_light_off()