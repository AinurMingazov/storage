from django.db import models
from django.urls import reverse


class Keeper(models.Model):
    """Модель описывает владельца товара"""
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=50, unique=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'keeper'
        verbose_name_plural = 'keepers'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:tool_list_by_keeper',
                       args=[self.slug])


class Category(models.Model):
    """Модель для разбивает товары по категориям"""
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=50, unique=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:tool_list_by_category',
                       args=[self.slug])


class Tool(models.Model):
    """Модель описывает товар"""
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='tools/%Y/%m/%d',
                              blank=True)
    keeper = models.ForeignKey(Keeper, on_delete=models.SET_NULL,
                               related_name='keeper', null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='category', null=True)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:tool_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('name',)


class Operation(models.Model):
    """Модель описывает перемещения товара"""
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
        ordering = ('-created',)
        verbose_name = 'operation'
        verbose_name_plural = 'operations'
