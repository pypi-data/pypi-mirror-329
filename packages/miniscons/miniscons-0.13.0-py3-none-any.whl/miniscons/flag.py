from dataclasses import dataclass
from SCons.Environment import Environment
from SCons.Script.Main import AddOption


@dataclass
class Flag:
    name: str

    def __repr__(self) -> str:
        return self.name

    def register(self, _: Environment) -> None:
        AddOption(self.name, action="store_true")
