from django.db import models


class Departments(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Managers(models.Model):
    username = models.CharField(max_length=150, default='asdf')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    city = models.CharField(max_length=150, default='Moscow', null=True)
    region = models.CharField(max_length=150, default='Moscow province', null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=150, null=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True)


class Clients(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Tasks(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    manager = models.ForeignKey(Managers, on_delete=models.CASCADE)

    class Meta:
        ordering = ['is_completed']


class Products(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Sales(models.Model):
    sale_time = models.TimeField()
    sale_date = models.DateField()
    manager = models.ForeignKey(Managers, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, through='Products_sale', related_name='prdcts')


class Products_sale(models.Model):
    sales = models.ForeignKey('Sales', on_delete=models.CASCADE)
    products = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('products', 'sales'), name='once_per_product_sale')
        ]
