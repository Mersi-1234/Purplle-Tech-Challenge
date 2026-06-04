class VisitorTracker:

    def __init__(self):
        self.visitors = {}

    def add(self, visitor_id):
        self.visitors[visitor_id] = True

    def count(self):
        return len(self.visitors)