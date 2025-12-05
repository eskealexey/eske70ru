from django.contrib import messages
from django.shortcuts import render
import math
from .forms import OhmLawForm, VoltageDividerForm, ADCCalculatorForm

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

def calculate_adc_value(voltage, resolution, vref, vmin=0):
    """Расчет цифрового значения для аналогового напряжения"""
    # Ограничение напряжения по диапазону
    if voltage < vmin:
        voltage = vmin
    if voltage > vref:
        voltage = vref

    # Расчет
    max_digital_value = (2 ** resolution) - 1
    voltage_range = vref - vmin

    # Цифровое значение
    digital_value = round((voltage - vmin) * max_digital_value / voltage_range)

    # Фактическое напряжение после квантования
    actual_voltage = (digital_value * voltage_range / max_digital_value) + vmin

    return {
        'digital_decimal': digital_value,
        'digital_binary': bin(digital_value)[2:].zfill(resolution),
        'digital_hex': f"0x{hex(digital_value)[2:].upper().zfill(math.ceil(resolution / 4))}",
        'actual_voltage': actual_voltage,
        'quantization_error': voltage - actual_voltage,
    }


def adc_calculator(request):
    """Основная view для расчета АЦП"""
    result = None
    characteristics = None
    snr_info = None

    if request.method == 'POST':
        form = ADCCalculatorForm(request.POST)

        if form.is_valid():
            # Получаем данные из формы
            resolution = form.cleaned_data['resolution']
            vref = form.cleaned_data['vref']
            vmin = form.cleaned_data['vmin']
            analog_voltage = form.cleaned_data['analog_voltage']
            sampling_rate = form.cleaned_data.get('sampling_rate', 0)
            signal_frequency = form.cleaned_data.get('signal_frequency', 0)

            # 1. Расчет цифрового значения
            result = calculate_adc_value(analog_voltage, resolution, vref, vmin)

            # 2. Расчет характеристик АЦП
            quantization_step = (vref - vmin) / (2 ** resolution)
            dynamic_range_db = 6.02 * resolution + 1.76
            max_digital_value = (2 ** resolution) - 1
            voltage_range = vref - vmin

            characteristics = {
                'quantization_step': quantization_step,
                'quantization_step_mv': quantization_step * 1000,  # в милливольтах
                'dynamic_range_db': dynamic_range_db,
                'max_digital_value': max_digital_value,
                'voltage_range': voltage_range,
                'lsb_weight': quantization_step,  # Вес младшего разряда
            }

            # 3. Расчет SNR и частотных характеристик (если заданы частоты)
            if sampling_rate > 0 and signal_frequency > 0:
                nyquist_freq = sampling_rate / 2
                is_aliasing = signal_frequency > nyquist_freq

                # Идеальный SNR для синусоидального сигнала
                snr_ideal = 6.02 * resolution + 1.76

                # Расчет эффективного числа разрядов (ENOB)
                # (в реальности нужно измеренное значение SNR)
                enob = (snr_ideal - 1.76) / 6.02

                # Время преобразования (условно)
                conversion_time = 1 / sampling_rate if sampling_rate > 0 else 0

                snr_info = {
                    'snr_ideal': snr_ideal,
                    'enob': enob,
                    'nyquist_freq': nyquist_freq,
                    'is_aliasing': is_aliasing,
                    'sampling_period': conversion_time * 1000,  # в мс
                    'max_signal_freq': nyquist_freq,
                }

            # 4. Примеры преобразования для разных напряжений
            examples = []
            test_points = 5
            for i in range(test_points + 1):
                test_voltage = vmin + (i * (vref - vmin) / test_points)
                example_result = calculate_adc_value(test_voltage, resolution, vref, vmin)
                examples.append({
                    'voltage': test_voltage,
                    'digital': example_result['digital_decimal'],
                    'binary': example_result['digital_binary'],
                    'actual': example_result['actual_voltage'],
                })

            result['examples'] = examples

    else:
        form = ADCCalculatorForm()

    context = {
        'form': form,
        'result': result,
        'characteristics': characteristics,
        'snr_info': snr_info,
        'title': 'Калькулятор АЦП',
    }

    return render(request, 'calc/acp.html', context)

