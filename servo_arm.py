import machine

class ServoArm:
    def __init__(self, pin_num):
        self.servo = machine.PWM(machine.Pin(pin_num))
        self.servo.freq(50)
        self.min_us = 500
        self.max_us = 2500

    def set_angle(self, angle):
        us = self.min_us + (self.max_us - self.min_us) * angle / 180
        duty = int(us / 20000 * 65535)
        self.servo.duty_u16(duty)

    def show_score(self, reaction_time_ms):
        clamped = min(max(reaction_time_ms, 100), 1000)
        angle = 180 - (clamped - 100) / 5
        angle = max(0, min(180, int(angle)))
        self.set_angle(angle)

    def reset(self):
        self.set_angle(0)