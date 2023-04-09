class HandlerController:
    def __init__(self, pipelines_table=None):
        self.user_pipeline = dict()
        self.user_step = dict()
        self.pipelines_table = pipelines_table

    def set_pipelines_table(self, pipelines_table):
        self.pipelines_table = pipelines_table

    def add_user(self, user_id):
        self.user_pipeline[user_id] = None
        self.user_step[user_id] = 0

    def set_pipeline(self, user_id, pipeline_id):
        self.user_pipeline[user_id] = pipeline_id
        self.user_step[user_id] = 0

    def get_handler(self, user_id):
        return self.pipelines_table[self.user_pipeline[user_id]].get_handler(
            self.user_step[user_id]
        )

    def get_handler_type(self, user_id):
        if user_id not in self.user_pipeline:
            self.user_pipeline[user_id] = None
            self.user_step[user_id] = 0
        return self.user_pipeline[user_id]

    def next_handler(self, user_id):
        if (
            len(self.pipelines_table[self.user_pipeline[user_id]])
            <= self.user_step[user_id]
        ):
            self.user_pipeline[user_id] = None
            return
        self.user_step[user_id] += 1

    def complete_pipeline(self, user_id):
        self.user_pipeline[user_id] = None
        self.user_step[user_id] = 0
