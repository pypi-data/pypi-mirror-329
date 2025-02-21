import sys
from .build import Build
from .flag import Flag
from .routine import Routine
from .script import Script
from .target import Target
from dataclasses import dataclass, field
from SCons.Environment import Environment


@dataclass
class Tasks:
    builds: list[Build] = field(default_factory=list)
    targets: list[Target] = field(default_factory=list)
    scripts: list[Script] = field(default_factory=list)
    routines: list[Routine] = field(default_factory=list)
    flags: list[Flag] = field(default_factory=list)

    @property
    def cli(self) -> str:
        sections = [
            ":".join(
                [k, "".join([f"\n  {i}" for i in v] if len(v) > 0 else "\n  None")]
            )
            for k, v in self.__dict__.items()
        ]

        return "".join(["\n", "\n\n".join(sections), "\n"])

    def dump(self) -> None:
        sys.stdout.write(f"{self.cli}\n")

    def register(self, env: Environment) -> None:
        for group in self.__dict__.values():
            for task in group:
                task.register(env)
