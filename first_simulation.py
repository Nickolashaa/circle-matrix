import os
import shutil

from random import randint
from main import CircleMatrix
from plot import generate_plot


if __name__ == "__main__":
    logs_dir = "logs"
    if os.path.exists(logs_dir):
        shutil.rmtree(logs_dir)
    os.makedirs(logs_dir) 

    cm = CircleMatrix(
        row_count=int(input("Введите кол-во строк: ")),
        expected_result=bool(int(input("Желаемый результат нижнего ряда (1=True, 0=False): "))),
    )
    print(f"Создана матрица {cm.row_count}x{cm.column_count}")
    cm.set_max_random_value(
        int(input(f"Введите максимальное значение (кратное {cm.column_count} и не меньше {cm.column_count * 2}): "))
    )
    cm.build()
    count = int(input("Введите кол-во симуляций: "))
    iterations_needed = []
    for i in range(count):
        print(f"Запуск симуляции {i + 1}")
        generated_numbers = [
            randint(1, cm.max_random_value)
            for _ in range(cm.row_count)
        ]
        print(generated_numbers)
        cnt = cm.simulate_without_gen(generated_numbers)
        iterations_needed.append(cnt)
        with open(f"{logs_dir}/simulation {i + 1}.txt", "w") as f:
            f.write('[' + ', '.join(list(map(str, generated_numbers))) + ']' + str(cm))

    print(iterations_needed)
    generate_plot(cm, iterations_needed)
    print("РАБОТА ЗАВЕРШЕНА")
    input("Для выхода нажмите любую кнопку... ")
