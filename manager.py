

class SpotNotFoundError(Exception):
    def __init__(self, not_found_spot_name):
        self.not_found_spot_name = not_found_spot_name

class OperationError(Exception):
    def __init__(self, code, reason):
        self.code = code
        self.reason = reason
    

class DeckManager:
    def __init__(self, spot_name_list: list, ): #initial_spot_status: list[dict] | None = None):
        self.deck_status = {}
        for spot_name in spot_name_list:
            self.deck_status[spot_name] = None

    def get_spot_status(self, spot_name):
        if not spot_name in self.deck_status:
            raise SpotNotFoundError(spot_name)
        return self.deck_status[spot_name]
    
    def get_all_spot_status(self):
        return self.deck_status

    def put_item(self, spot_name, new_item):
        if not spot_name in self.deck_status:
            raise SpotNotFoundError(spot_name)
        if not self.deck_status[spot_name] == None:
            raise OperationError(409, "Already item exists")

        self.deck_status[spot_name] = new_item
        return True

    def trash_item(self, spot_name):
        if not spot_name in self.deck_status:
            raise SpotNotFoundError(spot_name)
        if self.deck_status[spot_name] == None:
            raise OperationError(code = 404, reason = "No object exists")
        self.deck_status[spot_name] = None
        return True

    def move_item(self, from_spot_name, to_spot_name):
        if not from_spot_name in self.deck_status:
            raise SpotNotFoundError(from_spot_name)
        if not to_spot_name in self.deck_status:
            raise SpotNotFoundError(to_spot_name)
        
        if self.deck_status[from_spot_name] == None:
            raise OperationError(404, "Item does not exist on {}".format(from_spot_name))
        if not self.deck_status[to_spot_name] == None:
            raise OperationError(409, "Item already exists on {}".format(to_spot_name))
        transfer_obj = self.deck_status[from_spot_name]
        self.deck_status[from_spot_name] = None
        self.deck_status[to_spot_name] = transfer_obj
        return True


if __name__ == '__main__':
    print("== Set up Deck: A-H spots")
    manager = DeckManager(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    print(manager.get_all_spot_status())
    
    print("== Put item on spot A")
    manager.put_item(spot_name = 'A', new_item = {'uuid': 'hoge'})
    print(manager.get_all_spot_status())

    print("== Put item on spot C")
    manager.put_item(spot_name = 'C', new_item = {'uuid': 'aaa'})
    print(manager.get_all_spot_status())

    print("== Move item from A to H")
    manager.move_item("A", "H")
    print(manager.get_all_spot_status())

    print("== Try to move item from H to C (but will Fail!)")
    try:
        manager.move_item("H", "C")
    except OperationError as e:
        print(e.reason)
    print(manager.get_all_spot_status())