from decimal import Decimal


def is_prime(num: int) -> bool:
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def get_tree_dimensions(count: int) -> list[int]:
    result = [2]
    num = 2

    if count == 1:
        return result

    while len(result) != count:
        while True:
            num += 1
            if is_prime(num):
                result.append(num)
                break
    return result


class Circle:
    def __init__(self, numbers: list[int], percentile: int, npp: int) -> None:
        if not (0 <= percentile <= 100):
            raise ValueError("Персентиль должен быть от 0 до 100")
        self.numbers = numbers
        self.percentile = percentile
        self.result: bool | None = None
        self.memory: list[int] = []
        self.npp = npp

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
        self,
        row_count: int,
        expected_result: bool,
        dimension: int,
        percentile_step: int = 10,
    ) -> None:
        self.row_count = row_count
        self.column_count = dimension ** (row_count - 1)
        self.matrix: list[list[Circle]] = []
        self.max_random_value: int = 0
        self.expected_result = expected_result
        self.dimension = dimension
        self.variants = [0]
        if self.dimension > 2:
            while len(self.variants) != self.dimension:
                self.variants.append(max(self.variants) + 1)
                self.variants.append(min(self.variants) - 1)
        self.percentile_step = percentile_step
        self.percentile_default = 50

    def set_max_random_value(self, value: int) -> None:
        if value < self.column_count * self.dimension or value % self.column_count != 0:
            raise ValueError(
                f"Максимальное значение должно быть не меньше и кратно числу столбцов * {self.dimension}"
            )
        self.max_random_value = value

    def reset_percentiles(self) -> None:
        for row in self.matrix:
            for circle in row:
                circle.percentile = self.percentile_default

    def _deactivate_circles(self) -> None:
        for row in self.matrix:
            for circle in row:
                circle.memory.append(circle.percentile)
                circle.result = None

    def _activate_circles(self, numbers: list[int]) -> None:
        for row_index in range(self.row_count):
            generated_number = numbers[row_index]
            for circle in self.matrix[row_index]:
                circle.calculate(generated_number)

    def _get_last_column_circle(self) -> int:
        if self.dimension == 2:
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
        
        row_cnt = 1

        for i in range(len(self.matrix[0])):
            if self.matrix[0][i].result is not None:
                main_index = i
                break
        
        while row_cnt < self.row_count:
            for variant in self.variants:
                if 0 <= main_index + variant < self.column_count:
                    if self.matrix[row_cnt][main_index + variant].result is not None:
                        main_index += variant
                        break
            row_cnt += 1
        

    def _update_percentile(self, column_index_to_change: int):
        last_circle = self.matrix[-1][column_index_to_change]

        if self.expected_result and last_circle.result is False:
            print(
                f"Уменьшение персентиля в {column_index_to_change + 1} колонке на {self.percentile_step}"
            )
            for row in self.matrix:
                row[column_index_to_change].percentile = max(
                    0, row[column_index_to_change].percentile - self.percentile_step
                )

        elif not self.expected_result and last_circle.result is True:
            print(
                f"Увеличение персентиля в {column_index_to_change + 1} колонке на {self.percentile_step}"
            )
            for row in self.matrix:
                row[column_index_to_change].percentile = min(
                    100, row[column_index_to_change].percentile + self.percentile_step
                )

    def build(self) -> None:
        if self.max_random_value == 0:
            raise ValueError("Необходимо задать максимальное значение")
        circle_capacity = self.dimension
        while circle_capacity * self.column_count < self.max_random_value:
            circle_capacity *= self.dimension

        count = 1
        for i in range(self.row_count):
            row: list[Circle] = []
            for j in range(self.column_count):
                numbers_to_circle: list[int] = []
                while len(numbers_to_circle) < circle_capacity:
                    numbers_to_circle.append(count)
                    count = count + 1 if count < self.max_random_value else 1
                row.append(
                    Circle(
                        numbers=numbers_to_circle, percentile=self.percentile_default, npp=j,
                    )
                )
            self.matrix.append(row)
            circle_capacity *= self.dimension
            count = 1

    def simulate(self, numbers: list[int]) -> int:
        cnt = 1
        while True:
            print(f"Попытка №{cnt}", end=": ")
            self._deactivate_circles()
            self._activate_circles(numbers)
            col_index = self._get_last_column_circle()
            if self.matrix[-1][col_index].result == self.expected_result:
                break
            self._update_percentile(col_index)
            cnt += 1
        print("Матрица стабилизирована")
        return cnt

    def __str__(self) -> str:
        tk_results = self.calculate_Tk()
        return (
            "\n"
            + "\n".join(
                f"Row {i:02d}, Tk {tk_results[i - 1]}: "
                + "  ".join(str(circle) for circle in row)
                for i, row in enumerate(self.matrix, 1)
            )
            + "\n"
        )

    def calculate_Tk(self) -> list[Decimal]:
        results = [Decimal(0) for _ in range(self.row_count)]
        for row_index in range(self.row_count):
            for col_index in range(self.column_count):
                percentile_decimal = Decimal(
                    self.matrix[row_index][col_index].percentile
                ) / Decimal(100)
                exponent = col_index * row_index
                power_value = Decimal(2) ** exponent
                results[row_index] += percentile_decimal * power_value

        rounded_results = []
        for r in results:
            str_r = str(r)
            if "." in str_r:
                integer_part, decimal_part = str_r.split(".")
                if len(decimal_part) > 4:
                    decimal_part = decimal_part[:4]
                rounded_results.append(Decimal(f"{integer_part}.{decimal_part}"))
            else:
                rounded_results.append(r)

        return rounded_results
