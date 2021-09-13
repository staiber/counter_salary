import pickle
import csv


class Rates:
    period_result = 0

    rates = "set.dat"

    with open(rates, "rb") as file:
        hourly_rate = pickle.load(file)
        overtime_rate = pickle.load(file)

    def __init__(self, hour, over):
        self.hourly_rate = hour
        self.overtime_rate = over

        with open(self.rates, "wb") as file:
            pickle.dump(self.hourly_rate, file)
            pickle.dump(self.overtime_rate, file)


def display_rates():
    print('\n')
    print("Ставка оплаты: ", Rates.hourly_rate, "в час.",
          "\tПереработка: ", round((Rates.hourly_rate * Rates.overtime_rate), 3), "в час.")

    while True:

        print('\n')
        choice = input("Хотите изменить ставки оплаты и переработки?  Введите 'yes' или 'no': ")
        print('\n')

        if choice.lower() == 'yes':
            change_rates()
            break

        elif choice.lower() == 'no':
            break

        else:
            print("Ошибка ввода, повторите ещё раз!")
            continue


def change_rates():
    Rates(hour=float(get_change_hour()), over=float(get_change_over()))


def get_change_hour():
    hour = float(input("Введите ставку оплаты: "))
    return hour


def get_change_over():
    over = float(input("Введите коофициент переработки: "))
    return over


def calc(hours, minutes):
    pay_overtime_min = (Rates.hourly_rate * Rates.overtime_rate) / 60
    pay_norm_min = Rates.hourly_rate / 60
    norm_limit_min = 480
    working_time_min = (hours * 60) + minutes

    if working_time_min > norm_limit_min:
        payment_over_time = (working_time_min - norm_limit_min) * pay_overtime_min
        payment_norm = norm_limit_min * pay_norm_min
        result = payment_norm + payment_over_time

        return result

    else:
        result = working_time_min * pay_norm_min
        return result


def user_input():

    while True:

        choice = input("Хотите ввести новые данные?  Введите 'yes' или 'no': ")
        print('\n')

        if choice.lower() == 'yes':

            data = "inf.csv"

            day = str(input("Введите день недели: "))
            date = int(input("Введите число: "))
            month = str(input("Введите месяц: "))
            hours = int(input("Количество отработанных часов: "))
            minutes = int(input("Количество отработанных минут: "))
            day_result = calc(hours, minutes)

            with open(data, "a", newline="") as FILE_INF:
                columns = ["day", "date", "month", "hours", "minutes", "day_result"]
                writer = csv.DictWriter(FILE_INF, fieldnames=columns)
                # writer.writeheader()

                inf = {

                    "day": day,
                    "date": date,
                    "month": month,
                    "hours": hours,
                    "minutes": minutes,
                    "day_result": day_result

                }

                writer.writerow(inf)

        elif choice.lower() == 'no':
            break

        else:
            print("Ошибка ввода, повторите ещё раз!")
            continue


def print_period(days):

    while True:

        choice = input("Хотите получить данные за определённый переод?  Введите 'yes' или 'no': ")
        print('\n')

        if choice.lower() == 'yes':

            period = int(input("Введите количество дней для рассчёта: "))
            print('\n')

            period_result = 0

            days.reverse()

            while len(days) > period:
                last_day = days[-1]
                days.remove(last_day)

            for day in days:

                print(day[1], day[2], " ", day[0], "-", day[3], "часов", day[4], "минут", "\t",
                      "Результат за день: ", round(float(day[5]), 2))
                print('\n')
                period_result += float(day[5])

            print("Результат за выбранный период: ", round(float(period_result), 2))
            print('\n')
            break

        elif choice.lower() == 'no':
            break

        else:
            print("Ошибка ввода, повторите ещё раз!")
            continue


def print_all_days():
    data = "inf.csv"

    with open(data, "r", newline="") as file_inf:
        reader = csv.reader(file_inf)

        days = list()

        for row in reader:
            print(row[1], row[2], " ", row[0], "-", row[3], "часов", row[4], "минут", "\t",
                  "Результат за день: ", round(float(row[5]), 2))
            print('\n')
            Rates.period_result += float(row[5])

            day = list()

            day.append(row[0])
            day.append(row[1])
            day.append(row[2])
            day.append(row[3])
            day.append(row[4])
            day.append(row[5])

            days.append(day)

    print("Результат за весь период: ", round(float(Rates.period_result), 2))
    print('\n')

    print_period(days)


def main():
    display_rates()
    print_all_days()
    user_input()


if __name__ == '__main__':
    main()
