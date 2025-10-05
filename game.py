import random
import os
from typing import List, Set

# Константы и данные
MAX_ATTEMPTS = 6

WORDS = list(str(word) for word in open("words.txt", 'r').read().replace("\n", "").split(" ") if word != "")

with open("stats.txt", 'r') as f:
    stats = {
        "games_played": int(f.readline().split(" ")[-1]),
        "games_won": int(f.readline().split(" ")[-1]),
        "total_score": int(f.readline().split(" ")[-1]),
        "best_score": int(f.readline().split(" ")[-1])
    }

def main():
    print("Добро пожаловать в игру 'Виселица'!")
    print("Попробуйте угадать слово по буквам.")
    
    # Загрузка статистики
    global stats
    
    while True:
        try:
            # Выбор случайного слова
            secret_word = choose_random_word(WORDS)
            guessed_letters = set()
            attempts_left = MAX_ATTEMPTS
            game_won = False
        
            # Игровой цикл
            while attempts_left > 0:
                # Отрисовка текущего состояния игры
                clear_console()
                print(f"Попыток осталось: {attempts_left}")
                draw_gallows(attempts_left)
                print("\nСлово: " + get_masked_word(secret_word, guessed_letters))
                print("Использованные буквы: " + ", ".join(sorted(guessed_letters)))
            
                current_guess = get_user_guess(guessed_letters)

                if current_guess in secret_word:
                    print("Буква угадана!")
                else:
                    print("Неудачная попытка!")
                    attempts_left -= 1
                guessed_letters.add(current_guess)
            
                input("\nНажмите Enter чтобы продолжить...")
            
                # Проверка условий окончания игры
                if check_win(secret_word, guessed_letters):
                    game_won = True
                    break
        except Exception as e:
            print(f"Неожиданная ошибка по ходу игры!\n{e}")
            print("Выход из программы")
            break
        
        try:
            clear_console()
            if game_won:
                print("Поздравляем! Вы выиграли!")
                print(f"Загаданное слово: {secret_word}")
                score = calculate_score(secret_word, MAX_ATTEMPTS - attempts_left)
                print(f"Ваш счет: {score}")
                update_stats(True, score)
            else:
                print("К сожалению, вы проиграли.")
                print(f"Загаданное слово: {secret_word}")
                update_stats(False, 0)
                draw_gallows(0)
        
            show_stats()
        
            play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
            if play_again not in ['да', 'д', 'yes', 'y', 'sure why not', 'yeah one more wont hurt']:
                print("Спасибо за игру!")
                break
        except Exception as e:
            print(f"Ошибка при попытке завершить игру!\n{e}")
            print("Выход из программы")
            break

def clear_console():
    """Очистка консоли"""

    try:
        os.system('cls' if os.name == 'nt' else 'clear')

    except Exception as e:
        print(f"Ошибка при попытке очистки консоли:\n{e}")

    return

def choose_random_word(word_list: List[str]) -> str:
    """Выбор случайного слова из списка"""

    try:
        return random.choice(word_list)

    except Exception as e:
        print(f"Ошибка при попытке выбора случайного слова из списка:\n{e}\n(можете продолжать игру")
        return "ОШИБКА"

def get_masked_word(secret_word: str, guessed_letters: Set[str]) -> str:
    """Генерация замаскированного слова"""

    try:
        return "".join((char if char in guessed_letters else "-") for char in secret_word)

    except Exception as e:
        print(f"Ошибка при попытке создать замаскированное слово:\n{e}")
        return "ОШИБКА"

def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""

    hangman = ""

    match attempts_left:
        case 0:
            hangman = """
            --------
            |      |
            |      o7
            |     \\|/
            |      |
            |     / \\
            -
            """
        case 1:
            hangman = """
            --------
            |      |
            |      0
            |     \\|/
            |      |
            |     /
            -
            """
        case 2:
            hangman = """
            --------
            |      |
            |      0
            |     \\|/
            |      |
            |     
            -
            """
        case 3:
            hangman = """
            --------
            |      |
            |      0
            |     \\|
            |      |
            |     
            -
            """
        case 4:
            hangman = """
            --------
            |      |
            |      0
            |      |
            |      |
            |     
            -
            """
        case 5:
            hangman = """
            --------
            |      |
            |      0
            |      |
            |  
            |
            -
            """
        case 6:
            hangman = """
            --------
            |      |
            |      0
            |      
            |   
            |
            -
            """
        case _:
            hangman = "Ошибка при отрисовке виселицы"
    
    try:
        print(hangman)
    except Exception as e:
        print(f"Не удалось отрисовать виселицу!\n{e}")

    return

def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""

    try:
        while True:
            print("Угадайте букву: ", end="")
            guess = str(input()).upper()

            if len(guess) != 1:
                print("Пожалуйста, введите одну букву!")
                continue
            if not guess.isalpha():
                print("Недопустимый ввод!")
                continue
            if guess in guessed_letters:
                print("Вы уже пробовали эту букву!")
                continue

            break

        return guess

    except Exception as e:
        print(f"Ошибка при обработке ввода пользователя:\n{e}")
        return "ОШИБКА"

def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Проверка, угадано ли все слово"""

    try:
        for char in secret_word:
            if char not in guessed_letters:
                return False

        return True

    except Exception as e:
        print(f"Ошибка при проверке победы!\n{e}")
        return True

def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""

    try:
        return len(secret_word) * 10 - attempts_used * 5

    except Exception as e:
        print(f"Ошибка при вычислении счёта:\n{e}")
        return -1

def update_stats(won: bool, score: int):
    """Обновление статистики в памяти"""

    try:
        global stats

        stats["games_played"] += 1
        stats["games_won"] += 1 if won else 0
        stats["total_score"] += score
        stats["best_score"] = max(stats["best_score"], score)

        with open("stats.txt", 'w') as f:
            f.write(f'''Games played: {stats["games_played"]}
Games won: {stats["games_won"]}
Total score: {stats["total_score"]}
Best score: {stats["best_score"]}''')

    except Exception as e:
        print(f"Ошибка при обновлении статистики:\n{e}")
    
    return

def show_stats():
    """Отображение статистики"""

    try:
        global stats

        win_percentage = round(stats["games_won"] / stats["games_played"] * 100, 2)
        average_score = round(stats["total_score"] / stats["games_played"], 2)
    
        print("\n=== Статистика ===")
        print(f"Всего игр: {stats['games_played']}")
        print(f"Побед: {stats['games_won']} ({win_percentage}%)")
        print(f"Лучший счет: {stats['best_score']}")
        if win_percentage != 0: print(f"Средний счёт: {average_score}")

    except Exception as e:
        print(f"Ошибка при отображении статистики:\n{e}")

    return

if __name__ == "__main__":
    main()