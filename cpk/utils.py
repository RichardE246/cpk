import toml
from pathlib import Path
from git import Repo
import shutil
import sys
import subprocess
import os

topdir = Path.home()
homedir = Path.joinpath(topdir, ".cpk")
bindir = Path.joinpath(homedir, "bin")
libdir = Path.joinpath(homedir, "lib")


def init(path):
    path = Path(path)
    path.mkdir()
    cpk_path = Path.joinpath(path,"cpk.toml")
    data = {
                "project":{
                            "name":str(path),
                            "version":"0.1.0"

                        }
            }
    # for attribute in attributes:
    #     data["project"][attribute] = input(f"{attribute}: ")
    cpk_path.write_text(toml.dumps(data))


def activate():   
    if not homedir.exists():
        homedir.mkdir(parents=False, exist_ok=False)
        # bindir = Path.joinpath(homedir, "bin")
        bindir.mkdir(parents=False, exist_ok=False)
        # libdir = Path.joinpath(homedir, "lib")
        libdir.mkdir(parents=False, exist_ok=False)
    if bindir not in os.environ["PATH"].split(":"):
        print("cpk bin directory not on your $PATH")
        print("add it by running:")
        print('export PATH="$HOME/.cpk/bin:$PATH"')



def get_bin(url):
    name = url.split("/")
    name = name[-1]
    name = name.removesuffix(".git")
    print(f"downloading {name}...")
    reponame = Path.joinpath(homedir, name)
    print(reponame)
    repo = Repo.clone_from(url, reponame)
    return reponame  

def build(path):
    tomlpath = Path.joinpath(path, "cpk.toml")
    if not tomlpath.exists():
        print("no cpk.toml found. Aborting")
        exit(0)
    data = toml.load(tomlpath)
    binary = data["project"]["binary"]
    print(f"building binary {binary}")
    build_step = data["project"]["build_step"]
    for step in build_step:
        print(step)
        subprocess.run(step, cwd=str(path.resolve()))
    binpath = Path.joinpath(path,binary)
    if binpath.exists():
        targetpath = Path.joinpath(bindir,binary)
        targetpath.symlink_to(binpath.absolute())

def install(url):
    name = get_bin(url)
    build(name)

def uninstall(name):
    pkgname = Path.joinpath(homedir, name)
    print(f"removing {pkgname}")
    tomlpath = Path.joinpath(pkgname, "cpk.toml")
    data = toml.load(tomlpath)
    binary = data["project"]["binary"]
    bin = Path.joinpath(bindir, binary)
    if bin.exists():
        print(f"removing symlink {bin}")
        bin.unlink()
    if pkgname.exists():
        print(f"uninstalling package")
        shutil.rmtree(pkgname)


