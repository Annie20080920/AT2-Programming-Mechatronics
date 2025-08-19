import machine
import utime
import random

class ReactionGame:
    def __init__(self, led_pin, left_button_pin, right_button_pin, servo_arm):
        self.led = machine.Pin(led_pin, machine.Pin.OUT)
        self.left_button = machine.Pin(left_button_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.right_button = machine.Pin(right_button_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.servo_arm = servo_arm

        self.reaction_time_left = -1
        self.reaction_time_right = -1
        self.timer_start = 0
        self.fastest_button = None

    def button_handler(self, pin):
        """IRQ handler for button presses"""
        if self.fastest_button is None:
            self.fastest_button = pin
            reaction = utime.ticks_diff(utime.ticks_ms(), self.timer_start)
            self.servo_arm.show_score(reaction)

            if pin == self.left_button:
                self.reaction_time_left = reaction
                print(f"Left player's reaction time: {reaction} ms")
            elif pin == self.right_button:
                self.reaction_time_right = reaction
                print(f"Right player's reaction time: {reaction} ms")

            # Disable further interrupts
            self.left_button.irq(handler=None)
            self.right_button.irq(handler=None)

    def play_turn(self, player):
        """Run one player's turn"""
        self.fastest_button = None
        print(f"\n Player {player}, get ready...")
        self.led.value(0)
        self.servo_arm.reset()
        utime.sleep(random.uniform(2, 5))

        print("GO!")
        self.led.value(1)
        self.timer_start = utime.ticks_ms()

        if player == "Left":
            self.left_button.irq(trigger=machine.Pin.IRQ_RISING, handler=self.button_handler)
        elif player == "Right":
            self.right_button.irq(trigger=machine.Pin.IRQ_RISING, handler=self.button_handler)

        while self.fastest_button is None:
            utime.sleep(0.01)

        self.led.value(0)
        utime.sleep(2)  # Show score for 2 seconds

    def run(self):
        """Run the full 2-player game"""
        self.play_turn("Left")
        self.play_turn("Right")

        print("\n Game Result:")
        print(f"Left Player:  {self.reaction_time_left} ms")
        print(f"Right Player: {self.reaction_time_right} ms")

        if self.reaction_time_left > 0 and self.reaction_time_right > 0:
            if self.reaction_time_left < self.reaction_time_right:
                print(" Left Player wins!")
            elif self.reaction_time_right < self.reaction_time_left:
                print(" Right Player wins!")
            else:
                print(" It's a tie!")
        else:
            print(" One or both players didn’t press their button!")
