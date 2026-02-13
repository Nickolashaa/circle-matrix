from datetime import datetime
import os
from random import randint

from core import CircleMatrix
from plot import generate_plot

if __name__ == "__main__":
    datetime_str = datetime.now().strftime("%Y.%m.%d %H.%M.%S")
    dir_name = f"launch {datetime_str}"
    os.makedirs(f"{dir_name}/logs", exist_ok=True)

    cm = CircleMatrix(
        row_count=int(input("Введите кол-во строк: ")),
        expected_result=bool(
            int(input("Желаемый результат нижнего ряда (1=True, 0=False): "))
        ),
    )
    print(f"Создана матрица {cm.row_count}x{cm.column_count}")
    cm.set_max_random_value(
        int(
            input(
                f"Введите максимальное значение (кратное {cm.column_count} и не меньше {cm.column_count * 2}): "
            )
        )
    )
    cm.build()
    count = int(input("Введите кол-во симуляций: "))
    iterations_needed = []
    for i in range(count):
        print(f"Запуск симуляции {i + 1}")
        generated_numbers = [
            randint(1, cm.max_random_value) for _ in range(cm.row_count)
        ]
        print(generated_numbers)
        cnt = cm.simulate_without_gen(generated_numbers)
        iterations_needed.append(cnt)
        with open(f"{dir_name}/logs/simulation {i + 1}.txt", "w") as f:
            f.write("[" + ", ".join(list(map(str, generated_numbers))) + "]" + str(cm))

    print(iterations_needed)
    generate_plot(
        cm=cm, iterations_needed=iterations_needed, file_name=f"{dir_name}/plot.png"
    )
    print("РАБОТА ЗАВЕРШЕНА")
    input("Для выхода нажмите любую кнопку... ")
