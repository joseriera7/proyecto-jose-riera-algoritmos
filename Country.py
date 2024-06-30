class Country:
    def __init__(self,c_id,name,code,group):
        self.name = name
        self.c_id = c_id
        self.code = code
        self.group = group
    
    def show(self):
        """
    Devuelve una representación en cadena del objeto, mostrando sus atributos.

    Returns:
        str: Una cadena con la información del objeto
    """
        return f"Country: {self.name}, ID: {self.c_id}, Group: {self.group}"
    
    def get_name_country(self):
        """
    Devuelve el nombre del pais.

    Returns:
        str: El nombre del pais.
    """
        return self.name