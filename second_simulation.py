import os
import shutil
import matplotlib.pyplot as plt
from main import CircleMatrix


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
        cnt = cm.simulate()
        iterations_needed.append(cnt)
        with open(f"{logs_dir}/simulation {i + 1}.txt", "w") as f:
            f.write(str(cm))

    print(iterations_needed)
    width = max(8, count * 0.5)
    height = max(6, max(iterations_needed) * 0.3)
    plt.figure(figsize=(width, height))

    plt.plot(range(1, len(iterations_needed) + 1), iterations_needed, marker="o", linestyle="-")
    plt.xlabel("Номер симуляции")
    plt.ylabel("Количество итераций до цели")
    plt.title("Симуляции CircleMatrix")

    step_x = max(1, count // 20)
    plt.xticks(range(1, len(iterations_needed) + 1, step_x))

    min_y, max_y = min(iterations_needed), max(iterations_needed)
    step_y = max(1, (max_y - min_y) // 20)
    plt.yticks(range(min_y, max_y + 1, step_y))

    plt.text(
        0.5, 0.95,
        f"rows={cm.row_count}, max_random_value={cm.max_random_value}",
        ha="center", va="center",
        transform=plt.gca().transAxes,
        bbox=dict(facecolor="white", alpha=0.6, edgecolor="gray")
    )

    plt.grid(True)
    plt.savefig("simulation_plot.png", dpi=300, bbox_inches="tight")
    print("РАБОТА ЗАВЕРШЕНА")
    input("Для выхода нажмите любую кнопку... ")
