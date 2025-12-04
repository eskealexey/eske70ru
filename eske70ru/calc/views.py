from django.contrib import messages
from django.shortcuts import render
from .forms import OhmLawForm, VoltageDividerForm


# def zakon_oma(request):
#     result = None
#     calculated_field = None
#     power = None
#
#     if request.method == 'POST':
#         form = OhmLawForm(request.POST)
#         if form.is_valid():
#             voltage = form.cleaned_data.get('voltage')
#             current = form.cleaned_data.get('current')
#             resistance = form.cleaned_data.get('resistance')
#
#             # Подсчет количества незаполненных полей
#             missing = [voltage, current, resistance].count(None)
#
#             # Проверка: должно быть заполнено ровно два параметра
#             if missing != 1:
#                 messages.error(request, 'Введите значения ровно для двух параметров.')
#             else:
#                 try:
#                     if voltage is None:
#                         if resistance == 0:
#                             messages.error(request, 'Сопротивление не может быть нулевым.')
#                         else:
#                             result = current * resistance
#                             calculated_field = 'voltage'
#                             voltage = result
#                             power = voltage * current
#                             messages.success(request, f'Рассчитано: Напряжение (U) = {result:.2f} В')
#
#                     elif current is None:
#                         if resistance == 0:
#                             messages.error(request, 'Сопротивление не может быть нулевым.')
#                         else:
#                             result = voltage / resistance
#                             calculated_field = 'current'
#                             current = result
#                             power = voltage * current
#                             messages.success(request, f'Рассчитано: Ток (I) = {result:.2f} А')
#
#                     elif resistance is None:
#                         if current == 0:
#                             messages.error(request, 'Ток не может быть нулевым.')
#                         else:
#                             result = voltage / current
#                             calculated_field = 'resistance'
#                             resistance = result
#                             power = voltage * current
#                             messages.success(request, f'Рассчитано: Сопротивление (R) = {result:.2f} Ом')
#                 except (TypeError, ZeroDivisionError) as e:
#                     messages.error(request, 'Произошла ошибка при расчёте. Проверьте введённые значения.')
#         else:
#             messages.error(request, 'Форма содержит ошибки.')
#     else:
#         form = OhmLawForm()
#
#     return render(request, 'calc/zakonoma.html', {
#         'form': form,
#         'result': result,
#         'calculated_field': calculated_field,
#         'power': power,
#         'title': 'Закон Ома для участка цепи',
#     })
#

def zakon_oma(request):
    result = None
    calculated_field = None
    power = None

    if request.method == 'POST':
        form = OhmLawForm(request.POST)
        if form.is_valid():
            try:
                voltage = form.cleaned_data.get('voltage')
                current = form.cleaned_data.get('current')
                resistance = form.cleaned_data.get('resistance')

                # Конвертация в float для расчётов
                voltage = float(voltage) if voltage is not None else None
                current = float(current) if current is not None else None
                resistance = float(resistance) if resistance is not None else None

                # Подсчёт заполненных полей
                filled = sum(1 for x in [voltage, current, resistance] if x is not None)

                if filled != 2:
                    messages.error(request, 'Введите значения ровно для двух параметров.')
                else:
                    if voltage is None:
                        if current is None or resistance is None:
                            messages.error(request, 'Недостаточно данных для расчёта напряжения.')
                        elif resistance == 0:
                            messages.error(request, 'Сопротивление не может быть нулевым.')
                        else:
                            result = current * resistance
                            calculated_field = 'voltage'
                            voltage = result
                            power = voltage * current
                            messages.success(request, f'Рассчитано: Напряжение (U) = {result:.2f} В')

                    elif current is None:
                        if voltage is None or resistance is None:
                            messages.error(request, 'Недостаточно данных для расчёта тока.')
                        elif resistance == 0:
                            messages.error(request, 'Сопротивление не может быть нулевым.')
                        else:
                            result = voltage / resistance
                            calculated_field = 'current'
                            current = result
                            power = voltage * current
                            messages.success(request, f'Рассчитано: Ток (I) = {result:.2f} А')

                    elif resistance is None:
                        if voltage is None or current is None:
                            messages.error(request, 'Недостаточно данных для расчёта сопротивления.')
                        elif current == 0:
                            messages.error(request, 'Ток не может быть нулевым.')
                        else:
                            result = voltage / current
                            calculated_field = 'resistance'
                            resistance = result
                            power = voltage * current
                            messages.success(request, f'Рассчитано: Сопротивление (R) = {result:.2f} Ом')

            except (ValueError, TypeError, ZeroDivisionError) as e:
                messages.error(request, f'Ошибка расчёта: {str(e)}')
        else:
            messages.error(request, 'Форма содержит ошибки. Проверьте введённые значения.')
    else:
        form = OhmLawForm()

    return render(request, 'calc/zakonoma.html', {
        'form': form,
        'result': result,
        'calculated_field': calculated_field,
        'power': power,
        'title': 'Закон Ома для участка цепи',
    })


def calculation_of_resistor_voltage_divider(request):
    result = None
    error = None

    if request.method == 'POST':
        form = VoltageDividerForm(request.POST)
        if form.is_valid():
            v_in = form.cleaned_data.get('voltage_input')
            v_out = form.cleaned_data.get('voltage_output')
            r1 = form.cleaned_data.get('resistance_1')
            r2 = form.cleaned_data.get('resistance_2')
            r_load = form.cleaned_data.get('resistance_load')

            # Проверка базовых значений
            if not v_in:
                error = "Введите напряжение питания (V_in)."
            elif v_out and v_out >= v_in:
                error = "V_out должно быть меньше V_in."
            elif v_out and v_out < 0:
                error = "V_out не может быть отрицательным."
            else:
                # Режим 1: Расчёт V_out по R1 и R2
                if v_out is None and r1 and r2 and r1 > 0 and r2 > 0:
                    if r_load and r_load > 0:
                        r_eq = (r2 * r_load) / (r2 + r_load)
                        v_out_calc = v_in * (r_eq / (r1 + r_eq))
                        result = (
                            f"С нагрузкой {r_load:.1f} Ом: "
                            f"V<sub>out</sub> = {v_out_calc:.3f} В "
                            f"(R<sub>экв</sub> = {r_eq:.2f} Ом)"
                        )
                    else:
                        v_out_calc = v_in * (r2 / (r1 + r2))
                        result = f"Без нагрузки: V<sub>out</sub> = {v_out_calc:.3f} В"

                # Режим 2: Расчёт R2 по V_out и R1
                elif v_out and r1 and not r2 and r1 > 0:
                    if v_out >= v_in:
                        error = "Невозможно получить V_out ≥ V_in в делителе."
                    else:
                        r2_calc = (v_out * r1) / (v_in - v_out)
                        result = f"При R1 = {r1} Ом → R2 = {r2_calc:.2f} Ом"

                # Режим 3: Расчёт R1 по V_out и R2
                elif v_out and r2 and not r1 and r2 > 0:
                    if v_out >= v_in:
                        error = "Невозможно получить V_out ≥ V_in в делителе."
                    else:
                        r1_calc = r2 * (v_in / v_out - 1)
                        result = f"При R2 = {r2} Ом → R1 = {r1_calc:.2f} Ом"

                # Режим 4: Недостаточно данных
                else:
                    error = "Введите достаточно данных для расчёта."

    else:
        form = VoltageDividerForm()

    return render(request, 'calc/voltage_divider.html', {
        'form': form,
        'result': result,
        'error': error,
        'title': 'Расчёт делителя напряжения'
    })

