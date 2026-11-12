#include "objects.h"
#include <iostream>

void PointDemo() {
    std::cout << "\n=== 1. Point: constructors, copies, pointers ===\n";
    Point first;
    Point original(1, 2);
    Point copy(original);
    copy.Move(10, 0);
    original.Print();
    copy.Print();

    // first уже существует: здесь присваивание, не создание объекта.
    first = original;
    first.Move(0, 10);
    first.Print();
    original.Print();
    std::cout << "GetX (inline method) = " << original.GetX() << '\n';

    Point* dynamic = new Point(3, 4);
    Point* alias = nullptr;
    alias = dynamic; // Копируем адрес. Новый Point НЕ создаётся.
    alias->Move(100, 0);
    std::cout << "Same address: " << (dynamic == alias) << '\n';
    dynamic->Print();
    alias->Print();
    delete dynamic; // Удаляем общий объект ровно один раз.
    dynamic = nullptr;
    alias = nullptr;

    // first.x_ = 5;              // Ошибка: private.
    // first.PrintCoordinates(); // Ошибка: protected.
    std::cout << "Leaving PointDemo: local objects are destroyed in reverse order\n";
}

void InheritanceDemo() {
    std::cout << "\n=== 2. Inheritance: no own constructors ===\n";
    {
        PlainPoint plain;
        plain.Print();
    } // Неявный деструктор PlainPoint вызывает деструктор Point.

    std::cout << "\n=== 3. Inheritance: own constructors ===\n";
    ColoredPoint first;
    ColoredPoint colored(5, 6, 1);
    ColoredPoint copy(colored);
    copy.SetColor(2);
    copy.Move(10, 0); // Метод Move унаследован от Point.
    colored.Print();
    copy.Print();

    Point* base = &colored; // Адрес существующего потомка, без нового объекта.
    std::cout << "Through Point*: ";
    base->Print(); // Point::Print: метод невиртуальный.
    // base->SetColor(3); // Ошибка: такого метода нет в Point.

    Point sliced = colored; // Копируем только базовую часть, без color_.
    sliced.Move(100, 0);
    sliced.Print();
    colored.Print();

    Point* baseObject = new Point(7, 8);
    baseObject->Print();
    delete baseObject; // Указатель Point*, объект тоже Point — это корректно.

    ColoredPoint* derived = new ColoredPoint(9, 10, 3);
    Point* view = derived; // Аналог Base* obj = new Derived().
    view->Print();
    // У Point деструктор НЕ virtual. Удаляем через ColoredPoint*,
    // а не через view: иначе поведение было бы неопределённым.
    delete derived;
    derived = nullptr;
    view = nullptr;
    std::cout << "Leaving InheritanceDemo\n";
}

int main() {
    PointDemo();
    InheritanceDemo();
    return 0;
}
