from pathlib import Path
from typing import Iterable

from click import command

from .io import ct_to_db, db_to_ct
from .. import path
from ..arg import (CMD_CT2DB,
                   CMD_DB2CT,
                   arg_input_path,
                   opt_force,
                   opt_max_procs)
from ..run import run_func
from ..task import as_list_of_tuples, dispatch


@run_func(CMD_CT2DB)
def run_ct_to_db(input_path: Iterable[str | Path], *,
                 force: bool,
                 max_procs: int):
    """ Convert connectivity table (CT) to dot-bracket (DB) files. """
    ct_files = list(path.find_files_chain(input_path, [path.ConnectTableSeg]))
    return dispatch(ct_to_db,
                    max_procs,
                    args=as_list_of_tuples(ct_files),
                    kwargs=dict(force=force),
                    pass_n_procs=False)


@run_func(CMD_DB2CT)
def run_db_to_ct(input_path: Iterable[str | Path], *,
                 force: bool,
                 max_procs: int):
    """ Convert dot-bracket (DB) to connectivity table (CT) files. """
    db_files = list(path.find_files_chain(input_path, [path.DotBracketSeg]))
    return dispatch(db_to_ct,
                    max_procs,
                    args=as_list_of_tuples(db_files),
                    kwargs=dict(force=force),
                    pass_n_procs=False)


params = [
    arg_input_path,
    opt_force,
    opt_max_procs,
]


@command(CMD_CT2DB, params=params)
def cli_ct2db(*args, **kwargs):
    """ Convert connectivity table (CT) to dot-bracket (DB) files. """
    run_ct_to_db(*args, **kwargs)


@command(CMD_DB2CT, params=params)
def cli_db2ct(*args, **kwargs):
    """ Convert dot-bracket (DB) to connectivity table (CT) files. """
    run_db_to_ct(*args, **kwargs)
