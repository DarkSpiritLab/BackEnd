

class threadChecker:
    def __init__(self):
        self.manager = dict()

    def check_run(self, name, max_count):
        runner = self.manager[name] if name in self.manager.keys() else 0
        if runner < max_count:
            runner += 1
            return True