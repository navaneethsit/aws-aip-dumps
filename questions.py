"""
Question bank for the AIP-C01 (AWS Certified Generative AI Developer –
Professional) practice / mock exam.

Schema for each question dict
-----------------------------
id            : int, unique
category      : str, one of CATEGORIES (the 5 official exam domains)
task          : optional str, official exam-guide task, e.g. "1.6" (shown as a pill)
type          : "single" | "multi"
question      : str, the stem
case          : optional str, key into CASE_STUDIES (long shared scenario text)
options       : list[str]
answer        : str       (single) -> exact option text
                list[str] (multi)  -> exact option texts (AWS: all-or-nothing)
explanation   : str, why the answer is correct and why the distractors are not
reference     : str, AWS documentation URL backing the answer
votes         : optional dict, community vote split {"A": 18, "C": 59, ...}
note          : optional str, caution shown with the feedback (e.g. disputed answer)

To add more questions: append dicts to EXTRA in questions_extra.py (same schema),
then run `python validate.py`.
"""
from questions_extra import EXTRA
from questions_extra2 import EXTRA2
from questions_extra3 import EXTRA3
from questions_extra4 import EXTRA4
from questions_extra5 import EXTRA5

CATEGORIES = [
    "1 · FM Integration, Data & Compliance",
    "2 · Implementation & Integration",
    "3 · Safety, Security & Governance",
    "4 · Operational Efficiency & Optimization",
    "5 · Testing, Validation & Troubleshooting",
]
D1, D2, D3, D4, D5 = CATEGORIES

CASE_STUDIES: dict[str, str] = {}

_DOCS = "https://docs.aws.amazon.com"

QUESTIONS = [
    # ------------------------------------------------------------------ #
    # Exam A · Topic 1 · Q1-Q10 (source: pasted practice set)
    # ------------------------------------------------------------------ #
    {
        "id": 1,
        "category": D3,
        "task": "3.4",
        "type": "single",
        "question": "A retail company has a generative AI (GenAI) product recommendation "
                    "application that uses Amazon Bedrock. The application suggests products to "
                    "customers based on browsing history and demographics. The company needs to "
                    "implement fairness evaluation across multiple demographic groups to detect "
                    "and measure bias in recommendations between two prompt approaches. The "
                    "company wants to collect and monitor fairness metrics in real time. The "
                    "company must receive an alert if the fairness metrics show a discrepancy of "
                    "more than 15% between demographic groups. The company must receive weekly "
                    "reports that compare the performance of the two prompt approaches.\n"
                    "Which solution will meet these requirements with the LEAST custom "
                    "development effort?",
        "options": [
            "A. Configure an Amazon CloudWatch dashboard to display default metrics from Amazon "
            "Bedrock API calls. Create custom metrics based on model outputs. Set up Amazon "
            "EventBridge rules to invoke AWS Lambda functions that perform post-processing "
            "analysis on model responses and publish custom fairness metrics.",
            "B. Create the two prompt variants in Amazon Bedrock Prompt Management. Use Amazon "
            "Bedrock Flows to deploy the prompt variants with defined traffic allocation. "
            "Configure Amazon Bedrock guardrails that have content filters to monitor "
            "demographic fairness. Set up Amazon CloudWatch alarms on the GuardrailContentSource "
            "dimension that use InvocationsIntervened metrics to detect recommendation "
            "discrepancy threshold violations.",
            "C. Set up Amazon SageMaker Clarify to analyze model outputs. Publish fairness "
            "metrics to Amazon CloudWatch. Create CloudWatch composite alarms that combine "
            "SageMaker Clarify bias metrics with Amazon Bedrock latency metrics to provide a "
            "comprehensive fairness evaluation dashboard.",
            "D. Create an Amazon Bedrock model evaluation job to compare fairness between the "
            "two prompt variants. Enable model invocation logging in Amazon CloudWatch. Set up "
            "CloudWatch alarms for InvocationsIntervened metrics with a dimension for each "
            "demographic group.",
        ],
        "answer": "C. Set up Amazon SageMaker Clarify to analyze model outputs. Publish fairness "
                  "metrics to Amazon CloudWatch. Create CloudWatch composite alarms that combine "
                  "SageMaker Clarify bias metrics with Amazon Bedrock latency metrics to provide a "
                  "comprehensive fairness evaluation dashboard.",
        "explanation": "SageMaker Clarify ships ready-made bias/fairness metrics (e.g. difference in "
                       "positive proportions, disparate impact) computed per demographic facet, and "
                       "the results can be published to CloudWatch, where an alarm fires on the 15% "
                       "gap — the least custom code.\n\n"
                       "**A** is all custom: Lambda post-processing plus hand-built metrics.\n"
                       "**B** misuses Guardrails: content filters detect harmful content categories, "
                       "not demographic fairness, and `InvocationsIntervened` counts blocked calls.\n"
                       "**D** misuses model evaluation jobs (offline/batch, not real-time) and "
                       "`InvocationsIntervened` has no per-demographic dimension.",
        "reference": f"{_DOCS}/sagemaker/latest/dg/clarify-measure-post-training-bias.html",
        "votes": {"A": 18, "B": 5, "C": 59, "D": 18},
        "note": "Disputed item (C only 59%). The exam guide (Skill 3.4.2) also lists fairness "
                "metrics in CloudWatch, A/B testing with Prompt Management/Flows, and "
                "LLM-as-a-judge — expect fairness questions to blend these. Here the "
                "'least custom development' cue points to a managed bias tool (Clarify).",
    },
    {
        "id": 2,
        "category": D3,
        "task": "3.1",
        "type": "multi",
        "question": "A finance company is developing an AI assistant to help clients plan "
                    "investments and manage their portfolios. The company identifies several "
                    "high-risk conversation patterns such as requests for specific stock "
                    "recommendations or guaranteed returns. High-risk conversation patterns could "
                    "lead to regulatory violations if the company cannot implement appropriate "
                    "controls.\n"
                    "The company must ensure that the AI assistant does not provide inappropriate "
                    "financial advice, generate content about competitors, or make claims that "
                    "are not factually grounded in the company's approved financial guidance. The "
                    "company wants to use Amazon Bedrock Guardrails to implement a solution.\n"
                    "Which combination of steps will meet these requirements? (Choose three.)",
        "options": [
            "A. Add the high-risk conversation patterns to a denied topics guardrail.",
            "B. Configure a content filter guardrail to filter prompts that contain the "
            "high-risk conversation patterns.",
            "C. Configure a content filter guardrail to filter prompts that contain competitor "
            "names.",
            "D. Add the names of competitors as custom word filters. Set the input and output "
            "actions to block.",
            "E. Set a low grounding score threshold.",
            "F. Set a high grounding score threshold.",
        ],
        "answer": [
            "A. Add the high-risk conversation patterns to a denied topics guardrail.",
            "D. Add the names of competitors as custom word filters. Set the input and output "
            "actions to block.",
            "F. Set a high grounding score threshold.",
        ],
        "explanation": "Match each requirement to the right Guardrails policy:\n"
                       "- **Inappropriate advice → denied topics (A):** you describe custom topics "
                       "(stock picks, guaranteed returns) in natural language and the guardrail blocks them.\n"
                       "- **Competitor content → word filters (D):** custom words/phrases blocked on "
                       "both input and output.\n"
                       "- **Ungrounded claims → contextual grounding check with a HIGH threshold (F):** "
                       "responses scoring below the threshold are blocked, so a higher threshold is stricter.\n\n"
                       "**B/C** are wrong: content filters only cover predefined categories (hate, "
                       "insults, sexual, violence, misconduct, prompt attack). **E** a low threshold "
                       "lets weakly grounded answers through.",
        "reference": f"{_DOCS}/bedrock/latest/userguide/guardrails.html",
        "votes": {"ADF": 100},
    },
    {
        "id": 3,
        "category": D2,
        "task": "2.4",
        "type": "single",
        "question": "A company has deployed an AI assistant as a React application that uses AWS "
                    "Amplify, an AWS AppSync GraphQL API, and Amazon Bedrock Knowledge Bases. The "
                    "application uses the GraphQL API to call the Amazon Bedrock "
                    "RetrieveAndGenerate API for knowledge base interactions. The company "
                    "configures an AWS Lambda resolver to use the RequestResponse invocation "
                    "type.\n"
                    "Application users report frequent timeouts and slow response times. Users "
                    "report these problems more frequently for complex questions that require "
                    "longer processing.\n"
                    "The company needs a solution to fix these performance issues and enhance the "
                    "user experience.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use AWS Amplify AI Kit to implement streaming responses from the GraphQL API and "
            "to optimize client-side rendering.",
            "B. Increase the timeout value of the Lambda resolver. Implement retry logic with "
            "exponential backoff.",
            "C. Update the application to send an API request to an Amazon SQS queue. Update the "
            "AWS AppSync resolver to poll and process the queue.",
            "D. Change the RetrieveAndGenerate API to the InvokeModelWithResponseStream API. "
            "Update the application to use an Amazon API Gateway WebSocket API to support the "
            "streaming response.",
        ],
        "answer": "A. Use AWS Amplify AI Kit to implement streaming responses from the GraphQL API "
                  "and to optimize client-side rendering.",
        "explanation": "The root cause is a synchronous request/response path: long answers hit the "
                       "AppSync/Lambda time limits and users see nothing until the end. Streaming "
                       "partial tokens through the existing Amplify + AppSync stack (Amplify AI Kit) "
                       "fixes both timeouts and perceived latency with the least rework.\n\n"
                       "**B** a longer Lambda timeout doesn't lift AppSync's own request limit, and "
                       "retries add latency. **C** AppSync resolvers can't poll SQS; async queuing "
                       "also adds delay. **D** abandons AppSync and the managed RAG call "
                       "(RetrieveAndGenerate) — a large redesign.",
        "reference": "https://docs.amplify.aws/react/ai/",
        "votes": {"A": 62, "D": 38},
        "note": "Disputed (A 62% vs D 38%). D would also stream, but it replaces AppSync and the "
                "managed RAG API; A keeps the architecture. Prefer the option that fixes the "
                "problem inside the existing stack.",
    },
    {
        "id": 4,
        "category": D1,
        "task": "1.2",
        "type": "single",
        "question": "An ecommerce company operates a global product recommendation system that "
                    "needs to switch between multiple foundation models (FM) in Amazon Bedrock "
                    "based on regulations, cost optimization, and performance requirements. The "
                    "company must apply custom controls based on proprietary business logic, "
                    "including dynamic cost thresholds, AWS Region-specific compliance rules, and "
                    "real-time A/B testing across multiple FMs. The system must be able to switch "
                    "between FMs without deploying new code. The system must route user requests "
                    "based on complex rules including user tier, transaction value, regulatory "
                    "zone, and real-time cost metrics that change hourly and require immediate "
                    "propagation across thousands of concurrent requests.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Deploy an AWS Lambda function that uses environment variables to store routing "
            "rules and Amazon Bedrock FM IDs. Use the Lambda console to update the environment "
            "variables when business requirements change. Configure an Amazon API Gateway REST "
            "API to read request parameters to make routing decisions.",
            "B. Deploy Amazon API Gateway REST API request transformation templates to implement "
            "routing logic based on request attributes. Store Amazon Bedrock FM endpoints as "
            "REST API stage variables. Update the variables when the system switches between "
            "models.",
            "C. Configure an AWS Lambda function to fetch routing configurations from the AWS "
            "AppConfig Agent for each user request. Run business logic in the Lambda function "
            "to select the appropriate FM for each request. Expose the FM through a single "
            "Amazon API Gateway REST API endpoint.",
            "D. Use AWS Lambda authorizers for an Amazon API Gateway REST API to evaluate routing "
            "rules that are stored in AWS AppConfig. Return authorization contexts based on "
            "business logic. Route requests to model-specific Lambda functions for each Amazon "
            "Bedrock FM.",
        ],
        "answer": "C. Configure an AWS Lambda function to fetch routing configurations from the AWS "
                  "AppConfig Agent for each user request. Run business logic in the Lambda function "
                  "to select the appropriate FM for each request. Expose the FM through a single "
                  "Amazon API Gateway REST API endpoint.",
        "explanation": "'Switch models **without deploying code**' + hourly-changing rules = **AWS "
                       "AppConfig**. The AppConfig Agent (Lambda extension) caches configuration "
                       "locally and polls for updates, so each request reads fresh rules with low "
                       "latency, while the proprietary routing logic lives in code.\n\n"
                       "**A** environment variables need a function update/redeploy and are not "
                       "dynamic. **B** stage variables and mapping templates can't express complex "
                       "business logic and need stage redeployment. **D** authorizer results are "
                       "cached (TTL), delaying propagation, and it needs one Lambda per FM — more "
                       "moving parts.",
        "reference": f"{_DOCS}/appconfig/latest/userguide/what-is-appconfig.html",
        "votes": {"C": 100},
    },
    {
        "id": 5,
        "category": D1,
        "task": "1.6",
        "type": "single",
        "question": "A company is developing an internal generative AI (GenAI) assistant that uses "
                    "Amazon Bedrock to summarize corporate documents for multiple business units. "
                    "The GenAI assistant must generate responses in a consistent format that "
                    "includes a document summary, classification of business risks, and terms "
                    "that are flagged for review. The GenAI assistant must adapt the tone of "
                    "responses for each user's business unit, such as legal, human resources, or "
                    "finance. The GenAI assistant must block hate speech, inappropriate topics, "
                    "and sensitive information such as personal health information.\n"
                    "The company needs a solution to centrally manage prompt variants across "
                    "business units and teams. The company wants to minimize ongoing "
                    "orchestration efforts and maintenance for post-processing logic. The company "
                    "also wants to have the ability to adjust content moderation criteria for the "
                    "GenAI assistant over time.\n"
                    "Which solution will meet these requirements with the LEAST maintenance "
                    "overhead?",
        "options": [
            "A. Use Amazon Bedrock Prompt Management to configure reusable templates and business "
            "unit-specific prompt variants. Apply Amazon Bedrock guardrails that have category "
            "filters and sensitive term lists to block prohibited content.",
            "B. Use Amazon Bedrock Prompt Management to define base templates. Enforce business "
            "unit-specific tone by using system prompt variables. Configure Amazon Bedrock "
            "guardrails to apply audience-based threshold tuning. Manage the guardrails by using "
            "an internal administration API.",
            "C. Use Amazon Bedrock with business unit-based instruction injection in API calls. "
            "Store response formatting rules in Amazon DynamoDB. Use AWS Step Functions to "
            "validate responses. Use Amazon Comprehend to apply content filters after the GenAI "
            "assistant generates responses.",
            "D. Use Amazon Bedrock with custom prompt templates that are stored in Amazon "
            "DynamoDB. Create one AWS Lambda function to select business unit-specific prompts. "
            "Create a second Lambda function to call Amazon Comprehend to filter prohibited "
            "content from responses.",
        ],
        "answer": "A. Use Amazon Bedrock Prompt Management to configure reusable templates and "
                  "business unit-specific prompt variants. Apply Amazon Bedrock guardrails that "
                  "have category filters and sensitive term lists to block prohibited content.",
        "explanation": "Both halves have a native managed feature: **Prompt Management** for central "
                       "templates + per-unit variants (consistent format and tone), and **Guardrails** "
                       "(content filters, denied topics, word/PII filters) for moderation that can be "
                       "edited over time — no orchestration or post-processing code.\n\n"
                       "**B** invents 'audience-based threshold tuning' and an internal admin API "
                       "(custom). **C/D** rebuild templating in DynamoDB/Lambda and bolt on "
                       "Comprehend + Step Functions post-processing — exactly the maintenance the "
                       "company wants to avoid.",
        "reference": f"{_DOCS}/bedrock/latest/userguide/prompt-management.html",
        "votes": {"A": 100},
    },
    {
        "id": 6,
        "category": D1,
        "task": "1.4",
        "type": "single",
        "question": "A financial services company is building a customer support application that "
                    "retrieves relevant financial regulation documents from a database based on "
                    "semantic similarities to user queries. The application must integrate with "
                    "Amazon Bedrock to generate responses. The application must be able to search "
                    "documents that are in English, Spanish, and Portuguese. The application must "
                    "filter documents by metadata such as publication date, regulatory agency, and "
                    "document type.\n"
                    "The database stores approximately 10 million document embeddings. To "
                    "minimize operational overhead, the company wants a solution that minimizes "
                    "management and maintenance effort. The application must provide low-latency "
                    "responses for real-time customer interactions.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon OpenSearch Serverless to provide vector search capabilities and "
            "metadata filtering. Connect to Amazon Bedrock Knowledge Bases to enable Retrieval "
            "Augmented Generation (RAG) capabilities that use an Anthropic Claude foundation "
            "model (FM).",
            "B. Deploy an Amazon Aurora PostgreSQL database with the pgvector extension. Define "
            "tables to store embeddings and metadata. Use SQL queries to perform similarity "
            "searches. Send retrieved documents to Amazon Bedrock to generate responses.",
            "C. Use Amazon S3 Vectors to configure a vector index and non-filterable metadata "
            "fields. Integrate S3 Vectors with Amazon Bedrock to enable Retrieval Augmented "
            "Generation (RAG) capabilities.",
            "D. Set up an Amazon Neptune Analytics graph database. Configure a vector index that "
            "has appropriate dimensionality to store document embeddings. Use Amazon Bedrock to "
            "perform graph-based retrieval and to generate responses.",
        ],
        "answer": "A. Use Amazon OpenSearch Serverless to provide vector search capabilities and "
                  "metadata filtering. Connect to Amazon Bedrock Knowledge Bases to enable "
                  "Retrieval Augmented Generation (RAG) capabilities that use an Anthropic Claude "
                  "foundation model (FM).",
        "explanation": "OpenSearch Serverless is fully managed, handles ~10M vectors at low latency, "
                       "supports metadata filtering, and is a native vector store for Bedrock "
                       "Knowledge Bases (managed ingestion + RAG). A multilingual embedding model "
                       "covers English/Spanish/Portuguese.\n\n"
                       "**B** Aurora + pgvector means you run, size and tune the database and the "
                       "retrieval code (pgvector is the right pick for smaller corpora, ~<1M). "
                       "**C** the option's *non-filterable* metadata fails the filtering requirement. "
                       "**D** Neptune Analytics is for graph workloads — unnecessary here.",
        "reference": f"{_DOCS}/bedrock/latest/userguide/knowledge-base-setup.html",
        "votes": {"A": 100},
    },
    {
        "id": 7,
        "category": D1,
        "task": "1.5",
        "type": "single",
        "question": "A medical company is building a generative AI (GenAI) application that uses "
                    "RAG to provide evidence-based medical information. The application uses "
                    "Amazon OpenSearch Service to retrieve vector embeddings. Users report that "
                    "searches frequently miss results that contain exact medical terms and "
                    "acronyms and return too many semantically similar but irrelevant documents. "
                    "The company needs to improve retrieval quality and maintain low end user "
                    "latency, even as the document collection grows to millions of documents.\n"
                    "Which solution will meet these requirements with the LEAST operational "
                    "overhead?",
        "options": [
            "A. Configure hybrid search by combining vector similarity with keyword matching to "
            "improve semantic understanding and exact term and acronym matching.",
            "B. Increase the dimensions of the vector embeddings from 384 to 1536. Use a "
            "post-processing AWS Lambda function to filter out irrelevant results after "
            "retrieval.",
            "C. Replace OpenSearch Service with Amazon Kendra. Use query expansion to handle "
            "medical acronyms and terminology variants during pre-processing.",
            "D. Implement a two-stage retrieval architecture in which initial vector search "
            "results are re-ranked by an ML model that is hosted on Amazon SageMaker AI.",
        ],
        "answer": "A. Configure hybrid search by combining vector similarity with keyword matching "
                  "to improve semantic understanding and exact term and acronym matching.",
        "explanation": "The symptom is classic: pure vector search misses **exact tokens/acronyms**. "
                       "Hybrid search (BM25 keyword + vector, score-combined) is built into "
                       "OpenSearch, so it fixes both misses and noise with a config change and no "
                       "new infrastructure.\n\n"
                       "**B** bigger embeddings don't create exact-match ability, and a Lambda filter "
                       "adds latency. **C** a platform migration is high effort. **D** a self-hosted "
                       "SageMaker reranker adds an endpoint to run and scale.",
        "reference": "https://opensearch.org/docs/latest/search-plugins/hybrid-search/",
        "votes": {"A": 100},
    },
    {
        "id": 8,
        "category": D3,
        "task": "3.2",
        "type": "single",
        "question": "A company runs a generative AI (GenAI)-powered summarization application in an "
                    "application AWS account that uses Amazon Bedrock. The application "
                    "architecture includes an Amazon API Gateway REST API that forwards requests "
                    "to AWS Lambda functions that are attached to private VPC subnets. The "
                    "application summarizes sensitive customer records that the company stores in "
                    "a governed data lake in a centralized data storage account. The company has "
                    "enabled Amazon S3, Amazon Athena, and AWS Glue in the data storage account.\n"
                    "The company must ensure that calls that the application makes to Amazon "
                    "Bedrock use only private connectivity between the company's application VPC "
                    "and Amazon Bedrock. The company's data lake must provide fine-grained "
                    "column-level access across the company's AWS accounts.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. In the application account, create interface VPC endpoints for Amazon Bedrock "
            "runtimes. Run Lambda functions in private subnets. Use IAM conditions on inference "
            "and data-plane policies to allow calls only to approved endpoints and roles. In the "
            "data storage account, use AWS Lake Formation LF-tag-based access control to create "
            "table and column-level cross-account grants.",
            "B. Run Lambda functions in private subnets. Configure a NAT gateway to provide access "
            "to Amazon Bedrock and the data lake. Use S3 bucket policies and ACLs to manage "
            "permissions. Export AWS CloudTrail logs to Amazon S3 to perform weekly reviews.",
            "C. Create a gateway endpoint only for Amazon S3 in the application account. Invoke "
            "Amazon Bedrock through public endpoints. Use database-level grants in AWS Lake "
            "Formation to manage data access. Stream AWS CloudTrail logs to Amazon CloudWatch "
            "Logs. Do not set up metric filters or alarms.",
            "D. Use VPC endpoints to provide access to Amazon Bedrock and Amazon S3 in the "
            "application account. Use only IAM path-based policies to manage data lake access. "
            "Send AWS CloudTrail logs to Amazon CloudWatch Logs. Periodically create dashboards "
            "and allow public fallback for cross-Region reads to reduce setup time.",
        ],
        "answer": "A. In the application account, create interface VPC endpoints for Amazon Bedrock "
                  "runtimes. Run Lambda functions in private subnets. Use IAM conditions on "
                  "inference and data-plane policies to allow calls only to approved endpoints and "
                  "roles. In the data storage account, use AWS Lake Formation LF-tag-based access "
                  "control to create table and column-level cross-account grants.",
        "explanation": "Two decisive cues: **private connectivity to Bedrock → interface VPC endpoint "
                       "(AWS PrivateLink)** for the Bedrock runtime; **fine-grained column-level, "
                       "cross-account access → AWS Lake Formation** (LF-tags scale across accounts).\n\n"
                       "**B** a NAT gateway routes over the public internet path; S3 ACLs aren't "
                       "column-level. **C** invokes Bedrock publicly and uses only database-level "
                       "grants. **D** IAM path policies can't do column-level control, and 'public "
                       "fallback' defeats private-only connectivity.",
        "reference": f"{_DOCS}/bedrock/latest/userguide/vpc-interface-endpoints.html",
        "votes": {"A": 100},
    },
    {
        "id": 9,
        "category": D1,
        "task": "1.6",
        "type": "single",
        "question": "A media company must use Amazon Bedrock to implement a robust governance "
                    "process for AI-generated content. The company needs to manage hundreds of "
                    "prompt templates. Multiple teams use the templates across multiple AWS "
                    "Regions to generate content. The solution must provide version control with "
                    "approval workflows that include notifications for pending reviews. The "
                    "solution must also provide detailed audit trails that document prompt "
                    "activities and consistent prompt parameterization to enforce quality "
                    "standards.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure Amazon Bedrock Studio prompt templates. Use Amazon CloudWatch to create "
            "dashboards that display prompt usage metrics. Store the approval status of content "
            "in Amazon DynamoDB. Use AWS Lambda functions to enforce approvals.",
            "B. Use Amazon Bedrock Prompt Management to implement version control. Configure AWS "
            "CloudTrail for audit logging. Use IAM policies to control approval permissions. "
            "Create parameterized prompt templates by specifying variables.",
            "C. Use AWS Step Functions to create an approval workflow. Store prompts as documents "
            "in Amazon S3. Use tags to implement version control. Use Amazon EventBridge to send "
            "notifications.",
            "D. Deploy Amazon SageMaker Canvas with prompt templates that are stored in Amazon S3. "
            "Use AWS CloudFormation to implement version control. Use AWS Config to enforce "
            "approval policies.",
        ],
        "answer": "B. Use Amazon Bedrock Prompt Management to implement version control. Configure "
                  "AWS CloudTrail for audit logging. Use IAM policies to control approval "
                  "permissions. Create parameterized prompt templates by specifying variables.",
        "explanation": "Prompt Management natively provides **versioning** and **variables** "
                       "(parameterized templates); **CloudTrail** records API activity for the audit "
                       "trail; **IAM** controls who may create/approve/use versions. This maps "
                       "directly to exam-guide Skill 1.6.3 (prompt governance).\n\n"
                       "**A** tracks content approvals in DynamoDB rather than governing templates. "
                       "**C** rebuilds versioning with S3 tags (custom). **D** SageMaker Canvas is "
                       "no-code ML, and AWS Config evaluates resource configuration — not prompt "
                       "approvals.",
        "reference": f"{_DOCS}/bedrock/latest/userguide/prompt-management.html",
        "votes": {"B": 100},
    },
    {
        "id": 10,
        "category": D2,
        "task": "2.4",
        "type": "single",
        "question": "A company is developing a customer support application that uses Amazon "
                    "Bedrock foundation models (FMs) to provide real-time AI assistance to the "
                    "company's employees. The application must display AI-generated responses "
                    "character by character as the responses are generated. The application needs "
                    "to support thousands of concurrent users with minimal latency. The responses "
                    "typically take 15 to 45 seconds to finish.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure an Amazon API Gateway WebSocket API with an AWS Lambda integration. "
            "Configure the WebSocket API to invoke the Amazon Bedrock "
            "InvokeModelWithResponseStream API and stream partial responses through WebSocket "
            "connections.",
            "B. Configure an Amazon API Gateway REST API with an AWS Lambda integration. Configure "
            "the REST API to invoke the Amazon Bedrock standard InvokeModel API and implement "
            "frontend client-side polling every 100 ms for complete response chunks.",
            "C. Implement direct frontend client connections to Amazon Bedrock by using IAM user "
            "credentials and the InvokeModelWithResponseStream API without any intermediate "
            "gateway or proxy layer.",
            "D. Configure an Amazon API Gateway HTTP API with an AWS Lambda integration. Configure "
            "the HTTP API to cache complete responses in an Amazon DynamoDB table and serve the "
            "responses through multiple paginated GET requests to frontend clients.",
        ],
        "answer": "A. Configure an Amazon API Gateway WebSocket API with an AWS Lambda integration. "
                  "Configure the WebSocket API to invoke the Amazon Bedrock "
                  "InvokeModelWithResponseStream API and stream partial responses through "
                  "WebSocket connections.",
        "explanation": "Token-by-token display needs (1) a model API that emits tokens "
                       "incrementally — **InvokeModelWithResponseStream** — and (2) a transport that "
                       "can push them to the browser over a long-lived connection — **API Gateway "
                       "WebSocket** (or SSE). 15–45 s responses also exceed what a plain synchronous "
                       "request comfortably handles.\n\n"
                       "**B** polling a non-streaming InvokeModel can't show partial text. **C** "
                       "embedding long-lived IAM user credentials in a front end is a security "
                       "anti-pattern. **D** caching full responses and paginating is not streaming.",
        "reference": f"{_DOCS}/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html",
        "votes": {"A": 100},
    },
] + EXTRA + EXTRA2 + EXTRA3 + EXTRA4 + EXTRA5
