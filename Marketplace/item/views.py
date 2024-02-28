from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemFrom, EditItemFrom
from django.db.models import Q
# Create your views here.
def items(request):
    query = request.GET.get('query', '')
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)
    category_id = request.GET.get('categories', 0)

    if category_id:
        items = items.filter(category_id=category_id)
    if query:
        items = items.filter(Q(name__icontains=query) | Q(descripation__icontains=query))
    context = {
        'items':items,
        'query': query,
        'categories': categories,
        'category_id':int(category_id)
    }
    return render(request, 'item/items.html', context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    realted_items = Item.objects.filter(Category=item.Category, is_sold=False).exclude(pk=pk)[0:3]

    context = {
        'item':item ,
        'realted_items':realted_items
    }
    return render(request, 'item/detail.html', context)
@login_required
def new(request):
    form = NewItemFrom()  # Define the form outside the if statement

    if request.method == 'POST':
        form = NewItemFrom(request.POST, request.FILES)
    
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)

    context = {
        'form': form,
        'title': 'title'
    }
    return render(request, 'item/form.html', context)


@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemFrom(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.pk)
    else:
        form = EditItemFrom(instance=item)

    context = {
        'form': form,
        'title': 'Edit item'
    }
    return render(request, 'item/form.html', context)
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by= request.user)
    item.delete()

    return redirect('dashboard:index') 