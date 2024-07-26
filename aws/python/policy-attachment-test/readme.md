# AWS Policy Attachment Test

This repo reproduces a bug with multiple aws.iam.PolicyAttachment or aws.iam.RolePolicyAttachment resources pointing to the same policy.arn and role.

### Creating multiple aws.iam.PolicyAttachment resources Bug

When creating multiple aws.iam.PolicyAttachment resouces with different logical names, but pointing to the same policy.arn and role; if you delete any of the aws.iam.PolicyAttachment resources, it removes the association between the role and policy.

**EVEN IF their still exists a resource aws.iam.PolicyAttachment pointing to those policy.arn and role resources**.

The code in this pulumi program repoduces this bug.

### Steps to reporduce:

1. Do a `pulumi up` but have only one of the aws.iam.PolicyAttachment resources uncommented
2. After this initial pulumi up, you will see that the policy and the role are correctly attached
3. Uncomment the second aws.iam.PolicyAttachment resource and do a `pulumi up`
4. Nothing changes with the existing resources in the stack, but a new resource is added to the stack and the policy and role are still attached properly
5. Comment out the second aws.iam.PolicyAttachment resource so that pulumi destorys that resource and removes it from the stack/state
6. Now if you check in the AWS console, you'll notice that the policy and role and no longer attached, even though our original aws.iam.PolicyAttachment resource still exists

***NOTE: This can be reproduced with the aws.iam.RolePolicyAttachment resource as well***

#### Links to the Github issues describing this bug:
- https://github.com/pulumi/pulumi/issues/918
- https://github.com/pulumi/pulumi-aws/issues/1980