import io
import base64

import matplotlib
matplotlib.use('Agg')   # Para multi-thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
# Para convertir matplotlib a imagen y luego a datos binarios
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg


def graficar(x, y):
    ''' 
        Crear el grafico que se desea mostrar en HTML
    '''
    
    fig = plt.figure()
    fig.suptitle('Cantidad de provincias consultadas', fontsize=16)
    ax = fig.add_subplot()
    #ax.bar(x, y, color='orange')
    ax.bar(x, y, color=['blue','red','green','yellow','brown'])
    ax.set_ylabel("Frecuencia")
    #ax.set_xlabel("Provincia")
    ax.set_facecolor('whitesmoke')
    ax.legend()
    plt.show()

    # Convertir ese grafico en una imagen para enviar por HTTP
    # y mostrar en el HTML
    image_html = io.BytesIO()
    FigureCanvas(fig).print_png(image_html)
    plt.close(fig)  # Cerramos la imagen para que no consuma memoria del sistema
    return image_html