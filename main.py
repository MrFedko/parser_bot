from salone_reviews import Parser
from db import db
from telegram import send_telegram


def lets_start():
    parser = Parser("Salone", '/home/chromedriver')
    db.connect()
    parser.get_all_rev()
    for item in parser.reviews_query:
        print(item)
        if not db.search_id(item['review_id']):
            db.insert(item)
            send_telegram(parser.get_message(item))

    db.connect.commit()
    db.close()


if __name__ == '__main__':
    lets_start()
