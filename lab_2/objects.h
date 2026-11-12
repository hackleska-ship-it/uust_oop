#ifndef LAB2_OBJECTS_H
#define LAB2_OBJECTS_H

// Точка: данные скрыты, работать с ними можно через открытые методы.
class Point {
private:
    int x_;
    int y_;

protected:
    // Доступен самому Point и его наследникам, но не main().
    void PrintCoordinates() const;

public:
    Point();
    Point(int x, int y);
    Point(const Point& other);
    ~Point();

    // Обычное присваивание копирует оба числа. Это не конструктор.
    Point& operator=(const Point& other) = default;

    // Пример реализации метода внутри определения класса.
    int GetX() const { return x_; }

    void Move(int dx, int dy);
    void Print() const;
};

// Наследник без собственных конструкторов и деструктора — отдельный
// обязательный пример из методички. Нужные специальные методы создаст компилятор.
class PlainPoint : public Point {};

class ColoredPoint : public Point {
private:
    int color_; // Простой числовой код цвета, например 1 — красный.

public:
    ColoredPoint();
    ColoredPoint(int x, int y, int color);
    ColoredPoint(const ColoredPoint& other);
    ~ColoredPoint();

    void SetColor(int color);
    // virtual намеренно нет: сравниваем вызовы по типу указателя.
    void Print() const;
};

// Композиция по значению: center_ — часть самого объекта Circle.
class Circle {
private:
    Point center_;
    int radius_;

public:
    Circle();
    Circle(int x, int y, int radius);
    Circle(const Circle& other);
    ~Circle();
    void Move(int dx, int dy);
    void Print() const;
};

// Та же композиция, но с единоличным владением динамической точкой.
class CirclePtr {
private:
    Point* center_;
    int radius_;

public:
    CirclePtr();
    CirclePtr(int x, int y, int radius);
    CirclePtr(const CirclePtr& other);
    ~CirclePtr();
    // Не разрешаем неявное присваивание владеющих указателей.
    // Создать копию через конструктор копирования по-прежнему можно.
    CirclePtr& operator=(const CirclePtr& other) = delete;
    void Move(int dx, int dy);
    void Print() const;
};

#endif
