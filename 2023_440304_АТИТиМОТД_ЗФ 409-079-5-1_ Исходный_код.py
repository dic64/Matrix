import PySimpleGUI as sg
import numpy as np

# Define a list of operations for the Combo element
operations = ['Определитель', 'Сумма', 'Произведение']

# Define a list of matrix types for the Dropdown element
matrix_types = ['Квадратная', 'Треугольная', 'Диагональная']

# Create the layout for the GUI with Dropdown element
layout = [
    [sg.Text('Введите размер матрицы (2-6):')],
    [sg.InputText(default_text='2', key='matrix_size')],
    [sg.Text('Выберите тип матрицы:')],
    [sg.Drop(values=matrix_types, default_value='Квадратная', key='matrix_type')],
    [sg.Text('Введите элементы первой матрицы, разделенные пробелами:')],
    [sg.Multiline(key='matrix1')],
    [sg.Text('Введите элементы второй матрицы, разделенные пробелами:')],
    [sg.Multiline(key='matrix2')],
    [sg.Combo(['Таблица', 'Текст'], default_value='Таблица', key='output_format'),
     sg.Combo(operations, default_value='Определитель', key='operation')],
    [sg.Button('Выполнить операцию'), sg.Button('Сбросить'), sg.Button('Справка')],
    [sg.Button('Сохранить результат'), sg.Button('Выход')],
]

# Create the window
window = sg.Window('Матричные операции', layout, resizable=True)

# Loop to process the events
while True:
    event, values = window.read()

    # If the user closes the window or clicks the Exit button, exit the loop
    if event == sg.WIN_CLOSED or event == 'Выход':
        break

    # Reset all fields
    if event == 'Сбросить':
        window['matrix_type'].update('Квадратная')
        window['matrix1'].update('')
        window['matrix2'].update('')
        window['output_format'].update('Таблица')
        window['operation'].update('Определитель')
        window['matrix_size'].update('2')

    try:
        # Validate input values and calculate the result
        matrix_size = int(values['matrix_size'])
        if matrix_size < 2 or matrix_size > 6:
            raise ValueError
        
        matrix_str = values['matrix1'].strip()
        if matrix_str:
            matrix_arr = np.array([float(x) for x in matrix_str.split()]).reshape(matrix_size, matrix_size)
        else:
            matrix_arr = np.zeros((matrix_size, matrix_size))
        
        if values['matrix2']:
            matrix2_arr = np.array([float(x) for x in values['matrix2'].strip().split()]).reshape(matrix_size, matrix_size)
        else:
            matrix2_arr = None

        matrix_type = values['matrix_type']

        if event == 'Выполнить операцию':
            operation = values['operation']
            
            if operation == 'Определитель':
                det = np.linalg.det(matrix_arr)
                result = round(det, 2)
                
            elif operation == 'Сумма':
                if not matrix2_arr.any():
                    raise ValueError('Введите элементы второй матрицы')
                result = np.add(matrix_arr, matrix2_arr)
                
            elif operation == 'Произведение':
                if not matrix2_arr.any():
                    raise ValueError('Введите элементы второй матрицы')
                if matrix_arr.shape[1] != matrix2_arr.shape[0]:
                    raise ValueError('Невозможно выполнить операцию: неправильные размеры матриц')
                result = np.dot(matrix_arr, matrix2_arr)

            # Display the result in the chosen format
            output_format = values['output_format']
            if output_format == 'Таблица':
                sg.popup_scrolled(result, title='Результат')  
                           
            elif output_format == 'Текст':
                sg.popup(f'Матрица типа {matrix_type}:\n{result}')
        
        # Show the help window on button press
        elif event == 'Справка':
            sg.popup(
            '1. Как пользоваться приложением:\n'
                '- Введите размер матрицы (2-6) и выберите тип матрицы: квадратная, треугольная или диагональная.\n'
                '- Введите все элементы обеих матриц через пробелы или оставьте поля пустыми, чтобы заполнить их нулями.\n'
                '- Выберите желаемый формат вывода результата: таблица или текст.\n'
                '- Выберите нужную операцию: определитель, сумма или произведение.\n'
                '- Нажмите кнопку "Выполнить операцию", чтобы увидеть результат в выбранном формате.\n\n'
            '2. Описание функций приложения:\n'
                '- Определитель: вычисляет определитель заданной матрицы.\n'
                '- Сумма: складывает две заданные матрицы.\n'
                '- Произведение: перемножает две заданные матрицы.\n\n'

            '3. Обработка ошибок:\n'
                '- Если введен некорректный размер матрицы, приложение сообщит об этом и предложит ввести корректное значение.\n'
                '- Если для операций "Сумма" и "Произведение" не введены элементы одной из матриц, приложение сообщит об этом и не выполнит операцию.\n'
                '- Если для операции "Произведение" переданы матрицы неправильных размеров, приложение сообщит об этом и не выполнит операцию.\n'
                '- Если введены некорректные значения элементов матрицы, приложение сообщит об этом и не выполнит операцию.\n\n'

            '4. Дополнительная информация:\n'
                '- Приложение использует библиотеку PySimpleGUI для создания интерфейса и библиотеку NumPy для работы с матрицами.\n'
                '- Пользователь может открыть окно справки, чтобы получить дополнительную информацию о том, как пользоваться приложением.\n'
            'Автор : Чудайкин К.Ю.',
            title='Справка')
        
        # Save the result to a file on button press
        elif event == 'Сохранить результат':
            filename = sg.popup_get_file('Введите имя файла для сохранения', save_as=True)
            if filename:
                np.savetxt(filename, result, fmt='%.2f')

    except ValueError as e:
        sg.popup(f'Ошибка: {e}')
    except Exception as e:
        sg.popup(f'Произошла ошибка: {e}')