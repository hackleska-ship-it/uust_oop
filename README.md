# Объектно-ориентированное программирование

Баширов Максим Эдуардович, группа ПРО-209Б.

| Работа | Материалы |
| --- | --- |
| № 2 — Объекты и классы | [Сборка и запуск](lab_2/START_HERE.md) |
| № 3 — Круги на форме и MVC | [Две программы, запуск и проверки](lab_3/README.md) |

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
run.bat
```

Нужен компилятор C++: g++, MSVC (Developer Command Prompt) или Zig.
`run.bat` пересобирает программу перед запуском; `demo.bat` запускает уже
собранный `build\lab2.exe`. Компилятор и исполняемый файл не хранятся в Git.

Сборка непосредственно с g++ из корня репозитория (Linux/macOS):

```sh
g++ -std=c++11 -Wall -Wextra -pedantic -Werror lab_2/objects.cpp lab_2/main.cpp -o lab2
./lab2
```

Сборка через CMake из корня репозитория:

```sh
cmake -S lab_2 -B lab_2/build
cmake --build lab_2/build
```

CMake создаёт `lab_2/build/lab2` в Linux/macOS или `lab_2/build/lab2.exe`
в Windows. При генераторе Visual Studio файл находится в `lab_2/build/Debug/lab2.exe`.

Без аргументов программа выполняет все пять разделов. После сборки через
`run.bat` или `build.bat` отдельные разделы запускаются из папки `lab_2`:

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

## Лабораторная работа № 3 — Круги на форме и MVC

Два графических приложения на Python и PySide6:

- [Часть 1](lab_3/part_1/main.py): создание кругов, собственный контейнер,
  выделение с Ctrl, удаление и перерисовка.
- [Часть 2](lab_3/part_2/main.py): три числа, девять связанных элементов управления,
  ограничения в модели, атомарные уведомления и сохранение между запусками.

В Windows после установки зависимостей через `lab_3/setup.bat` запускаются
`lab_3/run_circles.bat` и `lab_3/run_mvc.bat`.
Команды для Windows и macOS, управление и проверки: [lab_3/README.md](lab_3/README.md).
