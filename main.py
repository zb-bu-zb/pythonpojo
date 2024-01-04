import sys
import subprocess
from Configs.configs import RESULT_PATH

if __name__=="__main__":
    report_path=RESULT_PATH
    WIN = sys.platform.startswith('win')
    steps = [
        f"pytest --alluredir {report_path}/allure-results --clean-alluredir",
        f"allure generate {report_path}/allure-results -c -o {report_path}/allure-report",
        f"allure open {report_path}/allure-report"
    ]
    for step in steps:
        subprocess.run("call " + step if WIN else step, shell=True)
