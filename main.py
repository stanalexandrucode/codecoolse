from datetime import datetime
from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from data import queries

app = Flask('codecool_series')
# app.secret_key = queries.random_api_key()
app.secret_key = '123'
page = 0
count = 0
column = 'rating'


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/tv-show/<id>')
def show_by_id(id):
    genres = queries.show_genre(id)
    show = queries.get_show_by_id(id)
    episode_data = queries.all_shows(id)
    return render_template('tv-show-id.html', show=show, genres=genres, episode_data=episode_data, id=id)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for("index"))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if queries.register_user(username, password, submission_time) is False:
            flash('Not registered')
        queries.register_user(username, password, submission_time)
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for("index"))
    if request.method == 'POST':
        username, typed_password = request.form.get('username'), request.form.get('password')
        user = queries.check_user(username)
        if user and queries.verify_password(typed_password, user[1]):
            session['user_id'] = user[0]
            session['username'] = username
            flash('User logged in!')
            return redirect('/')
        else:
            flash('User or Password do not match')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'user_id' not in session:
        flash('You are not logged in!')
    else:
        session.pop('user_id', None)
        session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/shows')
@app.route('/shows/most-rated')
def most_rated():
    active_page = page
    offset = page * 15
    data = queries.top_15('rating', 'DESC', offset)
    return render_template('rated.html', data=data, active_page=active_page)


@app.route('/shows/most-rated/<column_title>')
def ordered_by(column_title):
    global count
    global column
    if column_title is not None:
        column = column_title
    else:
        column = column

    if count % 2 == 0:
        order = 'DESC'
        count += 1
    else:
        order = 'ASC'
        count += 1

    active_page = page
    offset = page * 15
    data = queries.top_15(column, order, offset)

    return render_template('rated.html', data=data, active_page=active_page)


@app.route('/nextpage')
def next_page():
    global page
    global column
    page += 1
    return redirect('/shows/most-rated')


@app.route('/downpage')
def previous_page():
    global page
    global column
    if page != 0:
        page -= 1
    if page == 0:
        page = page
    return redirect('/shows/most-rated')


@app.route('/all_actors')
def all_actors():
    if request.is_json:
        data = queries.get_all_actors_query()
        return jsonify(data)
    return render_template("all-actors.html")


@app.route('/actorsDetails/<id>')
def actorsDetails(id):
    if request.is_json:
        data = queries.get_actors_details_query(id)
        return jsonify(data)
    return render_template("actors-details.html", id=id)


@app.route('/add_comment', methods=['POST', "GET"])
def add_comment():
    user_id = session['user_id']
    data = request.get_json()
    queries.insert_comment_query(data['id'], user_id, data['message'])
    return "comment added"


@app.route('/get_comment/<id>')
def get_comment(id):
    user_id = session['user_id']
    data = queries.get_comment_query(id, user_id)
    return jsonify(data)


def main():
    app.run(debug=True,
            port=8001)


if __name__ == '__main__':
    main()
