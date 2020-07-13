import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.style as style
import io
from random import randrange as rand
from wrdcld import words_plot
import base64

def get_barplot(result):
    font = {
        'family': 'sans-serif',
        'color':  'navy',
        'weight': 'normal',
        'size': 14,
        }
    style.use('seaborn-darkgrid')
    result.pop('null')

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Sentiment Analysis for emotions", fontdict = font)
    axis.set_xlabel("Emotions", fontdict = font)
    axis.set_ylabel("Occurences", fontdict = font)
    
    x = list(i.upper() for i in result.keys())
    y = [int(i) for i in result.values()]
    axis.bar(x, y,  color=['green', 'orange', 'magenta', 'red', 'navy','cyan'])
    
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

    return pngImageB64String

def get_piechart(result):

    style.use('seaborn-darkgrid')
    labels = []
    sizes = []
    c = []
    color=['green', 'orange', 'magenta', 'red', 'navy','cyan']
    g = 0

    for i,j in result.items():
        if j>0:
            labels.append(i.upper())
            sizes.append(j)
            c.append(color[g])
        g += 1

    n = len(labels)
    
    s = sum(sizes)
    for i in range(len(labels)):
        sizes[i] = (sizes[i] / s) * 100
    
    explode = (0.1,) * n

    fig, _ = plt.subplots()
    patches, _ = plt.pie(sizes, colors=c, explode=explode, shadow=True, startangle=90)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(labels, sizes)]
    
    plt.legend(patches, labels, loc="lower left", fontsize=14)

    plt.axis('equal')
    
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

    return pngImageB64String

def get_wordcloud(r_str, num):
    fig = words_plot(r_str, num)

    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

    return pngImageB64String