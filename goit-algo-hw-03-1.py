from pathlib import Path
import argparse
import shutil
from colorama import init, Fore

# Ініціалізуємо colorama
init(autoreset=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Копіювання файлів з сортуванням за розширеннями.")  # Створюємо парсер аргументів командного рядка
    parser.add_argument("--source", type=Path, help="Шлях до вихідної директорії")  # Додаємо аргумент для шляху до вихідної директорії
    parser.add_argument("--dest", type=Path, default=Path("dist"), help="Шлях до директорії призначення (за замовчуванням 'dist')")  # Додаємо аргумент для шляху до директорії призначення
    args = parser.parse_args()  # Отримуємо аргументи

    if args.source is None:                                                         # Запитуємо шлях до вихідної директорії, якщо він не вказаний
        source_input = input("Введіть шлях до вихідної директорії: ")
        if source_input:
            args.source = Path(source_input)
        else:
            print(Fore.RED + "Шлях до вихідної директорії є обов'язковим.")         # Виводимо повідомлення про обов'язковість шляху до вихідної директорії
            exit(1)
    
    if not args.source.exists() or not args.source.is_dir():                        # Перевіряємо існування та коректність вказаної директорії
        print(Fore.RED + f"Директорія '{args.source}' не існує або не є директорією.")
        exit(1)
    
    return args

def copy_files(src, dst, parent_folder_name="", folders_created=0, files_copied=0):
    try:
        for item in src.iterdir():
            if item.is_dir():
                folders_created, files_copied = copy_files(item, dst, item.name, folders_created, files_copied)  # Рекурсивно викликаємо для піддиректорії
            else:
                ext = item.suffix[1:]                                               # Отримуємо розширення файлу без крапки
                if not ext:
                    ext = "no_extension"                                            # Якщо файл без розширення
                dest_dir = dst / ext
                if not dest_dir.exists():
                    dest_dir.mkdir(parents=True, exist_ok=True)                     # Створюємо директорію для розширення
                    folders_created += 1

                new_name = item.name                                                # Формуємо нову назву файлу, якщо такий файл вже існує
                if parent_folder_name:
                    new_name = f"{item.stem}_{parent_folder_name}{item.suffix}"

                dest_file = dest_dir / new_name

                if dest_file.exists():
                    new_name = f"{item.stem}_{parent_folder_name}{item.suffix}"
                    dest_file = dest_dir / new_name

                shutil.copy2(item, dest_file)                                       # Копіюємо файл
                files_copied += 1
    except Exception as e:
        print(Fore.RED + f"Помилка при копіюванні файлів: {e}")
    
    return folders_created, files_copied

def main():
    args = parse_args()                                                             # Отримуємо аргументи командного рядка
    args.dest.mkdir(parents=True, exist_ok=True)                                    # Створюємо директорію призначення, якщо вона не існує
    folders_created, files_copied = copy_files(args.source, args.dest)              # Копіюємо файли та отримуємо кількість створених папок та скопійованих файлів
    print(Fore.GREEN + "Операція копіювання завершена")                             # Виводимо звіт про завершення операції
    print(Fore.GREEN + f"Створено папок: {folders_created}")
    print(Fore.GREEN + f"Скопійовано файлів: {files_copied}")

if __name__ == "__main__":
    main()
