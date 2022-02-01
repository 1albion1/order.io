
from menu.models import Menu
class  Custom_Session():
    
    def __init__(self,request):
        self.session = request.session
        ss = self.session.get('skey')
        #kontollon nese ekziston si session
        if "skey" not in request.session:
            ss = self.session['skey'] = {}
        self.ss = ss
    
    def add(self,product):
        product_id = product.id
        if product_id not in self.ss:
            self.ss[product_id] = {
                "id": int(product.id),
                "price":float(product.price),
                "name":str(product.name),
                "description":str(product.description),
                "calories":float(product.calories),
                "meal_category":str(product.category.name),
                }
        self.save()
    
    def remove(self,product):
        product_id = product
        if product_id in self.ss:
            del self.ss[product_id]
        self.save()
        
    def get_menu_items(self):
        return self.ss

    def save(self):
        self.session.modified = True
    
    def __len__(self):
        return len(self.ss.items())
    
    def clear(self):
        ss_copy = self.ss.copy()
        for key in ss_copy:
            del self.ss[key]
        self.save()
    
    def get_total_price(self):
        total_price = 0
        for key in self.ss:
            total_price += self.ss[key]['price']
        return total_price
    
    def get_meal_ids(self):
        ids = set()
        for key in self.ss:
            ids.add(self.ss[key]['id'])
        return ids