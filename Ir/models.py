from django.db import models
from rest_framework import serializers



class SensosrData(models.Model):

    device_id = models.CharField(
        max_length=50,
        help_text="Unique identifier for the IoT device."
    )
    temprature=models.FloatField(
        help_text="Temperature in celsius"

    )
    humidity=models.FloatField(
        help_text="Humidity in percentage"
    )
    smoke=models.FloatField(
        help_text="Smoke level in ppm"

    )
    Timestamp=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-Timestamp']
        verbose_name='Sensor Data'
        verbose_name_plural="Sensor Datas"
    def __str__(self):
        return f"{self.device_id} @ {self.Timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class SensorReading(models.Model):
    temprature = models.FloatField(
        help_text="Temperature in celsius"
    )
    humidity = models.FloatField(
        help_text="Humidity in percentage"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Sensor Reading'
        verbose_name_plural = "Sensor Readings"
    
    def __str__(self):
        return f"Reading @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"



class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model=SensorReading
        fields=['temprature', 'humidity']
        read_only_fields=['timestamp']

    def validate_temprature(self, value):
        if value < -10.0 or value > 50.0:
            raise serializers.ValidationError("Temperature is outside the expected range (-10C to 50C).")
        return value
    def validate_humidity(self, value):
        if value < 0.0 or value > 100.0:
            raise serializers.ValidationError("Humidity must be between 0% and 100%.")
        return value 


class EmailVerification(models.Model):
    user=models.ForeignKey('auth.User', on_delete=models.CASCADE)
    code=models.CharField(max_length=6)
    is_used=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)


# Create your models here.
