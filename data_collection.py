import wikipediaapi
import random
import re
import pandas as pd
from tqdm import tqdm

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "SpaceRestorerBot/1.0 (+https://github.com/your-repo)",
]

USER_AGENT = random.choice(USER_AGENTS)

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^А-Яа-яЁёA-Za-z0-9 ]+', '', text)
    return text.strip()

def get_wiki(lang="ru"):
    return wikipediaapi.Wikipedia(
        language=lang,
        user_agent=USER_AGENT
    )

def get_wiki_page(title, lang="ru"):
    wiki = get_wiki(lang)
    page = wiki.page(title)
    if page.exists():
        return clean_text(page.text)
    return ""

def get_random_articles(n=50, lang="ru"):
    wiki = get_wiki(lang)
    texts = []
    for _ in tqdm(range(n), desc="Случайные статьи"):
        try:
            page = wiki.randompage()
            text = clean_text(page.text)
            if text:
                texts.append(text)
        except Exception:
            continue
    return texts

def make_dataset(text, n_samples=5000, min_words=2, max_words=4):
    words = text.split()
    rows = []
    for _ in range(n_samples):
        if len(words) < max_words:
            break
        start = random.randint(0, len(words) - max_words)
        end = start + random.randint(min_words, max_words)
        snippet = words[start:end]
        if len(snippet) < min_words:
            continue
        target_text = " ".join(snippet)
        input_text = "".join(snippet)
        rows.append({"text_no_spaces": input_text, "text_restored": target_text})
    return rows

def generate_synthetic(rows_count=2000):
    russian_words = [
        "Москва", "телефон", "компьютер", "игра", "музыка", "новый", "куплю", "сдам",
        "квартира", "студия", "дом", "комната", "дача", "гараж", "офис", "склад",
        "ремонт", "доставка", "срочно", "недорого", "бесплатно", "ищу", "продам",
        "работа", "учитель", "репетитор", "няня", "такси", "сантехник", "электрик",
        "пылесос", "ноутбук", "холодильник", "телевизор", "монитор", "стол", "диван",
        "кресло", "шкаф", "кровать", "велосипед", "машина", "авто", "запчасти",
        "собака", "котенок", "кошка", "щенок", "билеты", "суши", "пицца", "еда",
        "магазин", "мебель", "одежда", "обувь", "куртка", "джинсы", "платье",
        "рюкзак", "чемодан", "игрушки", "книги", "портрет", "музыка", "гитара",
        "пианино", "барабан", "камера", "фото", "видео", "принтер", "роутер"
    ]

    brands = [
        "Philips", "Samsung", "iPhone", "iPad", "MacBook", "Xbox", "PlayStation", 
        "Sony", "LG", "Asus", "Lenovo", "Dell", "Acer", "MSI", "Huawei", "Honor",
        "Xiaomi", "Oppo", "Vivo", "Realme", "Redmi", "Nokia", "Motorola", "Google Pixel",
        "Adidas", "Nike", "Puma", "Reebok", "Levi’s", "Lacoste", "Gucci", "Prada",
        "Bosch", "Siemens", "Electrolux", "Whirlpool", "Indesit", "Miele", "Ariston",
        "JBL", "Marshall", "Sennheiser", "Beats", "Casio", "Rolex", "Tag Heuer",
        "Lego", "Ikea", "Avito", "Yandex", "Сбербанк", "TCL", "Sharp", "Gigabyte"
    ]

    numbers = [
        "2023", "2024", "14", "13", "13Pro", "15", "15Pro", "11", "12", "12Pro", "10",
        "One", "360", "5", "7", "8", "9", "16", "17", "18", "19", "20", "21", "22",
        "23", "24", "25", "30", "32", "40", "50", "55", "65", "70", "100", "2107",
        "27 дюймов", "70 литров", "28", "37 размер", "2 года", "6 соток", "5.1", "4K"
    ]


    rows = []
    for _ in range(rows_count):
        rw = random.choice(russian_words)
        br = random.choice(brands)
        num = random.choice(numbers)

        pattern_parts = random.choice([
            [rw, num],         # ["Москва", "2023"]
            [rw, br],          # ["телефон", "Philips"]
            [br, num],         # ["iPhone", "14"]
            [rw, br, num],     # ["телефон", "Philips", "2023"]
            [br, num, rw]      # ["iPhone", "14", "Москва"]
        ])

        add_comma = False
        if random.random() < 0.1:  
            idx = random.randint(0, len(pattern_parts) - 2) 
            pattern_parts[idx] = pattern_parts[idx] + ","
            add_comma = True
            comma_index = idx

        pattern = "".join(pattern_parts)

        target = re.sub(r'([А-Яа-яЁё])([0-9])', r'\1 \2', pattern)
        target = re.sub(r'([0-9])([А-Яа-яЁё])', r'\1 \2', target)
        target = re.sub(r'([А-Яа-яЁё])([A-Za-z])', r'\1 \2', target)
        target = re.sub(r'([A-Za-z])([А-Яа-яЁё])', r'\1 \2', target)
        target = re.sub(r'([A-Za-z])([0-9])', r'\1 \2', target)
        target = re.sub(r'([0-9])([A-Za-z])', r'\1 \2', target)

        if add_comma:
            target = target.replace(",", ", ")

        rows.append({"text_no_spaces": pattern, "text_restored": target})
    return rows


if __name__ == "__main__":
    print(f"User-Agent: {USER_AGENT}\n")

    brand_pages = [
        "Apple",
        "Google",
        "Microsoft",
        "Amazon",
        "Meta",
        "Tesla",
        "Samsung",
        "Huawei",
        "Xiaomi",
        "Intel",
        "AMD",
        "PlayStation",
        "Xbox",
        "Nintendo",
        "LG",
        "Philips",
        "Sony",
        "Dell",
        "HP",
        "Asus",
        "Lenovo",
    ]

    print("Скачиваем брендовые статьи...")
    brand_texts = [get_wiki_page(title, lang="ru") for title in brand_pages]

    print("Скачиваем случайные статьи...")
    random_texts = get_random_articles(n=100, lang="ru")

    print("Формируем общий корпус...")
    full_text = " ".join(brand_texts + random_texts)

    print("Создаём датасет из Википедии...")
    wiki_rows = make_dataset(full_text, n_samples=10000)

    print("Создаём синтетический датасет...")
    synthetic_rows = generate_synthetic(rows_count=3000)

    all_rows = wiki_rows + synthetic_rows
    df = pd.DataFrame(all_rows)

    df.to_csv("train_model_data\wiki_dataset.csv", index=False, encoding="utf-8", sep=';')
    print("Готово! Сохранено в wiki_dataset.csv")
