import Rpi.GPIO as GPIO



class Raspi:
    @staticmethod
    def getRam():
        return GPIO.RPI_INFO["RAM"]

    @staticmethod
    def getProcessor():
        return GPIO.RPI_INFO["PROCESSOR"]

    @staticmethod
    def getRevision():
        return GPIO.RPI_INFO["REVISION"]

    @staticmethod
    def getType():
        return GPIO.RPI_INFO["TYPE"]

