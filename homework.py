from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60
    COEFF_CALORIE_1: float
    COEFF_CALORIE_1: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.get_distance() / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Should be method get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_Message = InfoMessage(type(self).__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_Message


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_calories = ((
            self.COEFF_CALORIE_1
            * self.get_mean_speed()
            - self.COEFF_CALORIE_2)
            * self.weight / self.M_IN_KM
            * (self.duration * self.MIN_IN_HOUR))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        self.height = height
        super().__init__(
            action,
            duration,
            weight)

    def get_spent_calories(self) -> float:
        spent_calories = ((
            self.COEFF_CALORIE_1
            * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * self.COEFF_CALORIE_2
            * self.weight)
            * (self.duration * self.MIN_IN_HOUR))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ):
        super().__init__(
            action, duration, weight,)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = ((
            self.get_mean_speed()
            + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2
            * self.weight)
        return spent_calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in ('SWM', 'RUN', 'WLK'):
        type_identificator: dict[str, Training] = {
            'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking}
        return type_identificator[workout_type](*data)
    print('Неизвестный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    training_message = training.show_training_info()
    print(training_message.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
