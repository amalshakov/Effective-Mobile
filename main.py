import csv
import re
from typing import Dict, List, Optional, Tuple, Union

DATE_PATTERN = re.compile(r"\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])")
AMOUNT_PATTERN = re.compile(r"^\d+$")


def request_command_number(num_commands: int) -> Optional[int]:
    """
    Запрашивает у пользователя номер команды и возвращает его.
    Если введено некорректное значение или значение вне диапазона,
    выводит сообщение об ошибке в консоль и возвращает None.

    Args:
    num_commands: Количество допустимых команд.

    Returns:
    Номер команды
    или None, если введено некорректное значение.
    """
    try:
        command_number = int(
            input(f"Введите номер команды (от 1 до {num_commands}): ")
        )
        if command_number not in range(1, num_commands + 1):
            raise ValueError("Ошибка: Введен некорректный номер команды!")
        return command_number
    except ValueError:
        print_error_message()
        return None


def print_error_message():
    """
    Выводит сообщение об ошибке при некорректном вводе номера команды.
    """
    print("---")
    print("Ошибка: Введен некорректный номер команды!")
    print("---")


class Transaction:
    """Класс, представляющий транзакцию.

    Атрибуты:
        date (str): Дата транзакции в формате "гггг-мм-дд".
        category (str): Категория транзакции (например, "Расход" или "Доход").
        amount (float): Сумма транзакции.
        description (str): Описание транзакции.
    """

    def __init__(
        self, date: str, category: str, amount: float, description: str
    ) -> None:
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description


class AccountManager:
    """Класс для управления транзакциями и финансами.

    Атрибуты:
        filename (str): Имя файла, в котором хранятся данные о транзакциях.
    """

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def load_transactions(self) -> List[List[Union[str, float]]]:
        """Загрузка данных о транзакциях из файла.
        Возвращает cписок списков с данными о транзакциях.
        """
        transactions: List[List[Union[str, float]]] = []
        with open(self.filename, newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                transactions.append(row)
        return transactions

    def save_transactions(
        self, transactions: List[List[Union[str, float]]]
    ) -> None:
        """Сохраняет данные о транзакциях в файл.

        Args:
        transactions: Принимает список списков с данными о транзакциях.
        """
        with open(self.filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(transactions)

    def add_transaction(self, transaction: Transaction) -> None:
        """Добавляет данные о транзакции в файл.

        Args:
            transaction (Transaction): Объект транзакции для добавления.
        """
        with open(self.filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    transaction.date,
                    transaction.category,
                    transaction.amount,
                    transaction.description,
                ]
            )

    def edit_transaction(
        self,
        transaction_index: int,
        new_transaction_data: List[Union[str, float]],
    ) -> None:
        """Редактирует существующую транзакцию."""
        transactions = self.load_transactions()
        transactions[transaction_index - 1] = new_transaction_data
        self.save_transactions(transactions)

    def search_transactions(
        self, criteria: Dict[str, Union[str, float]]
    ) -> Union[List[List[Union[str, float]]], None]:
        """Поиск транзакций по критериям."""
        transactions = self.load_transactions()
        result = []
        for transaction in transactions:
            match = True
            for key, value in criteria.items():
                if key == "date" and transaction[0] != value:
                    match = False
                    break
                if key == "category" and transaction[1] != value:
                    match = False
                    break
                if key == "amount" and transaction[2] != value:
                    match = False
                    break
            if match:
                result.append(transaction)
        return result

    def show_balance(self) -> float:
        """Выводит баланс счета.

        Returns:
            Баланс счета, рассчитанный на основе доходов и расходов.
        """
        transactions = self.load_transactions()
        balance = 0
        for transaction in transactions:
            amount = float(transaction[2])
            if transaction[1] == "Доход":
                balance += amount
            elif transaction[1] == "Расход":
                balance -= amount
        return balance

    def show_expenses(self) -> Tuple[List[List[Union[str, float]]], float]:
        """Показывает все расходы.

        Returns:
            Список списков с данными о расходах и общую сумму расходов.
        """
        transactions = self.load_transactions()
        expenses = 0
        transactions_expenses = []
        for transaction in transactions:
            if transaction[1] == "Расход":
                amount = float(transaction[2])
                expenses += amount
                transactions_expenses.append(transaction)
        return transactions_expenses, expenses

    def show_profit(self) -> Tuple[List[List[Union[str, float]]], float]:
        """Показывает все доходы.

        Returns:
            Список списков с данными о доходах и общую сумму доходов.
        """
        transactions = self.load_transactions()
        profit = 0
        transactions_profit = []
        for transaction in transactions:
            if transaction[1] == "Доход":
                amount = float(transaction[2])
                profit += amount
                transactions_profit.append(transaction)
        return transactions_profit, profit

    def check_transaction_number_input(
        self, transaction_number: str, len_transactions: int
    ) -> bool:
        """Проверяет корректность введенного номера записи.

        Args:
            transaction_number: Введенный пользователем номер записи.
            len_transactions: Общее количество записей.

        Returns:
            True, если введенный номер записи корректен, иначе False.
        """
        try:
            number = int(transaction_number)
            return 1 <= number <= len_transactions
        except ValueError:
            return False

    def check_date_input(self) -> str:
        """Проверяет корректность введенной даты и возвращает ее.

        Returns:
            Введенную пользователем дату в формате 'гггг-мм-дд'.
        """
        while True:
            date_input = input("Введите дату в формате гггг-мм-дд: ")
            if DATE_PATTERN.match(date_input):
                return date_input
            print(
                "Неправильный формат даты. Например - "
                "для 4 мая 2024г формат даты будет такой: 2024-05-04."
            )

    def check_amount_input(self, category: str) -> int:
        """Проверяет корректность введенной суммы.

        Args:
            category: Категория транзакции.

        Returns:
            Введенную пользователем сумму.
        """
        while True:
            amount_input = input(f"{category}. Введите сумму (в рублях): ")
            if AMOUNT_PATTERN.match(amount_input):
                return int(amount_input)
            print("Неправильный формат суммы. Только цифры!")


if __name__ == "__main__":
    account_manager = AccountManager("transactions.csv")
    print(
        "Добро пожаловать в консольное приложение 'Личный финансовый кошелек'."
    )

    while True:
        print("Что Вы хотите сделать?")
        print("1. Вывести баланс, все доходы или расходы.")
        print("2. Добавить запись (о доходе или расходе).")
        print("3. Редактировать запись.")
        print("4. Поиск по записям.")
        print("5. Выйти из программы.")
        command = request_command_number(5)

        if command == 1:
            while True:
                print("1. Вывести баланс.")
                print("2. Вывести все расходы.")
                print("3. Вывести все доходы.")
                sub_command = request_command_number(3)
                if sub_command == 1:
                    balance = account_manager.show_balance()
                    print("---")
                    print(f"Ваш баланс составляет: {balance} руб.")
                    print("---")
                    break
                elif sub_command == 2:
                    transactions, expenses = account_manager.show_expenses()
                    print("---")
                    print("Все расходы:")
                    for transaction in transactions:
                        print(transaction)
                    print(f"Общая сумма расходов: {expenses} руб.")
                    print("---")
                    break
                elif sub_command == 3:
                    transactions, profit = account_manager.show_profit()
                    print("---")
                    print("Все доходы:")
                    for transaction in transactions:
                        print(transaction)
                    print(f"Общая сумма доходов: {profit} руб.")
                    print("---")
                    break

        elif command == 2:
            while True:
                print("1. Добавить запись о Расходе?")
                print("2. Добавить запись о Доходе?")
                sub_command = request_command_number(2)
                if sub_command == 1:
                    category = "Расход"
                    break
                elif sub_command == 2:
                    category = "Доход"
                    break
            amount = account_manager.check_amount_input(category)
            description = input(f"{category}. Введите описание: ").strip()
            date = account_manager.check_date_input()
            transaction = Transaction(
                date=date,
                category=category,
                amount=amount,
                description=description,
            )
            account_manager.add_transaction(transaction)
            print("---")
            print("Запись добавлена!")
            print("---")

        elif command == 3:
            transactions = account_manager.load_transactions()
            len_transactions = len(transactions)
            print("Список всех транзакций:")
            for index, transaction in enumerate(transactions):
                print(f"{index+1}. {transaction}")
            while True:
                transaction_number_input = input(
                    "Введите номер записи, которую хотите отредактировать: "
                )
                if account_manager.check_transaction_number_input(
                    transaction_number_input, len_transactions
                ):
                    break
                else:
                    print(
                        "Неправильный номер записи. Введите "
                        f"номер записи от 1 до {len_transactions}."
                    )
            while True:
                print("1. Новая категория будет - Расход?")
                print("2. Новая категория будет - Доход?")
                sub_command = request_command_number(2)
                if sub_command == 1:
                    new_category = "Расход"
                    break
                elif sub_command == 2:
                    new_category = "Доход"
                    break
            new_transaction_data = [
                account_manager.check_date_input(),
                new_category,
                account_manager.check_amount_input(new_category),
                input("Введите новое описание: "),
            ]
            account_manager.edit_transaction(sub_command, new_transaction_data)
            print("---")
            print("Запись отредактирована!")
            print("---")

        elif command == 4:
            while True:
                print("1. Поиск записей по категории.")
                print("2. Поиск записей по дате.")
                print("3. Поиск записей по сумме.")
                sub_command = request_command_number(3)
                if sub_command == 1:
                    key = "category"
                    break
                elif sub_command == 2:
                    key = "date"
                    break
                elif sub_command == 3:
                    key = "amount"
                    break
            search_query = input("Введите поисковый запрос: ")
            criteria = {key: search_query}
            search_result = account_manager.search_transactions(criteria)
            print("---")
            print("Результаты поиска:")
            for transaction in search_result:
                print(transaction)
            print("---")

        elif command == 5:
            print("---")
            print("До свидания!")
            print("---")
            break
