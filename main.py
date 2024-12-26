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

#open connection to ev3
conn = rpyc.classic.connect("ev3dev")

print("Connected to EV3")

#intialize motors
ev3dev2_motor = conn.modules['ev3dev2.motor']

left_motor = ev3dev2_motor.LargeMotor(ev3dev2_motor.OUTPUT_A)
right_motor = ev3dev2_motor.LargeMotor(ev3dev2_motor.OUTPUT_D)
print("Connected drive motors")

#max speed value for large motors
speed = 1050

def apply_dead_zone(value, dead_zone=0.1):
    if abs(value) < dead_zone:
        return 0.0
    return value

# main loop
try:
  while True:
      # force pygame to process input
      pygame.event.pump()
      # Debug joystick axis values
      #for i in range(joystick.get_numaxes()):
      #  print(f"Axis {i}: {joystick.get_axis(i):.2f}")

      # axis numbers are for xbox series x controller
      left_stick_y = apply_dead_zone(joystick.get_axis(1) * -1)
      right_stick_y = apply_dead_zone(joystick.get_axis(3) * -1)
      



      left_speed = speed * left_stick_y
      right_speed = speed * right_stick_y

      left_motor.run_forever(speed_sp=int(left_speed))
      right_motor.run_forever(speed_sp=int(right_speed))
      # debug speed
      print(f"Left speed: {left_speed:.2f}, Right Stick Y: {right_speed:.2f}")

      # delay for pygame cpu usage
      pygame.time.wait(10)

finally:
    # clean up
    joystick.quit()
    pygame.quit()
