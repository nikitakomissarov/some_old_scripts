
from asks import Links
from page import Page
from filter import filtering

url = 'http://ouds.alm.su/' #Указать сайт, на котором производится проверка
key = 'http://ouds' #Указать маркер, по которому скрипт будет определять, какая ссылка относится к сайту

if __name__ == "__main__":
    start = Page(url).get_driver()  # Создает драйвер в Page
    final_links = (Links(start).requesting(key))  # Передает драйвер в поиск ссылок в Asks

    filtered_links = final_links[0] #Разбивка возвращенного списка ссылок на 3 по группам, успешные
    invalid_links = final_links[1] #С ошибкой подключения
    foreign_links = final_links[2] # Внешние
    wrong_links = final_links[3]

    # print(f'FIRST PAGE GOTTEN {filtered_links}')
    # print(f'WRONG LINKS {invalid_links}')
    # print(f'FOREIGN LINKS {foreign_links}')

    for i in filtered_links:
        print(f'PAGE IN PROGRESS {i}')
        new_url = i
        next_page = Page(new_url).get_driver() #Снова передает в класс, чтобы создать экземпляр драйвера хром
        next_clean_links = Links(next_page).requesting(key, filtered_links, invalid_links, foreign_links, wrong_links) #Проверка списка ранее полученных ссылок и формирование нового списка ссылок
        filtered_links = filtering(filtered_links, next_clean_links[0]) #Фильтрация полученных вновь списков на предмет дублей и отправка обратно в цикл
        invalid_links = filtering(invalid_links, next_clean_links[1])
        foreign_links = filtering(foreign_links, next_clean_links[2])
        wrong_links = filtering(wrong_links, next_clean_links[3])
    print(f'INVALID LINKS: {invalid_links}')  #Вывод список ВСЕХ ссылок, которые не передали 200
    print(f'FOREIGN LINKS: {foreign_links}')  #Выводит список внешних ссылок
    # print(f'WRONG LINKS: {wrong_links}') #Выводит объектов, по которым структурные ошибки (invalid schema и missing schema)



