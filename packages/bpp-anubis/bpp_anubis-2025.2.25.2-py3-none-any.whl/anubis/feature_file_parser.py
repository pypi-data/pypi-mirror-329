import os
from behave.model import Feature as BehaveFeature, Scenario, ScenarioOutline
from behave.model_core import FileLocation
from behave.parser import parse_file
from behave.tag_expression import TagExpression
from glob import glob
from pathlib import Path


def get_tests(paths: list, tags: list, unit: str) -> list[BehaveFeature]:
    """Given a list of feature files and tags, return a list of tests matching those criteria"""
    parsed_gherkin = parse_tests(paths)
    return get_testable_tests(parsed_gherkin, tags, unit)


def parse_tests(paths: list) -> list[BehaveFeature]:
    """Given a list of feature files parse each feature and return list of tests"""
    parsed_gherkin: list[BehaveFeature] = []

    # get all paths to the feature files and take care of duplicates
    all_paths: list = []
    for path in paths:
        all_paths.extend([path] if os.path.isfile(path) else glob(f'{path}/**/*.feature', recursive=True))

    # parse the feature files, remove None cases
    for path in set([Path(str(Path(path).absolute())) for path in all_paths]):
        parsed_gherkin.append(parse_file(path))

    return [gherkin for gherkin in parsed_gherkin if gherkin]


def get_testable_tests(gherkin: list[BehaveFeature], tags: list[list[str]], unit) -> list[BehaveFeature]:
    """given a list of tests and tags, return tests that match those tags"""
    tags: list = [tag for group in tags for tag in group]
    testable_tests: list = []
    expression: TagExpression = TagExpression(tags)

    if unit.lower() == 'feature':
        testable_tests.extend([f for f in gherkin if expression.check(f.tags)])
    elif unit.lower() == 'scenario':
        for feature in gherkin:
            for scenario in feature.scenarios:
                if expression.check(list(set(feature.tags + scenario.effective_tags))):
                    testable_tests.append(scenario)
    else:  # unit == 'example'
        for feature in gherkin:
            for scenario in feature.scenarios:
                if isinstance(scenario, ScenarioOutline):
                    for ex_table in scenario.examples:
                        if expression.check(list(set(scenario.effective_tags + ex_table.tags + feature.tags))):
                            for row in ex_table.table.rows:
                                setattr(row, 'location', FileLocation(f'{ex_table.filename}', row.line))
                                testable_tests.append(row)
                elif isinstance(scenario, Scenario) and expression.check(scenario.tags + feature.tags):
                    testable_tests.append(scenario)
    [setattr(item, 'location', FileLocation(os.path.join(os.getcwd(), f'{item.location}'), item.line)) for item in testable_tests]
    return testable_tests
