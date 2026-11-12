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

#endif
