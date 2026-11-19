"""Проверки требований на настоящих Qt-виджетах и изолированном хранилище."""

import contextlib
import io
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
LAB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_ROOT))

from PySide6.QtCore import QPoint, QSettings, Qt
from PySide6.QtTest import QSignalSpy, QTest
from PySide6.QtWidgets import QApplication
from part_1.main import CCircle, CircleStorage, MainWindow as CirclesWindow
from part_2.main import MainWindow as NumbersWindow, NumberModel

APP = QApplication.instance() or QApplication([])


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = str(Path(self.temp.name) / "values.ini")
        self.model = NumberModel(QSettings(self.path, QSettings.Format.IniFormat))
        self.spy = QSignalSpy(self.model.changed)

    def test_single_initial_notification_and_noop(self):
        self.model.initialize()
        self.assertEqual(self.spy.count(), 1)
        self.model.initialize()
        self.model.set_a(0)
        self.model.set_b(0)
        self.model.set_c(0)
        self.assertEqual(self.spy.count(), 1)

    def test_permissive_a_c_and_nearest_b(self):
        self.model.initialize()
        self.model.set_a(80)
        self.assertEqual(self.model.values(), (80, 80, 80))
        self.model.set_c(20)
        self.assertEqual(self.model.values(), (20, 20, 20))
        self.model.set_c(90)
        self.model.set_b(200)
        self.assertEqual(self.model.values(), (20, 90, 90))
        self.model.set_b(-50)
        self.assertEqual(self.model.values(), (20, 20, 90))

    def test_atomic_notifications_for_many_changes(self):
        self.model.initialize()
        snapshots = []

        def observe(a, b, c):
            self.assertEqual(self.model.values(), (a, b, c))
            self.assertTrue(0 <= a <= b <= c <= 100)
            snapshots.append((a, b, c))

        self.model.changed.connect(observe)
        rng = random.Random(209)
        for _ in range(300):
            key, value = rng.choice("abc"), rng.randint(-100, 200)
            before = self.model.values()
            count = self.spy.count()
            getattr(self.model, "set_" + key)(value)
            a, b, c = self.model.values()
            self.assertTrue(0 <= a <= b <= c <= 100)
            if key == "a":
                self.assertEqual(a, min(100, max(0, value)))
            elif key == "c":
                self.assertEqual(c, min(100, max(0, value)))
            else:
                self.assertEqual(b, min(before[2], max(before[0], value)))
            self.assertEqual(self.spy.count() - count, int(self.model.values() != before))
        self.assertEqual(len(snapshots), self.spy.count() - 1)

    def test_model_accepts_only_integers(self):
        for setter in (self.model.set_a, self.model.set_b, self.model.set_c):
            for invalid in ("50", 3.5, None, True):
                with self.assertRaises(TypeError):
                    setter(invalid)
        self.assertEqual(self.spy.count(), 0)

    def test_restore_and_use_without_a_form_in_another_process(self):
        self.model.initialize()
        self.model.set_c(90)
        self.model.set_b(60)
        self.model.set_a(10)
        script = (
            "from PySide6.QtCore import QCoreApplication,QSettings;"
            "from part_2.main import NumberModel;"
            "app=QCoreApplication([]);"
            "m=NumberModel(QSettings(__import__('sys').argv[1],QSettings.IniFormat));"
            "events=[];m.changed.connect(lambda *v:events.append(v));"
            "m.initialize();assert m.values()==(10,60,90);"
            "assert events==[(10,60,90)];m.set_b(100);"
            "assert m.values()==(10,90,90);print('model without QWidget: OK')"
        )
        result = subprocess.run([sys.executable, "-c", script, self.path], cwd=LAB_ROOT,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK", result.stdout)

    def test_corrupt_persistent_values_are_normalized(self):
        settings = QSettings(self.path, QSettings.Format.IniFormat)
        settings.setValue("a", 120)
        settings.setValue("b", "not a number")
        settings.setValue("c", -10)
        settings.sync()
        model = NumberModel(settings)
        spy = QSignalSpy(model.changed)
        model.initialize()
        self.assertEqual(model.values(), (100, 100, 100))
        self.assertEqual(spy.count(), 1)


class NumbersGuiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.model = NumberModel(QSettings(str(Path(self.temp.name) / "gui.ini"), QSettings.IniFormat))
        self.output = io.StringIO()
        self.redirect = contextlib.redirect_stdout(self.output)
        self.redirect.__enter__()
        self.addCleanup(self.redirect.__exit__, None, None, None)
        self.window = NumbersWindow(self.model)
        self.addCleanup(self.window.close)
        self.model.initialize()
        self.window.show()
        APP.processEvents()

    def assert_synchronized(self):
        values = self.model.values()
        self.assertTrue(0 <= values[0] <= values[1] <= values[2] <= 100)
        for row, value in zip((self.window.row_a, self.window.row_b, self.window.row_c), values):
            self.assertEqual(row.line_edit.text(), str(value))
            self.assertEqual(row.spin_box.value(), value)
            self.assertEqual(row.slider.value(), value)

    def test_initial_form_refreshes_exactly_once(self):
        self.assertEqual(self.window.update_count, 1)
        self.assert_synchronized()

    def test_all_nine_controls_and_no_feedback(self):
        for row in (self.window.row_a, self.window.row_b, self.window.row_c):
            for control in (row.line_edit, row.spin_box, row.slider):
                old = self.model.values()
                count = self.window.update_count
                if control is row.line_edit:
                    control.setFocus()
                    control.setText("65")
                    QTest.keyClick(control, Qt.Key_Return)
                else:
                    control.setValue(35)
                APP.processEvents()
                self.assert_synchronized()
                self.assertEqual(self.window.update_count - count, int(old != self.model.values()))

    def test_invalid_empty_and_out_of_range_text_on_focus_loss(self):
        for row in (self.window.row_a, self.window.row_b, self.window.row_c):
            for text in ("", "abc", "-", "999", "-5"):
                row.line_edit.setFocus()
                APP.processEvents()
                row.line_edit.setText(text)
                row.slider.setFocus()
                APP.processEvents()
                self.assert_synchronized()

    def test_invalid_spinbox_text_is_corrected_on_focus_loss(self):
        for row in (self.window.row_a, self.window.row_b, self.window.row_c):
            for text in ("", "999", "bad"):
                row.spin_box.setFocus()
                APP.processEvents()
                row.spin_box.lineEdit().setText(text)
                row.slider.setFocus()
                APP.processEvents()
                self.assert_synchronized()
                self.assertEqual(row.spin_box.text(), str(row.getter()))

    def test_pending_line_edit_is_saved_when_window_closes(self):
        row = self.window.row_a
        row.line_edit.setFocus()
        APP.processEvents()
        row.line_edit.setText("75")
        self.window.close()
        APP.processEvents()
        self.assertEqual(self.model.values(), (75, 75, 75))


class CircleTests(unittest.TestCase):
    def test_circle_boundary_and_container_order(self):
        first, second = CCircle(100, 100), CCircle(150, 100)
        self.assertTrue(first.contains_point(QPoint(130, 100)))
        self.assertFalse(first.contains_point(QPoint(131, 100)))
        storage = CircleStorage()
        storage.add(first)
        storage.add(second)
        self.assertEqual(list(storage), [first, second])
        self.assertEqual(storage.hit_test(QPoint(125, 100)), [second, first])
        first.set_selected(True)
        storage.remove_selected()
        self.assertEqual(list(storage), [second])

    def setUp(self):
        self.window = CirclesWindow()
        self.addCleanup(self.window.close)
        self.window.show()
        APP.processEvents()
        self.area = self.window.paint_area
        self.storage = self.window._storage

    def click(self, x, y, ctrl=False):
        QTest.mouseClick(self.area, Qt.LeftButton,
                         Qt.ControlModifier if ctrl else Qt.NoModifier, QPoint(x, y))
        APP.processEvents()

    def test_creation_selection_ctrl_toggle_and_delete(self):
        self.click(100, 100)
        self.click(150, 100)
        self.assertEqual(len(self.storage), 2)
        self.click(125, 100)
        self.assertEqual([c.is_selected() for c in self.storage], [False, True])
        self.click(100, 100, ctrl=True)
        self.assertEqual(self.storage.selected_count(), 2)
        self.click(100, 100, ctrl=True)
        self.assertEqual(self.storage.selected_count(), 1)
        QTest.keyClick(self.area, Qt.Key_Delete)
        self.assertEqual(len(self.storage), 1)
        self.assertEqual(self.storage.selected_count(), 0)

    def test_alternative_overlap_rule_and_resize(self):
        self.click(100, 100)
        self.click(150, 100)
        self.area.SELECT_ALL_ON_HIT = True
        self.click(125, 100)
        self.assertEqual(self.storage.selected_count(), 2)
        self.window.resize(1000, 700)
        APP.processEvents()
        self.assertEqual(len(self.storage), 2)
        image = self.area.grab().toImage()
        self.assertEqual(image.pixelColor(150, 100).name(), "#0000ff")
        self.assertEqual(image.pixelColor(400, 200).name(), "#ffffff")
        QTest.keyClick(self.area, Qt.Key_Delete)
        self.assertEqual(len(self.storage), 0)

    def test_right_click_does_not_create_a_circle(self):
        QTest.mouseClick(self.area, Qt.RightButton, Qt.NoModifier, QPoint(200, 100))
        self.assertEqual(len(self.storage), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
