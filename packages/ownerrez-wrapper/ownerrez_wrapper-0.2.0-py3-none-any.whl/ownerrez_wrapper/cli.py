#!/usr/bin/env python3
import argparse
from datetime import datetime
import json
from typing import Any
import os
from pathlib import Path
from dotenv import load_dotenv
from .api import API
from uuid import UUID

def json_serial(obj: Any) -> str:
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    if hasattr(obj, '__dict__'):
        return {k: v for k, v in obj.__dict__.items() if v is not None}
    raise TypeError(f"Type {type(obj)} not serializable")

def print_json(data: Any) -> None:
    """Print data as formatted JSON"""
    print(json.dumps(data, indent=2, default=json_serial))

def load_env():
    """Load environment variables from .env file"""
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(env_path)

def main():
    # Load environment variables from .env file
    load_env()
    
    parser = argparse.ArgumentParser(description='OwnerRez API CLI')
    
    # Authentication arguments
    parser.add_argument('--username', help='OwnerRez API username')
    parser.add_argument('--token', help='OwnerRez API token')
    
    # Commands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Properties command
    properties_parser = subparsers.add_parser('properties', help='List all properties')
    
    # Property command
    property_parser = subparsers.add_parser('property', help='Get a specific property')
    property_parser.add_argument('property_id', type=int, help='Property ID')
    
    # Bookings command
    bookings_parser = subparsers.add_parser('bookings', help='Get bookings for a property')
    bookings_parser.add_argument('property_id', type=int, help='Property ID')
    bookings_parser.add_argument('--since', type=str, help='Get bookings since date (YYYY-MM-DD)')
    
    # Booking command
    booking_parser = subparsers.add_parser('booking', help='Get a specific booking')
    booking_parser.add_argument('booking_id', type=int, help='Booking ID')
    
    # Guest command
    guest_parser = subparsers.add_parser('guest', help='Get a specific guest')
    guest_parser.add_argument('guest_id', type=int, help='Guest ID')
    
    # Check if unit is booked command
    booked_parser = subparsers.add_parser('is-booked', help='Check if a unit is currently booked')
    booked_parser.add_argument('property_id', type=int, help='Property ID')
    
    args = parser.parse_args()
    
    # Get credentials from arguments or environment
    username = args.username or os.environ.get('OWNERREZ_USERNAME')
    token = args.token or os.environ.get('OWNERREZ_TOKEN')
    
    if not username or not token:
        parser.error('Username and token must be provided via arguments, environment variables, or .env file')
    
    api = API(username=username, token=token)
    
    try:
        if args.command == 'properties':
            properties = api.getproperties()
            print_json(properties)
            
        elif args.command == 'property':
            property = api.getproperty(property_id=args.property_id)
            print_json(property)
            
        elif args.command == 'bookings':
            since_date = datetime.strptime(args.since, "%Y-%m-%d") if args.since else datetime.today()
            bookings = api.getbookings(property_id=args.property_id, since_utc=since_date)
            print_json(bookings)
            
        elif args.command == 'booking':
            booking = api.getbooking(booking_id=args.booking_id)
            print_json(booking)
            
        elif args.command == 'guest':
            guest = api.getguest(guest_id=args.guest_id)
            print_json(guest)
            
        elif args.command == 'is-booked':
            is_booked = api.isunitbooked(property_id=args.property_id)
            print_json({"is_booked": is_booked})
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main() 