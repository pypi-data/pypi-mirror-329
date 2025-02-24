from enum import Enum
from os import getcwd
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

import click
from tornado.template import Template

from tinybird.tb.modules.feedback_manager import FeedbackManager


class Provider(Enum):
    GitHub = 0
    GitLab = 1


WORKFLOW_VERSION = "v0.0.1"

GITHUB_CI_YML = """
name: Tinybird - CI Workflow

on:
  workflow_dispatch:
  pull_request:
    branches:
      - main
      - master
    types: [opened, reopened, labeled, unlabeled, synchronize]{% if data_project_dir != '.' %}
    paths:
      - '{{ data_project_dir }}/**'{% end %}

concurrency: ${{! github.workflow }}-${{! github.event.pull_request.number }}

jobs:
  ci:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: '{{ data_project_dir }}'
    services:
      tinybird:
        image: tinybirdco/tinybird-local:beta
        ports:
          - 7181:7181
    steps:
      - uses: actions/checkout@v3
      - name: Install Tinybird CLI
        run: curl -LsSf https://api.tinybird.co/static/install.sh | sh
      - name: Build project
        run: tb build
      - name: Test project
        run: tb test run
"""


GITLAB_YML = """
include:
  - local: .gitlab/tinybird/*.yml

stages:
  - tests
"""


GITLAB_CI_YML = """
tinybird_ci_workflow:
  image: ubuntu:latest
  stage: tests
  interruptible: true
  needs: []
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - .gitlab/tinybird/*{% if data_project_dir != '.' %}
        - {{ data_project_dir }}/*
        - {{ data_project_dir }}/**/*{% end %}
  before_script:
    - apt update && apt install -y curl
    - curl -LsSf https://api.tinybird.co/static/install.sh | sh
  script:
    - export PATH="$HOME/.local/bin:$PATH"
    - cd $CI_PROJECT_DIR/{{ data_project_dir }}
    - tb build
    - tb test run
  services:
    - name: tinybirdco/tinybird-local:beta
      alias: tinybird-local
"""


class CICDFile:
    def __init__(
        self,
        template: str,
        file_name: str,
        dir_path: Optional[str] = None,
        warning_message: Optional[str] = None,
    ):
        self.template = template
        self.file_name = file_name
        self.dir_path = dir_path
        self.warning_message = warning_message

    @property
    def full_path(self) -> str:
        return f"{self.dir_path}/{self.file_name}" if self.dir_path else self.file_name


class CICDGeneratorBase:
    cicd_files: List[CICDFile] = []

    def __call__(self, path: str, params: Dict[str, Any]):
        for cicd_file in self.cicd_files:
            if cicd_file.dir_path:
                Path(f"{path}/{cicd_file.dir_path}").mkdir(parents=True, exist_ok=True)
            content = Template(cicd_file.template).generate(**params)
            if Path(f"{path}/{cicd_file.full_path}").exists():
                continue
            with open(f"{path}/{cicd_file.full_path}", "wb") as f:
                f.write(content)
            click.echo(FeedbackManager.info_cicd_file_generated(file_path=cicd_file.full_path))
            if cicd_file.warning_message is not None:
                return FeedbackManager.warning_for_cicd_file(
                    file_name=cicd_file.file_name, warning_message=cicd_file.warning_message.format(**params)
                )

    def is_already_generated(self, path: str) -> bool:
        for cicd_file in self.cicd_files:
            if cicd_file.file_name and Path(f"{path}/{cicd_file.full_path}").exists():
                return True
        return False

    @classmethod
    def build_generator(cls, provider: str) -> Union["GitHubCICDGenerator", "GitLabCICDGenerator"]:
        builder: Dict[str, Union[Type[GitHubCICDGenerator], Type[GitLabCICDGenerator]]] = {
            Provider.GitHub.name: GitHubCICDGenerator,
            Provider.GitLab.name: GitLabCICDGenerator,
        }
        return builder[provider]()


class GitHubCICDGenerator(CICDGeneratorBase):
    cicd_files = [
        CICDFile(
            template=GITHUB_CI_YML,
            file_name="tinybird-ci.yml",
            dir_path=".github/workflows",
        ),
    ]


class GitLabCICDGenerator(CICDGeneratorBase):
    cicd_files = [
        CICDFile(
            template=GITLAB_YML,
            file_name=".gitlab-ci.yml",
            dir_path=".",
        ),
        CICDFile(
            template=GITLAB_CI_YML,
            file_name="tinybird-ci.yml",
            dir_path=".gitlab/tinybird",
        ),
    ]


async def init_cicd(
    path: Optional[str] = None,
    data_project_dir: Optional[str] = None,
):
    for provider in Provider:
        path = path if path else getcwd()
        data_project_dir = data_project_dir if data_project_dir else "."
        generator = CICDGeneratorBase.build_generator(provider.name)
        params = {
            "data_project_dir": data_project_dir,
            "workflow_version": WORKFLOW_VERSION,
        }
        warning_message = generator(path, params)
        if warning_message:
            click.echo(warning_message)


async def check_cicd_exists(path: Optional[str] = None) -> Optional[Provider]:
    path = path if path else getcwd()
    for provider in Provider:
        generator = CICDGeneratorBase.build_generator(provider.name)
        if generator.is_already_generated(path):
            return provider
    return None
