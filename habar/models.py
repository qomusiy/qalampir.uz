from django.db import models

# Create your models here.



class Bolim(models.Model):
    name = models.CharField(max_length=150)
    is_avtive = models.BooleanField()

    def __str__(self):
        return self.name
    
class Habar(models.Model):
    title = models.CharField(max_length=100)
    mindef = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    view = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='habar_img', default='habar_img/default.jpg')
    bolim = models.ForeignKey(Bolim, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, {self.bolim.name}"

class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sponsor_img/')
    is_active = models.BooleanField()

    def __str__(self):
        return self.name
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    view = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Contacts"
        ordering = ['view']

    def __str__(self):
        return f"{self.name} - {self.email}"