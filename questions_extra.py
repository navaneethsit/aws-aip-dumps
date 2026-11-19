"""
Additional AIP-C01 questions (bank expansion).

Same schema as questions.py (see its docstring). Append dicts to EXTRA, use unique
ids, pick `category` from CATEGORIES (the 5 official exam domains), then run:

    py -3 validate.py

Batches so far:
  - 11-30 : Exam A · Topic 1 · Q11-Q30 (pasted practice set, with community votes)
  - 31-50 : Exam A · Topic 1 · Q31-Q50 (screenshots; source answers hidden, so answers
            are derived from the exam guide + AWS docs and carry no vote data)
"""

_BR = "https://docs.aws.amazon.com/bedrock/latest/userguide"

D1 = "1 · FM Integration, Data & Compliance"
D2 = "2 · Implementation & Integration"
D3 = "3 · Safety, Security & Governance"
D4 = "4 · Operational Efficiency & Optimization"
D5 = "5 · Testing, Validation & Troubleshooting"

EXTRA: list[dict] = [
    # ------------------------------------------------------------------ #
    # Exam A · Topic 1 · Q11-Q20
    # ------------------------------------------------------------------ #
    {
        "id": 11,
        "category": D1,
        "task": "1.6",
        "type": "multi",
        "question": "A company is using Amazon Bedrock to design an application to help researchers "
                    "apply for grants. The application is based on an Amazon Nova Pro foundation "
                    "model (FM). The application contains four required inputs and must provide "
                    "responses in a consistent text format. The company wants to receive a "
                    "notification in Amazon Bedrock if a response contains bullying language. "
                    "However, the company does not want to block all flagged responses.\n"
                    "The company creates an Amazon Bedrock flow that takes an input prompt and "
                    "sends it to the Amazon Nova Pro FM. The Amazon Nova Pro FM provides a "
                    "response.\n"
                    "Which additional steps must the company take to meet these requirements? "
                    "(Choose two.)",
        "options": [
            "A. Use Amazon Bedrock Prompt Management to specify the required inputs as variables. "
            "Select an Amazon Nova Pro FM. Specify the output format for the response. Add the "
            "prompt to the prompts node of the flow.",
            "B. Create an Amazon Bedrock guardrail that applies the hate content filter. Set the "
            "filter response to block. Add the guardrail to the prompts node of the flow.",
            "C. Create an Amazon Bedrock prompt router. Specify an Amazon Nova Pro FM. Add the "
            "required inputs as variables to the input node of the flow. Add the prompt router to "
            "the prompts node. Add the output format to the output node.",
            "D. Create an Amazon Bedrock guardrail that applies the insults content filter. Set the "
            "filter response to detect. Add the guardrail to the prompts node of the flow.",
            "E. Create an Amazon Bedrock application inference profile that specifies an Amazon "
            "Nova Pro FM. Specify the output format for the response in the description. Include a "
            "tag for each of the input variables. Add the profile to the prompts node of the flow.",
        ],
        "answer": [
            "A. Use Amazon Bedrock Prompt Management to specify the required inputs as variables. "
            "Select an Amazon Nova Pro FM. Specify the output format for the response. Add the "
            "prompt to the prompts node of the flow.",
            "D. Create an Amazon Bedrock guardrail that applies the insults content filter. Set the "
            "filter response to detect. Add the guardrail to the prompts node of the flow.",
        ],
        "explanation": "Two independent needs:\n"
                       "- **Required inputs + consistent format → a managed prompt (A):** Prompt "
                       "Management defines the variables, model and output format, and plugs into the "
                       "flow's prompts node.\n"
                       "- **Notify on bullying but don't block → guardrail in *detect* mode (D):** the "
                       "insults content filter covers bullying/demeaning language; with action = "
                       "detect the guardrail records the finding without blocking the response.\n\n"
                       "**B** the hate filter targets identity-based hate and 'block' stops the "
                       "response. **C** a prompt router picks between models of one family — it doesn't "
                       "define variables or output formats. **E** an application inference profile is "
                       "for cost tracking/tagging, not prompt templating.",
        "reference": f"{_BR}/guardrails-components.html",
        "votes": {"AD": 100},
    },
    {
        "id": 12,
        "category": D5,
        "task": "5.1",
        "type": "single",
        "question": "A healthcare company is using Amazon Bedrock to build a Retrieval Augmented "
                    "Generation (RAG) application that helps practitioners make clinical decisions. "
                    "The application must achieve high accuracy for patient information retrievals, "
                    "identify hallucinations in generated content, and reduce human review costs.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon Comprehend to analyze and classify RAG responses and to extract medical "
            "entities and relationships. Use AWS Step Functions to orchestrate automated "
            "evaluations. Configure Amazon CloudWatch metrics to track entity recognition "
            "confidence scores. Configure CloudWatch to send an alert when accuracy falls below "
            "specified thresholds.",
            "B. Implement automated large language model (LLM)-based evaluations that use a "
            "specialized model that is fine-tuned for medical content to assess all responses. "
            "Deploy AWS Lambda functions to parallelize evaluations. Publish results to Amazon "
            "CloudWatch metrics that track relevance and factual accuracy.",
            "C. Configure Amazon CloudWatch Synthetics to generate test queries that have known "
            "answers on a regular schedule, and track model success rates. Set up dashboards that "
            "compare synthetic test results against expected outcomes.",
            "D. Deploy a hybrid evaluation system that uses an automated LLM-as-a-judge evaluation "
            "to initially screen responses and targeted human reviews for edge cases. Use Amazon "
            "SageMaker Feature Store to maintain evaluation datasets. Use a built-in Amazon Bedrock "
            "evaluation to track retrieval precision and hallucination rates.",
        ],
        "answer": "D. Deploy a hybrid evaluation system that uses an automated LLM-as-a-judge "
                  "evaluation to initially screen responses and targeted human reviews for edge "
                  "cases. Use Amazon SageMaker Feature Store to maintain evaluation datasets. Use a "
                  "built-in Amazon Bedrock evaluation to track retrieval precision and hallucination "
                  "rates.",
        "explanation": "The stem names three things: **retrieval accuracy**, **hallucination "
                       "detection**, **lower human-review cost**. Bedrock's built-in RAG evaluation "
                       "(retrieval and generation metrics) plus an **LLM-as-a-judge** first pass "
                       "automates most scoring, and **humans review only edge cases** — exactly the "
                       "cost reduction asked for.\n\n"
                       "**A** Comprehend extracts entities; it doesn't judge groundedness. **B** "
                       "fine-tuning and judging *all* responses is heavy and still custom. **C** "
                       "Synthetics checks scheduled known-answer queries — it doesn't evaluate "
                       "retrieval quality or hallucinations in real answers.",
        "reference": f"{_BR}/evaluation-kb.html",
        "votes": {"D": 100},
    },
    {
        "id": 13,
        "category": D2,
        "task": "2.3",
        "type": "multi",
        "question": "A company configures a landing zone in AWS Control Tower. The company handles "
                    "sensitive data that must remain within the European Union. The company must use "
                    "only the eu-central-1 Region. The company uses SCPs to enforce data residency "
                    "policies. GenAI developers at the company are assigned IAM roles that have full "
                    "permissions for Amazon Bedrock.\n"
                    "The company must ensure that GenAI developers can use the Amazon Nova Pro model "
                    "through Amazon Bedrock only by using cross-Region inference (CRI) and only in "
                    "eu-central-1. The company enables model access for the GenAI developer IAM roles "
                    "in Amazon Bedrock. However, when a GenAI developer attempts to invoke the model "
                    "through the Amazon Bedrock Chat/Text playground, the GenAI developer receives the "
                    "following error.\n"
                    "User: arn:aws:sts::123456789012:assumed-role/AssumedDevRole/DevUserName\n"
                    "Action: bedrock:InvokeModelWithResponseStream\n"
                    "On resource(s): arn:aws:bedrock:eu-west-3::foundation-model/amazon.nova-pro-v1:0\n"
                    "Context: a service control policy explicitly denies the action\n"
                    "The company needs a solution to resolve the error. The solution must retain the "
                    "company's existing governance controls and must provide precise access control. "
                    "The solution must comply with the company's existing data residency policies.\n"
                    "Which combination of solutions will meet these requirements? (Choose two.)",
        "options": [
            "A. Add the AdministratorAccess policy to the GenAI developer IAM role.",
            "B. Extend the existing SCPs to enable CRI for the eu.amazon.nova-pro-v1:0 inference "
            "profile.",
            "C. Enable Amazon Bedrock model access for Amazon Nova Pro in the eu-west-3 Region.",
            "D. Validate that the GenAI developer IAM roles have permissions to invoke Amazon Nova "
            "Pro through the eu.amazon.nova-pro.v1:0 inference profile on all European Union AWS "
            "Regions that can serve the model.",
            "E. Extend the existing SCP to enable CRI for the eu.* inference profile.",
        ],
        "answer": [
            "B. Extend the existing SCPs to enable CRI for the eu.amazon.nova-pro-v1:0 inference "
            "profile.",
            "D. Validate that the GenAI developer IAM roles have permissions to invoke Amazon Nova "
            "Pro through the eu.amazon.nova-pro.v1:0 inference profile on all European Union AWS "
            "Regions that can serve the model.",
        ],
        "explanation": "A CRI inference profile routes the call to *destination* Regions. The SCP "
                       "currently allows only eu-central-1, so it explicitly denies the foundation-model "
                       "ARN in eu-west-3. The precise fix is two-part:\n"
                       "- **B:** extend the SCP to allow only the specific `eu.amazon.nova-pro-v1:0` "
                       "profile (and its EU destination Regions) — governance stays, scope stays narrow.\n"
                       "- **D:** the IAM role must be allowed to invoke through the inference profile "
                       "*and* the underlying model in every EU Region the profile can route to.\n\n"
                       "**A** AdministratorAccess breaks least privilege (and can't override an SCP). "
                       "**C** model access isn't enabled per destination Region for CRI. **E** "
                       "`eu.*` is a wildcard for all EU profiles — not precise.",
        "reference": f"{_BR}/cross-region-inference.html",
        "votes": {"B": 20, "BD": 80},
        "note": "Mildly disputed (BD 80%, B alone 20%). The stem asks for TWO steps and 'precise "
                "access control', so SCP (B) + IAM validation (D) is the pairing; E is the "
                "'too broad' trap.",
    },
    {
        "id": 14,
        "category": D3,
        "task": "3.1",
        "type": "single",
        "question": "A financial services company is developing a customer service AI assistant by "
                    "using Amazon Bedrock. The AI assistant must not discuss investment advice with "
                    "users. The AI assistant must block harmful content, mask personally identifiable "
                    "information (PII), and maintain audit trails for compliance reporting. The AI "
                    "assistant must apply content filtering to both user inputs and model responses "
                    "based on content sensitivity.\n"
                    "The company requires an Amazon Bedrock guardrail configuration that will "
                    "effectively enforce policies with minimal false positives. The solution must "
                    "provide multiple handling strategies for multiple types of sensitive content.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure a single guardrail and set content filters to high for all categories. Set "
            "up denied topics for investment advice and include sample phrases to block. Set up "
            "sensitive information filters that apply the block action for all PII entities. Apply "
            "the guardrail to all model inference calls.",
            "B. Configure multiple guardrails by using tiered policies. Create one guardrail and set "
            "content filters to high. Configure the guardrail to block PII for public interactions. "
            "Configure a second guardrail and set content filters to medium. Configure the second "
            "guardrail to mask PII for internal use. Configure multiple topic-specific guardrails to "
            "block investment advice and set up contextual grounding checks.",
            "C. Configure a guardrail and set content filters to medium for harmful content. Set up "
            "denied topics for investment advice and include clear definitions and sample phrases to "
            "block. Configure sensitive information filters to mask PII in responses and to block "
            "financial information in inputs. Enable both input and output evaluations that use "
            "custom blocked messages for audits.",
            "D. Create a separate guardrail for each use case. Create one guardrail that applies a "
            "harmful content filter. Create a guardrail to apply topic filters for investment "
            "advice. Create a guardrail to apply sensitive information filters to block PII. Use "
            "AWS Step Functions to chain the guardrails together sequentially. Use conditional "
            "logic based on content classification.",
        ],
        "answer": "C. Configure a guardrail and set content filters to medium for harmful content. "
                  "Set up denied topics for investment advice and include clear definitions and "
                  "sample phrases to block. Configure sensitive information filters to mask PII in "
                  "responses and to block financial information in inputs. Enable both input and "
                  "output evaluations that use custom blocked messages for audits.",
        "explanation": "One well-tuned guardrail covers every requirement: **medium** filter strength "
                       "balances protection against false positives; a **denied topic** with a clear "
                       "definition + sample phrases handles investment advice; the sensitive-information "
                       "policy supports *different actions per entity* (**mask** PII in responses, "
                       "**block** financial data in inputs = 'multiple handling strategies'); and it "
                       "evaluates both input and output.\n\n"
                       "**A** high everywhere + block-all PII causes false positives and can't mask. "
                       "**B/D** multiple guardrails / Step Functions chaining add needless complexity "
                       "and operational overhead when one guardrail already covers every policy.",
        "reference": f"{_BR}/guardrails-sensitive-filters.html",
        "votes": {"C": 100},
    },
    {
        "id": 15,
        "category": D1,
        "task": "1.5",
        "type": "single",
        "question": "An ecommerce company is developing a generative AI (GenAI) solution that uses "
                    "Amazon Bedrock with Anthropic Claude to recommend products to customers. "
                    "Customers report that some of the recommended products are not available for "
                    "sale on the website or are not relevant to the customer. Customers also report "
                    "that the solutions takes a long time to generate some recommendations.\n"
                    "The company investigates the issues and finds that most interactions between "
                    "customers and the product recommendation solution are unique. The company "
                    "confirms that the solutions recommends products that are not in the company's "
                    "product catalog. The company must resolve these issues.\n"
                    "Which solution will meet this requirement?",
        "options": [
            "A. Increase grounding within Amazon Bedrock Guardrails. Enable Automated Reasoning "
            "checks. Set up provisioned throughput.",
            "B. Use prompt engineering to restrict the model responses to relevant products. Use "
            "streaming techniques such as the InvokeModelWithResponseStream action to reduce "
            "perceived latency for the customers.",
            "C. Create an Amazon Bedrock knowledge base. Implement Retrieval Augmented Generation "
            "(RAG). Set the PerformanceConfigLatency parameter to optimized.",
            "D. Store product catalog data in Amazon OpenSearch Service. Validate the model's "
            "product recommendations against the product catalog. Use Amazon DynamoDB to implement "
            "response caching.",
        ],
        "answer": "C. Create an Amazon Bedrock knowledge base. Implement Retrieval Augmented "
                  "Generation (RAG). Set the PerformanceConfigLatency parameter to optimized.",
        "explanation": "Two defects, two fixes: **non-catalog products = ungrounded model → RAG over "
                       "the product catalog (Knowledge Bases)**; **slow responses → latency-optimized "
                       "inference** (`performanceConfig.latency = optimized`, on supported models).\n\n"
                       "**A** guardrail grounding needs a source to compare to, and provisioned "
                       "throughput is costly capacity, not a latency fix. **B** prompting cannot "
                       "reliably stop invented SKUs, and streaming only changes *perceived* latency. "
                       "**D** caching is useless when 'most interactions are unique', and validating "
                       "after the fact adds latency.",
        "reference": f"{_BR}/latency-optimized-inference.html",
        "votes": {"B": 20, "C": 80},
        "note": "Clue: 'most interactions are unique' rules out caching (D). 'Recommends products "
                "not in the catalog' = grounding problem → RAG, not prompt tweaks (B).",
    },
    {
        "id": 16,
        "category": D2,
        "task": "2.1",
        "type": "multi",
        "question": "A company is using AWS Lambda and REST APIs to build a reasoning agent to "
                    "automate support workflows. The system must preserve memory across interactions, "
                    "share the relevant agent state, and support event-driven invocation and "
                    "synchronous invocation. The system must also enforce access control and "
                    "session-based permissions.\n"
                    "Which combination of steps provides the MOST scalable solution? (Choose two.)",
        "options": [
            "A. Use Amazon Bedrock AgentCore to manage memory and session-aware reasoning. Deploy "
            "the agent with built-in identity support, event handling, and observability.",
            "B. Register the Lambda functions and the REST APIs as actions by using Amazon API "
            "Gateway and Amazon EventBridge. Enable Amazon Bedrock AgentCore to invoke the Lambda "
            "functions and the REST APIs without custom orchestration code.",
            "C. Use Amazon Bedrock Agents for reasoning and conversation management. Use AWS Step "
            "Functions and Amazon SQS queues for orchestration. Store the agent state in Amazon "
            "DynamoDB to maintain memory between steps.",
            "D. Deploy the reasoning logic as a container on Amazon ECS behind Amazon API Gateway. "
            "Use Amazon Aurora to store memory data and identity data.",
            "E. Build a custom RAG pipeline by using Amazon Kendra and Amazon Bedrock. Use AWS "
            "Lambda to orchestrate tool invocations. Store the agent state in Amazon S3.",
        ],
        "answer": [
            "A. Use Amazon Bedrock AgentCore to manage memory and session-aware reasoning. Deploy "
            "the agent with built-in identity support, event handling, and observability.",
            "B. Register the Lambda functions and the REST APIs as actions by using Amazon API "
            "Gateway and Amazon EventBridge. Enable Amazon Bedrock AgentCore to invoke the Lambda "
            "functions and the REST APIs without custom orchestration code.",
        ],
        "explanation": "Every requirement maps to a managed AgentCore capability: **Memory** (state "
                       "across interactions), **Identity** (access control, session-based "
                       "permissions), a **Runtime** with sync + event-driven invocation, and "
                       "**Observability** — so A. B then exposes the existing Lambda functions and "
                       "REST APIs to the agent as tools with no custom orchestration glue.\n\n"
                       "**C** hand-builds memory/orchestration (Step Functions + SQS + DynamoDB). **D** "
                       "and **E** are fully custom stacks that you scale and secure yourself.",
        "reference": "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html",
        "votes": {"A": 29, "AB": 71},
        "note": "Disputed (AB 71%, A alone 29%). Option B is loosely worded — AgentCore Gateway is "
                "the feature that turns Lambda functions/APIs into agent tools — but it is the only "
                "other option that avoids custom orchestration. The stem asks for TWO answers.",
    },
    {
        "id": 17,
        "category": D1,
        "task": "1.4",
        "type": "single",
        "question": "A financial services company is developing a Retrieval Augmented Generation "
                    "(RAG) application to help investment analysts query complex financial "
                    "relationships across multiple investment vehicles, market sectors, and "
                    "regulatory environments. The dataset contains highly interconnected entities "
                    "that have multi-hop relationships. The analysts must be able to examine the "
                    "relationships holistically to provide accurate investment guidance. The "
                    "application must deliver comprehensive answers that capture indirect "
                    "relationships between financial entities. The application must produce "
                    "responses in less than 3 seconds.\n"
                    "Which solution will meet these requirements with the LEAST operational "
                    "overhead?",
        "options": [
            "A. Use Amazon Bedrock Knowledge Bases with Graph RAG and Amazon Neptune Analytics to "
            "store the financial data. Analyze the multi-hop relationships between entities and "
            "automatically identify related information across documents.",
            "B. Use Amazon Bedrock Knowledge Bases and an Amazon OpenSearch Service vector store to "
            "implement custom relationship identification logic that uses AWS Lambda functions to "
            "query multiple vector embeddings in sequence.",
            "C. Use an Amazon OpenSearch Serverless vector database with k-nearest neighbor (k-NN) "
            "searches. Implement manual relationship mapping in an application layer that runs in "
            "an Amazon EC2 Auto Scaling group.",
            "D. Use Amazon DynamoDB to store financial data in a custom indexing system. Use an AWS "
            "Lambda function to query relevant records based on input questions. Use Amazon "
            "SageMaker AI to generate responses.",
        ],
        "answer": "A. Use Amazon Bedrock Knowledge Bases with Graph RAG and Amazon Neptune "
                  "Analytics to store the financial data. Analyze the multi-hop relationships "
                  "between entities and automatically identify related information across "
                  "documents.",
        "explanation": "'Highly interconnected entities', 'multi-hop' and 'indirect relationships' "
                       "are the trigger words for **GraphRAG**. Bedrock Knowledge Bases builds the "
                       "graph automatically in Neptune Analytics and combines vector search with graph "
                       "traversal — managed, fast, and no relationship-mapping code.\n\n"
                       "**B/C/D** all require custom relationship logic (sequential vector queries, "
                       "manual mapping, custom indexing) — more operational overhead and slower, "
                       "which jeopardises the 3-second target.",
        "reference": f"{_BR}/knowledge-base-build-graphs.html",
        "votes": {"A": 100},
    },
    {
        "id": 18,
        "category": D4,
        "task": "4.3",
        "type": "single",
        "question": "A healthcare company uses Amazon Bedrock to deploy an application that "
                    "generates summaries of clinical documents. The application experiences "
                    "inconsistent response quality with occasional factual hallucinations. Monthly "
                    "costs exceed the company's projections by 40%. A GenAI developer must implement "
                    "a near real-time monitoring solution to detect hallucinations, identify abnormal "
                    "token consumption, and provide early warnings of cost anomalies. The solution "
                    "must require minimal custom development work and maintenance overhead.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure Amazon CloudWatch alarms to monitor InputTokenCount and OutputTokenCount "
            "metrics to detect anomalies. Store model invocation logs in an Amazon S3 bucket. Use "
            "AWS Glue and Amazon Athena to identify potential hallucinations.",
            "B. Run Amazon Bedrock evaluation jobs that use LLM-based judgments to detect "
            "hallucinations. Configure Amazon CloudWatch to track token usage. Create an AWS Lambda "
            "function to process CloudWatch metrics. Configure the Lambda function to send usage "
            "pattern notifications.",
            "C. Configure Amazon Bedrock to store model invocation logs in an Amazon S3 bucket. "
            "Enable text output logging. Configure Amazon Bedrock guardrails to run contextual "
            "grounding checks to detect hallucinations. Create Amazon CloudWatch anomaly detection "
            "alarms for token usage metrics.",
            "D. Use AWS CloudTrail to log all Amazon Bedrock API calls. Create a custom dashboard "
            "in Amazon QuickSight to visualize token usage patterns. Use Amazon SageMaker Model "
            "Monitor to detect quality drift in generated summaries.",
        ],
        "answer": "C. Configure Amazon Bedrock to store model invocation logs in an Amazon S3 "
                  "bucket. Enable text output logging. Configure Amazon Bedrock guardrails to run "
                  "contextual grounding checks to detect hallucinations. Create Amazon CloudWatch "
                  "anomaly detection alarms for token usage metrics.",
        "explanation": "All three needs are covered by built-in features: **contextual grounding "
                       "checks** (hallucination detection at inference time, near real time), **model "
                       "invocation logging** (audit trail), and **CloudWatch anomaly detection** on "
                       "token-usage metrics (abnormal consumption / cost early warning) — minimal code.\n\n"
                       "**A** hallucination detection via Glue + Athena is batch and custom. **B** "
                       "evaluation jobs are offline, not near real time, plus a custom Lambda. **D** "
                       "CloudTrail doesn't carry prompts/tokens, and Model Monitor is for SageMaker "
                       "endpoints, not Bedrock.",
        "reference": f"{_BR}/guardrails-contextual-grounding-check.html",
        "votes": {"B": 11, "C": 89},
    },
    {
        "id": 19,
        "category": D3,
        "task": "3.3",
        "type": "single",
        "question": "A company is building a generative AI (GenAI) application that produces content "
                    "based on a variety of internal and external data sources. The company wants to "
                    "ensure that the generated output is fully traceable. The application must "
                    "support data source registration and enable metadata tagging to attribute "
                    "content to its original source. The application must also maintain audit logs of "
                    "data access and usage throughout the pipeline.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use AWS Lake Formation to catalog data sources and control access. Apply metadata "
            "tags directly in Amazon S3. Use AWS CloudTrail to monitor API activity.",
            "B. Use AWS Glue Data Catalog to register and tag data sources. Use Amazon CloudWatch "
            "Logs to monitor access patterns and application behavior.",
            "C. Store data in Amazon S3 and use object tagging for attribution. Use AWS Glue Data "
            "Catalog to manage schema information. Use AWS CloudTrail to log access to S3 buckets.",
            "D. Use AWS Glue Data Catalog to register all data sources. Apply metadata tags to "
            "attribute data sources. Use AWS CloudTrail to log access and activity across services.",
        ],
        "answer": "D. Use AWS Glue Data Catalog to register all data sources. Apply metadata tags to "
                  "attribute data sources. Use AWS CloudTrail to log access and activity across "
                  "services.",
        "explanation": "This mirrors exam-guide Skill 3.3.2 almost word for word: **Glue Data Catalog "
                       "to register data sources**, **metadata tagging for source attribution**, and "
                       "**CloudTrail for audit logging** across the pipeline.\n\n"
                       "**A** Lake Formation is for access control, and S3 tags alone don't register "
                       "sources. **B** CloudWatch Logs is not an audit trail of data access (CloudTrail "
                       "is). **C** logs only S3 bucket access and uses the Catalog just for schemas, "
                       "not source registration.",
        "reference": "https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html",
        "votes": {"C": 14, "D": 86},
    },
    {
        "id": 20,
        "category": D4,
        "task": "4.2",
        "type": "single",
        "question": "A financial services company needs to build a document analysis system that uses "
                    "Amazon Bedrock to process quarterly reports. The system must analyze financial "
                    "data, perform sentiment analysis, and validate compliance across batches of "
                    "reports. Each batch contains 5 reports. Each report requires multiple foundation "
                    "model (FM) calls. The solution must finish the analysis within 10 seconds for "
                    "each batch. Current sequential processing takes 45 seconds for each batch.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use AWS Lambda functions with provisioned concurrency to process each analysis type "
            "sequentially. Configure the Lambda function timeouts to 10 seconds. Configure automatic "
            "retries with exponential backoff.",
            "B. Use AWS Step Functions with a Parallel state to invoke separate AWS Lambda functions "
            "for each analysis type simultaneously. Configure Amazon Bedrock client timeouts. Use "
            "Amazon CloudWatch metrics to track execution time and model inference latency.",
            "C. Create an Amazon SQS queue to buffer analysis requests. Deploy multiple AWS Lambda "
            "functions with reserved concurrency. Configure each Lambda function to process "
            "different aspects of each report sequentially and then combine the results.",
            "D. Deploy an Amazon ECS cluster that runs containers that process each report "
            "sequentially. Use a load balancer to distribute batch workloads. Configure an "
            "auto-scaling policy based on CPU utilization to handle demand fluctuations.",
        ],
        "answer": "B. Use AWS Step Functions with a Parallel state to invoke separate AWS Lambda "
                  "functions for each analysis type simultaneously. Configure Amazon Bedrock client "
                  "timeouts. Use Amazon CloudWatch metrics to track execution time and model "
                  "inference latency.",
        "explanation": "The slowness is **sequential** work (45 s). The three analyses are independent, "
                       "so run them **in parallel** — Step Functions' *Parallel* state fans out to "
                       "separate Lambdas and joins the results, cutting wall-clock time toward the "
                       "slowest single branch.\n\n"
                       "**A, C, D** keep processing sequential (provisioned concurrency, SQS buffering, "
                       "ECS autoscaling only add capacity/throughput, not parallelism inside a batch). "
                       "A 10-second Lambda timeout would also just fail slow calls.",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/state-parallel.html",
        "votes": {"A": 8, "B": 83, "C": 8},
    },

    # ------------------------------------------------------------------ #
    # Exam A · Topic 1 · Q21-Q30
    # ------------------------------------------------------------------ #
    {
        "id": 21,
        "category": D3,
        "task": "3.1",
        "type": "single",
        "question": "A company is using Amazon Bedrock to build a customer-facing AI assistant to "
                    "handle sensitive customer inquiries. The company must use defense-in-depth "
                    "safety controls to block sophisticated prompt injection attacks. The company "
                    "must keep audit logs of all safety interventions. The AI assistant must have "
                    "cross-Region failover capabilities.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure Amazon Bedrock guardrails to use content filters to protect against prompt "
            "injection attacks. Set the content filters to high. Use a guardrail profile to "
            "implement cross-Region guardrail inference. Use Amazon CloudWatch Logs with custom "
            "metrics to capture detailed guardrail intervention events.",
            "B. Configure Amazon Bedrock guardrails to use content filters to protect against prompt "
            "injection attacks. Set the content filters to high. Use AWS WAF to block suspicious "
            "inputs. Use AWS CloudTrail to log API calls for audits.",
            "C. Deploy Amazon Comprehend custom classification to detect prompt injection attacks. "
            "Use Amazon API Gateway to validate requests. Use Amazon CloudWatch Logs with custom "
            "metrics to capture detailed intervention events.",
            "D. Configure Amazon Bedrock guardrails to use custom content filters to protect against "
            "harmful content. Set the content filters to high. Use word filters to protect against "
            "known attack patterns. Configure cross-Region guardrail replication to provide "
            "failover capabilities. Store logs in AWS CloudTrail for compliance auditing.",
        ],
        "answer": "A. Configure Amazon Bedrock guardrails to use content filters to protect against "
                  "prompt injection attacks. Set the content filters to high. Use a guardrail "
                  "profile to implement cross-Region guardrail inference. Use Amazon CloudWatch Logs "
                  "with custom metrics to capture detailed guardrail intervention events.",
        "explanation": "Match each requirement to a native feature: the **prompt-attack content "
                       "filter** (jailbreak / prompt injection) at high strength; **cross-Region "
                       "guardrail inference** via a guardrail profile for failover; and **CloudWatch "
                       "Logs + custom metrics** capturing guardrail *intervention* events as the audit "
                       "log.\n\n"
                       "**B** WAF inspects HTTP patterns, not prompt semantics, and CloudTrail doesn't "
                       "record safety interventions. **C** a custom Comprehend classifier is custom "
                       "work. **D** 'cross-Region guardrail replication' isn't a feature (the real one "
                       "is guardrail profiles), word filters only catch known strings, and CloudTrail "
                       "isn't the intervention log.",
        "reference": f"{_BR}/guardrails-cross-region.html",
        "votes": {"A": 75, "B": 6, "D": 13, "other": 6},
        "note": 'CertyIQ key says B (guardrail + AWS WAF + CloudTrail). Kept A (community vote 75%): B has no'
                " cross-Region failover, WAF can't detect semantic prompt injection, and CloudTrail doesn't "
                'record guardrail interventions.',
    },
    {
        "id": 22,
        "category": D5,
        "task": "5.1",
        "type": "single",
        "question": "A company is designing a canary deployment strategy for a payment processing API. "
                    "The system must support automated gradual traffic shifting between multiple "
                    "Amazon Bedrock models based on real-time inference metrics, historical traffic "
                    "patterns, and service health. The solution must be able to gradually increase "
                    "traffic to new model versions. The system must increase traffic if metrics "
                    "remain healthy and decrease traffic if the performance degrades below acceptable "
                    "thresholds.\n"
                    "The company needs to comprehensively monitor inference latency and error rates "
                    "during the deployment phase. The company must also be able to halt deployments "
                    "and revert to a previous model version without any manual intervention.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon Bedrock with provisioned throughput to host the versions of the model. "
            "Configure an Amazon EventBridge rule to invoke an AWS Step Functions workflow when a "
            "new model version is released. Configure the workflow to shift traffic in stages, wait "
            "for a specified time period, and invoke an AWS Lambda function to check Amazon "
            "CloudWatch performance metrics. Configure the workflow to increase traffic if the "
            "metrics meet thresholds and to trigger a traffic rollback if performance metrics fall "
            "below thresholds.",
            "B. Use AWS Lambda functions to invoke various Amazon Bedrock model versions. Use an "
            "Amazon API Gateway HTTP API with stage variables and weighted routing to shift traffic "
            "gradually to new model versions. Use Amazon CloudWatch to monitor performance metrics. "
            "Use external logic to adjust traffic between model versions and to roll back if "
            "performance falls below thresholds.",
            "C. Use Amazon SageMaker AI endpoint variants to represent multiple Amazon Bedrock model "
            "versions. Use variant weights to shift traffic. Use Amazon CloudWatch to monitor "
            "performance metrics. Use SageMaker Model Monitor to trigger AWS Lambda functions to "
            "roll back a model deployment if performance drops below a specified threshold. "
            "Configure an Amazon EventBridge rule to roll back model deployments if an anomaly is "
            "detected.",
            "D. Use Amazon OpenSearch Service to track inference logs. Configure OpenSearch Service "
            "to invoke an AWS Systems Manager Automation runbook to update Amazon Bedrock model "
            "endpoints to shift traffic based on the inference logs.",
        ],
        "answer": "A. Use Amazon Bedrock with provisioned throughput to host the versions of the "
                  "model. Configure an Amazon EventBridge rule to invoke an AWS Step Functions "
                  "workflow when a new model version is released. Configure the workflow to shift "
                  "traffic in stages, wait for a specified time period, and invoke an AWS Lambda "
                  "function to check Amazon CloudWatch performance metrics. Configure the workflow "
                  "to increase traffic if the metrics meet thresholds and to trigger a traffic "
                  "rollback if performance metrics fall below thresholds.",
        "explanation": "Bedrock has no built-in weighted traffic shifting, so the canary must be "
                       "orchestrated: **Step Functions** stages the traffic percentage, waits, has a "
                       "**Lambda check CloudWatch latency/error metrics**, then either ramps up or "
                       "**automatically rolls back** — no manual step. EventBridge kicks it off on a "
                       "new version.\n\n"
                       "**B** 'external logic' means manual/custom adjustment. **C** SageMaker "
                       "endpoint variants don't represent Bedrock models, and Model Monitor tracks "
                       "ML data/quality drift. **D** OpenSearch → Systems Manager can't update 'Bedrock "
                       "endpoints' (there are none) and is not a deployment controller.",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html",
        "votes": {"A": 82, "B": 9, "C": 9},
    },
    {
        "id": 23,
        "category": D5,
        "task": "5.2",
        "type": "single",
        "question": "A financial services company uses an AI application to process financial "
                    "documents by using Amazon Bedrock. During business hours, the application "
                    "handles approximately 10,000 requests each hour, which requires consistent "
                    "throughput.\n"
                    "The company uses the CreateProvisionedModelThroughput API to purchase "
                    "provisioned throughput. Amazon CloudWatch metrics show that the provisioned "
                    "capacity is unused while on-demand requests are being throttled. The company "
                    "finds the following code in the application:\n"
                    "python response = bedrock_runtime.invoke_model(modelId=\"anthropic.claude-v2\", "
                    "body=json.dumps(payload))\n"
                    "The company needs the application to use the provisioned throughput and to "
                    "resolve the throttling issues.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Increase the number of model units (MUs) in the provisioned throughput "
            "configuration.",
            "B. Replace the model ID parameter with the ARN of the provisioned model that the "
            "CreateProvisionedModelThroughput API returns.",
            "C. Add exponential backoff retry logic to handle throttling exceptions during peak "
            "hours.",
            "D. Modify the application to use the InvokeModelWithResponseStream API instead of the "
            "InvokeModel API.",
        ],
        "answer": "B. Replace the model ID parameter with the ARN of the provisioned model that the "
                  "CreateProvisionedModelThroughput API returns.",
        "explanation": "The code calls the **base model ID** (`anthropic.claude-v2`), so requests go "
                       "to on-demand capacity and get throttled while the purchased capacity sits "
                       "idle. To use Provisioned Throughput you must pass the **provisioned model ARN** "
                       "(returned by `CreateProvisionedModelThroughput`) as `modelId`.\n\n"
                       "**A** more MUs just buys more unused capacity. **C** retries paper over "
                       "throttling without using what you paid for. **D** streaming doesn't change "
                       "which capacity pool serves the call.",
        "reference": f"{_BR}/prov-thru-use.html",
        "votes": {"B": 92, "C": 8},
    },
    {
        "id": 24,
        "category": D3,
        "task": "3.4",
        "type": "single",
        "question": "A company is building an AI advisory application by using Amazon Bedrock. The "
                    "application will provide recommendations to customers. The company needs the "
                    "application to explain its reasoning process and cite specific sources for data. "
                    "The application must retrieve information from company data sources and show "
                    "step-by-step reasoning for recommendations. The application must also link data "
                    "claims to source documents and maintain response latency under 3 seconds.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Use Amazon Bedrock Knowledge Bases with source attribution enabled. Use the "
            "Anthropic Claude Messages API with RAG to set high-relevance thresholds for source "
            "documents. Store reasoning and citations in Amazon S3 for auditing purposes.",
            "B. Use Amazon Bedrock with Anthropic Claude models and extended thinking. Configure a "
            "4,000-token thinking budget. Store reasoning traces and citations in Amazon DynamoDB "
            "for auditing purposes.",
            "C. Configure Amazon SageMaker AI with a custom Anthropic Claude model. Use the model's "
            "reasoning parameter and AWS Lambda to process responses. Add source citations from a "
            "separate Amazon RDS database.",
            "D. Use Amazon Bedrock with Anthropic Claude models and chain-of-thought reasoning. "
            "Configure custom retrieval tracking with the Amazon Bedrock Knowledge Bases API. Use "
            "Amazon CloudWatch to monitor response latency metrics.",
        ],
        "answer": "A. Use Amazon Bedrock Knowledge Bases with source attribution enabled. Use the "
                  "Anthropic Claude Messages API with RAG to set high-relevance thresholds for "
                  "source documents. Store reasoning and citations in Amazon S3 for auditing "
                  "purposes.",
        "explanation": "Knowledge Bases return **citations / source attribution** natively, retrieval "
                       "is fast enough for a 3-second target, and it's fully managed — the least "
                       "overhead. Relevance thresholds keep claims tied to strong sources, and S3 "
                       "holds the audit copy (exam-guide Skill 3.4.1: evidence presentation for source "
                       "attribution).\n\n"
                       "**B** a 4,000-token thinking budget can alone blow a 3 s latency target. **C** "
                       "a self-managed SageMaker model + Lambda + RDS is maximum overhead. **D** "
                       "'custom retrieval tracking' rebuilds what attribution gives you.",
        "reference": f"{_BR}/kb-test-retrieve-generate.html",
        "votes": {"A": 50, "B": 28, "D": 22},
        "note": "Disputed (A 50%, B 28%, D 22%). A doesn't obviously show step-by-step reasoning; "
                "B does, but its thinking budget threatens the 3-second limit. The deciding cues "
                "are 'LEAST operational overhead' + 'link claims to source documents' + the latency "
                "ceiling. In the real exam, weigh which requirement the other options violate.",
    },
    {
        "id": 25,
        "category": D4,
        "task": "4.1",
        "type": "single",
        "question": "A financial services company uses multiple foundation models (FMs) through "
                    "Amazon Bedrock for its generative AI (GenAI) applications. To comply with a new "
                    "regulation for GenAI use with sensitive financial data, the company needs a token "
                    "management solution.\n"
                    "The token management solution must proactively alert when applications approach "
                    "model-specific token limits. The solution must also process more than 5,000 "
                    "requests each minute and maintain token usage metrics to allocate costs across "
                    "business units.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Develop model-specific tokenizers in an AWS Lambda function. Configure the Lambda "
            "function to estimate token usage before sending requests to Amazon Bedrock. Configure "
            "the Lambda function to publish metrics to Amazon CloudWatch and trigger alarms when "
            "requests approach thresholds. Store detailed token usage in Amazon DynamoDB to report "
            "costs.",
            "B. Implement Amazon Bedrock Guardrails with token quota policies. Capture metrics on "
            "rejected requests. Configure Amazon EventBridge rules to trigger notifications based "
            "on Amazon Bedrock Guardrails metrics. Use Amazon CloudWatch dashboards to visualize "
            "token usage trends across models.",
            "C. Deploy an Amazon SQS dead-letter queue for failed requests. Configure an AWS Lambda "
            "function to analyze token-related failures. Use Amazon CloudWatch Logs Insights to "
            "generate reports on token usage patterns based on error logs from Amazon Bedrock API "
            "responses.",
            "D. Use Amazon API Gateway to create a proxy for all Amazon Bedrock API calls. Configure "
            "request throttling based on custom usage plans with predefined token quotas. Configure "
            "API Gateway to reject requests that will exceed token limits.",
        ],
        "answer": "A. Develop model-specific tokenizers in an AWS Lambda function. Configure the "
                  "Lambda function to estimate token usage before sending requests to Amazon "
                  "Bedrock. Configure the Lambda function to publish metrics to Amazon CloudWatch and "
                  "trigger alarms when requests approach thresholds. Store detailed token usage in "
                  "Amazon DynamoDB to report costs.",
        "explanation": "'**Proactively** alert when approaching limits' means estimating tokens "
                       "**before** the call (model-specific tokenizer / token counting), publishing "
                       "CloudWatch metrics + alarms, and keeping per-business-unit usage records (e.g. "
                       "DynamoDB) for chargeback. This matches exam-guide Skill 4.1.1 (token estimation "
                       "and tracking).\n\n"
                       "**B** Guardrails have **no token-quota policy** (a feature that doesn't "
                       "exist), and rejected-request metrics are reactive. **C** failure-based "
                       "analysis only fires *after* a limit is hit. **D** API Gateway usage plans "
                       "count requests, not tokens.",
        "reference": f"{_BR}/count-tokens.html",
        "votes": {"A": 83, "D": 17},
    },
    {
        "id": 26,
        "category": D2,
        "task": "2.1",
        "type": "single",
        "question": "A retail company is developing a customer service application that must process "
                    "10,000 daily queries about products, orders, and warranties. The application must "
                    "be able to respond to queries about 50,000 product documents that are updated "
                    "every day. The application must integrate with an order management API to check "
                    "the status of orders and to help process returns. The application must maintain "
                    "context throughout multi-turn interactions with customers. The company must "
                    "collect complete audit trails for application responses.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Deploy a fine-tuned Amazon Bedrock Anthropic Claude model for each product category. "
            "Create AWS Lambda functions to connect each model to the order management API. Store "
            "conversation history in Amazon DynamoDB.",
            "B. Create a custom model that uses continued pre-training on Amazon Bedrock to handle "
            "all product documentation. Set up an Amazon API Gateway REST API that uses AWS Lambda "
            "functions to connect the model to the order management API.",
            "C. Use Amazon SageMaker AI with containers to deploy models. Use Amazon Kendra to "
            "search product documents. Use AWS Step Functions to orchestrate calls to the order "
            "management API.",
            "D. Use an Amazon Bedrock agent with action groups to integrate with the order "
            "management API. Associate an Amazon Bedrock knowledge base with the agent to search "
            "product documentation by using Retrieval Augmentation Generation (RAG). Enable trace "
            "events to capture audit trails.",
        ],
        "answer": "D. Use an Amazon Bedrock agent with action groups to integrate with the order "
                  "management API. Associate an Amazon Bedrock knowledge base with the agent to "
                  "search product documentation by using Retrieval Augmentation Generation (RAG). "
                  "Enable trace events to capture audit trails.",
        "explanation": "Every requirement has a native Bedrock Agents feature: **action groups** "
                       "(order-management API), an attached **knowledge base** (RAG over documents "
                       "that change daily — re-sync, don't retrain), built-in **session memory** for "
                       "multi-turn context, and **trace events** for audit trails.\n\n"
                       "**A/B** fine-tuning or continued pre-training can't keep up with *daily* "
                       "document updates and is costly. **C** self-hosted SageMaker + Kendra + Step "
                       "Functions is the highest-overhead design.",
        "reference": f"{_BR}/trace-events.html",
        "votes": {"A": 17, "D": 83},
    },
    {
        "id": 27,
        "category": D2,
        "task": "2.5",
        "type": "single",
        "question": "An ecommerce company is using Amazon Bedrock to build a generative AI (GenAI) "
                    "application. The application uses AWS Step Functions to orchestrate a multi-agent "
                    "workflow to produce detailed product descriptions. The workflow consists of three "
                    "sequential states: a description generator, a technical specifications validator, "
                    "and a brand voice consistency checker. Each state produces intermediate reasoning "
                    "traces and outputs that are passed to the next state. The application uses an "
                    "Amazon S3 bucket for process storage and to store outputs.\n"
                    "During testing, the company discovers that outputs between Step Functions states "
                    "frequently exceed the 256 KB quota and cause workflow failures.\n"
                    "A GenAI Developer needs to revise the application architecture to efficiently "
                    "handle the Step Functions 256 KB quota and maintain workflow observability. The "
                    "revised architecture must preserve the existing multi-agent reasoning and acting "
                    "(ReAct) pattern.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Store intermediate outputs in Amazon DynamoDB. Pass only references between states. "
            "Create a Map state that retrieves the complete data from DynamoDB when required for "
            "each agent's processing step.",
            "B. Configure an Amazon Bedrock integration to use the S3 bucket URI in the input "
            "parameter for large outputs. Use the ResultPath field and the ResultSelector field to "
            "route S3 references between the agent steps while maintaining the sequential validation "
            "workflow.",
            "C. Use AWS Lambda functions to compress outputs to less than 256 KB before each agent "
            "state. Configure each agent task to decompress the outputs before processing and to "
            "compress results before passing them to the next state.",
            "D. Configure a separate Step Functions state machine to handle each agent's processing. "
            "Use Amazon EventBridge to coordinate the execution flow between state machines. Use S3 "
            "references for the outputs as event data.",
        ],
        "answer": "B. Configure an Amazon Bedrock integration to use the S3 bucket URI in the input "
                  "parameter for large outputs. Use the ResultPath field and the ResultSelector field "
                  "to route S3 references between the agent steps while maintaining the sequential "
                  "validation workflow.",
        "explanation": "The standard fix for the 256 KB payload limit is the **claim-check pattern**: "
                       "keep big payloads in S3 and pass only **references** through state. The "
                       "Step Functions Bedrock integration can read input from and write output to an "
                       "**S3 URI**, and `ResultSelector` / `ResultPath` shape the small pointer that "
                       "flows to the next state — the S3 bucket already exists, so no new service.\n\n"
                       "**A** adds DynamoDB (which has its own 400 KB item limit) and misuses a Map "
                       "state (for iteration). **C** compression is brittle — outputs can still "
                       "outgrow 256 KB. **D** splitting into multiple state machines + EventBridge is a "
                       "redesign that breaks the simple sequential flow.",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/connect-bedrock.html",
        "votes": {"A": 13, "B": 88},
    },
    {
        "id": 28,
        "category": D1,
        "task": "1.4",
        "type": "single",
        "question": "A company provides a service that helps users from around the world discover new "
                    "restaurants. The service has 50 million monthly active users. The company wants "
                    "to implement a semantic search solution across a database that contains 20 "
                    "million restaurants and 200 million reviews. The company currently stores the "
                    "data in a PostgresQL database.\n"
                    "The solution must support complex natural language queries and return results for "
                    "at least 95% of queries within 500 ms. The solution must maintain data freshness "
                    "for restaurant details that update hourly. The solution must also scale "
                    "cost-effectively during peak usage periods.\n"
                    "Which solution will meet these requirements with the LEAST development effort?",
        "options": [
            "A. Migrate the restaurant data to Amazon OpenSearch Service. Implement keyword-based "
            "search rules that use custom analyzers and relevance tuning to find restaurants based "
            "on attributes such as cuisine type, feature, and location. Create Amazon API Gateway "
            "HTTP API endpoints to transform user queries into structured search parameters.",
            "B. Migrate the restaurant data to Amazon OpenSearch Service. Use a foundation model (FM) "
            "in Amazon Bedrock to generate vector embeddings from restaurant descriptions, reviews, "
            "and menu items. When users submit natural language queries, convert the queries to "
            "embeddings by using the same FM. Perform k-nearest neighbors (k-NN) searches to find "
            "semantically similar results.",
            "C. Keep the restaurant data in PostgresQL and implement a pgvector extension. Use a "
            "foundation model (FM) in Amazon Bedrock to generate vector embeddings from restaurant "
            "data. Store the vector embeddings directly in PostgreSQL. Create an AWS Lambda function "
            "to convert natural language queries to vector representations by using the same FM. "
            "Configure the Lambda function to perform similarity searches within the database.",
            "D. Migrate restaurant data to an Amazon Bedrock knowledge base by using a custom "
            "ingestion pipeline. Configure the knowledge base to automatically generate embeddings "
            "from restaurant information. Use the Amazon Bedrock Retrieve API with built-in vector "
            "search capabilities to query the knowledge base directly by using natural language "
            "input.",
        ],
        "answer": "B. Migrate the restaurant data to Amazon OpenSearch Service. Use a foundation "
                  "model (FM) in Amazon Bedrock to generate vector embeddings from restaurant "
                  "descriptions, reviews, and menu items. When users submit natural language "
                  "queries, convert the queries to embeddings by using the same FM. Perform "
                  "k-nearest neighbors (k-NN) searches to find semantically similar results.",
        "explanation": "Scale is the discriminator: ~220M documents, 50M MAU and a **p95 < 500 ms** "
                       "target. OpenSearch's distributed k-NN (sharded, scalable, near-real-time "
                       "indexing for hourly updates) with Bedrock embeddings delivers semantic search "
                       "at that scale. Use the **same embedding model** for documents and queries.\n\n"
                       "**A** keyword rules are not semantic search. **C** pgvector in a single "
                       "PostgreSQL won't hold p95 < 500 ms at this vector count and traffic without "
                       "heavy tuning. **D** a custom ingestion pipeline into a knowledge base is the "
                       "less natural fit at this scale and gives less control over index tuning.",
        "reference": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html",
        "votes": {"A": 10, "B": 70, "D": 20},
        "note": "Compare with Q6, where Knowledge Bases + OpenSearch Serverless won because the "
                "stem stressed *minimal operational overhead* at ~10M vectors. Here the stem stresses "
                "*scale + latency* (~220M items, p95 < 500 ms), so the direct OpenSearch route is "
                "preferred. D (20%) is the credible rival.",
    },
    {
        "id": 29,
        "category": D5,
        "task": "5.2",
        "type": "single",
        "question": "A medical company uses Amazon Bedrock to power a clinical documentation "
                    "summarization system. The system produces inconsistent summaries when handling "
                    "complex clinical documents. The system performed well on simple clinical "
                    "documents.\n"
                    "The company needs a solution that diagnoses inconsistencies, compares prompt "
                    "performance against established metrics, and maintains historical records of "
                    "prompt versions.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Create multiple prompt variants by using Prompt management in Amazon Bedrock. "
            "Manually test the prompts with simple clinical documents. Deploy the highest performing "
            "version by using the Amazon Bedrock console.",
            "B. Implement version control for prompts in a code repository with a test suite that "
            "contains complex clinical documents and quantifiable evaluation metrics. Use an "
            "automated testing framework to compare prompt versions and document performance "
            "patterns.",
            "C. Deploy each new prompt version to separate Amazon Bedrock API endpoints. Split "
            "production traffic between the endpoints. Configure Amazon CloudWatch to capture "
            "response metrics and user feedback for automatic version selection.",
            "D. Create a custom prompt evaluation flow in Amazon Bedrock Flows that applies the same "
            "clinical document inputs to different prompt variants. Use Amazon Comprehend Medical to "
            "analyze and score the factual accuracy of each version.",
        ],
        "answer": "B. Implement version control for prompts in a code repository with a test suite "
                  "that contains complex clinical documents and quantifiable evaluation metrics. Use "
                  "an automated testing framework to compare prompt versions and document "
                  "performance patterns.",
        "explanation": "The three asks are **diagnose** (a test set that includes the *complex* "
                       "documents that fail), **compare against established metrics** (quantifiable, "
                       "automated evaluation), and **keep history** (version control). B delivers all "
                       "three systematically — exam-guide Skill 5.2.3: prompt testing frameworks and "
                       "version comparison.\n\n"
                       "**A** tests only *simple* documents (the cases that already work) and is "
                       "manual. **C** experiments on production traffic and auto-selects from noisy "
                       "feedback. **D** Comprehend Medical extracts medical entities — it doesn't "
                       "score the factual accuracy of summaries.",
        "reference": f"{_BR}/prompt-management.html",
        "votes": {"A": 7, "B": 57, "D": 36},
        "note": "Disputed (B 57%, D 36%). D is attractive because Flows can run the same inputs "
                "across variants, but its scoring tool (Comprehend Medical) doesn't evaluate summary "
                "accuracy. B is the only option that tests the *failing* case (complex documents) "
                "with measurable metrics and keeps version history.",
    },
    {
        "id": 30,
        "category": D3,
        "task": "3.1",
        "type": "multi",
        "question": "A company uses Amazon Bedrock to generate technical content for customers. The "
                    "company has recently experienced a surge in hallucination outputs when the "
                    "company's model generates summaries of long technical documents. The model "
                    "outputs include inaccurate or fabricated details. The company's current solution "
                    "uses a large foundation model (FM) with a basic one-shot prompt that includes the "
                    "full document in a single input.\n"
                    "The company needs a solution that will reduce hallucinations and meet factual "
                    "accuracy goals. The solution must process more than 1,000 documents each hour and "
                    "deliver summaries within 3 seconds for each document.\n"
                    "Which combination of solutions will meet these requirements? (Choose two.)",
        "options": [
            "A. Implement zero-shot chain-of-thought (CoT) instructions that require step-by-step "
            "reasoning with explicit fact verification before the model generates each summary.",
            "B. Use Retrieval Augmented Generation (RAG) with an Amazon Bedrock knowledge base. "
            "Apply semantic chunking and tuned embeddings to ground summaries in source content.",
            "C. Configure Amazon Bedrock guardrails to block any generated output that matches "
            "patterns that are associated with hallucinated content.",
            "D. Increase the temperature parameter in Amazon Bedrock.",
            "E. Prompt the Amazon Bedrock model to summarize each full document in one pass.",
        ],
        "answer": [
            "A. Implement zero-shot chain-of-thought (CoT) instructions that require step-by-step "
            "reasoning with explicit fact verification before the model generates each summary.",
            "B. Use Retrieval Augmented Generation (RAG) with an Amazon Bedrock knowledge base. "
            "Apply semantic chunking and tuned embeddings to ground summaries in source content.",
        ],
        "explanation": "Attack hallucinations from two sides: **ground** the output in source text "
                       "(B: RAG with semantic chunking so the model works from the relevant passages "
                       "instead of one giant input) and **improve the reasoning** (A: CoT with explicit "
                       "fact-verification steps).\n\n"
                       "**C** guardrails can't block outputs by matching 'hallucination patterns' "
                       "(the real feature is the contextual grounding check against a provided "
                       "source). **D** a higher temperature *increases* randomness and fabrication. "
                       "**E** is the existing one-pass approach that caused the problem.",
        "reference": f"{_BR}/guardrails-contextual-grounding-check.html",
        "votes": {"AB": 88, "BC": 6, "C": 6},
        "note": 'Mildly disputed. The contextual grounding check *is* a real Guardrails feature, but option C'
                " describes pattern-matching on 'hallucinated content', which is not how it works — that is "
                'why C is out. CertyIQ key says B + C. Kept A + B (community vote 88%): option C describes '
                "pattern-matching on 'hallucinated content', which is not how guardrails work (the real "
                'feature is the contextual grounding check).'
    },

    # ------------------------------------------------------------------ #
    # Exam A · Topic 1 · Q31-Q40 (from screenshots — source answers were hidden,
    # so every answer below is derived from the exam guide + AWS docs; no vote data)
    # ------------------------------------------------------------------ #
    {
        "id": 31,
        "category": D4,
        "task": "4.3",
        "type": "single",
        "question": "A company has a recommendation system. The system's applications run on Amazon "
                    "EC2 instances. The applications make API calls to Amazon Bedrock foundation "
                    "models (FMs) to analyze customer behavior and generate personalized product "
                    "recommendations.\n"
                    "The system is experiencing intermittent issues. Some recommendations do not match "
                    "customer preferences. The company needs an observability solution to monitor "
                    "operational metrics and detect patterns of operational performance degradation "
                    "compared to established baselines. The solution must also generate alerts with "
                    "correlation data within 10 minutes when FM behavior deviates from expected "
                    "patterns.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure Amazon CloudWatch Container Insights for the application infrastructure. "
            "Set up CloudWatch alarms for latency thresholds. Add custom metrics for token counts by "
            "using the CloudWatch embedded metric format. Create CloudWatch dashboards to visualize "
            "the data.",
            "B. Implement AWS X-Ray to trace requests through the application components. Enable "
            "CloudWatch Logs Insights for error pattern detection. Set up AWS CloudTrail to monitor "
            "all API calls to Amazon Bedrock. Create custom dashboards in Amazon QuickSight.",
            "C. Enable Amazon CloudWatch Application Insights for the application resources. Create "
            "custom metrics for recommendation quality, token usage, and response latency by using "
            "the CloudWatch embedded metric format with dimensions for request types and user "
            "segments. Configure CloudWatch anomaly detection on the model metrics. Establish log "
            "pattern analysis by using CloudWatch Logs Insights.",
            "D. Use Amazon OpenSearch Service with the Observability plugin. Ingest model metrics and "
            "logs by using Amazon Kinesis. Create custom Piped Processing Language (PPL) queries to "
            "analyze model behavior patterns. Establish operational dashboards to visualize "
            "anomalies in real time.",
        ],
        "answer": "C. Enable Amazon CloudWatch Application Insights for the application resources. "
                  "Create custom metrics for recommendation quality, token usage, and response "
                  "latency by using the CloudWatch embedded metric format with dimensions for "
                  "request types and user segments. Configure CloudWatch anomaly detection on the "
                  "model metrics. Establish log pattern analysis by using CloudWatch Logs Insights.",
        "explanation": "Key phrases: **'compared to established baselines'** → **CloudWatch anomaly "
                       "detection** (learns a baseline and flags deviations); **'FM behavior deviates'** "
                       "→ custom GenAI metrics (recommendation quality, token usage, latency) via the "
                       "**embedded metric format**; **'correlation data'** → **Application Insights** "
                       "correlates metrics/log anomalies across the EC2 application resources; Logs "
                       "Insights adds log-pattern analysis. All native, near-real-time (well under "
                       "10 minutes).\n\n"
                       "**A** uses fixed latency thresholds (no baseline) and Container Insights is for "
                       "containers, not EC2 apps. **B** X-Ray/CloudTrail/QuickSight give traces and "
                       "audit but no baseline-based alerting. **D** is a heavy, self-assembled "
                       "pipeline (Kinesis + OpenSearch + PPL) — high overhead.",
        "reference": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-application-insights.html",
        "note": "Answer derived from the stem's cues (baseline → anomaly detection; correlation → "
                "Application Insights). High confidence — C is the only option with both.",
    },
    {
        "id": 32,
        "category": D5,
        "task": "5.2",
        "type": "single",
        "question": "An enterprise application uses an Amazon Bedrock foundation model (FM) to "
                    "process and analyze 50 to 200 pages of technical documents. Users are "
                    "experiencing inconsistent responses and receiving truncated outputs when "
                    "processing documents that exceed the FM's context window limits.\n"
                    "Which solution will resolve this problem?",
        "options": [
            "A. Configure fixed-size chunking at 4,000 tokens for each chunk with 20% overlap. Use "
            "application-level logic to link multiple chunks sequentially until the FM's maximum "
            "context window of 200,000 tokens is reached before making inference calls.",
            "B. Use hierarchical chunking with parent chunks of 8,000 tokens and child chunks of "
            "2,000 tokens. Use Amazon Bedrock Knowledge Bases built-in retrieval to automatically "
            "select relevant parent chunks based on query context. Configure overlap tokens to "
            "maintain semantic continuity.",
            "C. Use semantic chunking with a breakpoint percentile threshold of 95% and a buffer "
            "size of 3 sentences. Use the Amazon Bedrock RetrieveAndGenerate API call to "
            "dynamically select the most relevant chunks based on embedding similarity scores.",
            "D. Create a pre-processing AWS Lambda function that analyzes document token count by "
            "using the FM's tokenizer. Configure the Lambda function to split documents into equal "
            "segments that fit within 80% of the context window. Configure the Lambda function to "
            "process each segment independently before aggregating the results.",
        ],
        "answer": 'C. Use semantic chunking with a breakpoint percentile threshold of 95% and a buffer size of '
                  '3 sentences. Use the Amazon Bedrock RetrieveAndGenerate API call to dynamically select the '
                  'most relevant chunks based on embedding similarity scores.',
        "explanation": 'Truncation and inconsistent answers come from forcing a 50–200-page document into the '
                       'context window. Fix it by retrieving **only the relevant parts**: **semantic chunking** '
                       'splits at meaning boundaries (the breakpoint percentile threshold decides where topics '
                       'shift; the buffer size adds neighbouring sentences for context) so each chunk is '
                       'self-contained, and **RetrieveAndGenerate** selects the most relevant chunks by embedding '
                       'similarity and generates from just those — always within the context window.\\n'
                       '\\n'
                       '**A** still tries to fill the 200,000-token window (the cause of the truncation). **D** '
                       'processes equal segments independently, so cross-segment context is lost and the aggregated '
                       'answer is inconsistent. **B** (hierarchical parent/child chunks) is plausible, but C is the '
                       "more direct match for 'dynamically select the most relevant chunks'.",
        "reference": f"{_BR}/kb-chunking.html",
        "note": 'Answer changed to C to match the CertyIQ answer key (my first derivation was B). B '
                '(hierarchical chunking) is the close alternative. Cross-check: the Bedrock API limits '
                "semantic-chunking bufferSize to 0-1. Option C's 'buffer size of 3 sentences' matches "
                'bufferSize 1 (previous + current + next sentence), so C is still a valid configuration.'
    },
    {
        "id": 33,
        "category": D2,
        "task": "2.2",
        "type": "single",
        "question": "A company is developing a generative AI (GenAI) application that analyzes "
                    "customer service calls in real-time and generates suggested responses for human "
                    "customer service agents. The application must process 500,000 concurrent calls "
                    "during peak hours with less than 200 ms end-to-end latency for each suggestion. "
                    "The company uses existing architecture to transcribe customer call audio "
                    "streams. The application must not exceed a pre-defined monthly compute budget "
                    "and must maintain auto scaling capabilities.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Deploy a large, complex reasoning model on Amazon Bedrock. Purchase provisioned "
            "throughput and optimize for batch processing.",
            "B. Deploy a low-latency, real-time optimized model on Amazon Bedrock. Purchase "
            "provisioned throughput and set up automatic scaling policies.",
            "C. Deploy a large language model (LLM) on an Amazon SageMaker AI real-time endpoint that "
            "uses dedicated GPU instances.",
            "D. Deploy a mid-sized language model on an Amazon SageMaker AI serverless endpoint that "
            "is optimized for batch processing.",
        ],
        "answer": "B. Deploy a low-latency, real-time optimized model on Amazon Bedrock. Purchase "
                  "provisioned throughput and set up automatic scaling policies.",
        "explanation": "Match the model and capacity to the constraints: **<200 ms real-time** → a "
                       "small/fast, latency-optimized model; **massive concurrency with predictable "
                       "cost** → **Provisioned Throughput** (reserved, fixed-price capacity that stays "
                       "within a budget); **auto scaling** → scaling policies on top. Smaller models "
                       "also cost far less per token (exam-guide Skills 2.2.3, 4.1.2).\n\n"
                       "**A** a large reasoning model is slow and expensive, and *batch* optimisation "
                       "contradicts real-time. **C** large LLMs on dedicated GPUs blow the budget and "
                       "add management. **D** batch-optimised and serverless cold starts can't hold "
                       "200 ms.",
        "reference": f"{_BR}/prov-throughput.html",
        "note": "Answer derived. High confidence — three options contradict 'real-time' or 'budget'.",
    },
    {
        "id": 34,
        "category": D5,
        "task": "5.1",
        "type": "multi",
        "question": "An ecommerce company is building an internal platform to develop generative AI "
                    "applications by using Amazon Bedrock foundation models (FMs). Developers need to "
                    "select models based on evaluations that are aligned to ecommerce use cases. The "
                    "platform must display accuracy metrics for text generation and summarization in "
                    "dashboards. The company has custom ecommerce datasets to use as standardized "
                    "evaluation inputs.\n"
                    "Which combination of steps will meet these requirements with the LEAST "
                    "operational overhead? (Choose two.)",
        "options": [
            "A. Import the datasets to an Amazon S3 bucket. Provide appropriate IAM permissions and "
            "cross-origin resource sharing (CORS) permissions to give the evaluation jobs access to "
            "the datasets.",
            "B. Import the datasets to an Amazon S3 bucket. Provide appropriate IAM permissions and a "
            "VPC endpoint configuration to give the evaluation jobs access to the datasets.",
            "C. Configure an AWS Lambda function to create model evaluation jobs on a schedule in the "
            "Amazon Bedrock console. Provide the URI of the S3 bucket that contains the datasets as "
            "an input. Configure the evaluation jobs to measure the real world knowledge (RWK) score "
            "for text generation and BERT Score for summarization. Configure a second Lambda function "
            "to check the status of the jobs and publish custom logs to Amazon CloudWatch. Create a "
            "custom Amazon CloudWatch Logs Insights dashboard.",
            "D. Use Amazon SageMaker Clarify on a schedule to create model evaluation jobs. Use open "
            "source frameworks to create and run standardized evaluations. Publish results to Amazon "
            "CloudWatch namespaces. Use the word error rate score for text generation and toxicity "
            "for summarization as metrics for accuracy. Configure an AWS Lambda function to check the "
            "status of the jobs and publish custom logs to CloudWatch. Create a custom Amazon "
            "CloudWatch Logs Insights dashboard.",
            "E. Run an Amazon SageMaker AI notebook job on a schedule by using the fmevals or ragas "
            "framework to run evaluations that use the datasets in the S3 bucket. Write Python code "
            "in the notebook that makes direct InvokeModel API calls to the FMs and processes their "
            "responses for evaluation. Publish job status and results to Amazon CloudWatch Logs to "
            "measure the real world knowledge (RWK) score for text generation and toxicity for "
            "summarization as metrics for accuracy. Create a custom CloudWatch Logs Insights "
            "dashboard.",
        ],
        "answer": [
                      'A. Import the datasets to an Amazon S3 bucket. Provide appropriate IAM permissions and '
                      'cross-origin resource sharing (CORS) permissions to give the evaluation jobs access to the '
                      'datasets.',
                      'C. Configure an AWS Lambda function to create model evaluation jobs on a schedule in the '
                      'Amazon Bedrock console. Provide the URI of the S3 bucket that contains the datasets as an '
                      'input. Configure the evaluation jobs to measure the real world knowledge (RWK) score for '
                      'text generation and BERT Score for summarization. Configure a second Lambda function to '
                      'check the status of the jobs and publish custom logs to Amazon CloudWatch. Create a custom '
                      'Amazon CloudWatch Logs Insights dashboard.',
                  ],
        "explanation": 'Use the **managed Bedrock Model Evaluations** feature instead of building an evaluation '
                       'harness. Two parts:\\n'
                       '- **Data access (A):** put the custom datasets in S3 and give the evaluation job IAM access '
                       "to them, plus the CORS configuration that Bedrock's console-based evaluation setup expects "
                       'on the dataset/output buckets.\\n'
                       '- **Running + reporting (C):** Lambda creates scheduled evaluation jobs using the built-in '
                       'accuracy metrics — **RWK score (text generation)** and **BERTScore (summarization)** — and a'
                       ' second Lambda publishes job status/results to CloudWatch for a dashboard.\\n'
                       '\\n'
                       '**B** a VPC endpoint is not part of how Bedrock evaluation jobs read S3 datasets (no AWS '
                       'evaluation doc describes it). **D** Clarify is a bias/explainability tool, and word error '
                       "rate (speech) and toxicity aren't accuracy metrics for these tasks. **E** a self-built "
                       'notebook harness with direct InvokeModel calls is the highest overhead.',
        "reference": f"{_BR}/model-evaluation-prompt-datasets.html",
        "note": "Back to A + C (CertyIQ's key, confirmed from its own page). C is agreed by every source. For"
                ' the other half, a second dump said B and the AWS docs are mixed on CORS: the custom-dataset'
                " page says CORS isn't required for automated jobs, while the console setup guidance lists "
                'CORS on the buckets; no AWS doc found mentions VPC endpoints for dataset access. '
                'Moderate-high confidence in A over B.'
    },
    {
        "id": 35,
        "category": D2,
        "task": "2.1",
        "type": "single",
        "question": "An elevator service company has developed an AI assistant application by using "
                    "Amazon Bedrock. The application generates elevator maintenance recommendations "
                    "to support the company's elevator technicians. The company uses Amazon Kinesis "
                    "Data Streams to collect the elevator sensor data.\n"
                    "New regulatory rules require that a human technician must review all AI-generated "
                    "recommendations. The company needs to establish human oversight workflows to "
                    "review and approve AI recommendations. The company must store all human "
                    "technician review decisions for audit purposes.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Create a custom approval workflow by using AWS Lambda functions and Amazon SQS queues "
            "for human review of AI recommendations. Store all review decisions in Amazon DynamoDB "
            "for audit purposes.",
            "B. Create an AWS Step Functions workflow that has a human approval step that uses the "
            "waitForTaskToken API to pause execution. After a human technician completes a review, "
            "use an AWS Lambda function to call the SendTaskSuccess API that has the approval "
            "decision. Store all review decisions in Amazon DynamoDB.",
            "C. Create an AWS Glue workflow that has a human approval step. After the human "
            "technician review, integrate the application with an AWS Lambda function that calls the "
            "SendTaskSuccess API. Store all human technician review decisions in Amazon DynamoDB.",
            "D. Configure Amazon EventBridge rules with custom event patterns to route AI "
            "recommendations to human technicians for review. Create AWS Glue jobs to process human "
            "technician approval queues. Use Amazon ElastiCache to cache all human technician review "
            "decisions.",
        ],
        "answer": "B. Create an AWS Step Functions workflow that has a human approval step that uses "
                  "the waitForTaskToken API to pause execution. After a human technician completes a "
                  "review, use an AWS Lambda function to call the SendTaskSuccess API that has the "
                  "approval decision. Store all review decisions in Amazon DynamoDB.",
        "explanation": "Human-in-the-loop on AWS = **Step Functions callback pattern**: a task with "
                       "`.waitForTaskToken` pauses the (Standard) workflow with a token; when the "
                       "technician decides, `SendTaskSuccess` / `SendTaskFailure` resumes it. DynamoDB "
                       "durably stores each decision for audit (exam-guide Skill 2.1.5).\n\n"
                       "**A** is the same idea rebuilt by hand (more overhead). **C** `SendTaskSuccess` "
                       "is a Step Functions API — Glue workflows have no human-approval step. **D** "
                       "EventBridge + Glue + a cache (ElastiCache is volatile — wrong for audit data).",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html",
        "note": "Answer derived. High confidence — `waitForTaskToken` + `SendTaskSuccess` is the "
                "textbook human-approval pattern, and C misattributes it to Glue.",
    },
    {
        "id": 36,
        "category": D3,
        "task": "3.2",
        "type": "multi",
        "question": "A bank is building a generative AI (GenAI) application that uses Amazon Bedrock "
                    "to assess loan applications by using scanned financial documents. The application "
                    "must extract structured data from the documents. The application must redact "
                    "personally identifiable information (PII) before inference. The application must "
                    "use foundation models (FMs) to generate approvals. The application must route "
                    "low-confidence document extraction results to human reviewers who are within the "
                    "same AWS Region as the loan applicant.\n"
                    "The company must ensure that the application complies with strict Regional data "
                    "residency and auditability requirements. The application must be able to scale to "
                    "handle 25,000 applications each day and provide 99.9% availability.\n"
                    "Which combination of solutions will meet these requirements? (Choose three.)",
        "options": [
            "A. Deploy Amazon Textract and Amazon Augmented AI (Amazon A2I) within the same Region to "
            "extract relevant data from the scanned documents. Route low-confidence pages to human "
            "reviewers.",
            "B. Use AWS Lambda functions to detect and redact PII from submitted documents before "
            "inference. Apply Amazon Bedrock guardrails to prevent inappropriate or unauthorized "
            "content in model outputs. Configure Region-specific IAM roles to enforce data residency "
            "requirements and to control access to the extracted data.",
            "C. Use Amazon Kendra and Amazon OpenSearch Service to extract field level values "
            "semantically from the uploaded documents before inference.",
            "D. Store uploaded documents in Amazon S3 and apply object metadata. Configure IAM "
            "policies to store original documents within the same Region as each applicant. Enable "
            "object tagging for future audits.",
            "E. Use AWS Glue Data Quality to validate the structured document data. Use AWS Step "
            "Functions to orchestrate a review workflow that includes a prompt engineering step that "
            "transforms validated data into optimized prompts before invoking Amazon Bedrock to "
            "assess loan applications.",
            "F. Use Amazon SageMaker Clarify to generate fairness and bias reports based on model "
            "scoring decisions that Amazon Bedrock makes.",
        ],
        "answer": [
            "A. Deploy Amazon Textract and Amazon Augmented AI (Amazon A2I) within the same Region to "
            "extract relevant data from the scanned documents. Route low-confidence pages to human "
            "reviewers.",
            "B. Use AWS Lambda functions to detect and redact PII from submitted documents before "
            "inference. Apply Amazon Bedrock guardrails to prevent inappropriate or unauthorized "
            "content in model outputs. Configure Region-specific IAM roles to enforce data residency "
            "requirements and to control access to the extracted data.",
            "D. Store uploaded documents in Amazon S3 and apply object metadata. Configure IAM "
            "policies to store original documents within the same Region as each applicant. Enable "
            "object tagging for future audits.",
        ],
        "explanation": "Map each explicit requirement to the service built for it:\n"
                       "- **Extract from scans + route low-confidence results to same-Region human "
                       "reviewers → Textract + Augmented AI (A).** A2I is the managed human-review "
                       "loop triggered by confidence thresholds.\n"
                       "- **Redact PII before inference, guard model output, enforce Regional residency "
                       "and access → B.**\n"
                       "- **Regional storage + auditability → S3 with metadata/tags and Region-bound "
                       "IAM (D).**\n\n"
                       "**C** Kendra/OpenSearch search documents; they are not field extractors for "
                       "scans. **E** validation/prompt-shaping is a nice-to-have, not a stated "
                       "requirement. **F** fairness/bias reporting isn't asked for.",
        "reference": "https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html",
        "note": "Answer derived, moderate confidence (A, B, D vs E). A, B, D each map to an explicit "
                "requirement (extraction + human review; PII redaction + residency; storage + "
                "audit). E is orchestration the stem doesn't ask for; C and F are clearly off-target.",
    },
    {
        "id": 37,
        "category": D2,
        "task": "2.3",
        "type": "single",
        "question": "A software company is using Amazon Q Business to build an AI assistant that allows "
                    "employees to access company information and personal information by using "
                    "natural language prompts. The company stores this information in an Amazon S3 "
                    "bucket.\n"
                    "Each department in the company has a dedicated prefix in the S3 bucket. Each "
                    "object name includes the S3 prefix of the department that it belongs to. Each "
                    "department can belong to only a single group in AWS IAM Identity Center. Each "
                    "employee belongs to a single department.\n"
                    "The company configures Amazon Q Business to access data stored in an S3 bucket as "
                    "a data source. The company needs to ensure that the AI assistant respects access "
                    "controls based on the user's IAM Identity Center group membership.\n"
                    "Which solution will meet this requirement with the LEAST operational overhead?",
        "options": [
            "A. Create a JSON file named acl.json in each department folder. In each file, create "
            "access control entries that specify the IAM Identity Center group that should have "
            "access to that department's data. Indicate the location of the JSON file in the Access "
            "Control section of the data source settings.",
            "B. Create a single JSON file named acl.json at the top level of the S3 bucket. Add "
            "access control entries that map each department's S3 prefix to its corresponding IAM "
            "Identity Center group. Indicate the location of the JSON file in the Access Control "
            "section of the data source settings.",
            "C. For each IAM Identity Center group, create a separate permissions set that denies "
            "access to all prefixes in the S3 bucket. Add a StringNotEquals condition key to the "
            "permissions set for each group that specifies the department each group is associated "
            "with. Attach the permissions sets to the Identity Center groups.",
            "D. Create a metadata file named metadata.json at the top level of the S3 bucket. Add an "
            "AccessControlList object to the file that specifies the S3 path of each department's "
            "prefix. Specify the IAM Identity Center group that should have access to each "
            "department's prefix. Reference the file location in the data source metadata settings.",
        ],
        "answer": "B. Create a single JSON file named acl.json at the top level of the S3 bucket. Add "
                  "access control entries that map each department's S3 prefix to its corresponding "
                  "IAM Identity Center group. Indicate the location of the JSON file in the Access "
                  "Control section of the data source settings.",
        "explanation": "The Amazon Q Business S3 connector reads **one ACL configuration file** "
                       "(JSON, stored in the same bucket) whose entries each carry a `keyPrefix` and a "
                       "list of `aclEntries` (name, `USER`/`GROUP`, `ALLOW`/`DENY`). A prefix entry "
                       "applies to every file under that path, so one file with one entry per "
                       "department maps prefixes to Identity Center groups — the least overhead. The "
                       "file's location is set in the data source's access-control settings.\n\n"
                       "**A** the data source takes one ACL file path, not one per folder. **C** IAM "
                       "permission sets govern AWS API access, not what Q Business returns from "
                       "indexed documents. **D** per-document metadata files carry ACLs for "
                       "individual documents, not a bucket-wide prefix map.",
        "reference": "https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/s3-user-management.html",
        "note": "Answer verified against the Amazon Q Business S3 ACL documentation. Remember: "
                "prefixes *not* listed in the ACL file are accessible to ALL users. (Q Business is "
                "closed to new customers; AWS points to Amazon Quick, but the exam guide still lists "
                "both.)",
    },
    {
        "id": 38,
        "category": D3,
        "task": "3.1",
        "type": "single",
        "question": "A healthcare company is using Amazon Bedrock to build a system to help "
                    "practitioners make clinical decisions. The system must provide treatment "
                    "recommendations to physicians based only on approved medical documentation and "
                    "must cite specific sources. The system must not hallucinate or produce "
                    "factually incorrect information.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Integrate Amazon Bedrock with Amazon Kendra to retrieve approved documents. Implement "
            "custom post-processing to compare generated responses against source documents and to "
            "include citations.",
            "B. Deploy an Amazon Bedrock knowledge base and connect it to approved clinical source "
            "documents. Use the Amazon Bedrock RetrieveAndGenerate API to return citations from the "
            "knowledge base.",
            "C. Use Amazon Bedrock and Amazon Comprehend Medical to extract medical entities. "
            "Implement verification logic against a medical terminology database.",
            "D. Use an Amazon Bedrock knowledge base with Retrieve API calls and InvokeModel API calls "
            "to retrieve approved clinical source documents. Implement verification logic to compare "
            "against retrieved sources and to cite sources.",
        ],
        "answer": "B. Deploy an Amazon Bedrock knowledge base and connect it to approved clinical "
                  "source documents. Use the Amazon Bedrock RetrieveAndGenerate API to return "
                  "citations from the knowledge base.",
        "explanation": "'Based **only** on approved documentation' + 'cite sources' + 'least overhead' "
                       "= a managed **Knowledge Base** with **RetrieveAndGenerate**, which retrieves "
                       "from the approved corpus, generates a grounded answer and returns "
                       "**citations** in one call — no custom verification code.\n\n"
                       "**A** and **D** hand-build the compare-and-cite logic that RetrieveAndGenerate "
                       "already provides. **C** Comprehend Medical extracts entities; it doesn't "
                       "ground or cite answers.",
        "reference": f"{_BR}/kb-test-retrieve-generate.html",
        "note": "Answer derived. High confidence — B and D differ only in whether you write the "
                "citation/verification logic yourself.",
    },
    {
        "id": 39,
        "category": D2,
        "task": "2.4",
        "type": "single",
        "question": "A financial services company is developing a real-time generative AI (GenAI) "
                    "assistant to support human call center agents. The GenAI assistant must "
                    "transcribe live customer speech, analyze context, and provide incremental "
                    "suggestions to call center agents while a customer is still speaking. To "
                    "preserve responsiveness, the GenAI assistant must maintain end-to-end latency "
                    "under 1 second from speech to initial response display. The architecture must "
                    "use only managed AWS services and must support bidirectional streaming to ensure "
                    "that call center agents receive updates in real time.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use the Amazon Transcribe streaming API to transcribe calls. Pass the text to Amazon "
            "Comprehend to perform sentiment analysis. Feed the results to Anthropic Claude on "
            "Amazon Bedrock by using the InvokeModel API. Store results in Amazon DynamoDB. Use a "
            "WebSocket API to display the results.",
            "B. Use Amazon Transcribe streaming with partial results enabled to deliver fragments of "
            "transcribed text before customers finish speaking. Forward text fragments to Amazon "
            "Bedrock by using the InvokeModelWithResponseStream API. Stream responses to call center "
            "agents through an Amazon API Gateway WebSocket API.",
            "C. Use Amazon Transcribe batch processing to convert calls to text. Pass complete "
            "transcripts to Anthropic Claude on Amazon Bedrock by using the ConverseStream API. "
            "Return responses through an Amazon Lex chatbot interface that call center agents can "
            "access from their work computers.",
            "D. Use the Amazon Transcribe streaming API with an AWS Lambda function to transcribe "
            "each audio segment. Configure the Lambda function to call the Amazon Titan Embeddings "
            "model on Amazon Bedrock by using the InvokeModel API. Configure the Lambda function to "
            "publish results to an Amazon SNS topic. Subscribe the call center agents to the SNS "
            "topic.",
        ],
        "answer": "B. Use Amazon Transcribe streaming with partial results enabled to deliver "
                  "fragments of transcribed text before customers finish speaking. Forward text "
                  "fragments to Amazon Bedrock by using the InvokeModelWithResponseStream API. "
                  "Stream responses to call center agents through an Amazon API Gateway WebSocket "
                  "API.",
        "explanation": "Streaming at every hop: **Transcribe streaming with partial results** emits "
                       "text *while the customer is still speaking*; **InvokeModelWithResponseStream** "
                       "returns tokens incrementally; an **API Gateway WebSocket** pushes them to the "
                       "agent over a bidirectional connection — meeting the sub-second 'initial "
                       "response' goal with managed services only.\n\n"
                       "**A** waits for full InvokeModel responses and adds sentiment/DynamoDB hops. "
                       "**C** *batch* transcription can't run during the call, and Lex is the wrong "
                       "UI. **D** Titan Embeddings produces vectors, not suggestions, and SNS isn't "
                       "bidirectional streaming.",
        "reference": "https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html",
        "note": "Answer derived. High confidence — only B is streaming end to end.",
    },
    {
        "id": 40,
        "category": D3,
        "task": "3.1",
        "type": "single",
        "question": "A media company is launching a platform that allows thousands of users every "
                    "hour to upload images and text content. The platform uses Amazon Bedrock to "
                    "process the uploaded content to generate creative compositions.\n"
                    "The company needs a solution to ensure that the platform does not process or "
                    "produce inappropriate content. The platform must not expose personally "
                    "identifiable information (PII) in the compositions. The solution must integrate "
                    "with the company's existing Amazon S3 storage workflow.\n"
                    "Which solution will meet these requirements with the LEAST infrastructure "
                    "management overhead?",
        "options": [
            "A. Enable the Enhanced Monitoring tool. Use an Amazon CloudWatch alarm to filter traffic "
            "to the platform. Use Amazon Comprehend PII detection to pre-process the data. Create a "
            "CloudWatch alarm to monitor for Amazon Comprehend PII detection events. Create an AWS "
            "Step Functions workflow that includes an Amazon Rekognition image moderation step.",
            "B. Use an Amazon API Gateway HTTP API with request validation templates to screen content "
            "before storing the uploaded content in Amazon S3. Use Amazon SageMaker AI to build "
            "custom content moderation models that process content before sending the processed "
            "content to Amazon Bedrock.",
            "C. Create an Amazon Cognito user pool that uses pre-authentication AWS Lambda functions "
            "to run content moderation checks. Use Amazon Textract to filter text content and Amazon "
            "Rekognition to filter image content before allowing users to upload content to the "
            "platform.",
            "D. Create an AWS Step Functions workflow that uses built-in Amazon Bedrock guardrails to "
            "filter content. Use Amazon Comprehend PII detection to pre-process the content. Use "
            "Amazon Rekognition image moderation.",
        ],
        "answer": "D. Create an AWS Step Functions workflow that uses built-in Amazon Bedrock "
                  "guardrails to filter content. Use Amazon Comprehend PII detection to pre-process "
                  "the content. Use Amazon Rekognition image moderation.",
        "explanation": "Pick the managed service for each safety job and orchestrate with a "
                       "serverless workflow: **Bedrock Guardrails** (inappropriate text in/out), "
                       "**Comprehend PII detection** (find/mask PII before processing) and "
                       "**Rekognition image moderation** (unsafe images), tied together with **Step "
                       "Functions** — defence in depth (exam-guide Skill 3.1.4) with no models or "
                       "servers to run.\n\n"
                       "**A** 'Enhanced Monitoring' and a CloudWatch alarm 'filtering traffic' aren't "
                       "moderation controls. **B** builds custom moderation models on SageMaker — "
                       "maximum overhead. **C** Textract extracts text; it doesn't moderate it, and "
                       "Cognito pre-authentication triggers run at sign-in, not on uploads.",
        "reference": "https://docs.aws.amazon.com/rekognition/latest/dg/moderation.html",
        "note": "Answer derived. High confidence — D is the only option using purpose-built managed "
                "moderation for text, PII and images.",
    },

    # ------------------------------------------------------------------ #
    # Exam A · Topic 1 · Q41-Q50 (from screenshots — answers derived, no vote data)
    # ------------------------------------------------------------------ #
    {
        "id": 41,
        "category": D2,
        "task": "2.5",
        "type": "single",
        "question": "A company has set up Amazon Q Developer Pro licenses for all developers at the "
                    "company. The company maintains a list of approved resources that developers must "
                    "use when developing applications. The approved resources include internal "
                    "libraries, proprietary algorithmic techniques, and sample code with approved "
                    "styling.\n"
                    "A new team of developers is using Amazon Q Developer to develop a new Java-based "
                    "application. The company must ensure that the new developer team uses the "
                    "company's approved resources. The company does not want to make project-level "
                    "modifications.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Create a Git repository that contains all of the approved internal libraries, "
            "algorithms, and code samples. Include this Git repository in the application project "
            "locally as part of the workspace. Ensure that the developers use the @workspace "
            "context to retrieve suggestions from the Git repository.",
            "B. In the project root folder, create a folder named .amazonq/rules. Add the approved "
            "internal libraries, algorithms, and code samples to the folder.",
            "C. Create a folder in the application project named rules. Store the guidelines and code "
            "in the folder for Amazon Q Developer to reference product code suggestions.",
            "D. Create an Amazon Q Developer customization that includes the approved data sources. "
            "Ensure that the developers use the customization to develop the application.",
        ],
        "answer": "D. Create an Amazon Q Developer customization that includes the approved data "
                  "sources. Ensure that the developers use the customization to develop the "
                  "application.",
        "explanation": "The discriminator is **'no project-level modifications'**. An Amazon Q "
                       "Developer **customization** (a Pro-tier feature) is created once by an admin "
                       "from approved private code/libraries (S3 or a code connection) and selected by "
                       "developers in the IDE, so suggestions follow internal libraries and styles "
                       "across all projects.\n\n"
                       "**A, B, C** all put content inside the project (workspace, `.amazonq/rules`, a "
                       "`rules` folder) — exactly the project-level change the company wants to avoid. "
                       "Project rules also apply only to the current workspace and hold guidance "
                       "(Markdown), not a library of code.",
        "reference": "https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/customizations-admin-customize.html",
        "note": "Answer derived; verified against the Amazon Q Developer docs (project rules apply "
                "only to the current workspace; customizations are an org-level Pro feature).",
    },
    {
        "id": 42,
        "category": D4,
        "task": "4.1",
        "type": "single",
        "question": "An ecommerce company is using Amazon Bedrock to build a customer service AI "
                    "assistant. The AI assistant needs to process over 50,000 customer inquiries every "
                    "day. The AI assistant occasionally experiences traffic spikes of up to 150,000 "
                    "inquiries every day during promotional events. Analysis shows that 40% of "
                    "inquiries follow similar patterns that share the same context.\n"
                    "A GenAI developer must design a solution that will ensure low latency and "
                    "consistent performance for the AI assistant during traffic spikes.\n"
                    "Which solution will meet these requirements MOST cost-effectively?",
        "options": [
            "A. Configure latency-optimized inference by setting the latency parameter to optimized "
            "in the performance configuration of the request to Amazon Bedrock. Use prompt caching to "
            "handle the repetitive inquiries.",
            "B. Purchase provisioned throughput and model units (MUs) that are sized to handle peak "
            "traffic loads. Use Amazon ElastiCache (Redis OSS) to cache repetitive inquiries.",
            "C. Use Amazon Bedrock Agents and custom knowledge bases to pre-process customer "
            "inquiries. Configure cross-Region inference to distribute traffic.",
            "D. Use AWS Lambda functions to pre-process requests by using a custom prompt routing "
            "mechanism. Use Amazon DynamoDB as a caching layer to handle frequently asked questions.",
        ],
        "answer": "A. Configure latency-optimized inference by setting the latency parameter to "
                  "optimized in the performance configuration of the request to Amazon Bedrock. Use "
                  "prompt caching to handle the repetitive inquiries.",
        "explanation": "Both stated facts have a native Bedrock feature: **low latency** → "
                       "latency-optimized inference (`performanceConfig.latency = optimized`); "
                       "**'40% share the same context'** → **prompt caching**, which reuses the "
                       "repeated prompt prefix to cut both latency and input-token cost. No extra "
                       "infrastructure and no capacity bought for rare spikes — the most cost-effective.\n\n"
                       "**B** provisioned throughput sized for the *peak* is paid for 24/7 even though "
                       "spikes are occasional, and adds ElastiCache to run. **C** Agents + knowledge "
                       "bases add machinery the stem doesn't need. **D** a custom routing + DynamoDB "
                       "cache is a custom build (and exact-match caching misses 'similar' questions).",
        "reference": f"{_BR}/prompt-caching.html",
        "note": "Answer derived. Cost cue: 'occasionally' spikes → don't buy peak-sized provisioned "
                "capacity. Latency-optimized inference is available only for some models.",
    },
    {
        "id": 43,
        "category": D1,
        "task": "1.5",
        "type": "single",
        "question": "A legal research company has a Retrieval Augmented Generation (RAG) application "
                    "that uses Amazon Bedrock and Amazon OpenSearch Service. The application stores "
                    "768-dimensional vector embeddings for 15 million legal documents, including "
                    "statutes, court rulings, and case summaries.\n"
                    "The company's current chunking strategy segments text into fixed-length blocks of "
                    "500 tokens. The current chunking strategy often splits contextually linked "
                    "information such as legal arguments, court opinions, or statute references across "
                    "separate chunks. Researchers report that generated outputs frequently omit key "
                    "context or cite outdated legal information.\n"
                    "Recent application logs show a 40% increase in response times. The p95 latency "
                    "metric exceeds 2 seconds. The company expects storage needs for the application to "
                    "grow from 90 GB to 360 GB within a year.\n"
                    "The company needs a solution to improve retrieval relevance and system performance "
                    "at scale.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Increase the embedding vector dimensionality from 768 to 4,096 without changing the "
            "existing chunking or pre-processing strategy.",
            "B. Replace dynamic retrieval with static, pre-written summaries that are stored in Amazon "
            "S3. Use Amazon CloudFront to serve the summaries to reduce compute demand and improve "
            "predictability.",
            "C. Update the chunking strategy to use semantic boundaries such as complete legal "
            "arguments, clauses, or sections rather than fixed token limits. Regenerate vector "
            "embeddings to align with the new chunk structure.",
            "D. Migrate from OpenSearch Service to Amazon DynamoDB. Implement keyword-based indexes to "
            "enable faster lookups for legal concepts.",
        ],
        "answer": "C. Update the chunking strategy to use semantic boundaries such as complete legal "
                  "arguments, clauses, or sections rather than fixed token limits. Regenerate vector "
                  "embeddings to align with the new chunk structure.",
        "explanation": "The root cause is stated in the stem: **fixed-length 500-token chunks split "
                       "linked legal reasoning**, so retrieval returns fragments and answers lose "
                       "context. Fix it at the source — chunk along **semantic/structural boundaries** "
                       "(arguments, clauses, sections) and re-embed. Coherent chunks also mean fewer "
                       "chunks need to be retrieved and sent to the model, helping latency.\n\n"
                       "**A** bigger vectors (768→4,096) add storage and slower search without "
                       "fixing the broken chunks. **B** static summaries remove dynamic retrieval and "
                       "worsen outdated-information issues. **D** DynamoDB + keyword indexes abandon "
                       "semantic search.",
        "reference": f"{_BR}/kb-chunking.html",
        "note": "Answer derived. High confidence — only C addresses the identified root cause "
                "(chunk boundaries) without regressing the architecture.",
    },
    {
        "id": 44,
        "category": D1,
        "task": "1.6",
        "type": "single",
        "question": "A company is developing a generative AI (GenAI)-powered customer support "
                    "application that uses Amazon Bedrock foundation models (FMs). The application must "
                    "maintain conversational context across multiple interactions with the same user. "
                    "The application must run clarification workflows to handle ambiguous user queries. "
                    "The company must store encrypted records of each user conversation to use for "
                    "personalization. The application must be able to handle thousands of concurrent "
                    "users while responding to each user quickly.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use an AWS Step Functions Express workflow to orchestrate conversation flow. Invoke "
            "AWS Lambda functions to run clarification logic. Store conversation history in Amazon "
            "RDS and use session IDs as the primary key.",
            "B. Use an AWS Step Functions Standard workflow to orchestrate clarification workflows. "
            "Include Wait for a Callback patterns to manage the workflows. Store conversation history "
            "in Amazon DynamoDB. Purchase on-demand capacity and configure server-side encryption.",
            "C. Deploy the application by using an Amazon API Gateway REST API to route user requests "
            "to an AWS Lambda function to update and retrieve conversation context. Store "
            "conversation history in Amazon S3 and configure server-side encryption. Save each "
            "interaction as a separate JSON file.",
            "D. Use AWS Lambda functions to call Amazon Bedrock inference APIs. Use Amazon SQS queues "
            "to orchestrate clarification steps. Store conversation history in an Amazon ElastiCache "
            "(Redis OSS) cluster. Configure encryption at rest.",
        ],
        "answer": "B. Use an AWS Step Functions Standard workflow to orchestrate clarification "
                  "workflows. Include Wait for a Callback patterns to manage the workflows. Store "
                  "conversation history in Amazon DynamoDB. Purchase on-demand capacity and configure "
                  "server-side encryption.",
        "explanation": "This is the exam guide's own pattern (Skill 1.6.2): **Step Functions for "
                       "clarification workflows** (a Standard workflow can *pause* with a callback "
                       "until the user answers) and **DynamoDB for conversation history** — "
                       "single-digit-millisecond reads, **on-demand capacity** for thousands of "
                       "concurrent users, **server-side encryption** for the stored records.\n\n"
                       "**A** Express workflows can't wait for an unpredictable human reply (5-minute "
                       "limit, no callback) and RDS scales less smoothly. **C** one S3 JSON file per "
                       "interaction is slow to read back as context. **D** ElastiCache is a cache — "
                       "wrong for durable personalization records — and SQS isn't a clarification "
                       "workflow.",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html",
        "note": "Answer derived. High confidence. (Source text for B is garbled: "
                "'DynamoDPurchase' = 'DynamoDB. Purchase'.)",
    },
    {
        "id": 45,
        "category": D1,
        "task": "1.3",
        "type": "single",
        "question": "A financial services company needs to pre-process unstructured data such as "
                    "customer transcripts, financial reports, and documentation. The company stores "
                    "the unstructured data in Amazon S3 to support an Amazon Bedrock application.\n"
                    "The company must validate data quality, create auditable metadata, monitor data "
                    "metrics, and customize text chunking to optimize foundation model (FM) "
                    "performance.\n"
                    "Which solution will meet these requirements with the LEAST development effort?",
        "options": [
            "A. Use Amazon SageMaker Data Wrangler to create a data flow. Configure Amazon CloudWatch "
            "metrics and alarms to monitor data quality. Use a custom AWS Lambda function to "
            "pre-process the data. Load processed data into Amazon Bedrock.",
            "B. Set up an AWS Glue crawler to catalog data sources. Create AWS Glue ETL jobs to run "
            "custom transformation scripts. Use AWS Glue Data Quality to validate and monitor data "
            "quality. Load processed data into Amazon Bedrock.",
            "C. Use Amazon Comprehend to extract entities. Create an AWS Lambda function to chunk "
            "text. Run Amazon Athena to query and validate data quality. Load processed data into "
            "Amazon Bedrock.",
            "D. Create an AWS Step Functions workflow to orchestrate data pre-processing tasks. Run "
            "custom code on Amazon EC2 instances to process the data. Use Amazon SageMaker Model "
            "Monitor to monitor data quality. Load processed data into Amazon Bedrock.",
        ],
        "answer": "B. Set up an AWS Glue crawler to catalog data sources. Create AWS Glue ETL jobs to "
                  "run custom transformation scripts. Use AWS Glue Data Quality to validate and "
                  "monitor data quality. Load processed data into Amazon Bedrock.",
        "explanation": "Match each requirement to a Glue capability: **auditable metadata** → Glue "
                       "crawler + Data Catalog; **customised text chunking** → Glue ETL jobs with "
                       "custom transformation scripts; **validate and monitor data quality** → **Glue "
                       "Data Quality** (rules and metrics). One managed service covers all four with "
                       "little glue code (exam-guide Skill 1.3.1).\n\n"
                       "**A** still needs a custom Lambda for processing. **C** Athena isn't a "
                       "data-quality tool and Comprehend doesn't chunk. **D** EC2 custom code + Model "
                       "Monitor (for ML endpoints, not raw data) is the highest effort.",
        "reference": "https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html",
        "note": "Answer derived. High confidence — B is the only option where every requirement "
                "has a native, managed home.",
    },
    {
        "id": 46,
        "category": D1,
        "task": "1.4",
        "type": "single",
        "question": "A company uses Amazon Bedrock to build a Retrieval Augmented Generation (RAG) "
                    "system. The RAG system uses an Amazon Bedrock knowledge base that is based on an "
                    "Amazon S3 bucket as the data source for emergency news video content. The system "
                    "retrieves transcripts, archived reports, and related documents from the S3 "
                    "bucket.\n"
                    "The RAG system uses state-of-the-art embedding models and a high-performing "
                    "retrieval setup. However, users report slow responses and irrelevant results, "
                    "which cause decreased user satisfaction. The company notices that vector searches "
                    "are evaluating too many documents across too many content types and over long "
                    "periods of time.\n"
                    "The company determines that the underlying models will not benefit from additional "
                    "fine tuning. The company must improve retrieval accuracy by applying smarter "
                    "constraints. The company wants a solution that requires minimal changes to the "
                    "existing architecture.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Enhance embeddings by using a domain-adapted model that is specifically trained on "
            "emergency news content for improved vector similarity.",
            "B. Migrate to Amazon OpenSearch Service. Use vector fields and metadata filters to define "
            "the scope of results retrieval.",
            "C. Enable metadata-aware filtering within the Amazon Bedrock knowledge base by indexing "
            "S3 object metadata.",
            "D. Migrate to an Amazon Q Business index to perform structured metadata filtering and "
            "document categorization during retrieval.",
        ],
        "answer": "C. Enable metadata-aware filtering within the Amazon Bedrock knowledge base by "
                  "indexing S3 object metadata.",
        "explanation": "The searches scan too many documents (content type, date range). The "
                       "'smarter constraint' is **metadata filtering**: attach metadata to the S3 "
                       "objects (content type, date, category), ingest it with the knowledge base, and "
                       "filter at query time so the vector search covers only the relevant subset — "
                       "better relevance **and** speed, with no change to the architecture (exam-guide "
                       "Skill 1.4.2).\n\n"
                       "**A** is the model-tuning route the stem rules out. **B/D** are migrations — "
                       "the opposite of 'minimal changes'.",
        "reference": f"{_BR}/kb-test-config.html",
        "note": "Answer derived. High confidence — 'minimal changes' + 'smarter constraints' = "
                "metadata filtering inside the existing knowledge base.",
    },
    {
        "id": 47,
        "category": D1,
        "task": "1.4",
        "type": "single",
        "question": "A financial services company is creating a Retrieval Augmented Generation (RAG) "
                    "application that uses Amazon Bedrock to generate summaries of market activities. "
                    "The application relies on a vector database that stores a small proprietary "
                    "dataset that has a low index count. The application must perform similarity "
                    "searches. The Amazon Bedrock model's responses must maximize accuracy and "
                    "maintain high performance.\n"
                    "The company needs to configure the vector database and integrate it with the "
                    "application.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Launch an Amazon MemoryDB cluster and configure the index by using the Flat "
            "algorithm. Configure a horizontal scaling policy based on performance metrics.",
            "B. Launch an Amazon MemoryDB cluster and configure the index by using the Hierarchical "
            "Navigable Small World (HNSW) algorithm. Configure a vertical policy based on performance "
            "metrics.",
            "C. Launch an Amazon Aurora PostgreSQL cluster and configure the index by using the "
            "Inverted File with Flat Compression (IVFFlat) algorithm. Configure the instance class "
            "to scale to a larger size when the load increases.",
            "D. Launch an Amazon DocumentDB cluster that has an Inverted File with Flat Compression "
            "(IVFFlat) index and a high probe value. Configure connections to the cluster as a "
            "replica set. Distribute reads to replica instances.",
        ],
        "answer": "A. Launch an Amazon MemoryDB cluster and configure the index by using the Flat "
                  "algorithm. Configure a horizontal scaling policy based on performance metrics.",
        "explanation": "**Small dataset + maximise accuracy + high performance** → an in-memory store "
                       "(MemoryDB) with the **Flat** index. Flat is a brute-force scan that returns "
                       "**exact** nearest neighbours; its cost grows with index size, which is "
                       "irrelevant for a small corpus, and in-memory search keeps latency low. "
                       "Horizontal scaling (more shards/replicas) handles read load.\n\n"
                       "**B** HNSW is *approximate* (trades recall for speed) and is meant for large "
                       "indexes. **C/D** IVFFlat is also approximate, and needs enough data to build "
                       "good clusters; a high probe value only partly recovers accuracy and slows "
                       "queries.",
        "reference": "https://docs.aws.amazon.com/memorydb/latest/devguide/vector-search-overview.html",
        "note": "Answer derived; the Flat/HNSW trade-off is quoted from the MemoryDB docs (Flat = "
                "exact, slow for large indexes; HNSW = approximate, much faster). Rule of thumb for "
                "the exam: small data + accuracy → Flat; very large data + speed → HNSW; "
                "Aurora pgvector for modest sizes (< ~1M vectors).",
    },
    {
        "id": 48,
        "category": D1,
        "task": "1.3",
        "type": "single",
        "question": "A GenAI developer is building a Retrieval Augmented Generation (RAG)-based "
                    "customer support application that uses Amazon Bedrock foundation models (FMs). "
                    "The application needs to process 50 GB of historical customer conversations that "
                    "are stored in an Amazon S3 bucket as JSON files. The application must use the "
                    "processed data as its retrieval corpus. The application's data processing "
                    "workflow must extract relevant data from customer support documents, remove "
                    "customer personally identifiable information (PII), and generate embeddings for "
                    "vector storage. The processing workflow must be cost-effective and must finish "
                    "within 4 hours.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Use AWS Lambda and Amazon Comprehend to process files in parallel, remove PII, and "
            "call Amazon Bedrock APIs to generate vectors. Configure Lambda concurrency limits and "
            "memory settings to optimize throughput.",
            "B. Create an AWS Glue ETL job to run PII detection scripts on the data. Use Amazon "
            "SageMaker Processing to run the HuggingFaceProcessor to generate embeddings by using a "
            "pre-trained model. Store the embeddings in Amazon OpenSearch Service.",
            "C. Deploy an Amazon EMR cluster that runs Apache Spark with user-defined functions (UDFs) "
            "that call Amazon Comprehend to detect PII. Use Amazon Bedrock APIs to generate vectors. "
            "Store outputs in Amazon Aurora PostgreSQL with the pgvector extension.",
            "D. Implement a data processing pipeline that uses AWS Step Functions to orchestrate a "
            "workload that uses Amazon Comprehend to detect PII and Amazon Bedrock to generate "
            "embeddings. Directly integrate the workflow with Amazon OpenSearch Serverless to store "
            "vectors and provide similarity search capabilities.",
        ],
        "answer": "D. Implement a data processing pipeline that uses AWS Step Functions to "
                  "orchestrate a workload that uses Amazon Comprehend to detect PII and Amazon "
                  "Bedrock to generate embeddings. Directly integrate the workflow with Amazon "
                  "OpenSearch Serverless to store vectors and provide similarity search "
                  "capabilities.",
        "explanation": "A fully **serverless, managed** pipeline: Step Functions (with a Distributed "
                       "Map to fan out over the S3 objects in parallel — comfortably inside 4 hours) "
                       "calls **Comprehend** for PII and **Bedrock** for embeddings, and writes into "
                       "**OpenSearch Serverless** for storage and similarity search. Nothing to "
                       "provision or tune, and you pay per use.\n\n"
                       "**A** stops at generating vectors (no vector store) and you hand-tune Lambda "
                       "concurrency/timeouts. **B** mixes Glue, SageMaker Processing and a managed "
                       "OpenSearch domain — more components and cost. **C** a persistent EMR cluster is "
                       "the highest overhead.",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/state-map-distributed.html",
        "note": "Answer derived. High confidence — D is the only option that is serverless end to "
                "end and includes the vector store.",
    },
    {
        "id": 49,
        "category": D1,
        "task": "1.2",
        "type": "single",
        "question": "A financial services company is developing a generative AI (GenAI) application "
                    "that serves both premium customers and standard customers. The application uses "
                    "AWS Lambda functions behind an Amazon API Gateway REST API to process requests. "
                    "The company needs to dynamically switch between AI models based on which customer "
                    "tier each user belongs to. The company also wants to perform A/B testing for new "
                    "features without redeploying code. The company needs to validate model parameters "
                    "like temperature and maximum token limits before applying changes.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Create an AWS Systems Manager Parameter Store parameters for each configuration. Use "
            "Lambda functions to poll for parameter updates. Use Amazon EventBridge events to trigger "
            "redeployments when configurations change.",
            "B. Store model configurations in Amazon DynamoDB tables. Optimize access patterns to "
            "retrieve configurations according to customer tier. Configure Lambda functions to query "
            "DynamoDB at the beginning of each request to determine which model to use.",
            "C. Use AWS AppConfig to manage model configurations. Use feature flags to perform A/B "
            "testing. Define JSON schema validation rules for model parameters. Configure Lambda "
            "functions to retrieve configurations by using the AWS AppConfig Agent.",
            "D. Create an Amazon ElastiCache (Redis OSS) cluster to store model configurations. Set "
            "short TTL values. Run custom validation logic in Lambda functions. Use Amazon CloudWatch "
            "metrics to monitor configuration usage.",
        ],
        "answer": "C. Use AWS AppConfig to manage model configurations. Use feature flags to perform "
                  "A/B testing. Define JSON schema validation rules for model parameters. Configure "
                  "Lambda functions to retrieve configurations by using the AWS AppConfig Agent.",
        "explanation": "Three cues, one service: **'without redeploying code'** + **A/B testing** → "
                       "AppConfig **feature flags** (with gradual rollout); **'validate parameters "
                       "like temperature/max tokens before applying'** → AppConfig **JSON Schema "
                       "validators**; low-overhead retrieval from Lambda → the **AppConfig Agent** "
                       "(cached, polled).\n\n"
                       "**A** forces redeployments and has no validation. **B** and **D** require "
                       "custom flag, rollout and validation logic and per-request lookups.",
        "reference": f"https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html",
        "note": "Answer derived. High confidence — cf. Q4: 'switch without redeploying' → AppConfig.",
    },
    {
        "id": 50,
        "category": D4,
        "task": "4.2",
        "type": "single",
        "question": "A company is using Amazon Bedrock and Anthropic Claude 3 Haiku to develop an AI "
                    "assistant. The AI assistant normally processes 10,000 requests each hour but "
                    "experiences surges of up to 30,000 requests each hour during peak usage periods. "
                    "The AI assistant must respond within 2 seconds while operating across multiple AWS "
                    "Regions.\n"
                    "The company observes that during peak usage periods, the AI assistant experiences "
                    "throughput bottlenecks that cause increased latency and occasional request "
                    "timeouts. The company must resolve the performance issues.\n"
                    "Which solution will meet this requirement?",
        "options": [
            "A. Purchase provisioned throughput and sufficient model units (MUs) in a single Region. "
            "Configure the application to retry failed requests with exponential backoff.",
            "B. Implement token batching to reduce API overhead. Use cross-Region inference profiles "
            "to automatically distribute traffic across available Regions.",
            "C. Set up auto scaling AWS Lambda functions in each Region. Implement client-side "
            "round-robin request distribution. Purchase one model unit (MU) of provisioned "
            "throughput as a backup.",
            "D. Implement batch inference for all requests by using Amazon S3 buckets across multiple "
            "Regions. Use Amazon SQS to set up an asynchronous retrieval process.",
        ],
        "answer": "B. Implement token batching to reduce API overhead. Use cross-Region inference "
                  "profiles to automatically distribute traffic across available Regions.",
        "explanation": "The bottleneck is **model throughput at peak**, and the requirement already "
                       "says 'operating across multiple Regions'. **Cross-Region inference profiles** "
                       "automatically route requests to the Region with capacity, raising effective "
                       "throughput and absorbing 3x surges with no capacity planning; batching "
                       "reduces per-call overhead.\n\n"
                       "**A** single-Region provisioned throughput sized for the surge is costly and "
                       "retries *add* latency. **C** client-side round-robin is custom and a single MU "
                       "is negligible capacity. **D** batch inference is asynchronous — it can't "
                       "satisfy a 2-second response.",
        "reference": f"{_BR}/cross-region-inference.html",
        "note": "Answer derived. Moderate-to-high confidence. 'Token batching' is loosely worded, "
                "but B is the only option that raises throughput without breaking the 2-second "
                "synchronous requirement. Compare Q13 (CRI + SCP) for the governance side.",
    },
]
