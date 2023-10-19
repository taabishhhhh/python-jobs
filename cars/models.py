from django.db import models


# Maker Model.
# 1. name : String field

# 1. maker : String field : Foreign Key
# 2. car_name : String field
# 3. hpp : Int field
# 4. launch_date : Date field

class Maker(models.model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Car(models.Model):

    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    car_name = models.CharField(max_length=256)
    hpp = models.PositiveBigIntegerField(max_length=256)
    launch_date = models.DateField()

    def __str__(self):
        return self.name

