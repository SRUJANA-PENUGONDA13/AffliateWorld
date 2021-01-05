from flask import Flask, render_template , request, redirect , url_for
import requests
import re

app = Flask(__name__)

@app.route('/')
def api_root():
    return render_template('index.html')

@app.route('/redirectedURL/<urlVal>')
def redirectedURL(urlVal):
   return render_template('redirectedURL.html', url_val=urlVal)

@app.route('/urlRedirection', methods=['POST'])
def transform_url():
    input_url = request.form['amazonURL']
    print(input_url)
    affiliate_code = "&tag=anupt-21&"
    if "amzn.to" in input_url:
        response = requests.get(input_url)
        redirected_url = response.url
    elif "amazon.in" in input_url:
        redirected_url = input_url
    else:
        return redirect(url_for('error',urlVal = '{"Response": 500, "Message": "Invalid Url"}'))
    if "&tag" in redirected_url:
        affiliate_name = re.search(r'&tag=(.*?)&', redirected_url).group(1)
        affiliate_name = "&tag" + affiliate_name + "&"
        redirected_url = redirected_url.replace(
            affiliate_name, affiliate_code)
    else:
        redirected_url = redirected_url + affiliate_code
    return redirect(url_for('redirectedURL',urlVal = redirected_url))

@app.route('/error/<urlVal>')
def error(urlVal):
    return render_template('errorURL.html', url_val=urlVal)

if __name__ == '__main__':
    app.run(debug = True)