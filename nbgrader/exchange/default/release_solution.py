import os
import shutil
from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IWGRP, S_IXGRP, S_IROTH, S_IXOTH, S_ISGID

from nbgrader.exchange.abc import ExchangeReleaseSolution as ABCExchangeReleaseSolution
from nbgrader.exchange.default import Exchange


class ExchangeReleaseSolution(Exchange, ABCExchangeReleaseSolution):

    def init_src(self):
        self.src_path = self.coursedir.format_path(self.coursedir.solution_directory, '.', self.coursedir.assignment_id)
        if not os.path.isdir(self.src_path):
            source = self.coursedir.format_path(self.coursedir.source_directory, '.', self.coursedir.assignment_id)
            if os.path.isdir(source):
                self.fail("Assignment '{}' has no solution '{}', run `nbgrader generate_solution` first.".format(
                    source, self.src_path))
            else:
                self._assignment_not_found(
                    self.src_path,
                    self.coursedir.format_path(self.coursedir.solution_directory, '.', '*'))

    def init_dest(self):
        if self.coursedir.course_id == '':
            self.fail("No course id specified. Re-run with --course flag.")

        self.course_path = os.path.join(self.root, self.coursedir.course_id)
        self.outbound_solution_path = os.path.join(self.course_path, 'solution')
        self.dest_path = os.path.join(self.outbound_solution_path, self.coursedir.assignment_id)
        # 0755
        # groupshared: +2040
        self.ensure_directory(
            self.course_path,
            S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH|((S_ISGID|S_IWGRP) if self.coursedir.groupshared else 0)
        )
        # 0755
        # groupshared: +2040
        self.ensure_directory(
            self.outbound_solution_path,
            S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH|((S_ISGID|S_IWGRP) if self.coursedir.groupshared else 0)
        )

    def copy_files(self):
        if os.path.isdir(self.dest_path):
            if self.force:
                self.log.info("Overwriting solution: {} {}".format(
                    self.coursedir.course_id, self.coursedir.assignment_id
                ))
                shutil.rmtree(self.dest_path)
            else:
                self.fail("Solution already exists, add --force to overwrite: {} {}".format(
                    self.coursedir.course_id, self.coursedir.assignment_id
                ))
        self.log.info("Releasing solution to assignment '{}/{}'".format(
                self.coursedir.course_id, self.coursedir.assignment_id))
        self.do_copy(self.src_path, self.dest_path)
        self.set_perms(
            self.dest_path,
            fileperms=(S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH|(S_IWGRP if self.coursedir.groupshared else 0)),
            dirperms=(S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH|((S_ISGID|S_IWGRP) if self.coursedir.groupshared else 0)))
        self.log.info("Solution released to: {}".format(self.dest_path))
