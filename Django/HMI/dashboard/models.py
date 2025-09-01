from django.db import models

class Datalog(models.Model):
    TIMESTAMP = models.DateTimeField(verbose_name="TimeStamp", primary_key=True)
    SERVO_MOTOR_RAW = models.IntegerField(verbose_name="Servo Motor Reading")
    SERVO_MOTOR_SCA = models.FloatField(verbose_name="Servo Motor Angle")
    SERVO_RAW = models.IntegerField(verbose_name="Sensor Reading")
    SERVO_SCA = models.FloatField(verbose_name="Sensor Distance")
    ARDUINO_RPI_STATUS = models.BooleanField(verbose_name="Serial Connection Status")
    ARDUINO_STATUS = models.BooleanField(verbose_name="Status Arduino")
    RPI_STATUS = models.BooleanField(verbose_name="Status Raspberry")
    
    def __str__(self):
        # Corrija esta linha para retornar o TIMESTAMP, que é um campo real.
        return str(self.TIMESTAMP)