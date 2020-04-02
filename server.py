from flask import Flask, request, send_file, abort
from function import generate_mask, post_stanfordnlp, generate_word_cloud
import uuid

app = Flask(__name__)

def generate(id, is_colored, out_path, png_path, txt_path, lang) :

    result_path = id + 'mask.png'
    
    generate_mask(is_colored, result_path, png_path)
    print(result_path)

    #post stanfordnlp
    txt = post_stanfordnlp(txt_path, lang)
    
    print('post to stanfordnlp success!')
    
    #execute word_cloud
    generate_word_cloud(out_path, result_path, is_colored, txt)

def upload(files, form, id):
    f = request.files['image']
    png_path = id + '.png'
    f.save(png_path)
    
    f = request.files['text']
    txt_path = id + '.txt'
    f.save(txt_path)

    lang = request.form['lang']    
        
    return png_path, txt_path, lang

@app.route('/random_color', methods= ['POST'])
def random_color():
    if request.method == 'POST':    
        if 'image' not in request.files:
            return abort(400, 'image not found!')

        if 'text' not in request.files:
            return abort(400, 'text not found!')
        
        if 'lang' not in request.form :
            return abort(400, 'lang not found!')
    
        id = str(uuid.uuid4())
        png_path, txt_path, lang = upload(request.files, request.form, id)
        
        print("upload complete!")

        out_path = id + 'out.png'
        generate(id, False, out_path, png_path, txt_path, lang)
        
        return send_file(out_path, mimetype='image/png')        
    return "Record not found", 400

@app.route('/image_color', methods= ['POST'])
def image_color():
    if request.method == 'POST':

        print(request.content_type)
        
        if 'image' not in request.files:
            print(13)
            return abort(400, 'image not found!')

        if 'text' not in request.files:
            print(23)
            return abort(400, 'text not found!')
        
        if 'lang' not in request.form :
            print(33)
            return abort(400, 'lang not found!')

        id = str(uuid.uuid4())
        png_path, txt_path, lang = upload(request.files, request.form, id)
        
        print("upload complete!")

        out_path = id + 'out.png'
        generate(id, True, out_path, png_path, txt_path, lang)
        
        return send_file(out_path, mimetype='image/png')        
    return "Record not found", 400

@app.route('/')
def main():
    return """
    <head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    </head>
    <div class=container>
    <div class="jumbotron mt-3">
    <h1>Word Cloud</h1>
    <A>Git hub repository : </A> <A href="https://github.com/gkswjdzz/word_cloud"> Word Cloud </A> <br>
    <A>API deployed on  </A> <A href="https://ainize.ai/gkswjdzz/word-cloud"> Ainize </A>
    <hr class="my-4">
    <!-- <h3>Image URL: <input id="source_url" placeholder="http://"> </h3><br> -->
    <h3> Image : <input id="image_input" accept="image/*" type="file" name="image"><h3><br>
    <h3> text : <input id="text_input" accept=".txt" type="file" name="text"><h3><br>
    
    <style>
    #submit{
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
    }
    </style>
    <h3>RUN:  <button type="submit" class="btn btn-primary btn-lg" id="submit">Submit</button></h3>
    <div id="result">
        <image id="resultImage">
        <input type='hidden' id="log" size='50'>
    </div>
    <script>
    const run = (retry_cnt=0, retry_sec=1) => {
        let formData = new FormData();

        if (retry_cnt < 3) {
            retry_cnt += 1
            retry_sec *= 2
        } else {
            throw Error('Retry Error');
        }
        url = "https://word-cloud.gkswjdzz.endpoint.ainize.ai/image-color"
        
        formData.append('image', document.getElementById('image_input').files[0])
        formData.append('text', document.getElementById('text_input').files[0])
        formData.append('lang', 'en_ewt_0.2.0')
        const options = {
            method: 'POST',
            body: formData,
        };
        <!--
        data = JSON.stringify({
            image: document.getElementById('image_input').files[0],
            text: document.getElementById('text_input').files[0],
            lang: 'en_ewt_0.2.0'
        })
        -->
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
                } else if (response.status === 500) {
                    document.getElementById("log").removeAttribute("type");
                    document.getElementById("log").value = 'internal server error!';
                    throw Error('Server Error - Debugging Please!');
                }else {
                    document.getElementById("log").removeAttribute("type");
                    document.getElementById("log").value = 'image file or text file not found!';
                    throw Error('Server Error - Debugging Please!');
                }
            })
            .then(response => response.blob())
            .then(blob => URL.createObjectURL(blob))
            .then(imageURL => {
                document.getElementById('log').setAttribute('type', 'hidden')
                document.getElementById('result').style.display = 'block';
                document.getElementById('resultImage').src = imageURL;
            })
    };
    document.getElementById('submit').onclick = () => run()
    </script>
    </div>
    </div>
"""

if __name__ == "__main__" :
    app.run(host='0.0.0.0')
    #app.run(debug=True)