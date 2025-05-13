@app.route('/', methods=['GET', 'POST'])
def homepage():
    return 'homepage'

@app.route('/page1', methods=['GET', 'POST'])
def page1():
    return send_from_directory('D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype.html')

@app.route('/page2', methods=['GET', 'POST'])
def page2():
    return send_from_directory('D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype2.html')