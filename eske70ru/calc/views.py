from django.contrib import messages
from django.shortcuts import render
from .forms import OhmLawForm


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

            # Подсчет количества незаполненных полей
            missing = [voltage, current, resistance].count(None)

            # Проверка: должно быть заполнено ровно два параметра
            if missing != 1:
                messages.error(request, 'Введите значения ровно для двух параметров.')
            else:
                try:
                    if voltage is None:
                        if resistance == 0:
                            messages.error(request, 'Сопротивление не может быть нулевым.')
                        else:
                            result = current * resistance
                            calculated_field = 'voltage'
                            voltage = result
                            power = voltage * current
                            messages.success(request, f'Рассчитано: Напряжение (U) = {result:.2f} В')

                    elif current is None:
                        if resistance == 0:
                            messages.error(request, 'Сопротивление не может быть нулевым.')
                        else:
                            result = voltage / resistance
                            calculated_field = 'current'
                            current = result
                            power = voltage * current
                            messages.success(request, f'Рассчитано: Ток (I) = {result:.2f} А')

                    elif resistance is None:
                        if current == 0:
                            messages.error(request, 'Ток не может быть нулевым.')
                        else:
                            result = voltage / current
                            calculated_field = 'resistance'
                            resistance = result
                            power = voltage * current
                            messages.success(request, f'Рассчитано: Сопротивление (R) = {result:.2f} Ом')
                except (TypeError, ZeroDivisionError) as e:
                    messages.error(request, 'Произошла ошибка при расчёте. Проверьте введённые значения.')
        else:
            messages.error(request, 'Форма содержит ошибки.')
    else:
        form = OhmLawForm()

    return render(request, 'calc/zakonoma.html', {
        'form': form,
        'result': result,
        'calculated_field': calculated_field,
        'power': power,
    })