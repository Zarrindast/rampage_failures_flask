from app import db, AttemptClass
from app import db, UserClass
from attempts import attempts_scraper

attempts_url = "https://en.wikipedia.org/wiki/List_of_unsuccessful_attacks_related_to_schools"

attempts_table = attempts_scraper(attempts_url)

def main():
    db.drop_all()
    db.create_all()

    for attempts_table_row in attempts_table:
        db_row_attempts = AttemptClass(
            date=attempts_table_row[0],
            location=attempts_table_row[1],
            person=None,
            description=attempts_table_row[2]
            )
        print(db_row_attempts)

        db.session.add(db_row_attempts)
        db.session.commit()
    
    db_row_users = UserClass(
        username=None,
        password=None
        )   
    print(db_row_users)
    db.session.add(db_row_users)
    db.session.commit()


if __name__ == '__main__':
    main()
