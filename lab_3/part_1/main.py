import sys

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QKeyEvent, QMouseEvent, QPaintEvent, QPainter, QPen, QResizeEvent
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class CCircle:
    """Круг сам отвечает за отрисовку и проверку попадания мыши."""

    RADIUS = 30

    def __init__(self, x: int, y: int) -> None:
        self.__center = QPoint(x, y)
        self._selected = False

    def draw(self, painter: QPainter) -> None:
        fill_color = QColor("#0000ff") if self._selected else QColor("#000000")
        border_color = QColor("#ff0000") if self._selected else QColor("#808080")
        painter.setPen(QPen(border_color, 2))
        painter.setBrush(fill_color)
        painter.drawEllipse(self.__center, self.RADIUS, self.RADIUS)

    def contains_point(self, point: QPoint) -> bool:
        dx = point.x() - self.__center.x()
        dy = point.y() - self.__center.y()
        return dx * dx + dy * dy <= self.RADIUS * self.RADIUS

    def set_selected(self, selected: bool) -> None:
        self._selected = selected

    def is_selected(self) -> bool:
        return self._selected


class CircleStorage:
    """Снаружи — перебираемая коллекция, внутри — закрытый список Python."""

    def __init__(self) -> None:
        self.__circles: list[CCircle] = []

    def add(self, circle: CCircle) -> None:
        self.__circles.append(circle)

    def clear_selection(self) -> None:
        for circle in self.__circles:
            circle.set_selected(False)

    def remove_selected(self) -> None:
        self.__circles = [circle for circle in self.__circles if not circle.is_selected()]

    def hit_test(self, point: QPoint) -> list[CCircle]:
        # Последний добавленный круг рисуется поверх остальных.
        return [circle for circle in reversed(self.__circles) if circle.contains_point(point)]

    def count(self) -> int:
        return len(self.__circles)

    def selected_count(self) -> int:
        return sum(circle.is_selected() for circle in self.__circles)

    def __len__(self) -> int:
        return len(self.__circles)

    def __iter__(self):
        return iter(self.__circles)


class PaintArea(QWidget):
    # True позволяет быстро переключить правило для пересекающихся кругов.
    SELECT_ALL_ON_HIT = False

    def __init__(self, storage: CircleStorage, status_label: QLabel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._storage = storage
        self._status_label = status_label
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._update_status()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))

        for circle in self._storage:
            circle.draw(painter)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.LeftButton:
            return

        self.setFocus()
        point = event.position().toPoint()
        hit_circles = self._storage.hit_test(point)
        ctrl_pressed = bool(event.modifiers() & Qt.ControlModifier)

        if hit_circles:
            targets = hit_circles if self.SELECT_ALL_ON_HIT else hit_circles[:1]
            if ctrl_pressed:
                for circle in targets:
                    circle.set_selected(not circle.is_selected())
            else:
                self._storage.clear_selection()
                for circle in targets:
                    circle.set_selected(True)
        else:
            if not ctrl_pressed:
                self._storage.clear_selection()
            circle = CCircle(point.x(), point.y())
            circle.set_selected(True)
            self._storage.add(circle)

        self._update_status()
        self.update()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            self._storage.remove_selected()
            self._update_status()
            self.update()
            event.accept()
            return

        super().keyPressEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._update_status()

    def _update_status(self) -> None:
        self._status_label.setText(
            f"Кругов: {len(self._storage)} | Выделено: {self._storage.selected_count()}"
        )


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ЛР №3. Часть 1. Круги на форме")
        self.resize(800, 520)
        self.setMinimumSize(400, 300)
        self._storage = CircleStorage()
        self._init_ui()

    def _init_ui(self) -> None:
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        status_label = QLabel(self)

        layout.addWidget(QLabel("ЛКМ — создать или выделить круг; Ctrl + ЛКМ — несколько; Delete — удалить."))

        self.paint_area = PaintArea(self._storage, status_label, self)
        layout.addWidget(self.paint_area, 1)
        layout.addWidget(status_label)

        self.setCentralWidget(central_widget)


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
