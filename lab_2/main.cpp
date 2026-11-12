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

int main() {
    PointDemo();
    return 0;
}
