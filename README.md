# Video Compressor

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- video_compressor - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and S3 storage. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Deploy the application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

## AWS Lambda Cost Analysis for Video Processing

### Overview

This document provides a cost analysis for using AWS Lambda to process 1,000,000 video files per hour, with each file averaging 10 MB in size. The analysis considers AWS Lambda's pricing tiers and calculates the estimated monthly cost based on the function's memory allocation and execution duration.

### Lambda Pricing

AWS Lambda pricing is based on the number of requests and the duration of each request. The duration cost depends on the amount of memory allocated to the function and the time it takes to execute.

- **Requests Pricing**: $0.20 per 1 million requests
- **Duration Pricing**: Varies based on memory allocation and execution duration

### Examples of Duration Pricing per 1ms

- 128 MB: $0.0000000021
- 512 MB: $0.0000000083
- 1024 MB: $0.0000000167
- 1536 MB: $0.0000000250
- 2048 MB: $0.0000000333

### Assumptions

- Each Lambda function invocation processes a single file.
- The average execution time per file is 1 second (1000 ms).
- The Lambda function is allocated 1024 MB of memory.

### Calculation

#### Monthly Requests

- **Total Files/Request per Month**: 1,000,000 files/hour * (730 hours in a month) = 730000000 per month
- **Amount of memory allocated**: 1024 MB x 0.0009765625 GB in a MB = 1 GB
- **Amount of ephemeral storage allocated**: 512 MB x 0.0009765625 GB in a MB = 0.5 GB

#### Cost for Requests

- **Total Request Cost (Monthly)**: 730,000,000 / 1,000,000 * $0.20 = $146

#### Cost for Duration

Using the price for 1024 MB of memory:

- **Total Compute (Seconds)**: 730,000,000 requests x 300 ms x 0.001 ms to sec conversion factor = 219,000,000.00 total compute (seconds)
- **Total Compute (GB-s)**: 1 GB x 219,000,000.00 seconds = 219,000,000.00 total compute (GB-s)
- **First 6 Billion GB-seconds**: $0.0000166667
- **Monthly Compute Charges**: 219,000,000.00 GB-s x 0.0000166667 USD = 3,650.01 USD

#### Total Monthly Cost

- **Total Cost**: Request Cost + Duration Cost = $146 + $3,650.01 = $3,796.01 USD

### Conclusion

The estimated monthly cost for processing 1,000,000 video files per hour with AWS Lambda, with each invocation allocated 1024 MB of memory, is approximately 3,796.01 USD.

## Cost Optimization Suggestions

1. **Review Execution Time**: Optimize the Lambda function code to reduce execution time, if possible.
2. **Adjust Memory Allocation**: Test with different memory allocations to find the optimal size that does not significantly affect performance but reduces cost.
3. **Use Reserved Concurrency**: Consider purchasing reserved concurrency for predictable workloads to benefit from cost savings.
