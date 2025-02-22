r'''
# Datadog CDK Constructs

[![NPM](https://img.shields.io/npm/v/datadog-cdk-constructs?color=blue&label=npm+cdk+v1)](https://www.npmjs.com/package/datadog-cdk-constructs)
[![NPM](https://img.shields.io/npm/v/datadog-cdk-constructs-v2?color=39a356&label=npm+cdk+v2)](https://www.npmjs.com/package/datadog-cdk-constructs-v2)
[![PyPI](https://img.shields.io/pypi/v/datadog-cdk-constructs?color=blue&label=pypi+cdk+v1)](https://pypi.org/project/datadog-cdk-constructs/)
[![PyPI](https://img.shields.io/pypi/v/datadog-cdk-constructs-v2?color=39a356&label=pypi+cdk+v2)](https://pypi.org/project/datadog-cdk-constructs-v2/)
[![Go](https://img.shields.io/github/v/tag/datadog/datadog-cdk-constructs-go?color=39a356&label=go+cdk+v2)](https://pkg.go.dev/github.com/DataDog/datadog-cdk-constructs-go/ddcdkconstruct)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/DataDog/datadog-cdk-constructs/blob/main/LICENSE)

Use this Datadog CDK Construct Library to deploy serverless applications using AWS CDK .

This CDK library automatically configures ingestion of metrics, traces, and logs from your serverless applications by:

* Installing and configuring the Datadog Lambda layers for your [.NET](https://docs.datadoghq.com/serverless/aws_lambda/installation/dotnet), [Java](https://docs.datadoghq.com/serverless/installation/java/?tab=awscdk), [Node.js](https://github.com/DataDog/datadog-lambda-layer-js), and [Python](https://github.com/DataDog/datadog-lambda-layer-python) Lambda functions.
* Enabling the collection of traces and custom metrics from your Lambda functions.
* Managing subscriptions from the Datadog Forwarder to your Lambda and non-Lambda log groups.

## AWS CDK v1 vs AWS CDK v2

**WARNING**: `AWS CDK v1` has reached end-of-support and `datadog-cdk-constructs` will no longer be receiving updates. It's strongly recommended to upgrade to `AWS CDK v2` ([official migration guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html)) and switch to using `datadog-cdk-constructs-v2`.

Two separate versions of Datadog CDK Constructs exist; `datadog-cdk-constructs` and `datadog-cdk-constructs-v2`. These are designed to work with `AWS CDK v1` and `AWS CDK v2` respectively.

* `datadog-cdk-constructs-v2` requires Node >= 14, while `datadog-cdk-constructs` supports Node >= 12.
* `datadog-cdk-constructs-v2` contains more features.
* Otherwise, the use of the two packages is identical.

## Lambda

### Package Installation

#### npm

For use with AWS CDK v2:

```
yarn add --dev datadog-cdk-constructs-v2
# or
npm install datadog-cdk-constructs-v2 --save-dev
```

For use with AWS CDK v1:

```
yarn add --dev datadog-cdk-constructs
# or
npm install datadog-cdk-constructs --save-dev
```

#### PyPI

For use with AWS CDK v2:

```
pip install datadog-cdk-constructs-v2
```

For use with AWS CDK v1:

```
pip install datadog-cdk-constructs
```

##### Note:

Pay attention to the output from your package manager as the `Datadog CDK Construct Library` has peer dependencies.

#### Go

For use with AWS CDK v2:

```
go get github.com/DataDog/datadog-cdk-constructs-go/ddcdkconstruct
```

AWS CDK v1 is not supported.

### Usage

#### AWS CDK

*The following examples assume the use of AWS CDK v2. If you're using CDK v1, import `datadog-cdk-constructs` rather than `datadog-cdk-constructs-v2`.*

Add this to your CDK stack:

#### TypeScript

```python
import { DatadogLambda } from "datadog-cdk-constructs-v2";

const datadogLambda = new DatadogLambda(this, "datadogLambda", {
  nodeLayerVersion: <LAYER_VERSION>,
  pythonLayerVersion: <LAYER_VERSION>,
  javaLayerVersion: <LAYER_VERSION>,
  dotnetLayerVersion: <LAYER_VERSION>
  addLayers: <BOOLEAN>,
  extensionLayerVersion: "<EXTENSION_VERSION>",
  forwarderArn: "<FORWARDER_ARN>",
  createForwarderPermissions: <BOOLEAN>,
  flushMetricsToLogs: <BOOLEAN>,
  site: "<SITE>",
  apiKey: "{Datadog_API_Key}",
  apiKeySecretArn: "{Secret_ARN_Datadog_API_Key}",
  apiKeySecret: <AWS_CDK_ISECRET>, // Only available in datadog-cdk-constructs-v2
  apiKmsKey: "{Encrypted_Datadog_API_Key}",
  enableDatadogTracing: <BOOLEAN>,
  enableMergeXrayTraces: <BOOLEAN>,
  enableDatadogLogs: <BOOLEAN>,
  injectLogContext: <BOOLEAN>,
  logLevel: <STRING>,
  env: <STRING>, //Optional
  service: <STRING>, //Optional
  version: <STRING>, //Optional
  tags: <STRING>, //Optional
});
datadogLambda.addLambdaFunctions([<LAMBDA_FUNCTIONS>])
datadogLambda.addForwarderToNonLambdaLogGroups([<LOG_GROUPS>])
```

#### Go

```go
import (
	"github.com/DataDog/datadog-cdk-constructs-go/ddcdkconstruct"
)
datadogLambda := ddcdkconstruct.NewDatadogLambda(
    stack,
    jsii.String("Datadog"),
    &ddcdkconstruct.DatadogLambdaProps{
        NodeLayerVersion:      jsii.Number(<LAYER_VERSION>),
        AddLayers:             jsii.Bool(<BOOLEAN>),
        Site:                  jsii.String(<SITE>),
        ApiKey:                jsii.String(os.Getenv("DD_API_KEY")),
        // ...
    })
datadogLambda.AddLambdaFunctions(&[]interface{}{myFunction}, nil)
datadogLambda.AddForwarderToNonLambdaLogGroups()
```

### Source Code Integration

[Source code integration](https://docs.datadoghq.com/integrations/guide/source-code-integration/) is enabled by default through automatic lambda tagging, and will work if:

* The Datadog Github integration is installed.
* Your datadog-cdk dependency satisfies either of the below versions:

  * `datadog-cdk-constructs-v2` >= 1.4.0
  * `datadog-cdk-constructs` >= 0.8.5

#### Alternative Methods to Enable Source Code Integration

If the automatic implementation doesn't work for your case, please follow one of the two guides below.

**Note: these alternate guides only work for Typescript.**

<details>
  <summary>datadog-cdk version satisfied, but Datadog Github integration NOT installed</summary>

If the Datadog Github integration is not installed, you need to import the `datadog-ci` package and manually upload your Git metadata to Datadog.
For the best results, import the `datadog-ci` package where your CDK Stack is initialized.

```python
const app = new cdk.App();

// Make sure to add @datadog/datadog-ci via your package manager
const datadogCi = require("@datadog/datadog-ci");
// Manually uploading Git metadata to Datadog.
datadogCi.gitMetadata.uploadGitCommitHash("{Datadog_API_Key}", "<SITE>");

const app = new cdk.App();
new ExampleStack(app, "ExampleStack", {});

app.synth();
```

</details>
<details>
  <summary>datadog-cdk version NOT satisfied</summary>

Change your initialization function as follows (in this case, `gitHash` value is passed to the CDK):

```python
async function main() {
  // Make sure to add @datadog/datadog-ci via your package manager
  const datadogCi = require("@datadog/datadog-ci");
  const [, gitHash] = await datadogCi.gitMetadata.uploadGitCommitHash("{Datadog_API_Key}", "<SITE>");

  const app = new cdk.App();
  // Pass in the hash to the ExampleStack constructor
  new ExampleStack(app, "ExampleStack", {}, gitHash);
}
```

Ensure you call this function to initialize your stack.

In your stack constructor, change to add an optional `gitHash` parameter, and call `addGitCommitMetadata()`:

```python
export class ExampleStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps, gitHash?: string) {
    ...
    ...
    datadogLambda.addGitCommitMetadata([<YOUR_FUNCTIONS>], gitHash)
  }
}
```

</details>

### Configuration

To further configure your DatadogLambda construct for Lambda, use the following custom parameters:

*Note*: The descriptions use the npm package parameters, but they also apply to PyPI and Go package parameters.

| npm package parameter        | PyPI package parameter          | Description                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `addLayers`                  | `add_layers`                    | Whether to add the runtime Lambda Layers or expect the user to bring their own. Defaults to `true`. When `true`, the Lambda Library version variables are also required. When `false`, you must include the Datadog Lambda library in your functions' deployment packages.                                                                                                                                                     |
| `pythonLayerVersion`         | `python_layer_version`          | Version of the Python Lambda layer to install, such as `83`. Required if you are deploying at least one Lambda function written in Python and `addLayers` is `true`. Find the latest version number [here](https://github.com/DataDog/datadog-lambda-python/releases).                                                                                                                                                                                                                 |
| `nodeLayerVersion`           | `node_layer_version`            | Version of the Node.js Lambda layer to install, such as `100`. Required if you are deploying at least one Lambda function written in Node.js and `addLayers` is `true`. Find the latest version number from [here](https://github.com/DataDog/datadog-lambda-js/releases).                                                                                                                                                                                                         |
| `javaLayerVersion`           | `java_layer_version`            | Version of the Java layer to install, such as `8`. Required if you are deploying at least one Lambda function written in Java and `addLayers` is `true`. Find the latest version number in the [Serverless Java installation documentation](https://docs.datadoghq.com/serverless/installation/java/?tab=awscdk). **Note**: `extensionLayerVersion >= 25` and `javaLayerVersion >= 5` are required for the DatadogLambda construct to instrument your Java functions properly.                  |
| `dotnetLayerVersion`         | `dotnet_layer_version`          | Version of the .NET layer to install, such as `13`. Required if you are deploying at least one Lambda function written in .NET and `addLayers` is `true`. Find the latest version number from [here](https://github.com/DataDog/dd-trace-dotnet-aws-lambda-layer/releases).                                                                                                                                                                                                                      |
| `extensionLayerVersion`      | `extension_layer_version`       | Version of the Datadog Lambda Extension layer to install, such as 5. When `extensionLayerVersion` is set, `apiKey` (or if encrypted, `apiKMSKey` or `apiKeySecretArn`) needs to be set as well. When enabled, lambda function log groups will not be subscribed by the forwarder. Learn more about the Lambda extension [here](https://docs.datadoghq.com/serverless/datadog_lambda_library/extension/). **Note**: If this parameter is set, it adds a layer even if `addLayers` is set to `false`. |
| `forwarderArn`               | `forwarder_arn`                 | When set, the plugin will automatically subscribe the Datadog Forwarder to the functions' log groups. Do not set `forwarderArn` when `extensionLayerVersion` is set.                                                                                                                                                                                                                                                           |
| `createForwarderPermissions` | `createForwarderPermissions`    | When set to `true`, creates a Lambda permission on the the Datadog Forwarder per log group. Since the Datadog Forwarder has permissions configured by default, this is unnecessary in most use cases.                                                                                                                                                                                                                          |
| `flushMetricsToLogs`         | `flush_metrics_to_logs`         | Send custom metrics using CloudWatch logs with the Datadog Forwarder Lambda function (recommended). Defaults to `true` . If you disable this parameter, it's required to set `apiKey` (or if encrypted, `apiKMSKey` or `apiKeySecretArn`).                                                                                                                                                                                     |
| `site`                       | `site`                          | Set which Datadog site to send data. This is only used when `flushMetricsToLogs` is `false` or `extensionLayerVersion` is set. Possible values are `datadoghq.com`, `datadoghq.eu`, `us3.datadoghq.com`, `us5.datadoghq.com`, `ap1.datadoghq.com`, and `ddog-gov.com`. The default is `datadoghq.com`.                                                                                                                         |
| `apiKey`                     | `api_key`                       | Datadog API Key, only needed when `flushMetricsToLogs` is `false` or `extensionLayerVersion` is set. For more information about getting a Datadog API key, see the [API key documentation](https://docs.datadoghq.com/account_management/api-app-keys/#api-keys).                                                                                                                                                                                                                                 |
| `apiKeySecretArn`            | `api_key_secret_arn`            | The ARN of the secret storing the Datadog API key in AWS Secrets Manager. Use this parameter in place of `apiKey` when `flushMetricsToLogs` is `false` or `extensionLayer` is set. Remember to add the `secretsmanager:GetSecretValue` permission to the Lambda execution role.                                                                                                                                                |
| `apiKeySecret`               | `api_key_secret`                | An [AWS CDK ISecret](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_secretsmanager.ISecret.html) representing a secret storing the Datadog API key in AWS Secrets Manager. Use this parameter in place of `apiKeySecretArn` to automatically grant your Lambda execution roles read access to the given secret. [See here](#automatically-grant-aws-secret-read-access-to-lambda-execution-role) for an example. **Only available in datadog-cdk-constructs-v2**.                                      |
| `apiKmsKey`                  | `api_kms_key`                   | Datadog API Key encrypted using KMS. Use this parameter in place of `apiKey` when `flushMetricsToLogs` is `false` or `extensionLayerVersion` is set, and you are using KMS encryption.                                                                                                                                                                                                                                         |
| `enableDatadogTracing`       | `enable_datadog_tracing`        | Enable Datadog tracing on your Lambda functions. Defaults to `true`.                                                                                                                                                                                                                                                                                                                                                           |
| `enableMergeXrayTraces`      | `enable_merge_xray_traces`      | Enable merging X-Ray traces on your Lambda functions. Defaults to `false`.                                                                                                                                                                                                                                                                                                                                                     |
| `enableDatadogLogs`          | `enable_datadog_logs`           | Send Lambda function logs to Datadog via the Datadog Lambda Extension. Defaults to `true`. Note: This setting has no effect on logs sent via the Datadog Forwarder.                                                                                                                                                                                                                                                            |
| `sourceCodeIntegration`      | `source_code_integration`       | Enable Datadog Source Code Integration, connecting your telemetry with application code in your Git repositories. This requires the Datadog Github integration to work, otherwise please follow the [alternative method](#alternative-methods-to-enable-source-code-integration). Learn more [here](https://docs.datadoghq.com/integrations/guide/source-code-integration/). Defaults to `true`.                               |
| `injectLogContext`           | `inject_log_context`            | When set, the Lambda layer will automatically patch console.log with Datadog's tracing ids. Defaults to `true`.                                                                                                                                                                                                                                                                                                                |
| `logLevel`                   | `log_level`                     | When set to `debug`, the Datadog Lambda Library and Extension will log additional information to help troubleshoot issues.                                                                                                                                                                                                                                                                                                     |
| `env`                        | `env`                           | When set along with `extensionLayerVersion`, a `DD_ENV` environment variable is added to all Lambda functions with the provided value. When set along with `forwarderArn`, an `env` tag is added to all Lambda functions with the provided value.                                                                                                                                                                              |
| `service`                    | `service`                       | When set along with `extensionLayerVersion`, a `DD_SERVICE` environment variable is added to all Lambda functions with the provided value. When set along with `forwarderArn`, a `service` tag is added to all Lambda functions with the provided value.                                                                                                                                                                       |
| `version`                    | `version`                       | When set along with `extensionLayerVersion`, a `DD_VERSION` environment variable is added to all Lambda functions with the provided value. When set along with `forwarderArn`, a `version` tag is added to all Lambda functions with the provided value.                                                                                                                                                                       |
| `tags`                       | `tags`                          | A comma separated list of key:value pairs as a single string. When set along with `extensionLayerVersion`, a `DD_TAGS` environment variable is added to all Lambda functions with the provided value. When set along with `forwarderArn`, the cdk parses the string and sets each key:value pair as a tag to all Lambda functions.                                                                                             |
| `enableColdStartTracing`     | `enable_cold_start_tracing`     | Set to `false` to disable Cold Start Tracing. Used in Node.js and Python. Defaults to `true`.                                                                                                                                                                                                                                                                                                                                  |
| `coldStartTraceMinDuration`  | `min_cold_start_trace_duration` | Sets the minimum duration (in milliseconds) for a module load event to be traced via Cold Start Tracing. Number. Defaults to `3`.                                                                                                                                                                                                                                                                                              |
| `coldStartTraceSkipLibs`     | `cold_start_trace_skip_libs`    | Optionally skip creating Cold Start Spans for a comma-separated list of libraries. Useful to limit depth or skip known libraries. Default depends on runtime.                                                                                                                                                                                                                                                                  |
| `enableProfiling`            | `enable_profiling`              | Enable the Datadog Continuous Profiler with `true`. Supported in Beta for Node.js and Python. Defaults to `false`.                                                                                                                                                                                                                                                                                                             |
| `encodeAuthorizerContext`    | `encode_authorizer_context`     | When set to `true` for Lambda authorizers, the tracing context will be encoded into the response for propagation. Supported for Node.js and Python. Defaults to `true`.                                                                                                                                                                                                                                                        |
| `decodeAuthorizerContext`    | `decode_authorizer_context`     | When set to `true` for Lambdas that are authorized via Lambda authorizers, it will parse and use the encoded tracing context (if found). Supported for Node.js and Python. Defaults to `true`.                                                                                                                                                                                                                                 |
| `apmFlushDeadline`           | `apm_flush_deadline`            | Used to determine when to submit spans before a timeout occurs, in milliseconds. When the remaining time in an AWS Lambda invocation is less than the value set, the tracer attempts to submit the current active spans and all finished spans. Supported for Node.js and Python. Defaults to `100` milliseconds.                                                                                                              |
| `redirectHandler`            | `redirect_handler`              | When set to `false`, skip redirecting handler to the Datadog Lambda Library's handler. Useful when only instrumenting with Datadog Lambda Extension. Defaults to `true`.                                                                                                                                                                                                                                                       |

**Note**: Using the parameters above may override corresponding function level `DD_XXX` environment variables.

#### Tracing

Enable X-Ray Tracing on your Lambda functions. For more information, see [CDK documentation](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Tracing.html).

```python
import * as lambda from "aws-cdk-lib/aws-lambda";

const lambda_function = new lambda.Function(this, "HelloHandler", {
  runtime: lambda.Runtime.NODEJS_14_X,
  code: lambda.Code.fromAsset("lambda"),
  handler: "hello.handler",
  tracing: lambda.Tracing.ACTIVE,
});
```

#### Nested Stacks

Add the Datadog CDK Construct to each stack you wish to instrument with Datadog. In the example below, we initialize the Datadog CDK Construct and call `addLambdaFunctions()` in both the `RootStack` and `NestedStack`.

```python
import { DatadogLambda } from "datadog-cdk-constructs-v2";
import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

class RootStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    new NestedStack(this, "NestedStack");

    const datadogLambda = new DatadogLambda(this, "DatadogLambda", {
      nodeLayerVersion: <LAYER_VERSION>,
      pythonLayerVersion: <LAYER_VERSION>,
      javaLayerVersion: <LAYER_VERSION>,
      dotnetLayerVersion: <LAYER-VERSION>,
      addLayers: <BOOLEAN>,
      forwarderArn: "<FORWARDER_ARN>",
      flushMetricsToLogs: <BOOLEAN>,
      site: "<SITE>",
      apiKey: "{Datadog_API_Key}",
      apiKeySecretArn: "{Secret_ARN_Datadog_API_Key}",
      apiKmsKey: "{Encrypted_Datadog_API_Key}",
      enableDatadogTracing: <BOOLEAN>,
      enableMergeXrayTraces: <BOOLEAN>,
      enableDatadogLogs: <BOOLEAN>,
      injectLogContext: <BOOLEAN>
    });
    datadogLambda.addLambdaFunctions([<LAMBDA_FUNCTIONS>]);

  }
}

class NestedStack extends cdk.NestedStack {
  constructor(scope: Construct, id: string, props?: cdk.NestedStackProps) {
    super(scope, id, props);

    const datadogLambda = new DatadogLambda(this, "DatadogLambda", {
      nodeLayerVersion: <LAYER_VERSION>,
      pythonLayerVersion: <LAYER_VERSION>,
      javaLayerVersion: <LAYER_VERSION>,
      dotnetLayerVersion: <LAYER-VERSION>,
      addLayers: <BOOLEAN>,
      forwarderArn: "<FORWARDER_ARN>",
      flushMetricsToLogs: <BOOLEAN>,
      site: "<SITE>",
      apiKey: "{Datadog_API_Key}",
      apiKeySecretArn: "{Secret_ARN_Datadog_API_Key}",
      apiKmsKey: "{Encrypted_Datadog_API_Key}",
      enableDatadogTracing: <BOOLEAN>,
      enableMergeXrayTraces: <BOOLEAN>,
      enableDatadogLogs: <BOOLEAN>,
      injectLogContext: <BOOLEAN>
    });
    datadogLambda.addLambdaFunctions([<LAMBDA_FUNCTIONS>]);

  }
}
```

#### Tags

Add tags to your constructs. We recommend setting an `env` and `service` tag to tie Datadog telemetry together. For more information see [official AWS documentation](https://docs.aws.amazon.com/cdk/latest/guide/tagging.html) and [CDK documentation](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Tags.html).

### Automatically grant AWS secret read access to Lambda execution role

**Only available in datadog-cdk-constructs-v2**

To automatically grant your Lambda execution roles read access to a given secret, pass in `apiKeySecret` in place of `apiKeySecretArn` when initializing the DatadogLambda construct.

```python
const { Secret } = require('aws-cdk-lib/aws-secretsmanager');

const secret = Secret.fromSecretPartialArn(this, 'DatadogApiKeySecret', 'arn:aws:secretsmanager:us-west-1:123:secret:DATADOG_API_KEY');

const datadogLambda = new DatadogLambda(this, 'DatadogLambda', {
  ...
  apiKeySecret: secret
  ...
});
```

When `addLambdaFunctions` is called, the Datadog CDK construct grants your Lambda execution roles read access to the given AWS secret. This is done through the [AWS ISecret's grantRead function](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_secretsmanager.ISecret.html#grantwbrreadgrantee-versionstages).

### How it works

The DatadogLambda construct takes in a list of lambda functions and installs the Datadog Lambda Library by attaching the Lambda Layers for [.NET](https://docs.datadoghq.com/serverless/aws_lambda/installation/dotnet), [Java](https://docs.datadoghq.com/serverless/installation/java/?tab=awscdk), [Node.js](https://github.com/DataDog/datadog-lambda-layer-js), and [Python](https://github.com/DataDog/datadog-lambda-layer-python) to your functions. It redirects to a replacement handler that initializes the Lambda Library without any required code changes. Additional configurations added to the Datadog CDK construct will also translate into their respective environment variables under each lambda function (if applicable / required).

While Lambda function based log groups are handled by the `addLambdaFunctions` method automatically, the construct has an additional function `addForwarderToNonLambdaLogGroups` which subscribes the forwarder to any additional log groups of your choosing.

## Step Functions

Only AWS CDK v2 is supported.

### Usage

#### TypeScript

Example stack: [step-functions-typescript-stack](https://github.com/DataDog/datadog-cdk-constructs/tree/main/examples/step-functions-typescript-stack)

##### Basic setup

```
import * as sfn from "aws-cdk-lib/aws-stepfunctions";
import { DatadogStepFunctions} from "datadog-cdk-constructs-v2";

const stateMachine = new sfn.StateMachine(...);
const datadogSfn = new DatadogStepFunctions(this, "DatadogSfn", {
  env: "<ENV>", // e.g. "dev"
  service: "<SERVICE>", // e.g. "my-cdk-service"
  version: "<VERSION>", // e.g. "1.0.0"
  forwarderArn: "<FORWARDER_ARN>", // e.g. "arn:test:forwarder:sa-east-1:12345678:1"
  tags: <TAGS>, // optional, e.g. "custom-tag-1:tag-value-1,custom-tag-2:tag-value-2"
});
datadogSfn.addStateMachines([stateMachine]);
```

##### Merging traces

To merge the Step Function's traces with downstream Lambda function or Step function's traces, modify the Lambda task payload or Step Function task input:

```
import * as tasks from "aws-cdk-lib/aws-stepfunctions-tasks";
import * as sfn from "aws-cdk-lib/aws-stepfunctions";
import { DatadogStepFunctions, DatadogLambda } from "datadog-cdk-constructs-v2";

const lambdaFunction = ...;
const lambdaTask = new tasks.LambdaInvoke(this, "MyLambdaTask", {
  lambdaFunction: lambdaFunction,
  payload: sfn.TaskInput.fromObject(
    DatadogStepFunctions.buildLambdaPayloadToMergeTraces(
      { "custom-key": "custom-value" }
    )
  ),
});

const childStateMachine = new sfn.StateMachine(...);
const invokeChildStateMachineTask = new tasks.StepFunctionsStartExecution(this, "InvokeChildStateMachineTask", {
  stateMachine: childStateMachine,
  input: sfn.TaskInput.fromObject(
    DatadogStepFunctions.buildStepFunctionTaskInputToMergeTraces({ "custom-key": "custom-value" }),
  ),
});

const stateMachine = new sfn.StateMachine(this, "CdkTypeScriptTestStateMachine", {
  definitionBody: sfn.DefinitionBody.fromChainable(lambdaTask.next(invokeChildStateMachineTask)),
});

const datadogLambda = ...;
datadogLambda.addLambdaFunctions([lambdaFunction]);

const datadogSfn = ...;
datadogSfn.addStateMachines([childStateMachine, stateMachine]);
```

#### Python

Example stack: [step-functions-python-stack](https://github.com/DataDog/datadog-cdk-constructs/tree/main/examples/step-functions-python-stack)

##### Basic setup

```
from aws_cdk import (
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)
from datadog_cdk_constructs_v2 import DatadogStepFunctions, DatadogLambda

state_machine = sfn.StateMachine(...)
datadog_sfn = DatadogStepFunctions(
    self,
    "DatadogSfn",
    env="<ENV>", # e.g. "dev"
    service="<SERVICE>", # e.g. "my-cdk-service"
    version="<VERSION>", # e.g. "1.0.0"
    forwarderArn="<FORWARDER_ARN>", # e.g. "arn:test:forwarder:sa-east-1:12345678:1"
    tags=<TAGS>, # optional, e.g. "custom-tag-1:tag-value-1,custom-tag-2:tag-value-2"
)
datadog_sfn.add_state_machines([child_state_machine, parent_state_machine])
```

##### Merging traces

To merge the Step Function's traces with downstream Lambda function or Step function's traces, modify the Lambda task payload or Step Function task input:

```
from aws_cdk import (
    aws_lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)
from datadog_cdk_constructs_v2 import DatadogStepFunctions, DatadogLambda

lambda_function = aws_lambda.Function(...)
lambda_task = tasks.LambdaInvoke(
    self,
    "MyLambdaTask",
    lambda_function=lambda_function,
    payload=sfn.TaskInput.from_object(
        DatadogStepFunctions.build_lambda_payload_to_merge_traces(
            {"custom-key": "custom-value"}
        )
    ),
)

child_state_machine = sfn.StateMachine(...)
invoke_child_state_machine_task = tasks.StepFunctionsStartExecution(
    self,
    "InvokeChildStateMachineTask",
    state_machine=child_state_machine,
    input=sfn.TaskInput.from_object(
        DatadogStepFunctions.build_step_function_task_input_to_merge_traces(
            {"custom-key": "custom-value"}
        )
    ),
)

state_machine = sfn.StateMachine(
    self,
    "CdkPythonTestStateMachine",
    definition_body=sfn.DefinitionBody.from_chainable(
        lambda_task.next(invoke_child_state_machine_task)
    ),
)

datadog_lambda = DatadogLambda(...)
datadog_lambda.add_lambda_functions([lambda_function])

datadog_sfn = DatadogStepFunctions(...)
datadog_sfn.add_state_machines([child_state_machine, state_machine])
```

#### Go

Example stack: [step-functions-go-stack](https://github.com/DataDog/datadog-cdk-constructs/tree/main/examples/step-functions-go-stack)

##### Basic setup

```
import (
	"github.com/DataDog/datadog-cdk-constructs-go/ddcdkconstruct"
	"github.com/aws/aws-cdk-go/awscdk/v2"
	sfn "github.com/aws/aws-cdk-go/awscdk/v2/awsstepfunctions"
)

stack := awscdk.NewStack(...)
stateMachine := sfn.NewStateMachine(...)
datadogSfn := ddcdkconstruct.NewDatadogStepFunctions(
  stack,
  jsii.String("DatadogSfn"),
  &ddcdkconstruct.DatadogStepFunctionsProps{
    Env:            jsii.String("<ENV>"), // e.g. "dev"
    Service:        jsii.String("<SERVICE>), // e.g. "my-cdk-service"
    Version:        jsii.String("<VERSION>"), // e.g. "1.0.0"
    ForwarderArn:   jsii.String("<FORWARDER_ARN>"), // e.g. "arn:test:forwarder:sa-east-1:12345678:1"
    Tags:           jsii.String("<TAGS>"), // optional, e.g. "custom-tag-1:tag-value-1,custom-tag-2:tag-value-2"
  }
)
datadogSfn.AddStateMachines(&[]sfn.StateMachine{stateMachine}, nil)
```

##### Merging traces

To merge the Step Function's traces with downstream Lambda function or Step function's traces, modify the Lambda task payload or Step Function task input:

```
import (
	"github.com/DataDog/datadog-cdk-constructs-go/ddcdkconstruct"
	"github.com/aws/aws-cdk-go/awscdk/v2/awslambda"
	sfn "github.com/aws/aws-cdk-go/awscdk/v2/awsstepfunctions"
	sfntasks "github.com/aws/aws-cdk-go/awscdk/v2/awsstepfunctionstasks"
	"github.com/aws/jsii-runtime-go"
)

lambdaFunction := awslambda.NewFunction(...)
lambdaPayload := ddcdkconstruct.DatadogStepFunctions_BuildLambdaPayloadToMergeTraces(&map[string]interface{}{
  "custom-key": "custom-value",
})
lambdaTask := sfntasks.NewLambdaInvoke(stack, jsii.String("MyLambdaTask"), &sfntasks.LambdaInvokeProps{
  LambdaFunction: lambdaFunction,
  Payload: sfn.TaskInput_FromObject(lambdaPayload),
})

childStateMachine := sfn.NewStateMachine(...)
stateMachineTaskInput := ddcdkconstruct.DatadogStepFunctions_BuildStepFunctionTaskInputToMergeTraces(
  &map[string]interface{}{
    "custom-key": "custom-value",
  }
)
invokeChildStateMachineTask := sfntasks.NewStepFunctionsStartExecution(
  stack,
  jsii.String("InvokeChildStateMachineTask"),
  &sfntasks.StepFunctionsStartExecutionProps{
    StateMachine: childStateMachine,
    Input: sfn.TaskInput_FromObject(stateMachineTaskInput),
  }
)
stateMachine := sfn.NewStateMachine(stack, jsii.String("CdkGoTestStateMachine"), &sfn.StateMachineProps{
  DefinitionBody: sfn.DefinitionBody_FromChainable(lambdaTask.Next(invokeChildStateMachineTask)),
})

datadogLambda := ...
datadogLambda.AddLambdaFunctions(&[]interface{}{lambdaFunction}, nil)

datadogSfn := ...
datadogSfn.AddStateMachines(&[]sfn.StateMachine{childStateMachine, stateMachine}, nil)
```

### Configuration

Parameters for creating the `DatadogStepFunctions` construct:

| npm package parameter | PyPI package parameter | Go package parameter | Description                                                                                                    |
| --------------------- | ---------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------- |
| `env`                 | `env`                  | `Env`                | The `env` tag to be added to the state machine.                                                                |
| `service`             | `service`              | `Service`            | The `service` tag to be added to the state machine.                                                            |
| `version`             | `version`              | `Version`            | The `version` tag to be added to the state machine.                                                            |
| `forwarderArn`        | `forwarder_arn`        | `ForwarderArn`       | ARN or Datadog Forwarder, which will subscribe to the state machine's log group.                               |
| `tags`                | `tags`                 | `Tags`               | A comma separated list of key:value pairs as a single string, which will be added to the state machine's tags. |

### How it works

The `DatadogStepFunctions` construct takes in a list of state machines and for each of them:

1. Set up logging, including:

   1. Set log level to ALL
   2. Set includeExecutionData to true
   3. Create and set destination log group (if not set already)
   4. Add permissions to the state machine role to log to CloudWatch Logs
2. Subscribe Datadog Forwarder to the state machine's log group
3. Set tags, including:

   1. `env`
   2. `service`
   3. `version`
   4. `DD_TRACE_ENABLED`: `true`. This enables tracing.

      1. To disable tracing, set it to `false` from AWS Management Console after the stack is deployed.
      2. If you wish to disable tracing using CDK, please open an issue so we can support it.
   5. `dd_cdk_construct` version tag
   6. custom tags passed as the `tags` paramater to `DatadogStepFunctions` construct

To merge the Step Function's traces with downstream Lambda function or Step function's traces, the construct adds `$$.Execution`, `$$.State` and `$$.StateMachine` fields into the Step Function task input or Lambda task payload.

### Troubleshooting

#### Log group already exists

If `cdk deploy` fails with an error like:

> Resource of type 'AWS::Logs::LogGroup' with identifier '{"/properties/LogGroupName":"/aws/vendedlogs/states/CdkStepFunctionsTypeScriptStack1-CdkTypeScriptTestChildStateMachine-Logs-dev"}' already exists.

You have two options:

1. Delete the log group if you no longer need the logs in it. You may do so from AWS Management Console, at CloudWatch -> Logs -> Log groups.
2. Update the state machine definition if you wish to use the existing log group:

```
import * as logs from 'aws-cdk-lib/aws-logs';

const logGroupName = "/aws/vendedlogs/states/xxx";
const logGroup = logs.LogGroup.fromLogGroupName(stack, 'StateMachineLogGroup', logGroupName);

const stateMachine = new sfn.StateMachine(stack, 'MyStateMachine', {
  logs: {
    destination: logGroup,
  },
  ...
});
```

## Resources to learn about CDK

* If you are new to AWS CDK then check out this [workshop](https://cdkworkshop.com/15-prerequisites.html).
* [CDK TypeScript Workshop](https://cdkworkshop.com/20-typescript.html)
* [Video Introducing CDK by AWS with Demo](https://youtu.be/ZWCvNFUN-sU)
* [CDK Concepts](https://youtu.be/9As_ZIjUGmY)

## Using Projen

The Datadog CDK Construct Libraries use Projen to maintain project configuration files such as the `package.json`, `.gitignore`, `.npmignore`, etc. Most of the configuration files will be protected by Projen via read-only permissions. In order to change these files, edit the `.projenrc.js` file, then run `npx projen` to synthesize the new changes. Check out [Projen](https://github.com/projen/projen) for more details.

## Migrating from v2-1.x.x to v2-2.x.x

In February 2025, Datadog released a major version update from `1.x.x` to `2.x.x`. The required changes to migrate to the new version are as follows:

1. Rename the classes for instrumenting Lambda functions:

   1. `Datadog` -> `DatadogLambda`
   2. `DatadogProps` -> `DatadogLambdaProps`
      For examples, see the [Usage](#usage) section of this page and [examples/](https://github.com/DataDog/datadog-cdk-constructs/tree/main/examples) folder of the GitHub repository.
2. Upgrade Node.js version to `18.18.0` or above.

## Opening Issues

If you encounter a bug with this package, we want to hear about it. Before opening a new issue, search the existing issues to avoid duplicates.

When opening an issue, include the Datadog CDK Construct version, Node version, and stack trace if available. In addition, include the steps to reproduce when appropriate.

You can also open an issue for a feature request.

## Contributing

If you find an issue with this package and have a fix, please feel free to open a pull request following the [procedures](https://github.com/DataDog/datadog-cdk-constructs/blob/main/CONTRIBUTING.md).

## Testing

If you contribute to this package you can run the tests using `yarn test`. This package also includes a sample application for manual testing:

1. Open a seperate terminal.
2. Run `yarn watch`, this will ensure the Typescript files in the `src` directory are compiled to Javascript in the `lib` directory.
3. Navigate to `src/sample`, here you can edit `index.ts` to test your contributions manually.
4. At the root directory, run `npx cdk --app lib/sample/index.js <CDK Command>`, replacing `<CDK Command>` with common CDK commands like `synth`, `diff`, or `deploy`.

* Note, if you receive "... is not authorized to perform: ..." you may also need to authorize the commands with your AWS credentials.

### Debug Logs

To display the debug logs for this library for Lambda, set the `DD_CONSTRUCT_DEBUG_LOGS` env var to `true` when running `cdk synth` (use `--quiet` to suppress generated template output).

Example:
*Ensure you are at the root directory*

```
DD_CONSTRUCT_DEBUG_LOGS=true npx cdk --app lib/sample/index.js synth --quiet
```

## Community

For product feedback and questions, join the `#serverless` channel in the [Datadog community on Slack](https://chat.datadoghq.com/).

## License

Unless explicitly stated otherwise all files in this repository are licensed under the Apache License Version 2.0.

This product includes software developed at Datadog (https://www.datadoghq.com/). Copyright 2021 Datadog, Inc.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import constructs as _constructs_77d1e7e8


class DatadogLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="datadog-cdk-constructs-v2.DatadogLambda",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        add_layers: typing.Optional[builtins.bool] = None,
        api_key: typing.Optional[builtins.str] = None,
        api_key_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        api_key_secret_arn: typing.Optional[builtins.str] = None,
        api_kms_key: typing.Optional[builtins.str] = None,
        apm_flush_deadline: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
        capture_lambda_payload: typing.Optional[builtins.bool] = None,
        cold_start_trace_skip_libs: typing.Optional[builtins.str] = None,
        create_forwarder_permissions: typing.Optional[builtins.bool] = None,
        decode_authorizer_context: typing.Optional[builtins.bool] = None,
        dotnet_layer_version: typing.Optional[jsii.Number] = None,
        enable_cold_start_tracing: typing.Optional[builtins.bool] = None,
        enable_datadog_asm: typing.Optional[builtins.bool] = None,
        enable_datadog_logs: typing.Optional[builtins.bool] = None,
        enable_datadog_tracing: typing.Optional[builtins.bool] = None,
        enable_merge_xray_traces: typing.Optional[builtins.bool] = None,
        enable_profiling: typing.Optional[builtins.bool] = None,
        encode_authorizer_context: typing.Optional[builtins.bool] = None,
        env: typing.Optional[builtins.str] = None,
        extension_layer_version: typing.Optional[jsii.Number] = None,
        flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
        forwarder_arn: typing.Optional[builtins.str] = None,
        grant_secret_read_access: typing.Optional[builtins.bool] = None,
        inject_log_context: typing.Optional[builtins.bool] = None,
        java_layer_version: typing.Optional[jsii.Number] = None,
        log_level: typing.Optional[builtins.str] = None,
        min_cold_start_trace_duration: typing.Optional[jsii.Number] = None,
        node_layer_version: typing.Optional[jsii.Number] = None,
        python_layer_version: typing.Optional[jsii.Number] = None,
        redirect_handler: typing.Optional[builtins.bool] = None,
        service: typing.Optional[builtins.str] = None,
        site: typing.Optional[builtins.str] = None,
        source_code_integration: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[builtins.str] = None,
        use_layers_from_account: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param add_layers: 
        :param api_key: 
        :param api_key_secret: 
        :param api_key_secret_arn: 
        :param api_kms_key: 
        :param apm_flush_deadline: 
        :param capture_lambda_payload: 
        :param cold_start_trace_skip_libs: 
        :param create_forwarder_permissions: 
        :param decode_authorizer_context: 
        :param dotnet_layer_version: 
        :param enable_cold_start_tracing: 
        :param enable_datadog_asm: 
        :param enable_datadog_logs: 
        :param enable_datadog_tracing: 
        :param enable_merge_xray_traces: 
        :param enable_profiling: 
        :param encode_authorizer_context: 
        :param env: 
        :param extension_layer_version: 
        :param flush_metrics_to_logs: 
        :param forwarder_arn: 
        :param grant_secret_read_access: 
        :param inject_log_context: 
        :param java_layer_version: 
        :param log_level: 
        :param min_cold_start_trace_duration: 
        :param node_layer_version: 
        :param python_layer_version: 
        :param redirect_handler: 
        :param service: 
        :param site: 
        :param source_code_integration: 
        :param tags: 
        :param use_layers_from_account: 
        :param version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2984f96d56b35b6bf9f462eeb539cb66d7814bc0c2c05efa693a19e965978d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DatadogLambdaProps(
            add_layers=add_layers,
            api_key=api_key,
            api_key_secret=api_key_secret,
            api_key_secret_arn=api_key_secret_arn,
            api_kms_key=api_kms_key,
            apm_flush_deadline=apm_flush_deadline,
            capture_lambda_payload=capture_lambda_payload,
            cold_start_trace_skip_libs=cold_start_trace_skip_libs,
            create_forwarder_permissions=create_forwarder_permissions,
            decode_authorizer_context=decode_authorizer_context,
            dotnet_layer_version=dotnet_layer_version,
            enable_cold_start_tracing=enable_cold_start_tracing,
            enable_datadog_asm=enable_datadog_asm,
            enable_datadog_logs=enable_datadog_logs,
            enable_datadog_tracing=enable_datadog_tracing,
            enable_merge_xray_traces=enable_merge_xray_traces,
            enable_profiling=enable_profiling,
            encode_authorizer_context=encode_authorizer_context,
            env=env,
            extension_layer_version=extension_layer_version,
            flush_metrics_to_logs=flush_metrics_to_logs,
            forwarder_arn=forwarder_arn,
            grant_secret_read_access=grant_secret_read_access,
            inject_log_context=inject_log_context,
            java_layer_version=java_layer_version,
            log_level=log_level,
            min_cold_start_trace_duration=min_cold_start_trace_duration,
            node_layer_version=node_layer_version,
            python_layer_version=python_layer_version,
            redirect_handler=redirect_handler,
            service=service,
            site=site,
            source_code_integration=source_code_integration,
            tags=tags,
            use_layers_from_account=use_layers_from_account,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addForwarderToNonLambdaLogGroups")
    def add_forwarder_to_non_lambda_log_groups(
        self,
        log_groups: typing.Sequence[_aws_cdk_aws_logs_ceddda9d.ILogGroup],
    ) -> None:
        '''
        :param log_groups: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d077b7f7df346dab533a634af3f0901767a9f2b837615c493fef851e2caeaa37)
            check_type(argname="argument log_groups", value=log_groups, expected_type=type_hints["log_groups"])
        return typing.cast(None, jsii.invoke(self, "addForwarderToNonLambdaLogGroups", [log_groups]))

    @jsii.member(jsii_name="addGitCommitMetadata")
    def add_git_commit_metadata(
        self,
        lambda_functions: typing.Sequence[typing.Union[_aws_cdk_aws_lambda_ceddda9d.Function, _aws_cdk_aws_lambda_ceddda9d.SingletonFunction]],
        git_commit_sha: typing.Optional[builtins.str] = None,
        git_repo_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lambda_functions: -
        :param git_commit_sha: -
        :param git_repo_url: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea846263375949d2a4455edf17977f56d13f60fa2f6f2d50679231a2ee9e68e)
            check_type(argname="argument lambda_functions", value=lambda_functions, expected_type=type_hints["lambda_functions"])
            check_type(argname="argument git_commit_sha", value=git_commit_sha, expected_type=type_hints["git_commit_sha"])
            check_type(argname="argument git_repo_url", value=git_repo_url, expected_type=type_hints["git_repo_url"])
        return typing.cast(None, jsii.invoke(self, "addGitCommitMetadata", [lambda_functions, git_commit_sha, git_repo_url]))

    @jsii.member(jsii_name="addLambdaFunctions")
    def add_lambda_functions(
        self,
        lambda_functions: typing.Sequence[typing.Union[_aws_cdk_aws_lambda_ceddda9d.Function, _aws_cdk_aws_lambda_ceddda9d.SingletonFunction]],
        construct: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    ) -> None:
        '''
        :param lambda_functions: -
        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9f739b7a469f9944fd92418630c6ace0920581d7aba71e8bb4836e1878bb6c)
            check_type(argname="argument lambda_functions", value=lambda_functions, expected_type=type_hints["lambda_functions"])
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(None, jsii.invoke(self, "addLambdaFunctions", [lambda_functions, construct]))

    @jsii.member(jsii_name="overrideGitMetadata")
    def override_git_metadata(
        self,
        git_commit_sha: builtins.str,
        git_repo_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param git_commit_sha: -
        :param git_repo_url: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add190e793382279b2292e564b6b7af77c9e86799063643d34222561b86f6bcd)
            check_type(argname="argument git_commit_sha", value=git_commit_sha, expected_type=type_hints["git_commit_sha"])
            check_type(argname="argument git_repo_url", value=git_repo_url, expected_type=type_hints["git_repo_url"])
        return typing.cast(None, jsii.invoke(self, "overrideGitMetadata", [git_commit_sha, git_repo_url]))

    @builtins.property
    @jsii.member(jsii_name="lambdas")
    def lambdas(
        self,
    ) -> typing.List[typing.Union[_aws_cdk_aws_lambda_ceddda9d.Function, _aws_cdk_aws_lambda_ceddda9d.SingletonFunction]]:
        return typing.cast(typing.List[typing.Union[_aws_cdk_aws_lambda_ceddda9d.Function, _aws_cdk_aws_lambda_ceddda9d.SingletonFunction]], jsii.get(self, "lambdas"))

    @lambdas.setter
    def lambdas(
        self,
        value: typing.List[typing.Union[_aws_cdk_aws_lambda_ceddda9d.Function, _aws_cdk_aws_lambda_ceddda9d.SingletonFunction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637733c25a7c2850eaee52097e2193a573cd89b62a7c3996ea0fda7addda066c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "DatadogLambdaProps":
        return typing.cast("DatadogLambdaProps", jsii.get(self, "props"))

    @props.setter
    def props(self, value: "DatadogLambdaProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cacc2a125e366ff9b1144af9ca07a68614e32ac99686c20a48c623921b3359e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> _constructs_77d1e7e8.Construct:
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: _constructs_77d1e7e8.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd01617eb2e87ed512be49dc83a00ad8014edd30800c640e958188cbcb58426f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transport")
    def transport(self) -> "Transport":
        return typing.cast("Transport", jsii.get(self, "transport"))

    @transport.setter
    def transport(self, value: "Transport") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01077f52f36828b6127966c542bcbf9e86506f40b406b02d331a1f5f35827b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gitCommitShaOverride")
    def git_commit_sha_override(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitCommitShaOverride"))

    @git_commit_sha_override.setter
    def git_commit_sha_override(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__213e6389c94903631c6747e04649248f0784d5717f40ad071d3c71802a5c3200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitCommitShaOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gitRepoUrlOverride")
    def git_repo_url_override(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitRepoUrlOverride"))

    @git_repo_url_override.setter
    def git_repo_url_override(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19e6a46905795090f9f235d7ea2f95c0282dcb3ea533553002ad0708e60f7cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitRepoUrlOverride", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="datadog-cdk-constructs-v2.DatadogLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "add_layers": "addLayers",
        "api_key": "apiKey",
        "api_key_secret": "apiKeySecret",
        "api_key_secret_arn": "apiKeySecretArn",
        "api_kms_key": "apiKmsKey",
        "apm_flush_deadline": "apmFlushDeadline",
        "capture_lambda_payload": "captureLambdaPayload",
        "cold_start_trace_skip_libs": "coldStartTraceSkipLibs",
        "create_forwarder_permissions": "createForwarderPermissions",
        "decode_authorizer_context": "decodeAuthorizerContext",
        "dotnet_layer_version": "dotnetLayerVersion",
        "enable_cold_start_tracing": "enableColdStartTracing",
        "enable_datadog_asm": "enableDatadogASM",
        "enable_datadog_logs": "enableDatadogLogs",
        "enable_datadog_tracing": "enableDatadogTracing",
        "enable_merge_xray_traces": "enableMergeXrayTraces",
        "enable_profiling": "enableProfiling",
        "encode_authorizer_context": "encodeAuthorizerContext",
        "env": "env",
        "extension_layer_version": "extensionLayerVersion",
        "flush_metrics_to_logs": "flushMetricsToLogs",
        "forwarder_arn": "forwarderArn",
        "grant_secret_read_access": "grantSecretReadAccess",
        "inject_log_context": "injectLogContext",
        "java_layer_version": "javaLayerVersion",
        "log_level": "logLevel",
        "min_cold_start_trace_duration": "minColdStartTraceDuration",
        "node_layer_version": "nodeLayerVersion",
        "python_layer_version": "pythonLayerVersion",
        "redirect_handler": "redirectHandler",
        "service": "service",
        "site": "site",
        "source_code_integration": "sourceCodeIntegration",
        "tags": "tags",
        "use_layers_from_account": "useLayersFromAccount",
        "version": "version",
    },
)
class DatadogLambdaProps:
    def __init__(
        self,
        *,
        add_layers: typing.Optional[builtins.bool] = None,
        api_key: typing.Optional[builtins.str] = None,
        api_key_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        api_key_secret_arn: typing.Optional[builtins.str] = None,
        api_kms_key: typing.Optional[builtins.str] = None,
        apm_flush_deadline: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
        capture_lambda_payload: typing.Optional[builtins.bool] = None,
        cold_start_trace_skip_libs: typing.Optional[builtins.str] = None,
        create_forwarder_permissions: typing.Optional[builtins.bool] = None,
        decode_authorizer_context: typing.Optional[builtins.bool] = None,
        dotnet_layer_version: typing.Optional[jsii.Number] = None,
        enable_cold_start_tracing: typing.Optional[builtins.bool] = None,
        enable_datadog_asm: typing.Optional[builtins.bool] = None,
        enable_datadog_logs: typing.Optional[builtins.bool] = None,
        enable_datadog_tracing: typing.Optional[builtins.bool] = None,
        enable_merge_xray_traces: typing.Optional[builtins.bool] = None,
        enable_profiling: typing.Optional[builtins.bool] = None,
        encode_authorizer_context: typing.Optional[builtins.bool] = None,
        env: typing.Optional[builtins.str] = None,
        extension_layer_version: typing.Optional[jsii.Number] = None,
        flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
        forwarder_arn: typing.Optional[builtins.str] = None,
        grant_secret_read_access: typing.Optional[builtins.bool] = None,
        inject_log_context: typing.Optional[builtins.bool] = None,
        java_layer_version: typing.Optional[jsii.Number] = None,
        log_level: typing.Optional[builtins.str] = None,
        min_cold_start_trace_duration: typing.Optional[jsii.Number] = None,
        node_layer_version: typing.Optional[jsii.Number] = None,
        python_layer_version: typing.Optional[jsii.Number] = None,
        redirect_handler: typing.Optional[builtins.bool] = None,
        service: typing.Optional[builtins.str] = None,
        site: typing.Optional[builtins.str] = None,
        source_code_integration: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[builtins.str] = None,
        use_layers_from_account: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param add_layers: 
        :param api_key: 
        :param api_key_secret: 
        :param api_key_secret_arn: 
        :param api_kms_key: 
        :param apm_flush_deadline: 
        :param capture_lambda_payload: 
        :param cold_start_trace_skip_libs: 
        :param create_forwarder_permissions: 
        :param decode_authorizer_context: 
        :param dotnet_layer_version: 
        :param enable_cold_start_tracing: 
        :param enable_datadog_asm: 
        :param enable_datadog_logs: 
        :param enable_datadog_tracing: 
        :param enable_merge_xray_traces: 
        :param enable_profiling: 
        :param encode_authorizer_context: 
        :param env: 
        :param extension_layer_version: 
        :param flush_metrics_to_logs: 
        :param forwarder_arn: 
        :param grant_secret_read_access: 
        :param inject_log_context: 
        :param java_layer_version: 
        :param log_level: 
        :param min_cold_start_trace_duration: 
        :param node_layer_version: 
        :param python_layer_version: 
        :param redirect_handler: 
        :param service: 
        :param site: 
        :param source_code_integration: 
        :param tags: 
        :param use_layers_from_account: 
        :param version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d91330a506031886b9d88e6eb264015f9a55aa2384c231f966073763613dde)
            check_type(argname="argument add_layers", value=add_layers, expected_type=type_hints["add_layers"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument api_key_secret", value=api_key_secret, expected_type=type_hints["api_key_secret"])
            check_type(argname="argument api_key_secret_arn", value=api_key_secret_arn, expected_type=type_hints["api_key_secret_arn"])
            check_type(argname="argument api_kms_key", value=api_kms_key, expected_type=type_hints["api_kms_key"])
            check_type(argname="argument apm_flush_deadline", value=apm_flush_deadline, expected_type=type_hints["apm_flush_deadline"])
            check_type(argname="argument capture_lambda_payload", value=capture_lambda_payload, expected_type=type_hints["capture_lambda_payload"])
            check_type(argname="argument cold_start_trace_skip_libs", value=cold_start_trace_skip_libs, expected_type=type_hints["cold_start_trace_skip_libs"])
            check_type(argname="argument create_forwarder_permissions", value=create_forwarder_permissions, expected_type=type_hints["create_forwarder_permissions"])
            check_type(argname="argument decode_authorizer_context", value=decode_authorizer_context, expected_type=type_hints["decode_authorizer_context"])
            check_type(argname="argument dotnet_layer_version", value=dotnet_layer_version, expected_type=type_hints["dotnet_layer_version"])
            check_type(argname="argument enable_cold_start_tracing", value=enable_cold_start_tracing, expected_type=type_hints["enable_cold_start_tracing"])
            check_type(argname="argument enable_datadog_asm", value=enable_datadog_asm, expected_type=type_hints["enable_datadog_asm"])
            check_type(argname="argument enable_datadog_logs", value=enable_datadog_logs, expected_type=type_hints["enable_datadog_logs"])
            check_type(argname="argument enable_datadog_tracing", value=enable_datadog_tracing, expected_type=type_hints["enable_datadog_tracing"])
            check_type(argname="argument enable_merge_xray_traces", value=enable_merge_xray_traces, expected_type=type_hints["enable_merge_xray_traces"])
            check_type(argname="argument enable_profiling", value=enable_profiling, expected_type=type_hints["enable_profiling"])
            check_type(argname="argument encode_authorizer_context", value=encode_authorizer_context, expected_type=type_hints["encode_authorizer_context"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument extension_layer_version", value=extension_layer_version, expected_type=type_hints["extension_layer_version"])
            check_type(argname="argument flush_metrics_to_logs", value=flush_metrics_to_logs, expected_type=type_hints["flush_metrics_to_logs"])
            check_type(argname="argument forwarder_arn", value=forwarder_arn, expected_type=type_hints["forwarder_arn"])
            check_type(argname="argument grant_secret_read_access", value=grant_secret_read_access, expected_type=type_hints["grant_secret_read_access"])
            check_type(argname="argument inject_log_context", value=inject_log_context, expected_type=type_hints["inject_log_context"])
            check_type(argname="argument java_layer_version", value=java_layer_version, expected_type=type_hints["java_layer_version"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument min_cold_start_trace_duration", value=min_cold_start_trace_duration, expected_type=type_hints["min_cold_start_trace_duration"])
            check_type(argname="argument node_layer_version", value=node_layer_version, expected_type=type_hints["node_layer_version"])
            check_type(argname="argument python_layer_version", value=python_layer_version, expected_type=type_hints["python_layer_version"])
            check_type(argname="argument redirect_handler", value=redirect_handler, expected_type=type_hints["redirect_handler"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument site", value=site, expected_type=type_hints["site"])
            check_type(argname="argument source_code_integration", value=source_code_integration, expected_type=type_hints["source_code_integration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument use_layers_from_account", value=use_layers_from_account, expected_type=type_hints["use_layers_from_account"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_layers is not None:
            self._values["add_layers"] = add_layers
        if api_key is not None:
            self._values["api_key"] = api_key
        if api_key_secret is not None:
            self._values["api_key_secret"] = api_key_secret
        if api_key_secret_arn is not None:
            self._values["api_key_secret_arn"] = api_key_secret_arn
        if api_kms_key is not None:
            self._values["api_kms_key"] = api_kms_key
        if apm_flush_deadline is not None:
            self._values["apm_flush_deadline"] = apm_flush_deadline
        if capture_lambda_payload is not None:
            self._values["capture_lambda_payload"] = capture_lambda_payload
        if cold_start_trace_skip_libs is not None:
            self._values["cold_start_trace_skip_libs"] = cold_start_trace_skip_libs
        if create_forwarder_permissions is not None:
            self._values["create_forwarder_permissions"] = create_forwarder_permissions
        if decode_authorizer_context is not None:
            self._values["decode_authorizer_context"] = decode_authorizer_context
        if dotnet_layer_version is not None:
            self._values["dotnet_layer_version"] = dotnet_layer_version
        if enable_cold_start_tracing is not None:
            self._values["enable_cold_start_tracing"] = enable_cold_start_tracing
        if enable_datadog_asm is not None:
            self._values["enable_datadog_asm"] = enable_datadog_asm
        if enable_datadog_logs is not None:
            self._values["enable_datadog_logs"] = enable_datadog_logs
        if enable_datadog_tracing is not None:
            self._values["enable_datadog_tracing"] = enable_datadog_tracing
        if enable_merge_xray_traces is not None:
            self._values["enable_merge_xray_traces"] = enable_merge_xray_traces
        if enable_profiling is not None:
            self._values["enable_profiling"] = enable_profiling
        if encode_authorizer_context is not None:
            self._values["encode_authorizer_context"] = encode_authorizer_context
        if env is not None:
            self._values["env"] = env
        if extension_layer_version is not None:
            self._values["extension_layer_version"] = extension_layer_version
        if flush_metrics_to_logs is not None:
            self._values["flush_metrics_to_logs"] = flush_metrics_to_logs
        if forwarder_arn is not None:
            self._values["forwarder_arn"] = forwarder_arn
        if grant_secret_read_access is not None:
            self._values["grant_secret_read_access"] = grant_secret_read_access
        if inject_log_context is not None:
            self._values["inject_log_context"] = inject_log_context
        if java_layer_version is not None:
            self._values["java_layer_version"] = java_layer_version
        if log_level is not None:
            self._values["log_level"] = log_level
        if min_cold_start_trace_duration is not None:
            self._values["min_cold_start_trace_duration"] = min_cold_start_trace_duration
        if node_layer_version is not None:
            self._values["node_layer_version"] = node_layer_version
        if python_layer_version is not None:
            self._values["python_layer_version"] = python_layer_version
        if redirect_handler is not None:
            self._values["redirect_handler"] = redirect_handler
        if service is not None:
            self._values["service"] = service
        if site is not None:
            self._values["site"] = site
        if source_code_integration is not None:
            self._values["source_code_integration"] = source_code_integration
        if tags is not None:
            self._values["tags"] = tags
        if use_layers_from_account is not None:
            self._values["use_layers_from_account"] = use_layers_from_account
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def add_layers(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("add_layers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_key_secret(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        result = self._values.get("api_key_secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    @builtins.property
    def api_key_secret_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_key_secret_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_kms_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apm_flush_deadline(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, jsii.Number]]:
        result = self._values.get("apm_flush_deadline")
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number]], result)

    @builtins.property
    def capture_lambda_payload(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("capture_lambda_payload")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cold_start_trace_skip_libs(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cold_start_trace_skip_libs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_forwarder_permissions(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_forwarder_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def decode_authorizer_context(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("decode_authorizer_context")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dotnet_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("dotnet_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_cold_start_tracing(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_cold_start_tracing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_datadog_asm(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_datadog_asm")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_datadog_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_datadog_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_datadog_tracing(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_datadog_tracing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_merge_xray_traces(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_merge_xray_traces")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_profiling(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_profiling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encode_authorizer_context(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("encode_authorizer_context")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(self) -> typing.Optional[builtins.str]:
        result = self._values.get("env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extension_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("extension_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def flush_metrics_to_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("flush_metrics_to_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def forwarder_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("forwarder_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grant_secret_read_access(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("grant_secret_read_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def inject_log_context(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("inject_log_context")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def java_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("java_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cold_start_trace_duration(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("min_cold_start_trace_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("node_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def python_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("python_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redirect_handler(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("redirect_handler")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site(self) -> typing.Optional[builtins.str]:
        result = self._values.get("site")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_code_integration(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("source_code_integration")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[builtins.str]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_layers_from_account(self) -> typing.Optional[builtins.str]:
        result = self._values.get("use_layers_from_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="datadog-cdk-constructs-v2.DatadogLambdaStrictProps",
    jsii_struct_bases=[],
    name_mapping={
        "add_layers": "addLayers",
        "capture_lambda_payload": "captureLambdaPayload",
        "enable_datadog_asm": "enableDatadogASM",
        "enable_datadog_logs": "enableDatadogLogs",
        "enable_datadog_tracing": "enableDatadogTracing",
        "enable_merge_xray_traces": "enableMergeXrayTraces",
        "grant_secret_read_access": "grantSecretReadAccess",
        "inject_log_context": "injectLogContext",
        "api_key": "apiKey",
        "api_key_secret": "apiKeySecret",
        "api_key_secret_arn": "apiKeySecretArn",
        "api_kms_key": "apiKmsKey",
        "extension_layer_version": "extensionLayerVersion",
        "flush_metrics_to_logs": "flushMetricsToLogs",
        "forwarder_arn": "forwarderArn",
        "java_layer_version": "javaLayerVersion",
        "log_level": "logLevel",
        "node_layer_version": "nodeLayerVersion",
        "python_layer_version": "pythonLayerVersion",
        "redirect_handler": "redirectHandler",
        "site": "site",
        "source_code_integration": "sourceCodeIntegration",
    },
)
class DatadogLambdaStrictProps:
    def __init__(
        self,
        *,
        add_layers: builtins.bool,
        capture_lambda_payload: builtins.bool,
        enable_datadog_asm: builtins.bool,
        enable_datadog_logs: builtins.bool,
        enable_datadog_tracing: builtins.bool,
        enable_merge_xray_traces: builtins.bool,
        grant_secret_read_access: builtins.bool,
        inject_log_context: builtins.bool,
        api_key: typing.Optional[builtins.str] = None,
        api_key_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        api_key_secret_arn: typing.Optional[builtins.str] = None,
        api_kms_key: typing.Optional[builtins.str] = None,
        extension_layer_version: typing.Optional[jsii.Number] = None,
        flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
        forwarder_arn: typing.Optional[builtins.str] = None,
        java_layer_version: typing.Optional[jsii.Number] = None,
        log_level: typing.Optional[builtins.str] = None,
        node_layer_version: typing.Optional[jsii.Number] = None,
        python_layer_version: typing.Optional[jsii.Number] = None,
        redirect_handler: typing.Optional[builtins.bool] = None,
        site: typing.Optional[builtins.str] = None,
        source_code_integration: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param add_layers: 
        :param capture_lambda_payload: 
        :param enable_datadog_asm: 
        :param enable_datadog_logs: 
        :param enable_datadog_tracing: 
        :param enable_merge_xray_traces: 
        :param grant_secret_read_access: 
        :param inject_log_context: 
        :param api_key: 
        :param api_key_secret: 
        :param api_key_secret_arn: 
        :param api_kms_key: 
        :param extension_layer_version: 
        :param flush_metrics_to_logs: 
        :param forwarder_arn: 
        :param java_layer_version: 
        :param log_level: 
        :param node_layer_version: 
        :param python_layer_version: 
        :param redirect_handler: 
        :param site: 
        :param source_code_integration: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a8c4fb2da825eb5b4c4706ded5ed3a805d4d22c40216a83a302992413a7603)
            check_type(argname="argument add_layers", value=add_layers, expected_type=type_hints["add_layers"])
            check_type(argname="argument capture_lambda_payload", value=capture_lambda_payload, expected_type=type_hints["capture_lambda_payload"])
            check_type(argname="argument enable_datadog_asm", value=enable_datadog_asm, expected_type=type_hints["enable_datadog_asm"])
            check_type(argname="argument enable_datadog_logs", value=enable_datadog_logs, expected_type=type_hints["enable_datadog_logs"])
            check_type(argname="argument enable_datadog_tracing", value=enable_datadog_tracing, expected_type=type_hints["enable_datadog_tracing"])
            check_type(argname="argument enable_merge_xray_traces", value=enable_merge_xray_traces, expected_type=type_hints["enable_merge_xray_traces"])
            check_type(argname="argument grant_secret_read_access", value=grant_secret_read_access, expected_type=type_hints["grant_secret_read_access"])
            check_type(argname="argument inject_log_context", value=inject_log_context, expected_type=type_hints["inject_log_context"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument api_key_secret", value=api_key_secret, expected_type=type_hints["api_key_secret"])
            check_type(argname="argument api_key_secret_arn", value=api_key_secret_arn, expected_type=type_hints["api_key_secret_arn"])
            check_type(argname="argument api_kms_key", value=api_kms_key, expected_type=type_hints["api_kms_key"])
            check_type(argname="argument extension_layer_version", value=extension_layer_version, expected_type=type_hints["extension_layer_version"])
            check_type(argname="argument flush_metrics_to_logs", value=flush_metrics_to_logs, expected_type=type_hints["flush_metrics_to_logs"])
            check_type(argname="argument forwarder_arn", value=forwarder_arn, expected_type=type_hints["forwarder_arn"])
            check_type(argname="argument java_layer_version", value=java_layer_version, expected_type=type_hints["java_layer_version"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument node_layer_version", value=node_layer_version, expected_type=type_hints["node_layer_version"])
            check_type(argname="argument python_layer_version", value=python_layer_version, expected_type=type_hints["python_layer_version"])
            check_type(argname="argument redirect_handler", value=redirect_handler, expected_type=type_hints["redirect_handler"])
            check_type(argname="argument site", value=site, expected_type=type_hints["site"])
            check_type(argname="argument source_code_integration", value=source_code_integration, expected_type=type_hints["source_code_integration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "add_layers": add_layers,
            "capture_lambda_payload": capture_lambda_payload,
            "enable_datadog_asm": enable_datadog_asm,
            "enable_datadog_logs": enable_datadog_logs,
            "enable_datadog_tracing": enable_datadog_tracing,
            "enable_merge_xray_traces": enable_merge_xray_traces,
            "grant_secret_read_access": grant_secret_read_access,
            "inject_log_context": inject_log_context,
        }
        if api_key is not None:
            self._values["api_key"] = api_key
        if api_key_secret is not None:
            self._values["api_key_secret"] = api_key_secret
        if api_key_secret_arn is not None:
            self._values["api_key_secret_arn"] = api_key_secret_arn
        if api_kms_key is not None:
            self._values["api_kms_key"] = api_kms_key
        if extension_layer_version is not None:
            self._values["extension_layer_version"] = extension_layer_version
        if flush_metrics_to_logs is not None:
            self._values["flush_metrics_to_logs"] = flush_metrics_to_logs
        if forwarder_arn is not None:
            self._values["forwarder_arn"] = forwarder_arn
        if java_layer_version is not None:
            self._values["java_layer_version"] = java_layer_version
        if log_level is not None:
            self._values["log_level"] = log_level
        if node_layer_version is not None:
            self._values["node_layer_version"] = node_layer_version
        if python_layer_version is not None:
            self._values["python_layer_version"] = python_layer_version
        if redirect_handler is not None:
            self._values["redirect_handler"] = redirect_handler
        if site is not None:
            self._values["site"] = site
        if source_code_integration is not None:
            self._values["source_code_integration"] = source_code_integration

    @builtins.property
    def add_layers(self) -> builtins.bool:
        result = self._values.get("add_layers")
        assert result is not None, "Required property 'add_layers' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def capture_lambda_payload(self) -> builtins.bool:
        result = self._values.get("capture_lambda_payload")
        assert result is not None, "Required property 'capture_lambda_payload' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_datadog_asm(self) -> builtins.bool:
        result = self._values.get("enable_datadog_asm")
        assert result is not None, "Required property 'enable_datadog_asm' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_datadog_logs(self) -> builtins.bool:
        result = self._values.get("enable_datadog_logs")
        assert result is not None, "Required property 'enable_datadog_logs' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_datadog_tracing(self) -> builtins.bool:
        result = self._values.get("enable_datadog_tracing")
        assert result is not None, "Required property 'enable_datadog_tracing' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_merge_xray_traces(self) -> builtins.bool:
        result = self._values.get("enable_merge_xray_traces")
        assert result is not None, "Required property 'enable_merge_xray_traces' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def grant_secret_read_access(self) -> builtins.bool:
        result = self._values.get("grant_secret_read_access")
        assert result is not None, "Required property 'grant_secret_read_access' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def inject_log_context(self) -> builtins.bool:
        result = self._values.get("inject_log_context")
        assert result is not None, "Required property 'inject_log_context' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_key_secret(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        result = self._values.get("api_key_secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    @builtins.property
    def api_key_secret_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_key_secret_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_kms_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extension_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("extension_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def flush_metrics_to_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("flush_metrics_to_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def forwarder_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("forwarder_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def java_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("java_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("node_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def python_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("python_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redirect_handler(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("redirect_handler")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def site(self) -> typing.Optional[builtins.str]:
        result = self._values.get("site")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_code_integration(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("source_code_integration")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogLambdaStrictProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatadogStepFunctions(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="datadog-cdk-constructs-v2.DatadogStepFunctions",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        env: typing.Optional[builtins.str] = None,
        forwarder_arn: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        tags: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param env: 
        :param forwarder_arn: 
        :param service: 
        :param tags: 
        :param version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22de8a6a119027e0b8ea7ca177be2b03b18fed9df0d8d06f09e4d0c4f3d1061a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DatadogStepFunctionsProps(
            env=env,
            forwarder_arn=forwarder_arn,
            service=service,
            tags=tags,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="buildLambdaPayloadToMergeTraces")
    @builtins.classmethod
    def build_lambda_payload_to_merge_traces(
        cls,
        payload: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param payload: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff43489bd1ac32321747cea710370f4bdce5f242ff13f9380a1361dc8d284ba)
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.sinvoke(cls, "buildLambdaPayloadToMergeTraces", [payload]))

    @jsii.member(jsii_name="buildStepFunctionTaskInputToMergeTraces")
    @builtins.classmethod
    def build_step_function_task_input_to_merge_traces(
        cls,
        input: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param input: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ee3a45fd279fff6068db6e8febc4482deff2e00f87e20181cac602b782daf5)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.sinvoke(cls, "buildStepFunctionTaskInputToMergeTraces", [input]))

    @jsii.member(jsii_name="addStateMachines")
    def add_state_machines(
        self,
        state_machines: typing.Sequence[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine],
        construct: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    ) -> None:
        '''
        :param state_machines: -
        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a8b1a0693488cc7f0ec2cc582bb311867b6a762accc86928ae3b12a97d6aef)
            check_type(argname="argument state_machines", value=state_machines, expected_type=type_hints["state_machines"])
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(None, jsii.invoke(self, "addStateMachines", [state_machines, construct]))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "DatadogStepFunctionsProps":
        return typing.cast("DatadogStepFunctionsProps", jsii.get(self, "props"))

    @props.setter
    def props(self, value: "DatadogStepFunctionsProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b10ed674eb55ba6d923f23a99b43b07d2c6f239f5c4ce9e7fa058477b59c90f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> _constructs_77d1e7e8.Construct:
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: _constructs_77d1e7e8.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b1d09fd1401fae9805dc0d66cb2c39f536e290d1dc30696de1ad72771731685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> _aws_cdk_ceddda9d.Stack:
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.get(self, "stack"))

    @stack.setter
    def stack(self, value: _aws_cdk_ceddda9d.Stack) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6ed5d0fcff8c46a1c7c2760ce2c125fa08fba4d53c4e7781f64cd428d87bf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stack", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="datadog-cdk-constructs-v2.DatadogStepFunctionsProps",
    jsii_struct_bases=[],
    name_mapping={
        "env": "env",
        "forwarder_arn": "forwarderArn",
        "service": "service",
        "tags": "tags",
        "version": "version",
    },
)
class DatadogStepFunctionsProps:
    def __init__(
        self,
        *,
        env: typing.Optional[builtins.str] = None,
        forwarder_arn: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        tags: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param env: 
        :param forwarder_arn: 
        :param service: 
        :param tags: 
        :param version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f1437564f1e6a00aa900ce6ba8b85e2a53793b8631eb501f23de91c18e435a)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument forwarder_arn", value=forwarder_arn, expected_type=type_hints["forwarder_arn"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if forwarder_arn is not None:
            self._values["forwarder_arn"] = forwarder_arn
        if service is not None:
            self._values["service"] = service
        if tags is not None:
            self._values["tags"] = tags
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def env(self) -> typing.Optional[builtins.str]:
        result = self._values.get("env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forwarder_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("forwarder_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[builtins.str]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogStepFunctionsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="datadog-cdk-constructs-v2.Node",
    jsii_struct_bases=[],
    name_mapping={"default_child": "defaultChild"},
)
class Node:
    def __init__(self, *, default_child: typing.Any) -> None:
        '''
        :param default_child: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b031a9a9356d281380eb23c847fc68b7a40ef4f9c9175b10723b3df950f40fd)
            check_type(argname="argument default_child", value=default_child, expected_type=type_hints["default_child"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_child": default_child,
        }

    @builtins.property
    def default_child(self) -> typing.Any:
        result = self._values.get("default_child")
        assert result is not None, "Required property 'default_child' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Node(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="datadog-cdk-constructs-v2.Runtime",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class Runtime:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0639977270a81d2f0f42855c73d20a000172a5161638228ab6cd9a064a29942a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Runtime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="datadog-cdk-constructs-v2.RuntimeType")
class RuntimeType(enum.Enum):
    DOTNET = "DOTNET"
    NODE = "NODE"
    PYTHON = "PYTHON"
    JAVA = "JAVA"
    CUSTOM = "CUSTOM"
    UNSUPPORTED = "UNSUPPORTED"


@jsii.enum(jsii_type="datadog-cdk-constructs-v2.TagKeys")
class TagKeys(enum.Enum):
    CDK = "CDK"
    ENV = "ENV"
    SERVICE = "SERVICE"
    VERSION = "VERSION"
    DD_TRACE_ENABLED = "DD_TRACE_ENABLED"


class Transport(
    metaclass=jsii.JSIIMeta,
    jsii_type="datadog-cdk-constructs-v2.Transport",
):
    def __init__(
        self,
        flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
        site: typing.Optional[builtins.str] = None,
        api_key: typing.Optional[builtins.str] = None,
        api_key_secret_arn: typing.Optional[builtins.str] = None,
        api_kms_key: typing.Optional[builtins.str] = None,
        extension_layer_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param flush_metrics_to_logs: -
        :param site: -
        :param api_key: -
        :param api_key_secret_arn: -
        :param api_kms_key: -
        :param extension_layer_version: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0096d7b257dfe55c39e9a74f016968fe42afe4617f426d50fed2ef3441338d7)
            check_type(argname="argument flush_metrics_to_logs", value=flush_metrics_to_logs, expected_type=type_hints["flush_metrics_to_logs"])
            check_type(argname="argument site", value=site, expected_type=type_hints["site"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument api_key_secret_arn", value=api_key_secret_arn, expected_type=type_hints["api_key_secret_arn"])
            check_type(argname="argument api_kms_key", value=api_kms_key, expected_type=type_hints["api_kms_key"])
            check_type(argname="argument extension_layer_version", value=extension_layer_version, expected_type=type_hints["extension_layer_version"])
        jsii.create(self.__class__, self, [flush_metrics_to_logs, site, api_key, api_key_secret_arn, api_kms_key, extension_layer_version])

    @jsii.member(jsii_name="applyEnvVars")
    def apply_env_vars(self, lam: _aws_cdk_aws_lambda_ceddda9d.Function) -> None:
        '''
        :param lam: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b2b48b92acf28e2e8ffef9123831fc89362305a97cfed821d91c642a67dd86)
            check_type(argname="argument lam", value=lam, expected_type=type_hints["lam"])
        return typing.cast(None, jsii.invoke(self, "applyEnvVars", [lam]))

    @builtins.property
    @jsii.member(jsii_name="flushMetricsToLogs")
    def flush_metrics_to_logs(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "flushMetricsToLogs"))

    @flush_metrics_to_logs.setter
    def flush_metrics_to_logs(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d37a95f6dd3d1a31b972e8a18e2e936cbf664a6115834cfcc7603f98c551a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flushMetricsToLogs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="site")
    def site(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "site"))

    @site.setter
    def site(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f64e6254d5b2c7300d506cc6c873060cbbc2f69b870b7754d459d721bfc9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "site", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972f96a848003a1b191a5a2b1b385eb8ae5537da456ee82835b121b2f7bee129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKeySecretArn")
    def api_key_secret_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeySecretArn"))

    @api_key_secret_arn.setter
    def api_key_secret_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a239562249ca542ce2cf0d1c83a0a743656792a47b3366d1ae3d031f42f5c3ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeySecretArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKmsKey")
    def api_kms_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKmsKey"))

    @api_kms_key.setter
    def api_kms_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a0c11321e5495d2118a192e3d4e7e1cc604ec8c806a36ab92a4dfc5dec7bfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extensionLayerVersion")
    def extension_layer_version(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "extensionLayerVersion"))

    @extension_layer_version.setter
    def extension_layer_version(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e4df65851315cbd779a7d51db28b4f9f2ff24e8d2030ab94830e4548e02f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionLayerVersion", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DatadogLambda",
    "DatadogLambdaProps",
    "DatadogLambdaStrictProps",
    "DatadogStepFunctions",
    "DatadogStepFunctionsProps",
    "Node",
    "Runtime",
    "RuntimeType",
    "TagKeys",
    "Transport",
]

publication.publish()

def _typecheckingstub__7d2984f96d56b35b6bf9f462eeb539cb66d7814bc0c2c05efa693a19e965978d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    add_layers: typing.Optional[builtins.bool] = None,
    api_key: typing.Optional[builtins.str] = None,
    api_key_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    api_key_secret_arn: typing.Optional[builtins.str] = None,
    api_kms_key: typing.Optional[builtins.str] = None,
    apm_flush_deadline: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
    capture_lambda_payload: typing.Optional[builtins.bool] = None,
    cold_start_trace_skip_libs: typing.Optional[builtins.str] = None,
    create_forwarder_permissions: typing.Optional[builtins.bool] = None,
    decode_authorizer_context: typing.Optional[builtins.bool] = None,
    dotnet_layer_version: typing.Optional[jsii.Number] = None,
    enable_cold_start_tracing: typing.Optional[builtins.bool] = None,
    enable_datadog_asm: typing.Optional[builtins.bool] = None,
    enable_datadog_logs: typing.Optional[builtins.bool] = None,
    enable_datadog_tracing: typing.Optional[builtins.bool] = None,
    enable_merge_xray_traces: typing.Optional[builtins.bool] = None,
    enable_profiling: typing.Optional[builtins.bool] = None,
    encode_authorizer_context: typing.Optional[builtins.bool] = None,
    env: typing.Optional[builtins.str] = None,
    extension_layer_version: typing.Optional[jsii.Number] = None,
    flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
    forwarder_arn: typing.Optional[builtins.str] = None,
    grant_secret_read_access: typing.Optional[builtins.bool] = None,
    inject_log_context: typing.Optional[builtins.bool] = None,
    java_layer_version: typing.Optional[jsii.Number] = None,
    log_level: typing.Optional[builtins.str] = None,
    min_cold_start_trace_duration: typing.Optional[jsii.Number] = None,
    node_layer_version: typing.Optional[jsii.Number] = None,
    python_layer_version: typing.Optional[jsii.Number] = None,
    redirect_handler: typing.Optional[builtins.bool] = None,
    service: typing.Optional[builtins.str] = None,
    site: typing.Optional[builtins.str] = None,
    source_code_integration: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[builtins.str] = None,
    use_layers_from_account: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d077b7f7df346dab533a634af3f0901767a9f2b837615c493fef851e2caeaa37(
    log_groups: typing.Sequence[_aws_cdk_aws_logs_ceddda9d.ILogGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea846263375949d2a4455edf17977f56d13f60fa2f6f2d50679231a2ee9e68e(
    lambda_functions: typing.Sequence[typing.Union[_aws_cdk_aws_lambda_ceddda9d.Function, _aws_cdk_aws_lambda_ceddda9d.SingletonFunction]],
    git_commit_sha: typing.Optional[builtins.str] = None,
    git_repo_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9f739b7a469f9944fd92418630c6ace0920581d7aba71e8bb4836e1878bb6c(
    lambda_functions: typing.Sequence[typing.Union[_aws_cdk_aws_lambda_ceddda9d.Function, _aws_cdk_aws_lambda_ceddda9d.SingletonFunction]],
    construct: typing.Optional[_constructs_77d1e7e8.Construct] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add190e793382279b2292e564b6b7af77c9e86799063643d34222561b86f6bcd(
    git_commit_sha: builtins.str,
    git_repo_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637733c25a7c2850eaee52097e2193a573cd89b62a7c3996ea0fda7addda066c(
    value: typing.List[typing.Union[_aws_cdk_aws_lambda_ceddda9d.Function, _aws_cdk_aws_lambda_ceddda9d.SingletonFunction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cacc2a125e366ff9b1144af9ca07a68614e32ac99686c20a48c623921b3359e(
    value: DatadogLambdaProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd01617eb2e87ed512be49dc83a00ad8014edd30800c640e958188cbcb58426f(
    value: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01077f52f36828b6127966c542bcbf9e86506f40b406b02d331a1f5f35827b96(
    value: Transport,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__213e6389c94903631c6747e04649248f0784d5717f40ad071d3c71802a5c3200(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19e6a46905795090f9f235d7ea2f95c0282dcb3ea533553002ad0708e60f7cd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d91330a506031886b9d88e6eb264015f9a55aa2384c231f966073763613dde(
    *,
    add_layers: typing.Optional[builtins.bool] = None,
    api_key: typing.Optional[builtins.str] = None,
    api_key_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    api_key_secret_arn: typing.Optional[builtins.str] = None,
    api_kms_key: typing.Optional[builtins.str] = None,
    apm_flush_deadline: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
    capture_lambda_payload: typing.Optional[builtins.bool] = None,
    cold_start_trace_skip_libs: typing.Optional[builtins.str] = None,
    create_forwarder_permissions: typing.Optional[builtins.bool] = None,
    decode_authorizer_context: typing.Optional[builtins.bool] = None,
    dotnet_layer_version: typing.Optional[jsii.Number] = None,
    enable_cold_start_tracing: typing.Optional[builtins.bool] = None,
    enable_datadog_asm: typing.Optional[builtins.bool] = None,
    enable_datadog_logs: typing.Optional[builtins.bool] = None,
    enable_datadog_tracing: typing.Optional[builtins.bool] = None,
    enable_merge_xray_traces: typing.Optional[builtins.bool] = None,
    enable_profiling: typing.Optional[builtins.bool] = None,
    encode_authorizer_context: typing.Optional[builtins.bool] = None,
    env: typing.Optional[builtins.str] = None,
    extension_layer_version: typing.Optional[jsii.Number] = None,
    flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
    forwarder_arn: typing.Optional[builtins.str] = None,
    grant_secret_read_access: typing.Optional[builtins.bool] = None,
    inject_log_context: typing.Optional[builtins.bool] = None,
    java_layer_version: typing.Optional[jsii.Number] = None,
    log_level: typing.Optional[builtins.str] = None,
    min_cold_start_trace_duration: typing.Optional[jsii.Number] = None,
    node_layer_version: typing.Optional[jsii.Number] = None,
    python_layer_version: typing.Optional[jsii.Number] = None,
    redirect_handler: typing.Optional[builtins.bool] = None,
    service: typing.Optional[builtins.str] = None,
    site: typing.Optional[builtins.str] = None,
    source_code_integration: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[builtins.str] = None,
    use_layers_from_account: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a8c4fb2da825eb5b4c4706ded5ed3a805d4d22c40216a83a302992413a7603(
    *,
    add_layers: builtins.bool,
    capture_lambda_payload: builtins.bool,
    enable_datadog_asm: builtins.bool,
    enable_datadog_logs: builtins.bool,
    enable_datadog_tracing: builtins.bool,
    enable_merge_xray_traces: builtins.bool,
    grant_secret_read_access: builtins.bool,
    inject_log_context: builtins.bool,
    api_key: typing.Optional[builtins.str] = None,
    api_key_secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    api_key_secret_arn: typing.Optional[builtins.str] = None,
    api_kms_key: typing.Optional[builtins.str] = None,
    extension_layer_version: typing.Optional[jsii.Number] = None,
    flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
    forwarder_arn: typing.Optional[builtins.str] = None,
    java_layer_version: typing.Optional[jsii.Number] = None,
    log_level: typing.Optional[builtins.str] = None,
    node_layer_version: typing.Optional[jsii.Number] = None,
    python_layer_version: typing.Optional[jsii.Number] = None,
    redirect_handler: typing.Optional[builtins.bool] = None,
    site: typing.Optional[builtins.str] = None,
    source_code_integration: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22de8a6a119027e0b8ea7ca177be2b03b18fed9df0d8d06f09e4d0c4f3d1061a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    env: typing.Optional[builtins.str] = None,
    forwarder_arn: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    tags: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff43489bd1ac32321747cea710370f4bdce5f242ff13f9380a1361dc8d284ba(
    payload: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ee3a45fd279fff6068db6e8febc4482deff2e00f87e20181cac602b782daf5(
    input: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a8b1a0693488cc7f0ec2cc582bb311867b6a762accc86928ae3b12a97d6aef(
    state_machines: typing.Sequence[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine],
    construct: typing.Optional[_constructs_77d1e7e8.Construct] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b10ed674eb55ba6d923f23a99b43b07d2c6f239f5c4ce9e7fa058477b59c90f(
    value: DatadogStepFunctionsProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1d09fd1401fae9805dc0d66cb2c39f536e290d1dc30696de1ad72771731685(
    value: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6ed5d0fcff8c46a1c7c2760ce2c125fa08fba4d53c4e7781f64cd428d87bf6(
    value: _aws_cdk_ceddda9d.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f1437564f1e6a00aa900ce6ba8b85e2a53793b8631eb501f23de91c18e435a(
    *,
    env: typing.Optional[builtins.str] = None,
    forwarder_arn: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    tags: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b031a9a9356d281380eb23c847fc68b7a40ef4f9c9175b10723b3df950f40fd(
    *,
    default_child: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0639977270a81d2f0f42855c73d20a000172a5161638228ab6cd9a064a29942a(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0096d7b257dfe55c39e9a74f016968fe42afe4617f426d50fed2ef3441338d7(
    flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
    site: typing.Optional[builtins.str] = None,
    api_key: typing.Optional[builtins.str] = None,
    api_key_secret_arn: typing.Optional[builtins.str] = None,
    api_kms_key: typing.Optional[builtins.str] = None,
    extension_layer_version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b2b48b92acf28e2e8ffef9123831fc89362305a97cfed821d91c642a67dd86(
    lam: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d37a95f6dd3d1a31b972e8a18e2e936cbf664a6115834cfcc7603f98c551a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f64e6254d5b2c7300d506cc6c873060cbbc2f69b870b7754d459d721bfc9fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972f96a848003a1b191a5a2b1b385eb8ae5537da456ee82835b121b2f7bee129(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a239562249ca542ce2cf0d1c83a0a743656792a47b3366d1ae3d031f42f5c3ba(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a0c11321e5495d2118a192e3d4e7e1cc604ec8c806a36ab92a4dfc5dec7bfa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e4df65851315cbd779a7d51db28b4f9f2ff24e8d2030ab94830e4548e02f64(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass
