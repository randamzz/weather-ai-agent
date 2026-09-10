class AgentContext:

    def __init__(self, user_request):

        self.user_request = user_request

        self.location = None
        self.weather = None
        self.recommendation = None