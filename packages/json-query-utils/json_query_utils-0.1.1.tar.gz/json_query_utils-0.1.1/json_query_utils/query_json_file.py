"""Parse the JSON file and search for the attribute."""

import click
import json
import logging
import os
import pathlib
import re
import sys

from collections import Counter
from datetime import datetime
from jsonpath_ng import parse

from rich.console import Console
from typing import Any, Dict, List


from json_query_utils import constants
from json_query_utils.file_utils import check_infile_status

DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP,
)

error_console = Console(stderr=True, style="bold red")

console = Console()


def extract_attribute(
    json_data: Dict[str, Any], attribute: str, infile: str, outfile: str, logfile: str
) -> None:
    """Extract the attribute from the JSON data.

    Args:
        json_data (dict): The JSON data.
        attribute (str): The attribute to extract.
        infile (str): The input file.
        outfile (str): The output file.
        logfile (str): The log file.
    """
    # Find all matches for the attribute
    matches = find_matches(json_data, attribute)
    if not matches:
        print(f"No instances of attribute '{attribute}' found.")
        return

    # Group matches by XPath
    xpath_dict = group_matches_by_xpath(matches)

    # If multiple paths exist, prompt user for selection
    selected_xpath = prompt_user_for_xpath(xpath_dict)

    # Print Python code to extract values
    python_code = get_python_code(selected_xpath)

    # Extract values based on the selected path
    selected_matches = xpath_dict[selected_xpath]
    values = extract_values(selected_matches)

    # Generate jq command
    jq_command = generate_jq_command(selected_xpath, infile)

    # Display results
    display_results(
        attribute,
        selected_matches,
        values,
        jq_command,
        outfile,
        python_code,
        infile,
        logfile,
    )


def find_matches(json_data, attribute):
    """Find all matches for the given attribute in the JSON data."""
    jsonpath_expr = parse(f"$..{attribute}")
    return [match for match in jsonpath_expr.find(json_data)]


def group_matches_by_xpath(matches):
    """Group the matches by their generalized XPath."""
    xpath_dict = {}
    for match in matches:
        # Use a regular expression to replace any indices with the wildcard [*]
        xpath_str = re.sub(r"\[\d+\]", "[*]", str(match.full_path))

        if xpath_str not in xpath_dict:
            xpath_dict[xpath_str] = []
        xpath_dict[xpath_str].append(match)
    return xpath_dict


def prompt_user_for_xpath(xpath_dict):
    """Prompt the user to select an XPath if multiple options exist."""
    if len(xpath_dict) > 1:
        print("\nMultiple unique paths found for the attribute. Please select one:")
        for i, xpath in enumerate(xpath_dict.keys(), start=1):
            print(f"  {i}. {xpath}")

        while True:
            try:
                choice = int(input("\nEnter the number of the path to parse: ")) - 1
                if 0 <= choice < len(xpath_dict):
                    selected_xpath = list(xpath_dict.keys())[choice]
                    return selected_xpath
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        return next(iter(xpath_dict))


def get_python_code(selected_xpath):
    """Derive the Python code required to retrieve values using jsonpath-ng."""
    python_code = f"""
from jsonpath_ng import parse

# Load JSON data (assuming 'json_data' is already loaded)
jsonpath_expr = parse("{selected_xpath}")
values = [match.value for match in jsonpath_expr.find(json_data)]
"""
    return python_code.strip()


def extract_values(selected_matches):
    """Extract the values from the selected matches."""
    values = [match.value for match in selected_matches]
    # Flatten list if values contain lists
    return [
        item
        for sublist in values
        for item in (sublist if isinstance(sublist, list) else [sublist])
    ]


def generate_jq_command(selected_xpath, infile: str):
    """Generate the jq command for the selected XPath."""
    jq_path = selected_xpath.replace("$.", ".")  # Remove leading '$'
    jq_path = jq_path.replace(
        "[*]", "[]"
    )  # Convert JSONPath wildcard to jq array syntax
    jq_path = jq_path.replace(".[", "[")  # Convert JSONPath wildcard to jq array syntax
    return f'jq ".{jq_path}?" {infile}'


def display_results(
    attribute: str,
    selected_matches: List[Any],
    values,
    jq_command: str,
    outfile: str,
    python_code: str,
    infile: str,
    logfile: str,
) -> None:
    """Display the results of the selection.

    Args:
        selected_matches (list): The selected matches.
        values (list): The values.
        jq_command (str): The jq command.
        outfile (str): The output file.
        python_code (str): The Python code.
        infile (str): The input file.
        logfile (str): The log file
    """
    distinct_values = list(set(values))
    value_counts = Counter(values)

    with open(outfile, "w") as of:
        of.write(f"## method-created: {os.path.abspath(__file__)}\n")
        of.write(
            f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n"
        )
        of.write(f"## created-by: {os.environ.get('USER')}\n")
        of.write(f"## attribute: {attribute}\n")
        of.write(f"## infile: {infile}\n")
        of.write(f"## logfile: {logfile}\n")

        of.write(
            "\n##\n## Excerpt of objects containing the attribute (full tree to root):\n##\n"
        )

        for match in selected_matches[:3]:  # Show only first 3 unique excerpts
            # Trace back to root object and print the full object tree
            parent_obj = match.context.value
            # Traverse upwards to the root of the object and print the whole structure
            # This prevents infinite loops and ensures we stop at the root
            if isinstance(parent_obj, dict) or isinstance(parent_obj, list):
                of.write(f"\n{json.dumps(match.context.value, indent=2)}\n")

        of.write(
            f"\n##\n## Python code to retrieve values using jsonpath-ng:\n##\n{python_code}\n"
        )

        of.write("\n##\n## Distinct values for the attribute:\n##\n")
        for value in distinct_values:
            of.write(f"  - {value}\n")

        of.write("\n##\n## Distinct values grouped by count:\n##\n")
        for value, count in value_counts.items():
            of.write(f"  - {value}: {count} occurrences\n")

        of.write("\n##\n## Suggested jq command:\n##\n")
        of.write(f"  {jq_command}\n")


def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
    """

    if value is None:
        click.secho(
            "--verbose was not specified and therefore was set to 'True'", fg="yellow"
        )
        return constants.DEFAULT_VERBOSE
    return value


@click.command()
@click.option("--attribute", help="The attribute to query for in the JSON file.")
@click.option("--infile", help="The input JSON file.")
@click.option("--logfile", help="The log file")
@click.option(
    "--outdir",
    help=f"The default is the current working directory - default is '{DEFAULT_OUTDIR}'",
)
@click.option("--outfile", help="The output final report file")
@click.option(
    "--verbose",
    is_flag=True,
    help=f"Will print more info to STDOUT - default is '{constants.DEFAULT_VERBOSE}'.",
    callback=validate_verbose,
)
def main(
    attribute: str, infile: str, logfile: str, outdir: str, outfile: str, verbose: bool
):
    """Parse the JSON file and search for the attribute."""

    error_ctr = 0

    if attribute is None:
        error_console.print("--attribute was not specified")
        error_ctr += 1

    if infile is None:
        error_console.print("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    check_infile_status(infile, "json")

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(
            f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]"
        )

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if outfile is None:
        outfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".txt"
        )
        console.print(
            f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]"
        )

    if logfile is None:
        logfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".log"
        )
        console.print(
            f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]"
        )

    logging.basicConfig(
        filename=logfile,
        format=constants.DEFAULT_LOGGING_FORMAT,
        level=constants.DEFAULT_LOGGING_LEVEL,
    )

    with open(infile, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    extract_attribute(json_data, attribute, infile, outfile, logfile)

    if verbose:
        print(f"The log file is '{logfile}'")
        console.print(
            f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]"
        )


if __name__ == "__main__":
    main()
