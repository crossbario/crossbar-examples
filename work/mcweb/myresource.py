from twisted.web import server, resource


class MyResource(resource.Resource):
    isLeaf = True

    def __init__(self, extra):
        resource.Resource.__init__(self)

    def render_GET(self, request):
        count = 10
        if 'count' in request.args:
            try:
                count = int(request.args['count'][-1])
            except ValueError:
                pass
        return '*' * count
