import numpy as np
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class FaresPolynomialSolver(App):
    def build(self):
        self.layout = FloatLayout()  # استخدام FloatLayout

        # إعداد لون الخلفية
        self.background_color = (0, 0, 0, 1)  # لون الخلفية (RGB + Alpha)
        with self.layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*self.background_color)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        # تحديث حجم المستطيل عند تغيير حجم الشاشة
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # إنشاء مستطيلات الإدخال
        self.inputs = []
        for i in range(8):  # دعم المعادلات من الدرجة السابعة
            input_box = TextInput(hint_text=f"Enter {chr(97 + i)}", multiline=False,
                                  size_hint=(0.8, 0.1), pos_hint={'x': 0.1, 'y': 0.8 - (i * 0.12)})
            input_box.background_color = (0.53, 0.81, 0.98, 1)  # لون سماوي
            self.inputs.append(input_box)
            self.layout.add_widget(input_box)

        # زر الحل
        solve_button = Button(text="Find Solutions", size_hint=(0.8, 0.1),
                              pos_hint={'x': 0.1, 'y': 0.1}, background_color=(0.0, 0.0, 0.5, 1), color=(1, 1, 1))
        solve_button.bind(on_press=self.solve_polynomial)
        self.layout.add_widget(solve_button)

        # مستطيل الحل
        self.result_label = Label(text="Solutions", size_hint=(0.8, 0.1),
                                  pos_hint={'x': 0.1, 'y': 0.2}, color=(1, 1, 1, 1))  # لون النص أبيض
        self.layout.add_widget(self.result_label)

        return self.layout

    def update_rect(self, instance, value):
        # تحديث حجم المستطيل الخلفي
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def solve_polynomial(self, instance):
        # قراءة القيم من المدخلات
        try:
            coefficients = [float(input_box.text) for input_box in self.inputs if input_box.text]
            roots = np.roots(coefficients)
            result = '\n'.join(map(str, roots))
            self.show_solutions(result, coefficients)  # تمرير المعاملات للحلول

        except ValueError:
            self.result_label.text = "Please Enter Correct Values"

    def show_solutions(self, result, coefficients):
        # نافذة جديدة لعرض الحلول
        solutions_layout = FloatLayout()  # استخدام FloatLayout
        solutions_label = Label(text=result, color=(1, 1, 1, 1))  # نص أبيض
        solutions_label.size_hint = (1, 0.8)
        solutions_label.pos_hint = {'x': 0, 'y': 0.2}
        solutions_layout.add_widget(solutions_label)

        graphic_button = Button(text="Graphic", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0}, background_color=(0.0, 0.0, 0.5, 1),
                                color=(1, 1, 1))
        graphic_button.bind(on_press=lambda x: self.plot_roots(coefficients, np.roots(coefficients)))  # تمرير المعاملات
        solutions_layout.add_widget(graphic_button)

        popup = Popup(title="Solutions", content=solutions_layout, size_hint=(0.8, 0.8))
        popup.open()

    def plot_roots(self, coefficients, roots):
        # إعداد القيم للرسم البياني
        x = np.linspace(-10, 10, 400)
        y = np.polyval(coefficients, x)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label='Equation')
        plt.axhline(0, color='gray', lw=0.5, ls='--')
        plt.axvline(0, color='gray', lw=0.5, ls='--')

        # رسم الجذور
        for root in roots:
            plt.plot(root, 0, 'ro')  # الجذور باللون الأحمر
            plt.text(root, 0, f' {root}', fontsize=12, verticalalignment='bottom')

        plt.title('Graphics')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid()
        plt.legend()
        plt.show()

if __name__ == '__main__':
    FaresPolynomialSolver().run()
