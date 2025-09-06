from flask import Blueprint, request, jsonify
import logging
import random

realtime_bp = Blueprint('realtime', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock event data for demonstration
MOCK_EVENTS = [
    {
        "id": "1",
        "category": "Kids",
        "time": "Saturday Morning",
        "hour": "9:00 AM",
        "title": "Kids Art & Craft Workshop",
        "description": "Creative painting and crafting session for children ages 4-10. All materials provided!",
        "location": "Community Center - 0.8 miles",
        "price": "$15/child",
        "imageUrl": None
    },
    {
        "id": "2",
        "category": "Dance",
        "time": "Every Tuesday",
        "hour": "7:30 PM",
        "title": "Beginner Salsa Dancing",
        "description": "Learn the basics of salsa in a fun, welcoming environment. No partner required!",
        "location": "Dance Studio Plus - 1.2 miles",
        "price": "$20/class",
        "imageUrl": None
    },
    {
        "id": "3",
        "category": "Outdoor",
        "time": "This Sunday",
        "hour": "10:00 AM",
        "title": "Family Nature Walk",
        "description": "Guided nature walk through Golden Gate Park with activities for kids.",
        "location": "Golden Gate Park - 2.1 miles",
        "price": "Free",
        "imageUrl": None
    },
    {
        "id": "4",
        "category": "Community",
        "time": "Next Friday",
        "hour": "6:00 PM",
        "title": "Neighborhood BBQ",
        "description": "Annual community gathering with food, games, and live music for all ages.",
        "location": "Mission Park - 0.5 miles",
        "price": "Free",
        "imageUrl": None
    },
    {
        "id": "5",
        "category": "Educational",
        "time": "Wednesday",
        "hour": "4:00 PM",
        "title": "Science Museum Workshop",
        "description": "Interactive STEM workshop for families featuring robotics and experiments.",
        "location": "Science Museum - 3.2 miles",
        "price": "$12/person",
        "imageUrl": None
    },
    {
        "id": "6",
        "category": "Fitness",
        "time": "Daily",
        "hour": "6:30 AM",
        "title": "Morning Yoga in the Park",
        "description": "Start your day with peaceful yoga sessions suitable for all skill levels.",
        "location": "Dolores Park - 1.8 miles",
        "price": "$10/class",
        "imageUrl": None
    },
    {
        "id": "7",
        "category": "Kids",
        "time": "Saturday Afternoon",
        "hour": "2:00 PM",
        "title": "Children's Story Time",
        "description": "Interactive storytelling session with puppets and activities for ages 3-8.",
        "location": "Public Library - 1.0 miles",
        "price": "Free",
        "imageUrl": None
    },
    {
        "id": "8",
        "category": "Community",
        "time": "Sunday Morning",
        "hour": "11:00 AM",
        "title": "Farmers Market",
        "description": "Fresh local produce, artisan goods, and live music in the town square.",
        "location": "Town Square - 0.3 miles",
        "price": "Free",
        "imageUrl": None
    }
]

@realtime_bp.route('/events', methods=['GET'])
def get_events():
    """Get nearby events based on location and filters"""
    try:
        # Get query parameters
        zip_code = request.args.get('zip', '94102')  # Default to SF zip
        radius = request.args.get('radius', 10, type=int)
        category = request.args.get('category', None)
        
        # Filter events by category if specified
        events = MOCK_EVENTS.copy()
        if category and category.lower() != 'all events':
            events = [event for event in events if event['category'].lower() == category.lower()]
        
        # Simulate distance-based filtering (in a real app, this would use actual geolocation)
        # For now, we'll just return a subset based on radius
        max_events = min(len(events), radius // 2 + 3)  # Simulate fewer events for smaller radius
        events = events[:max_events]
        
        # Add some randomization to make it feel more dynamic
        if len(events) > 3:
            events = random.sample(events, min(len(events), 6))
        
        logger.info(f"Retrieved {len(events)} events for zip: {zip_code}, radius: {radius}, category: {category}")
        return jsonify(events)
        
    except Exception as e:
        logger.error(f"Error retrieving events: {str(e)}")
        return jsonify({'error': 'Failed to retrieve events'}), 500

@realtime_bp.route('/events/<event_id>', methods=['GET'])
def get_event_details(event_id):
    """Get detailed information about a specific event"""
    try:
        # Find the event by ID
        event = next((e for e in MOCK_EVENTS if e['id'] == event_id), None)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        # Add additional details for the specific event view
        detailed_event = event.copy()
        detailed_event.update({
            "fullDescription": f"{event['description']} This event is perfect for families and individuals looking to engage with their community. Registration is recommended but not required.",
            "organizer": "Community Events Team",
            "contact": "events@community.org",
            "capacity": "50 people",
            "requirements": "None - all skill levels welcome"
        })
        
        logger.info(f"Retrieved details for event: {event_id}")
        return jsonify(detailed_event)
        
    except Exception as e:
        logger.error(f"Error retrieving event details: {str(e)}")
        return jsonify({'error': 'Failed to retrieve event details'}), 500

