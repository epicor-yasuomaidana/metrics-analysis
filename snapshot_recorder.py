import os
import re

from chrome_utils import ChromeDriver, ChromeOptions, GrafanaUrlInputs


def generate_name(pattern: str, url_inputs: GrafanaUrlInputs):
    pattern = pattern.format(url_inputs.names_space, url_inputs.from_ts)
    if url_inputs.identifier:
        pattern = pattern + f" {url_inputs.identifier}"
    return pattern


import click


@click.command()
@click.argument('names_space', type=str)
@click.argument('from_ts', type=str)
@click.option('--to-ts', type=str, help='End timestamp format: %Y-%m-%d %H:%M:%S ')
@click.option('--identifier', default="", type=str, help='Identifier')
@click.option('--delta', type=str, default="1h20m", help='Default delta time if --to-ts is not provided (e.g., 1h20m)')
def main(names_space, from_ts, to_ts, identifier, delta):
    """
    Main entry point for the snapshot recorder CLI.

    Args:\n
        names_space (str): The namespace for the Grafana dashboard.\n
        from_ts (str): Start timestamp in '%Y-%m-%d %H:%M:%S' format.\n
        to_ts (str): End timestamp in '%Y-%m-%d %H:%M:%S' format.\n
        identifier (str): Optional identifier for the snapshot.\n

    This function initializes Chrome options, prepares Grafana URL inputs,
    iterates over dashboard versions and names, and interacts with the user
    to record snapshots.
    """

    chrome_profile_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data",
                                       "Default")
    options = ChromeOptions(chrome_profile_path, "Default")

    if not to_ts:
        from datetime import datetime, timedelta
        from_ts_dt = datetime.strptime(from_ts, "%Y-%m-%d %H:%M:%S")
        delta_match = re.match(r"(?:(\d+)h)?(?:(\d+)m)?", delta)
        hours = int(delta_match.group(1)) if delta_match.group(1) else 0
        minutes = int(delta_match.group(2)) if delta_match.group(2) else 0
        to_ts_dt = from_ts_dt + timedelta(hours=hours, minutes=minutes)
        to_ts = to_ts_dt.strftime("%Y-%m-%d %H:%M:%S")

    grafana_inputs = GrafanaUrlInputs(
        from_ts=from_ts,
        to_ts=to_ts,
        names_space=names_space,
        identifier=identifier,
        version="caef215f-c5eb-4e98-8fd6-6d0a7ffa378a/k6-execution-monitoring"
    )
    recorder = ChromeDriver(grafana_inputs, options)
    versions = ["caef215f-c5eb-4e98-8fd6-6d0a7ffa378a/k6-execution-monitoring",
                "besqnnwstd0cgd/7870e96c-4f6f-5b74-9169-d99fdbd190bf",
                "rD8loTpLs/143a66de-4a8f-5ce0-be10-2c30cd4970b2"]
    names = ["K6 Result - {} {}", "SQL Monitor - {} {}", ("Pod {} AppServer - {}", "Pod {} TaskAgent - {}")]
    keys = ["K6", "AppServer", "TaskAgent", "SQL"]
    values = []
    for version, name in zip(versions, names):
        grafana_inputs.version = version
        recorder.go_to_dashboard(grafana_inputs.build_url())
        if isinstance(name, str):
            print(f"\033[94m{generate_name(name, grafana_inputs)}\033[0m")
            values.append(input("Paste dashboard url:"))
        else:
            for n in name:
                print(f"\033[94m{generate_name(n, grafana_inputs)}\033[0m")
                values.append(input("Paste dashboard url:"))
    recorder.driver.close()
    print("\n\n")
    print(f"{names_space} {from_ts.split()[0]} 📅  {from_ts.split()[1]} ⌛  {identifier}")
    for key, value in zip(keys, values):
        print(f"{key}: {value}")


if __name__ == '__main__':
    main()
