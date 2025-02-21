import os
from .constants import SCONS_FLAGS
from .containers import unique
from dataclasses import dataclass, field
from SCons.Environment import Environment


@dataclass
class Build:
    name: str

    files: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)

    packages: dict[str, list[str]] = field(default_factory=dict)

    output: str = "dist"
    shared: bool = False

    rename: str | None = None

    def __repr__(self) -> str:
        return self.name

    @property
    def target(self) -> str:
        return os.path.join(self.output, self.rename if self.rename else self.name)

    def path(self, file: str) -> str:
        root = os.path.splitext(os.path.normpath(file))[0]
        return f"{root.replace('.', '-')}-[{self.name}]"

    def merge(self, env: Environment) -> dict[str, list[str]]:
        merged = {
            k: unique(env.get(k, []) + self.packages.get(k, [])) for k in SCONS_FLAGS
        }

        merged["CXXFLAGS"] += self.flags
        return merged

    def nodes(self, env: Environment, merged: dict[str, list[str]]) -> list[str]:
        return [env.Object(self.path(file), file, **merged) for file in self.files]

    def register(self, env: Environment) -> None:
        merged = self.merge(env)
        nodes = self.nodes(env, merged)

        if self.shared:
            outputs = env.Library(self.target, nodes, **merged)
            env.Alias(self.name, outputs[0])
        else:
            env.Program(self.target, nodes, **merged)
            env.Alias(self.name, self.target)
