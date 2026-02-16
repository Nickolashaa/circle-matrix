from datetime import datetime
import os
from random import randint

from core import CircleMatrix, get_tree_dimensions
from plot import generate_plot


if __name__ == "__main__":
    datetime_str = datetime.now().strftime("%Y.%m.%d %H.%M.%S")
    dir_name = f"launch {datetime_str}"

    print("РАБОТА НАЧАТА")

    tree_count = int(input("Введите количество деревьев: "))
    if tree_count <= 0:
        raise ValueError("Число деревьев должно быть > 0")

    dimensions = get_tree_dimensions(count=tree_count)

    for dimension in dimensions:
        os.makedirs(f"{dir_name}/{dimension}ичное/logs", exist_ok=True)
        print(f"Расчёт {dimension}ичного дерева")

        cm = CircleMatrix(
            row_count=int(input("Введите кол-во строк: ")),
            expected_result=bool(
                int(input("Желаемый результат нижнего ряда (1=True, 0=False): "))
            ),
            dimension=dimension,
        )
        print(f"Создана матрица {cm.row_count}x{cm.column_count}")

        cm.set_max_random_value(
            int(
                input(
                    f"Введите максимальное значение (кратное {cm.column_count} и не меньше {cm.column_count * dimension}): "
                )
            )
        )

        cm.build()

        simulation_count = int(input("Введите кол-во симуляций: "))
        iterations_needed = []

        for i in range(simulation_count):
            print(f"Запуск симуляции {i + 1}")

            generated_numbers = [
                randint(1, cm.max_random_value) for _ in range(cm.row_count)
            ]

            print(f"Сгенерированные значения: {generated_numbers}")

            cnt = cm.simulate(generated_numbers)
            iterations_needed.append(cnt)

            with open(
                f"{dir_name}/{dimension}ичное/logs/simulation {i + 1}.txt", "w"
            ) as f:
                f.write(
                    "Сгенерированные числа: ["
                    + ", ".join(list(map(str, generated_numbers)))
                    + "]"
                    + str(cm)
                )

            # cm.reset_percentiles()

        generate_plot(
            cm=cm,
            iterations_needed=iterations_needed,
            file_name=f"{dir_name}/{dimension}ичное/plot.png",
        )
    print("РАБОТА ЗАВЕРШЕНА")
    input("Для выхода нажмите любую кнопку...")
