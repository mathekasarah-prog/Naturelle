class Product:
    
    Store_Name = "SmartStock"
    
    def __init__(self, name, price, quantity, category):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        
        
    def info(self):
        print(f"Product:{self.name}")
        print(f"Price:Ksh {self.price}")
        print(f"Quantity: {self.quantity}")
        print(f"Category: {self.category}")
        
        
    def is_valid(self):
        if not isinstance(self.name, str) or not self.name.strip():
            return False
        
        if isinstance(self.price, bool) or not isinstance(self.price, (int, float)) or self.price <= 0:
            return False
        
        if isinstance(self.quantity, bool) or not isinstance(self.quantity,int) or self.quantity <0:
            return False
        
        if not isinstance(self.category, str) or not self.category.strip():
            return False
        
        
        return True
    
    def inventory_value(self):
        return self.price * self.quantity
    
    
products = [
    Product("Shea Glow Body Butter", 950, 25, "Body Care"),
    Product("African Black Soap", 650, 25, "Skin Care"),
    Product("Rosemary Hair Oil", 1100, 25, "Hair Care"),
    Product("Sandalwood Scented Candle", 1500, 25, "Wellness"),
    Product("Lavender Bath Set", 1800, 25, "Wellness"),
    Product("Chebe & Hibiscus Hair Butter", 1250, 25, "Hair Care"),
    Product("Aloe & Honey Leave-In Conditioner", 1100, 25, "Hair Care"),
    Product("Moringa Wellness Capsules", 1500, 25, "Wellness"),
    Product("Purify Bath Salts", 950, 25, "Wellness"),
    Product("Niacinamide Face Cream", 1350, 25, "Skin Care"),
    Product("Mango Body Butter", 1200, 32, "Body Care"),
    Product("Turmeric & Honey Natural Soap", 650, 18, "Skin Care"),
    Product("Rose & Aloe Face Mist", 850, 20, "Skin Care"),
    Product("Moringa Body Scrub", 1100, 33, "Body Care"),
    Product("Rosehip Seed Oil", 1350, 30, "Skin Care"),
    Product("Lavender & Frankincense Candle", 1500, 33, "Wellness"),
]