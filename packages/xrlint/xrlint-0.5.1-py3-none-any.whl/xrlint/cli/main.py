#  Copyright © 2025 Brockmann Consult GmbH.
#  This software is distributed under the terms and conditions of the
#  MIT license (https://mit-license.org/).

import sys

import click

# Warning: do not import heavy stuff here, it can
# slow down commands like "xrlint --help" otherwise.
from xrlint.cli.constants import (
    DEFAULT_MAX_WARNINGS,
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_CONFIG_FILE_YAML,
)
from xrlint.version import version


@click.command(name="xrlint")
@click.option(
    "--no-config-lookup",
    "no_config_lookup",
    help="Disable use of default configuration files",
    is_flag=True,
)
@click.option(
    "--config",
    "-c",
    "config_path",
    help="Use this configuration instead of looking for a default configuration file",
    metavar="FILE",
)
@click.option(
    "--print-config",
    "inspect_path",
    help="Print the configuration for the given file",
    metavar="FILE",
)
@click.option(
    "--plugin",
    "plugin_specs",
    help=(
        "Specify plugins. MODULE is the name of Python module"
        " that defines an 'export_plugin()' function."
    ),
    metavar="MODULE",
    multiple=True,
)
@click.option(
    "--rule",
    "rule_specs",
    help=(
        "Specify rules. SPEC must have format"
        " '<rule-name>: <rule-config>' (note the space character)."
    ),
    metavar="SPEC",
    multiple=True,
)
@click.option(
    "-o",
    "--output-file",
    "output_file",
    help="Specify file to write report to",
    metavar="FILE",
)
@click.option(
    "-f",
    "--format",
    "output_format",
    help=f"Use a specific output format - default: {DEFAULT_OUTPUT_FORMAT}",
    default=DEFAULT_OUTPUT_FORMAT,
    metavar="NAME",
)
@click.option(
    "--color/--no-color",
    "color_enabled",
    default=True,
    help="Force enabling/disabling of color",
)
@click.option(
    "--max-warnings",
    "max_warnings",
    help=(
        f"Number of warnings to trigger nonzero exit code"
        f" - default: {DEFAULT_MAX_WARNINGS}"
    ),
    type=int,
    default=DEFAULT_MAX_WARNINGS,
    metavar="COUNT",
)
@click.option(
    "--init",
    "init_mode",
    help=f"Write initial configuration file '{DEFAULT_CONFIG_FILE_YAML}' and exit.",
    is_flag=True,
)
@click.argument("files", nargs=-1)
@click.version_option(version)
@click.help_option()
def main(
    no_config_lookup: bool,
    config_path: str | None,
    inspect_path: str | None,
    plugin_specs: tuple[str, ...],
    rule_specs: tuple[str, ...],
    max_warnings: int,
    output_file: str | None,
    output_format: str,
    color_enabled: bool,
    init_mode: bool,
    files: tuple[str, ...],
):
    """Validate the given dataset FILES.

    When executed, XRLint does the following three things:

    (1) Unless options '--no-config-lookup' or '--config' are used
    it searches for a default configuration file in the current working
    directory. Default configuration files are determined by their
    filename, namely 'xrlint_config.py' or 'xrlint-config.<format>',
    where <format> refers to the filename extensions
    'json', 'yaml', and 'yml'. A Python configuration file ('*.py'),
    is expected to provide XRLInt configuration from a function
    'export_config()', which may include custom plugins and rules.

    (2) It then validates each dataset in FILES against the configuration.
    The default dataset patters are '**/*.zarr' and '**/.nc'.
    FILES may comprise also directories or URLs. The supported URL
    protocols are the ones supported by xarray. Using remote
    protocols may require installing additional packages such as
    S3Fs (https://s3fs.readthedocs.io/) for the 's3' protocol.
    If a directory is provided that not matched by any file pattern,
    it will be traversed recursively.

    (3) The validation result is dumped to standard output if not otherwise
    stated by '--output-file'. The output format is 'simple' by default.
    Other inbuilt formats are 'json' and 'html' which you can specify
    using the '--format' option.

    Please refer to the documentation (https://bcdev.github.io/xrlint/)
    for more information.
    """
    from xrlint.cli.engine import XRLint

    if init_mode:
        XRLint.init_config_file()
        return

    cli_engine = XRLint(
        no_config_lookup=no_config_lookup,
        config_path=config_path,
        plugin_specs=plugin_specs,
        rule_specs=rule_specs,
        output_format=output_format,
        output_path=output_file,
        output_styled=color_enabled,
        max_warnings=max_warnings,
    )

    if inspect_path:
        cli_engine.init_config()
        cli_engine.print_config_for_file(inspect_path)
        return

    if files:
        cli_engine.init_config()
        results = cli_engine.validate_files(files)
        report = cli_engine.format_results(results)
        cli_engine.write_report(report)

        error_status = cli_engine.result_stats.error_count > 0
        max_warn_status = cli_engine.max_warnings_exceeded
        if max_warn_status and not error_status:
            click.echo("Maximum number of warnings exceeded.")
        if max_warn_status or error_status:
            raise click.exceptions.Exit(1)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
