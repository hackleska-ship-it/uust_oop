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

#endif
