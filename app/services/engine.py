# Business logic: e.g., recommendation algorithms or ML calls
# Logic for generating recommendations (start with dummy data)
from typing import List, Optional
from app.database import get_supabase
from supabase import Client

FAKE_ITEMS = [
  {"id": 1, "name": "Wireless Headphones", "category": "electronics", "popularity": 85},
  {"id": 2, "name": "Running Shoes", "category": "sports", "popularity": 92},
  {"id": 3, "name": "Coffee Maker", "category": "home", "popularity": 78},
  {"id": 4, "name": "Yoga Mat", "category": "sports", "popularity": 65},
  {"id": 5, "name": "Smartphone Case", "category": "electronics", "popularity": 88},
  {"id": 6, "name": "Desk Lamp", "category": "home", "popularity": 42},
  {"id": 7, "name": "Protein Powder", "category": "health", "popularity": 76},
  {"id": 8, "name": "Backpack", "category": "fashion", "popularity": 81},
  {"id": 9, "name": "Bluetooth Speaker", "category": "electronics", "popularity": 94},
  {"id": 10, "name": "Dumbbell Set", "category": "sports", "popularity": 67},
  {"id": 11, "name": "Wall Clock", "category": "home", "popularity": 33},
  {"id": 12, "name": "Sunglasses", "category": "fashion", "popularity": 79},
  {"id": 13, "name": "Vitamins", "category": "health", "popularity": 71},
  {"id": 14, "name": "Sneakers", "category": "fashion", "popularity": 86},
  {"id": 15, "name": "Tablet", "category": "electronics", "popularity": 97},
  {"id": 16, "name": "Water Bottle", "category": "sports", "popularity": 64},
  {"id": 17, "name": "Pillow", "category": "home", "popularity": 58},
  {"id": 18, "name": "Winter Jacket", "category": "fashion", "popularity": 73},
  {"id": 19, "name": "Fitness Tracker", "category": "electronics", "popularity": 89},
  {"id": 20, "name": "Tennis Racket", "category": "sports", "popularity": 52},
  {"id": 21, "name": "Bed Sheets", "category": "home", "popularity": 61},
  {"id": 22, "name": "Handbag", "category": "fashion", "popularity": 84},
  {"id": 23, "name": "Multivitamins", "category": "health", "popularity": 69},
  {"id": 24, "name": "Smart Watch", "category": "electronics", "popularity": 95},
  {"id": 25, "name": "Basketball", "category": "sports", "popularity": 47},
  {"id": 26, "name": "Towels", "category": "home", "popularity": 38},
  {"id": 27, "name": "Scarf", "category": "fashion", "popularity": 41},
  {"id": 28, "name": "First Aid Kit", "category": "health", "popularity": 55},
  {"id": 29, "name": "Laptop", "category": "electronics", "popularity": 99},
  {"id": 30, "name": "Soccer Ball", "category": "sports", "popularity": 63},
  {"id": 31, "name": "Blanket", "category": "home", "popularity": 57},
  {"id": 32, "name": "Belt", "category": "fashion", "popularity": 36},
  {"id": 33, "name": "Essential Oils", "category": "health", "popularity": 72},
  {"id": 34, "name": "USB Drive", "category": "electronics", "popularity": 48},
  {"id": 35, "name": "Jump Rope", "category": "sports", "popularity": 44},
  {"id": 36, "name": "Curtains", "category": "home", "popularity": 29},
  {"id": 37, "name": "Watch", "category": "fashion", "popularity": 82},
  {"id": 38, "name": "Thermometer", "category": "health", "popularity": 31},
  {"id": 39, "name": "Monitor", "category": "electronics", "popularity": 77},
  {"id": 40, "name": "Gym Bag", "category": "sports", "popularity": 59},
  {"id": 41, "name": "Rug", "category": "home", "popularity": 45},
  {"id": 42, "name": "Hat", "category": "fashion", "popularity": 53},
  {"id": 43, "name": "Yoga Block", "category": "sports", "popularity": 27},
  {"id": 44, "name": "Printer", "category": "electronics", "popularity": 39},
  {"id": 45, "name": "Shampoo", "category": "health", "popularity": 62},
  {"id": 46, "name": "Cushion", "category": "home", "popularity": 34},
  {"id": 47, "name": "Necklace", "category": "fashion", "popularity": 68},
  {"id": 48, "name": "Resistance Bands", "category": "sports", "popularity": 56},
  {"id": 49, "name": "Router", "category": "electronics", "popularity": 73},
  {"id": 50, "name": "Lip Balm", "category": "health", "popularity": 25},
  {"id": 51, "name": "Vase", "category": "home", "popularity": 37},
  {"id": 52, "name": "Socks", "category": "fashion", "popularity": 49},
  {"id": 53, "name": "Foam Roller", "category": "sports", "popularity": 54},
  {"id": 54, "name": "Keyboard", "category": "electronics", "popularity": 66},
  {"id": 55, "name": "Hand Sanitizer", "category": "health", "popularity": 43},
  {"id": 56, "name": "Candle", "category": "home", "popularity": 71},
  {"id": 57, "name": "Boots", "category": "fashion", "popularity": 76},
  {"id": 58, "name": "Water Bottle", "category": "sports", "popularity": 58},
  {"id": 59, "name": "Camera", "category": "electronics", "popularity": 91},
  {"id": 60, "name": "Face Wash", "category": "health", "popularity": 47},
  {"id": 61, "name": "Photo Frame", "category": "home", "popularity": 28},
  {"id": 62, "name": "Slippers", "category": "fashion", "popularity": 42},
  {"id": 63, "name": "Boxing Gloves", "category": "sports", "popularity": 51},
  {"id": 64, "name": "Power Bank", "category": "electronics", "popularity": 88},
  {"id": 65, "name": "Toothbrush", "category": "health", "popularity": 35},
  {"id": 66, "name": "Mirror", "category": "home", "popularity": 46},
  {"id": 67, "name": "Tie", "category": "fashion", "popularity": 24},
  {"id": 68, "name": "Ski Goggles", "category": "sports", "popularity": 33},
  {"id": 69, "name": "Mouse", "category": "electronics", "popularity": 59},
  {"id": 70, "name": "Sunscreen", "category": "health", "popularity": 74},
  {"id": 71, "name": "Picture Frame", "category": "home", "popularity": 23},
  {"id": 72, "name": "Earrings", "category": "fashion", "popularity": 67},
  {"id": 73, "name": "Hiking Boots", "category": "sports", "popularity": 77},
  {"id": 74, "name": "Charger", "category": "electronics", "popularity": 82},
  {"id": 75, "name": "Moisturizer", "category": "health", "popularity": 63},
  {"id": 76, "name": "Bath Mat", "category": "home", "popularity": 19},
  {"id": 77, "name": "Gloves", "category": "fashion", "popularity": 39},
  {"id": 78, "name": "Bicycle Helmet", "category": "sports", "popularity": 55},
  {"id": 79, "name": "Speaker System", "category": "electronics", "popularity": 86},
  {"id": 80, "name": "Contact Lens Solution", "category": "health", "popularity": 32},
  {"id": 81, "name": "Bookshelf", "category": "home", "popularity": 44},
  {"id": 82, "name": "Bracelet", "category": "fashion", "popularity": 52},
  {"id": 83, "name": "Gym Gloves", "category": "sports", "popularity": 29},
  {"id": 84, "name": "HDMI Cable", "category": "electronics", "popularity": 41},
  {"id": 85, "name": "Bandages", "category": "health", "popularity": 18},
  {"id": 86, "name": "Lamp Shade", "category": "home", "popularity": 27},
  {"id": 87, "name": "Wallet", "category": "fashion", "popularity": 78},
  {"id": 88, "name": "Camping Tent", "category": "sports", "popularity": 64},
  {"id": 89, "name": "Webcam", "category": "electronics", "popularity": 57},
  {"id": 90, "name": "Protein Bars", "category": "health", "popularity": 69},
  {"id": 91, "name": "Nightstand", "category": "home", "popularity": 36},
  {"id": 92, "name": "Ring", "category": "fashion", "popularity": 48},
  {"id": 93, "name": "Fishing Rod", "category": "sports", "popularity": 43},
  {"id": 94, "name": "SD Card", "category": "electronics", "popularity": 61},
  {"id": 95, "name": "Pain Reliever", "category": "health", "popularity": 54},
  {"id": 96, "name": "Plant Pot", "category": "home", "popularity": 47},
  {"id": 97, "name": "Hairbrush", "category": "health", "popularity": 26},
  {"id": 98, "name": "Sweater", "category": "fashion", "popularity": 71},
  {"id": 99, "name": "Dumbbell Rack", "category": "sports", "popularity": 38},
  {"id": 100, "name": "E-Reader", "category": "electronics", "popularity": 62}
]

async def get_recommendations(user_id: Optional[int], limit: int = 5) -> List[dict]:
    db_error = None
    category_boost = None
    if user_id:
        try:
            supabase = get_supabase()
            response = supabase.table("user_preferences") \
                .select("preferred_category") \
                .eq("user_id", user_id) \
                .execute()
            
            if response.data:
                category_boost = response.data[0]["preferred_category"]
                print(f"DEBUG - Found category_boost for user {user_id}: '{category_boost}'")
            else:
                print(f"DEBUG - No preferences found for user {user_id} in table")

        except Exception as e:
            db_error = str(e)
            print(f"DB error (using fallback): {e}")

    def score(item):
        base: int = item["popularity"]
        if category_boost and item["category"] == category_boost:
            base += 30  # strong boost for preferred category
        return base

    sorted_items = sorted(FAKE_ITEMS, key=score, reverse=True)
    if db_error:
        sorted_items[0]["name"] = f"DEBUG ERROR: {db_error}"
    return sorted_items[:limit]