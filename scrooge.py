from os import name
import re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
console.clear()

console.print(Panel.fit("💰 [bold green]Скрудж[/bold green] 💰\nДавайте проанализируем ваши расходы.", title="Добро пожаловать!"))

console.print("Вводите данные о покупках в формате: [bold blue]<название>:<сумма>:<категория>[/bold blue]")
console.print("Вы можете вводить несколько статей расходов за раз. В этом случае разделяйте из запятыми ',' ")
console.print("Например:'[bold blue] кофе:50:Еда, обед:120:Еда, книга:300:Развлечения, такси:100:Транспорт[/bold blue]'", emoji=False)

console.rule("[yellow]Начнем[/yellow]")

input_strings = []

def check_purch(purch):
    patt = re.compile(r"^[^:]+:\d+(\.\d+)?:[^:]+$")
    return True if patt.match(purch) else False

while True:
    #    break # ДЛЯ ТЕСТА В РЕЛИЗЕ ЗАКОМЕНТИТЬ!!!
    console.print("Введите данные\nЧтобы закончить ввод наберите '[red]стоп[/red]'\n[green]>>>[green]", end='')
    user_input = input().lower()
    user_input = user_input.replace(' ', '')

    if user_input == 'стоп':
        console.print("Ввод завершен 👍")
        break
    for x in user_input.split(','):
        if check_purch(x):
            input_strings.append(x)
            console.print(f"Покупка [green]{x}[/green] была добавлена. ✅")
        else:
            console.print(f"Покупка [red]{x}[/red] введена не корректно и не включена в список. ❌")
    
    console.print(f"Всего в списке: [green]{len(input_strings)}[/green]\n")

#input_strings = "кофе:50:Еда,обед:120:Еда,книга:300:Развлечения,такси:100:Транспорт,кино:400:Развлечения,шаурма:80:Еда,автобус:60:Транспорт,чай:30:Еда,подарок:500:Подарки,бензин:2000:Транспорт,мороженое:70:Еда,билеты:600:Развлечения,ужин:250:Еда,кофе:60:Еда,пицца:300:Еда,метро:40:Транспорт,концерт:800:Развлечения,сок:20:Еда,цветы:200:Подарки,бензин:1500:Транспорт,завтрак:90:Еда,такси:200:Транспорт,книга:150:Развлечения,обед:180:Еда,кофе:40:Еда,парковка:50:Транспорт,ужин:300:Еда,билеты:700:Развлечения,подарок:1000:Подарки,бензин:2500:Транспорт,мороженое:50:Еда,такси:120:Транспорт,книга:250:Развлечения,обед:200:Еда,кофе:30:Еда,автобус:70:Транспорт,чай:25:Еда,подарок:300:Подарки,бензин:1800:Транспорт".lower().split(',') # СТРОКА ДЛЯ ТЕСТА В РЕЛИЗЕ ЗАКОМЕНТИТЬ!!!

categ_dict = {}

for purch in input_strings:
    
    name, cost, categ = purch.split(':')
    cost = float(cost)
    
    if categ not in categ_dict:
        categ_dict[categ] = []
    
    categ_dict[categ].append((name, cost))

total_cat = [(cat, sum(cost for _, cost in items)) for cat, items in categ_dict.items()]# Общая сумма расходов
aver_cat = [(cat, sum(cost for _, cost in items) / len(items)) for cat, items in categ_dict.items()] # Средняя сумма по категориям
count_cat = [(cat, len(items)) for cat, items in categ_dict.items()] # Средняя сумма по категориям
purch_cat = [(cat, " ".join(name for name, _ in items), len(items))for cat, items in categ_dict.items()]# Список покупок по категориям 


console.rule("[green]Отчет[/green]")

console.print(f"[bold blue]Общий отчет по расходам.[/bold blue]")

total_all = sum([x[1] for x in count_cat])
total_cost = sum([x[1] for x in total_cat])
total_aver = total_cost/total_all

console.print(f"Количество покупок: {total_all}")
console.print(f"Общая сумма расходов: {total_cost}")
console.print(f"Среднее значение расходов: {total_aver:8.2f}")

table = Table(title=f"Детализация по категориям") 

table.add_column("Категория")
table.add_column("Список покупок")
table.add_column("Суммарная стоимость")
table.add_column("Средняя цена")
table.add_column("Количество покупок")

for i in range(len(total_cat)):
    table.add_row(total_cat[i][0], purch_cat[i][1], str(total_cat[i][1]), str(round(aver_cat[i][1], 2)), str(count_cat[i][1]))

console.print(table)

console.print(f"Сформирован [green]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/green]")
console.print("Для выхода нажмите Enter ⏎")
input()
