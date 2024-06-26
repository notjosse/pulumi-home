import pulumi
import pulumi_pulumiservice as service

deployment_settings_resource = service.DeploymentSettings(
    "dev-deployment",
    organization=pulumi.get_organization(),
    project=pulumi.get_project(),
    source_context=service.DeploymentSettingsSourceContextArgs(
        git=service.DeploymentSettingsGitSourceArgs(
            branch="main",
            repo_url="https://github.com/notjosse/pulumi-home.git",
            repo_dir="aws/python/ecs-flask-app",
        ),
    ),
    stack=pulumi.get_stack(),
    )