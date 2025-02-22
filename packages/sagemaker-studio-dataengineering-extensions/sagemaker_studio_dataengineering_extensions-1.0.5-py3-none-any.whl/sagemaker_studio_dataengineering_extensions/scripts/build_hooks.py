from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import os
import time
import subprocess

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        super().initialize(version, build_data)

        # Get the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        print(f'custom build script triggered, dir is {project_dir}')

        # test the run_commands function
        # uncomment this and run bb when make changes in run_commands function
        # self.test_run_commands()

        if os.environ.get("SKIP_CUSTOM_BUILD"):
            print("skipping custom build initialize")
            return  # exit immediately if we've already done the second build

        self.prepare_env()

        self.build_spark_monitoring_widget()
        self.build_data_explorer()
        self.build_connection_magic_jlextension()
        self.build_ui_doc_manager()
        self.build_studio_ui_theme()

    def run_commands(self, *commands, fail_fast=True):
        """
        Run one or more terminal commands and return their output.

        Args:
        *commands: Variable number of command strings to execute.

        Returns:
        A list of tuples, each containing the command, return code, stdout, and stderr.
        """
        results = []

        for cmd in commands:
            try:
                # Run the command and capture output
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                
                # Get the return code
                return_code = process.returncode


                if fail_fast and return_code != 0:
                # If fail_fast is True and an exception occurred, stop execution
                    raise BuildException(f'command {cmd} failed with return_code {return_code}\n stdout is {stdout}\n stderr is {stderr}')
                # Append results
                results.append((cmd, return_code, stdout.strip(), stderr.strip()))

            except BuildException as e:
                raise e
            except Exception as e:
                # If there's an error running the command, capture it
                results.append((cmd, -1, "", str(e)))

        return results

    def test_run_commands(self):
        commands = [
            "echo Hello, World!",
            "ls -l",
            "invalid_command",  # This will cause an error
            "pwd"
        ]
        output = self.run_commands(*commands)
        for cmd, return_code, out, error in output:
            print(f'cmd {cmd} with return_code {return_code}, out is {out}, error is {error}')

    def prepare_env(self):
        print(f"running prepare_env commands")
        commands = [
            #configure npm
            "peru-npm configure-npm",
        ]

        CONDA_BUILD = os.environ.get('CONDA_BUILD', False)

        if not CONDA_BUILD:
            output = self.run_commands(*commands)

    def build_spark_monitoring_widget(self):
        print(f"running build_spark_monitoring_widget commands")
        dir = "src/sagemaker_studio_dataengineering_extensions/sagemaker_spark_monitor_widget"
        
        build_commands = [
            f"cd {dir} && jlpm install && jlpm build:lib && jlpm build:lib:prod && jlpm run build:labextension && rm -r .yarn lib node_modules"
        ]

        conda_commands = [
            f"cd {dir} && rm -rf .npmrc .yarnrc.yml && npm install"
        ]

        conda_commands.extend(build_commands)

        # command for brazil-build
        commands = [
            # copy npm config generated from peru-npm to current dir
            f"cp .npmrc {dir}/ ",
            # configure npm server jlpm(yarn) is using to point to internal amazon registry
            f"cd {dir} && jlpm config set npmRegistryServer $(run-npm config get registry)",
            # configure http whitelist of jlpm(yarn) as it's http registry and was refused in jlpm(yarn) by default
            f"cd {dir} && jlpm config set unsafeHttpWhitelist $(echo $(run-npm config get registry) | sed -E 's#^(https?://)?([^/:]+)(:[0-9]+)?.*#\\2#')",
        ]
        commands.extend(build_commands)

        CONDA_BUILD = os.environ.get('CONDA_BUILD', False)

        if CONDA_BUILD:
            print(f"running conda build")
            output = self.run_commands(*conda_commands)
        else:
            output = self.run_commands(*commands)
        
        # debugging info
        # for cmd, return_code, out, error in output:
        #     print(f'building spark_monitoring_widget --- cmd "{cmd}" with return_code {return_code}, out is {out}, error is {error}')
    
    def build_data_explorer(self):
        dir = "src/sagemaker_studio_dataengineering_extensions/sagemaker_data_explorer"
        commands = [
            #configure npm
            "peru-npm configure-npm",
            # configure npm server jlpm(yarn) is using to point to internal amazon registry
            f"cd {dir} && jlpm config set npmRegistryServer $(run-npm config get registry)",
            # configure http whitelist of jlpm(yarn) as it's http registry and was refused in jlpm(yarn) by default
            f"cd {dir} && jlpm config set unsafeHttpWhitelist $(echo $(run-npm config get registry) | sed -E 's#^(https?://)?([^/:]+)(:[0-9]+)?.*#\\2#')",
            # command to build spark monitor
            f"cd {dir} && jlpm install && jlpm build:prod && rm -r .yarn lib node_modules"
        ]

        conda_commands = [
            f"cd {dir} && rm -rf .npmrc .yarnrc.yml && npm install && jlpm install && jlpm build:prod && rm -r .yarn lib node_modules"
        ]

        CONDA_BUILD = os.environ.get('CONDA_BUILD', False)
 
        if CONDA_BUILD:
            print(f"running conda build")
            output = self.run_commands(*conda_commands)
        else:
            output = self.run_commands(*commands)

    def build_connection_magic_jlextension(self):
        print(f"running build_connection_magic_jlextension commands")
        dir = "src/sagemaker_studio_dataengineering_extensions/sagemaker_connection_magics_jlextension"
        
        build_commands = [
            # command to build
            f"cd {dir} && npm install && npm run clean && npm run build:lib:prod && npm run build:labextension",
            # command to clean up
            f"cd {dir} && rm -rf build lib node_modules dist",
        ]

        conda_commands = [
            f"cd {dir} && rm -rf .npmrc"
        ]

        conda_commands.extend(build_commands)

        # command for brazil-build
        commands = [
            # copy npm config generated from peru-npm to current dir
            f"cp .npmrc {dir}/ ",
        ]

        commands.extend(build_commands)

        CONDA_BUILD = os.environ.get('CONDA_BUILD', False)

        if CONDA_BUILD:
            print(f"running conda build")
            output = self.run_commands(*conda_commands)
        else:
            output = self.run_commands(*commands)

    def build_ui_doc_manager(self):
        print(f"running sagemaker_ui_doc_manager_jl_plugin commands")
        dir = "src/sagemaker_studio_dataengineering_extensions/sagemaker_ui_doc_manager_jl_plugin"

        build_commands = [
            # command to build
            f"cd {dir} && npm install && npm run build:prod",

            # command to clean up
            f"cd {dir} && rm -rf build lib node_modules",
        ]

        conda_commands = [
            f"cd {dir} && rm -rf .npmrc"
        ]

        conda_commands.extend(build_commands)

        # command for brazil-build
        commands = [
            # copy npm config generated from peru-npm to current dir
            f"cp .npmrc {dir}/ ",
        ]

        commands.extend(build_commands)

        CONDA_BUILD = os.environ.get('CONDA_BUILD', False)

        if CONDA_BUILD:
            print(f"running conda build")
            output = self.run_commands(*conda_commands)
        else:
            output = self.run_commands(*commands)

    def build_studio_ui_theme(self):
        print(f"running sagemaker_studio_theme build")
        dir = "src/sagemaker_studio_dataengineering_extensions/sagemaker_studio_theme"

        build_commands = [
            # command to build
            f"cd {dir} && npm install && npm run build:prod",

            # command to clean up
            f"cd {dir} && rm -rf build lib node_modules",
        ]

        conda_commands = [
            f"cd {dir} && rm -rf .npmrc"
        ]

        conda_commands.extend(build_commands)

        # command for brazil-build
        commands = [
            # copy npm config generated from peru-npm to current dir
            f"cp .npmrc {dir}/ ",
        ]

        commands.extend(build_commands)

        CONDA_BUILD = os.environ.get('CONDA_BUILD', False)

        if CONDA_BUILD:
            print(f"running conda build")
            output = self.run_commands(*conda_commands)
        else:
            output = self.run_commands(*commands)

    def finalize(self, version, build_data, artifact_directory):
        if os.environ.get("SKIP_CUSTOM_BUILD"):
            print("skipping custom build finalize")
            return  # exit immediately if we've already done the second build

        # 2. Prepare a new environment for the second build
        env = os.environ.copy()
        env["SKIP_CUSTOM_BUILD"] = "1"  # ensures we don't recurse again

        try:
            # Temporarily change the build directory for the second build
            with open("pyproject.toml", "r") as file:
                original_config = file.read()

            modified_config = original_config.replace(
                "name = \"sagemaker-studio-dataengineering-extensions\"",
                "name = \"amzn-sagemaker-studio-dataengineering-extensions\"",
            )

            modified_config = modified_config.replace(
                "directory = \"./external-distribution\"",
                "directory = \"./build\""
            )

            modified_config = modified_config.replace(
                'packages = ["src/sagemaker_studio_dataengineering_extensions"]',
                'packages = ["external-distribution"]'
            )

            modified_config = modified_config.replace(
                'include = ["src/sagemaker_studio_dataengineering_extensions"]',
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

class BuildException(Exception):
    pass
