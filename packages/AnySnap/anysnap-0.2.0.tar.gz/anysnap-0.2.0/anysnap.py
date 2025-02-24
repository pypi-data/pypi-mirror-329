#! /usr/bin/python3

import sys
import os
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
import json
import fnmatch

import click
import plumbum
from plumbum import local, FG, TF

findmnt = local["findmnt"]["-J"]["--target"]
echo = local["echo"]


def get_fstype(path):
    retcode, mnt, _ = findmnt[path].run(retcode=(0, 1))
    if retcode == 1:
        return None
    mnt = json.loads(mnt)

    fstype = mnt["filesystems"][0]["fstype"]
    return fstype


def dry_run(cmd):
    return lambda *x: echo[cmd][*x] & FG


class Snapshot:
    def __init__(
        self, source, base, label, dryrun=False, verbose=False, recursive=False
    ):
        self.source = Path(source)
        self._base = Path(base)
        self._label = label
        self._name = self.source.name

        self._dryrun = dryrun
        self._verbose = verbose
        self._recursive = recursive

    def now(self):
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def list(self):
        raise NotImplementedError

    def clean(self, keep):
        if keep > 0:
            snapshots = sorted(self.list())
            for todel in snapshots[0:-keep]:
                self.delete(todel)

    def name(self, pattern=False):
        name = f"{self._name}@{self._label}-"
        if pattern:
            return name + "*"
        else:
            return name + self.now()

    def snapshot(self):
        raise NotImplementedError

    def delete(self, snap):
        raise NotImplementedError


class Zfs(Snapshot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._zfs = local["zfs"]
        self._snapshot = self._zfs["snapshot"]
        self._destroy = self._zfs["destroy"]
        self._list = self._zfs["list", "-H", "-o", "name", "-t", "snapshot"]

        if self._recursive:
            self._snapshot = self._snapshot["-r"]

        if self._dryrun:
            self._snapshot = dry_run(self._snapshot)
            self._destroy = dry_run(self._destroy)

    @staticmethod
    def check(target):
        """Check if a target is a valid candidate for a ZFS snapshot.

        The binary btrfs must exist and the target must be a ZFS filesystem (and not a path).
        """
        try:
            zfs = local["zfs"]
        except plumbum.commands.processes.CommandNotFound:
            return False

        return target[0] != "/" and zfs["list", target] & TF

    def list(self):
        pattern = self.name(pattern=True)

        subvol = self._list(self.source)
        subvol = subvol.rstrip().split("\n")

        pattern = str(self.source.parent / pattern)
        return fnmatch.filter(subvol, pattern)

    def delete(self, snap):
        self._destroy(str(snap))

    def snapshot(self):
        snap = str(self.source.parent / self.name())
        self._snapshot(snap)


class Btrfs(Snapshot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._btrfs = local["btrfs"]
        self._list = self._btrfs["subvolume", "list", "-r", "-s", "-o"]
        self._snapshot = self._btrfs["subvolume", "snapshot", "-r"]
        self._delete = self._btrfs["subvolume", "delete"]

        if self._name == "":
            self._name = "rootfs"

        self._basedir = self.source / self._base
        if not self._dryrun:
            self._basedir.mkdir(parents=True, exist_ok=True)

        if self._dryrun:
            self._snapshot = dry_run(self._snapshot)
            self._delete = dry_run(self._delete)

    @staticmethod
    def check(target):
        """Check if a target is a valid candidate for a BTRFS snapshot.

        The binary btrfs must exist and the target must be a BTRFS subvolume.
        """
        try:
            btrfs = local["btrfs"]
        except plumbum.commands.processes.CommandNotFound:
            return False

        return get_fstype(target) == "btrfs" and btrfs["subvolume", "show", target] & TF

    def list(self):
        pattern = self.name(pattern=True)

        subvol = self._list(self.source)
        subvol = subvol.rstrip()
        if len(subvol) == 0:
            return []

        subvol = [line.split()[-1] for line in subvol.split("\n")]
        subvol = [str(self.source / sub) for sub in subvol]

        return fnmatch.filter(subvol, str(self.source / self._base / pattern))

    def delete(self, snap):
        self._delete(str(snap))

    def snapshot(self):
        snap = str(self._basedir / self.name())
        self._snapshot(str(self.source), snap)


class S3ql(Snapshot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._basedir = self.source.parent / self._base
        if not self._dryrun:
            self._basedir.mkdir(parents=True, exist_ok=True)

        _s3qlcp = local["s3qlcp"]
        _s3qlrm = local["s3qlrm"]
        _s3qllock = local["s3qllock"]

        if self._dryrun:
            self._s3qlcp = dry_run(self._s3qlcp)
            self._s3qlrm = dry_run(self._s3qlrm)
            self._s3qllock = dry_run(self._s3qllock)

    @staticmethod
    def check(target):
        """Check if a target is a valid candidate for a S3QL snapshot.

        The binary s3qlcp must exist and the target must be inside a S3QL
        mountpoint.
        """

        try:
            _ = local["s3qlcp"]
        except plumbum.commands.processes.CommandNotFound:
            return False

        return get_fstype(target) == "fuse.s3ql"

    def list(self):
        pattern = self.name(pattern=True)
        return sorted(self._basedir.glob(pattern))

    def delete(self, snap):
        self._s3qlrm(str(snap))

    def snapshot(self):
        snap = str(self._basedir / self.name())
        self._s3qlcp(str(self.source), snap)
        self._s3qllock(snap)


class Dispatcher(dict):
    def auto(self, target):
        for _, backend in self.items():
            if backend.check(target):
                return backend
        click.echo("ERROR: unable to find a suitable backend", err=True)
        sys.exit(1)


dispatcher = Dispatcher()
dispatcher["s3ql"] = S3ql
dispatcher["zfs"] = Zfs
dispatcher["btrfs"] = Btrfs


@click.command()
@click.version_option()
@click.option("-v", "--verbose", is_flag=True, default=False, help="Verbose mode")
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Do nothing, just display actions",
)
@click.option(
    "-k", "--keep", default=10, help="Number of snapshots to keep (0 keeps everything)"
)
@click.option(
    "-f",
    "--fstype",
    type=click.Choice(["auto", "btrfs", "s3ql", "zfs"], case_sensitive=False),
    default="auto",
    help="Filesystem type (should be autodetected)",
)
@click.option(
    "-d",
    "--snapdir",
    default="../",
    metavar="DIRECTORY",
    help="Base path for the snapshots (depends on the filesystem)",
)
@click.option("-l", "--label", default="anysnap", help="Label for the snapshot name")
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    default=False,
    help="Recursive snapshot",
)
@click.argument("target")
def main(verbose, dry_run, keep, fstype, snapdir, label, recursive, target):
    """Snapshot TARGET and clean obsolete snapshots.

    Depending of the filesystem type, TARGET can be a subvolume (btrfs), a
    sub-directory (s3ql) or a filesystem (zfs).
    """

    if fstype == "auto":
        backend = dispatcher.auto(target)
        if verbose:
            click.echo(f"Backend automatically selected {backend}")
    else:
        backend = dispatcher[fstype]

    # parser.add_argument(
    #     "--rrsync",
    #     action="store_true",
    #     default=False,
    #     help="Run rrsync to receive data, before doing anything",
    # )

    snapshot = backend(
        target, snapdir, label, dryrun=dry_run, verbose=verbose, recursive=recursive
    )
    # if args.rrsync:
    #     run_rrsync(["rrsync", str(snapshot.source)])

    snapshot.snapshot()
    snapshot.clean(keep)
