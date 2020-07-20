from data import data_manager
import bcrypt
import os


def random_api_key():
    """
    :return: salt in secret key
    """
    return os.urandom(100)


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_show_by_id(id):
    return data_manager.execute_dml_statement('SELECT * '
                                              'FROM shows '
                                              'WHERE id = %(id)s;', {'id': id})


def username_exists(username):
    return data_manager.execute_dml_statement('SELECT * FROM users WHERE username = %(username)s;',
                                              {'username': username})


def register_user(username, text_password, submission_time):
    if username_exists(username):
        return False
    return data_manager.execute_dml_statement('INSERT INTO users (username,password,submission_time) '
                                              'VALUES (%(username)s,%(password)s,%(submission_time)s)',
                                              {"username": username,
                                               "password": encrypt_password(text_password),
                                               "submission_time": submission_time})


def check_user(username):
    return data_manager.execute_dml_statement('SELECT id, password '
                                              'FROM users '
                                              'WHERE username '
                                              'ILIKE %(username)s;', {"username": username})


def encrypt_password(password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_pass.decode("utf-8")


def verify_password(text_password, hashed_pass):
    return bcrypt.checkpw(text_password.encode("utf-8"), hashed_pass.encode("utf-8"))


def show_genre(id):
    return data_manager.execute_select('SELECT g.name '
                                       'FROM show_genres as sg '
                                       'LEFT JOIN genres as g '
                                       'ON sg.genre_id=g.id '
                                       'WHERE sg.show_id = %(id)s '
                                       'GROUP BY sg.show_id, g.name; ',
                                       {'id': id})


def top_15(sort='rating', direction='DESC', offset=0):
    return data_manager.execute_select(
        f"""SELECT shows.id, shows.title,shows.year,shows.runtime,shows.trailer, shows.homepage, shows.rating,
            string_agg(genres.name, ', ' ORDER BY name) as genres
            FROM shows
            JOIN show_genres ON shows.id=show_genres.show_id
            JOIN genres ON show_genres.genre_id=genres.id
            GROUP BY shows.id, rating
            ORDER BY {sort} {direction}  limit 15 OFFSET {offset};""", (sort, direction, offset))


def all_shows(id):
    return data_manager.execute_select('''
                                SELECT se.id as seasonid, sh.id, sh.title, sh.year, se.season_number AS no_of_seasons, se.title seasons, se.overview, COUNT(ep.episode_number) ep_no
                                FROM shows sh
                                LEFT JOIN seasons se ON sh.id = se.show_id
                                LEFT JOIN episodes ep ON se.id = ep.season_id
                                WHERE sh.id = %(id)s
                                GROUP BY sh.id, seasons, no_of_seasons, se.overview,se.id;''',
                                       {'id': id})


def get_all_actors_query():
    return data_manager.execute_select('''
    SELECT id, name
    FROM actors
    ''')


def get_actors_details_query(id):
    return data_manager.execute_select(f'''
        select actors.id as id, show_characters.character_name as character,
        shows.title as title
        from shows join show_characters
        on shows.id = show_characters.show_id
        join actors 
        on show_characters.actor_id = actors.id
        group by actors.id,show_characters.character_name,shows.title
        having actors.id = {id}''', {"id": id})


def get_comment_query(show_id, user_id):
    return data_manager.execute_select(f'''
    SELECT *
    FROM comments
    WHERE show_id = {show_id} AND user_id ={user_id}
    ''', {"show_id": show_id, "user_id": user_id})


def insert_comment_query(show_id, user_id, message):
    return data_manager.execute_dml_statement('INSERT INTO comments (show_id,user_id,message) '
                                              'VALUES (%(show_id)s,%(user_id)s,%(message)s)',
                                              {"show_id": show_id,
                                               "user_id": user_id,
                                               "message": message})
