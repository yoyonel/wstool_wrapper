#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import logging
import os
import subprocess

#
from colorlog import ColoredFormatter

__author__ = 'atty_l'

# ---- LOG -----
LOGFORMAT = "%(log_color)s[%(asctime)s][%(levelname)s][%(filename)s][%(funcName)s] %(message)s"
# logging.basicConfig(format=LOGFORMAT, level=logging.INFO)
# logger = logging.getLogger(__name__)
# --- Colors ---
# url: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
# coloredlogs.install()

formatter = ColoredFormatter(LOGFORMAT)
LOG_LEVEL = logging.DEBUG
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger("pythonConfig")
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)


# --------------


# url: https://docs.python.org/3/library/typing.html#typing.io
def load_json_file(config_json_file):
    """

    :param config_json_file:
    :type config_json_file: typing.BinaryIO
    :return:
    :rtype: dict
    """
    return json.load(config_json_file)


def generate_wstool_parameters_from_json_repo(repo, default_branch):
    """

    :param repo:
    :param default_branch:
    :return:
    """
    return {
        "scm_entry": repo["repository"],
        "uri": repo.get("uri", repo["repository"].split("/")[-1].split(".")[0]),
        "version": repo.get("branch", default_branch)
    }


def wstool_parameters_from_json_repos(json_repos):
    """

    :param json_repos:
    :type json_repos: dict
    :return:
    :rtype: list
    """
    # Convert into wstool arguments
    default_branch = json_repos.get("default_branch", "master")

    wstool_parameters = [
        generate_wstool_parameters_from_json_repo(json_repo, default_branch)
        for json_repo in json_repos["repos"]
    ]
    logger.debug("wstool_args: {}".format(wstool_parameters))

    return wstool_parameters


def subprocess_cmd(cmd, **kwargs):
    """

    :param cmd:
    :return:
    """
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, **kwargs)
    except OSError as e:
        logger.error("OSError when invoking subprocess: %s", cmd, exc_info=True)
        raise e

    ret_comm = p.communicate()
    return ret_comm, p


def wstool_init_ws(directory):
    """

    :param directory:
    :return:
    """
    try:
        ret_comm, p = subprocess_cmd(["wstool", "init", directory])
    except OSError:
        logger.error("Can't init workspace!", exc_info=True)
        raise RuntimeError

    logger.debug("comm: %s - p.returncode: %s", ret_comm, p.returncode)


def wstool_clone_repos(
        params,
        target_workspace=".",
        update_after_set=False,
        update_submodules=False,
        print_stdout=True
):
    """

    :param params:
    :param target_workspace:
    :param update_after_set:
    :param update_submodules:
    :param print_stdout:
    :return:
    """
    for param in params:
        logger.info("Perform wstool operations for: %s ...", param['uri'])
        cmd = ["wstool",
               "set",
               param['uri'],
               param['scm_entry'],
               "--version-new={}".format(param['version']),
               "--git",
               "--target-workspace={}".format(target_workspace),
               "--confirm"
               ]
        if update_after_set:
            cmd.append("--update")
        logger.debug("cmd: %s", cmd)
        try:
            comm, p = subprocess_cmd(cmd)
            stdout, err = comm
            if print_stdout:
                # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
                print(stdout.decode('utf-8'))
        except OSError:
            logger.error("Perform wstool operation for: %s ... FAILED", param['uri'], exc_info=True)
            raise RuntimeError

        logger.info("Perform wstool operation for: %s ... DONE", param['uri'])
        #
        logger.debug("stdout: %s", stdout)
        logger.debug("err: %s", err)
        logger.debug("exit code: %s", p.returncode)

    if update_submodules:
        str_wstool_operation = "Perform wstool update on all submodules ..."
        logger.info(str_wstool_operation)
        cmd = "wstool update".split()
        try:
            # https://stackoverflow.com/questions/6194499/pushd-through-os-system
            comm, p = subprocess_cmd(cmd, cwd=target_workspace)
            stdout, err = comm
            if print_stdout:
                print(stdout.decode("utf-8"))
        except OSError:
            logger.info(str_wstool_operation + "FAILED", exc_info=True)
            raise RuntimeError

        logger.info(str_wstool_operation + "DONE")
        #
        logger.debug("stdout: %s", stdout)
        logger.debug("err: %s", err)
        logger.debug("exit code: %s", p.returncode)


def process(args):
    """

    :param args:
    :type args: ArgumentParser
    :return:
    """
    # TODO: Handle exceptions/errors
    json_repos = load_json_file(args.json_file)
    logger.debug("json_repos: %s", json_repos)
    wstool_params = wstool_parameters_from_json_repos(json_repos)

    wstool_init_ws(args.directory)

    wstool_clone_repos(
        wstool_params,
        target_workspace=args.directory,
        update_after_set=args.update,
        update_submodules=args.update_submodules
    )


def parse_arguments():
    """

    :return:
    """
    # Parse arguments
    parser = argparse.ArgumentParser()
    # url: https://docs.python.org/3/library/argparse.html#argparse.FileType
    parser.add_argument("json_file", type=argparse.FileType("r"))
    parser.add_argument("directory", type=str, default=os.path.expanduser("."))
    parser.add_argument("--update_after_set", dest="update",
                        action="store_true",
                        help="Update after set entry")
    parser.add_argument("--update_submodules", dest="update_submodules",
                        action="store_true",
                        help="Update (all) submodules of the project.")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="increase output verbosity")

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()

    # post config for logger
    # because we use a parameter for setting the level logging
    # url: https://docs.python.org/2/library/logging.html#logging.Logger.setLevel
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    # debug for argparser
    for arg, value in sorted(vars(args).items()):
        logger.debug("Argument %s: %s", arg, value)

    process(args)


if __name__ == '__main__':
    main()
