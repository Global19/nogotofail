r'''
Copyright 2014 Google Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from nogotofail.mitm.connection.handlers.connection import LoggingHandler
from nogotofail.mitm.connection.handlers.connection import handlers
from nogotofail.mitm.connection.handlers.store import handler


@handler(handlers, default=False)
class DropTLS(LoggingHandler):

    name = "droptls"
    description = "Drops TLS connections but lets SSLv3 through"
    ALERT = "\x15%s\x00\x02\x02\x50"

    def on_ssl(self, client_hello):
        super(DropTLS, self).on_ssl(client_hello)
        if client_hello.version.major > 3 or client_hello.version.minor > 0:
            # Send a fatal internal_error alert
            self.connection.inject_response(DropTLS.ALERT % (client_hello.version.to_bytes()))
            self.connection.close()
        return False

