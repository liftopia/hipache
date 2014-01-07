
import base


class DomainMatchingTestCase(base.TestCase):

    def test_wildcard(self):
        port = 2080
        self.spawn_httpd(port)
        self.register_frontend('*.foo.bar', ['http://localhost:{0}'.format(port)])
        self.assertEqual(self.http_request('test.foo.bar'), 200)
        self.assertEqual(self.http_request('pipo.foo.bar'), 200)
        self.assertEqual(self.http_request('foo.bar'), 400)

    def test_naked_domain(self):
        port = 2080
        self.spawn_httpd(port)
        self.register_frontend('foo.bar', ['http://localhost:{0}'.format(port)])
        self.assertEqual(self.http_request('foo.bar'), 200)

    def test_wildcard_priority(self):
        port = 2080
        self.spawn_httpd(port)
        self.spawn_httpd(port + 1, code=201)
        self.spawn_httpd(port + 2, code=202)
        self.spawn_httpd(port + 3, code=203)
        self.register_frontend('*.foo.bar', ['http://localhost:{0}'.format(port)])
        self.register_frontend('foo.bar', ['http://localhost:{0}'.format(port + 1)])
        self.register_frontend('pipo.foo.bar', ['http://localhost:{0}'.format(port + 2)])
        self.register_frontend('*.pipo.foo.bar', ['http://localhost:{0}'.format(port + 3)])
        self.assertEqual(self.http_request('test.foo.bar'), 200)
        self.assertEqual(self.http_request('foo.bar'), 201)
        self.assertEqual(self.http_request('pipo.foo.bar'), 202)
        self.assertEqual(self.http_request('test.pipo.foo.bar'), 203)
