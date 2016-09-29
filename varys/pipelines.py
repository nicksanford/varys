from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import ScrapedSephoraProduct, ScrapedSephoraReview, db_connect

class VarysPipeline(object):
    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        now = str(datetime.now())
        item_type = item.__class__.__name__
        item.update({'inserted_at': now, 'updated_at': now})

        if item_type == 'SephoraProduct':
            record = ScrapedSephoraProduct(**item)
        elif item_type == 'SephoraReview':
            record = ScrapedSephoraReview(**item)
        else:
            raise

        try:
            session.add(record)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
