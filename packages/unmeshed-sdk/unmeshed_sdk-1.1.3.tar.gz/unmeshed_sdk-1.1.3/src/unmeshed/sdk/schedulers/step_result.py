from dataclasses import dataclass

@dataclass(frozen=True)
class StepResult:
    result: object

    def get_result(self):
        return self.result