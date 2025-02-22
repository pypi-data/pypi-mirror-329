import os
import subprocess
import time

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        super().initialize(version, build_data)

        # Get the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        print(f'custom build, dir is {project_dir}')

    def finalize(self, version, build_data, artifact_directory):
        if os.environ.get("SKIP_CUSTOM_BUILD"):
            return  # exit immediately if we've already done the second build

        # # 2. Prepare a new environment for the second build
        env = os.environ.copy()
        env["SKIP_CUSTOM_BUILD"] = "1"  # ensures we don't recurse again

        try:
            # Temporarily change the build directory for the second build
            with open("pyproject.toml", "r") as file:
                original_config = file.read()

            modified_config = original_config.replace(
                "name = \"sagemaker-studio-dataengineering-sessions\"",
                "name = \"amzn-sagemaker-studio-dataengineering-sessions\"",
            )

            modified_config = modified_config.replace(
                "directory = \"./external-distribution\"",
                "directory = \"./build\""
            )

            modified_config = modified_config.replace(
                'packages = ["src/sagemaker_studio_dataengineering_sessions"]',
                'packages = ["external-distribution"]'
            )

            modified_config = modified_config.replace(
                'include = ["src/sagemaker_studio_dataengineering_sessions"]',
                'include = ["external-distribution"]'
            )

            with open("pyproject.toml", "w") as file:
                file.write(modified_config)

            subprocess.run([
                ".venv/bin/python3", "-m", "pip", "install", "hatch"
            ], env=env, check=True)

            time.sleep(7)

            subprocess.run([
                ".venv/bin/python3", "-m", "hatch", "build"
            ], env=env, check=True)

            # Restore the original pyproject.toml configuration
            with open("pyproject.toml", "w") as file:
                file.write(original_config)
        finally:
            # Restore the original pyproject.toml configuration
            with open("pyproject.toml", "w") as file:
                file.write(original_config)


