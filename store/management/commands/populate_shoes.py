from django.core.management.base import BaseCommand
from store.models import Shoe
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the database with sample shoe data'

    def handle(self, *args, **kwargs):
        shoes_data = [
            # Nike records (Brand ID: 1) - 13 records
            {"name": "Nike Air Force 1", "brand_id": 1, "price": 90.00,
                "description": "Classic style shoe by Nike."},
            {"name": "Nike Air Max 90", "brand_id": 1, "price": 120.00,
                "description": "Iconic design with a visible Air unit."},
            {"name": "Nike Air VaporMax", "brand_id": 1, "price": 180.00,
                "description": "Lightweight and cushioned performance shoe."},
            {"name": "Nike React Infinity Run", "brand_id": 1, "price": 160.00,
                "description": "Designed for long-distance comfort and injury prevention."},
            {"name": "Nike ZoomX Vaporfly", "brand_id": 1, "price": 250.00,
                "description": "Elite racing shoe with maximum energy return."},
            {"name": "Nike Blazer Mid", "brand_id": 1, "price": 100.00,
                "description": "Retro basketball-inspired style."},
            {"name": "Nike Air Huarache", "brand_id": 1, "price": 110.00,
                "description": "Sleek design with cushioned support."},
            {"name": "Nike Free Run", "brand_id": 1, "price": 80.00,
                "description": "Minimalistic design for natural movement."},
            {"name": "Nike Pegasus Trail", "brand_id": 1, "price": 130.00,
                "description": "Trail-ready shoe with durable traction."},
            {"name": "Nike LeBron Soldier", "brand_id": 1, "price": 140.00,
                "description": "High-performance basketball shoe."},
            {"name": "Nike SB Dunk Low", "brand_id": 1, "price": 110.00,
                "description": "Skate-inspired style with vibrant colorways."},
            {"name": "Nike Air Zoom Pegasus", "brand_id": 1, "price": 120.00,
                "description": "Reliable everyday running shoe."},
            {"name": "Nike Metcon 7", "brand_id": 1, "price": 130.00,
                "description": "Training shoe for CrossFit and high-intensity workouts."},

            # Adidas records (Brand ID: 2) - 12 records
            {"name": "Adidas Superstar", "brand_id": 2, "price": 85.00,
                "description": "Iconic shell-toe design with classic style."},
            {"name": "Adidas Stan Smith", "brand_id": 2, "price": 75.00,
                "description": "Timeless minimalist sneaker."},
            {"name": "Adidas Ultraboost 22", "brand_id": 2, "price": 180.00,
                "description": "Cushioned running shoe with energy-returning Boost technology."},
            {"name": "Adidas NMD_R1", "brand_id": 2, "price": 130.00,
                "description": "Modern design with urban street style."},
            {"name": "Adidas Gazelle", "brand_id": 2, "price": 80.00,
                "description": "Vintage-inspired silhouette with modern updates."},
            {"name": "Adidas Samba", "brand_id": 2, "price": 70.00,
                "description": "Classic indoor soccer shoe with retro flair."},
            {"name": "Adidas Yeezy Boost 350", "brand_id": 2, "price": 220.00,
                "description": "Limited edition collaboration with cutting-edge design."},
            {"name": "Adidas ZX 2K Boost", "brand_id": 2, "price": 150.00,
                "description": "Fusion of retro style and modern technology."},
            {"name": "Adidas EQT Support", "brand_id": 2, "price": 100.00,
                "description": "Engineered for stability and support."},
            {"name": "Adidas Continental 80", "brand_id": 2, "price": 90.00,
                "description": "Retro running style with modern comfort."},
            {"name": "Adidas Adilette Slides", "brand_id": 2, "price": 35.00,
                "description": "Comfortable and stylish leisure footwear."},
            {"name": "Adidas Harden Vol. 5", "brand_id": 2, "price": 140.00,
                "description": "Basketball shoe with innovative design for performance."},

            # New Balance records (Brand ID: 3) - 12 records
            {"name": "New Balance 574", "brand_id": 3, "price": 80.00,
                "description": "Iconic casual sneaker with timeless design."},
            {"name": "New Balance 990v5", "brand_id": 3, "price": 175.00,
                "description": "Premium quality and comfort in a classic silhouette."},
            {"name": "New Balance Fresh Foam 1080", "brand_id": 3, "price": 150.00,
                "description": "Cushioned for long-distance running with a smooth ride."},
            {"name": "New Balance 997H", "brand_id": 3, "price": 95.00,
                "description": "Modern take on the classic 997 design."},
            {"name": "New Balance 880v11", "brand_id": 3, "price": 130.00,
                "description": "Versatile running shoe with responsive cushioning."},
            {"name": "New Balance 840v4", "brand_id": 3, "price": 100.00,
                "description": "Balanced cushioning for everyday use."},
            {"name": "New Balance 608v5", "brand_id": 3, "price": 65.00,
                "description": "Reliable work and casual training shoe."},
            {"name": "New Balance 2002R", "brand_id": 3, "price": 150.00,
                "description": "Heritage running style combined with modern comfort."},
            {"name": "New Balance 1300", "brand_id": 3, "price": 200.00,
                "description": "Premium retro running shoe with exceptional support."},
            {"name": "New Balance 1500", "brand_id": 3, "price": 180.00,
                "description": "Lightweight and responsive for performance and style."},
            {"name": "New Balance 990v4", "brand_id": 3, "price": 170.00,
                "description": "Iconic design with high performance and comfort."},
            {"name": "New Balance Minimus Trail", "brand_id": 3, "price": 140.00,
                "description": "Minimalist design ideal for trail running."},

            # Puma records (Brand ID: 4) - 13 records
            {"name": "Puma Suede Classic", "brand_id": 4, "price": 70.00,
                "description": "Iconic suede design with a timeless look."},
            {"name": "Puma Future Rider", "brand_id": 4, "price": 80.00,
                "description": "Retro-inspired running shoe with modern flair."},
            {"name": "Puma RS-X3", "brand_id": 4, "price": 110.00,
                "description": "Bold design with futuristic elements."},
            {"name": "Puma Cali", "brand_id": 4, "price": 95.00,
                "description": "Modern take on classic Californian style."},
            {"name": "Puma Thunder Spectra", "brand_id": 4, "price": 85.00,
                "description": "Vibrant and sporty design for everyday wear."},
            {"name": "Puma Ignite Flash", "brand_id": 4, "price": 100.00,
                "description": "Responsive cushioning technology for active lifestyles."},
            {"name": "Puma One", "brand_id": 4, "price": 90.00,
                "description": "Minimalistic design for everyday performance."},
            {"name": "Puma Cell Alien", "brand_id": 4, "price": 120.00,
                "description": "High-performance shoe with advanced cushioning."},
            {"name": "Puma Clyde Court", "brand_id": 4, "price": 130.00,
                "description": "Basketball-inspired innovation for dynamic play."},
            {"name": "Puma Future Rider Play On", "brand_id": 4, "price": 85.00,
                "description": "Playful twist on a classic design for a fresh look."},
            {"name": "Puma Roma", "brand_id": 4, "price": 75.00,
                "description": "Retro style updated for modern comfort."},
            {"name": "Puma LQD Cell", "brand_id": 4, "price": 95.00,
                "description": "Engineered for on-court performance with secure support."},
            {"name": "Puma Hybrid Rocket", "brand_id": 4, "price": 105.00,
                "description": "Fusion of style and speed for active lifestyles."},
        ]

        now = timezone.now()
        for data in shoes_data:
            Shoe.objects.create(
                name=data["name"],
                brand_id=data["brand_id"],
                price=data["price"],
                description=data["description"],
                # This field is auto-handled by auto_now_add if set; otherwise, we provide it here.
                date_created=now
            )
        self.stdout.write(self.style.SUCCESS("Successfully populated shoes."))
