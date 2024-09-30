# coding: utf-8

from traitlets import default

from .baseapp import NbGrader, nbgrader_aliases, nbgrader_flags
from ..exchange import Exchange, ExchangeReleaseSolution, ExchangeError


aliases = {}
aliases.update(nbgrader_aliases)
aliases.update({
    "timezone": "Exchange.timezone",
    "course": "CourseDirectory.course_id",
})

flags = {}
flags.update(nbgrader_flags)
flags.update({
    'force': (
        {'ExchangeReleaseSolution': {'force': True}},
        "Force overwrite of existing files in the exchange."
    ),
    'f': (
        {'ExchangeReleaseSolution': {'force': True}},
        "Force overwrite of existing files in the exchange."
    ),
})


class ReleaseSolutionApp(NbGrader):

    name = u'nbgrader-release-solution'
    description = u'Release assignment solution to the nbgrader exchange'

    aliases = aliases
    flags = flags

    examples = """
        Release solution for an assignment to students. For the usage of instructors.

        This command is run from the top-level nbgrader folder.

        The command releases the solution present in the `solution` folder. To populate
        this folder use the `nbgrader generate_solution` command.

        To release the solution for an assignment named `assignment1` run:

            nbgrader release_solution assignment1

        If the solution has already been released, you will have to add the
        `--force` flag to overwrite the released solution:

            nbgrader release_solution --force assignment1

        To query the exchange to see a list of your released assignments:

            nbgrader list --solution
        """

    @default("classes")
    def _classes_default(self):
        classes = super(ReleaseSolutionApp, self)._classes_default()
        classes.extend([Exchange, ExchangeReleaseSolution])
        return classes

    def start(self):
        super(ReleaseSolutionApp, self).start()

        # set assignment and course
        if len(self.extra_args) == 1:
            self.coursedir.assignment_id = self.extra_args[0]
        elif len(self.extra_args) > 2:
            self.fail("Too many arguments")
        elif self.coursedir.assignment_id == "":
            self.fail("Must provide assignment name:\nnbgrader <command> ASSIGNMENT [ --course COURSE ]")

        release = self.exchange.ReleaseSolution(
            coursedir=self.coursedir,
            authenticator=self.authenticator,
            parent=self)
        try:
            release.start()
        except ExchangeError:
            self.fail("nbgrader release_solution failed")
