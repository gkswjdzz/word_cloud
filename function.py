from os import path
from PIL import Image
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

import os
import requests

detectron2_url = 'http://localhost/predictions'
stanfordnlp_url = 'http://localhost:81/analyze'

mpl.use('agg')

def postStanfordnlp(filepath, lang) :
    """
        input : txt file
        lang : ko => model_version : ko_kaist
    """

    files = { 
        'file' : open(filepath, 'rb')
    }
    data = {
        'model_version' : lang
    }
    predictions = requests.post(stanfordnlp_url, data= data, files=files)

    text = []
    
    ret = predictions.json()
    
    for key in ret :
        for word in ret[key] :
            if word['upos'] == 'NOUN':
                text.append(word['lemma'])

    txt = ' '.join(text)
    
    print(txt)
    print('end post stanfordnlp')
    
    return txt

def generateWordCloud(mask_path, text):
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read the whole text.
    #text = open(path.join(d, txt_path)).read()

    # read the mask image
    # taken from
    # http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
    alice_mask = np.array(Image.open(path.join(d, mask_path)))

    stopwords = set(STOPWORDS)
    stopwords.add("said")

    wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
                stopwords=stopwords, contour_width=3, contour_color='steelblue')

    # generate word cloud
    wc.generate(text)

    # store to file
    wc.to_file(path.join(d, "word.png"))

    return "word.png"
def generate_mask(jpg_path):
    print('in function generate_mask')
    predictions = postDetectron2(jpg_path)
    polygons = getPolygons(predictions, None)

    img = Image.open(jpg_path)
    img_np = np.array(img)

    print(img_np.shape)
    height, width, _ = img_np.shape

    img_np = np.array([255] * (height * width * 3), dtype=np.uint8)
    img_np = img_np.reshape(height, width, 3)
    
    xy = polygons[0]['0']
    print(xy)
    fig = plt.figure()
    ax = plt.subplot()
    ax.imshow(img_np)
    ax.axis('off')
    ax.add_patch(mpl.patches.Polygon(xy, fill=True, facecolor='k', edgecolor='none', alpha=1.0))
    
    fig.savefig('mask.png')

    return 'mask.png'

def postDetectron2(filepath) :
    files = { 'file' : open(filepath, 'rb')}
    predictions = requests.post(detectron2_url, files=files)

    return predictions.json()

def getPolygons(predictions, className) :
    polygons = []

    for idx in predictions.keys() :
        polygons.append(predictions[idx]['polygons'])

    return polygons
