
class Parc():
    def __init__(self, billet, money, attractionliste):
        self._billet = billet
        self._money = money
        self._attractionliste = attractionliste

    def sell_tickets(self):
        pass
    
    def add_attraction(self):
        pass

    def delete_attraction(self):
        pass

    def desactivate_attraction(self):
        pass



class Employe():
    def __init__(self, name, age, fonction):
        self._name = name 
        self._age = age
        self.fonction = fonction
    
    def Travailler(self):
        pass

    def SeReposer(self):
        pass



class Employebilleterie(Employe):
    def __init__(self):
        super().__init__()
        
    def receive_money(self):
        pass

    def return_money(self):
        pass



class EmployeAttraction(Employe):
    def __init__(self):
        super().__init__()

    def start_attraction(self):
        pass

    def stop_attraction(self):
        pass



class Attraction():
    def __init__(self, name, fileposition, availableplace, attractiontype):
        self._name = name
        self._fileposition = fileposition
        self._availableplace = availableplace
        self._attractiontype = attractiontype

    def reduce_file(self):
        pass

    def show_status(self):
        pass



class Manege(Attraction):
    def __init__(self, nbr_cabine, vmax):
        super().__init__()
        self.nbr_cabine = nbr_cabine
        self.vmax = vmax 
    
    def start(self):
        pass

    def stop(self):
        pass

    def available_place(self):
        pass



class MontagneRusse(Attraction):
    def __init__(self, nbr_cabine, vmax):
        super().__init__()
        self.nbr_cabine = nbr_cabine
        self.vmax = vmax

    def start(self):
        pass

    def stop(self):
        pass

    def available_place(self):
        pass



class Caroussel(Attraction):
    def __init__(self, nbr_cabine, vmax, hmax):
        super().__init__()
        self.nbr_cabine = nbr_cabine
        self.vmax = vmax
        self.hmax = hmax
    
    def start(self):
        pass

    def stop(self):
        pass

    def available_place(self):
        pass