from behave.runner import Runner
from behave.configuration import Configuration
from pathlib import Path


def test_runner(*data) -> Path:
    parallel_index, args, args_unknown, tests = data
    json_result_dir: Path = args.output.joinpath('json_results')
    output_file: Path = json_result_dir.joinpath(str(parallel_index) + '.json')

    if not json_result_dir.is_dir():
        json_result_dir.mkdir(parents=True, exist_ok=True)

    # set up the args required to kick off a test run
    behave_command_args: list = []
    for k, v in vars(args.D).items():
        behave_command_args.extend(['-D', f'{k}={v}'])
    behave_command_args.extend(['-D', f'parallel={parallel_index}'])
    behave_command_args.extend(['-f', 'json', '-o', f'{output_file}'])
    behave_command_args.extend(f'--tags={tag}' for tag_group in args.tags for tag in tag_group)
    behave_command_args.append('--no-summary')
    behave_command_args.extend(args_unknown)
    behave_command_args.extend(tests)
    config: Configuration = Configuration(command_args=behave_command_args)
    Runner(config).run()
    return output_file
