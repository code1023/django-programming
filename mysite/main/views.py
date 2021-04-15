from django.shortcuts import render, redirect

from .models import Cafe


def index(request):
    context = {
        'locations': Cafe.locations
    }
    return render(request, 'main/index.html', context)


def cafelist(request):
    selected_locations = request.GET.getlist('locations')
    search = request.GET.get('search')
    
    if selected_locations:
        # location값이 selected_locations에 포함되는 카페들만 필터링하겠다는 의미
        cafes = Cafe.objects.filter(location__in=selected_locations)
    elif search:
        # 카페의 name이 검색어 search를 포함하고 있는 카페들만 필터링하겠다는 의미
        cafes = Cafe.objects.filter(name__icontains=search)
    else:
        cafes = Cafe.objects.all()
    
    context = {
        'cafes': cafes,
    }
    
    return render(request, 'main/cafelist.html', context)


def cafedetails(request, pk):
    cafe = Cafe.objects.get(pk=pk)
    context = {
        'cafe': cafe,
    }
    
    return render(request, 'main/cafedetails.html', context)

def about(request):
    return render(request, 'main/about.html')


def write(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'location': request.POST.get('location'),
            'phone': request.POST.get('phone'),
            'content': request.POST.get('content'),
            'mainphoto': request.FILES.get('mainphoto'),
            'subphoto': request.FILES.get('subphoto')
        }
        
        cafe = Cafe.objects.create(**data)
        
        return redirect(f'/cafelist/{cafe.pk}/')
    
    context = {
        'locations': Cafe.locations,
    }
    
    return render(request, 'main/write.html', context)
