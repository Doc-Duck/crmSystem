import time

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import Sales, Tasks, Managers
from django.db.models import Count, Case, When, CharField, Value, Sum, F
from django.db.models.functions import Concat, TruncDate, TruncTime
from .forms import *
import random
from django.forms import formset_factory
from datetime import date, datetime
from django.views.decorators.http import require_http_methods
from django.contrib import messages


def main(request):
    sales = Sales.objects.all().annotate(date=TruncTime('sale_time')).values('sale_date', 'manager__last_name',
                                                                             'client__last_name', 'date').annotate(
        sum=Sum(F('products_sale__quantity') * F('products__price')))
    # print(sales)
    task_form = TaskForm(request.POST)
    tasks = Tasks.objects.all().filter(manager__username=request.user.username).values('title', 'content',
                                                                                       'is_completed', 'id')
    order_form = OrderByForm(request.POST)
    current_user = request.user
    sales_count = Sales.objects.count()
    sales_per_manager = Sales.objects.all().select_related('manager').values('manager__first_name',
                                                                             'manager__department__name',
                                                                             'manager__last_name').annotate(
        total=Count('id')).annotate(sum=Sum(F('products_sale__quantity') * F('products__price'))).order_by(
        Case(When(manager__first_name=current_user.first_name, then=0), default=1),
        '-sum')
    radn_num = [[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for i in sales_per_manager]
    if request.method == "POST" and order_form.is_valid():
        radn_num = [[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for i in sales_per_manager]
        order_by = order_form.cleaned_data['order_by']
        sales_per_manager = Sales.objects.all().select_related('manager').values('manager__first_name',
                                                                                 'manager__department__name',
                                                                                 'manager__last_name').annotate(
            total=Count('id')).annotate(sum=Sum(F('products_sale__quantity') * F('products__price'))).order_by(
            Case(When(manager__first_name=current_user.first_name, then=0), default=1),
            f'{order_by}')
    if request.method == 'POST' and task_form.is_valid():
        title = task_form.cleaned_data['title']
        content = task_form.cleaned_data['content']
        manager = Managers.objects.get(first_name=current_user.first_name)
        task = Tasks(title=title, content=content, manager=manager)
        task.save()

    return render(request, 'crm/dashboard.html',
                  {'user': current_user,
                   'sales_count': sales_count,
                   'spm': sales_per_manager,
                   'form': order_form,
                   'task_form': task_form,
                   'tasks': tasks,
                   'color': radn_num,
                   'sales': sales})


def completeTodo(request, todo_id):
    todo = Tasks.objects.get(pk=todo_id)
    todo.is_completed = True
    todo.save()

    return redirect('/crm')


def delete_all_completed(request):
    delt = Tasks.objects.all().filter(is_completed=True)
    for it in delt:
        it.delete()
    return redirect('/crm')


def delete_one(request, todo_id):
    todo = Tasks.objects.get(pk=todo_id)
    todo.delete()
    return redirect('/crm')


def settings(request):
    user = request.user.username
    print(user)
    info = Managers.objects.select_related('department').get(username=user)
    form = SettingsForm(instance=info)
    context = {
        'info': info,
        'form': form
    }
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Data updated successfully')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            region = form.cleaned_data['region']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            department = form.cleaned_data['department']
            Managers.objects.filter(first_name=request.user.first_name).update(first_name=first_name,
                                                                               last_name=last_name, region=region,
                                                                               address=address, email=email,
                                                                               department=department)
            info = Managers.objects.select_related('department').get(username=user)
    return render(request, 'crm/settings.html', context=context)


def sales(request):
    add_deal_form = Sales_add()
    product_form = formset_factory(ProductSale, extra=1)
    clien_form = ClientForm()
    form = ProductForm()
    user = request.user
    sales = Sales.objects.all().annotate(date=TruncTime('sale_time')).filter(
        manager__first_name=user.first_name).annotate(sum=Sum(F('products_sale__quantity') * F('products__price')))
    context = {
        'sales': sales,
        'form': form,
        'c_form': clien_form,
        'sales_add': add_deal_form,
        'product_form': product_form
    }
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            department = form.cleaned_data['department']
            department_obj = Departments.objects.get(name=department)
            product = Products(name=name, price=price, department=department_obj)
            product.save()
    return render(request, 'crm/sales.html', context=context)


@require_http_methods(['POST'])
def add_client(request):
    form = ClientForm(request.POST)
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        try:
            test = Clients.objects.get(first_name=first_name, last_name=last_name, email=email)
        except:
            messages.success(request, 'Client has been added successfully')
            test = False
        finally:
            if not test:
                client = Clients(first_name=first_name, last_name=last_name, email=email)
                client.save()
            else:
                messages.error(request, 'Client already in base')
    return redirect('sales')


@require_http_methods(['POST'])
def add_deal(request):
    form = Sales_add(request.POST)
    form_fac = formset_factory(ProductSale, extra=3)(request.POST)
    if form.is_valid():
        client = form.cleaned_data['client']
        sale = Sales(sale_date=date.today(), sale_time=time.strftime('%H:%M:%S'),
                     manager=Managers.objects.get(username=request.user.username), client=client)
        sale.save()
    if form_fac.is_valid():
        for fr in form_fac:
            name = fr.cleaned_data['products']
            quantity = fr.cleaned_data['quantity']
            product_id = Sales.objects.all().last().pk
            product_sale = Products_sale(products_id=Products.objects.get(name=name).pk, quantity=quantity,
                                         sales_id=product_id)
            product_sale.save()
    return redirect('sales')


def products(request):
    form = ProductForm()
    products = Products_sale.objects.values('products__name', 'products__price',
                                            "products__department__name").annotate(sum=Sum('quantity')).order_by('-sum')
    context = {
        'form': form,
        'products': products
    }
    return render(request, 'crm/products.html', context=context)


@require_http_methods(['POST'])
def prod_add_form(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        product = Products(name=form.cleaned_data['name'], price=form.cleaned_data['price'], department=form.cleaned_data['department'])
        product.save()
    return redirect('products')


def department_managment(request):
    form = DepartmentForm()
    departments = Managers.objects.values('department__name','department__location').annotate(managers=Count('id'))
    current_dep = Departments.objects.get(pk=Managers.objects.values('department_id').get(username=request.user.username).get('department_id'))
    print(departments, current_dep)
    context = {
        'all_dep': departments,
        'cur_dep': current_dep,
        'form': form
    }
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        deps = Departments.objects.all().values('name')
        lst = []
        for dep in deps:
            lst.append(dep.get('name'))
        if form.is_valid():
            if form.cleaned_data['name'] not in lst:
                Departments(name=form.cleaned_data['name'], location=form.cleaned_data['location']).save()
    return render(request, 'crm/departments_managment.html', context=context)