"""
AIP-C01 questions 105, 115-119, 122-136 (from screenshots; the source's suggested answers
were hidden, so every answer is derived from the exam guide + AWS docs and carries no vote
data or answer-key check).

Same schema as questions.py. Q105 came from a different site's numbering (Topic 3).
Hyphenation artefacts from the screenshots (e.g. 'Bed-rock') were cleaned.
"""

_BR = "https://docs.aws.amazon.com/bedrock/latest/userguide"
_AC = "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide"

D1 = "1 · FM Integration, Data & Compliance"
D2 = "2 · Implementation & Integration"
D3 = "3 · Safety, Security & Governance"
D4 = "4 · Operational Efficiency & Optimization"
D5 = "5 · Testing, Validation & Troubleshooting"

EXTRA4: list[dict] = [
    {
        "id": 105, "category": D1, "task": "1.6", "type": "single",
        "question": "A retail company runs an application that makes product recommendations to customers on the company's website. The application uses Amazon Bedrock to generate recommendations by dynamically constructing prompts and sending them to foundation models (FMs). A GenAI developer has deployed an update to the application that instructs the FM to include a specific promotional message when the FM generates a response to prompts. When the developer tests the application, the promotional message does not always appear in the responses. When the promotional message does appear in the responses, it does not always flow with the rest of the text. The GenAI developer must ensure that the promotional message always appears in the FM responses.\n"
                    "Which solution will meet this requirement?",
        "options": [
            "A. Use an Amazon Bedrock Guardrails filter on the prompt. Set the input filter strength to HIGH.",
            "B. Generate multiple response variants that include the promotional message in different ways. Use a reranker model to select the most coherent version based on relevance to the original prompt.",
            "C. Run the prompt through Amazon Bedrock. Process the response through Amazon Bedrock AgentCore to add the promotional message. Rerank the results by using the original prompt and the desired message as context.",
            "D. Reinforce the requirement to include the new promotional message within product recommendations by using an output indicator in prompts to the FM.",
        ],
        "answer": "D. Reinforce the requirement to include the new promotional message within product recommendations by using an output indicator in prompts to the FM.",
        "explanation": "The failure is that the **instruction in the prompt is too weak** — the model sometimes ignores it and, when it complies, the text reads awkwardly. The fix is prompt engineering: state the requirement explicitly with an **output indicator** (a clear output-format/placement instruction such as 'end every recommendation with: …, phrased naturally within the paragraph'), so the message is part of the specified output (exam-guide Skill 1.6.5: structured input components, output format specifications).\n\n"
                       "**A** Guardrails input filters detect harmful input; they don't make a response contain text. **B** generate-and-rerank multiplies cost and still doesn't *guarantee* the message. **C** AgentCore is an agent runtime, not a text post-processor, and reranking doesn't enforce inclusion.",
        "reference": f"{_BR}/prompt-engineering-guidelines.html",
        "note": "Answer derived. High confidence — the only option that changes how the FM is instructed.",
    },
    {
        "id": 115, "category": D5, "task": "5.1", "type": "single",
        "question": "A company is developing a customer support chat assistant that uses an Amazon Bedrock foundation model (FM). The company wants to update to a newer FM version but needs to implement a validation system to detect semantic drift in responses. The company wants to ensure that performance and functionality for end users remains consistent.\n"
                    "The company needs a solution to compare responses between current and new FM versions for 500 test cases. The solution must detect changes in response meaning, generate quantitative similarity scores, complete validations, and log detailed results for historical comparison.\n"
                    "Which solution will meet these requirements with the LEAST operational complexity?",
        "options": [
            "A. Configure Amazon CloudWatch Synthetics canaries that use custom JavaScript code to send identical prompts to both new and existing FM versions. Store responses in Amazon S3. Perform manual reviews to identify semantic differences between FM versions.",
            "B. Configure an AWS Step Functions workflow that sends test prompts to both new and existing FM versions. Use Amazon Bedrock embedding models to calculate cosine similarity scores. Store the results in Amazon DynamoDB with a composite key schema.",
            "C. Use Amazon Bedrock model evaluation jobs to compare the new FM version against the current version using the 500 test cases. Configure the evaluation to calculate semantic similarity metrics. Store results in Amazon S3 for historical comparison.",
            "D. Build a custom solution by using Amazon SageMaker AI to train a classifier model on historical responses to detect anomalies when the solution compares responses from the new FM version to previous patterns.",
        ],
        "answer": 'C. Use Amazon Bedrock model evaluation jobs to compare the new FM version against the '
                  'current version using the 500 test cases. Configure the evaluation to calculate semantic '
                  'similarity metrics. Store results in Amazon S3 for historical comparison.',
        "explanation": "'**LEAST operational complexity**' points to the managed feature: **Amazon Bedrock model "
                       "evaluation jobs**. Run the 500 test cases against the new version with the current version's"
                       ' answers as reference responses, compute **semantic similarity** scores (for example '
                       "BERTScore, or LLM-as-a-judge correctness against the reference), and keep each job's results"
                       ' in **S3** for historical comparison. No workflow, embedding code or database to build.\\n'
                       '\\n'
                       '**B** works, but it is the custom equivalent (a Step Functions workflow, embedding calls, '
                       'cosine maths and a DynamoDB schema to build and maintain). **A** relies on manual review. '
                       '**D** training a classifier is the heaviest option.',
        "reference": f"{_BR}/titan-embedding-models.html",
        "note": "Cross-check: changed from B to C. 'LEAST operational complexity' favours the managed "
                'evaluation feature, and B is the hand-built version of the same check. Moderate confidence '
                '(no answer key covers this question).'
    },
    {
        "id": 116, "category": D4, "task": "4.1", "type": "single",
        "question": "A media company is building an AI-powered content moderation system by using Amazon Bedrock. The system first classifies text by using a small, low-latency model. Then the system escalates requests that have a confidence score below 0.65 to a larger, more expensive model.\n"
                    "The system must respond in near real time for high-confidence results. The system must process low-confidence requests asynchronously. The system must scale to meet sudden spikes in demand. The company wants to optimize costs for the system by invoking the larger model only when required. The company wants to use decoupled components to achieve high resiliency for the system.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon API Gateway to invoke the small model synchronously. If the small model's confidence score is below 0.65, synchronously call the larger model. Use provisioned concurrency to handle traffic spikes.",
            "B. Use an AWS Step Functions workflow that has parallel branches to run both the small model and the large model for every request. Choose the large model result when confidence score values differ.",
            "C. Send requests to an Amazon SQS queue. Use AWS Fargate to process messages. Invoke the small model first. If the confidence score is below 0.65, place the request in a second SQS queue to process asynchronously by using the large model.",
            "D. Deploy both models on Amazon EC2 instances and enable auto scaling. Use a custom application heuristic to route requests to the appropriate instance based on phrase length and keyword rules.",
        ],
        "answer": "C. Send requests to an Amazon SQS queue. Use AWS Fargate to process messages. Invoke the small model first. If the confidence score is below 0.65, place the request in a second SQS queue to process asynchronously by using the large model.",
        "explanation": "This is a **model cascade** (exam-guide Skills 2.2.3, 4.1.2): the cheap model handles everything first, and only low-confidence items are **escalated through a second queue** for **asynchronous** processing by the large model. **SQS** decouples the stages (resilience, absorbs spikes) and **Fargate** workers scale with queue depth, with no servers to manage.\n\n"
                       "**A** calls the large model *synchronously* (the stem wants async) and couples the stages. **B** runs the expensive model for every request — defeating cost optimisation. **D** keyword heuristics instead of confidence scores and self-managed EC2 capacity.",
        "reference": "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 117, "category": D3, "task": "3.1", "type": "single",
        "question": "A social messaging company is building an AI chat assistant by using Amazon Bedrock. The company must ensure that every inference complies with an approved safety policy. The company wants to block harmful prompts before model invocations, filter streamed model outputs in real time, and route flagged cases for human review.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure an AWS Step Functions workflow. Configure a step to use an AWS Lambda function to pre-check inputs by using the ApplyGuardrail API. Use an InvokeModelWithResponseStream API step that has the guardrail attached. Configure a second Lambda function step to post-check outputs by using the ApplyGuardrail API. Route flagged items to an Amazon SQS queue. Enforce guardrail use by using a bedrock:GuardrailIdentifier IAM condition.",
            "B. Configure an AWS Step Functions workflow. Configure a step to call the ApplyGuardrail API before inference. Then call the InvokeModel API without streaming and use the guardrail. Store the results in Amazon S3. Use the client UI to hide problematic tokens.",
            "C. Configure an AWS Step Functions workflow. Configure a step to use the InvokeModelWithResponseStream API that has the guardrail attached for in-stream filtering. Run an AWS Lambda post-check step by using the ApplyGuardrail API to check flagged cases. Do not perform pre-inference.",
            "D. Configure an AWS Step Functions workflow that includes steps to perform pre-checks and post-checks by using the ApplyGuardrail API and the InvokeModelWithResponseStream API. Attach the guardrail to the check steps. Use process controls such as code reviews instead of IAM enforcement to ensure that guardrails are always applied.",
        ],
        "answer": "A. Configure an AWS Step Functions workflow. Configure a step to use an AWS Lambda function to pre-check inputs by using the ApplyGuardrail API. Use an InvokeModelWithResponseStream API step that has the guardrail attached. Configure a second Lambda function step to post-check outputs by using the ApplyGuardrail API. Route flagged items to an Amazon SQS queue. Enforce guardrail use by using a bedrock:GuardrailIdentifier IAM condition.",
        "explanation": "Each stated need appears exactly once: **block harmful prompts before invocation** → pre-check with `ApplyGuardrail`; **filter streamed outputs in real time** → `InvokeModelWithResponseStream` with the guardrail attached (stream filtering); **post-check** the final output; **route flagged cases for human review** → SQS queue; and **'every inference complies'** → *enforce* guardrail use with the `bedrock:GuardrailIdentifier` IAM condition (defence in depth, Skill 3.1.4).\n\n"
                       "**B** disables streaming and hides tokens only in the client (unsafe). **C** has no pre-inference check. **D** relies on code reviews instead of IAM enforcement, so compliance isn't guaranteed.",
        "reference": f"{_BR}/guardrails-use-independent-api.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 118, "category": D3, "task": "3.2", "type": "single",
        "question": "A financial services company uses Amazon Bedrock to analyze customer data that is stored in an Amazon S3 bucket. The data includes personally identifiable information (PII). The company must mask PII from foundation model (FM) responses.\n"
                    "Which solution will meet this requirement with the LEAST operational effort?",
        "options": [
            "A. Create a guardrail in Amazon Bedrock to filter PII content. Define the PII type and set the guardrail action to MASK. Configure Amazon Bedrock to apply the filter to each FM response.",
            "B. Use Amazon Comprehend to detect PII entities in the S3 data before invoking Amazon Bedrock. Configure an AWS Lambda function to call the Amazon Comprehend DetectPiiEntities API to mask detected PII. Store the processed data back to the original S3 bucket.",
            "C. Use Amazon Macie to scan the S3 bucket for PII data. Configure an AWS Lambda function to store PII in a second S3 bucket. Use an Amazon EventBridge rule to invoke the Lambda function.",
            "D. Configure an AWS Lambda function to search for PII data. Implement a step in the Lambda function code to store the PII in a second S3 bucket and non-PII data into a third S3 bucket.",
        ],
        "answer": "A. Create a guardrail in Amazon Bedrock to filter PII content. Define the PII type and set the guardrail action to MASK. Configure Amazon Bedrock to apply the filter to each FM response.",
        "explanation": "The requirement is about **FM responses**, so the control belongs at inference: a **Bedrock guardrail** with a **sensitive-information (PII) filter set to MASK** redacts PII from each response with no custom code or data pipeline.\n\n"
                       "**B/C/D** operate on the data at rest in S3 (modifying, scanning or splitting it) — more code and effort, and they don't stop the model from emitting PII in its output.",
        "reference": f"{_BR}/guardrails-sensitive-filters.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 119, "category": D5, "task": "5.1", "type": "single",
        "question": "A healthcare company is implementing a clinical knowledge base application on Amazon Bedrock that provides medical information to doctors. During testing, a quality team discovers that the generative AI (GenAI) model occasionally fabricates medical treatment recommendations that do not originate from the approved clinical guidelines.\n"
                    "The quality team needs to implement a solution to detect the hallucinations before releasing the application. The solution must analyze model responses against verified medical information. The solution must identify semantic inconsistencies when users ask similar questions in different ways.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Deploy a real-time monitoring system that uses Amazon CloudWatch Logs Insights to analyze response patterns and to flag factual inaccuracies based on predefined keywords. Implement AWS Lambda functions to compare responses with known answers from an Amazon DynamoDB table.",
            "B. Create a reference dataset with validated question-answer pairs from clinical guidelines. Implement output diffing by using Amazon Bedrock Guardrails for response consistency analysis. Use Amazon Bedrock evaluation to detect factual inaccuracies.",
            "C. Configure Amazon Bedrock Guardrails with custom rules to detect and block potentially hallucinated content by identifying specific patterns in the GenAI responses. Use Amazon SageMaker Feature Store to maintain a repository of verified clinical guidelines.",
            "D. Create an Amazon Bedrock automatic model evaluation job with a custom prompt dataset. Set up anomaly detection alarms to identify factual inaccuracies. Implement Amazon SNS notifications when inaccuracies are detected.",
        ],
        "answer": "B. Create a reference dataset with validated question-answer pairs from clinical guidelines. Implement output diffing by using Amazon Bedrock Guardrails for response consistency analysis. Use Amazon Bedrock evaluation to detect factual inaccuracies.",
        "explanation": "This matches exam-guide Skill 4.3.6 (GenAI-specific failure modes): a **golden dataset** of validated Q&A pairs from the clinical guidelines to compare against, **output diffing** to test **response consistency** when the same question is paraphrased, and Bedrock **evaluation** to score factual accuracy — all **before release**.\n\n"
                       "**A** keyword matching can't catch semantic hallucinations and is a post-release monitor. **C** guardrails can't detect hallucination by 'specific patterns', and a Feature Store is not a guideline repository. **D** anomaly alarms and SNS are runtime monitoring, not pre-release comparison against verified answers.",
        "reference": f"{_BR}/model-evaluation-metrics.html",
        "note": "Answer derived. Moderate-high confidence — B is the only option combining a verified reference set with a consistency check across paraphrases.",
    },
    {
        "id": 122, "category": D5, "task": "5.1", "type": "single",
        "question": "A financial company is building an AI-powered recommendation system. The system uses real-time market data and verified internal documents. The system must include evaluation capabilities that collect explicit user ratings and detect problematic responses in real time. The system must include evaluation capabilities that track model performance over time and support A/B testing of different prompt or model variants.\n"
                    "The system must orchestrate multi-step workflows. The workflows must retrieve trusted knowledge, validate inputs, and generate recommendations. The system must securely store all user feedback, flagged events, and audit logs in a compliance-ready immutable repository. The repository must be write-once, tamper-evident storage that is suitable for regulated audit retention.\n"
                    "Which architecture will meet these requirements?",
        "options": [
            "A. Deploy a fine-tuned FM on Amazon SageMaker JumpStart. Use Amazon Bedrock AgentCore to orchestrate input validation and retrieval workflows. Store user feedback and flagged queries in Amazon DynamoDB. Run scheduled Amazon Athena queries on AWS CloudTrail logs for anomaly detection. Store generated outputs in encrypted Amazon S3 buckets. Enable S3 Object Lock.",
            "B. Configure Amazon API Gateway to invoke an Amazon Bedrock FM that retrieves from Amazon Kendra. Store all responses in encrypted Amazon S3 buckets. Enable S3 Object Lock. Use Amazon Macie to scan stored logs for problematic content.",
            "C. Use Amazon Bedrock AgentCore to orchestrate retrieval from curated Amazon Kendra indexes. Configure an AWS Lambda function to sanitize input. Configure a function to check post-generation fact consistency. Configure a function to split traffic for A/B testing. Store user feedback in Amazon DynamoDB. Write audit logs through AWS CloudTrail. Store the logs in Amazon S3. Enable S3 Object Lock. Use Amazon SageMaker Model Monitor to track data drift and output anomalies continuously.",
            "D. Build an Amazon Lex chat-based AI assistant with aliases that route a percentage of queries to two Amazon SageMaker AI endpoints for recommendations. Log interactions to Amazon CloudWatch Logs. Conduct quarterly manual audits for hallucination and prompt-injection detection. Store feedback in Amazon RDS with encryption.",
        ],
        "answer": "C. Use Amazon Bedrock AgentCore to orchestrate retrieval from curated Amazon Kendra indexes. Configure an AWS Lambda function to sanitize input. Configure a function to check post-generation fact consistency. Configure a function to split traffic for A/B testing. Store user feedback in Amazon DynamoDB. Write audit logs through AWS CloudTrail. Store the logs in Amazon S3. Enable S3 Object Lock. Use Amazon SageMaker Model Monitor to track data drift and output anomalies continuously.",
        "explanation": "Only C covers every stated capability: **multi-step orchestration** (AgentCore) that retrieves **trusted knowledge** (curated Kendra indexes) and **validates inputs**; **real-time detection of problematic responses** (post-generation fact-consistency check); **A/B testing** (traffic-split function); **user ratings** (DynamoDB); **audit logs** (CloudTrail) kept in **S3 with Object Lock** — the write-once, tamper-evident store required; and continuous **drift/anomaly tracking** over time.\n\n"
                       "**A** has no A/B testing or real-time problematic-response check (Athena queries are batch). **B** lacks orchestration, evaluation and A/B testing. **D** relies on quarterly *manual* audits and stores feedback in RDS (not immutable).",
        "reference": f"{_AC}/what-is-bedrock-agentcore.html",
        "note": "Answer derived. High confidence by elimination — C is the only complete architecture (and the only one pairing A/B testing with S3 Object Lock).",
    },
    {
        "id": 123, "category": D4, "task": "4.2", "type": "single",
        "question": "A retail company has a product recommendation system that uses a foundation model (FM) in Amazon Bedrock. The system processes and searches millions of product embeddings that are updated hourly. The company regularly adds new products.\n"
                    "During peak shopping events, the current solution experiences high latency and occasional failures when the system performs similarity searches across the product catalog. The company must resolve the performance issues.\n"
                    "Which solution will meet this requirement?",
        "options": [
            "A. Implement Amazon OpenSearch Service with a multi-node architecture. Configure vector-specific index settings and memory circuit breakers. Establish dedicated vector operation queues to handle surge capacity during peak usage events.",
            "B. Deploy an Amazon DynamoDB table that uses sparse vector compression. Implement parallel query executors to handle search operations. Configure DynamoDB Streams and AWS Lambda functions to maintain the vector index in real time.",
            "C. Set up an Amazon Bedrock knowledge base that uses custom vector partitioning. Implement hierarchical metadata structures. Integrate the knowledge base with Amazon EventBridge to provide synchronized catalog updates and to generate vectors.",
            "D. Deploy an Amazon Neptune cluster with specialized vector endpoints. Configure custom similarity computation functions. Use the Neptune bulk loader API to manage vector updates across the product catalog.",
        ],
        "answer": "A. Implement Amazon OpenSearch Service with a multi-node architecture. Configure vector-specific index settings and memory circuit breakers. Establish dedicated vector operation queues to handle surge capacity during peak usage events.",
        "explanation": "OpenSearch Service is the AWS vector store built for **large-scale similarity search with frequent updates**: a **multi-node** (sharded) cluster spreads the load, **vector index settings** (e.g. HNSW parameters) tune query performance, **memory circuit breakers** protect nodes from out-of-memory failures, and queues absorb surges — covering both the latency and the failures (exam-guide Skills 1.4.3, 4.2.6, 4.3.5).\n\n"
                       "**B** DynamoDB has no native vector search ('sparse vector compression' isn't a feature). **C** 'custom vector partitioning' isn't a Knowledge Bases capability. **D** Neptune is a graph database, not tuned for large-scale similarity search.",
        "reference": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html",
        "note": "Answer derived. High confidence (B/C/D describe features that don't exist).",
    },
    {
        "id": 124, "category": D3, "task": "3.2", "type": "single",
        "question": "A healthcare company is developing an application that processes sensitive patient data and generates treatment summaries by using a foundation model (FM). The application must maintain an audit trail of all prompts and completions. The application must securely handle protected health information (PHI) data throughout the processing lifecycle. The company must track all prompt-completion pairs with original patient data, but the company must redact any PHI from stored records. The company must enforce healthcare-specific data retention policies.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Store prompt-completion pairs in Amazon S3 and enable default server-side encryption. Deploy an AWS Lambda function that scans records by using Amazon Comprehend Medical. Configure the Lambda function to delete PHI data after a required retention period.",
            "B. Use Amazon Bedrock Prompt Management and Amazon Bedrock Flows to detect PHI. Configure Amazon Bedrock Guardrails to use sensitive information filters to mask PHI automatically. Store logs in Amazon S3 and configure appropriate retention settings.",
            "C. Store prompt-completion pairs in Amazon S3. Configure S3 Object Lock in compliance mode. Apply tag-based S3 Lifecycle policies to PHI data. Configure an AWS Lambda function to redact patient information after the application processes the data.",
            "D. Store patient data in an Amazon Bedrock knowledge base. Use Amazon Comprehend Medical to identify PHI. Configure an AWS Lambda function to manage data retention according to healthcare policies.",
        ],
        "answer": 'B. Use Amazon Bedrock Prompt Management and Amazon Bedrock Flows to detect PHI. Configure '
                  'Amazon Bedrock Guardrails to use sensitive information filters to mask PHI automatically. '
                  'Store logs in Amazon S3 and configure appropriate retention settings.',
        "explanation": '**Bedrock Guardrails sensitive-information filters** mask PHI automatically in prompts and '
                       'completions, so the stored prompt-completion records are already redacted. The logs (the '
                       'audit trail of every pair) go to **S3 with retention / lifecycle settings** for the '
                       'healthcare retention policy. The pairs can still be tracked to a patient through non-PHI '
                       'identifiers.\\n'
                       '\\n'
                       '**C** contradicts itself: **S3 Object Lock in compliance mode makes objects immutable**, so '
                       'PHI in a locked record can never be redacted or deleted afterwards. **A** *deletes* PHI '
                       'after the retention period instead of redacting it, so PHI sits in storage until then. **D**'
                       ' a knowledge base is not an audit store.',
        "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html",
        "note": "Cross-check: changed from C to B. C can't work, because Object Lock compliance mode forbids "
                "modifying the stored records, so PHI can't be redacted later. B's 'Prompt Management and "
                "Flows to detect PHI' wording is loose, but Guardrails masking plus S3 retention meets every "
                'requirement. Moderate confidence (no answer key covers this question).'
    },
    {
        "id": 125, "category": D1, "task": "1.3", "type": "single",
        "question": "A financial services company runs an AI application that uses Amazon Bedrock foundation models (FMs) to generate personalized investment recommendations based on customer documents. The AI application processes customer portfolios, financial statements, and regulatory documentation to create personalized recommendations.\n"
                    "The company is experiencing inconsistent model performance because of poor data quality. Some documents contain personally identifiable information (PII) that the company must redact. Other documents contain formatting inconsistencies that confuse the FMs. The company needs a solution that ensures consistent, high-quality inputs to optimize FM. The solution must comply with financial regulations and PII handling policies.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Use Amazon Macie to automatically detect and redact PII. Use AWS Lambda functions and Amazon Textract to enforce standard document formatting. Create dynamic prompts that adapt to individual document schemas to improve model consistency.",
            "B. Use Amazon Comprehend to detect PII by using custom entity recognition. Use AWS Step Functions to orchestrate document preprocessing workflows. Use prompt templates with conditional logic to handle schema variations effectively.",
            "C. Use Amazon Bedrock Guardrails to filter out PII during inference. Use pre-processing AWS Lambda functions to standardized document formatting. Use few-shot prompting techniques and standardized examples to improve model performance across document types.",
            "D. Use Amazon Textract to analyze document structures and extract text. Use Amazon Comprehend to detect PII and analyze sentiment. Design prompt engineering strategies that use structured metadata to improve FM reasoning and reduce hallucinations.",
        ],
        "answer": "C. Use Amazon Bedrock Guardrails to filter out PII during inference. Use pre-processing AWS Lambda functions to standardized document formatting. Use few-shot prompting techniques and standardized examples to improve model performance across document types.",
        "explanation": "Two defects, each with a light, native fix: **PII** → **Bedrock Guardrails** sensitive-information filters (managed redaction, no custom entity models); **inconsistent formatting** → a small **Lambda pre-processing** step that standardises documents; and **few-shot prompting with standardised examples** gives the FM consistent expectations across document types (exam-guide Skills 1.3.4, 1.6.5).\n\n"
                       "**A** Macie *discovers* PII in S3 but doesn't redact it. **B** custom Comprehend entity recognition + Step Functions orchestration is much more to build and maintain. **D** Textract + Comprehend (with sentiment analysis, which isn't needed) adds services without redacting PII.",
        "reference": f"{_BR}/guardrails.html",
        "note": "Answer derived. Moderate-high confidence.",
    },
    {
        "id": 126, "category": D2, "task": "2.3", "type": "single",
        "question": "A global company uses an organization in AWS Organizations to manage 25 AWS accounts. The company's products have 50,000 daily user interactions. The company is using Amazon Bedrock AgentCore to build an AI assistant.\n"
                    "The AI assistant must access customer data that is stored in multiple AWS accounts across several business units. The AI assistant needs to perform actions on behalf of specific users by querying Amazon DynamoDB tables that contain customer information in each business unit's AWS account. Each business unit maintains its own AWS account that hosts its own DynamoDB tables.\n"
                    "The company must enforce strict data access security boundaries and must collect full audit trails that show which user's credentials are used to perform each action. The solution must allow the AgentCore application to access resources across multiple accounts while preserving user identity context. The solution must support the company's plan to expand to more than 40 AWS accounts in the next year.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Configure the AI assistant to use an outbound credential provider that runs AssumeRole operations to dynamically obtain temporary credentials so the AI assistant can access resources across accounts. Create an IAM role in each business unit account that has a trust relationship to the AI assistant's execution role and permissions to access the DynamoDB tables. Ensure that AssumeRole calls include session tags to identify the end user.",
            "B. Create a separate AI assistant in each business unit account. Deploy an Amazon API Gateway REST API that runs request routing logic. Create AWS Lambda authorizers to direct user queries to the appropriate AI assistant based on the customer's business unit identifier from the request context.",
            "C. Use AWS Resource Access Manager (AWS RAM) to share the DynamoDB tables from each business unit account to a central account where the AI assistant runs. Configure AWS RAM permissions to allow cross-account access to the DynamoDB tables. Grant the AgentCore execution role permissions to access the shared resources directly.",
            "D. Configure SCPs for the organization to explicitly allow the AI assistant's execution role principal to perform dynamodb:GetItem and dynamodb:Query actions across all member accounts. Configure the AI assistant to reference cross-account DynamoDB table ARNs directly in their resource definitions.",
        ],
        "answer": "A. Configure the AI assistant to use an outbound credential provider that runs AssumeRole operations to dynamically obtain temporary credentials so the AI assistant can access resources across accounts. Create an IAM role in each business unit account that has a trust relationship to the AI assistant's execution role and permissions to access the DynamoDB tables. Ensure that AssumeRole calls include session tags to identify the end user.",
        "explanation": "The standard cross-account pattern: **AgentCore Identity's outbound credential provider** performs **AssumeRole** into a role in each business-unit account (trust to the assistant's execution role, least-privilege DynamoDB permissions). **Session tags** carry the **end-user identity** into the temporary credentials, so CloudTrail records *which user* each action ran as, and adding the 26th–40th account just means creating one more role — low overhead.\n\n"
                       "**B** a separate assistant per account is 40+ deployments to run. **C** RAM can't share DynamoDB tables. **D** SCPs only *limit* permissions; they never grant access, and DynamoDB table ARNs alone don't create cross-account access.",
        "reference": f"{_AC}/identity.html",
        "note": "Answer derived. High confidence — C and D rely on features that don't work that way (RAM doesn't share DynamoDB; SCPs don't grant).",
    },
    {
        "id": 127, "category": D3, "task": "3.1", "type": "single",
        "question": "A hospital is building an AI application to help medical clinicians to make treatment decisions. The application uses Amazon Bedrock to analyze patient case histories and suggest diagnoses. The application must maintain sub-500 ms response times to integrate with the hospital's existing real-time clinical workflow. To comply with privacy regulations, the application must log all personally identifiable information (PII) handling decisions for audits. The application must detect and remove PII from responses with at least 99% accuracy.\n"
                    "After initial deployment, clinicians report that diagnostic summaries from the application occasionally include patient names and medical record numbers that were not present in the original case history inputs. An investigation reveals that Amazon Comprehend Medical successfully detects and removes PII from inputs with 95% accuracy, and the application replaces all detected entities with tokens before it sends inputs to Amazon Bedrock. However, the application continues to generate patient-identifying information in approximately 3-5% of outputs.\n"
                    "The company needs a solution to prevent the application from displaying PII in outputs while meeting all other operational requirements.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure Amazon Bedrock guardrails with sensitive information filters to detect and block PII in model outputs.",
            "B. Implement a secondary PII detection layer by using regular expressions and custom entity recognition to detect identifiers that Amazon Comprehend Medical misses before sending inputs to Amazon Bedrock.",
            "C. Remove detailed medical context from case histories during pre-processing to prevent the model from generating patient-specific information based on clinical pattern associations.",
            "D. Enable session isolation in Amazon Bedrock API calls. Clear conversation history between requests to prevent patient information from persisting across multiple case analyses.",
        ],
        "answer": "A. Configure Amazon Bedrock guardrails with sensitive information filters to detect and block PII in model outputs.",
        "explanation": "The leak is in the **outputs** (the model generates identifiers that were never in the input), so improving *input* de-identification can't fix it. A guardrail **sensitive-information filter on the output** detects and blocks (or masks) PII in generated text, runs with low added latency (compatible with sub-500 ms) and records interventions for the audit requirement.\n\n"
                       "**B** only strengthens input scrubbing — the model still invents identifiers. **C** removing clinical context degrades the diagnostic purpose. **D** session isolation addresses cross-request memory, which isn't the problem.",
        "reference": f"{_BR}/guardrails-sensitive-filters.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 128, "category": D3, "task": "3.1", "type": "single",
        "question": "A company is designing a GenAI solution to help children between the ages of 8 and 14 understand world history. The system must support concurrent use for up to 30 children in a classroom and provide responses in less than 1 second. The company is using Amazon Bedrock and Amazon Nova Pro with a knowledge base that contains history textbooks that are written for students between the ages of 6 and 21. The company uses an Amazon Bedrock flow to ensure that the solution uses the knowledge base to generate every response. The company sets the prompt response temperature to 0.7.\n"
                    "Early testing of the solution results in some responses that are historically inaccurate, violent, and not appropriate for children. A GenAI developer must prevent the solution from responding to prompts inaccurately and inappropriately.\n"
                    "Which solution will meet this requirement?",
        "options": [
            "A. Increase the inference temperature in the flow. Add a node to the flow after the initial response that calls the Amazon Nova model to remove any violence from the response. Return the result of the model call.",
            "B. Configure Amazon Bedrock guardrails for the model responses by using content filters. Set the content filter strength high and set the guardrail action to block. Add the guardrail to the flow. Reduce the inference temperature in the flow.",
            "C. Use Amazon Bedrock Data Automation with a custom output that removes all violent content from the knowledge base. Increase the inference temperature in the flow.",
            "D. Configure Amazon Bedrock guardrails for the prompts by using content filters. Set the content filter strength to high and set the guardrail action to block. Add the guardrail to the flow. Reduce the inference temperature in the flow.",
        ],
        "answer": "B. Configure Amazon Bedrock guardrails for the model responses by using content filters. Set the content filter strength high and set the guardrail action to block. Add the guardrail to the flow. Reduce the inference temperature in the flow.",
        "explanation": "Two problems → two levers on the **output side**: **inappropriate/violent content** → a guardrail **content filter on model responses** (high strength, action = block) attached to the flow; **historical inaccuracy** → a **lower temperature** so the model sticks to the retrieved textbook content instead of creative variation (exam-guide Skill 4.2.4).\n\n"
                       "**A/C** *increase* the temperature, which makes inaccuracy worse (and A adds a second model call, hurting the 1-second limit). **D** filters the *prompts*, but the unsuitable content is in the *responses*.",
        "reference": f"{_BR}/guardrails.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 129, "category": D1, "task": "1.5", "type": "single",
        "question": "A legal research company is developing an AI-powered chat assistant that uses Amazon Bedrock with a knowledge base that contains millions of legal documents. When attorneys search for legal case precedents, the initial retrieval returns many documents. The company wants the chat assistant to generate all responses within 3 seconds.\n"
                    "The foundation model (FM) that the chat assistant uses has a context window limitation that allows effective processing for only 10 documents for each query. Currently, the retrieval configuration fetches 50 documents by using semantic search. Attorneys report that highly relevant precedents frequently appear in positions 15-40 of the results.\n"
                    "The company needs a solution to improve the relevance of query results. The solution must meet the company's latency and context window constraints.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Maintain the 50-document retrieval but increase the FM's temperature parameter. Implement prompt engineering techniques that instruct the model to identify the most relevant documents from the full result set before the model generates responses.",
            "B. Enable reranking on the knowledge base by using a reranker model with language-specific configurations. Configure the chat assistant to initially retrieve 50 documents. Use the reranker model's cross-encoder architecture to evaluate query-document pairs. Return only the top 10 highest-scored documents.",
            "C. Configure three separate knowledge bases. Configure one knowledge base to use 500 token chunks, another to use 1,000 token chunks, and the third to use 2,000 token chunks. Implement a pre-processing action group by using an AWS Lambda function that retrieves 50 documents from each knowledge base, merges the 150 total results, and uses term frequency - inverse document frequency (TF-IDF) scoring to select the top 10 documents.",
            "D. Implement a post-processing action group by using an AWS Lambda function that retrieves 50 documents and calculates cosine similarity scores between the query embedding and each document embedding by using Amazon Titan Embeddings. Configure the action group to sort by similarity score and return the top 10 documents.",
        ],
        "answer": "B. Enable reranking on the knowledge base by using a reranker model with language-specific configurations. Configure the chat assistant to initially retrieve 50 documents. Use the reranker model's cross-encoder architecture to evaluate query-document pairs. Return only the top 10 highest-scored documents.",
        "explanation": "Classic **retrieve wide, rerank narrow**: fetch 50 candidates cheaply, then a **reranker model** (cross-encoder that scores each query–document pair) promotes the truly relevant precedents from positions 15–40 into the top 10 that fit the context window — a managed Knowledge Bases feature with low latency (exam-guide Skill 1.5.4).\n\n"
                       "**A** a higher temperature adds randomness and the FM can only see 10 documents anyway. **C** three knowledge bases, 150 results and TF-IDF is heavy and keyword-based. **D** re-scoring with the same embedding similarity re-creates the original ordering problem and adds a Lambda hop.",
        "reference": f"{_BR}/rerank.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 130, "category": D2, "task": "2.3", "type": "single",
        "question": "A multinational healthcare company is building a GenAI solution to analyze patient medical records and clinical trial data to identify treatment patterns and generate research insights. Some of the countries where the company operates require the company to store patient data on premises within each country.\n"
                    "The solution must provide low-latency, AI-assisted diagnostics for remote clinics around the world. The solution must use cloud-based foundation models (FMs) to perform advanced, large-scale analytics. The company needs a solution that ensures data residency, delivers sub-100 ms inference at clinics, and supports consistent development workflows across hybrid environments.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Use AWS Global Accelerator to reduce latency for remote clinics. Replicate on-premises patient data to Amazon S3 by using AWS DataSync. Process all model requests through a centralized inference endpoint that is hosted in one AWS Region.",
            "B. Deploy open source FMs on Amazon EC2 instances in each country to comply with data residency requirements. Store patient data locally on Amazon EBS volumes. Use AWS Systems Manager to manage model updates across countries. Manually export aggregated research insights as CSV files to Amazon S3 buckets in each AWS Region to perform cross-country analysis.",
            "C. Deploy FMs in multiple AWS Regions on Amazon EC2 GPU instances. Replicate patient data from on-premises systems to the cloud. Centralize model training and inference.",
            "D. Use AWS Outposts to process and store sensitive on-premises patient data in countries that have data residency requirements. Deploy AWS Wavelength at remote clinics to perform real-time inference.",
        ],
        "answer": "D. Use AWS Outposts to process and store sensitive on-premises patient data in countries that have data residency requirements. Deploy AWS Wavelength at remote clinics to perform real-time inference.",
        "explanation": "Hybrid + residency + edge latency maps to exam-guide Skill 2.3.4: **AWS Outposts** runs AWS services and keeps patient data on premises **inside each country** with the same APIs and tooling as the cloud (consistent development workflows), while **AWS Wavelength** puts compute at the edge for **sub-100 ms** inference at clinics.\n\n"
                       "**A/C** replicate patient data to the cloud and centralise inference, violating residency and the latency target. **B** self-managed open-source FMs, manual CSV exports and Systems Manager updates are the highest overhead.",
        "reference": "https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 131, "category": D1, "task": "1.2", "type": "single",
        "question": "A global company runs an AI-powered document-processing pipeline that uses Amazon Bedrock to summarize text documents. The pipeline occasionally times out during peak traffic periods. The timeouts cause service degradation.\n"
                    "The company needs a solution to detect when error rates exceed 10% within any 60-second window. The solution must switch to an alternate process path when the error rate threshold is exceeded. The solution must automatically resume normal Amazon Bedrock processing when the pipeline recovers. The company must ensure that the pipeline processes all documents within 15 minutes.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure an AWS Step Functions workflow that implements a circuit breaker pattern by tracking Amazon Bedrock invocation failures in Amazon DynamoDB. Configure the workflow to route processing jobs between normal and alternate processing paths based on the current failure state.",
            "B. Configure an AWS Step Functions workflow that uses an AWS Lambda function to poll Amazon CloudWatch metrics for Amazon Bedrock. Store error rate metrics in Amazon DynamoDB. When the error rate exceeds 10%, instruct company staff to manually update the workflow to divert traffic to the alternate processing path.",
            "C. Configure an AWS Step Functions state machine that includes a Task state to implement Retry/Catch logic for Amazon Bedrock calls. Configure an Amazon CloudWatch alarm that triggers an Amazon EventBridge rule to direct traffic from the state machine to the alternate processing path when the error rate exceeds 10%.",
            "D. Deploy multiple identical AWS Step Functions state machines that use multiple Amazon Bedrock models behind an Amazon API Gateway API. Use a custom health check AWS Lambda function to route requests to whichever state machine responds fastest.",
        ],
        "answer": "A. Configure an AWS Step Functions workflow that implements a circuit breaker pattern by tracking Amazon Bedrock invocation failures in Amazon DynamoDB. Configure the workflow to route processing jobs between normal and alternate processing paths based on the current failure state.",
        "explanation": "This is the **circuit breaker pattern** (exam-guide Skill 1.2.3): failures are counted over a window in **DynamoDB**, the workflow reads the breaker state — *closed* (normal Bedrock path), *open* (alternate path) and *half-open* (probe) — so it **switches automatically** when errors exceed 10% in 60 seconds and **resumes normal processing** when the probe succeeds, with no manual steps.\n\n"
                       "**B** requires staff to manually divert traffic. **C** Retry/Catch handles individual failures, and the alarm-based switch has no automatic way to resume normal processing or measure a 60-second rolling rate. **D** racing multiple state machines is wasteful and doesn't detect error rates.",
        "reference": "https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html",
        "note": "Answer derived. High confidence.",
    },
    {
        "id": 132, "category": D1, "task": "1.3", "type": "single",
        "question": "A media company needs to automatically generate searchable metadata for a video library that contains 10,000 hours of content. Each video includes visual scenes, spoken dialogue, background music, and on-screen text.\n"
                    "The company needs a solution to extract scene descriptions, speaker transcripts with timestamps, text overlay content, and emotional context from each video. The output must synchronize all metadata types with one another and create a searchable index. Users must be able to search based on any metadata type and jump directly to a specific moment in each video.\n"
                    "What solution will meet these requirements?",
        "options": [
            "A. Create an Amazon SageMaker AI processing job that extracts video frames at regular intervals. Use Amazon Transcribe to process audio and perform speech-to-text conversions. Use an Anthropic Claude model in Amazon Bedrock to process frames individually to produce multimodal scene analyses. Store outputs in separate Amazon S3 buckets that are organized by content type.",
            "B. Create an Amazon SageMaker AI processing job that extracts video frames at fixed intervals and attaches timestamps. Use Amazon Transcribe with time markers enabled to process audio. Use an Anthropic Claude model in Amazon Bedrock to analyze frame-transcript pairs. Store outputs in a unified JSON structure that preserves temporal relationships.",
            "C. Create an Amazon SageMaker AI parallel processing job that is orchestrated by a SageMaker AI pipeline. Configure multiple steps in the pipeline to extract video segments, process audio streams by using Amazon Transcribe, analyze video frames by using Amazon Rekognition to detect text in scenes, use Amazon Comprehend to perform sentiment analysis, and store unified metadata in Amazon DynamoDB with time-based partitioning.",
            "D. Create an Amazon SageMaker AI processing job that configures Anthropic Claude Opus in Amazon Bedrock to produce a comprehensive multimodal analysis for each video. Configure the processing job to extract metadata by using a single inference request and to index results in Amazon OpenSearch Service to provide temporal search capabilities.",
        ],
        "answer": "B. Create an Amazon SageMaker AI processing job that extracts video frames at fixed intervals and attaches timestamps. Use Amazon Transcribe with time markers enabled to process audio. Use an Anthropic Claude model in Amazon Bedrock to analyze frame-transcript pairs. Store outputs in a unified JSON structure that preserves temporal relationships.",
        "explanation": "The key requirement is **synchronisation across metadata types**. B timestamps every extracted frame and the Transcribe output (**time markers**), then has a multimodal FM analyse **frame + matching transcript pairs** together, so scene description, dialogue, on-screen text and emotional context are produced against the same timeline and stored in one **unified structure that preserves temporal relationships** — enabling 'jump to this moment' search (exam-guide Skill 1.3.2).\n\n"
                       "**A** stores outputs in separate buckets by type (not synchronised). **D** one inference request per whole video can't give moment-level timestamps. **C** stitches Rekognition and Comprehend outputs, which can't describe scenes or emotional context as well and adds more services.",
        "reference": "https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html",
        "note": "Answer derived, moderate confidence (B vs C). B is the design that keeps modalities aligned on one timeline; its output would then be indexed for search.",
    },
    {
        "id": 133, "category": D3, "task": "3.2", "type": "single",
        "question": "A financial services company is developing a GenAI application that needs to analyze data across multiple AWS accounts by using a foundation model (FM). The data and application are in Amazon S3 buckets in three separate accounts. Account A contains transaction data. Account B contains customer profiles, including personally identifiable information (PII). Account C hosts the GenAI application. The company plans to add data sources from seven more business units within the next few months.\n"
                    "The company must have strict control over PII data. The company must ensure that the FM accesses only necessary data fields.\n"
                    "The company needs a solution to establish secure cross-account access for the GenAI application.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use AWS Identity Center to create a permission set for the FM service account. Configure resource-based policies on each S3 bucket to allow specific access to Account C. Deploy a custom AWS Lambda authorizer to filter PII data before passing it to the FM.",
            "B. Configure Amazon Bedrock cross-account IAM roles. Create role-based access policies in each source account that allow access only for specific S3 bucket paths. Apply tagbased access controls on S3 objects to classify and control access to PII data.",
            "C. Set up AWS Lake Formation in each source account. Register the S3 buckets with Lake Formation. Create IAM roles in each source account that have permissions to access specific S3 bucket paths. Configure Lake Formation permissions to allow access only to specific data columns by using Lake Formation tag-based access controls. Use Amazon SageMaker AI to deploy the FM with an execution role in Account C that can assume the cross-account IAM roles to access the data through Lake Formation.",
            "D. Configure resource-based policies on S3 buckets in each source account to allow access from the GenAI application in Account C. Configure identity-based policies for the FM's service role that allow access only to specific data columns by using AWS Lake Formation tag-based access controls. Set up a VPC endpoint in each account to provide secure cross-account access.",
        ],
        "answer": "C. Set up AWS Lake Formation in each source account. Register the S3 buckets with Lake Formation. Create IAM roles in each source account that have permissions to access specific S3 bucket paths. Configure Lake Formation permissions to allow access only to specific data columns by using Lake Formation tag-based access controls. Use Amazon SageMaker AI to deploy the FM with an execution role in Account C that can assume the cross-account IAM roles to access the data through Lake Formation.",
        "explanation": "'**Only necessary data fields**' + strict PII control = **column-level access**, which is **Lake Formation**; **tag-based access control** (LF-Tags) scales to the seven additional business units (tag, don't re-engineer). Cross-account access uses a **role in each source account that the application's execution role assumes**, so every account keeps its own boundary and audit trail (exam-guide Skill 3.2.1).\n\n"
                       "**A** a custom Lambda authorizer filtering PII is custom work and not a data-layer control. **B** S3 paths and object tags can't restrict individual columns. **D** S3 resource policies grant object-level access that bypasses Lake Formation's column controls, and a VPC endpoint isn't a cross-account access mechanism.",
        "reference": "https://docs.aws.amazon.com/lake-formation/latest/dg/tag-based-access-control.html",
        "note": "Answer derived, moderate confidence (C vs D). C routes all access through Lake Formation (column-level); D's S3 resource policies would bypass it.",
    },
    {
        "id": 134, "category": D2, "task": "2.1", "type": "single",
        "question": "A logistics company is building an agentic GenAI-powered solution to automate freight optimization. The solution must retrieve data in real time from multiple internal and external systems. The solution must include a human-in-the-loop approval step before the optimization process is finished. The solution must support modular growth as the number of integrations and amount of logic increases.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Use an Amazon SageMaker AI endpoint that hosts a large language model (LLM) that directly calls all internal databases and external APIs. Use a custom web application that provides a UI to implement the human-in-the-loop review step.",
            "B. Build a hierarchical system by using the Strands Agents SDK and Amazon Bedrock AgentCore. Configure a coordinating agent to delegate tasks to multiple specialized agents. Use MCP to facilitate inter-agent messaging. Use AWS Step Functions to implement a human-in-the-loop approval step.",
            "C. Use AWS Glue to aggregate operational data into Amazon S3. Use Amazon Athena to query the data. Invoke an AWS Lambda function to generate route assignments. Use Amazon SNS to send notifications to supervisor agents.",
            "D. Use a single Amazon Bedrock AgentCore agent with AWS Lambda based tools to integrate with all internal and external systems. Use AWS Step Functions to orchestrate the approval workflow.",
        ],
        "answer": "B. Build a hierarchical system by using the Strands Agents SDK and Amazon Bedrock AgentCore. Configure a coordinating agent to delegate tasks to multiple specialized agents. Use MCP to facilitate inter-agent messaging. Use AWS Step Functions to implement a human-in-the-loop approval step.",
        "explanation": "**Modular growth** is the discriminator: a **coordinator agent delegating to specialised agents** (Strands Agents on AgentCore) lets you add integrations as new specialised agents/tools via **MCP** without growing one monolith, while **Step Functions** provides the managed **human approval** (callback) step (exam-guide Skills 2.1.1, 2.1.5, 2.1.7).\n\n"
                       "**A** a custom-built LLM serving and UI is the highest overhead. **C** Glue/Athena aggregation isn't *real-time* retrieval and isn't agentic. **D** a single agent with every tool becomes harder to extend as logic grows.",
        "reference": f"{_AC}/what-is-bedrock-agentcore.html",
        "note": "Answer derived, moderate-high confidence (B vs D): 'modular growth' favours the multi-agent design.",
    },
    {
        "id": 135, "category": D2, "task": "2.3", "type": "single",
        "question": "A financial services company is building a fraud detection system by using Amazon Bedrock. The system will monitor activity in multiple stock trading applications that run in the United States and Europe. The system must process 1,000 transactions every second with sub-500 ms response times. The system must also maintain high availability during connectivity disruptions.\n"
                    "The company must ensure that data for European customers is processed only in AWS Regions that are based in Europe.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure AWS Lambda functions and Amazon EKS applications to use the InvokeModel API with a global inference profile. Deploy an automated failover system that uses Amazon Route 53 health checks. Create a dedicated European inference profile and enable Geographic cross-Region inference for European applications. Use Amazon CloudWatch alarms to monitor utilization metrics.",
            "B. Configure all applications to use the InvokeModel API with provisioned throughput for an Anthropic Claude model in each Region separately. Set up a custom Application Load Balancer to distribute traffic based on Regional capacity and response times. Implement a Regional failover mechanism that uses Amazon EventBridge rules to handle connectivity disruptions.",
            "C. Configure all applications to use the InvokeModelWithResponseStream API with on-demand throughput. Deploy an Amazon API Gateway REST API with Regional endpoints in each location where the company operates to route requests to the closest Amazon Bedrock endpoint. Create separate IAM roles for applications that run in the United States and Europe. Grant the IAM roles Region-specific permissions.",
            "D. Configure applications that run in the United States to use provisioned throughput with the InvokeModel API. Configure European applications to use a Europe-specific geographic inference profile to ensure data sovereignty. Configure automatic scaling for provisioned capacity based on utilization metrics. Use Amazon EventBridge and AWS Lambda functions to implement cross-Region failover mechanisms.",
        ],
        "answer": 'A. Configure AWS Lambda functions and Amazon EKS applications to use the InvokeModel API '
                  'with a global inference profile. Deploy an automated failover system that uses Amazon Route '
                  '53 health checks. Create a dedicated European inference profile and enable Geographic '
                  'cross-Region inference for European applications. Use Amazon CloudWatch alarms to monitor '
                  'utilization metrics.',
        "explanation": 'Use **cross-Region inference**, chosen per application: US applications use a **global '
                       'inference profile** (routes across commercial Regions, most throughput and availability, '
                       'about 10% cheaper), and European applications use a **geographic EU profile**, so their data'
                       ' is processed only in EU Regions. **Route 53 health-check failover** covers connectivity '
                       'disruptions, and CloudWatch alarms watch utilisation.\\n'
                       '\\n'
                       "**D** relies on things Bedrock doesn't offer: Provisioned Throughput can't be used with "
                       'inference profiles, and there is no automatic scaling of provisioned capacity. **B** builds '
                       'custom load balancing across separately provisioned Regions. **C** on-demand calls without '
                       "failover, and Region-specific IAM permissions don't route traffic.",
        "reference": f"{_BR}/cross-region-inference.html",
        "note": 'Cross-check: changed from D to A. AWS docs show global and geographic (EU) inference '
                "profiles are chosen per application, and that Provisioned Throughput doesn't work with "
                'inference profiles. No auto-scaling for provisioned capacity was found either, which '
                'undercuts D. Moderate confidence (no answer key covers this question).'
    },
    {
        "id": 136, "category": D5, "task": "5.2", "type": "single",
        "question": "A company is implementing a 2-week initiative to incorporate GenAI into several hundred existing applications to provide context-driven natural language help for users. To simplify the process to choose an appropriate model for each application, a GenAI Developer is building a system to automatically compare foundation models (FMs) based on general text generation accuracy. The system runs a job that performs a series of steps.\n"
                    "First, the system creates a service role and attaches an IAM permissions policy that allows Amazon Bedrock to invoke the FMs and grants access to Amazon S3. Then the system requests and receives access to all the FMs that need to be tested. Then the system creates S3 buckets to store the evaluation results. Then the system creates evaluation configurations by using the TREX built-in dataset. Finally, the system specifies the Accuracy metric and Generation evaluation type in each evaluation configuration.\n"
                    "When the GenAI developer attempts to run the system, it fails with an AccessDenied exception. The GenAI developer must resolve the issue.\n"
                    "Which solution will meet this requirement?",
        "options": [
            "A. Create a trust policy that defines Amazon Bedrock as the service principal. Attach the trust policy to the service role.",
            "B. Configure cross-origin resource sharing (CORS) permissions that allow GET and DELETE actions on the S3 buckets.",
            "C. Change the test dataset from TREX to Gigaword in the evaluation configurations.",
            "D. Change the evaluation type to Summarization and the metric type to Correctness in the evaluation configurations.",
        ],
        "answer": "A. Create a trust policy that defines Amazon Bedrock as the service principal. Attach the trust policy to the service role.",
        "explanation": "The steps give the service role a **permissions policy** but never a **trust policy**. Bedrock evaluation jobs *assume* the service role, so the role's trust relationship must name **`bedrock.amazonaws.com`** as the service principal; without it, the assume-role call is denied → `AccessDenied` (exam-guide Skill 5.2.2: diagnosing integration problems).\n\n"
                       "**B** CORS is a browser/human-evaluation concern (and unrelated to AccessDenied on assuming a role). **C/D** the TREX dataset (text generation, accuracy) and the Generation/Accuracy configuration are a valid combination; changing them wouldn't fix an authorisation error.",
        "reference": f"{_BR}/model-evaluation-security-service-roles.html",
        "note": "Answer derived. High confidence.",
    },
]
