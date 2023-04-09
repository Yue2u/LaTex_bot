class HandlersPipeline:
    def __init__(self, tag="basic", handlers_seq=None):
        self.handlers = ()
        self.tag = tag
        if handlers_seq:
            self.handlers = handlers_seq

    def clear(self):
        self.handlers = ()

    def init_with_seq(self, handlers):
        self.handlers = handlers

    def get_handler(self, idx):
        if len(self.handlers) <= idx:
            return False
        return self.handlers[idx]

    def __len__(self):
        return len(self.handlers)
