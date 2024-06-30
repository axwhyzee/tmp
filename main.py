from dataclasses import asdict, dataclass
from typing import Iterable
import yaml
from pathlib import Path
import logging

from models.common import TestName
from models.models import BaseTest, GeneralTSSTest

logger = logging.getLogger(__name__)


@dataclass
class VerifierConfig:
    module: str
    run_on: str
    timezone: str = 'UTC'
    days_start: int | None = None
    skip_non_trading: bool | None = True


def test_factory(test_name: TestName):
    if test_name == TestName.TSS_DAYS_START:
        return 


def to_yaml(
    module_config: VerifierConfig, 
    tests: Iterable[BaseTest]
) -> None:
    RELATIVE_VERIFIER_DIR = 'verifiers'

    verifier_yaml_path = Path(RELATIVE_VERIFIER_DIR) / f'{module_config.module}.yaml'
    
    if verifier_yaml_path.exists():
        return logger.error(f'There is another verifier with same module name: {verifier_yaml_path}')

    verifier_json = {k: v for k, v in asdict(module_config).items() if v}
    verifier_json['tests'] = [verifier_method.__dict__ for verifier_method in tests]

    yaml.safe_dump(verifier_json, default_flow_style=False, sort_keys=False)


to_yaml(VerifierConfig('module', 'trday.US'), [])