class Country:
    def __init__(self,c_id,name,code,group):
        self.name = name
        self.c_id = c_id
        self.code = code
        self.group = group
    
    def show(self):
        return f"Country: {self.name}, ID: {self.c_id}, Group: {self.group}"
    
    def get_name_country(self):
        return self.name