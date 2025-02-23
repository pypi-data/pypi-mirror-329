from typing import List
from datetime import datetime
from .restAdapter import RestAdapter
from .model import Property, Booking, Guest


class API(object):
    """
    OwnerRez API wrapper class
    """

    def __init__(self,username, token):
        """
        Initialize the OwnerRez API wrapper with the OwnerRez username and token
        :param username: OwnerRez username
        :param token: OwnerRez token
        """
        self.username = username
        self.token = token
    
    
    def getproperties(self) -> list:
        """
        Get a list of properties.
        """
        restAdapt = RestAdapter(self.username,self.token)
        results = []
        property_list = restAdapt.get(endpoint='properties')
        for prop in property_list.data['items']:
            prop = Property(**prop)
            results.append(prop)
        return results

    def getproperty(self, property_id: int) -> Property:
        """
        Get a single property by ID.
        """
        restAdapt = RestAdapter(self.username,self.token)
        property_data = restAdapt.get(endpoint=f'properties/{property_id}')
        return Property(**property_data.data)

    def getbookings(self, property_id: int, since_utc: datetime) -> List[Booking]:
        """
        Get a list of bookings for a property since a given date.
        """
        restAdapt = RestAdapter(self.username,self.token)
        results = []
        params = {'since_utc': since_utc, 'property_id': property_id}
        booking_list = restAdapt.get(endpoint='bookings', ep_params=params)
        
        for booking in booking_list.data['items']:
            booking = Booking(**booking)
            results.append(booking)
        return results
    
    def getbooking(self, booking_id: int) -> Booking:
        """
        Get a single booking by ID.
        """
        restAdapt = RestAdapter(self.username,self.token)
        booking = restAdapt.get(endpoint=f'bookings/{booking_id}')
        return Booking(**booking.data)
    
    def getguest(self, guest_id: int) -> Guest:
        """
        Get a single guest by ID.
        """
        restAdapt = RestAdapter(self.username,self.token)
        guest = restAdapt.get(endpoint=f'guests/{guest_id}')
        return Guest(**guest.data)
    
    def isunitbooked(self, property_id: int) -> bool:
        """
        Check if a unit is booked today.
        """
        today = datetime.today()
        bookings = self.getbookings(property_id=property_id, since_utc=today)
        for booking in bookings:
            # Convert string dates to datetime if they aren't already
            arrival = booking.arrival if isinstance(booking.arrival, datetime) else datetime.strptime(booking.arrival, "%Y-%m-%d")
            departure = booking.departure if isinstance(booking.departure, datetime) else datetime.strptime(booking.departure, "%Y-%m-%d")
            if arrival <= today and departure >= today:
                return True
        return False