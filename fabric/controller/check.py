from pprint import pprint
import pkg_resources

def _get_wamplets():
    """
    List installed WAMPlets.
    """
    res = {}

    for entrypoint in pkg_resources.iter_entry_points('crossbar.node'):
        try:
            e = entrypoint.load()
        except Exception as e:
            pass
        else:
            ep = {
                u'class': e,
                u'dist': entrypoint.dist.key,
                u'version': entrypoint.dist.version,
            }

            if hasattr(e, '__doc__') and e.__doc__:
                ep[u'doc'] = e.__doc__.strip()
            else:
                ep[u'doc'] = None

            res[entrypoint.name] = ep

    return res


pprint(_get_wamplets())
