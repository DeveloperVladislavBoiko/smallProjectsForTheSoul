import re
import string
import numpy as np
from typing import List, Dict, Optional, Set
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pymorphy3
from functools import lru_cache


class AdvancedRussianCommandMatcher:
    def __init__(self, commands_file="commands.txt"):
        # Инициализация морфологического анализатора
        self.morph = pymorphy3.MorphAnalyzer()

        self.commands = self._load_commands(commands_file)
        self.synonyms = self._load_synonyms()
        self.stop_words = self._get_stop_words()

        # Строим индексы
        self._build_indices()

    def _load_commands(self, file_path: str) -> List[str]:
        """Загрузка команд из файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                commands = [line.strip() for line in f if line.strip()]
                if not commands:
                    raise ValueError(f"Файл '{file_path}' пуст")
                return commands
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл с командами '{file_path}' не найден")

    def _load_synonyms(self) -> Dict[str, Set[str]]:
        """Расширенный словарь синонимов с учетом разных форм слов"""
        synonyms = {
            'погода': {'прогноз', 'метео', 'дождь', 'солнце', 'температура'},
            'включить': {'запустить', 'активировать', 'врубить', 'стартовать'},
            'выключить': {'отключить', 'деактивировать', 'стоп', 'остановить'},
            'музыка': {'песня', 'трек', 'мелодия', 'аудио', 'звук'},
            'найти': {'поиск', 'отыскать', 'разыскать', 'обнаружить'},
            'открыть': {'запустить', 'развернуть', 'включить', 'показать'},
            'закрыть': {'выключить', 'свернуть', 'остановить', 'завершить'},
            'сказать': {'произнести', 'озвучить', 'показать', 'сообщить'},
            'показать': {'отобразить', 'вывести', 'продемонстрировать', 'открыть'}
        }

        # Автоматически добавляем нормальные формы для каждого синонима
        expanded_synonyms = {}
        for word, syns in synonyms.items():
            expanded_set = set(syns)
            expanded_set.add(word)
            # Добавляем все нормальные формы
            for s in list(expanded_set):
                expanded_set.add(self._get_normal_form(s))
            expanded_synonyms[word] = expanded_set

        return expanded_synonyms

    def _get_stop_words(self) -> Set[str]:
        """Расширенный список стоп-слов для русского языка"""
        return {
            'это', 'как', 'так', 'и', 'в', 'над', 'к', 'до', 'не', 'на', 'но', 'за', 'то', 'с', 'ли',
            'а', 'во', 'от', 'со', 'для', 'о', 'же', 'ну', 'вы', 'бы', 'что', 'кто', 'он', 'она', 'мне',
            'мной', 'меня', 'тебе', 'тобой', 'тебя', 'нам', 'нами', 'нас', 'вам', 'вами', 'вас', 'их',
            'ими', 'его', 'её', 'им', 'ними', 'него', 'неё', 'них', 'который', 'которая', 'которое'
        }

    @lru_cache(maxsize=10000)
    def _get_normal_form(self, word: str) -> str:
        """Получение нормальной формы слова с кэшированием"""
        parsed = self.morph.parse(word)[0]
        return parsed.normal_form

    def _preprocess_text(self, text: str) -> str:
        """Предварительная обработка текста с учетом морфологии"""
        text = text.lower().strip()
        text = re.sub(r'[{}]'.format(string.punctuation), ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def _tokenize(self, text: str) -> List[str]:
        """Продвинутая токенизация с нормализацией и обработкой синонимов"""
        text = self._preprocess_text(text)
        words = text.split()

        processed_words = []
        for word in words:
            if word in self.stop_words:
                continue

            # Получаем нормальную форму слова
            normal_form = self._get_normal_form(word)

            # Проверяем синонимы
            found_synonyms = set()
            for base_word, syns in self.synonyms.items():
                if normal_form in syns or word in syns:
                    found_synonyms.add(base_word)

            if found_synonyms:
                processed_words.extend(found_synonyms)
            else:
                processed_words.append(normal_form)

        return processed_words

    def _build_indices(self):
        """Построение индексов для быстрого поиска"""
        # Создаем TF-IDF матрицу
        self.vectorizer = TfidfVectorizer(tokenizer=self._tokenize)
        command_texts = [" ".join(self._tokenize(cmd)) for cmd in self.commands]
        self.tfidf_matrix = self.vectorizer.fit_transform(command_texts)

        # Индекс ключевых слов для каждой команды
        self.command_keywords = []
        for cmd in self.commands:
            keywords = set(self._tokenize(cmd))
            # Добавляем синонимы для каждого ключевого слова
            expanded_keywords = set()
            for word in keywords:
                expanded_keywords.add(word)
                for base, syns in self.synonyms.items():
                    if word in syns:
                        expanded_keywords.add(base)
            self.command_keywords.append(expanded_keywords)

    def _get_semantic_similarity(self, query: str, command: str, command_idx: int) -> float:
        """Вычисление семантического сходства с учетом синонимов и морфологии"""
        # Преобразуем запрос в набор токенов
        query_tokens = set(self._tokenize(query))
        command_tokens = self.command_keywords[command_idx]

        # Простое совпадение токенов
        common_tokens = query_tokens & command_tokens
        token_sim = len(common_tokens) / max(len(query_tokens),
                                             len(command_tokens)) if query_tokens and command_tokens else 0

        # TF-IDF косинусное сходство
        query_vec = self.vectorizer.transform([" ".join(query_tokens)])
        cmd_vec = self.vectorizer.transform([" ".join(command_tokens)])
        tfidf_sim = cosine_similarity(query_vec, cmd_vec)[0][0]

        # Комбинированная оценка
        return 0.7 * token_sim + 0.3 * tfidf_sim

    def find_best_match(self, query: str, threshold: float = 0.65) -> Optional[str]:
        """Поиск наилучшего соответствия с учетом морфологии и синонимов"""
        if not query or not self.commands:
            return None

        best_match = None
        best_score = 0.0

        for idx, cmd in enumerate(self.commands):
            score = self._get_semantic_similarity(query, cmd, idx)

            if score > best_score and score >= threshold:
                best_score = score
                best_match = cmd

        # Если точного совпадения нет, попробуем найти частичные
        if best_match is None:
            for idx, cmd in enumerate(self.commands):
                score = self._get_semantic_similarity(query, cmd, idx)
                if score > 0.4 and (best_match is None or score > best_score):
                    best_score = score
                    best_match = cmd

            if best_match:
                return f"Возможно, вы имели в виду: {best_match}"

        return best_match


def main():
    try:
        print("🔍 Умная система распознавания команд (русский язык)")
        print("Загрузка морфологического анализатора...")

        matcher = AdvancedRussianCommandMatcher()

        print("Система готова к работе. Для выхода введите 'выход'")
        while True:
            query = input("\nВаш запрос: ").strip()
            if query.lower() in ('выход', 'exit', 'quit'):
                break

            best_match = matcher.find_best_match(query)

            if best_match:
                print(f"\n✅ Результат: {best_match}")
            else:
                print("\n❌ Не удалось распознать команду")
                print("Попробуйте использовать другие формулировки")

    except Exception as e:
        print(f"\n⚠ Ошибка: {e}")
        print("Проверьте наличие файла commands.txt и установку pymorphy3")


if __name__ == "__main__":
    # Установите pymorphy3 если еще не установлен: pip install pymorphy3
    main()
  
