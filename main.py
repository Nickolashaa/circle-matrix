from random import randint


class Circle:
    def __init__(self, numbers: list[int], percentile: int = 50) -> None:
        if not (0 <= percentile <= 100):
            raise ValueError("Персентиль должен быть от 0 до 100")
        self.numbers = numbers
        self.percentile = percentile
        self.result: bool | None = None
        self.memory: list[int] = []

    def calculate(self, generated_number: int) -> None:
        if generated_number not in self.numbers:
            self.result = None
            return

        split_index = int(len(self.numbers) * self.percentile / 100)
        self.result = generated_number in self.numbers[split_index:]

    def __str__(self) -> str:
        nums = ",".join(map(str, self.numbers))
        return (
            f"({nums}, {self.percentile}%, {self.result})"
            if self.result is not None
            else f"({nums}, {self.percentile}%)"
        )


class CircleMatrix:
    def __init__(
        self, row_count: int, expected_result: bool, percentile_step: int = 10
    ) -> None:
        self.row_count = row_count
        self.column_count = 2 ** (row_count - 1)
        self.matrix: list[list[Circle]] = []
        self.max_random_value: int | None = None
        self.expected_result = expected_result
        self.percentile_step = percentile_step

    def set_max_random_value(self, value: int) -> None:
        if value < self.column_count * 2 or value % self.column_count != 0:
            raise ValueError(
                "Максимальное значение должно быть не меньше и кратно числу столбцов * 2"
            )
        self.max_random_value = value

    def _deactivate_circles(self) -> None:
        for row in self.matrix:
            for circle in row:
                circle.memory.append(circle.percentile)
                circle.result = None

    def _activate_circles(self) -> None:
        for row in self.matrix:
            generated_number = randint(1, self.max_random_value)
            for circle in row:
                circle.calculate(generated_number)
                
    def _activate_circles_without_gen(self, numbers: list[int]) -> None:
        for row_index in range(self.row_count):
            generated_number = numbers[row_index]
            for circle in self.matrix[row_index]:
                circle.calculate(generated_number)

    def _get_last_column_circle(self) -> int:
        col_start, col_end = 0, self.column_count
        column_index_to_change = 0
        for row in self.matrix:
            for j, circle in enumerate(row[col_start:col_end]):
                if circle.result is not None:
                    column_index_to_change = col_start + j
                    mid = (col_start + col_end) // 2
                    if circle.result:
                        col_start = mid
                    else:
                        col_end = mid
                    break
        return column_index_to_change

    def _update_percentile(self, column_index_to_change: int):
        last_circle = self.matrix[-1][column_index_to_change]

        if self.expected_result and last_circle.result is False:
            print(f"Уменьшение персентиля на {self.percentile_step}")
            for row in self.matrix:
                row[column_index_to_change].percentile = max(
                    0, row[column_index_to_change].percentile - self.percentile_step
                )

        elif not self.expected_result and last_circle.result is True:
            print(f"Увеличение персентиля на {self.percentile_step}")
            for row in self.matrix:
                row[column_index_to_change].percentile = min(
                    100, row[column_index_to_change].percentile + self.percentile_step
                )

    def build(self) -> None:
        if self.max_random_value is None:
            raise ValueError("Необходимо задать максимальное значение")
        circle_capacity = 2
        while circle_capacity < self.max_random_value / 8:
            circle_capacity *= 2

        count = 1
        for _ in range(self.row_count):
            row: list[Circle] = []
            for _ in range(self.column_count):
                numbers_to_circle = []
                while len(numbers_to_circle) < circle_capacity:
                    numbers_to_circle.append(count)
                    count = count + 1 if count < self.max_random_value else 1
                row.append(Circle(numbers=numbers_to_circle))
            self.matrix.append(row)
            circle_capacity *= 2

    def simulate(self) -> int:
        cnt = 1
        while True:
            print(f"Попытка №{cnt}")
            self._deactivate_circles()
            generated_numbers = [
                randint(1, self.max_random_value)
                for _ in range(self.row_count)
            ]
            self._activate_circles_without_gen(generated_numbers)
            col_index = self._get_last_column_circle()
            self._update_percentile(col_index)
            flag = True
            for i in range(self.column_count):
                if self.matrix[-1][i].result != self.expected_result:
                    flag = False
                    break
            if flag is True:
                break
            cnt += 1
        return cnt
        
    def simulate_without_gen(self, numbers: list[int]) -> int:
        cnt = 1
        while True:
            print(f"Попытка №{cnt}")
            self._deactivate_circles()
            self._activate_circles_without_gen(numbers)
            col_index = self._get_last_column_circle()
            self._update_percentile(col_index)
            if self.matrix[-1][col_index].result == self.expected_result:
                break
            cnt += 1
        return cnt

    def __str__(self) -> str:
        return (
            "\n"
            + "\n".join(
                f"Row {i:02d}: " + "  ".join(str(circle) for circle in row)
                for i, row in enumerate(self.matrix, 1)
            )
            + "\n"
        )

    def check_result(self) -> bool:
        flag = True
        for col_index in range(self.column_count):
            if self.matrix[-1][col_index].result != self.expected_result:
                flag = False
                break
        return flag