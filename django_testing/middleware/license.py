class LicenseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("Before View Execution")

        response = self.get_response(request)

        print("After View Execution")

        return response