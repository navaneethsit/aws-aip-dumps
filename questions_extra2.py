"""
AIP-C01 questions 51-75 (from screenshots; the source's suggested answers were hidden,
so every answer is derived from the exam guide + AWS docs and carries no vote data).

Same schema as questions.py. Q98 is missing from the source set and Q99 was an
AI Practitioner (AIF-C01) question, so neither is included.
"""

_BR = "https://docs.aws.amazon.com/bedrock/latest/userguide"
_MCP = "https://modelcontextprotocol.io/specification/2025-06-18/basic/transports"

D1 = "1 · FM Integration, Data & Compliance"
D2 = "2 · Implementation & Integration"
D3 = "3 · Safety, Security & Governance"
D4 = "4 · Operational Efficiency & Optimization"
D5 = "5 · Testing, Validation & Troubleshooting"

EXTRA2: list[dict] = [
    {
        "id": 51, "category": D4, "task": "4.1", "type": "single",
        "question": "A company uses Amazon Bedrock to develop an AI assistant to provide customer support. Analysis shows that 40% of customer queries use varied phrasing or wording to ask the same questions.\n"
                    "The company wants a solution to reduce redundant model calls. The solution must ensure that semantically equivalent questions receive consistent answers. The solution must ensure low latency.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Deploy an Amazon DynamoDB Accelerator (DAX) cluster as an in-memory cache. Specify the query text as the partition key and the model response text as the sort key. Query the cache by using a filter expression with the LIKE operator.",
            "B. Use Amazon Bedrock to generate embeddings from customer queries. Use Amazon MemoryDB for Valkey to store hash sets of vector embeddings and model responses. Use a RANGE query to find similar queries and their responses.",
            "C. Deploy Amazon OpenSearch Service that has k-nearest neighbor (k-NN) capabilities to store query-response text pairs. Use an approximate k-NN technique to find similar queries and their responses.",
            "D. Create a caching solution by using Amazon DynamoDB to create a global secondary index on the normalized query text. Apply stemming to incoming queries. Query the index of cached customer queries.",
        ],
        "answer": 'B. Use Amazon Bedrock to generate embeddings from customer queries. Use Amazon MemoryDB for '
                  'Valkey to store hash sets of vector embeddings and model responses. Use a RANGE query to '
                  'find similar queries and their responses.',
        "explanation": 'A **semantic cache** needs (1) an **embedding** of each incoming question and (2) a fast '
                       '**similarity lookup** over previously answered questions. B does both: Bedrock generates the'
                       ' embeddings, and **MemoryDB** keeps vectors and responses **in memory** (lowest latency) '
                       'with vector search; a **range (radius) query** returns cached questions within a similarity '
                       'threshold, so paraphrased questions get the same stored answer without a new model call '
                       '(exam-guide Skill 4.1.4).\\n'
                       '\\n'
                       '**A** DAX caches DynamoDB items by exact key; there is no LIKE/semantic matching. **C** '
                       'stores only *text* pairs and never creates embeddings, yet k-NN search needs vectors; a '
                       'disk-based OpenSearch domain is also slower than in-memory. **D** stemming catches spelling '
                       'variants, not paraphrases.',
        "reference": "https://docs.aws.amazon.com/memorydb/latest/devguide/vector-search-overview.html",
        "note": "Cross-check: changed back to B. CertyIQ's key says C, but C never generates embeddings (k-NN"
                " can't run on raw text pairs), while MemoryDB's in-memory vector search (which supports "
                'range queries) is the lower-latency semantic cache. Moderate confidence.'
    },
    {
        "id": 52, "category": D2, "task": "2.1", "type": "single",
        "question": "A company uses AWS Lambda functions to build an AI agent solution. A GenAI developer must set up a Model Context Protocol (MCP) server that accesses user information. The GenAI developer must also configure the AI agent to use the new MCP server. The GenAI developer must ensure that only authorized users can access the MCP server.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use a Lambda function to host the MCP server. Grant the AI agent Lambda functions permission to invoke the Lambda function that hosts the MCP server. Configure the AI agent's MCP client to invoke the MCP server asynchronously.",
            "B. Use a Lambda function to host the MCP server. Grant the AI agent Lambda functions permission to invoke the Lambda function that hosts the MCP server. Configure the AI agent to use the STDIO transport with the MCP server.",
            "C. Use a Lambda function to host the MCP server. Create an Amazon API Gateway HTTP API that proxies requests to the Lambda function. Configure the AI agent solution to use the Streamable HTTP transport to make requests through the HTTP API. Use Amazon Cognito to enforce OAuth 2.1.",
            "D. Use a Lambda layer to host the MCP server. Add the Lambda layer to the AI agent Lambda functions. Configure the agentic AI solution to use the STDIO transport to send requests to the MCP server. In the AI agent's MCP configuration, specify the Lambda layer ARN as the command. Specify the user credentials as environment variables.",
        ],
        "answer": "C. Use a Lambda function to host the MCP server. Create an Amazon API Gateway HTTP API that proxies requests to the Lambda function. Configure the AI agent solution to use the Streamable HTTP transport to make requests through the HTTP API. Use Amazon Cognito to enforce OAuth 2.1.",
        "explanation": "A remote MCP server needs a **network transport** — MCP's **Streamable HTTP** — and the MCP authorization model is **OAuth 2.1**. Lambda behind **API Gateway HTTP API** exposes that endpoint, and **Cognito** issues/validates the OAuth tokens so only authorized users reach it (exam-guide Skill 2.1.7: Lambda-hosted stateless MCP servers).\n\n"
                       "**A** has no MCP transport and no user authorization (only IAM between functions). **B/D** STDIO is for local subprocess servers on the same machine — it cannot talk to a remote Lambda, and putting credentials in environment variables is insecure.",
        "reference": _MCP,
        "note": "Answer derived. High confidence — see also Q75 (same pattern).",
    },
    {
        "id": 53, "category": D2, "task": "2.1", "type": "single",
        "question": "A company wants to create an annual rewards program for its customers. The rewards that customers earn vary based on different parameters such as the categories of the items ordered and the customers' purchase history.\n"
                    "The company needs a generative AI (GenAI) solution that uses three Amazon Bedrock agents to help customers during online catalog browsing. The agents must use knowledge bases and action groups to handle the search, recommendation, and order modules. The modules must operate sequentially. An AWS Lambda function must calculate estimated rewards for each recommended item. The solution must provide graceful degradation during service disruptions.\n"
                    "Which solution will meet these requirements with the MOST operational efficiency?",
        "options": [
            "A. Define an Amazon API Gateway REST API behind each agent. Create a second Lambda function to orchestrate the calls to the agents and the rewards Lambda function. Configure the second Lambda function with a retry/fallback mechanism.",
            "B. Create an AWS Step Functions state machine with four tasks that run the agents and the rewards Lambda function. Set up retry and catch branches for each of the task steps.",
            "C. Configure each agent with a separate retry/fallback mechanism. Create a second Lambda function to orchestrate the calls to the agents and the rewards Lambda function. Define an Amazon API Gateway REST API behind the second Lambda function.",
            "D. Create a second Lambda function to orchestrate the calls to the agents and the rewards Lambda function. Create an AWS Step Functions state machine with one task that runs the second Lambda function. Set up retry and catch branches for the task step.",
        ],
        "answer": "B. Create an AWS Step Functions state machine with four tasks that run the agents and the rewards Lambda function. Set up retry and catch branches for each of the task steps.",
        "explanation": "Sequential modules + graceful degradation = a **Step Functions state machine** with one task per step (three agents + the rewards Lambda) and **Retry/Catch per task**, so a failure in one module can fall back or degrade without custom orchestration code (exam-guide Skills 1.2.3, 2.1.2). It's declarative and gives per-step visibility.\n\n"
                       "**A/C** hand-write the orchestration in a Lambda and add pointless API Gateway layers. **D** wraps all steps in a single Lambda task, so Step Functions can only retry/catch the whole thing — no per-step degradation, and you still maintain the orchestration code.",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 54, "category": D2, "task": "2.5", "type": "single",
        "question": "A company is creating a workflow to review customer-facing communications before the company sends the communications. The company uses a pre-defined message template to generate the communications and stores the communications in an Amazon S3 bucket. The workflow needs to capture a specific portion from the template and send it to an Amazon Bedrock model. The workflow must store model responses back to the original S3 bucket.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Create a flow in Amazon Bedrock Flows. Configure S3 action nodes at the beginning and end of the flow to retrieve and store the communications and the model responses. In the middle of the flow, configure an expression to parse each communication. Configure an agent step to send the parsed input to the model for review.",
            "B. Create an AWS Step Functions Express workflow state machine. Use an Amazon S3 integration GetObject step to retrieve the original communications. Use an intrinsic function Pass step to parse the communications and to pass the results to an Amazon Bedrock InvokeModel step. Configure an Amazon S3 integration PutObject step to store the model responses back to the S3 bucket.",
            "C. Create an Amazon Bedrock agent that has an action group. Configure instructions to define how the agent should parse the communications. Configure the action group to retrieve the communications from the S3 bucket, invoke the Amazon Bedrock model, and store the model responses back to the S3 bucket.",
            "D. Create an Amazon Bedrock agent that has a single action group. Configure three AWS Lambda functions in the action group. Configure the functions to retrieve the communications from the S3 bucket, parse the communications and invoke the Amazon Bedrock model, and store the model responses back to the S3 bucket.",
        ],
        "answer": "B. Create an AWS Step Functions Express workflow state machine. Use an Amazon S3 integration GetObject step to retrieve the original communications. Use an intrinsic function Pass step to parse the communications and to pass the results to an Amazon Bedrock InvokeModel step. Configure an Amazon S3 integration PutObject step to store the model responses back to the S3 bucket.",
        "explanation": "This is a **deterministic pipeline** (read → extract a fixed part of a template → call a model → write back). Step Functions covers every step with native SDK/optimized integrations — S3 `GetObject`/`PutObject`, **intrinsic functions** to slice the template, and Bedrock `InvokeModel` — with no code and no LLM 'reasoning' in the control path.\n\n"
                       "**C/D** an *agent* is for open-ended, model-driven tool use; using it (plus Lambdas) for a fixed sequence adds non-determinism and code. **A** Flows does have S3 storage/retrieval nodes, but the option routes the parsed input through an *agent* node instead of a prompt node, and uses expressions for template parsing — a poorer fit than Step Functions' intrinsic functions.",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/connect-bedrock.html",
        "note": "Answer derived, moderate-high confidence (B vs A). Bedrock Flows *does* have S3 storage and retrieval nodes (verified in the docs), so A isn't impossible — but its agent step is the wrong building block for a fixed pipeline.",
    },
    {
        "id": 55, "category": D5, "task": "5.1", "type": "single",
        "question": "A financial technology company is using Amazon Bedrock to build an assessment system for the company's customer service AI assistant. The AI assistant must provide financial recommendations that are factually accurate, compliant with financial regulations, and conversationally appropriate. The company needs to combine automated quality evaluations at scale with targeted human reviews of critical interactions.\n"
                    "What solution will meet these requirements?",
        "options": [
            "A. Configure a pipeline in which financial experts manually score all responses for accuracy, compliance, and conversational quality. Use Amazon SageMaker notebooks to analyze results to identify improvement areas.",
            "B. Configure Amazon Bedrock evaluations that use Anthropic Claude Sonnet as a judge model to assess response accuracy and appropriateness. Configure custom Amazon Bedrock guardrails to check responses for compliance with financial policies. Add Amazon Augmented AI (Amazon A2I) human reviews for flagged critical interactions.",
            "C. Create an Amazon Lex bot to manage the customer service interactions. Configure AWS Lambda functions to check responses against a static compliance database. Configure intents in the bot that call the Lambda functions to check the responses. Add an additional intent to collect end-user reviews.",
            "D. Configure Amazon CloudWatch to monitor response patterns from the AI assistant. Configure CloudWatch alerts for potential compliance violations. Establish a team of human evaluators to review flagged interactions.",
        ],
        "answer": "B. Configure Amazon Bedrock evaluations that use Anthropic Claude Sonnet as a judge model to assess response accuracy and appropriateness. Configure custom Amazon Bedrock guardrails to check responses for compliance with financial policies. Add Amazon Augmented AI (Amazon A2I) human reviews for flagged critical interactions.",
        "explanation": "'Automated evaluation **at scale** + **targeted** human review' = **LLM-as-a-judge** (Bedrock evaluations) for the bulk, **Guardrails** for policy compliance, and **Amazon A2I** to route only flagged critical interactions to humans (exam-guide Skills 5.1.3/5.1.5, 3.4.3).\n\n"
                       "**A** is fully manual (no scale). **C** a Lex bot with a static database isn't an evaluation system. **D** CloudWatch can't judge answer accuracy, so there's nothing meaningful to alert on.",
        "reference": f"{_BR}/model-evaluation-metrics.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 56, "category": D2, "task": "2.1", "type": "single",
        "question": "A healthcare company is using Amazon Bedrock to develop a real-time patient care AI assistant to respond to queries for separate departments that handle clinical inquiries, insurance verification, appointment scheduling, and insurance claims. The company wants to use a multi-agent architecture.\n"
                    "The company must ensure that the AI assistant is scalable and can onboard new features for patients. The AI assistant must be able to handle thousands of parallel patient interactions. The company must ensure that patients receive appropriate domain-specific responses to queries.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Isolate data for each agent by using separate knowledge bases. Use IAM filtering to control access to each knowledge base. Deploy a supervisor agent to perform natural language intent classification on patient inquiries. Configure the supervisor agent to route queries to specialized collaborator agents to respond to department-specific queries. Configure each specialized collaborator agent to use Retrieval Augmented Generation (RAG) with the agent's department-specific knowledge base.",
            "B. Create a separate supervisor agent for each department. Configure individual collaborator agents to perform natural language intent classification for each specialty domain within each department. Integrate each collaborator agent with department-specific knowledge bases only. Implement manual handoff processes between the supervisor agents.",
            "C. Isolate data for each department in separate knowledge bases. Use IAM filtering to control access to each knowledge base. Deploy a single general-purpose agent. Configure multiple action groups within the general-purpose agent to perform specific department functions. Implement rule-based routing logic within the general-purpose agent instructions.",
            "D. Implement multiple independent supervisor agents that run in parallel to respond to patient inquiries for each department. Configure multiple collaborator agents for each supervisor agent. Integrate all agents with the same knowledge base. Use external routing logic to merge responses from multiple supervisor agents.",
        ],
        "answer": "A. Isolate data for each agent by using separate knowledge bases. Use IAM filtering to control access to each knowledge base. Deploy a supervisor agent to perform natural language intent classification on patient inquiries. Configure the supervisor agent to route queries to specialized collaborator agents to respond to department-specific queries. Configure each specialized collaborator agent to use Retrieval Augmented Generation (RAG) with the agent's department-specific knowledge base.",
        "explanation": "This is exactly **Bedrock multi-agent collaboration**: one **supervisor** classifies intent and routes to **specialised collaborator agents**, each grounded in its own department **knowledge base**. New departments/features are onboarded by adding a collaborator, and the managed service handles parallel sessions.\n\n"
                       "**B** multiple supervisors and manual handoffs defeat the pattern. **C** one general agent with rule-based routing is brittle and doesn't scale as capabilities grow. **D** parallel independent supervisors sharing a single knowledge base lose domain isolation and need external merging logic.",
        "reference": f"{_BR}/agents-multi-agent-collaboration.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 57, "category": D2, "task": "2.3", "type": "single",
        "question": "A company uses an AI assistant application to summarize the company's website content and provide information to customers. The company plans to use Amazon Bedrock to give the application access to a foundation model (FM).\n"
                    "The company needs to deploy the AI assistant application to a development environment and a production environment. The solution must integrate the environments with the FM. The company wants to test the effectiveness of various FMs in each environment. The solution must provide product owners with the ability to easily switch between FMs for testing purposes in each environment.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Create one AWS CDK application. Create multiple pipelines in AWS CodePipeline. Configure each pipeline to have its own settings for each FM. Configure the application to invoke the Amazon Bedrock FMs by using the aws_bedrock.ProvisionedModel.fromProvisionedModelArn() method.",
            "B. Create a separate AWS CDK application for each environment. Configure the applications to invoke the Amazon Bedrock FMs by using the aws_bedrock.FoundationModel.fromFoundationModelId() method. Create a separate pipeline in AWS CodePipeline for each environment.",
            "C. Create one AWS CDK application. Configure the application to invoke the Amazon Bedrock FMs by using the aws_bedrock.FoundationModel.fromFoundationModelId() method. Create a pipeline in AWS CodePipeline pipeline that has a deployment stage for each environment that uses AWS CodeBuild deploy actions.",
            "D. Create an AWS CDK application for the production environment. Configure the application to invoke the Amazon Bedrock FMs by using the aws_bedrock.ProvisionedModel.fromProvisionedModelArn() method. Create a pipeline in AWS CodePipeline. Configure the pipeline to deploy to the production environment by using an AWS CodeBuild deploy action. For the development environment, manually recreate the resources by referring to the production application code.",
        ],
        "answer": "C. Create one AWS CDK application. Configure the application to invoke the Amazon Bedrock FMs by using the aws_bedrock.FoundationModel.fromFoundationModelId() method. Create a pipeline in AWS CodePipeline pipeline that has a deployment stage for each environment that uses AWS CodeBuild deploy actions.",
        "explanation": "**One CDK app, one pipeline with a stage per environment** keeps dev and prod consistent (same code, per-stage config), and `FoundationModel.fromFoundationModelId()` lets you reference any on-demand FM by ID so owners can switch models by changing configuration — ideal for testing different FMs.\n\n"
                       "**A/D** `ProvisionedModel.fromProvisionedModelArn()` binds to a purchased Provisioned Throughput model — costly and rigid for *testing* many FMs; D also hand-recreates dev. **B** separate CDK apps and pipelines per environment cause drift and duplicate maintenance.",
        "reference": "https://docs.aws.amazon.com/cdk/v2/guide/stages.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 58, "category": D1, "task": "1.4", "type": "single",
        "question": "A hotel company wants to enhance a legacy Java-based property management system (PMS) by adding AI capabilities. The company wants to use Amazon Bedrock Knowledge Bases to provide staff with room availability information and hotel-specific details. The solution must maintain separate access controls for each hotel that the company manages. The solution must provide room availability information in near real time and must maintain consistent performance during peak usage periods.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Deploy a single Amazon Bedrock knowledge base that contains combined data for all hotels. Configure AWS Lambda functions to synchronize data from each hotel's PMS database through direct API connections. Implement AWS CloudTrail logging with hotel-specific filters to audit access logs for each hotel's data.",
            "B. Create an Amazon EventBridge rule for each hotel that is invoked by changes to the PMS database for each hotel. Configure the rule to send updates to a centralized Amazon Bedrock knowledge base in a management AWS account. Configure resource-based policies to enforce hotel-specific access controls for hotel staff.",
            "C. Implement one Amazon Bedrock knowledge base for each hotel in a multi-account structure. Use direct data ingestion to provide real-time room availability information. Schedule regular synchronization for less critical information.",
            "D. Build a centralized Amazon Bedrock agent that uses multiple knowledge bases. Implement AWS IAM Identity Center with hotel-specific permission sets to control hotel staff data access.",
        ],
        "answer": "C. Implement one Amazon Bedrock knowledge base for each hotel in a multi-account structure. Use direct data ingestion to provide real-time room availability information. Schedule regular synchronization for less critical information.",
        "explanation": "Strong isolation = **one knowledge base per hotel** (separate accounts make access boundaries simple and keep each hotel's load independent for consistent performance). **Near-real-time** availability = Knowledge Bases **direct ingestion** (ingest changes via API immediately), while slower-changing details use scheduled data-source sync — a tiered freshness design (exam-guide Skill 1.4.5).\n\n"
                       "**A** one shared KB can't give per-hotel access control (CloudTrail filters only audit). **B** knowledge bases don't use resource-based policies for per-tenant data access, and a central KB again mixes tenants. **D** a central agent over many KBs adds a routing layer and doesn't address near-real-time ingestion.",
        "reference": f"{_BR}/kb-direct-ingestion.html",
        "note": "Answer derived, moderate confidence — C is the only option pairing per-hotel isolation with direct ingestion for freshness.",
    },
    {
        "id": 59, "category": D1, "task": "1.2", "type": "single",
        "question": "A company is implementing a serverless inference API by using AWS Lambda. The API will dynamically invoke multiple AI models hosted on Amazon Bedrock. The company needs to design a solution that can switch between model providers without modifying or redeploying Lambda code in real time. The design must include safe rollout of configuration changes and validation and rollback capabilities.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Store the active model provider in AWS Systems Manager Parameter Store. Configure a Lambda function to read the parameter at runtime to determine which model to invoke.",
            "B. Store the active model provider in AWS AppConfig. Configure a Lambda function to read the configuration at runtime to determine which model to invoke.",
            "C. Configure an Amazon API Gateway REST API to route requests to separate Lambda functions. Hardcode each Lambda function to a specific model provider. Switch the integration target manually.",
            "D. Store the active model provider in a JSON file hosted on Amazon S3. Use AWS AppConfig to reference the S3 file as a hosted configuration source. Configure a Lambda function to read the file through AppConfig at runtime to determine which model to invoke.",
        ],
        "answer": "B. Store the active model provider in AWS AppConfig. Configure a Lambda function to read the configuration at runtime to determine which model to invoke.",
        "explanation": "**Runtime configuration + safe rollout + validation + rollback** is AppConfig's purpose: deployment strategies (gradual rollout, bake time), **validators** (JSON schema / Lambda), and **automatic rollback** on CloudWatch alarms. Keeping the model choice in an AppConfig profile means no code change or redeploy (exam-guide Skill 1.2.2).\n\n"
                       "**A** Parameter Store has no staged rollout, validation or rollback. **C** is manual and hardcoded. **D** works, but adds an S3 hop for no benefit — AppConfig already hosts configuration data natively.",
        "reference": "https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html",
        "note": "Answer derived. High confidence — cf. Q4 and Q49.",
    },
    {
        "id": 60, "category": D2, "task": "2.4", "type": "single",
        "question": "A company is building a generative AI (GenAI) application that uses Amazon Bedrock APIs to process complex customer inquiries. During peak usage periods, the application experiences intermittent API timeouts that cause issues such as broken response chunks and delayed data delivery. The application struggles to ensure that prompts remain within token limits when handling complex customer inquiries of varying lengths. Users have reported truncated inputs and incomplete responses. The company has also observed foundation model (FM) invocation failures.\n"
                    "The company needs a retry strategy that automatically handles transient service errors and prevents overwhelming Amazon Bedrock during peak usage periods. The strategy must also adapt to changing service availability and support response streaming and token-aware request handling.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Implement a standard retry strategy that uses a 1-second fixed delay between attempts and a 3-retry maximum for all errors. Handle streaming response timeouts by restarting streams. Cap token usage for each session.",
            "B. Implement an adaptive retry strategy that uses exponential backoff with jitter and a circuit breaker pattern that temporarily disables retries when error rates exceed a predefined threshold. Implement a streaming response handler that monitors for chunk delivery timeouts. Configure the handler to buffer successfully received chunks and intelligently resume streaming from the last received chunk when connections are re-established.",
            "C. Use the AWS SDK to configure a retry strategy in standard mode. Wrap Amazon Bedrock API calls in try-catch blocks that handle timeout exceptions. Return cached completions for failed streaming requests. Enforce a global token limit for all users. Add jitter-based retry logic and lightweight token trimming for each request. Resume broken streams by requesting only the missing chunks from the point of failure. Maintain a small in-memory buffer of the most recent chunks to minimize redundant data transfer.",
            "D. Set Amazon Bedrock client request timeouts to 30 seconds. Implement client-side load shedding. Buffer partial results and stop new requests when the application performance begins to degrade. Set static token usage caps for all requests. Configure exponential backoff retries, dynamic chunk sizing, and context-aware token limits.",
        ],
        "answer": "B. Implement an adaptive retry strategy that uses exponential backoff with jitter and a circuit breaker pattern that temporarily disables retries when error rates exceed a predefined threshold. Implement a streaming response handler that monitors for chunk delivery timeouts. Configure the handler to buffer successfully received chunks and intelligently resume streaming from the last received chunk when connections are re-established.",
        "explanation": "Match each stated need: **'transient errors' + 'don't overwhelm Bedrock' + 'adapt to availability'** → exponential backoff **with jitter** plus a **circuit breaker** that stops retries when errors spike; **'response streaming'** → a stream handler that detects chunk timeouts and **buffers/resumes** instead of restarting (exam-guide Skill 2.4.3).\n\n"
                       "**A** fixed delay and fixed retries cause retry storms and restart streams. **C** claims to 'resume by requesting missing chunks', which Bedrock streaming APIs can't do, and a global token limit hurts users. **D** static caps and client-side load shedding aren't adaptive retry handling.",
        "reference": "https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html",
        "note": "Answer derived. Moderate-high confidence — B is the only option that is adaptive (backoff+jitter+circuit breaker) and handles streaming recovery.",
    },
    {
        "id": 61, "category": D3, "task": "3.2", "type": "single",
        "question": "A bank is developing a generative AI (GenAI)-powered AI assistant that uses Amazon Bedrock to assist the bank's website users with account inquiries and financial guidance. The bank must ensure that the AI assistant does not reveal any personally identifiable information (PII) in customer interactions.\n"
                    "The AI assistant must not send PII in prompts to the GenAI model. The AI assistant must not respond to customer requests to provide investment advice. The bank must collect audit logs of all customer interactions, including any images or documents that are transmitted during customer interactions.\n"
                    "Which solution will meet these requirements with the LEAST operational effort?",
        "options": [
            "A. Use Amazon Macie to detect and redact PII in user inputs and in the model responses. Apply prompt engineering techniques to force the model to avoid investment advice topics. Use AWS CloudTrail to capture conversation logs.",
            "B. Use an AWS Lambda function and Amazon Comprehend to detect and redact PII. Use Amazon Comprehend topic modeling to prevent the AI assistant from discussing investment advice topics. Set up custom metrics in Amazon CloudWatch to capture customer conversations.",
            "C. Configure Amazon Bedrock guardrails to apply a sensitive information policy to detect and filter PII. Set up a topic policy to ensure that the AI assistant avoids investment advice topics. Use the Converse API to log model invocations. Enable delivery and image logging to Amazon S3.",
            "D. Use regex controls to match patterns for PII. Apply prompt engineering techniques to avoid returning PII or investment advice topics to customers. Enable model invocation logging, delivery logging, and image logging to Amazon S3.",
        ],
        "answer": "C. Configure Amazon Bedrock guardrails to apply a sensitive information policy to detect and filter PII. Set up a topic policy to ensure that the AI assistant avoids investment advice topics. Use the Converse API to log model invocations. Enable delivery and image logging to Amazon S3.",
        "explanation": "Everything has a native Bedrock control: **sensitive-information policy** (PII is detected on the *input* before it reaches the model and filtered from outputs), a **denied-topic policy** for investment advice, and **model invocation logging** with S3 delivery and **image/data logging** for the audit trail of prompts, responses and attachments.\n\n"
                       "**A** Macie scans data at rest in S3 — not live prompts — and prompt engineering can't reliably block topics; CloudTrail doesn't capture prompt content. **B** topic *modeling* isn't a blocking control and CloudWatch metrics aren't a conversation log. **D** regex and prompt engineering are brittle and custom.",
        "reference": f"{_BR}/model-invocation-logging.html",
        "note": "Answer derived. High confidence. (Option C's 'use the Converse API to log' is loosely worded — logging is enabled in Bedrock's invocation-logging settings.)",
    },
    {
        "id": 62, "category": D3, "task": "3.4", "type": "single",
        "question": "A financial services company is developing a customer service AI assistant application that uses a foundation model (FM) in Amazon Bedrock. The application must provide transparent responses by documenting reasoning and by citing sources that are used for Retrieval Augmented Generation (RAG). The application must capture comprehensive audit trails for all responses to users. The application must be able to serve up to 10,000 concurrent users and must respond to each customer inquiry within 2 seconds.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Enable tracing for Amazon Bedrock agents. Configure structured prompts that direct the FM to provide evidence presentations. Integrate Amazon Bedrock knowledge bases with data sources to enable RAG. Configure the application to reference and cite authoritative content. Deploy the application in a Multi-AZ architecture. Use Amazon API Gateway and AWS Lambda functions to scale the application. Use Amazon CloudFront to provide low-latency delivery.",
            "B. Enable tracing for Amazon Bedrock agents. Integrate a custom RAG pipeline with Amazon OpenSearch Service to retrieve and cite sources. Configure structured prompts to present retrieved evidence. Deploy the application behind an Amazon API Gateway REST API. Use AWS Lambda functions and Amazon CloudFront to scale the application and to provide low latency. Store logs in Amazon S3 and use AWS CloudTrail to capture audit trails.",
            "C. Use Amazon CloudWatch to monitor latency and error rates. Embed model prompts directly in the application backend to cite sources. Store application interactions with users in Amazon RDS for audits.",
            "D. Store generated responses and supporting evidence in an Amazon S3 bucket. Enable versioning on the bucket for audits. Use AWS Glue to catalog retrieved documents. Process the retrieved documents in Amazon Athena to generate periodic compliance reports.",
        ],
        "answer": "A. Enable tracing for Amazon Bedrock agents. Configure structured prompts that direct the FM to provide evidence presentations. Integrate Amazon Bedrock knowledge bases with data sources to enable RAG. Configure the application to reference and cite authoritative content. Deploy the application in a Multi-AZ architecture. Use Amazon API Gateway and AWS Lambda functions to scale the application. Use Amazon CloudFront to provide low-latency delivery.",
        "explanation": "Maps to exam-guide Skill 3.4.1: **agent tracing** for reasoning traces, **evidence presentation / source attribution** via **Knowledge Bases** (managed RAG with citations), plus a scalable serverless front end (API Gateway + Lambda, Multi-AZ, CloudFront) for 10,000 concurrent users.\n\n"
                       "**B** builds a *custom* RAG pipeline on OpenSearch (more overhead). **C** has no reasoning transparency or RAG. **D** produces periodic reports, not per-response transparency or real-time serving.",
        "reference": f"{_BR}/trace-events.html",
        "note": "Answer derived. High confidence (A vs B differ in managed vs custom RAG).",
    },
    {
        "id": 63, "category": D1, "task": "1.4", "type": "single",
        "question": "A healthcare company is developing a document management system that stores medical research papers in an Amazon S3 bucket. The company needs to build a comprehensive metadata framework that will improve search precision for a generative AI (GenAI) application that analyzes the research papers. The metadata framework must include document timestamps, author information, and research domain classifications.\n"
                    "The solution must maintain a consistent metadata structure across all uploaded documents. The solution must give foundation models (FMs) the ability to understand document context without accessing the full content.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Store document timestamps in Amazon S3 system metadata. Use S3 object tags to implement domain classification. Implement custom user-defined metadata to store author information.",
            "B. Set up S3 Object Lock with legal holds to track document timestamps. Use S3 object tags to store author information. Implement S3 access points for domain classification.",
            "C. Use S3 Inventory reports to track document timestamps. Create S3 access points to implement domain classification. Store author information in S3 Storage Lens dashboards.",
            "D. Use custom user-defined metadata to store author information. Use S3 Object Lock retention periods to track document timestamps. Use S3 Event Notifications to implement domain classification.",
        ],
        "answer": "A. Store document timestamps in Amazon S3 system metadata. Use S3 object tags to implement domain classification. Implement custom user-defined metadata to store author information.",
        "explanation": "This is the exam guide's own example (Skill 1.4.2): **S3 object (system) metadata for timestamps** (e.g. Last-Modified), **custom user-defined metadata for authorship**, and **object tags for domain classification**. Metadata travels with each object, so the retrieval layer can filter and give FMs context without reading the full document.\n\n"
                       "**B/C/D** misuse unrelated S3 features — Object Lock (retention/legal hold), access points (network/access control), Inventory/Storage Lens (reporting), and Event Notifications (triggers) are not metadata/classification mechanisms.",
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 64, "category": D1, "task": "1.4", "type": "single",
        "question": "Example Corp provides a personalized video generation service that millions of enterprise customers use. Customers generate marketing videos by submitting prompts to the company's proprietary generative AI (GenAI) model. To improve output relevance and personalization, Example Corp wants to enhance the prompts by using customer-specific context such as product preferences, customer attributes, and business history.\n"
                    "The customers have strict data governance requirements. The customers must retain full ownership and control over their own data. The customers do not require real-time access. However, semantic accuracy must be high and retrieval latency must remain low to support customer experience use cases.\n"
                    "Example Corp wants to minimize architectural complexity in its integration pattern. Example Corp does not want to deploy and manage services in each customer's environment unless necessary.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Ensure that each customer sets up an Amazon Q Business index that includes the customer's internal data. Ensure that each customer designates Example Corp as a data accessor to allow Example Corp to retrieve relevant content by using a secure API to enrich prompts at runtime.",
            "B. Use federated search with Model Context Protocol (MCP) by deploying real-time MCP servers for each customer. Retrieve data in real time during prompt generation.",
            "C. Ensure that each customer configures an Amazon Bedrock knowledge base. Allow cross-account querying so Example Corp can retrieve structured data for prompt augmentation.",
            "D. Configure Amazon Kendra to crawl customer data sources. Share the resulting indexes across accounts so Example Corp can query each customer's Amazon Kendra index to retrieve augmentation data.",
        ],
        "answer": "A. Ensure that each customer sets up an Amazon Q Business index that includes the customer's internal data. Ensure that each customer designates Example Corp as a data accessor to allow Example Corp to retrieve relevant content by using a secure API to enrich prompts at runtime.",
        "explanation": "This is the **Amazon Q index for ISVs** pattern: the customer builds an Amazon Q Business index over its own data and adds the ISV as a **data accessor**; the ISV calls a secure retrieval API (`SearchRelevantContent`) cross-account. The customer **retains ownership and control** (it can scope or revoke access, and ACLs are honoured), the ISV deploys **nothing** in the customer environment, and semantic retrieval is built in.\n\n"
                       "**B** real-time MCP servers per customer means deploying and running infrastructure in every environment (and real-time isn't needed). **C** Bedrock knowledge bases have no cross-account query/sharing model of this kind. **D** Kendra indexes can't be shared across accounts for third-party querying this way.",
        "reference": "https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/isv.html",
        "note": 'Answer derived, moderate confidence; the data-accessor mechanism itself is verified in the '
                'Amazon Q Business ISV docs. (Q Business is closed to new customers, but the exam guide still'
                ' lists it.) CertyIQ key says C (customer-owned Bedrock knowledge base with cross-account '
                'querying). Kept A: it is the documented Amazon Q index for ISVs pattern (customer owns the '
                'index; the ISV is a data accessor). If the real exam follows the key, C is the alternative. '
                "Cross-check: the second dump's key also says A, so it is two sources (bank + second dump) "
                "against CertyIQ's C."
    },
    {
        "id": 65, "category": D1, "task": "1.5", "type": "single",
        "question": "A company is building a legal research AI assistant that uses Amazon Bedrock with an Anthropic Claude foundation model (FM). The AI assistant must retrieve highly relevant case law documents to augment the FM's responses. The AI assistant must identify semantic relationships between legal concepts, specific legal terminology, and citations. The AI assistant must perform quickly and return precise results.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure an Amazon Bedrock knowledge base to use a default vector search configuration. Use Amazon Bedrock to expand queries to improve retrieval for legal documents based on specific terminology and citations.",
            "B. Use Amazon OpenSearch service to deploy a hybrid search architecture that combines vector search with keyword search. Apply an Amazon Bedrock reranker model to optimize result relevance.",
            "C. Enable the Amazon Kendra query suggestion feature for end users. Use Amazon Bedrock to perform post-processing of search results to identify semantic similarity in the documents and to produce precise results.",
            "D. Use Amazon OpenSearch Service with vector search and Amazon Bedrock Titan embeddings to index and search legal documents. Use custom AWS Lambda functions to merge results with keyword-based filters that are stored in an Amazon RDS database.",
        ],
        "answer": "B. Use Amazon OpenSearch service to deploy a hybrid search architecture that combines vector search with keyword search. Apply an Amazon Bedrock reranker model to optimize result relevance.",
        "explanation": "Semantic relationships need **vectors**; **exact legal terms and citations** need **keyword** matching → **hybrid search**. A **reranker model** then reorders the top candidates for precision. This is exam-guide Skill 1.5.4 (hybrid search + Bedrock reranker models).\n\n"
                       "**A** default vector-only retrieval misses exact citations. **C** query *suggestions* don't improve retrieval and Bedrock post-processing adds latency. **D** hand-merging with Lambda and an RDS keyword store is custom, slower and harder to maintain.",
        "reference": f"{_BR}/rerank.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 66, "category": D4, "task": "4.3", "type": "multi",
        "question": "A company deploys multiple Amazon Bedrock based generative AI (GenAI) applications across multiple business units for customer service, content generation, and document analysis. Some applications show unpredictable token usage patterns. The company requires a comprehensive observability solution that provides real-time visibility into token usage patterns across multiple models. The observability solution must support custom dashboards for multiple stakeholder groups and provide alerting capabilities for token consumption across all the foundational models that the company's applications use.\n"
                    "Which combination of solutions will meet these requirements with the LEAST operational overhead? (Choose two.)",
        "options": [
            "A. Use Amazon CloudWatch metrics as data sources to create custom Amazon QuickSight dashboards that show token usage trends and usage patterns across FMs.",
            "B. Use Amazon CloudWatch Logs Insights to analyze Amazon Bedrock invocation logs for token consumption patterns and usage attribution by application. Create custom queries to identify high-usage scenarios. Add log widgets to dashboards to enable continuous monitoring.",
            "C. Create custom Amazon CloudWatch dashboards that combine native Amazon Bedrock token and invocation CloudWatch metrics. Set up CloudWatch alarms to monitor token usage thresholds.",
            "D. Create dashboards that show token usage trends and patterns across the company's FMs by using an Amazon Bedrock zero-ETL integration with Amazon Managed Grafana.",
            "E. Implement Amazon EventBridge rules to capture Amazon Bedrock model invocation events. Route token usage data to an Amazon Data Firehose delivery stream that targets Amazon OpenSearch Serverless. Use OpenSearch dashboards to analyze usage patterns.",
        ],
        "answer": [
            "B. Use Amazon CloudWatch Logs Insights to analyze Amazon Bedrock invocation logs for token consumption patterns and usage attribution by application. Create custom queries to identify high-usage scenarios. Add log widgets to dashboards to enable continuous monitoring.",
            "C. Create custom Amazon CloudWatch dashboards that combine native Amazon Bedrock token and invocation CloudWatch metrics. Set up CloudWatch alarms to monitor token usage thresholds.",
        ],
        "explanation": "Stay inside CloudWatch, where Bedrock already publishes data:\n"
                       "- **C:** native Bedrock **token/invocation metrics** → custom **dashboards** for each stakeholder group and **alarms** on thresholds across all models.\n"
                       "- **B:** **invocation logs + Logs Insights** add the *attribution* (which application/unit is consuming tokens) and high-usage queries, with log widgets on the same dashboards.\n\n"
                       "**A** QuickSight can't use CloudWatch metrics as a direct source (needs an export pipeline). **D** there's no Bedrock 'zero-ETL integration' with Managed Grafana. **E** a Firehose + OpenSearch pipeline is the heaviest to build and run.",
        "reference": f"{_BR}/monitoring-cw.html",
        "note": "Answer derived, moderate confidence — B + C are the two native, no-pipeline options; A, D and E need extra services or a feature that doesn't exist.",
    },
    {
        "id": 67, "category": D2, "task": "2.2", "type": "multi",
        "question": "A company is designing a solution that uses foundation models (FMs) to support multiple AI workloads. Some FMs must be invoked on demand and in real time. Other FMs require consistent high-throughput access for batch processing.\n"
                    "The solution must support hybrid deployment patterns and run workloads across cloud infrastructure and on-premises infrastructure to comply with data residency and compliance requirements.\n"
                    "Which combination of steps will meet these requirements? (Choose two.)",
        "options": [
            "A. Use AWS Lambda to orchestrate low-latency FM inference by invoking FMs hosted on Amazon SageMaker AI asynchronous endpoints.",
            "B. Configure provisioned throughput in Amazon Bedrock to ensure consistent performance for high-volume workloads.",
            "C. Deploy FMs to Amazon SageMaker AI endpoints with support for edge deployment by using Amazon SageMaker Neo. Orchestrate the FMs by using AWS Lambda to support hybrid deployment.",
            "D. Use Amazon Bedrock with auto-scaling to handle unpredictable traffic surges.",
            "E. Use Amazon SageMaker JumpStart to host and invoke the FMs.",
        ],
        "answer": [
            "B. Configure provisioned throughput in Amazon Bedrock to ensure consistent performance for high-volume workloads.",
            "C. Deploy FMs to Amazon SageMaker AI endpoints with support for edge deployment by using Amazon SageMaker Neo. Orchestrate the FMs by using AWS Lambda to support hybrid deployment.",
        ],
        "explanation": "Two requirements are explicit and each has one fitting option: **'consistent high-throughput access'** → **Bedrock Provisioned Throughput** (B); **'hybrid cloud + on-premises for data residency'** → models packaged for edge/on-prem with **SageMaker AI endpoints + SageMaker Neo**, orchestrated by Lambda (C) (exam-guide Skills 2.2.1, 2.3.4).\n\n"
                       "**A** asynchronous endpoints are not low-latency real time. **D** Bedrock is already serverless — it handles on-demand traffic but nothing on-premises, so it doesn't address hybrid. **E** JumpStart is a model hub, not a hybrid deployment mechanism.",
        "reference": f"{_BR}/prov-throughput.html",
        "note": "Answer derived, moderate confidence (B + C vs D). B and C are the only options that satisfy the two hard requirements (consistent throughput, hybrid/on-prem).",
    },
    {
        "id": 68, "category": D1, "task": "1.1", "type": "single",
        "question": "A company is planning to deploy multiple generative AI (GenAI) applications to five independent business units that operate in multiple countries in Europe and the Americas. Each application uses Amazon Bedrock Retrieval Augmented Generation (RAG) patterns with business unit-specific knowledge bases that store terabytes of unstructured data.\n"
                    "The company must establish well-architected, standardized components for security controls, observability practices, and deployment patterns across all the GenAI applications. The components must be reusable, versioned, and governed consistently.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure Amazon API Gateway REST API endpoints for the GenAI applications. Deploy common security, observability, and RAG patterns based on the AWS Well-Architected Generative AI Lens in standardized AWS CloudFormation templates. Use CloudFormation Guard after the deployment to validate policy compliance in each business unit.",
            "B. Create standardized AWS CloudFormation templates to implement security, observability, and RAG patterns based on the AWS Well-Architected Generative AI Lens. Establish a centralized repository that performs version control. Integrate a CI/CD pipeline with CloudFormation Guard to enforce consistent and repeatable deployments across business units.",
            "C. Use AWS Service Catalog to define standardized portfolios and versioned products for each business unit. Use the portfolios to enforce security, observability, and RAG patterns based on the AWS Well-Architected Generative AI Lens. Require the business units to use the Service Catalog console to deploy resources.",
            "D. Document security controls, observability requirements, and RAG patterns based on the AWS Well-Architected Generative AI Lens in a shared design document. Use Amazon Macie to enforce deployment. Delegate implementation responsibility to each business unit.",
        ],
        "answer": 'C. Use AWS Service Catalog to define standardized portfolios and versioned products for each'
                  ' business unit. Use the portfolios to enforce security, observability, and RAG patterns '
                  'based on the AWS Well-Architected Generative AI Lens. Require the business units to use the '
                  'Service Catalog console to deploy resources.',
        "explanation": "'Reusable, **versioned**, and **governed consistently**' across independent business units "
                       'is the **AWS Service Catalog** value proposition: platform teams publish approved '
                       '**products** (CloudFormation-based, embedding the security, observability and RAG patterns '
                       'from the Well-Architected Generative AI Lens) in **portfolios**, every product has versions,'
                       ' and business units can launch only what their portfolio allows — governance by construction'
                       ' (exam-guide Skill 1.1.3).\\n'
                       '\\n'
                       '**A** validates with CloudFormation Guard only *after* deployment (reactive) and adds an '
                       'unrelated API layer. **B** templates + repository + CI/CD with Guard can standardise '
                       'deployments, but nothing stops a unit from deploying outside the pipeline — it standardises '
                       "but doesn't govern. **D** is documentation plus a misapplied service (Macie), with no "
                       'enforcement.',
        "reference": "https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html",
        "note": 'Answer changed to C to match the CertyIQ answer key (my first derivation was B). Service '
                "Catalog is on the exam guide's in-scope list and fits 'standardised, versioned, governed'; B"
                ' is the close alternative.'
    },
    {
        "id": 69, "category": D5, "task": "5.1", "type": "single",
        "question": "A company upgraded its Amazon Bedrock powered foundation model (FM) that supports a multilingual customer service assistant. After the upgrade, the assistant exhibited inconsistent behavior across languages. The assistant began generating different responses in some languages when presented with identical questions.\n"
                    "The company needs a solution to detect and address similar problems for future updates. The evaluation must be completed within 45 minutes for all supported languages. The evaluation must process at least 15,000 test conversations in parallel. The evaluation process must be fully automated and integrated into the CI/CD pipeline. The solution must block deployment if quality thresholds are not met.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Create a distributed traffic simulation framework that sends translation-heavy workloads to the assistant in multiple languages simultaneously. Use Amazon CloudWatch metrics to monitor latency, concurrency, and throughput. Run simulations before production releases to identify infrastructure bottlenecks.",
            "B. Deploy the assistant in multiple AWS Regions with Amazon Route 53 latency-based routing and AWS Global Accelerator to improve global performance. Store multilingual conversation logs in Amazon S3. Perform weekly post-deployment audits to review consistency.",
            "C. Create a pre-processing pipeline that normalizes all incoming messages into a consistent format before sending the messages to the assistant. Apply rule-based checks to flag potential hallucinations in the outputs. Focus the evaluation on the normalized text to simplify testing across languages.",
            "D. Set up standardized multilingual test conversations with identical meaning. Run the test conversations in parallel by using Amazon Bedrock model evaluation jobs. Apply similarity and hallucination thresholds. Integrate the process into the CI/CD pipeline to block releases that fail.",
        ],
        "answer": "D. Set up standardized multilingual test conversations with identical meaning. Run the test conversations in parallel by using Amazon Bedrock model evaluation jobs. Apply similarity and hallucination thresholds. Integrate the process into the CI/CD pipeline to block releases that fail.",
        "explanation": "The defect is **cross-language response inconsistency**, so the test must use the **same question in each language**, score **similarity/hallucination**, run **at scale in parallel** (Bedrock model evaluation jobs) and act as an automated **quality gate** in CI/CD that blocks failing releases (exam-guide Skills 5.1.4, 5.1.9).\n\n"
                       "**A** tests infrastructure load, not answer consistency. **B** weekly post-deployment audits are after the fact, not a gate. **C** normalising to one format hides the language-specific behaviour being tested, and rule-based checks can't judge consistency.",
        "reference": f"{_BR}/model-evaluation-metrics.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 70, "category": D4, "task": "4.3", "type": "single",
        "question": "A company is developing a generative AI (GenAI) application that uses Amazon Bedrock foundation models (FMs). The application has several custom tool integrations. The application has experienced unexpected token consumption surges despite consistent user traffic.\n"
                    "The company needs a solution that uses Amazon Bedrock model invocation logging to monitor InputTokenCount metrics and OutputTokenCount metrics. The solution must detect unusual patterns in tool usage and identify which specific tool integrations cause abnormal token consumption. The solution must also automatically adjust thresholds as traffic patterns change.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon CloudWatch Logs to capture model invocation logs. Create CloudWatch dashboards based on InputTokenCount metrics and OutputTokenCount metrics. Configure static CloudWatch alarms with fixed thresholds for each tool integration.",
            "B. Store model invocation logs in an Amazon S3 bucket. Use AWS Glue to catalog the logs. Analyze token consumption patterns by using scheduled Amazon Athena queries that generate reports on tool usage trends.",
            "C. Use Amazon CloudWatch Logs to capture model invocation logs. Create CloudWatch metric filters to extract tool-specific invocation patterns. Apply CloudWatch anomaly detection alarms that adjust baselines for each tool's metrics.",
            "D. Store model invocation logs in an Amazon S3 bucket. Create an AWS Lambda function to process logs in real time. Manually update Amazon CloudWatch alarm thresholds based on token consumption trends that the Lambda function identifies.",
        ],
        "answer": "C. Use Amazon CloudWatch Logs to capture model invocation logs. Create CloudWatch metric filters to extract tool-specific invocation patterns. Apply CloudWatch anomaly detection alarms that adjust baselines for each tool's metrics.",
        "explanation": "**'Automatically adjust thresholds'** = **CloudWatch anomaly detection** (a learned, self-adjusting band). **'Which specific tool'** = **metric filters** on the invocation logs that emit per-tool metrics. Together: near-real-time, per-tool anomaly alarms with no manual tuning (exam-guide Skills 4.3.2, 4.3.4).\n\n"
                       "**A** static fixed thresholds can't adapt. **B** Athena reports are batch, not real-time alerting. **D** *manually* updating thresholds contradicts the requirement.",
        "reference": f"{_BR}/model-invocation-logging.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 71, "category": D2, "task": "2.3", "type": "single",
        "question": "A company is using Amazon Bedrock to develop an AI-powered application that uses a foundation model (FM) that supports cross-Region inference and provisioned throughput. The application must serve users in Europe and North America with consistently low latency. The application must comply with data residency regulations that require European user data to remain within Europe-based AWS Regions.\n"
                    "During testing, the application experiences service degradation when Regional traffic spikes reach service quotas. The company needs a solution that maintains application resilience and minimizes operational complexity.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Deploy separate Amazon Bedrock instances in North American and European Regions. Use a custom routing layer that directs traffic based on user location. Configure Amazon CloudWatch alarms to monitor Regional service usage. Use Amazon SNS to send email alerts to the company when usage approaches specified thresholds.",
            "B. Use Amazon Bedrock cross-Region inference profiles by specifying geographical codes in profile IDs when the application calls the InvokeModel API. Configure separate Amazon API Gateway HTTP APIs to direct European and North American users to the appropriate Regional endpoints.",
            "C. Deploy a multi-Region Amazon API Gateway HTTP API and AWS Lambda functions that implement retry logic to handle throttling. Configure the Lambda functions to call the FM in the nearest secondary Region when the application reaches service quotas in the primary Region. Use intelligent routing to ensure compliance with data residency requirements.",
            "D. Configure provisioned throughput for Amazon Bedrock in multiple Regions. Implement failover logic in the application code to switch between Regions when throttling occurs. Use AWS Global Accelerator to route traffic to the appropriate endpoints based on user location.",
        ],
        "answer": "B. Use Amazon Bedrock cross-Region inference profiles by specifying geographical codes in profile IDs when the application calls the InvokeModel API. Configure separate Amazon API Gateway HTTP APIs to direct European and North American users to the appropriate Regional endpoints.",
        "explanation": "**Geographic cross-Region inference profiles** (e.g. `eu.` and `us.` prefixes) let Bedrock automatically route to any Region *within that geography* when one is at quota — resilience with no custom failover — while **European traffic never leaves Europe**. Separate Regional API endpoints send each user group to the right profile.\n\n"
                       "**A/C/D** build custom routing, retry-to-secondary-Region or failover logic, which is exactly the operational complexity the company wants to avoid (C could even fail over outside Europe).",
        "reference": f"{_BR}/cross-region-inference.html",
        "note": "Answer derived. High confidence. Compare Q13 (CRI + SCP) and Q96.",
    },
    {
        "id": 72, "category": D2, "task": "2.3", "type": "single",
        "question": "An international company is building an AI assistant that uses RAG. The company wants the AI assistant to have near real-time, low-latency performance. The AI assistant must provide service to several geographic areas. The company's customers will use proprietary data with the AI assistant. The proprietary data must not leave the company's immediate geographic area.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Deploy an Amazon Bedrock model with a cross-Region model inference profile. Create Amazon S3 buckets in each AWS Region the company operates in. Store a knowledge base in each respective S3 bucket. In each Region, configure Amazon Kendra to interact with the respective knowledge base. In each Region, configure an AWS Lambda function that uses Kendra and Amazon Bedrock to process AI assistant prompts.",
            "B. Deploy an Amazon Bedrock model in each AWS Region the company operates in. Configure an Amazon Bedrock cross-Region model inference profile. Configure a vector database that uses Amazon Bedrock Knowledge Bases. Store the knowledge bases in Amazon S3 in each Region the company operates in.",
            "C. Use AWS Outposts to deploy an outpost in each AWS Region the company operates in. Create Amazon S3 buckets to store knowledge bases in each corresponding Region. Deploy Amazon RDS configured as a vector database to each outpost. Deploy an Amazon Bedrock model with a cross-Region inference profile in a central Region.",
            "D. Configure a knowledge base stored in the Amazon S3 Express One Zone storage class in each AWS Local Zone the company operates in. Use Amazon RDS to deploy a vector database in each Local Zone the company operates in. Deploy a large language model (LLM) to Amazon EC2 instances in each Local Zone. Configure the AI assistant to route prompts to the model in the respective Local Zone.",
        ],
        "answer": "B. Deploy an Amazon Bedrock model in each AWS Region the company operates in. Configure an Amazon Bedrock cross-Region model inference profile. Configure a vector database that uses Amazon Bedrock Knowledge Bases. Store the knowledge bases in Amazon S3 in each Region the company operates in.",
        "explanation": "Keep **data and inference regional**, and keep it **managed**: Bedrock in each operating Region (low latency), geography-scoped cross-Region inference for resilience within the area, and **Knowledge Bases** with the vector store and S3 source data in each Region so proprietary data never leaves its area.\n\n"
                       "**A** adds Kendra and Lambda glue and uses a single (not per-Region) model setup. **C** a central-Region model sends prompts (and retrieved data) out of the data's area, and Outposts/RDS are heavy. **D** self-hosting an LLM on EC2 in Local Zones is far more operational work.",
        "reference": f"{_BR}/cross-region-inference.html",
        "note": "Answer derived, moderate confidence (B vs A) — B is the managed, per-Region design.",
    },
    {
        "id": 73, "category": D2, "task": "2.4", "type": "single",
        "question": "A company is building a generative AI (GenAI) application that processes financial reports and provides summaries for analysts. The application must run two compute environments. In one environment, AWS Lambda function must use the Python SDK to analyze reports on demand. In the second environment, Amazon EKS containers must use the JavaScript SDK to batch process multiple reports on a schedule. The application must maintain conversational context throughout multi-turn interactions, use the same foundation model (FM) across environments, and ensure consistent authentication.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use the Amazon Bedrock InvokeModel API with a separate authentication method for each environment. Store conversation states in Amazon DynamoDB. Use custom I/O formatting logic for each programming language.",
            "B. Use the Amazon Bedrock Converse API directly in both environments with a common authentication mechanism that uses IAM roles. Store conversation states in Amazon ElastiCache. Creating programming language-specific wrappers for model parameters.",
            "C. Create a centralized Amazon API Gateway REST API endpoint that handles all model interactions by using the InvokeModel API. Store interaction history in application process memory in each Lambda function or EKS container. Use environment variables to configure model parameters.",
            "D. Use the Amazon Bedrock Converse API and IAM roles for authentication. Pass previous messages in the request messages array to maintain conversational context. Use programming language-specific SDKs to establish consistent API interfaces.",
        ],
        "answer": "D. Use the Amazon Bedrock Converse API and IAM roles for authentication. Pass previous messages in the request messages array to maintain conversational context. Use programming language-specific SDKs to establish consistent API interfaces.",
        "explanation": "The **Converse API** gives one consistent request/response shape across models and languages, and carries **multi-turn context in the `messages` array**; **IAM roles** (Lambda execution role, EKS IRSA) give the same authentication mechanism in both environments; each environment uses its native SDK.\n\n"
                       "**A** has two authentication methods and per-language formatting logic. **B** reasonable until it adds an ElastiCache state store and custom wrappers (extra moving parts, and a cache isn't a durable conversation store). **C** in-process memory loses context across invocations/pods.",
        "reference": f"{_BR}/conversation-inference.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 74, "category": D4, "task": "4.2", "type": "single",
        "question": "A company is building a serverless application that uses AWS Lambda functions to help students around the world summarize notes. The application uses Anthropic Claude through Amazon Bedrock. The company observed that most of the traffic occurs during evenings in each time zone. Users report experiencing throttling errors during peak usage times in their times zones.\n"
                    "The company needs to resolve the throttling issues by ensuring continuous operation of the application. The solution must maintain application performance quality. The company needs a solution that does not require a fixed hourly cost during low traffic periods.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Create custom Amazon CloudWatch metrics to monitor model errors. Set provisioned throughput to a value that is safely higher than the peak traffic observed.",
            "B. Create custom Amazon CloudWatch metrics to monitor model errors. Set up a failover mechanism to redirect invocations to a backup AWS Region when the errors exceed a specified threshold.",
            "C. Enable invocation logging in Amazon Bedrock. Monitor key metrics such as Invocations, InputTokenCount, OutputTokenCount, and Invocation Throttles. Distribute traffic across cross-Region inference endpoints.",
            "D. Enable invocation logging in Amazon Bedrock. Monitor InvocationLatency, InvocationClientErrors, and InvocationServerErrors metrics. Distribute traffic across multiple versions of the same model.",
        ],
        "answer": "C. Enable invocation logging in Amazon Bedrock. Monitor key metrics such as Invocations, InputTokenCount, OutputTokenCount, and Invocation Throttles. Distribute traffic across cross-Region inference endpoints.",
        "explanation": "The peaks follow **time zones**, so capacity is idle somewhere else at any moment. **Cross-Region inference** (on-demand, pay per token) pools capacity across Regions, absorbing a Region's evening peak with no fixed hourly cost, while the `InvocationThrottles` metric confirms the effect. \n\n"
                       "**A** Provisioned Throughput sized above peak bills hourly even at low traffic. **B** custom failover logic is reactive and more to maintain. **D** versions of the same model share the same Regional quota and don't add capacity.",
        "reference": f"{_BR}/cross-region-inference.html",
        "note": "Answer derived. High confidence — the 'no fixed hourly cost' clause rules out provisioned throughput.",
    },
    {
        "id": 75, "category": D2, "task": "2.1", "type": "single",
        "question": "A company is developing a new AI-powered application that needs to integrate with various specialized tools. These tools currently run as Model Context Protocol (MCP) servers on the local machines of developers and do not maintain states between invocations. The company plans to deploy each MCP server as an AWS Lambda function to support the company's production application.\n"
                    "The solution must be accessible to both internal applications and authorized third-party partners. The solution must use strict authentication and authorization controls.\n"
                    "Which additional steps will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Create a custom Lambda invocation transport by using the Lambda Invoke API. Implement IAM authentication and grant InvokeFunction permissions to authorized users and roles.",
            "B. Expose the Lambda functions through Amazon API Gateway REST API endpoints. Implement API keys for authentication. Configure the applications that need to access the MCP servers to use standard HTTP requests instead of the MCP protocol.",
            "C. Create Lambda function URLs and enable a custom Streamable HTTP transport and SigV4. Implement AWS IAM authentication. Grant InvokeFunctionUrl permissions to authorized users and roles.",
            "D. Expose the Lambda function through Amazon API Gateway HTTP API endpoints with the Streamable HTTP transport. Use Amazon Cognito to implement OAuth authentication. Configure API Gateway to validate OAuth tokens.",
        ],
        "answer": "D. Expose the Lambda function through Amazon API Gateway HTTP API endpoints with the Streamable HTTP transport. Use Amazon Cognito to implement OAuth authentication. Configure API Gateway to validate OAuth tokens.",
        "explanation": "Stateless local MCP servers → **Lambda** behind **API Gateway HTTP API** using the standard **Streamable HTTP** transport. Authorisation for both internal apps and **third-party partners** should be **OAuth** (Cognito) validated by a JWT authorizer in API Gateway — no custom code, and partners don't need AWS IAM identities.\n\n"
                       "**A** a custom Invoke-based transport isn't MCP-compatible. **B** API keys are weak authentication and bypass the MCP protocol. **C** a *custom* transport plus SigV4 forces partners to hold AWS credentials and sign requests.",
        "reference": _MCP,
        "note": "Answer derived. High confidence — same pattern as Q52.",
    },
]
