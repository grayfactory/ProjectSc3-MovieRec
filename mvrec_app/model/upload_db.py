from mvrec_app import db
from mvrec_app.model.table_model import Movies, RatingUsers
import csv

def get_movie_data():
    
    with open(app.root_path + '/model/movies_db.csv') as f:
        df = csv.reader(f)
        for n,line in enumerate(df):
            if n > 0:
            # print(line)
                recode = Movies(id=n, 
                                movie_id=int(line[0]),
                                title=line[2],
                                genre=line[3],
                                weight_rating=round(float(line[1]),3))
                db.session.add(recode)
        db.session.commit()

def get_user_data():
    print(app.root_path, '===='*40)
    with open(app.root_path + '/model/user_rating.csv') as f:
        df = csv.reader(f)
        for n, line in enumerate(df):
            print(line)
            if n > 1:
                user = RatingUsers(
                                    id=n,
                                    user_id=int(line[0]),
                                    movie_id=int(line[1]),
                                    rating=float(line[2])
                                    )
                db.session.add(user)
        db.session.commit()

def create_table():
    db.create_all()