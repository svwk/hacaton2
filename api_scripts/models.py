from dateutil import parser

from pydantic import BaseModel, field_validator
from typing import Literal

Education = Literal[
    "Высшее - специалист", "Среднее профессиональное", "Среднее", "Неоконченное высшее", "Бакалавр", "Несколько высших", "Магистр", "Неоконченное среднее", "MBA", "Ученая степень"]
EmploymentStatus = Literal[
    "Работаю по найму полный рабочий день/служу", "Собственное дело", "Не работаю", "Работаю по найму неполный рабочий день", "Студент", "Декретный отпуск", "Пенсионер"]
Experience = Literal[
    "10 и более лет", "3 - 4 года", "2 - 3 года", "4 - 5 лет", "5 - 6 лет", "1 - 2 года", "6 - 7 лет", "7 - 8 лет", "8 - 9 лет", "6 месяцев - 1 год", "9 - 10 лет", "Нет стажа", "4 - 6 месяцев", "менее 4 месяцев"]
FamilyStatus = Literal[
    "Никогда в браке не состоял(а)", "Женат / замужем", "Разведён / Разведена", "Гражданский брак / совместное проживание", "Вдовец / вдова"]
GoodsCategory = Literal["Furniture", "Mobile_devices", "Travel", "Medical_services", "Education", "Fitness", "Other"]
LoanTerm = Literal[6, 12, 18, 24]
Gender = Literal[0, 1]
Snils = Literal[0, 1]


class ClientData(BaseModel):
    skillfactory_id: str
    birth_date: str
    education: Education
    employment_status: EmploymentStatus
    value: Experience
    job_start_date: str
    position: str
    month_profit: float
    month_expense: float
    gender: Gender
    family_status: FamilyStatus
    child_count: int
    snils: Snils
    loan_amount: float
    loan_term: LoanTerm
    goods_category: GoodsCategory
    merch_code: int

    @field_validator("month_profit", "month_expense", "loan_amount")
    def field_positive(cls, value: float | int) -> float | int:
        if value <= 0:
            raise ValueError(" must be non-negative")
        return value

    @field_validator("child_count")
    def field_non_negative(cls, value: float | int) -> float | int:
        if value < 0:
            raise ValueError(" must be non-negative")
        return value

    @field_validator("child_count")
    def field_is_integer(cls, value: float | int | str) -> int:
        try:
            result = int(value)
        except ValueError:
            raise ValueError(" must be an integer")
        return result

    @field_validator("month_profit", "month_expense", "loan_amount")
    def field_is_number(cls, value: float | int | str) -> float:
        try:
            result = float(value)
        except ValueError:
            raise ValueError(" must be a number")
        return result

    @field_validator("birth_date", "job_start_date")
    def field_is_not_empty_string(cls, value: str) -> str:
        if len(value) == 0:
            raise ValueError(" must not be empty")
        return value

    @field_validator("birth_date", "job_start_date")
    def field_is_date(cls, value: str) -> str:
        try:
            parser.parse(value)
        except ValueError:
            raise ValueError(" incorrect data format, should be YYYY-MM-DD")
        return value


class BankDecisions(BaseModel):
    BankA_decision: int
    BankB_decision: int
    BankC_decision: int
    BankD_decision: int
    BankE_decision: int
