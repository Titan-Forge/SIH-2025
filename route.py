from app import app
@app.route('/about')
def about():
    return "about page working"
