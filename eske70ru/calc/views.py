from django.contrib import messages
from django.shortcuts import render

from .forms import OhmLawForm
from django.shortcuts import render, redirect
from .forms import OhmLawForm
from django.contrib import messages

def zakon_oma(request):

    result = None
    calculated_field = None
    power = None

    if request.method == 'POST':
        form = OhmLawForm(request.POST)
        if form.is_valid():
            voltage = form.cleaned_data.get('voltage')
            current = form.cleaned_data.get('current')
            resistance = form.cleaned_data.get('resistance')

            # Расчет недостающего параметра
            if voltage is None:
                # U = I × R
                result = current * resistance
                calculated_field = 'voltage'
                voltage = result
            elif current is None:
                # I = U / R
                result = voltage / resistance
                calculated_field = 'current'
                current = result
            elif resistance is None:
                # R = U / I
                result = voltage / current
                calculated_field = 'resistance'
                resistance = result
            power = voltage * current
            messages.success(request, f'Рассчитано: {calculated_field} = {result:.2f}')

    else:
        form = OhmLawForm()



    return render(request, 'calc/zakonoma.html', {
        'form': form,
        'result': result,
        'calculated_field': calculated_field,
        'power': power,
    })

