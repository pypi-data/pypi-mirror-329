import json
import logging
import os
from datetime import datetime as dt
from json.decoder import JSONDecodeError
from pathlib import Path
from time import gmtime, strftime

GREEN_START = '\033[92m'
GREY_START = '\033[90m'
RED_START = '\033[91m'
END_COLOR = '\033[0m'
linesep = os.linesep
tab = '\t'

logger = logging.getLogger()


# helpers ---------------------------------------------------------------------
def __get_widths(feature_path, s, p, f, hide_sum, hide_passed, hide_failed, extra_width=0) -> tuple:
    """This does all the terrible work of finding the widths of lines for output"""
    # todo - simplify this at some point
    width_p_name: int = max([len(line['name']) for line in p]) if p else 0
    width_p_location: int = max([len(line['location']) for line in p]) if p else 0
    width_f_name: int = max([len(line['name']) for line in f]) if f else 0
    width_f_location: int = max([len(line['location']) for line in f]) if f else 0
    width_s: int = max([len(line) for line in s])

    return (
        max(
            len(feature_path),
            (width_p_name + width_p_location) * int(not hide_passed),
            (width_f_name + width_f_location) * int(not hide_failed),
            width_s * int(not hide_sum)) + extra_width,
        width_p_name,
        width_p_location,
        width_f_name,
        width_f_location,
        width_s
    )


# ----------------------------------------------------------------------------
def handle_passing_failing_scenarios(width: int, scenarios: list) -> str:
    scenarios: list = sorted(list(scenarios), key=lambda test: int(test['location'].split(':')[-1]))
    details: list = []

    for s in scenarios:
        dc = GREEN_START if s["status"].lower() == 'passed' else RED_START
        details.append({
            'scenario': f'{tab}{dc}●{END_COLOR} {s["name"].ljust(width)}{tab}{GREY_START}',
            'location': f'# {s["location"]}{END_COLOR}'
        })
    return '\n'.join([s['scenario'] + s['location'] for s in details])


def write_result_aggregate(files: list[Path], aggregate_out_file):
    """Combine json files into one json file"""
    agg_fp: Path = Path(aggregate_out_file)
    aggregate: list = []

    for fp in files:
        try:
            with fp.open('r') as f:
                current_file_data = json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            current_file_data = []
        aggregate += current_file_data

    with agg_fp.open('w+', encoding='utf-8') as f:
        f.write(json.dumps(aggregate))


def get_result_values(aggregate_file: str):
    try:
        with open(aggregate_file) as f:
            res: dict = json.load(f)
    except FileNotFoundError:
        return 0, 0, 0

    statuses: list = []
    for feature in res:
        if 'elements' in feature:
            for scenario in feature['elements']:
                if scenario['type'] != 'background':
                    statuses.append(scenario['status'])

    passed: int = statuses.count('passed')
    failed: int = statuses.count('failed')
    total: int = passed + failed
    return passed, failed, total


def print_result_summary(args, start, end, num_passed, num_failed):
    total: int = num_passed + num_failed
    pass_rate: str = f'{num_passed / total * 100:.2f}%' if total > 0 else 'n/a'
    fail_rate: str = f'{num_failed / total * 100:.2f}%' if total > 0 else 'n/a'
    pass_txt: str  = f'{tab}Passed:  <{num_passed}, {pass_rate}>'
    fail_txt: str  = f'{tab}Failed:  <{num_failed}, {fail_rate}>'
    run_txt: str   = f'{tab}Runtime: <{strftime("%Hh %Mm %Ss", gmtime((end - start).total_seconds()))}>'
    summary: list = [pass_rate, fail_rate, pass_txt, fail_txt, run_txt]

    with args.aggregate.open() as f:
        res: dict = json.load(f)

    for feature_path in set([feature.get('location', '') for feature in res]):
        elements = [e for f in res for e in f.get('elements', []) if f.get('location', '') == feature_path]
        passed: list = [e for e in elements if e['type'] != 'background' and e['status'].lower() == 'passed']
        failed: list = [e for e in elements if e['type'] != 'background' and e['status'].lower() == 'failed']
        elements_with_results = passed + failed

        width, width_pn, _, _, _, _ = __get_widths(feature_path.split(":")[0],
            summary, passed, failed, args.hide_passed, args.hide_failed, args.hide_summary, 4 * len(tab))

        result_details_print = handle_passing_failing_scenarios(width_pn, elements_with_results)
        print(f'\n{feature_path.split(":")[0]} '.ljust(width, '-') + '\n' + result_details_print)

    if not args.hide_summary:
        print('\nResults Summary ♡𓃥♡', pass_txt, fail_txt, run_txt, sep='\n')


def json_results_to_xml(start_time: dt, json_file: Path, junit_file: Path):
    screenshot_path: str = ""

    with json_file.open("r") as f:
        results: dict = json.loads(f.read())
    scenarios: list = [scenario for feature in results for scenario in feature.get("elements", {}) if
                 scenario.get("type").lower() == "scenario"]

    with junit_file.open("w") as f:
        f.write(
            '<testsuite name="RegressionSuite"'
            f' tests="{len([s for s in scenarios if s.get("type") == "scenario"])}"'
            f' errors="{len([s for s in scenarios if s.get("status") not in ["passed", "failed", "skipped"]])}"'
            f' failures="{len([s for s in scenarios if s.get("status", "").lower() == "failed"])}"'
            f' skipped="{len([s for s in scenarios if s.get("status", "").lower() == "skipped"])}"'
            f' timestamp="{dt.now().isoformat()}">\n'
        )

        for s in scenarios:
            f.write(
                "<testcase"
                f' classname="{".".join(s.get("location").lstrip("features/").split("/")).split(":")[0]}"'
                f' name="{s.get("name")}"'
                f' status="{s.get("status")}"'
                f' time="{sum([step.get("result", {}).get("duration", 0) for step in s.get("steps", [])]):.6f}">\n'
            )

            # I know this is ugly, but this just needs to make the file
            if s.get("status").lower() == "failed":
                failed_step: dict = next(
                    step for step in s.get("steps", []) if
                    step.get("result", {}).get("status", "").lower() == "failed"
                )
                error_value: list | str = failed_step.get("result", {}).get("error_message", "")
                error_message: str = error_value if isinstance(error_value, str) else "\n".join(
                    line for line in error_value)

                # add the screenshot
                so_name: str = s["name"].title().replace(" ", "").replace('"', "")
                sp_name: str = failed_step.get("name", "n/a").title().replace(" ", "").replace('"', "")
                screenshot_path = os.path.join(".output", "screenshots", f"{so_name}--{sp_name}.png")

                f.write("<failure>\n")
                f.write("<![CDATA[\n")
                f.write(
                    f'Failing step: {failed_step.get("keyword", "n/a")} {failed_step.get("name", "n/a")}'
                    + f' ... failed in {failed_step.get("result", {}).get("duration", "n/a"):.3f}s\n'
                )
                f.write(f'Location: {failed_step.get("location")}\n')
                f.write(error_message + "\n")
                f.write("]]>\n")
                f.write("</failure>\n")

            f.write("<system-out>\n")

            if s.get("status").lower() == "failed" and os.path.isfile(screenshot_path):
                f.write(f"[[ATTACHMENT|{screenshot_path}]]")

            f.write("<![CDATA[\n@scenario.begin\n")
            f.write(" ".join(f"@{tag}" for tag in s.get("tags", [])) + "\n")
            f.write("" + s.get("keyword") + ": " + s.get("name") + "\n")
            for step in s.get("steps", []):
                # step_result = step.get("result", {})
                step_status = step.get("result", {}).get("status", "(step skipped)")
                step_duration = step.get("result", {}).get("duration", None)
                step_text = f"in {step_duration:.2f}s" if step_status != "(step skipped)" else ""
                f.write(f"\t{step.get('keyword')} {step.get('name')} ... {step_status} {step_text}\n")
            f.write(
                "@scenario.end\n--------------------------------------------------------------------------------\n]]>\n")
            f.write("</system-out>\n</testcase>\n\n")
        f.write("</testsuite>\n")
