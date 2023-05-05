import cons
import game
import vision as vs
import utils

class MarketClosedException(Exception):
    pass

class BoxOpenException(Exception):
    pass

class ShouldntBeInMyOffersException(Exception):
    pass

class TypoException(Exception):
    pass

class WeirdExceptionSearchBox1(Exception):
    pass

class WeirdExceptionSearchBox2(Exception):
    pass

class CantFindItemBox(Exception):
    pass

class CantReadNumberException(Exception):
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def __str__(self):
        return f"{self.variable_name} should be an integer."

class CantReadNumberException(Exception):
    pass

# def exception_solver(level):
#     counter = 0
#     if level == 'Full':
#         if vs.check_if_image_on_screen(cons.THE_DEVIl_PATH):
#             raise BoxOpenException("Box is open, let's try closing it and trying again")
#
#         if not vs.check_if_image_on_screen(cons.MARKET_PATH):
#             raise MarketClosedException("Market is closed, let's try opening it")
#
#         if vs.check_if_image_on_screen(cons.OFFERS_PATH):
#             raise ShouldntBeInMyOffersException("We shouldn't be in the My Offers tab, lets go back to market")
#
#         if not vs.check_if_image_on_screen(cons.ITEMS_PATH):
#             raise CantFindItemBox("Cant find items, market might be closed, we might be in offers, or box is up")
#         try:
#             if not utils.validate_entity('coin', 'text', cons.COORDS['search_box']):
#                 raise TypoException("You made a typo while searching, let's try again")
#         except:
#             print("Vision can't find reference for item search, going through checklist")
#             if vs.check_if_image_on_screen(cons.THE_DEVIl_PATH):
#                 raise BoxOpenException("Box is open, let's try closing it and trying again")
#             if not vs.check_if_image_on_screen(cons.MARKET_PATH):
#                 raise MarketClosedException("Market is closed, let's try opening it")
#             if vs.check_if_image_on_screen(cons.ITEMS_PATH):
#                 raise Exception("This is weird, validate_entity can't find rerefence")
#
#         elif vs.check_if_image_on_screen(cons.ITEMS_PATH) and counter is 0:
#             counter += 1
#             raise WeirdExceptionSearchBox1("Price is correct but vision can't find market, trying one more time")
#
#
# def
#
#
# Exception logic 1:
# ##############################
#
# if not vs.check_if_image_on_screen(cons.ITEMS_PATH):
#     raise CantFindItemBox("Cant find items, market might be closed, we might be in offers, or box is up")
#
# ######################################################
#
# if vs.check_if_image_on_screen(cons.THE_DEVIl_PATH):
#     raise BoxOpenException("Box is open, let's try closing it and trying again")
#
# if not vs.check_if_image_on_screen(cons.MARKET_PATH):
#     raise MarketClosedException("Market is closed, let's try opening it")
#
# if vs.check_if_image_on_screen(cons.OFFERS_PATH):
#     raise ShouldntBeInMyOffersException("We shouldn't be in the My Offers tab, lets go back to market")
#
# else:
#     raise Exception("Cant figure out what's wrong with search box, shutting down")
#
# ##################################
#
# Exception logic 2:
#
# if not vs.check_if_image_on_screen(cons.ITEMS_PATH):
#     raise CantFindItemBox("Cant find items, market might be closed, we might be in offers, or box is up")
#
# if vs.check_if_image_on_screen(cons.THE_DEVIl_PATH):
#     raise BoxOpenException("Box is open, let's try closing it and trying again")
#
# if not vs.check_if_image_on_screen(cons.MARKET_PATH):
#     raise MarketClosedException("Market is closed, let's try opening it")
#
# if vs.check_if_image_on_screen(cons.OFFERS_PATH):
#     raise ShouldntBeInMyOffersException("We shouldn't be in the My Offers tab, lets go back to market")
#
# if not vs.check_if_image_on_screen(cons.ITEMS_PATH):
#     raise CantFindItemBox("Cant find items, market might be closed, we might be in offers, or box is up")
#
# else:
#     raise Exception("Cant figure out what's wrong with price setting, shutting down")
#
#
# Exception logic 3:
#
# def exceptions_searchbox_validation():
#     if not vs.check_if_image_on_screen(cons.ITEMS_PATH):
#         raise CantFindItemBox("Cant find items, market might be closed, we might be in offers, or box is up")
#     if vs.check_if_image_on_screen(cons.THE_DEVIl_PATH):
#         raise BoxOpenException("Box is open, let's try closing it and trying again")
#     if not vs.check_if_image_on_screen(cons.MARKET_PATH):
#         raise MarketClosedException("Market is closed, let's try opening it")
#     if vs.check_if_image_on_screen(cons.OFFERS_PATH):
#         raise ShouldntBeInMyOffersException("We shouldn't be in the My Offers tab, lets go back to market")
#     else:
#         raise Exception("Cant figure out what's wrong with search box, shutting down")
#
#
#
#
#
# def handle_exceptions(func, *args, **kwargs):
#     try:
#         return func(*args, **kwargs)
#     except Exception as e:
#         # Check the type of the exception and handle it accordingly
#         if isinstance(e, CantFindItemBox):
#             if vs.check_if_image_on_screen(cons.THE_DEVIl_PATH):
#                 utils.send_key('enter')
#                 time.sleep(0.1)
#             if vs.check_if_image_on_screen(cons.MARKET_PATH):
#                 game.timeout_prevention()
#                 time.sleep(0.1)
#             if vs.check_if_image_on_screen(cons.OFFERS_PATH):
#                 game.go_to_market()
#                 time.sleep(0.1)
#             if
#
#             # Handle ValueError
#             print("ValueError:", e)
#         elif isinstance(e, TypeError):
#             # Handle TypeError
#             print("TypeError:", e)
#         else:
#             # Handle other exceptions
#             print("Exception:", e)
#
