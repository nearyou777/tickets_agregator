from shared.models import Wishlist, Tickets
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sqlalchemy.orm import Session

def add_wishlist(session:"Session" , user_id,  destination_country):
    wishlist = Wishlist(
        user_id=user_id,
         destination_country= destination_country,
    )
    session.add(wishlist)
    session.commit()


def find_offers_for_wishlist(session:"Session", wishlist_id):
    wishlist = session.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not wishlist:
        return []
    

def show_user_alerts(session:"Session", user_id):
    print(type(session.query(Wishlist).filter(Wishlist.user_id == user_id).all()))
    return session.query(Wishlist).filter(Wishlist.user_id == user_id).all()
    # Пример фильтрации предложений (по аэропорту назначения и диапазону цен)
    # offers = session.query(Tickets).filter(
    #     Tickets.DepartureAirports.like(f"%{wishlist. destination_country}%"),
    #     Tickets.Price.between(wishlist.min_price, wishlist.max_price)
    # ).all()
    