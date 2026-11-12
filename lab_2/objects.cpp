#include "objects.h"
#include <iostream>

Point::Point() : x_(0), y_(0) {
    std::cout << "Point()\n";
}

// После двоеточия находится список инициализации полей.
Point::Point(int x, int y) : x_(x), y_(y) {
    std::cout << "Point(x, y)\n";
}

// other — существующая точка; копируем её координаты в новую.
Point::Point(const Point& other) : x_(other.x_), y_(other.y_) {
    std::cout << "Point(copy)\n";
}

Point::~Point() {
    std::cout << "~Point ";
    PrintCoordinates();
    std::cout << '\n';
}

void Point::PrintCoordinates() const {
    std::cout << '(' << x_ << ", " << y_ << ')';
}

// Пример реализации метода за пределами определения класса.
void Point::Move(int dx, int dy) {
    std::cout << "Point::Move\n";
    x_ += dx;
    y_ += dy;
}

void Point::Print() const {
    std::cout << "Point::Print ";
    PrintCoordinates();
    std::cout << '\n';
}
