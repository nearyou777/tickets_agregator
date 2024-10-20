from shared.models import Tickets
from shared.config import engine
from dotenv import load_dotenv
import os
from datetime import  timedelta
from sqlalchemy.orm import sessionmaker
load_dotenv()
Session = sessionmaker(bind=engine)

def autodelete():
    with Session() as session:

        data = session.query(Tickets).filter(Tickets.DateAdded >= Tickets.DateAdded + timedelta(days=30)).all()
        for row in data:
            print(row.DateAdded)
            if os.path.isfile(f'imgs/{row.PictureName}'):
                try:
                    os.remove(f'imgs/{row.PictureName}')
                except Exception as e:
                    print('zalupa')
        data = session.query(Tickets).filter(Tickets.DateAdded >= Tickets.DateAdded + timedelta(days=30)).delete(synchronize_session=False)
        session.commit()
       

if __name__ == '__main__':
    autodelete()