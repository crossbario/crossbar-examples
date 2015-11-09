from twisted.web import server, resource


class MyResouce(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return "<html>Hello, world!</html>"
