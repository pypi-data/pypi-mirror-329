from dataclasses import dataclass


@dataclass
class Product:
    product_id: str = ""
    subscription: bool = False
