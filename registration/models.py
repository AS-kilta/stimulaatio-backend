from django.db import models

class Registration(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    is_invited = models.BooleanField()
    ticket_type = models.CharField(max_length=100)
    sillis = models.BooleanField()
    table_company = models.CharField(max_length=100, blank=True, default="")
    avec = models.CharField(max_length=100, blank=True, default="")
    special_diet = models.CharField(max_length=200, blank=True, default="")
    menu_type = models.CharField(max_length=100)
    greeting = models.BooleanField()
    freshman_year = models.CharField(max_length=4, blank=True, default="")
    greeting_group = models.CharField(max_length=100, blank=True, default="")
    show_name = models.BooleanField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
