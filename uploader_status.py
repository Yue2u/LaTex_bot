class UploaderStatus:
    def __init__(self):
        self.is_user_uploading = dict()
        self.upload_path = dict()
        self.user_uploads_count = dict()

    def start_upload(self, user_id, upload_path):
        self.is_user_uploading[user_id] = True
        self.user_uploads_count[user_id] = 0
        self.upload_path[user_id] = upload_path

    def stop_upload(self, user_id):
        self.is_user_uploading[user_id] = False

    def uploads_count(self, user_id):
        if user_id not in self.user_uploads_count:
            self.is_user_uploading[user_id] = False
            self.user_uploads_count[user_id] = 0
        return self.user_uploads_count[user_id]

    def add_uploads(self, user_id, upl_amount):
        if (
            user_id not in self.user_uploads_count
            or not self.is_user_uploading[user_id]
        ):
            return
        self.user_uploads_count[user_id] += upl_amount

    def is_uploading(self, user_id):
        if user_id not in self.is_user_uploading:
            self.is_user_uploading[user_id] = False
            self.user_uploads_count[user_id] = 0
        return self.is_user_uploading[user_id]

    def get_path(self, user_id):
        return self.upload_path[user_id]
