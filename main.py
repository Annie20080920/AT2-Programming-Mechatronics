from servo_arm import ServoArm
from reaction_game import ReactionGame

if __name__ == "__main__":
    servo_arm = ServoArm(pin_num=0)  # GP0 for servo
    game = ReactionGame(
        led_pin=15,          # LED on GP15
        left_button_pin=14,  # Left button on GP14
        right_button_pin=16, # Right button on GP16
        servo_arm=servo_arm
    )
    game.run()