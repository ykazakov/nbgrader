from traitlets import Bool

from .exchange import Exchange


class ExchangeFetchSolution(Exchange):

    replace_missing_files = Bool(False, help="Whether to replace missing files on fetch").tag(config=True)
