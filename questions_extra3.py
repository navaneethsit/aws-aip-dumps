"""
AIP-C01 questions 76-97 and 100 (from screenshots; the source's suggested answers were
hidden, so every answer is derived from the exam guide + AWS docs and carries no vote data).

Same schema as questions.py. Q98 is missing from the source set and the Q99 screenshot
was an AI Practitioner (AIF-C01) question, so neither is included.
"""

_BR = "https://docs.aws.amazon.com/bedrock/latest/userguide"

D1 = "1 · FM Integration, Data & Compliance"
D2 = "2 · Implementation & Integration"
D3 = "3 · Safety, Security & Governance"
D4 = "4 · Operational Efficiency & Optimization"
D5 = "5 · Testing, Validation & Troubleshooting"

EXTRA3: list[dict] = [
    {
        "id": 76, "category": D2, "task": "2.4", "type": "single",
        "question": "A company has a generative AI (GenAI) application that uses Amazon Bedrock to provide real-time responses to customer queries. The company has noticed intermittent failures with API calls to foundation models (FMs) during peak traffic periods.\n"
                    "The company needs a solution to handle transient errors and provide detailed observability into FM performance. The solution must prevent cascading failures during throttling events and provide distributed tracing across service boundaries to identify latency contributors. The solution must also enable correlation of performance issues with specific FM characteristics.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Implement a custom retry mechanism with a fixed delay of 1 second between retries. Configure Amazon CloudWatch alarms to monitor the application's error rates and latency metrics.",
            "B. Configure the AWS SDK with standard retry mode and exponential backoff with jitter. Use AWS X-Ray tracing with annotations to identify and filter service components.",
            "C. Implement client-side caching of all FM responses. Add custom logging statements in the application code to record API call durations.",
            "D. Configure the AWS SDK with adaptive retry mode. Use AWS CloudTrail distributed tracing to monitor throttling events.",
        ],
        "answer": "B. Configure the AWS SDK with standard retry mode and exponential backoff with jitter. Use AWS X-Ray tracing with annotations to identify and filter service components.",
        "explanation": "**Transient errors / don't cascade** → SDK retries with **exponential backoff and jitter** (fixed delays synchronise clients and amplify throttling). **Distributed tracing across service boundaries** + **correlating with FM characteristics** → **AWS X-Ray** with **annotations** (e.g. model ID, token counts) that you can filter on (exam-guide Skills 2.4.3, 2.5.6).\n\n"
                       "**A** fixed 1-second retries create retry storms and have no tracing. **C** caching all responses is not retry handling and custom logs aren't distributed traces. **D** CloudTrail is an API audit log, not a distributed tracing tool.",
        "reference": "https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html",
        "note": "Answer derived. High confidence — 'CloudTrail distributed tracing' is a non-existent feature.",
    },
    {
        "id": 77, "category": D3, "task": "3.2", "type": "single",
        "question": "A company is building a video analysis platform on AWS. The platform will analyze a large video archive by using Amazon Rekognition and Amazon Bedrock. The platform must comply with predefined privacy standards. The platform must also use secure model I/O, control foundation model (FM) access patterns, and provide an audit of who accessed what and when.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure VPC endpoints for Amazon Bedrock model API calls. Implement Amazon Bedrock Guardrails to filter harmful or unauthorized content in prompts and responses. Use Amazon Bedrock trace events to track all agent and model invocations for auditing purposes. Export the traces to Amazon CloudWatch Logs as an audit record of model usage. Store all prompts and outputs in Amazon S3 with server-side encryption with AWS KMS keys (SSE-KMS).",
            "B. Define access control by using IAM with attribute-based controls to map departments to specific permissions. Configure VPC endpoints for Amazon Bedrock model API calls. Use IAM condition keys to enforce specific GuardrailIdentifier and ModelId values. Configure AWS CloudTrail to capture management and data events for S3 objects and KMS key usage activities. Enable S3 server access logging to record detailed file-level interactions with the video archives. Send all CloudTrail logs to AWS CloudTrail Lake. Set up Amazon CloudWatch alarms to detect and alert on unexpected activity from Amazon Bedrock, Amazon Rekognition, and AWS KMS.",
            "C. Restrict access to services by using VPC endpoint policies. Use AWS Config to track resource changes and compliance with security rules. Use server-side encryption with AWS KMS keys (SSE-KMS) to encrypt data at rest. Store the model's I/O in separate Amazon S3 buckets. Enable S3 server access logging to track file-level interactions.",
            "D. Configure AWS CloudTrail Insights to analyze API call patterns across accounts and detect anomalous activity in Amazon Bedrock, Amazon Rekognition, Amazon S3, and AWS KMS. Deploy Amazon Macie to scan and classify the video archive. Use server-side encryption with AWS KMS keys (SSE-KMS) to encrypt all stored data. Configure CloudTrail to capture KMS API usage events for audit purposes. Configure Amazon EventBridge rules to process CloudTrail Insights anomalies and Macie findings. Use CloudWatch alarms to trigger automated notifications and security responses when potential security issues are detected.",
        ],
        "answer": "B. Define access control by using IAM with attribute-based controls to map departments to specific permissions. Configure VPC endpoints for Amazon Bedrock model API calls. Use IAM condition keys to enforce specific GuardrailIdentifier and ModelId values. Configure AWS CloudTrail to capture management and data events for S3 objects and KMS key usage activities. Enable S3 server access logging to record detailed file-level interactions with the video archives. Send all CloudTrail logs to AWS CloudTrail Lake. Set up Amazon CloudWatch alarms to detect and alert on unexpected activity from Amazon Bedrock, Amazon Rekognition, and AWS KMS.",
        "explanation": "Three stated needs, one option covering all three: **secure model I/O** → VPC endpoints (private path); **control FM access patterns** → IAM **ABAC** plus condition keys that pin `bedrock:GuardrailIdentifier` and `ModelId`; **audit of who accessed what and when** → **CloudTrail** management + data events (S3, KMS), S3 server access logs, CloudTrail Lake for queries, and alarms on unexpected activity.\n\n"
                       "**A** has no identity-based access control — it can't say *who* may use which model/guardrail, and trace events aren't a 'who accessed' audit. **C** lacks access control on the FM and a true audit trail. **D** is detection/classification tooling (Insights, Macie) without access control or model-access enforcement.",
        "reference": f"{_BR}/vpc-interface-endpoints.html",
        "note": "Answer derived, moderate confidence — B is the only option combining access control + private connectivity + a who/what/when audit trail.",
    },
    {
        "id": 78, "category": D1, "task": "1.2", "type": "single",
        "question": "An insurance company uses Amazon SageMaker AI infrastructure to support a web-based application that allows customers to predict what their insurance premiums will be. The company stores customer data that is used to train the SageMaker AI model in an Amazon S3 bucket. The dataset is growing rapidly. The company wants a solution to continuously re-train the model. The solution must automatically re-train and re-deploy the model to the application when an employee uploads a new customer data file to the S3 bucket.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use AWS Glue to run an ETL job on each uploaded file. Configure the ETL job to use the AWS SDK to invoke the Sage Maker AI model endpoint. Use real-time inference with the endpoint to re-deploy the model after it is re-trained on the updated customer dataset.",
            "B. Create an AWS Lambda function and webhook handlers to generate an event when an employee uploads a new file. Configure SageMaker Pipelines to re-deploy the model after it is re-trained on the updated customer dataset. Use Amazon EventBridge to create an event bus. Set the Lambda function event as the source and SageMaker Pipelines as the target.",
            "C. Create an AWS Step Functions Express workflow with AWS SDK integrations to retrieve the customer data from the S3 bucket when an employee uploads a new file to the S3 bucket. Use a SageMaker Data Wrangler flow to export the data from the S3 bucket to SageMaker Autopilot. Use SageMaker Autopilot to re-deploy the model after it has been re-trained on the updated customer dataset.",
            "D. Create an AWS Step Functions Standard workflow. Configure the first state to call an AWS Lambda function to respond when an employee uploads a new file to the S3 bucket. Use a pipeline in SageMaker Pipelines to re-deploy the model after it has been re-trained on the updated customer dataset. Use the next state in the workflow to run the pipeline when the first state receives a response.",
        ],
        "answer": "B. Create an AWS Lambda function and webhook handlers to generate an event when an employee uploads a new file. Configure SageMaker Pipelines to re-deploy the model after it is re-trained on the updated customer dataset. Use Amazon EventBridge to create an event bus. Set the Lambda function event as the source and SageMaker Pipelines as the target.",
        "explanation": "An **event-driven retraining loop**: the S3 upload raises an event, **EventBridge** routes it, and **SageMaker Pipelines** (a native EventBridge target) runs train → evaluate → register/deploy, so retraining and redeployment are automatic (exam-guide Skills 1.2.4, 2.3.2).\n\n"
                       "**A** an ETL job calling an inference endpoint doesn't retrain anything. **C** Express workflows are for short high-volume work (retraining is long-running), and Data Wrangler/Autopilot are interactive/AutoML tools, not an automated retrain-and-redeploy pipeline. **D** is workable but wraps a Step Functions workflow around something EventBridge can trigger directly, so it adds an unnecessary layer.",
        "reference": "https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html",
        "note": "Answer derived, moderate confidence (B vs D). B is the direct event-driven route; D works but is more orchestration than needed.",
    },
    {
        "id": 79, "category": D5, "task": "5.1", "type": "single",
        "question": "A company uses Amazon Bedrock to implement a Retrieval Augmented Generation (RAG)-based system to serve medical information to users. The company needs to compare multiple chunking strategies, evaluate the generation quality of two foundation models (FMs), and enforce quality thresholds for deployment.\n"
                    "Which Amazon Bedrock evaluation configuration will meet these requirements?",
        "options": [
            "A. Create a retrieve-only evaluation job that uses a supported version of Anthropic Claude Sonnet as the evaluator model. Configure metrics for context relevance and context coverage. Define deployment thresholds in a separate CI/CD pipeline.",
            "B. Create a retrieve-and-generate evaluation job that uses custom precision at k metrics and an LLM-as-a-judge metric that uses a scale of 1-5. Include each chunking strategy in the evaluation dataset. Use a supported version of Anthropic Claude Sonnet to evaluate responses from both FMs.",
            "C. Create a separate evaluation job for each chunking strategy and FM combination. Use Amazon Bedrock built-in metrics for correctness and completeness. Manually review scores before deployment approval.",
            "D. Set up a pipeline that uses multiple retrieve-only evaluation jobs to assess retrieval quality. Create separate evaluation jobs for both FMs that use Amazon Nova Pro as the LLM-as-a-judge model. Evaluate based on faithfulness and citation precision metrics.",
        ],
        "answer": "B. Create a retrieve-and-generate evaluation job that uses custom precision at k metrics and an LLM-as-a-judge metric that uses a scale of 1-5. Include each chunking strategy in the evaluation dataset. Use a supported version of Anthropic Claude Sonnet to evaluate responses from both FMs.",
        "explanation": "The requirement spans **both retrieval (chunking strategies) and generation (two FMs)**, so you need a **retrieve-and-generate** evaluation job — retrieve-only jobs can't assess answer quality. A **custom retrieval metric** (precision@k) captures chunk quality, an **LLM-as-a-judge** scored 1–5 gives a numeric score you can gate on, and the dataset spans the chunking strategies.\n\n"
                       "**A/D** retrieve-only jobs ignore generation quality. **C** manual review of many separate jobs doesn't enforce thresholds automatically.",
        "reference": f"{_BR}/evaluation-kb.html",
        "note": "Answer derived, moderate confidence — B is the only configuration covering retrieval + generation with a numeric, gate-able score.",
    },
    {
        "id": 80, "category": D3, "task": "3.1", "type": "single",
        "question": "A wildlife conservation agency operates zoos globally. The agency uses various sensors, trackers, and audiovisual recorders to monitor animal behavior. The agency wants to launch a generative AI (GenAI) assistant that can ingest multimodal data to study animal behavior.\n"
                    "The GenAI assistant must support natural language queries, avoid speculative behavioral interpretations, and maintain audit logs for ethical research audits.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Ingest raw videos into Amazon Rekognition to detect animal postures and expressions. Use Amazon Data Firehose to stream sensor and GPS data into an Amazon S3 data lake. Prompt an Amazon Bedrock foundation model (FM) by using basic templates that are stored in AWS Systems Manager Parameter Store. Use IAM policies to control access. Use AWS CloudTrail for audit logging.",
            "B. Use Amazon SageMaker Processing and Amazon Transcribe to pre-process multimodal data. Ingest summaries into an Amazon Bedrock Retrieval Augmented Generation (RAG) knowledge base. Apply Amazon Bedrock guardrails to restrict speculative outputs. Use AWS AppConfig to manage prompt templates. Use AWS CloudTrail to log research activity for audits.",
            "C. Use Amazon OpenSearch Serverless to index behavioral logs and telemetry events. Use Amazon Comprehend to extract entities. Use Amazon Bedrock to build a layer to answer questions. Embed study summaries into OpenSearch Serverless documents. Use IAM to control access. Use AWS CloudTrail to log user interactions with the AI assistant.",
            "D. Configure Amazon Q Business to federate data across Amazon S3, Amazon Kinesis, and Amazon SageMaker Feature Store. Configure Amazon EventBridge to invoke data ingestion jobs. Use custom AWS Lambda functions to filter large language model (LLM) outputs for ethical compliance before returning results to users.",
        ],
        "answer": "B. Use Amazon SageMaker Processing and Amazon Transcribe to pre-process multimodal data. Ingest summaries into an Amazon Bedrock Retrieval Augmented Generation (RAG) knowledge base. Apply Amazon Bedrock guardrails to restrict speculative outputs. Use AWS AppConfig to manage prompt templates. Use AWS CloudTrail to log research activity for audits.",
        "explanation": "Each requirement lands on a managed feature: **multimodal ingestion** → pre-process audio/video/sensor data into summaries (SageMaker Processing, Transcribe) and ground the assistant with a **Knowledge Base (RAG)**; **'avoid speculative interpretations'** → **Guardrails** (e.g. grounding/denied topics); governed prompt templates via **AppConfig**; **audit logs** via **CloudTrail**.\n\n"
                       "**A** has no grounding or output control, only basic templates. **C** lacks a speculation control and a managed RAG layer. **D** Q Business over Kinesis/Feature Store isn't a fit, and custom Lambda output filters are the custom work Guardrails replaces.",
        "reference": f"{_BR}/guardrails.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 81, "category": D3, "task": "3.3", "type": "multi",
        "question": "A company uses an organization in AWS Organizations with all features enabled to manage multiple AWS accounts. Employees use Amazon Bedrock across multiple accounts. The company must prevent specific topics and proprietary information from being included in prompts to Amazon Bedrock models. The company must ensure that employees can use only approved Amazon Bedrock models. The company centrally manages IAM roles for employees.\n"
                    "Which combination of solutions will meet these requirements? (Choose two.)",
        "options": [
            "A. Create an IAM permissions boundary for each employee's IAM role. Configure the permissions boundary to require an approved Amazon Bedrock guardrail identifier to invoke Amazon Bedrock models. Create an SCP that allows employees to use only approved models.",
            "B. Create an SCP that allows employees to use only approved models. Configure the SCP to require employees to specify a guardrail identifier in calls to invoke an approved model.",
            "C. Create an SCP that prevents an employee from invoking a model if a centrally deployed guardrail identifier is not specified in a call to the model. Create a permissions boundary on each employee's IAM role that allows each employee to invoke only approved models.",
            "D. Use AWS CloudFormation to create a custom Amazon Bedrock guardrail that has a block filtering policy. Use stack sets to deploy the guardrail to each account in the organization.",
            "E. Use AWS CloudFormation to create a custom Amazon Bedrock guardrail that has a mask filtering policy. Use stack sets to deploy the guardrail to each account in the organization.",
        ],
        "answer": [
                      'C. Create an SCP that prevents an employee from invoking a model if a centrally deployed '
                      'guardrail identifier is not specified in a call to the model. Create a permissions boundary '
                      "on each employee's IAM role that allows each employee to invoke only approved models.",
                      'D. Use AWS CloudFormation to create a custom Amazon Bedrock guardrail that has a block '
                      'filtering policy. Use stack sets to deploy the guardrail to each account in the '
                      'organization.',
                  ],
        "explanation": 'Two controls:\\n'
                       '- **Enforce the guardrail org-wide (C):** an **SCP** that denies model invocation unless '
                       '`bedrock:GuardrailIdentifier` equals the **centrally deployed guardrail**. This is the '
                       'pattern AWS documents (an explicit Deny for any other guardrail). Because IAM roles are '
                       'centrally managed, a **permissions boundary** on each role limits them to the approved '
                       'models.\\n'
                       '- **Deploy the guardrail everywhere (D):** CloudFormation **StackSets** create the same '
                       'guardrail in every account with a **BLOCK** policy. Denied topics support only BLOCK (or '
                       'detect), so blocking is what keeps specific topics and proprietary terms out of prompts.\\n'
                       '\\n'
                       '**B** only requires *a* guardrail identifier, so an employee could pass any permissive '
                       'guardrail. **A** puts the guardrail requirement in per-role boundaries instead of an '
                       'organization-wide SCP. **E** a mask policy cannot apply to denied topics.',
        "reference": f"{_BR}/guardrails-permissions.html",
        "note": 'Cross-check: changed to C + D. Sources disagreed (CertyIQ B + E, second dump C + D, my first'
                ' pass B + D). The AWS API settles the guardrail half: denied topics allow only BLOCK or NONE'
                " (no masking), so E can't meet 'prevent specific topics'. C names the centrally deployed "
                "guardrail, which matches AWS's documented enforcement pattern. Moderate-high confidence."
    },
    {
        "id": 82, "category": D2, "task": "2.5", "type": "single",
        "question": "A company is designing an API for a generative AI (GenAI) application that uses a foundation model (FM) that is hosted on a managed model service. The API must stream responses to reduce latency, enforce token limits to manage compute resource usage, and implement retry logic to handle model timeouts and partial responses.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Integrate an Amazon API Gateway HTTP API with an AWS Lambda function to invoke Amazon Bedrock. Use Lambda response streaming to stream responses. Enforce token limits within the Lambda function. Implement retry logic for model timeouts by using Lambda and API Gateway timeout configurations.",
            "B. Connect an Amazon API Gateway HTTP API directly to Amazon Bedrock. Simulate streaming by using client-side polling. Enforce token limits on the frontend. Configure retry behavior by using API Gateway integration settings.",
            "C. Connect an Amazon API Gateway WebSocket API to an Amazon ECS service that hosts a containerized inference server. Stream responses by using the WebSocket protocol. Enforce token limits within Amazon ECS. Handle model timeouts by using ECS task lifecycle hooks and restart policies.",
            "D. Integrate an Amazon API Gateway REST API with an AWS Lambda function that invokes Amazon Bedrock. Use Lambda response streaming to stream responses. Enforce token limits within the Lambda function. Implement retry logic by using Lambda and API Gateway timeout configurations.",
        ],
        "answer": "D. Integrate an Amazon API Gateway REST API with an AWS Lambda function that invokes Amazon Bedrock. Use Lambda response streaming to stream responses. Enforce token limits within the Lambda function. Implement retry logic by using Lambda and API Gateway timeout configurations.",
        "explanation": "API Gateway **REST APIs now support response streaming** with Lambda proxy integrations (Lambda `InvokeWithResponseStream`), so tokens from Bedrock's streaming API flow to the client progressively; the Lambda function enforces token limits and retries (exam-guide Skills 2.4.2, 2.5.1). It's fully serverless — least operational overhead.\n\n"
                       "**A** is the same design on an **HTTP API**, which does not offer this REST-API response-streaming feature. **B** client-side polling simulates streaming poorly and enforcing limits on the frontend is unsafe. **C** self-hosting an inference server on ECS is the opposite of 'managed model service' and 'least overhead'.",
        "reference": "https://docs.aws.amazon.com/apigateway/latest/developerguide/response-transfer-mode-lambda.html",
        "note": 'Answer derived. High confidence on REST-vs-others; the REST API response-streaming feature '
                '(Nov 2025) is verified in the AWS docs. A is nearly identical but names an HTTP API. CertyIQ'
                " key says A (HTTP API). Kept D: the API Gateway docs state 'Response streaming is only "
                "supported for REST APIs', so an HTTP API cannot stream. A second dump (resources/1.text) "
                "also says A (HTTP API). Kept D: the API Gateway docs state 'Response streaming is only "
                "supported for REST APIs'."
    },
    {
        "id": 83, "category": D4, "task": "4.1", "type": "single",
        "question": "A retail company is using Amazon Bedrock to develop a customer service AI assistant. Analysis shows that 70% of customer inquiries are simple product questions that a smaller model can effectively handle. However, 30% of inquiries are complex return policy questions that require advanced reasoning. The company wants to implement a cost-effective model selection framework to automatically route customer inquiries to appropriate models based on inquiry complexity. The framework must maintain high customer satisfaction and minimize response latency.\n"
                    "Which solution will meet these requirements with the LEAST implementation effort?",
        "options": [
            "A. Create a multi-stage architecture that uses a small foundation model (FM) to classify the complexity of each inquiry. Route simple inquiries to a smaller, more cost-effective model. Route complex inquiries to a larger, more capable model. Use AWS Lambda functions to handle the routing logic.",
            "B. Use Amazon Bedrock intelligent prompt routing to automatically analyze inquiries. Route simple product inquiries to smaller models, and route complex return policy inquiries to more capable larger models.",
            "C. Implement a single-model solution that uses an Amazon Bedrock mid-sized foundation model (FM) with on-demand pricing. Include special instructions in model prompts to handle both simple and complex inquiries by using the same model.",
            "D. Create separate Amazon Bedrock endpoints for simple and complex inquiries. Implement a rule-based routing system based on keyword detection. Use on-demand pricing for the smaller model and provisioned throughput for the larger model.",
        ],
        "answer": "B. Use Amazon Bedrock intelligent prompt routing to automatically analyze inquiries. Route simple product inquiries to smaller models, and route complex return policy inquiries to more capable larger models.",
        "explanation": "**Bedrock Intelligent Prompt Routing** is the managed feature for exactly this: it predicts, per request, which model in a family will give the best quality/cost and routes simple prompts to the cheaper model and complex ones to the larger one — no classifier or routing code (exam-guide Skills 4.1.2, 2.4.4).\n\n"
                       "**A** builds the same thing by hand (classifier + Lambda routing). **C** one mid-sized model compromises either cost or quality. **D** keyword rules misclassify queries, and provisioned throughput adds fixed cost.",
        "reference": f"{_BR}/prompt-routing.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 84, "category": D1, "task": "1.6", "type": "single",
        "question": "A specialty coffee company has a mobile app that generates personalized coffee roast profiles by using Amazon Bedrock with a three-stage prompt chain. The prompt chain converts user inputs into structured metadata, retrieves relevant logs for coffee roasts, and generates a personalized roast recommendation for each customer. Users in multiple AWS Regions report inconsistent roast recommendations for identical inputs, slow inference during the retrieval step, and unsafe recommendations such as brewing at excessively high temperatures. The company must improve the stability of outputs for repeated inputs. The company must also improve app performance and the safety of the app's outputs. The updated solution must ensure 99.5% output consistency for identical inputs and achieve inference latency of less than 1 second. The solution must also block unsafe or hallucinated recommendations by using validated safety controls.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Deploy Amazon Bedrock with provisioned throughput to stabilize inference latency. Apply Amazon Bedrock guardrails that have semantic denial rules to block unsafe outputs. Use Amazon Bedrock Prompt Management to manage prompts by using approval workflows.",
            "B. Use Amazon Bedrock Agents to manage chaining. Log model inputs and outputs to Amazon CloudWatch Logs. Use logs from Amazon CloudWatch to perform A/B testing for prompt versions.",
            "C. Cache prompt results in Amazon ElastiCache. Use AWS Lambda functions to pre-process metadata and to trace end-to-end latency. Use AWS X-Ray to identify and remediate performance bottlenecks.",
            "D. Use Amazon Kendra to improve roast log retrieval accuracy. Store normalized prompt metadata within Amazon DynamoDB. Use AWS Step Functions to orchestrate multistep prompts.",
        ],
        "answer": "A. Deploy Amazon Bedrock with provisioned throughput to stabilize inference latency. Apply Amazon Bedrock guardrails that have semantic denial rules to block unsafe outputs. Use Amazon Bedrock Prompt Management to manage prompts by using approval workflows.",
        "explanation": "Three problems, three native controls: **latency stability/<1 s** → Provisioned Throughput (dedicated capacity, no throttling variance); **unsafe/hallucinated output** → Guardrails (semantic denied topics, grounding checks); **inconsistent prompts across Regions/versions** → Prompt Management with versioning and approval workflows so everyone runs the same validated prompt.\n\n"
                       "**B** logging and A/B testing observe problems but don't block unsafe output. **C** caching and tracing don't add safety controls. **D** Kendra/DynamoDB/Step Functions address neither safety nor consistency.",
        "reference": f"{_BR}/prompt-management.html",
        "note": "Answer derived. Moderate-high confidence — A is the only option with a validated safety control.",
    },
    {
        "id": 85, "category": D3, "task": "3.3", "type": "single",
        "question": "A company is developing a generative AI (GenAI) application by using Amazon Bedrock. The application will analyze patterns and relationships in the company's data. The application will process millions of new data points daily across AWS Regions in Europe, North America, and Asia before storing the data in Amazon S3.\n"
                    "The application must comply with local data protection and storage regulations. Data residency and processing must occur within the same continent. The application must also maintain audit trails of the application's decision-making processes and provide data classification capabilities.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Deploy the application in each Region with local IAM policies. Use Amazon Bedrock cross-Region inference to distribute the workload. Use Amazon CloudWatch to log AI decision-making processes and data processing activities. Manually track compliance certifications across Regions.",
            "B. Use SCPs with AWS Organizations to manage location-specific permissions. Use AWS CloudTrail immutable logs to audit the decision-making processes. Import a custom model into Amazon Bedrock and deploy the model to each Region.",
            "C. Use Amazon S3 Object Lock with Region-specific S3 bucket policies. Pre-process the data points within the Region based on geographic origin before sending the data points to Amazon Bedrock. Use Amazon Macie to classify the data. Use AWS CloudTrail immutable logs to audit the decision-making processes.",
            "D. Create separate AWS accounts for each Region with individual compliance frameworks. Use Amazon SageMaker AI with custom monitoring to track model performance and compliance with data residency requirements. Create manual reports for each regulatory jurisdiction.",
        ],
        "answer": "C. Use Amazon S3 Object Lock with Region-specific S3 bucket policies. Pre-process the data points within the Region based on geographic origin before sending the data points to Amazon Bedrock. Use Amazon Macie to classify the data. Use AWS CloudTrail immutable logs to audit the decision-making processes.",
        "explanation": "Map each requirement: **data residency/processing in-region** → Region-specific bucket policies and pre-processing data in the Region of origin before calling Bedrock there; **immutable retention** → S3 Object Lock; **data classification** → **Macie**; **audit trail of decision-making** → **CloudTrail** immutable (tamper-evident) logs.\n\n"
                       "**A** cross-Region inference could move processing outside the continent and compliance tracking is manual. **B** has no classification capability, and importing custom models to each Region is heavy. **D** manual reports and separate frameworks per account aren't automated controls.",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html",
        "note": "Answer derived. High confidence — C is the only option with classification (Macie) plus residency-preserving processing.",
    },
    {
        "id": 86, "category": D3, "task": "3.3", "type": "single",
        "question": "A financial services company is deploying a generative AI (GenAI) application that uses Amazon Bedrock to assist customer service representatives to provide personalized investment advice to customers. The company must implement a comprehensive governance solution that follows responsible AI practices and meets regulatory requirements.\n"
                    "The solution must detect and prevent hallucinations in recommendations. The solution must have safety controls for customer interactions. The solution must also monitor model behavior drift in real time and maintain audit trails of all prompt-response pairs for regulatory review.\n"
                    "The company must deploy the solution within 60 days. The solution must integrate with the company's existing compliance dashboard and respond to customers within 200 ms.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Configure Amazon Bedrock guardrails to apply custom content filters and toxicity detection. Use Amazon Bedrock Model Evaluation to detect hallucinations. Store prompt-response pairs in Amazon DynamoDB to capture audit trails and set a TTL. Integrate Amazon CloudWatch custom metrics with the existing compliance dashboard.",
            "B. Deploy Amazon Bedrock and use AWS PrivateLink to access the application securely. Use AWS Lambda functions to implement custom prompt validation. Store prompt-response pairs in an Amazon S3 bucket and configure S3 Lifecycle policies. Create custom Amazon CloudWatch dashboards to monitor model performance metrics.",
            "C. Use Amazon Bedrock Agents and Amazon Bedrock Knowledge Bases to ground responses. Use Amazon Bedrock Guardrails to enforce content safety. Use Amazon OpenSearch Service to store and index prompt-responses pairs. Integrate OpenSearch Service with Amazon QuickSight to create compliance reports and to detect model behavior drift.",
            "D. Use Amazon SageMaker Model Monitor to detect model behavior drift. Use AWS WAF to filter content. Store customer interactions in an encrypted Amazon RDS database. Use Amazon API Gateway to create custom HTTP APIs to integrate with the compliance dashboard.",
        ],
        "answer": "A. Configure Amazon Bedrock guardrails to apply custom content filters and toxicity detection. Use Amazon Bedrock Model Evaluation to detect hallucinations. Store prompt-response pairs in Amazon DynamoDB to capture audit trails and set a TTL. Integrate Amazon CloudWatch custom metrics with the existing compliance dashboard.",
        "explanation": "Prefer **managed, native** pieces that don't add latency: **Guardrails** (content safety), Bedrock **evaluation** for hallucination checks, **DynamoDB** (single-digit-ms writes) for prompt-response audit pairs, and **CloudWatch custom metrics** feeding the existing compliance dashboard — quick to deploy in 60 days.\n\n"
                       "**B** relies on custom Lambda prompt validation and has no hallucination/drift detection. **C** adding Agents + KB retrieval in the response path makes the 200 ms target unrealistic, and OpenSearch + QuickSight is heavy. **D** SageMaker Model Monitor is for SageMaker endpoints (not Bedrock) and WAF isn't an AI safety control.",
        "reference": f"{_BR}/guardrails.html",
        "note": "Answer derived, moderate confidence (A vs C). Deciding cues: 'least operational overhead', '200 ms' and '60 days' favour A's lightweight managed stack.",
    },
    {
        "id": 87, "category": D3, "task": "3.2", "type": "single",
        "question": "A company uses AWS Lake Formation to set up a data lake that contains databases and tables for multiple business units across multiple AWS Regions. The company wants to use a foundation model (FM) through Amazon Bedrock to perform fraud detection. The FM must ingest sensitive financial data from the data lake. The data includes some customer personally identifiable information (PII).\n"
                    "The company must design an access control solution that prevents PII from appearing in a production environment. The FM must access only authorized data subsets that have PII redacted from specific data columns. The company must capture audit trails for all data access.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Create a separate dataset in a separate Amazon S3 bucket for each business unit and Region combination. Configure S3 bucket policies to control access based on IAM roles that are assigned to FM training instances. Use S3 access logs to track data access.",
            "B. Configure the FM to authenticate by using IAM roles and Lake Formation permissions based on LF-Tag expressions. Define business units and Regions as LF-Tags that are assigned to databases and tables. Use AWS CloudTrail to collect comprehensive audit trails of data access.",
            "C. Use direct IAM principal grants on specific databases and tables in Lake Formation. Create a custom application layer that logs access requests and further filters sensitive columns before sending data to the FM.",
            "D. Configure the FM to request temporary credentials from AWS STS. Access the data by using presigned S3 URLs that are generated by an API that applies business unit and Regional filters. Use AWS CloudTrail to collect comprehensive audit trails of data access.",
        ],
        "answer": "B. Configure the FM to authenticate by using IAM roles and Lake Formation permissions based on LF-Tag expressions. Define business units and Regions as LF-Tags that are assigned to databases and tables. Use AWS CloudTrail to collect comprehensive audit trails of data access.",
        "explanation": "**Fine-grained, column-level control across business units and Regions** is Lake Formation's job; **LF-Tag-based access control** scales it (tag databases/tables/columns by business unit, Region, sensitivity and grant by tag expression) so the FM's role sees only authorised subsets with PII columns excluded. **CloudTrail** records every data-access API call (exam-guide Skill 3.2.1).\n\n"
                       "**A** copies datasets per unit/Region and can't express column-level rules. **C** direct per-resource grants don't scale, and column filtering in a custom app layer is custom work. **D** presigned S3 URLs bypass Lake Formation's column-level controls.",
        "reference": "https://docs.aws.amazon.com/lake-formation/latest/dg/tag-based-access-control.html",
        "note": "Answer derived. High confidence. (Source text contained OCR typos 'PM'/'PH' for 'PII'.)",
    },
    {
        "id": 88, "category": D1, "task": "1.5", "type": "single",
        "question": "A company runs a Retrieval Augmented Generation (RAG) application that uses Amazon Bedrock Knowledge Bases to perform regulatory compliance queries. The application uses the RetrieveAndGenerateStream API. The application retrieves relevant documents from a knowledge base that contains more than 50,000 regulatory documents, legal precedents, and policy updates.\n"
                    "The RAG application is producing suboptimal responses because the initial retrieval often returns semantically similar but contextually irrelevant documents. The poor responses are causing model hallucinations and incorrect regulatory guidance. The company needs to improve the performance of the RAG application so it returns more relevant documents.\n"
                    "Which solution will meet this requirement with the LEAST operational overhead?",
        "options": [
            "A. Deploy an Amazon SageMaker endpoint to run a fine-tuned ranking model. Use an Amazon API Gateway REST API to route requests. Configure the application to make requests through the REST API to rerank the results.",
            "B. Use Amazon Comprehend to classify documents and apply relevance scores. Integrate the RAG application's reranking process with Amazon Textract to run document analysis. Use Amazon Neptune to perform graph-based relevance calculations.",
            "C. Implement a retrieval pipeline that uses the Amazon Bedrock Knowledge Bases Retrieve API to perform initial document retrieval. Call the Amazon Bedrock Rerank API to rerank the results. Invoke the InvokeModelWithResponseStream operation to generate responses.",
            "D. Use the latest Amazon reranker model through the reranking configuration within Amazon Bedrock Knowledge Bases. Use the model to improve document relevance scoring and to reorder results based on contextual assessments.",
        ],
        "answer": "D. Use the latest Amazon reranker model through the reranking configuration within Amazon Bedrock Knowledge Bases. Use the model to improve document relevance scoring and to reorder results based on contextual assessments.",
        "explanation": "'Semantically similar but contextually irrelevant' is the reranker use case. Knowledge Bases lets you **turn on a managed reranker model in the retrieval configuration**, so the existing `RetrieveAndGenerateStream` flow just gets better ordering — a configuration change with no new code or infrastructure.\n\n"
                       "**C** also works but means rebuilding the pipeline (Retrieve → Rerank → InvokeModel) in application code. **A** self-hosted SageMaker ranker plus API Gateway is the most overhead. **B** Comprehend/Textract/Neptune are not reranking tools.",
        "reference": f"{_BR}/rerank.html",
        "note": "Answer derived. High confidence (D vs C is 'configuration' vs 'custom pipeline').",
    },
    {
        "id": 89, "category": D3, "task": "3.1", "type": "single",
        "question": "A company is developing a customer communication platform that uses an AI assistant powered by an Amazon Bedrock foundation model (FM). The AI assistant summarizes customer messages and generates initial response drafts.\n"
                    "The company wants to use Amazon Comprehend to implement layered content filtering. The layered content filtering must prevent sharing of offensive content, protect customer privacy, and detect potential inappropriate advice solicitation. Inappropriate advice solicitation includes requests for unethical practices, harmful activities, or manipulative behaviors. The solution must maintain acceptable overall response times, so all pre-processing filters must finish before the content reaches the FM.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use parallel processing with asynchronous API calls. Use toxicity detection for offensive content. Use prompt safety classification for inappropriate advice solicitation. Use personally identifiable information (PII) detection without redaction.",
            "B. Use custom classification to build an FM that detects offensive content and inappropriate advice solicitation. Apply personally identifiable information (PII) detection as a secondary filter only when messages pass the custom classifier.",
            "C. Deploy a multi-stage process. Configure the process to use prompt safety classification first, then toxicity detection on safe prompts only, and finally personally identifiable information (PII) detection in streaming mode. Route flagged messages through Amazon EventBridge for human review.",
            "D. Use toxicity detection with thresholds configured to 0.5 for all categories. Use parallel processing for both prompt safety classification and personally identifiable information (PII) detection with entity redaction. Apply Amazon CloudWatch alarms to filter metrics.",
        ],
        "answer": "D. Use toxicity detection with thresholds configured to 0.5 for all categories. Use parallel processing for both prompt safety classification and personally identifiable information (PII) detection with entity redaction. Apply Amazon CloudWatch alarms to filter metrics.",
        "explanation": "Comprehend's trust-and-safety features map one-to-one: **toxicity detection** (offensive content, with category scores you can threshold), **prompt safety classification** (detects unsafe/inappropriate requests), and **PII detection with entity redaction** (protect privacy). Running the independent filters **in parallel** keeps the added latency to the slowest single filter, so all finish before the FM call.\n\n"
                       "**A** detects PII but doesn't redact it, so privacy isn't protected. **B** 'build an FM' with custom classification is far heavier than built-in features. **C** strictly sequential stages add latency and PII detection should finish before the FM, not stream.",
        "reference": "https://docs.aws.amazon.com/comprehend/latest/dg/trust-safety.html",
        "note": "Answer derived, moderate confidence (D vs A): redaction (privacy) and parallel execution (latency) are the discriminators.",
    },
    {
        "id": 90, "category": D3, "task": "3.1", "type": "single",
        "question": "A software as a service (SaaS) company is building a recommendation model that uses Amazon SageMaker AI to support an application that recommends airline cabin upgrades to customers. The company will host SageMaker AI models on Amazon Bedrock by using Amazon Bedrock Custom Model Import. Airline companies will use the application to send customized offers to customers.\n"
                    "The model must examine the travel history of customers to help make more relevant recommendations. The company stores customer travel history data in an Amazon RDS database. The company must ensure that the application delivers consistent, relevant, and accurate results across multiple airlines and customer populations.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon Bedrock Knowledge Bases to implement a RAG architecture to analyze customer travel history data to give the application semantic search capabilities. Use the semantic search capabilities to retrieve relevant booking patterns, preferences, and loyalty information to generate personalized cabin upgrade recommendations. Apply Amazon Bedrock guardrails to filter content. Use AWS Step Functions and AWS Lambda functions to orchestrate validation workflows to reduce hallucinations.",
            "B. Implement text-to-SQL transformations with SQL validations to accurately retrieve relevant booking patterns, preferences, and loyalty information from the RDS database. Use the results to generate personalized cabin upgrade recommendations. Apply Amazon Bedrock guardrails to filter content. Use AWS Step Functions and AWS Lambda functions to orchestrate validation workflows to reduce hallucinations.",
            "C. Use Amazon OpenSearch Service to implement vector searches of customer travel history embeddings. Use the vector searches to give the application the ability to perform similarity-based retrieval of booking patterns, preferences, and loyalty information to generate personalized cabin upgrade recommendations. Apply Amazon Bedrock guardrails to filter responses. Use confidence scoring and semantic similarity searches to reduce hallucinations.",
            "D. Implement text-to-SQL transformations with SQL validations to accurately retrieve relevant booking patterns, preferences, and loyalty information from the RDS database. Use the results to generate personalized cabin upgrade recommendations. Apply Amazon Bedrock guardrails to filter responses. Use confidence scoring and semantic similarity searches to reduce hallucinations.",
        ],
        "answer": "D. Implement text-to-SQL transformations with SQL validations to accurately retrieve relevant booking patterns, preferences, and loyalty information from the RDS database. Use the results to generate personalized cabin upgrade recommendations. Apply Amazon Bedrock guardrails to filter responses. Use confidence scoring and semantic similarity searches to reduce hallucinations.",
        "explanation": "Customer travel history is **structured data in RDS**, so **text-to-SQL with SQL validation** retrieves exact, deterministic records (exam-guide Skill 3.1.2) instead of fuzzy vector similarity over copied embeddings (A, C). Output safety comes from **Guardrails**, and hallucinations are reduced with **confidence scoring and semantic-similarity verification** of the response against the retrieved data (Skill 3.1.3).\n\n"
                       "**A/C** replicate structured data into vector stores, losing exactness and freshness. **B** also uses text-to-SQL, but relies on Step Functions/Lambda validation workflows rather than confidence/similarity verification, and applies guardrails to 'content' rather than responses.",
        "reference": f"{_BR}/guardrails-contextual-grounding-check.html",
        "note": "Answer derived, LOW-MODERATE confidence (D vs B). Both use text-to-SQL; D's tail ('confidence scoring and semantic similarity searches') mirrors exam-guide Skill 3.1.3 for reducing hallucinations, while B's tail is generic orchestration. If you can reveal the source's suggested answer, I'll confirm or correct.",
    },
    {
        "id": 91, "category": D3, "task": "3.2", "type": "single",
        "question": "A company is using Amazon Bedrock to develop a customer support AI assistant. The AI assistant must respond to customer questions about their accounts. The AI assistant must not expose personal information in responses. The company must comply with data residency policies by ensuring that all processing occurs within the same AWS Region where each customer is located.\n"
                    "The company wants to evaluate how effective the AI assistant is at preventing the exposure of personal information before the company makes the AI assistant available to customers.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure a cross-Region Amazon Bedrock guardrail to apply sensitive information filters. Set the guardrail to detect mode during development and testing. Switch to block mode for production deployment.",
            "B. Configure an Amazon Bedrock guardrail to apply sensitive information filters. Set the guardrail to mask mode during development and testing. Switch to block mode for production deployment. Deploy a copy of the guardrail to each Region where the company operates.",
            "C. Configure an Amazon Bedrock guardrail to apply content and topic filters. Set the guardrail to detect mode during development, testing, and production. Disable invocation logging for the Amazon Bedrock model.",
            "D. Configure a cross-Region Amazon Bedrock guardrail to apply a set of content and word filters. Set the guardrail to detect mode during development and testing. Switch to mask mode for production deployment.",
        ],
        "answer": "B. Configure an Amazon Bedrock guardrail to apply sensitive information filters. Set the guardrail to mask mode during development and testing. Switch to block mode for production deployment. Deploy a copy of the guardrail to each Region where the company operates.",
        "explanation": "Two constraints decide it. **Residency:** processing must stay in each customer's Region, so the guardrail must be deployed **per Region** — a *cross-Region* guardrail (A, D) can route evaluation across Regions. **PII exposure:** use the **sensitive information filter**, test with **mask** mode so you can see what would be redacted, then **block** in production.\n\n"
                       "**C/D** use content/topic/word filters, which aren't PII controls, and C disables invocation logging (hurting evaluation).",
        "reference": f"{_BR}/guardrails-sensitive-filters.html",
        "note": "Answer derived, LOW-MODERATE confidence (A vs B). 'Detect' mode is Guardrails' built-in evaluation mode (A), but A's *cross-Region* guardrail conflicts with 'all processing within the same Region'; B satisfies residency. If you can reveal the source answer I'll confirm.",
    },
    {
        "id": 92, "category": D1, "task": "1.4", "type": "single",
        "question": "A university recently digitized a collection of archival documents, academic journals, and manuscripts. The university stores the digital files in an AWS Lake Formation data lake.\n"
                    "The university hires a GenAI developer to build a solution to allow users to search the digital files by using text queries. The solution must return journal abstracts that are semantically similar to a user's query. Users must be able to search the digitized collection based on text and metadata that is associated with the journal abstracts. The metadata of the digitized files does not contain keywords. The solution must match similar abstracts to one another based on the similarity of their text. The data lake contains fewer than 1 million files.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Use Amazon Titan Embeddings in Amazon Bedrock to create vector representations of the digitized files. Store embeddings in the OpenSearch Neural Plugin for Amazon OpenSearch Service.",
            "B. Use Amazon Comprehend to extract topics from the digitized files. Store the topics and file metadata in an Amazon Aurora PostgreSQL database. Query the abstract metadata against the data in the Aurora database.",
            "C. Use Amazon SageMaker AI to deploy a sentence-transformer model. Use the model to create vector representations of the digitized files. Store embeddings in an Amazon Aurora PostgreSQL database that has the pgvector extension.",
            "D. Use Amazon Titan Embeddings in Amazon Bedrock to create vector representations of the digitized files. Store embeddings in an Amazon Aurora PostgreSQL Serverless database that has the pgvector extension.",
        ],
        "answer": "D. Use Amazon Titan Embeddings in Amazon Bedrock to create vector representations of the digitized files. Store embeddings in an Amazon Aurora PostgreSQL Serverless database that has the pgvector extension.",
        "explanation": "**Semantic similarity between abstracts, no keywords** → vector embeddings. A **managed embedding model** (Titan Embeddings on Bedrock — nothing to host) plus **Aurora PostgreSQL Serverless with pgvector** (scales automatically, no cluster tuning) is the lowest-overhead design for a corpus **under 1 million** files, and the relational store handles the metadata filtering too.\n\n"
                       "**A** OpenSearch (domain sizing, shards, tuning) is more to run at this modest scale. **B** topic extraction isn't similarity search. **C** hosting a SageMaker sentence-transformer adds an endpoint to manage.",
        "reference": "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html",
        "note": "Answer derived. High confidence — the '< 1 million' clue points to pgvector; the 'least overhead' clue points to Serverless and a managed embedding model.",
    },
    {
        "id": 93, "category": D2, "task": "2.5", "type": "multi",
        "question": "A financial services company wants to use Amazon Bedrock foundation models (FMs) to analyze call center recordings. When calls end, the call center stores recordings as MP3 files in an Amazon S3 bucket. The company needs to generate summaries and sentiment analysis for the recordings in a structured format as soon as new files are created. The recordings average 20 MB in size.\n"
                    "Which combination of solutions will meet these requirements? (Choose two.)",
        "options": [
            "A. Use AWS Step Functions to orchestrate a workflow to process the recordings. Configure steps to invoke Amazon Transcribe to convert audio to text, validate job completion, and to invoke an AWS Lambda function to process the text by using Amazon Bedrock FMs to generate structured analysis output.",
            "B. Use AWS Step Functions to orchestrate a workflow to process the recordings. Configure steps to invoke Amazon Transcribe to convert audio to text, validate job completion, and to directly invoke Amazon Bedrock FMs to generate summaries and sentiment analysis in JSON format.",
            "C. Use AWS Step Functions to orchestrate a workflow to process the recordings. Configure steps to invoke Amazon Transcribe to convert audio to text, validate job completion, and to invoke an AWS Lambda function to create a prompt to invoke Amazon Bedrock FMs to generate structured analysis output.",
            "D. Configure the source S3 bucket to send events to Amazon EventBridge. Create an EventBridge rule to invoke the Step Functions workflow when an object is created in the bucket.",
            "E. Configure the source S3 bucket to send notifications to the Step Functions workflow when an object is created in the bucket.",
        ],
        "answer": [
                      'B. Use AWS Step Functions to orchestrate a workflow to process the recordings. Configure '
                      'steps to invoke Amazon Transcribe to convert audio to text, validate job completion, and to '
                      'directly invoke Amazon Bedrock FMs to generate summaries and sentiment analysis in JSON '
                      'format.',
                      'D. Configure the source S3 bucket to send events to Amazon EventBridge. Create an '
                      'EventBridge rule to invoke the Step Functions workflow when an object is created in the '
                      'bucket.',
                  ],
        "explanation": '**Trigger (D):** S3 event notifications cannot target Step Functions directly (so E is out),'
                       ' but S3 → **EventBridge** → rule → Step Functions works. **Processing (B):** Step Functions '
                       'orchestrates **Transcribe** (audio → text), checks that the job completed, then calls '
                       '**Amazon Bedrock directly** through its native Bedrock integration to produce the summary '
                       'and sentiment as **JSON** — no Lambda code to write or maintain.\\n'
                       '\\n'
                       '**A/C** put a Lambda function in the middle to call Bedrock, adding code and operational '
                       'overhead that the direct integration avoids (A and C are near-identical to each other).',
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html",
        "note": 'Answer changed to B + D to match the CertyIQ answer key (my first derivation was A + D). D '
                'is certain; among A/B/C the key picks the direct-integration (no Lambda) option.'
    },
    {
        "id": 94, "category": D3, "task": "3.2", "type": "single",
        "question": "A medical device company wants to feed reports of medical procedures that used the company's devices into an AI assistant. To protect patient privacy, the AI assistant must expose patient personally identifiable information (PII) only to surgeons. The AI assistant must redact PII for engineers. The AI assistant must reference only medical reports that are less than 3 years old.\n"
                    "The company stores reports in an Amazon S3 bucket as soon as each report is published. The company has already set up an Amazon Bedrock knowledge base. The AI assistant uses Amazon Cognito to authenticate users.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Enable Amazon Macie PII detection on the S3 bucket. Use an S3 trigger to invoke an AWS Lambda function that redacts PII from the reports. Configure the Lambda function to delete outdated documents from the bucket and to invoke knowledge base syncing.",
            "B. Invoke an AWS Lambda function to sync the S3 bucket and the knowledge base when a new report is uploaded to the bucket. Use a second Lambda function to invoke Amazon Comprehend to detect and redact PII if a user is part of the engineer Cognito user group. Set up an S3 Lifecycle configuration to remove reports that are older than 3 years from the bucket.",
            "C. Set up an S3 Lifecycle configuration on the bucket to remove reports that are older than 3 years. Schedule an AWS Lambda function to run daily syncs between the bucket and the knowledge base. When users interact with the AI assistant, call the ApplyGuardrail configuration that matches the user's Cognito user group to redact PII from the agent's responses if appropriate.",
            "D. Create a second knowledge base. Set up an S3 Lifecycle configuration on the bucket to remove reports that are older than 3 years. Invoke an AWS Lambda function that syncs the bucket with the original knowledge base when a new report is uploaded to the bucket. Use Amazon Comprehend to detect and redact PII before syncing the bucket with the second knowledge base. When a user interacts with the AI assistant, redirect the model to the appropriate knowledge base depending on the user's Cognito user group.",
        ],
        "answer": "C. Set up an S3 Lifecycle configuration on the bucket to remove reports that are older than 3 years. Schedule an AWS Lambda function to run daily syncs between the bucket and the knowledge base. When users interact with the AI assistant, call the ApplyGuardrail configuration that matches the user's Cognito user group to redact PII from the agent's responses if appropriate.",
        "explanation": "Three needs: **drop reports older than 3 years** → **S3 Lifecycle expiration** plus a **scheduled sync** so the knowledge base reflects the deletions; **PII exposed only to surgeons** → decide per user at response time with the **ApplyGuardrail API**, choosing the guardrail (PII masking) that matches the user's **Cognito group**, so one knowledge base serves both roles.\n\n"
                       "**A** Macie detects but doesn't redact, and a redacted copy would hide PII from surgeons too. **B** only removes reports from S3 (no KB sync for deletions) and its Comprehend step isn't wired to the response path. **D** maintains two knowledge bases and duplicate pipelines.",
        "reference": f"{_BR}/guardrails-use-independent-api.html",
        "note": "Answer derived, moderate-high confidence.",
    },
    {
        "id": 95, "category": D4, "task": "4.3", "type": "single",
        "question": "A large ecommerce company has deployed a foundation model (FM) to generate product descriptions. The company's engineering team monitors technical metrics such as token usage, latency, and error rates by using Amazon CloudWatch. The company's marketing team tracks business metrics such as conversion rates and revenue impact in its own systems.\n"
                    "The company needs a unified observability solution that correlates technical performance with business outcomes. The solution must provide automatic alerts to stakeholders when operational metrics indicate degradation. The solution must provide comprehensive visibility across both technical and business metrics.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Create CloudWatch dashboards that include technical metrics and imported business metrics. Configure CloudWatch composite alarms that combine technical data and business data. Use Amazon SNS to set up notifications to stakeholders.",
            "B. Use Amazon Managed Grafana to visualize technical metrics from CloudWatch with business metrics from external sources. Configure Amazon Managed Grafana alerts to invoke AWS Lambda functions. Configure the Lambda functions to remediate issues automatically when metrics exceed predefined thresholds.",
            "C. Stream CloudWatch metrics to Amazon S3 by using CloudWatch metric streams. Create Amazon QuickSight dashboards to visualize the combined technical metrics and business metrics. Set up Amazon EventBridge rules to send notifications to stakeholders when metrics exceed predefined thresholds.",
            "D. Configure CloudWatch custom dashboards that integrate operational metrics with imported business metrics. Set up CloudWatch composite alarms with anomaly detection. Use Amazon SNS to create alarm actions to notify stakeholders when correlated metrics indicate performance issues.",
        ],
        "answer": "D. Configure CloudWatch custom dashboards that integrate operational metrics with imported business metrics. Set up CloudWatch composite alarms with anomaly detection. Use Amazon SNS to create alarm actions to notify stakeholders when correlated metrics indicate performance issues.",
        "explanation": "Keep it in CloudWatch: import the business metrics as custom metrics so **technical and business data sit side by side**, use **composite alarms** to correlate several signals, add **anomaly detection** so 'degradation' is judged against a learned baseline rather than a static number, and notify stakeholders via **SNS** (exam-guide Skills 4.3.1, 4.3.3).\n\n"
                       "**A** is close but uses static thresholds without anomaly detection. **B** adds automatic remediation Lambdas the stem doesn't ask for and another service to run. **C** metric streams to S3 + QuickSight are for BI reporting, with no real-time operational alerting.",
        "reference": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Composite_Alarm.html",
        "note": "Answer derived. Moderate-high confidence (D vs A: anomaly detection).",
    },
    {
        "id": 96, "category": D2, "task": "2.3", "type": "single",
        "question": "A GenAI developer is evaluating Amazon Bedrock foundation models (FMs) to enhance a Europe-based company's internal business application. The company has a multi-account landing zone in AWS Control Tower. The company uses SCPs to allow its accounts to use only the eu-north-1 Region and the eu-west-1 Region. All customer data must remain in private networks within the approved AWS Regions.\n"
                    "The GenAI developer selects an FM based on analysis and testing and hosts the model in the eu-central-1 Region and the eu-west-3 Region. The GenAI developer must enable access to the FM for the company's employees. The GenAI developer must ensure that requests to the FM are private and remain with the same Regions as the FM.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Deploy an AWS Lambda function that is exposed by a private Amazon API Gateway REST API to a VPC in eu-north-1. Create a VPC endpoint for the selected FM in eu-central-1 and eu-west-3. Extend existing SCPs to allow employees to use the FM. Integrate the REST API with the business application.",
            "B. Deploy the FM on Amazon EC2 instances in eu-north-1. Deploy a private Amazon API Gateway REST API in front of the EC2 instances. Configure an Amazon Bedrock VPC endpoint. Integrate the REST API with the business application.",
            "C. Configure the FM to use cross-Region inference through an eu.amazon.* endpoint to ensure that all calls remain within Europe. Configure an Amazon Bedrock VPC endpoint. Extend existing SCPs to allow employees to use the FM through inference profiles in Europe-based Regions where the FM is available. Use an inference profile to integrate Amazon Bedrock with the business application.",
            "D. Deploy the FM in Amazon SageMaker AI in eu-north-1. Configure a SageMaker AI VPC endpoint. Extend existing SCPs to allow employees to use the SageMaker AI endpoint. Integrate the FM in SageMaker AI with the business application.",
        ],
        "answer": "C. Configure the FM to use cross-Region inference through an eu.amazon.* endpoint to ensure that all calls remain within Europe. Configure an Amazon Bedrock VPC endpoint. Extend existing SCPs to allow employees to use the FM through inference profiles in Europe-based Regions where the FM is available. Use an inference profile to integrate Amazon Bedrock with the business application.",
        "explanation": "A **geographic (`eu.`) cross-Region inference profile** routes only to Regions in Europe; a **Bedrock VPC endpoint (PrivateLink)** keeps the traffic on private networks; and the **SCPs must be extended** to allow the inference profile and its EU destination Regions (the existing SCP permits only eu-north-1 and eu-west-1, so it would otherwise deny the FM in eu-central-1/eu-west-3) — exactly the Q13 pattern.\n\n"
                       "**A** VPC endpoints are created for *services*, not 'for an FM' per Region. **B/D** self-hosting the FM on EC2 or SageMaker AI abandons Bedrock and the requirement to use the FM in the Regions selected.",
        "reference": f"{_BR}/cross-region-inference.html",
        "note": "Answer derived. High confidence — compare Q13 and Q71.",
    },
    {
        "id": 97, "category": D1, "task": "1.5", "type": "single",
        "question": "A healthcare company is developing an application to process medical queries. The application must answer complex queries with high accuracy by reducing semantic dilution. The application must refer to domain-specific terminology in medical documents to reduce ambiguity in medical terminology. The application must be able to respond to 1,000 queries each minute with response times less than 2 seconds.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Use Amazon API Gateway to route incoming queries to an Amazon Bedrock agent. Configure the agent to use an Anthropic Claude model to decompose queries and an Amazon Titan model to expand queries. Create an Amazon Bedrock knowledge base to store the reference medical documents.",
            "B. Configure an Amazon Bedrock knowledge base to store the reference medical documents. Enable query decomposition in the knowledge base. Configure an Amazon Bedrock flow that uses a foundation model (FM) and the knowledge base to support the application.",
            "C. Use Amazon SageMaker AI to host custom ML models for both query decomposition and query expansion. Configure Amazon Bedrock knowledge bases to store the reference medical documents. Encrypt the documents in the knowledge base.",
            "D. Create an Amazon Bedrock agent to orchestrate multiple AWS Lambda functions to decompose queries. Create an Amazon Bedrock knowledge base to store the reference medical documents. Use the agent's built-in knowledge base capabilities. Add deep research and reasoning capabilities to the agent to reduce ambiguity in the medical terminology.",
        ],
        "answer": "B. Configure an Amazon Bedrock knowledge base to store the reference medical documents. Enable query decomposition in the knowledge base. Configure an Amazon Bedrock flow that uses a foundation model (FM) and the knowledge base to support the application.",
        "explanation": "'Complex queries' diluted semantically → **query decomposition**: Knowledge Bases can **break a complex query into sub-queries** (an orchestration setting you simply enable), retrieving precise passages from the domain documents. A **Bedrock Flow** wires the FM and knowledge base together without code (exam-guide Skill 1.5.5). It avoids agent reasoning loops, which also protects the 2-second latency target at 1,000 queries/minute.\n\n"
                       "**A/D** agents add multi-step reasoning latency and orchestration (and D's 'deep research' can't meet 2 s). **C** self-hosting custom ML models is the highest overhead.",
        "reference": f"{_BR}/kb-test-config.html",
        "note": "Answer derived. High confidence — query decomposition is a built-in Knowledge Bases option (verified in the docs).",
    },
    {
        "id": 100, "category": D2, "task": "2.3", "type": "single",
        "question": "A company is creating a generative AI (GenAI) application that uses Amazon Bedrock foundation models (FMs). The application must use Microsoft Entra ID to authenticate. All FM API calls must stay on private network paths. Access to the application must be limited by department to specific model families. The company also needs a comprehensive audit trail of model interactions.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure SAML federation between Microsoft Entra ID and IAM. Create department-specific IAM roles that allow only the required ModelId values. Create AWS PrivateLink interface VPC endpoints for Amazon Bedrock runtime services. Enable AWS CloudTrail to capture Amazon Bedrock API calls. Configure Amazon Bedrock model invocation logging to record detailed model interactions.",
            "B. Create an identity provider (IdP) connection in IAM to authenticate by using Microsoft Entra ID. Assign department permission sets to control access to specific model families. Deploy AWS Lambda functions in private subnets with a NAT gateway for egress to Amazon Bedrock public endpoints. Enable CloudWatch Logs to capture model interactions for auditing purposes.",
            "C. Create a SAML identity provider (IdP) in IAM to authenticate by using Microsoft Entra ID. Use IAM permissions boundaries to limit department roles' access to specific model families. Configure public Amazon Bedrock API endpoints with VPC routing to maintain private network connectivity. Set up AWS CloudTrail with Amazon S3 Lifecycle rules to manage audit logs of model interactions.",
            "D. Configure OpenID Connect (OIDC) federation between Microsoft Entra ID and IAM. Use attribute-based access control to map department attributes to specific model access permissions. Apply SCP policies to restrict access to Amazon Bedrock FM families based on department. Use Microsoft Entra ID's built-in logging capabilities to maintain an audit trail of model interactions.",
        ],
        "answer": "A. Configure SAML federation between Microsoft Entra ID and IAM. Create department-specific IAM roles that allow only the required ModelId values. Create AWS PrivateLink interface VPC endpoints for Amazon Bedrock runtime services. Enable AWS CloudTrail to capture Amazon Bedrock API calls. Configure Amazon Bedrock model invocation logging to record detailed model interactions.",
        "explanation": "Each requirement has one fitting mechanism: **Entra ID authentication** → **SAML federation** to IAM; **department → model-family limits** → department IAM roles that allow only specific `ModelId` values; **private network paths** → **PrivateLink interface VPC endpoints** for Bedrock runtime; **audit** → **CloudTrail** (API calls) plus **model invocation logging** (prompts/responses).\n\n"
                       "**B** sends traffic through a NAT gateway to *public* endpoints. **C** 'public endpoints with VPC routing' is not private connectivity, and permissions boundaries alone don't grant access. **D** SCPs can't map per-department attributes, and Entra logs don't record model interactions.",
        "reference": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 101, "category": D3, "task": "3.2", "type": "single",
        "question": "A company wants to automatically detect personally identifiable information (PII) in documents stored in Amazon S3 before using those documents in a generative AI workflow.\n"
                    "Which AWS service is designed for discovering sensitive data in S3?",
        "options": [
            "A. Amazon Macie",
            "B. Amazon Route 53",
            "C. AWS CodeBuild",
            "D. Amazon EBS",
        ],
        "answer": "A. Amazon Macie",
        "explanation": "**Amazon Macie** discovers and classifies sensitive data — including PII — in **Amazon S3** (data at rest), so you can find and remediate sensitive records before the documents are ingested into a RAG pipeline (exam-guide Skill 3.2.2).\n\n"
                       "**B** Route 53 is DNS. **C** CodeBuild is a build service. **D** EBS is block storage. None of them analyse content. For *real-time* PII redaction or blocking during Amazon Bedrock inference, use **Bedrock Guardrails** (sensitive-information filters) instead — compare Q61 and Q94.",
        "reference": "https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html",
        "note": "Practice scenario supplied with the set, not a numbered official exam question. Easy service-recognition item: Macie = discover PII in S3 at rest; Guardrails = filter PII at inference time.",
    },
]
