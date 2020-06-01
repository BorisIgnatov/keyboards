from keyboard.models import Keyboard


def search(request):
    keyboards = Keyboard.objects
    if request.POST.get('switches'):
        key_list = Brand.objects.none()
        for i in request.POST.getlist('switches'):
            key_list = key_list | keyboards.filter(switches__name__contains=i)
        keyboards = key_list

    if request.POST.get('brands'):
        key_list = Brand.objects.none()
        for i in request.POST.getlist('brands'):
            key_list = key_list | keyboards.filter(brand_name__name__contains=i)
        keyboards = key_list

    if request.POST.get('priceMin'):
        min = request.POST.get('priceMin')
        keyboards = keyboards.filter(price__gte=min)

    if request.POST.get('priceMax'):
        max = request.POST.get('priceMax')
        keyboards = keyboards.filter(price__lte=max)

    if request.POST.get('keyboard_name'):
        try:
            key_list = Brand.objects.none()
            key_list = key_list | keyboards.filter(model_name__icontains=request.POST.get('keyboard_name'))
            keyboards = key_list
        except Exception as e:
            pass

    return keyboards.all()
