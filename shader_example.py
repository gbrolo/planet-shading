from software_renderer import Software_Renderer
from texture_loader import texture_loader
from polygon_math import VERTEX_3

GL = Software_Renderer('render.bmp')

def init_renderer():
    GL.glInit()
    GL.glCreateWindow(1920, 1080)
    GL.glViewPort(0, 0, 1920, 1080)
    GL.glClear(0, 0, 0)
    GL.glColor(1, 1, 1)

############################################### DRAWING FUNCTIONS ############################################
def render():
    # mars
    obj = 'planet/planet.obj'
    translate = (0, 0, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1        
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    init_renderer()
    GL.glLookAt(
        VERTEX_3(20, 1, 20), 
        VERTEX_3(0, 0, 0), 
        VERTEX_3(0, 1, 0)
    )

    GL.glDrawStars()

    GL.renderIs = 'planet'
    GL.glLoadObj(obj, translate, scale, rotate, intensity)

    # phobos
    obj = 'planet/moon.obj'
    translate = (0.8, 0.3, 0)
    scale = (0.02, 0.03, 0.02)
    rotate = (0, 0, 0)
    intensity = 1        
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')

    GL.renderIs = 'moon'
    GL.glLoadObj(obj, translate, scale, rotate, intensity)

    # deimos
    obj = 'planet/moon.obj'
    translate = (0.7, -0.3, 0)
    scale = (0.015, 0.008, 0.01)
    rotate = (0, 0, 5)
    intensity = 1        
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')

    GL.renderIs = 'moon'
    GL.glLoadObj(obj, translate, scale, rotate, intensity)

    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

################################################# EXAMPLES ####################################################
render()
