#!/usr/bin/env python comment

from big_ol_pile_of_manim_imports import *
from PiCreature.PiCreature import *

#code for getting the grid
class Grid(VMobject):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        VMobject.__init__(self, **kwargs)

    def generate_points(self):
        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))


class ScreenGrid(VGroup):
    CONFIG = {
        "rows":8,
        "columns":14,
        "height": FRAME_Y_RADIUS*2,
        "width": 14,
        "grid_stroke":0.5,
        "grid_color":WHITE,
        "axis_color":RED,
        "axis_stroke":2,
        "show_points":False,
        "point_radius":0,
        "labels_scale":0.5,
        "labels_buff":0,
        "number_decimals":2
    }

    def __init__(self,**kwargs):
        VGroup.__init__(self,**kwargs)
        rows=self.rows
        columns=self.columns
        grilla=Grid(width=self.width,height=self.height,rows=rows,columns=columns).set_stroke(self.grid_color,self.grid_stroke)

        vector_ii=ORIGIN+np.array((-self.width/2,-self.height/2,0))
        vector_id=ORIGIN+np.array((self.width/2,-self.height/2,0))
        vector_si=ORIGIN+np.array((-self.width/2,self.height/2,0))
        vector_sd=ORIGIN+np.array((self.width/2,self.height/2,0))

        ejes_x=Line(LEFT*self.width/2,RIGHT*self.width/2)
        ejes_y=Line(DOWN*self.height/2,UP*self.height/2)

        ejes=VGroup(ejes_x,ejes_y).set_stroke(self.axis_color,self.axis_stroke)

        divisiones_x=self.width/columns
        divisiones_y=self.height/rows

        direcciones_buff_x=[UP,DOWN]
        direcciones_buff_y=[RIGHT,LEFT]
        dd_buff=[direcciones_buff_x,direcciones_buff_y]
        vectores_inicio_x=[vector_ii,vector_si]
        vectores_inicio_y=[vector_si,vector_sd]
        vectores_inicio=[vectores_inicio_x,vectores_inicio_y]
        tam_buff=[0,0]
        divisiones=[divisiones_x,divisiones_y]
        orientaciones=[RIGHT,DOWN]
        puntos=VGroup()
        leyendas=VGroup()


        for tipo,division,orientacion,coordenada,vi_c,d_buff in zip([columns,rows],divisiones,orientaciones,[0,1],vectores_inicio,dd_buff):
            for i in range(1,tipo):
                for v_i,direcciones_buff in zip(vi_c,d_buff):
                    ubicacion=v_i+orientacion*division*i
                    punto=Dot(ubicacion,radius=self.point_radius)
                    coord=round(punto.get_center()[coordenada],self.number_decimals)
                    leyenda=TextMobject("%s"%coord).scale(self.labels_scale)
                    leyenda.next_to(punto,direcciones_buff,buff=self.labels_buff)
                    puntos.add(punto)
                    leyendas.add(leyenda)

        self.add(grilla,ejes,leyendas)
        if self.show_points==True:
            self.add(puntos)

# To watch one of these scenes, run the following:
# python -m manim example_scenes.py SquareToCircle -pl
#
# Use the flat -l for a faster rendering at a lower
# quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the n'th animation of a scene.


class OpeningManimExample(Scene):
    def construct(self):
        title = TextMobject("This is some \\LaTeX")
        basel = TexMobject(
            "\\sum_{n=1}^\\infty "
            "\\frac{1}{n^2} = \\frac{\\pi^2}{6}"
        )
        VGroup(title, basel).arrange_submobjects(DOWN)
        self.play(
            Write(title),
            FadeInFrom(basel, UP),
        )
        self.wait()

        transform_title = TextMobject("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(FadeOutAndShiftDown, basel),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = TextMobject("This is a grid")
        grid_title.scale(1.5)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeInFromDown(grid_title),
            Write(grid),
        )
        self.wait()

        grid_transform_title = TextMobject(
            "That was a non-linear function \\\\"
            "applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: p + np.array([
                np.sin(p[1]),
                np.sin(p[0]),
                0,
            ]),
            run_time=3,
        )
        self.wait()
        self.play(
            Transform(grid_title, grid_transform_title)
        )
        self.wait()


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class WarpSquare(Scene):
    def construct(self):
        square = Square()
        self.play(ApplyPointwiseFunction(
            lambda point: complex_to_R3(np.exp(R3_to_complex(point))),
            square
        ))
        self.wait()


class WriteStuff(Scene):
    def construct(self):
        example_text = TextMobject(
            "Solid State Physics",
            tex_to_color_map={"text": YELLOW}
        )
        example_tex = TexMobject(
            "\\sum_{k=2}^\\infty {1 \\over k^4} = {\\pi^8 \\over 6}",
        )
        group = VGroup(example_text, example_tex)
        group.arrange_submobjects(DOWN)
        group.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)

        self.play(Write(example_text))
        self.play(Write(example_tex))
        self.wait()

class FirstScene(Scene):
	def construct(self):
		text=TextMobject("Monit Sharma")
		self.play(Write(text))

class AddText(Scene):
    def construct(self):
        text1 = TextMobject("Term Paper Presentation")
        self.add(text1)
        self.wait(3)

class WriteText(Scene):
    def construct(self):
        text = TextMobject("Term Paper Presentation")
        text.to_corner(UR)
        text2 = TextMobject("Topic of The Term Paper")
        text2.to_edge(UL)
        text1 = TextMobject("Brillouin Zone Boundaries")
        vector = np.array([1,2,0])
        text1.move_to(vector)
        self.play(Write(text), run_time=3)
        self.wait(1)
        
        self.wait(1)
        self.play(Write(text2))
        self.wait(1)
        
        self.wait(1)
        self.play(Write(text1))
        self.wait(1)

class Intro(Scene):
    def construct(self):
        text = TextMobject("Many Fermions Body")
        self.play(Write(text))

class Positions(Scene):
    def construct(self):
        grid=ScreenGrid()
        object = Dot()
        ReferenceText=TextMobject("Monit Sharma")
        ReferenceText.move_to(3*LEFT+2*UP)
        
        #vector = np.array([-3,-2,0])
        object.move_to(ReferenceText.get_center() + 5*RIGHT)
        
        #object.to_corner(UR, buff = 1.23)
        self.add(grid,ReferenceText,object)
        self.wait()
        
        object.shift(RIGHT)
        ReferenceText.shift(RIGHT)
        self.wait()

        object.shift(DOWN)
        ReferenceText.shift(DOWN)
        self.wait()

        object.shift(LEFT)
        ReferenceText.shift(LEFT)
        self.wait()

        object.shift(UP)
        ReferenceText.shift(UP)
        self.wait()

class RotateObject(Scene):
    def construct(self):
        textM = TextMobject("Solid State")
        textC = TextMobject("Physics")
        textM.shift(UP)
        textM.rotate(PI/2)

        self.play(Write(textM),  Write(textC))
        self.wait(2)

        textM.rotate(PI/4)
        self.wait(2)

class FlipObject(Scene):
    def construct(self):
        textM = TextMobject("something")
        textM.flip(UP)
        self.play(Write(textM))
        self.wait(2)

class RenderingSettings(Scene):
    def construct(self):
        # Texts
        obj1=TextMobject("A")
        obj2=TextMobject("B").to_corner(UL)
        obj3=TextMobject("C").to_corner(UR)
        obj4=TextMobject("D").to_corner(DR)
        obj5=TextMobject("E").to_corner(DL)
        # Animations
        #
        self.play(Write(obj1)) #0
        self.wait(2)           #1
        #
        self.play(Write(obj2)) #2
        self.wait(2)           #3
        #
        self.play(Write(obj3)) #4
        self.wait(2)           #5
        #
        self.play(Write(obj4)) #6
        self.wait(2)           #7
        #
        self.play(Write(obj5)) #8
        self.wait(2)

class Introduction(Scene):
    def construct(self):
        text = TextMobject("Many Fermion Study")

class EulersFormulaWords(Scene):
    def construct(self):
        self.add(TexMobject("V-E+F=2"))

# See old_projects folder for many, many more
 
class AudioTest(Scene):
    def construct(self):
        group_dots=VGroup(*[Dot()for _ in range(3)])
        group_dots.arrange_submobjects(RIGHT)
        for dot in group_dots:
            self.add_sound("click")
            self.play(FadeIn(dot))
        self.wait()

class SVGTest(Scene):
    def construct(self):
        svg =  SVGMobject("camera")
        self.play(Write(svg))
        self.wait()

class ImageTest(Scene):
    def construct(self):
        image = ImageMobject("note")
        self.play(FadeIn(image))
        self.wait()

class NumberCreature(Scene):
    def construct(self):
        creature = SVGMobject("PiCreatures_plain")\
            .scale(2)
        creature[4].set_color(BLUE)
        self.add(creature)
#from big_ol_pile_of_manim_imports import *



class PiDice(Scene):

    def construct(self):
        Ale=Alex().to_edge(DOWN)
        palabras_ale = TextMobject("Manu \\\\You're Cute")
        self.add(Ale)
        self.play(PiCreatureSays(Ale, palabras_ale, bubble_kwargs = {"height" : 4, "width" : 6},target_mode="speaking"))
        self.wait()
        
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)

class EulersFormulaWords(Scene):
    def construct(self):
        self.add(TexMobject("V-E+F=2"))

class TheTheoremWords(Scene):
    def construct(self):
        self.add(TextMobject("The Theorem:"))

class ProofAtLastWords(Scene):
    def construct(self):
        self.add(TextMobject("The Proof At Last..."))

class DualSpanningTreeWords(Scene):
    def construct(self):
        self.add(TextMobject("Spanning trees have duals too!"))