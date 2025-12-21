import time
import pygame
import rpyc

# Initialize Pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Check for connected joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    pygame.quit()
    exit()

# Open the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Connected to joystick: {joystick.get_name()}")

# open connection to ev3
conn = rpyc.classic.connect("ev3dev")

print("Connected to EV3")

# intialize speaker
ev3dev2_sound = conn.modules["ev3dev2.sound"]

sound = ev3dev2_sound.Sound()
print("Connected to speaker")
sound.volume = 100

# inititialize lights
ev3dev2_led = conn.modules["ev3dev2.led"]
leds = ev3dev2_led.Leds()
print("Connected to lights")

#initialize power
ev3dev2_power = conn.modules["ev3dev2.power"]
power = ev3dev2_power.PowerSupply()
print("Connected to power")

# intialize motors
ev3dev2_motor = conn.modules["ev3dev2.motor"]

left_motor = ev3dev2_motor.LargeMotor(ev3dev2_motor.OUTPUT_A)
right_motor = ev3dev2_motor.LargeMotor(ev3dev2_motor.OUTPUT_D)
print("Connected drive motors")

# max speed value for large motors
speed = 1050


def apply_dead_zone(value, dead_zone=0.1):
    if abs(value) < dead_zone:
        return 0.0
    return value


# main loop
try:
    last_time = time.time()
    a_button_pressed = False  # Track button state to avoid 
    print("Starting main loop")
    while True:
        
        # force pygame to process input
        pygame.event.pump()

        # Check for X button press (button 0 on Xbox controller)
        current_a_button = joystick.get_button(0)
        if current_a_button and not a_button_pressed:
            print("Hello there")
            left_motor.run_forever(speed_sp=0)
            right_motor.run_forever(speed_sp=0)
            leds.set_color("LEFT", "RED")
            leds.set_color("RIGHT", "RED")
            sound.speak("Hello there!")
            a_button_pressed = True

        elif not current_a_button:
            a_button_pressed = False
            leds.set_color("LEFT", "GREEN")
            leds.set_color("RIGHT", "GREEN")
        # Debug joystick axis values
        # for i in range(joystick.get_numaxes()):
        #  print(f"Axis {i}: {joystick.get_axis(i):.2f}")

        # axis numbers are for xbox series x controller
        left_stick_y = apply_dead_zone(joystick.get_axis(1) * -1)
        right_stick_y = apply_dead_zone(joystick.get_axis(3) * -1)

        # print(f"Left Stick Y: {left_stick_y:.2f}, Right Stick Y: {right_stick_y:.2f}")

        left_speed = speed * left_stick_y
        right_speed = speed * right_stick_y

        left_motor.run_forever(speed_sp=int(left_speed))
        right_motor.run_forever(speed_sp=int(right_speed))
        # debug speed
        # print(f"Left speed: {left_speed:.2f}, Right Stick Y: {right_speed:.2f}")

        # delay for pygame cpu usage
        #print(f"Delta: {time.time() - last_time:.2f}")
        
        voltage = power.measured_volts
        amps = power.measured_amps
        watts = voltage * amps
        print(f"Power: {watts:.2f}W")

        last_time = time.time()
        pygame.time.wait(10)

finally:
    # clean up
    joystick.quit()
    pygame.quit()
