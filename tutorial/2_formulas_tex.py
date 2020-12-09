from big_ol_pile_of_manim_imports import *

class Formula(Scene):
    def construct(self):
        formula_tex=TexMobject(r"\frac{d}{dx}f(x)")
        formula_tex.scale(1.5)
        self.add(formula_tex)

class Matrix(Scene):
    def construct(self):
        formula_text_1 = TexMobject(r""" \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}""")
        formula_text_1.scale(2)
        self.add(formula_text_1)
