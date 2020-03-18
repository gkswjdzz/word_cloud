from flask import Flask, request, flash, send_file
import json
import numpy as np
import matplotlib as mlp
from function import generate_mask, postStanfordnlp, generateWordCloud
import uuid
app = Flask(__name__)

#detectron2_url = 'https://ainized-detectron2.gkswjdzz.ainize.ai/predictions'

@app.route('/')
def init():
    return 

@app.route('/Image_color', methods= ['PUT', 'POST'])
def image_color():
    # form txt image 
    # option : class

    if request.method == 'POST':
        if 'jpg_path' not in request.files:
            return 'file_path not found!'

        if 'txt_path' not in request.files:
            return 'txt_path not found!'
        
        if 'lang' not in request.form :
            return 'lang not found!'
        
        f = request.files['jpg_path']
        jpg_path = f.filename
        f.save(f.filename)
        
        f = request.files['txt_path']
        txt_path = f.filename
        f.save(f.filename)

        lang = request.form['lang']
        
        print("upload complete!")

        #post detectrion2
        mask_path = generate_mask(jpg_path)
        print(mask_path)
        #post stanfordnlp
        txt = postStanfordnlp(txt_path, lang)
        # print(predictions)

        print('post to stanfordnlp success!')
        #execute word_cloud
        img_path = generateWordCloud(mask_path, txt)

        return send_file(img_path, mimetype='image/png')        
    return 'complete'

if __name__ == "__main__" :
    app.run(debug=True)