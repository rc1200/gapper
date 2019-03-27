from django.db import models


class Carousel(models.Model):
    heading = models.CharField(max_length=200)
    carousel_num = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, width_field='width_field', height_field='height_field')
    height_field = models.IntegerField(default=0, null=True, blank=True)
    width_field = models.IntegerField(default=0, null=True, blank=True)
    is_active = models.CharField(max_length=10, null=True, blank=True)
    text = models.TextField()
    text_align = models.CharField(max_length=20, default='text-right', null=True, blank=True)
    button_text = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '{} : {} : {}'.format(str(self.carousel_num), self.is_active, self.heading)


class ContactMe(models.Model):
    senderEmail = models.EmailField('Your Email', max_length=70)
    message = models.TextField()
