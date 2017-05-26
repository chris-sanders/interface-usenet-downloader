from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import when
import socket

class UsenetDownloaderRequires(RelationBase):
    scope = scopes.GLOBAL
    auto_accessors=['hostname','port','apikey']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hookenv.atexit(lambda: self.remove_state(self.states.triggered))

    @hook('{requires:usenetdownloader}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.triggered')
        if self.hostname() and self.port() and self.apikey():
            self.set_state('{relation_name}.available')
            if self.hostname() != self.get_local('hostname') or\
               self.port() != self.get_local('port') or \
               self.apikey() != self.get_local('apikey'):
                self.set_local('hostname',self.hostname())
                self.set_local('port',self.port())
                self.set_local('apikey',self.apikey())
                self.remove_state('{relation_name}.configured')

    @hook('{requires:salt}-relation-{departed}')
    def departed(self):
        self.remove_state('{relation_name}.available')


