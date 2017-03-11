class PMS:

    current_post = None
    data = None
    has_data = False
    fint = None
    has_unsent_data = True

    def set_fint(self, fint):
        self.fint = fint

    def set_data(self, current_post, answer_post):
        if not self.has_unsent_data and not self.has_data:
            if self.current_post != current_post:
                self.data = answer_post
                self.current_post = current_post
                self.has_data = True
                return True
        return False

    def run(self):
        if self.has_unsent_data:
            if self.fint.answer(cid = self.current_post, content = self.data):
                self.has_unsent_data = False
                return
        if self.has_data:
            if self.fint.answer(cid=self.current_post, content=self.data):
                self.has_data = False
            else:
                self.has_unsent_data = True
                self.has_data = False


