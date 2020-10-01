from PyLetterB import users
import random


def get_random_users(film, order=None):
    page = random.randint(0, 20)
    userList = []
    first_time = True
    while len(userList) < 25 and page != 1:
        if not first_time:
            page = page // 2
        userList = users.get_users_by_film_per_page(film, page, order)
        first_time = False
    return userList


def get_like_dict(film, user_count=25):
    user_list = get_random_users(film)
    random.shuffle(user_list)
    film_dict = dict()
    film_list = []
    for i in range(0, user_count):
        if i < len(user_list):
            film_list.extend(users.get_user_likes_all(user_list[i]))
    for f in film_list:
        if f == film:
            continue
        elif f not in film_dict:
            film_dict[f] = 1
        else:
            film_dict[f] += 1
    return film_dict


def films_with_like_count(film, user_count=25, like_count=10, picks=3):
    film_dict = get_like_dict(film, user_count=user_count)
    small = 100
    finds = []
    found = ''
    if len(film_dict) > 0:
        for i in range(0, picks):
            for key, value in film_dict.items():
                if abs(like_count - value) < small:
                    found = key
                    small = abs(like_count - value)
            finds.append(found)
            small = 100
            film_dict.pop(found)
    return finds

