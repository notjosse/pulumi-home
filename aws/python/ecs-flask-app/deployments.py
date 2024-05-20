import pulumi_pulumiservice as service

deployment_settings_resource = service.DeploymentSettings("deploymentSettingsResource",
    organization="josse-pulumi-corp",
    project="ecs-flask-app",
    source_context=service.DeploymentSettingsSourceContextArgs(
        git=service.DeploymentSettingsGitSourceArgs(
            branch="main",
            repo_dir="https://github.com/notjosse/pulumi-home.git",
            repo_url="aws/python/ecs-flask-app",
        ),
    ),
    stack="dev",
    )