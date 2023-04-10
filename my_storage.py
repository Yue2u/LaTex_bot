class SimpleStorage:
    def __init__(self):
        self.data = dict()

    def set_data(self, user_id, key, value):
        """Saves user' data"""
        if user_id not in self.data:
            self.data[user_id] = dict()
        self.data[user_id][key] = value

    def get_data(self, user_id, key):
        """Returns user' data"""
        if user_id not in self.data or key not in self.data[user_id]:
            return None
        return self.data[user_id][key]

    def get_clean_data(self, user_id, key):
        """Returns user' data and deletes it"""
        if user_id not in self.data:
            return None
        return self.data[user_id].pop(key, None)
