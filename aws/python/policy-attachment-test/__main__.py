"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

suffix = 'josse'

# Create an AWS resource (S3 Bucket)
bucket = aws.s3.Bucket(f'my-bucket-{suffix}')

lambda_assume_role_policy = aws.iam.get_policy_document(statements=[{
    "actions": ["sts:AssumeRole"],
    "principals": [{
        "type": "Service",
        "identifiers": ["lambda.amazonaws.com"],
    }],
}])

lambda_role = aws.iam.Role(
    f"lambda-role-{suffix}",
    name=f"lambda-role-{suffix}",
    assume_role_policy=lambda_assume_role_policy.json,
    description='role to be assumed by lambda function')

lambda_role_bucket_policy = aws.iam.Policy(
    f"lambda-role-policy-{suffix}",
    name=f"lambda-role-policy-{suffix}",
    description="allow lambda function to get all objects from bucket",
    policy=pulumi.Output.json_dumps(
        {
        "Version": "2012-10-17",
        "Statement": [{
            "Action": ["s3:GetObject"],
            "Effect": "Allow",
            "Resource": bucket.arn.apply(lambda arn: f'{arn}/*'),
        }],
    })
)

lambda_role_policy_attachment = aws.iam.PolicyAttachment(
    f"lambda-role-policy-attach-{suffix}",
    name=f"lambda-role-policy-attach-{suffix}",
    policy_arn=lambda_role_bucket_policy.arn,
    roles=[lambda_role.name],
)

# lambda_role_policy_attachment2 = aws.iam.PolicyAttachment(
#     f"lambda-role-policy-attach-{suffix}-2",
#     name=f"lambda-role-policy-attach-{suffix}-2",
#     policy_arn=lambda_role_bucket_policy.arn,
#     roles=[lambda_role.name],
# )


# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
