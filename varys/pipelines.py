from datetime import datetime
from sqlalchemy.orm import sessionmaker
from .models import ScrapedSephoraProduct, ScrapedSephoraReview, db_connect
import logging
logger = logging.getLogger(__name__)

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
            logger.error('unimplemented item type %s', item_type)
            raise ValueError('unimplemented item type {}'.format(item_type))

        try:
            session.add(record)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error('hit exception on insterting record %s', e)
            raise ValueError('hit exception on insterting record {}'.format(e))
        finally:
            session.close()

        return item
