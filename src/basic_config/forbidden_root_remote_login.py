from . import base


class ForbiddenRootRemoteLogin(base.Base):

    def __init__(self, system, version):
        super(ForbiddenRootRemoteLogin, self).__init__(system, version)
        self._op_file = "/etc/ssh/sshd_config"
        self._status = self.check()
        self._prepare()

    def check(self):
        cmd = "grep '^PermitRootLogin no' '{origin}'".format(origin=self._op_file)
        stdout, err = self._run_command(cmd)
        if stdout.find("PermitRootLogin no") >= 0:
            self._status = True
        else:
            self._status = False
        return self._status

    def set(self, status):
        if status == self._status:
            return
        if status:
            return self._set(status)
        else:
            return not self._set(status)

    def _prepare(self):
        prepare_cmd = "cp '{origin}' '{end}'".format(origin=self._op_file, end=self._op_file+"_tmp")
        self._run_command(prepare_cmd)

    def _set(self, status):
        cmd = "sed -i 's/PermitRootLogin {origin}/PermitRootLogin {end}/g' '{op_file}' \
            && sed -i 's/#PermitRootLogin {end}/PermitRootLogin {end}/' '{op_file}'"
        origin = "yes"
        end = "no"
        if not status:
            origin = "no"
            end = "yes"
        cmd = cmd.format(origin=origin, end=end, op_file=self._op_file)
        self._run_command(cmd)
        return self.check()