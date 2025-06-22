import os
from dotenv import load_dotenv
from decouple import config

# Load environment variables from .env file
load_dotenv()

# API Configuration
GROQ_API_KEY = config("GROQ_API_KEY")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

#search_engine = ConsultationSearchEngine(GOOGLE_API_KEY, GOOGLE_CSE_ID)

# LLM Configuration
MODEL_NAME = "llama3-70b-8192" #"gemma2-9b-it"

# UI Configuration
PAGE_TITLE = "E-commerce Customer Support"
PAGE_ICON = "💬"
PAGE_LAYOUT = "centered"


# Business Categories and Types
BUSINESS_CATEGORIES = {
    "Products": [
        "Online Clothing Store",
        "Gadget Shop",
        "General E-commerce Store",
        "Niche Product Seller",
        "Packaged Snacks Brand",
        "Food & Beverage Production",
        "Wig/Hair Vendor",
        "Skincare Brand",
        "Pharmacy",
        "Nutrition Brand",
        "Hardware Sales & Repairs",
        "Software Sales & Licensing",
        "Furniture Manufacturer",
        "Textile Producer",
        "Soap & Detergent Maker",
        "Agro-processor",
        "Poultry Farm",
        "Crop Farm",
        "Agricultural Tools Reseller",
        "Fish Farming",
        "Jewelry Maker",
        "Craft Supplies Seller"
    ],
    "Services": [
        "Restaurant",
        "Food Vendor",
        "Real Estate Agent",
        "Property Manager",
        "Shortlet Apartment Service",
        "Land Seller",
        "Tailor/Fashion Designer",
        "Makeup Artist",
        "Private Clinic",
        "Fitness Coach",
        "Mental Health Coach",
        "Private Tutor",
        "Online Course Creator",
        "Study Abroad Coach",
        "EdTech Platform",
        "Event Planner",
        "MC/Host",
        "DJ/Band",
        "Wedding Vendor",
        "Tax Consultant",
        "Grant Writer",
        "Bookkeeper",
        "Legal/Regulatory Consultant",
        "Web Development Agency",
        "SaaS Startup",
        "App Developer",
        "Cybersecurity Consultant",
        "Cloud & Networking Provider",
        "Business Strategy Consultant",
        "HR & Recruitment Consultant",
        "Legal Advisory",
        "Compliance Specialist",
        "Courier/Dispatch Service",
        "Trucking Company",
        "Freight Forwarding",
        "Delivery Bike Operator",
        "PR Agency",
        "Influencer Manager",
        "Content Creation Studio",
        "Podcast Producer",
        "Hotel",
        "Shortlet Manager",
        "Travel Agency",
        "Travel Abroad Consultant / Visa Agent",
        "Portrait Artist",
        "Interior Decor Artist",
        "Civil Engineer",
        "Building Contractor",
        "Electrician",
        "Plumber",
        "Surveyor",
        "Other Unique/Niche Services"
    ]
}

# Flatten business categories for backward compatibility
BUSINESS_TYPES = []
for category, types in BUSINESS_CATEGORIES.items():
    BUSINESS_TYPES.extend(types)

# Legacy business types for backward compatibility
# BUSINESS_TYPES = [
#     "e-commerce", "banking", "logistics", "health", "hospitality", "telecom",
#     "hair vendors", "food vendors", "cloth vendors", "skincare vendors", 
#     "kitchenware vendors", "real estate personnel", "gadget vendors", 
#     "phone vendors", "laptop vendors", "house rental agents", 
#     "fashion designers", "nail technicians", "makeup artists", 
#     "jewelry vendors", "bags vendors", "fashion eyeglasses vendors"
# ]

# Default Business Type
DEFAULT_BUSINESS_TYPE = "General E-commerce Store"