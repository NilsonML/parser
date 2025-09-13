def category_parser(num_of_category):

    match num_of_category:
        case 1:
            url = "https://eda.ru/recepty/zavtraki"
        case 2:
            url = "https://eda.ru/recepty/bulony"
        case 3:
            url = "https://eda.ru/recepty/zakuski"
        case 4:
            url = "https://eda.ru/recepty/napitki"
        case 5:
            url = "https://eda.ru/recepty/osnovnye-blyuda"
        case 6:
            url = "https://eda.ru/recepty/pasta-picca"
        case 7:
            url = "https://eda.ru/recepty/rizotto"
        case 8:
            url = "https://eda.ru/recepty/salaty"
        case 9:
            url = "https://eda.ru/recepty/sousy-marinady"
        case 10:
            url = "https://eda.ru/recepty/supy"
        case 11:
            url = "https://eda.ru/recepty/sendvichi"
        case 12:
            url = "https://eda.ru/recepty/vypechka-deserty"
        case 13:
            url = "https://eda.ru/recepty"
    return url
        