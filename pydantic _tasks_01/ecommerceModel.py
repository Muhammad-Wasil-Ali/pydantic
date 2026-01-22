from pydantic import BaseModel,Field,computed_field,model_validator,field_validator
from typing import List
from enum import Enum
import re
# Address Model
class Address(BaseModel):
    street:str
    city:str
    postal_code:str=Field(min_length=5,max_length=5)
    country:str="USA"
    

# product model

class Category(str,Enum):
    ELECTRONICS="Electronics"
    CLOTHING="Clothing"
    FOOD="Food"
    BOOKS="Books"
class Product(BaseModel):
    product_id:int=Field(strict=True)
    name:str
    price:float=Field(multiple_of=0.01)
    category:Category
    in_stock:bool

class OrderItem(BaseModel):
    product:Product
    quantity: int = Field(ge=1, le=100, strict=True)
    discount_percent: float = Field(default=0, ge=0, le=100)
    
    @computed_field
    @property
    def total_price(self)->float:
        productPrice=self.product.price*self.quantity
        discountPercentage=1-(self.discount_percent)/100
        
        return productPrice*discountPercentage


class STATUS(str,Enum):
    PENDING="Pending"
    PROCESSING="Proessing"
    SHIPPED="Shipped"
    DELIVER="Deliver"
class Order(BaseModel):
    order_id:str=Field(...,pattern=r"^ORD-\d{5}$")
    customer_name:str
    # shipping_address:Address
    items:List[OrderItem]
    status:STATUS
    
    @computed_field
    @property
    def grand_total(self)->float:
        gtotal=0
        for item in self.items:
            gtotal+=item.total_price
        
        return gtotal
    
    @model_validator(mode="after")
    def check_at_least_one_in_stock(self):
        in_stock_items=[item for item in self.items if item.product.in_stock]
        
        if len(in_stock_items)==0:
            raise ValueError("At least one item must be in stock")
        
        return self
    
    @field_validator("customer_name")
    @classmethod
    def name_to_title_class(cls,v):
        return v.title()
    
    @field_validator("order_id")
    @classmethod
    def validating_order_id_pattern(cls,v):
        pattern=r"^ORD-\d{5}$"
        
        if not re.match(pattern,v):
            raise ValueError("Order id is invalid Format shoudl be 'ORD-XXXXXX' ")
        return v
    
print("="*50)
print("Creating 4 products with differnt categories")

product1=Product(product_id=12345,name="Laptop",price=100.12,category="Electronics",in_stock=True)

product2=Product(product_id=23456,name="Apple",price=10.12,category="Food",in_stock=True)

product3=Product(product_id=34567,name="The Art Of Public Speaking",price=20.20,category="Books",in_stock=True)

product4=Product(product_id=45678,name="Nike Shirt",price=32.20,category="Clothing",in_stock=True)

print("4 products created")

print("="*50)
print("Creating 2 OrderItems")

orderItem1=OrderItem(product=product1,quantity=2)
orderItem2=OrderItem(product=product3,quantity=4)

print("Now Placing Order")

order1=Order(order_id="ORD-12345",customer_name="Muhammad wasil",status="Pending",items=[orderItem1,orderItem2])

print("Order placed successfully : ",order1)


