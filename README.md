# Объектно-ориентированное программирование

Баширов Максим Эдуардович, группа ПРО-209Б.

## Лабораторная работа № 2 — Объекты и классы

### Смысл работы

Консольное приложение на C++11. Программа демонстрирует конструкторы и
деструкторы, модификаторы доступа, копирование объектов и указателей,
наследование и два способа композиции.

### Что реализовано

| Файл | Содержание |
| --- | --- |
| [objects.h](lab_2/objects.h) | Классы Point, PlainPoint, ColoredPoint, Circle и CirclePtr |
| [objects.cpp](lab_2/objects.cpp) | Реализации методов классов |
| [main.cpp](lab_2/main.cpp) | Пять разделов демонстрации |
| [START_HERE.md](lab_2/START_HERE.md) | Сборка и запуск |
| [REQUIREMENTS.md](lab_2/REQUIREMENTS.md) | Соответствие заданию |
| [THEORY.md](lab_2/THEORY.md) | Теория и вопросы к защите |
| [EXPECTED_OUTPUT.txt](lab_2/EXPECTED_OUTPUT.txt) | Вывод полного запуска |

### Запуск

В Windows из папки `lab_2`:

```bat
build.bat
run.bat
```

Нужен компилятор C++: g++, MSVC (Developer Command Prompt) или Zig.
`run.bat` пересобирает программу перед запуском; `demo.bat` запускает уже
собранный `build\lab2.exe`. Компилятор и исполняемый файл не хранятся в Git.

Сборка непосредственно с g++:

```sh
g++ -std=c++11 -Wall -Wextra -pedantic -Werror lab_2/objects.cpp lab_2/main.cpp -o lab2
```

Также поддерживается CMake:

```sh
cmake -S lab_2 -B lab_2/build
cmake --build lab_2/build
```

Без аргументов программа выполняет все пять разделов. Для отдельного раздела:

```bat
build\lab2.exe point
build\lab2.exe plain
build\lab2.exe inheritance
build\lab2.exe value
build\lab2.exe pointer
```

### Репозиторий

```sh
git clone https://github.com/hackleska-ship-it/uust_oop.git
cd uust_oop
git log --oneline --reverse
```

История изменений доступна в [коммитах репозитория](https://github.com/hackleska-ship-it/uust_oop/commits/main/).
