from .containers import flatten
from dataclasses import dataclass, field
from SCons.Environment import Environment


@dataclass
class Script:
    name: str

    cmd: list[str | list[str]] = field(default_factory=list)

    def __repr__(self) -> str:
        return self.name

    @property
    def action(self) -> str:
        return " ".join(flatten(self.cmd))

    def register(self, env: Environment) -> None:
        alias = env.Alias(self.name, [], self.action)
        env.AlwaysBuild(alias)
