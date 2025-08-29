class Schedule:
    def __init__(self, data):
        self.data = data

    def add_data(self):
        return {
            "data":f"Process adding {self.data} to database"
        }