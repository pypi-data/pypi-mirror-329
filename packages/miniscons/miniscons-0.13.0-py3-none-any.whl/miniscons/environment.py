import os
import psutil
from .constants import SCONS_FLAGS
from emoji import emojize
from glob import glob
from SCons.Environment import Environment
from SCons.Script import SConscript


def environment(source: str | None = None) -> Environment:
    if source is None:
        matches = glob("**/SConscript_conandeps", recursive=True)

        if matches:
            source = matches[0]

    return SConscript(source, must_exist=True)


def conan(
    defines: list[str] | None = None,
    source: str | None = None,
) -> Environment:
    if defines is None:
        defines = []

    conandeps = environment(source)["conandeps"]
    conandeps["CPPDEFINES"] += defines

    env = Environment(
        num_jobs=psutil.cpu_count(),
        ENV={"PATH": os.getenv("PATH", "")},
        CXXCOMSTR=emojize(":wrench: Compiling $TARGET"),
        LINKCOMSTR=emojize(":link: Linking $TARGET"),
    )

    env.MergeFlags(conandeps)
    return env


def packages(
    names: list[str],
    libs: list[str] | None = None,
    explicit: bool = False,
    source: str | None = None,
) -> dict[str, list[str]]:
    if libs is None:
        libs = names.copy()

    if not explicit:
        names.append("conandeps")

    reduced = {"LIBS": libs}

    for name, package in environment(source).items():
        if name in names:
            for flag in SCONS_FLAGS:
                reduced[flag] = reduced.get(flag, []) + package.get(flag, [])

    return reduced
