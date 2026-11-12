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

ColoredPoint::ColoredPoint() : Point(), color_(0) {
    std::cout << "ColoredPoint()\n";
}

ColoredPoint::ColoredPoint(int x, int y, int color)
    : Point(x, y), color_(color) {
    std::cout << "ColoredPoint(x, y, color)\n";
}

ColoredPoint::ColoredPoint(const ColoredPoint& other)
    : Point(other), color_(other.color_) {
    std::cout << "ColoredPoint(copy)\n";
}

ColoredPoint::~ColoredPoint() {
    std::cout << "~ColoredPoint\n";
}

void ColoredPoint::SetColor(int color) {
    std::cout << "ColoredPoint::SetColor\n";
    color_ = color;
}

void ColoredPoint::Print() const {
    std::cout << "ColoredPoint::Print ";
    PrintCoordinates(); // protected-метод доступен в наследнике.
    std::cout << " color=" << color_ << '\n';
    Point::Print(); // Явный вызов метода предка внутри метода потомка.
}

Circle::Circle() : center_(), radius_(1) {
    std::cout << "Circle()\n";
}

Circle::Circle(int x, int y, int radius)
    : center_(x, y), radius_(radius) {
    std::cout << "Circle(x, y, radius)\n";
}

Circle::Circle(const Circle& other)
    : center_(other.center_), radius_(other.radius_) {
    std::cout << "Circle(copy)\n";
}

Circle::~Circle() {
    std::cout << "~Circle (center is destroyed automatically after this)\n";
    // delete не нужен: center_ — непосредственное поле, а не new Point.
}

void Circle::Move(int dx, int dy) {
    std::cout << "Circle::Move\n";
    center_.Move(dx, dy);
}

void Circle::Print() const {
    std::cout << "Circle::Print radius=" << radius_ << '\n';
    center_.Print();
}

CirclePtr::CirclePtr() : center_(new Point()), radius_(1) {
    std::cout << "CirclePtr()\n";
}

CirclePtr::CirclePtr(int x, int y, int radius)
    : center_(new Point(x, y)), radius_(radius) {
    std::cout << "CirclePtr(x, y, radius)\n";
}

CirclePtr::CirclePtr(const CirclePtr& other)
    : center_(new Point(*other.center_)), radius_(other.radius_) {
    std::cout << "CirclePtr(copy: separate center)\n";
}

CirclePtr::~CirclePtr() {
    std::cout << "~CirclePtr (delete owned center now)\n";
    delete center_; // Эта точка была создана через new в конструкторе.
}

void CirclePtr::Move(int dx, int dy) {
    std::cout << "CirclePtr::Move\n";
    center_->Move(dx, dy);
}

void CirclePtr::Print() const {
    std::cout << "CirclePtr::Print radius=" << radius_ << '\n';
    center_->Print();
}
