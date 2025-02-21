from .build import Build
from dataclasses import dataclass, field
from SCons.Environment import Environment


@dataclass
class Target:
    name: str
    build: Build

    args: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{self.name} -> {self.build.name}"

    @property
    def action(self) -> str:
        return " ".join([self.build.target, *self.args])

    def register(self, env: Environment) -> None:
        alias = env.Alias(self.name, [self.build.target], self.action)
        env.AlwaysBuild(alias)
