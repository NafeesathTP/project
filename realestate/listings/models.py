from django.db import models

# Create your models here.
class Location(models.Model):
    city = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city},{self.State},{self.country}"

class PropertyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties')

    def __str__(self):
        return self.title