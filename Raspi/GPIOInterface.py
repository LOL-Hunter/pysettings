import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class Mode:
    BOARD = GPIO.BOARD
    BCM = GPIO.BCM

class Interface:
    def __init__(self):
        pass
    @staticmethod
    def setWarnings(b):
        GPIO.setwarnings(b)
    @staticmethod
    def setBoardMode(mode=Mode.BOARD):
        GPIO.setmode(mode)


class _Pin:
    def __init__(self, pin, mode, initial=0):
        self._pin = pin
        GPIO.setup(pin, mode, initial=initial)
    def cleanup(self):
        GPIO.cleanup(self._pin)
    def cleanupAll(self):
        GPIO.cleanup()


class PinOut(_Pin):
    def __init__(self, pin, initial=0):
        super().__init__(pin, GPIO.OUT, initial)
    def setLow(self):
        GPIO.output(self._pin, 0)
    def setHigh(self):
        GPIO.output(self._pin, 1)
    def setState(self, s):
        GPIO.output(self._pin, s)

class Pwm:
    def __init__(self, freq = 50, initial=0):
        self._pin = PinOut(18)

        self._pwm = GPIO.PWM(12, freq)
        self._pwm.start(50)
    def setDutyCycle(self, d):
        self._pwm.ChangeDutyCycle(d)
    def stop(self):
        self._pwm.stop()
    def setFreq(self, f):
        self._pwm.ChangeFrequency(f)


class PinIn(_Pin):
    def __init__(self, pin, initial=0):
        super().__init__(pin, GPIO.IN, initial)
    def getState(self):
        return bool(GPIO.input(self._pin))


