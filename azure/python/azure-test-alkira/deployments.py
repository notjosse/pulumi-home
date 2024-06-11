import pulumi
import pulumi_pulumiservice as service

deployment_settings_resource = service.DeploymentSettings(
    "dev-deployment",
    organization=pulumi.get_organization(),
    project=pulumi.get_project(),
    operation_context=service.DeploymentSettingsOperationContextArgs(
        # pre_run_commands=[],
    ),
    source_context=service.DeploymentSettingsSourceContextArgs(
        git=service.DeploymentSettingsGitSourceArgs(
            branch="develop",
            repo_url="https://github.com/notjosse/pulumi-home.git",
            repo_dir="azure/python/azure-test-alkira",
        ),
    ),
    stack=pulumi.get_stack(),
    )