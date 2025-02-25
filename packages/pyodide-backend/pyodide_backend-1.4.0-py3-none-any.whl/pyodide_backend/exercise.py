import json

from .process import WasmProcess, FILENAME
from .task import TaskNoOutput, TaskCaptureCodeExecutionOutput
from pythonwhat import test_exercise


class PyodideExercise:
    def __init__(self, pec: str, solution: str, sct: str):
        self.pec = pec
        self.solution = solution
        self.sct = sct

        self.user_process = None
        self.solution_process = None

    def run_init(self):
        self.user_process = WasmProcess()

        result, _raw_output = self.user_process.executeTask(
            TaskCaptureCodeExecutionOutput([self.pec])
        )

        return result

    def run_code(self, code: str):
        if self.user_process == None:
            self.user_process = WasmProcess()
            output, _ = self.user_process.executeTask(
                TaskCaptureCodeExecutionOutput([self.pec, code])
            )
            return str(json.dumps(output))

        output, _ = self.user_process.executeTask(
            TaskCaptureCodeExecutionOutput([code])
        )
        return str(json.dumps(output))

    def map_output(self, output):
        if output["type"] == "error":
            return {"payload": output["payload"], "type": "error"}

        return {
            "payload": {
                "output": output["payload"],
                "script_name": FILENAME,
            },
            "type": "script-output",
        }

    def run_submit(self, code: str):
        submit_process = WasmProcess()
        submit_process.shell.displayhook.returns_result = False

        outputs, raw_output = submit_process.executeTask(
            TaskCaptureCodeExecutionOutput([self.pec, code])
        )

        if self.solution_process == None:
            self.solution_process = WasmProcess()
            self.solution_process.executeTask(TaskNoOutput([self.pec, self.solution]))

        test_result = test_exercise(
            sct=self.sct,
            student_code=code,
            solution_code=self.solution,
            pre_exercise_code=self.pec,
            student_process=submit_process,
            solution_process=self.solution_process,
            raw_student_output=raw_output,
            ex_type="CodingExercise",
            error=None,  # TODO verify if this is ever non-None for coding exercises
        )

        result = [self.map_output(output) for output in outputs] + [
            {"payload": test_result, "type": "sct"},
        ]

        return str(json.dumps(result))
