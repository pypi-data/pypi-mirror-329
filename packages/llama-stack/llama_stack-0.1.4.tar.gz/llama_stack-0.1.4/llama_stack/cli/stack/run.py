# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import argparse
import os
from pathlib import Path

from llama_stack.cli.subcommand import Subcommand

REPO_ROOT = Path(__file__).parent.parent.parent.parent


class StackRun(Subcommand):
    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self.parser = subparsers.add_parser(
            "run",
            prog="llama stack run",
            description="""Start the server for a Llama Stack Distribution. You should have already built (or downloaded) and configured the distribution.""",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self.parser.set_defaults(func=self._run_stack_run_cmd)

    def _add_arguments(self):
        self.parser.add_argument(
            "config",
            type=str,
            help="Path to config file to use for the run",
        )
        self.parser.add_argument(
            "--port",
            type=int,
            help="Port to run the server on. Defaults to 8321",
            default=int(os.getenv("LLAMA_STACK_PORT", 8321)),
        )
        self.parser.add_argument(
            "--image-name",
            type=str,
            help="Name of the image to run. Defaults to the current conda environment",
        )
        self.parser.add_argument(
            "--disable-ipv6",
            action="store_true",
            help="Disable IPv6 support",
            default=False,
        )
        self.parser.add_argument(
            "--env",
            action="append",
            help="Environment variables to pass to the server in KEY=VALUE format. Can be specified multiple times.",
            default=[],
            metavar="KEY=VALUE",
        )
        self.parser.add_argument(
            "--tls-keyfile",
            type=str,
            help="Path to TLS key file for HTTPS",
        )
        self.parser.add_argument(
            "--tls-certfile",
            type=str,
            help="Path to TLS certificate file for HTTPS",
        )
        self.parser.add_argument(
            "--image-type",
            type=str,
            help="Image Type used during the build. This can be either conda or container or venv.",
            choices=["conda", "container", "venv"],
            default="conda",
        )

    def _run_stack_run_cmd(self, args: argparse.Namespace) -> None:
        import yaml
        from termcolor import cprint

        from llama_stack.distribution.build import ImageType
        from llama_stack.distribution.configure import parse_and_maybe_upgrade_config
        from llama_stack.distribution.utils.config_dirs import (
            BUILDS_BASE_DIR,
            DISTRIBS_BASE_DIR,
        )
        from llama_stack.distribution.utils.exec import formulate_run_args, run_with_pty

        if not args.config:
            self.parser.error("Must specify a config file to run")
            return

        config_file = Path(args.config)
        has_yaml_suffix = args.config.endswith(".yaml")
        template_name = None

        if not config_file.exists() and not has_yaml_suffix:
            # check if this is a template
            config_file = Path(REPO_ROOT) / "llama_stack" / "templates" / args.config / "run.yaml"
            if config_file.exists():
                template_name = args.config

        if not config_file.exists() and not has_yaml_suffix:
            # check if it's a build config saved to conda dir
            config_file = Path(BUILDS_BASE_DIR / ImageType.conda.value / f"{args.config}-run.yaml")

        if not config_file.exists() and not has_yaml_suffix:
            # check if it's a build config saved to container dir
            config_file = Path(BUILDS_BASE_DIR / ImageType.container.value / f"{args.config}-run.yaml")

        if not config_file.exists() and not has_yaml_suffix:
            # check if it's a build config saved to ~/.llama dir
            config_file = Path(DISTRIBS_BASE_DIR / f"llamastack-{args.config}" / f"{args.config}-run.yaml")

        if not config_file.exists():
            self.parser.error(
                f"File {str(config_file)} does not exist.\n\nPlease run `llama stack build` to generate (and optionally edit) a run.yaml file"
            )
            return

        print(f"Using run configuration: {config_file}")
        config_dict = yaml.safe_load(config_file.read_text())
        config = parse_and_maybe_upgrade_config(config_dict)

        run_args = formulate_run_args(args.image_type, args.image_name, config, template_name)

        run_args.extend([str(config_file), str(args.port)])
        if args.disable_ipv6:
            run_args.append("--disable-ipv6")

        for env_var in args.env:
            if "=" not in env_var:
                cprint(
                    f"Environment variable '{env_var}' must be in KEY=VALUE format",
                    color="red",
                )
                return
            key, value = env_var.split("=", 1)  # split on first = only
            if not key:
                cprint(
                    f"Environment variable '{env_var}' has empty key",
                    color="red",
                )
                return
            run_args.extend(["--env", f"{key}={value}"])

        if args.tls_keyfile and args.tls_certfile:
            run_args.extend(["--tls-keyfile", args.tls_keyfile, "--tls-certfile", args.tls_certfile])
        run_with_pty(run_args)
