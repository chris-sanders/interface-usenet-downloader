from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import when
from charmhelpers.core import hookenv

class UsenetDownloaderProvides(RelationBase):
    scope = scopes.GLOBAL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hookenv.atexit(lambda: self.remove_state(self.states.triggered))

    @hook('{provides:usenetdownloader}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.available')
        self.set_state('{relation_name}.triggered')

    @hook('{provides:usenetdownloader}-relation-{departed}')
    def departed(self):
        self.remove_state('{relation_name}.available')

    def configure(self,hostname,port,apikey):
        relation_info = {
            'hostname': address,
            'port': port,
            'apikey': apikey
             }
        self.set_remote(**relation_info)
        self.set_state('{relation_name}.configured')

