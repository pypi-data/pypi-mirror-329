import subprocess


class LocalRunner:
    def __init__(self, work_dir: str) -> None:
        self.work_dir = work_dir
        self.p = None

    def popen_run(self, cmd: str) -> subprocess.Popen:
        # print(cmd)
        self.p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        return self.p

    def get_output_run(self, cmd: str):
        # print(cmd)
        status, output = subprocess.getstatusoutput(cmd)
        return status, output

    def flush_output(self):
        for line in iter(self.p.stdout.readline, b''):
            print('\t' + line.decode().strip())

    def simple_run(self, cmd: str):
        return self.get_output_run(cmd)

    def complex_run(self, cmd: str):
        self.popen_run(cmd)
        self.flush_output()
        self.p.wait()
        # print('STATUS_CODE', self.p.returncode)
        if self.p.returncode != 0:
            raise Exception('Run: [{}] failed.'.format(cmd))
        return self.p.returncode, None
