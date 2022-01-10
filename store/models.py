from django.db import models
from django.urls import reverse


class Keeper(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'keeper'
        verbose_name_plural = 'keeper'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:tool_list_by_keeper',
                       args=[self.slug])


class Tool(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='tools/%Y/%m/%d',
                              blank=True)
    keeper = models.ForeignKey(Keeper, on_delete=models.CASCADE,
                               related_name='keeper')
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:tool_detail',
                       args=[self.id, self.slug])


class Operation(models.Model):
    giver = models.ForeignKey(Keeper,
                              related_name='giver',
                              on_delete=models.CASCADE)
    taker = models.ForeignKey(Keeper,
                              related_name='taker',
                              on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'operation'
        verbose_name_plural = 'operations'
