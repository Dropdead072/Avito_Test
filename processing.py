import pandas as pd
import numpy as np
import re
import string
from typing import List


class SpaceRestorer:
    '''
    Euristic based cleaner
    '''
    def __init__(self):
        self.letter_digit_pattern = re.compile(r'([а-яА-Яa-zA-Z])(\d+)')  # letter -> digit
        self.digit_letter_pattern = re.compile(r'(\d+)([а-яА-Яa-zA-Z])')  # digit -> letter
        self.capital_pattern = re.compile(r'([а-яa-z])([А-ЯA-Z])')        # Capital
        self.lang_switch_pattern = re.compile(
            r'([а-яА-ЯёЁ])([a-zA-Z])|([a-zA-Z])([а-яА-ЯёЁ])'
        )  # Cyrilics->Latin
        self.comma_pattern = re.compile(r',\s*')  # , 

        self.common_words = [
            "куплю", "продам", "срочно", "новый", "новая", "отдам",
            "ищу", "сдаю", "сдам", "работа", "доставка", "недорого",
            "комната", "квартира", "дом", "гараж", "диван", "шкаф",
            "стол", "кровать", "стиральную", "машину"
        ]
        self.brands = [
            "iphone", "samsung", "lg", "philips", "ikea", "asus", "xiaomi",
            "sony", "huawei", "nokia", "playstation", "xbox", "fender",
            "yamaha", "indesit", "merida", "hp"
        ]

    def restore_spaces(self, text: str) -> str:
        text = self.letter_digit_pattern.sub(r'\1 \2', text)
        text = self.digit_letter_pattern.sub(r'\1 \2', text)
        text = self.capital_pattern.sub(r'\1 \2', text)
        text = self.lang_switch_pattern.sub(
            lambda m: (m.group(1) + " " + m.group(2)) if m.group(1) else (m.group(3) + " " + m.group(4)),
            text
        )

        text = self.comma_pattern.sub(", ", text)

        for word in self.common_words + self.brands:
            text = re.sub(fr'({word})([а-яА-Яa-zA-Z])', r'\1 \2', text, flags=re.IGNORECASE)

        text = re.sub(r'\s+', ' ', text).strip()
        return text


def read_and_split_file(file_path):
    '''
    Read the input file from the task (can't use read_csv because the data
    has ',' in the data part as well as uses it as a sep)
    '''
    data = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        headers = file.readline().strip().split(',', 1)
        
        for line in file:
            parts = line.strip().split(',', 1)
            data.append(parts)
    
    df = pd.DataFrame(data, columns=headers)
    df.set_index(headers[0], inplace=True)
    return df


def find_space_indices(text):
    '''
    Find space indexes from string
    '''
    indices = []
    for i, char in enumerate(text):
        if char == ' ':
            indices.append(i)
    return indices
