from flask import Flask, request, send_file, abort
from function import generate_mask, post_stanfordnlp, generate_word_cloud
import uuid

app = Flask(__name__)

def generate(id, is_colored, out_path, png_path, txt_path, lang, class_name, font_size) :

    result_path = id + 'mask.png'
    
    generate_mask(is_colored, result_path, png_path, class_name)
    print(result_path)

    #post stanfordnlp
    txt = post_stanfordnlp(txt_path, lang)
    
    print('post to stanfordnlp success!')
    
    #execute word_cloud
    generate_word_cloud(out_path, result_path, is_colored, txt, font_size)

def upload(files, form, id):
    f = request.files['image']
    png_path = id + '.png'
    f.save(png_path)
    
    f = request.files['text']
    txt_path = id + '.txt'
    f.save(txt_path)

    lang = request.form['lang']    
    class_name = request.form['thing']
    font_size = request.form['font_size']

    return png_path, txt_path, lang, class_name, font_size

@app.route('/random_color', methods= ['POST'])
def random_color():
    if request.method == 'POST':
        print(request.content_type)
        
        if 'image' not in request.files:
            return abort(400, 'image not found!')

        if 'text' not in request.files:
            return abort(400, 'text not found!')
        
        if 'lang' not in request.form or request.form['lang'] != 'en_ewt_0.2.0':
            return abort(400, 'lang not found!')

        if 'thing' not in request.form :
            return abort(400, 'thing not found!')

        if 'font_size' not in request.form :
            return abort(400, 'thing not found!')

        id = str(uuid.uuid4())
        png_path, txt_path, lang, class_name, font_size = upload(request.files, request.form, id)
        font_size = round(font_size)
        if 0 > font_size or font_size > 100 :
            return abort(400, 'invalid font size')
        print("upload complete!")

        out_path = id + 'out.png'
        generate(id, False, out_path, png_path, txt_path, lang, class_name, font_size)
        
        return send_file(out_path, mimetype='image/png')        
    return "Record not found", 400

@app.route('/image_color', methods= ['POST'])
def image_color():
    if request.method == 'POST':

        print(request.content_type)
        
        if 'image' not in request.files:
            return abort(400, 'image not found!')

        if 'text' not in request.files:
            return abort(400, 'text not found!')
        
        if 'lang' not in request.form or request.form['lang'] != 'en_ewt_0.2.0':
            return abort(400, 'lang not found!')

        if 'thing' not in request.form :
            return abort(400, 'thing not found!')

        if 'font_size' not in request.form :
            return abort(400, 'thing not found!')

        id = str(uuid.uuid4())
        png_path, txt_path, lang, class_name, font_size = upload(request.files, request.form, id)
        font_size = round(int(font_size))
        if 0 > font_size or font_size > 100 :
            return abort(400, 'invalid font size')
        print("upload complete!")

        out_path = id + 'out.png'
        generate(id, True, out_path, png_path, txt_path, lang, class_name, font_size)
        
        return send_file(out_path, mimetype='image/png')        
    return "Record not found", 400

@app.route('/')
def main():
    return """
    <head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>
    <div class=container>
    <div class="jumbotron mt-5">
    <h1>Word Cloud</h1>
    <A>Git hub repository : </A> <A href="https://github.com/gkswjdzz/word_cloud"> Word Cloud </A> <br>
    <A>API deployed on  </A> <A href="https://ainize.ai/gkswjdzz/word-cloud"> Ainize </A>
    <hr class="my-2">
    <h5> Image : <input id="image_input" accept="image/*" type="file" name="image"><h5>
    <h5> Text : <input id="text_input" accept=".txt" type="file" name="text"><h5><br>
    <h5> Things : <select id="things">
            <option value="person">person</option>
            <option value="bicycle">bicycle</option>
            <option value="car">car</option>
            <option value="motorcycle">motorcycle</option>
            <option value="airplane">airplane</option>
            <option value="bus">bus</option>
            <option value="train">train</option>
            <option value="truck">truck</option>
            <option value="boat">boat</option>
            <option value="traffic light">traffic light</option>
            <option value="fire hydrant">fire hydrant</option>
            <option value="street sign">street sign</option>
            <option value="stop sign">stop sign</option>
            <option value="parking meter">parking meter</option>
            <option value="bench">bench</option>
            <option value="bird">bird</option>
            <option value="cat">cat</option>
            <option value="dog">dog</option>
            <option value="horse">horse</option>
            <option value="sheep">sheep</option>
            <option value="cow">cow</option>
            <option value="elephant">elephant</option>
            <option value="bear">bear</option>
            <option value="zebra">zebra</option>
            <option value="giraffe">giraffe</option>
            <option value="hat">hat</option>
            <option value="backpack">backpack</option>
            <option value="umbrella">umbrella</option>
            <option value="shoe">shoe</option>
            <option value="eye">eye</option>
            <option value="handbag">handbag</option>
            <option value="tie">tie</option>
            <option value="suitcase">suitcase</option>
            <option value="frisbee">frisnee</option>
            <option value="skis">skis</option>
            <option value="snowboard">snowboard</option>
            <option value="sports ball">sports ball</option>
            <option value="kite">kite</option>
            <option value="baseball">baseball</option>
            <option value="baseball glove">baseball glove</option>
            <option value="skateboard">skateboard</option>
            <option value="surfboard">surfboard</option>
            <option value="tennis racket">tennis racket</option>
            <option value="bottle">bottle</option>
            <option value="plate">plate</option>
            <option value="wine glass">wine glass</option>
            <option value="cup">cup</option>
            <option value="fork">fork</option>
            <option value="knife">knife</option>
            <option value="spoon">spoon</option>
            <option value="bowl">bowl</option>
            <option value="banana">banana</option>
            <option value="apple">apple</option>
            <option value="sandwich">sandwich</option>
            <option value="orange">orange</option>
            <option value="broccoli">broccoli</option>
            <option value="carrot">carrot</option>
            <option value="hot dog">hot dog</option>
            <option value="pizza">pizza</option>
            <option value="donut">donut</option>
            <option value="cake">cake</option>
            <option value="chair">chair</option>
            <option value="couch">couch</option>
            <option value="potted">potted</option>
            <option value="bed">bed</option>
            <option value="mirror">mirror</option>
            <option value="dining table">dining table</option>
            <option value="window">window</option>
            <option value="desk">desk</option>
            <option value="toilet">toilet</option>
            <option value="door">door</option>
            <option value="tv">tv</option>
            <option value="laptop">laptop</option>
            <option value="mouse">mouse</option>
            <option value="remote">remote</option>
            <option value="keyboard">keyboard</option>
            <option value="cell phone">cell phone</option>
            <option value="microwave">microwave</option>
            <option value="oven">oven</option>
            <option value="toaster">toaster</option>
            <option value="sink">sink</option>
            <option value="refrigerator">refrigerator</option>
            <option value="blender">blender</option>
            <option value="book">book</option>
            <option value="clock">clock</option>
            <option value="vase">vase</option>
            <option value="scissors">scissors</option>
            <option value="teddy bear">teddy bear</option>
            <option value="hair drier">hair drier</option>
            <option value="toothbrush">toothbrush</option>
            <option value="hair brush">hair brush</option>
        </select><h5>
        <!--
        <input type="range" name="rangeInput" min="10" max="100" onchange="updateTextInput(this.value);">
        <input type="text" id="text_input" size=3 value="20" disabled="disabled">
        -->
        Max Font Size : <input type="range" name="rangeInput" min="0" max="100" onchange="updateTextInput(this.value);">
        <input type="text" id="textInput" size=3 value="20" disabled="disabled">
    <style>
    #submit{
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
    }
    </style>
    <h3>RUN:<button type="button" id="submit" class="btn btn-primary">
        Submit
    </button>
    </h3>
    <div id="result">
        <image id="resultImage">
        <input type='hidden' id="log" size='50'>
    </div>
    <script>
    function updateTextInput(val) {
          document.getElementById('textInput').value=val; 
        }
    const run = (retry_cnt=0, retry_sec=1) => {
        let formData = new FormData();

        if (retry_cnt < 3) {
            retry_cnt += 1
            retry_sec *= 2
        } else {
            throw Error('Retry Error');
        }
        url = "https://word-cloud.gkswjdzz.endpoint.ainize.ai/image_color"
        
        formData.append('image', document.getElementById('image_input').files[0])
        formData.append('text', document.getElementById('text_input').files[0])
        formData.append('lang', 'en_ewt_0.2.0')
        formData.append('thing', document.getElementById('things').value)
        formData.append('font_size', document.getElementById('textInput').value)
        
        const options = {
            method: 'POST',
            body: formData,
        };
        fetch(url, options)
            .then(response => {
                console.log(response)
                if (response.status === 200) {
                    return response;
                } else if (response.status === 429) {
                    console.log(`retry ${retry_cnt}th after ${retry_sec}secs ...`);
                    setTimeout(
                        () => {
                            run(retry_cnt, retry_sec)
                        }, retry_sec * 1000
                    )
                    document.getElementById('submit').removeAttribute('disabled', false);
                } else if (response.status === 500) {
                    document.getElementById("log").removeAttribute("type");
                    document.getElementById("log").value = 'internal server error!';
                    document.getElementById('submit').removeAttribute('disabled', false);
                    throw Error('Server Error - Debugging Please!');
                }else {
                    document.getElementById("log").removeAttribute("type");
                    document.getElementById("log").value = 'image file or text file not found!';
                    document.getElementById('submit').removeAttribute('disabled');
                    document.getElementById('submit').innerHTML = 'Submit';
                    throw Error('Server Error - Debugging Please!');
                }
            })
            .then(response => response.blob())
            .then(blob => URL.createObjectURL(blob))
            .then(imageURL => {
                document.getElementById('log').setAttribute('type', 'hidden')
                document.getElementById('result').style.display = 'block';
                document.getElementById('resultImage').src = imageURL;
                document.getElementById('submit').removeAttribute('disabled');
                document.getElementById('submit').innerHTML = 'Submit';
            })
    };
    document.getElementById('submit').onclick = () => {
        run();
       document.getElementById('submit').innerHTML = '<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Loading...';
       document.getElementById('submit').setAttribute('disabled', true);
    };
    
    </script>
    </div>
    </div>
"""

if __name__ == "__main__" :
    app.run(host='0.0.0.0')
    #app.run(debug=True)