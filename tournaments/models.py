from django.db import models

class Tournament(models.Model):
    name = models.CharField(max_length=250)
    is_open = models.BooleanField(default=False)
    golf_course = models.CharField(max_length=250)
    entry_fee = models.IntegerField()
    start_date = models.DateField()
    number_of_pools = models.IntegerField()
    day_one_score_count = models.IntegerField(blank=True)
    day_two_score_count = models.IntegerField(blank=True)
    day_three_score_count = models.IntegerField(blank=True)
    day_four_score_count = models.IntegerField(blank=True)

    def __str__(self):
        return self.name + ' ' + str(self.start_date)

    def start_date_year(self):
        return self.start_date.strftime('%Y')
