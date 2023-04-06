from traitlets import Bool
from .exchange import Exchange


class ExchangeList(Exchange):

    inbound = Bool(False, help="List inbound files rather than outbound.").tag(config=True)
    solution = Bool(False, help="List released solutions to assignments.").tag(config=True)
    cached = Bool(False, help="List assignments in submission cache.").tag(config=True)
    remove = Bool(False, help="Remove, rather than list files.").tag(config=True)

    def list_files(self):
        """Return list of available files """
        raise NotImplementedError

    def remove_files(self):
        """Remove available files """
        raise NotImplementedError

    def start(self):
        if self.inbound + self.solution + self.cached > 1:
            self.fail("Options --inbound --solution and --cached are exclusive.")

        super(ExchangeList, self).start()

        if self.remove:
            return self.remove_files()
        else:
            return self.list_files()
