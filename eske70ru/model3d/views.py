from django.shortcuts import render

from .models import Model3D

# Create your views here.
def views(request):
    model3ds = Model3D.objects.all()

    # if model3ds:
    #     context = {'model3ds':model3ds}
    # else:
    #     context = {'model3ds':None}

    context = {
        'model3ds':model3ds,
        'title': 'Модели 3D',
    }
    print(context)
    return render(request,'model3d/model3d_all.html', context=context)
