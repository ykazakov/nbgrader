# coding: utf-8

from traitlets import default

from .baseapp import NbGrader, nbgrader_aliases, nbgrader_flags
from ..exchange import Exchange, ExchangeFetchSolution, ExchangeError


aliases = {}
aliases.update(nbgrader_aliases)
aliases.update({
    "timezone": "Exchange.timezone",
    "course": "CourseDirectory.course_id",
})

flags = {}
flags.update(nbgrader_flags)
flags.update({
    'replace': (
        {'ExchangeFetchSolution': {'replace_missing_files': True}},
        "replace missing files, even if the solution has already been fetched"
    ),
})


class FetchSolutionApp(NbGrader):

    name = u'nbgrader-fetch-solution'
    description = u'Fetch solution for an assignment from the nbgrader exchange'

    aliases = aliases
    flags = flags

    examples = """
        Fetch solution for an assignment, if an instructor has released it.
        For the usage of students.

        You can run this command from any directory, but usually, you will have a
        directory where you are keeping your course assignments.

        To fetch solution for an assignment by name into the current directory:

            nbgrader fetch_solution assignment1

        To fetch solution for an assignment for a specific course, simply include 
        the argument with the '--course' flag.

            nbgrader fetch_solution assignment1 --course=phys101

        This will create an new directory named `solution` in the assignment 
        directory.
        """

    @default("classes")
    def _classes_default(self):
        classes = super(FetchSolutionApp, self)._classes_default()
        classes.extend([Exchange, ExchangeFetchSolution])
        return classes

    def start(self):
        super(FetchSolutionApp, self).start()

        # set assignment and course
        if len(self.extra_args) == 0 and self.coursedir.assignment_id == "":
            self.fail("Must provide assignment name:\nnbgrader fetch_solution ASSIGNMENT [ --course COURSE ]")

        if self.coursedir.assignment_id != "":
            fetch = self.exchange.FetchSolution(
                coursedir=self.coursedir,
                authenticator=self.authenticator,
                parent=self)
            try:
                fetch.start()
            except ExchangeError:
                self.fail("nbgrader fetch_solution failed")
        else:
            failed = False

            for arg in self.extra_args:
                self.coursedir.assignment_id = arg
                fetch = self.exchange.FetchSolution(
                    coursedir=self.coursedir,
                    authenticator=self.authenticator,
                    parent=self)
                try:
                    fetch.start()
                except ExchangeError:
                    failed = True

            if failed:
                self.fail("nbgrader fetch_solution failed")
