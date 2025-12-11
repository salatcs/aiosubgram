from .publisher import PublisherMethods
from .advertiser import AdvertiserMethods
from .general import GeneralMethods

class APIMethods(PublisherMethods, AdvertiserMethods, GeneralMethods):
    pass