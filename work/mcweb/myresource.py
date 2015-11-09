from twisted.web import server, resource


class MyResource(resource.Resource):
    isLeaf = True

    def __init__(self, what):
        print(what)
        resource.Resource.__init__(self)

    def render_GET(self, request):
        return "<html>Hello, world!</html>"
