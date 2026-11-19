"""
AIP-C01 questions 137-149: the 13 questions in resources/1.text that were not already in the
bank (the other 37 were duplicates and were skipped).

That file carries an answer letter and an explanation for each question, but its letters are not
fully reliable (e.g. file Q7's letter contradicts its own explanation), so each answer here was
checked by reasoning against the exam guide and AWS docs. IDs are new (the file's own numbering
is not used). Same schema as questions.py.
"""

_BR = "https://docs.aws.amazon.com/bedrock/latest/userguide"
_AC = "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide"

D1 = "1 · FM Integration, Data & Compliance"
D2 = "2 · Implementation & Integration"
D3 = "3 · Safety, Security & Governance"
D4 = "4 · Operational Efficiency & Optimization"
D5 = "5 · Testing, Validation & Troubleshooting"

EXTRA5: list[dict] = [
    {
        "id": 137, "category": D2, "task": "2.1", "type": "single",
        "question": "A company is building a custom agentic application. The company must have fine-grained control over the agent orchestration loop. The application must implement custom logic to select tools, handle multi-turn conversations that involve complex state management, integrate with proprietary logging systems, and implement custom retry strategies for tool failures. The company wants to use Amazon Bedrock FMs but must have full control over the orchestration logic. The company has expertise in building orchestration logic but wants to use AWS infrastructure to manage model inference and tool execution.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon Bedrock AgentCore Runtime to deploy the application agents. Use AgentCore Gateway to integrate the application with tools. Use AgentCore Memory to manage conversation states. Use AgentCore Policy to handle tool selection and retry logic.",
            "B. Use Amazon Bedrock AgentCore to build a custom orchestration layer that controls the agent orchestration loop, tool invocation, and state management. Use Amazon Bedrock to manage model inference.",
            "C. Use Amazon Bedrock AgentCore built-in memory and session management capabilities to persist conversation state. Configure the managed tool execution runtime to automatically handle tool failures and retries.",
            "D. Use AWS Step Functions to orchestrate multiple calls to Amazon Bedrock AgentCore Runtime endpoints. Implement custom state management and retry logic between individual agent invocations.",
        ],
        "answer": "B. Use Amazon Bedrock AgentCore to build a custom orchestration layer that controls the agent orchestration loop, tool invocation, and state management. Use Amazon Bedrock to manage model inference.",
        "explanation": "The defining requirement is that **the company owns the orchestration loop** (tool selection, state, logging, retries) while AWS runs the **model inference and hosting**. AgentCore is framework-agnostic: you can host a fully custom agent loop on it and call Bedrock for inference, keeping every orchestration decision in your code (exam-guide Skill 2.1.1/2.1.6).\n\n"
                       "**A** hands tool selection and retries to AgentCore features — AgentCore *Policy* governs authorization, it doesn't decide which tool to call or implement retry logic. **C** relies on managed, automatic failure handling — the opposite of custom control. **D** puts a Step Functions layer *around* agent endpoints, so the loop inside each agent is still a managed black box.",
        "reference": f"{_AC}/what-is-bedrock-agentcore.html",
        "note": "Answer agrees with the second dump's key (B) and my reasoning. High confidence.",
    },
    {
        "id": 138, "category": D4, "task": "4.1", "type": "single",
        "question": "A company uses Amazon Bedrock to deploy an application that generates technical documentation for users across multiple AWS Regions and in multiple languages. Users frequently submit semantically similar questions in different languages, which results in increased inference costs and response latency.\n"
                    "The company needs a caching solution that significantly reduces inference costs, provides low-latency responses globally, maintains cache freshness with a 5-minute TTL, and minimizes custom cache key generation and application-managed caching logic.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Create a custom caching system that uses AWS Lambda functions to store inference results in an Amazon DynamoDB table. Use Amazon CloudFront to distribute cached responses to global users with a 5-minute TTL.",
            "B. Configure prompt caching in Amazon Bedrock for semantically similar queries across languages. Use Amazon CloudFront and Lambda@Edge functions to handle Regional cache distribution. Set a TTL of 5 minutes for both caching layers.",
            "C. Create Amazon ElastiCache (Redis OSS) clusters in each Region where the application runs to store inference results with custom fingerprinting for multilingual queries. Configure automatic replication between Regional clusters with a 5-minute TTL.",
            "D. Use Amazon DynamoDB Accelerator (DAX) to cache inference results and to automatically manage TTL. Use Amazon CloudFront to distribute API responses globally. Use edge functions to handle language-specific transformations.",
        ],
        "answer": "B. Configure prompt caching in Amazon Bedrock for semantically similar queries across languages. Use Amazon CloudFront and Lambda@Edge functions to handle Regional cache distribution. Set a TTL of 5 minutes for both caching layers.",
        "explanation": "The stem's constraint that eliminates the others is **'minimizes custom cache key generation and application-managed caching logic'**. **A** (custom Lambda + DynamoDB), **C** (ElastiCache with *custom fingerprinting*) and **D** (DAX plus language-specific edge transformations) all require exactly that. **B** is the only option built from managed caching features: **Bedrock prompt caching** (whose default cache lifetime is 5 minutes — matching the TTL clue) plus CloudFront/Lambda@Edge for global low-latency distribution (exam-guide Skill 4.1.4).\n\n"
                       "Be aware the item is flawed: Bedrock prompt caching reuses matching prompt *prefixes*; it does not recognise differently worded or cross-language questions as equivalent.",
        "reference": f"{_BR}/prompt-caching.html",
        "note": "LOW-MODERATE confidence. The second dump's key says C (ElastiCache with custom fingerprinting), arguing that prompt caching can't match paraphrases across languages — which is technically true — but C contradicts the stem's 'minimize custom cache key generation' requirement. I chose B as the only option consistent with the stem's constraints. If you learn the source's real answer, correct it.",
    },
    {
        "id": 139, "category": D1, "task": "1.5", "type": "single",
        "question": "A pharmaceutical company is developing a Retrieval Augmented Generation application that uses an Amazon Bedrock knowledge base. The knowledge base uses Amazon OpenSearch Service as a data source for more than 25 million scientific papers. Users report that the application produces inconsistent answers that cite irrelevant sections of papers when queries span methodology, results, and discussion sections of the papers.\n"
                    "The company needs to improve the knowledge base to preserve semantic context across related paragraphs on the scale of the entire corpus of data.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Configure the knowledge base to use fixed-size chunking. Set a 300-token maximum chunk size and a 10% overlap between chunks. Use an appropriate Amazon Bedrock embedding model.",
            "B. Configure the knowledge base to use hierarchical chunking. Use parent chunks that contain 1,000 tokens and child chunks that contain 200 tokens. Set a 50-token overlap between chunks.",
            "C. Configure the knowledge base to use semantic chunking. Use a buffer size of 1 and a breakpoint percentile threshold of 85% to determine chunk boundaries based on content meaning.",
            "D. Configure the knowledge base not to use chunking. Manually split each document into separate files before ingestion. Apply post-processing reranking during retrieval.",
        ],
        "answer": "B. Configure the knowledge base to use hierarchical chunking. Use parent chunks that contain 1,000 tokens and child chunks that contain 200 tokens. Set a 50-token overlap between chunks.",
        "explanation": "Answers spanning methodology, results and discussion need **broad context around a precise hit**. **Hierarchical chunking** embeds small **child chunks** for precise matching, then returns their larger **parent chunks** at retrieval time, so related paragraphs come back together; it uses no FM during ingestion, which matters across **25 million papers**.\n\n"
                       "**A** small fixed chunks isolate paragraphs from their neighbours. **C** semantic chunking uses a foundation model to find boundaries, adding cost and ingestion time at this scale, and still returns single chunks. **D** no chunking plus manual splitting is not scalable, and reranking can't restore context that was split away.",
        "reference": f"{_BR}/kb-chunking.html",
        "note": "Answer agrees with the second dump's key (B). Moderate-high confidence (B vs C; compare Q32, where the key favoured semantic chunking for a different symptom).",
    },
    {
        "id": 140, "category": D3, "task": "3.3", "type": "single",
        "question": "A research company is developing a GenAI system to produce summaries of technical documents. The company must catalog all data sources in a central location. The company needs a solution that can automatically discover and update data sources. The solution must tag each generated summary with citations as metadata that users can query. The solution must retain tamper-evident, immutable audit logs for every model invocation and store input/output records.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon Comprehend to identify data sources in the documents. Store generated summaries in Amazon S3 and enable S3 Object Lock. Use Amazon CloudWatch metrics to generate reports about application throughput. Do not include logs for each invocation.",
            "B. Use AWS Glue Data Catalog with crawlers to maintain data sources. Store generated summaries in Amazon S3. Write object tags that include a source ID. Store Amazon Bedrock model invocation logs in Amazon S3. Enable S3 Object Lock on the S3 bucket that stores invocation logs. Use AWS CloudTrail log file integrity validation to provide tamper-evident immutability.",
            "C. Store application outputs in Amazon DynamoDB. Apply item-level tags that include source attribution. Write application events to Amazon CloudWatch Logs. Use IAM roles to provide audit traceability.",
            "D. Use AWS AppConfig feature flags to implement data versioning. Restrict access to the model by using IAM condition keys. Maintain a versioned mapping file of source-to-output relationships in Amazon S3.",
        ],
        "answer": "B. Use AWS Glue Data Catalog with crawlers to maintain data sources. Store generated summaries in Amazon S3. Write object tags that include a source ID. Store Amazon Bedrock model invocation logs in Amazon S3. Enable S3 Object Lock on the S3 bucket that stores invocation logs. Use AWS CloudTrail log file integrity validation to provide tamper-evident immutability.",
        "explanation": "Each requirement maps to one native capability (exam-guide Skills 3.3.1–3.3.2): **central catalog with automatic discovery/updates** → **Glue Data Catalog + crawlers**; **citations as queryable metadata** → S3 object tags carrying a source ID; **record of every invocation's input and output** → **Bedrock model invocation logging** to S3; **immutable and tamper-evident** → **S3 Object Lock** on the log bucket plus **CloudTrail log file integrity validation**.\n\n"
                       "**A** explicitly omits per-invocation logs and Comprehend doesn't catalogue sources. **C** CloudWatch Logs plus IAM isn't tamper-evident. **D** AppConfig feature flags are not data versioning, and a mapping file isn't an audit log.",
        "reference": "https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html",
        "note": "Answer agrees with the second dump's key (B). High confidence.",
    },
    {
        "id": 141, "category": D4, "task": "4.3", "type": "single",
        "question": "A financial services company processes more than 10,000 customer inquiries every day through a multi-agent GenAI application that uses Amazon Bedrock AgentCore. The application agents invoke several custom tools. During peak usage periods, users report that the custom tools experience up to 40% failure rates. The tools perform inconsistently for different teams at the company.\n"
                    "A GenAI developer must implement an observability solution that provides end-to-end visibility into agent interactions and tool behavior. The solution must use built-in Amazon Bedrock capabilities and must not require custom instrumentation. The GenAI developer needs a solution that requires minimal performance overhead.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Enable AgentCore Observability and trace collection. Use AWS X-Ray to capture distributed traces for the custom tools. Build Amazon CloudWatch dashboards to visualize metrics for errors, throttling, and latency during peak usage periods.",
            "B. Use Amazon CloudWatch Container Insights to monitor the agents. Configure an AWS Lambda function to poll the Amazon Bedrock API for tool usage metrics. Configure the function to store results in CloudWatch to generate alerts.",
            "C. Build a custom ETL pipeline that uses AWS Lambda functions to process Amazon CloudWatch logs from Amazon Bedrock. Store the processed data in Amazon DynamoDB. Use Amazon QuickSight to visualize cross-team performance patterns.",
            "D. Enable AgentCore Observability and send trace data to Amazon CloudWatch Logs. Use a custom AWS Lambda function to extract tool performance metrics from the logs. Use Amazon Managed Grafana to visualize trends.",
        ],
        "answer": "A. Enable AgentCore Observability and trace collection. Use AWS X-Ray to capture distributed traces for the custom tools. Build Amazon CloudWatch dashboards to visualize metrics for errors, throttling, and latency during peak usage periods.",
        "explanation": "**'Built-in capabilities, no custom instrumentation'** points to **AgentCore Observability**, which emits metrics, logs and traces for agent sessions and tool calls into CloudWatch/X-Ray. Tracing the tools (X-Ray) gives end-to-end visibility, and CloudWatch dashboards show errors, throttling and latency by period (exam-guide Skills 4.3.1, 4.3.4).\n\n"
                       "**B** Container Insights targets containers and a polling Lambda is custom. **C/D** both build custom ETL/extraction functions to derive metrics that the built-in telemetry already provides.",
        "reference": f"{_AC}/observability.html",
        "note": "Answer agrees with the second dump's key (A). High confidence — B, C and D all need custom code.",
    },
    {
        "id": 142, "category": D2, "task": "2.5", "type": "single",
        "question": "A company needs a system to automatically generate study materials from multiple content sources. The content sources include document files (PDF files, PowerPoint presentations, and Word documents) and multimedia files (recorded videos). The system must process more than 10,000 content sources daily with peak loads of 500 concurrent uploads. The system must also extract key concepts from document files and multimedia files and create contextually accurate summaries. The generated study materials must support real-time collaboration with version control.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon Bedrock Data Automation (BDA) with AWS Lambda functions to orchestrate document file processing. Use Amazon Bedrock Knowledge Bases to process all multimedia. Store the content in Amazon DocumentDB with replication. Collaborate by using Amazon SNS topic subscriptions. Track changes by using Amazon Bedrock Agents.",
            "B. Use Amazon Bedrock Data Automation (BDA) with foundation models (FMs) to process document files. Integrate BDA with Amazon Textract for PDF extraction and with Amazon Transcribe for multimedia files. Store the processed content in Amazon S3 with versioning enabled. Store the metadata in Amazon DynamoDB. Collaborate in real time by using AWS AppSync GraphQL subscriptions and DynamoDB.",
            "C. Use Amazon Bedrock Data Automation (BDA) with Amazon SageMaker AI endpoints to host content extraction and summarization models. Use Amazon Bedrock Guardrails to extract content from all file types. Store document files in Amazon Neptune for time series analysis. Collaborate by using Amazon Bedrock Chat for real-time messaging.",
            "D. Use Amazon Bedrock Data Automation (BDA) with AWS Lambda functions to process batches of content files. Fine-tune foundation models (FMs) in Amazon Bedrock to classify documents across all content types. Store the processed data in Amazon ElastiCache (Redis OSS) by using Cluster Mode with sharding. Use Prompt management in Amazon Bedrock for version control.",
        ],
        "answer": "B. Use Amazon Bedrock Data Automation (BDA) with foundation models (FMs) to process document files. Integrate BDA with Amazon Textract for PDF extraction and with Amazon Transcribe for multimedia files. Store the processed content in Amazon S3 with versioning enabled. Store the metadata in Amazon DynamoDB. Collaborate in real time by using AWS AppSync GraphQL subscriptions and DynamoDB.",
        "explanation": "Match each requirement to a purpose-built service: **multimodal extraction at scale** → **Bedrock Data Automation** with FMs for documents, Textract for PDFs and Transcribe for video/audio; **version control of materials** → **S3 versioning**; **metadata** → DynamoDB; **real-time collaboration** → **AppSync GraphQL subscriptions** (push updates to collaborators).\n\n"
                       "**A** Knowledge Bases are a retrieval store, not a multimedia processor, and SNS isn't collaboration. **C** Guardrails don't extract content, Neptune isn't for time series, and 'Bedrock Chat' isn't a collaboration feature. **D** fine-tuning for classification and ElastiCache storage don't address extraction or durable versioning, and Prompt Management versions prompts, not documents.",
        "reference": f"{_BR}/bda.html",
        "note": "Answer agrees with the second dump's key (B). High confidence — the other options misuse services.",
    },
    {
        "id": 143, "category": D1, "task": "1.4", "type": "single",
        "question": "A company is using Amazon Bedrock to build a GenAI assistant that answers employee questions based on internal documentation. The company stores documents in Amazon S3, Atlassian Confluence, and an internal wiki system. The GenAI assistant must retrieve relevant content and provide grounded responses.\n"
                    "The solution must meet the following requirements:\n"
                    "* Integrate multiple document sources into a single retrieval layer.\n"
                    "* Support semantic search rather than keyword-only queries.\n"
                    "* Minimize custom ingestion and synchronization logic.\n"
                    "* Ensure that retrieved content can be directly used to augment the GenAI assistant's foundation model (FM).\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon Bedrock Knowledge Bases and managed data connectors to ingest content from the source documents. Enable semantic retrieval to augment the FM.",
            "B. Index documents from the source documents into Amazon OpenSearch Service by using keyword mappings. Invoke the FM and manually select search results.",
            "C. Store the source documents in Amazon S3. Use AWS Lambda functions to generate embeddings. Implement custom retrieval logic in the GenAI assistant application layer.",
            "D. Store the source documents in Amazon DynamoDB. Query the DynamoDB table directly to provide contextual input to the FM.",
        ],
        "answer": "A. Use Amazon Bedrock Knowledge Bases and managed data connectors to ingest content from the source documents. Enable semantic retrieval to augment the FM.",
        "explanation": "**Bedrock Knowledge Bases** gives one managed retrieval layer over many sources through **managed data connectors** (S3, Confluence and others), handles chunking, embedding and sync, supports **semantic (vector) search**, and returns passages ready to augment the FM — exam-guide Skill 1.4.4 (integration components for document systems and wikis).\n\n"
                       "**B** keyword mappings aren't semantic and results are chosen manually. **C** custom embedding and retrieval code is the ingestion/sync logic the company wants to avoid. **D** DynamoDB isn't a semantic search engine.",
        "reference": f"{_BR}/data-source-connectors.html",
        "note": "Answer agrees with the second dump's key (A). High confidence.",
    },
    {
        "id": 144, "category": D1, "task": "1.5", "type": "single",
        "question": "A financial services company wants to develop an Amazon Bedrock application that gives analysts the ability to query quarterly earnings reports and financial statements. The financial documents are typically 5-100 pages long and contain both tabular data and text. The application must provide contextually accurate responses that preserve the relationship between financial metrics and their explanatory text. To support accurate and scalable retrieval, the application must incorporate document segmentation and context management strategies.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use a direct model invocation approach that uses Anthropic Claude to process each financial document as a single input. Use fine-tuned prompts that instruct the model to parse tables and text separately.",
            "B. Use Amazon Bedrock Knowledge Bases to create a Retrieval Augmented Generation (RAG) application that retrieves relevant information from contextually chunked sections of financial documents. Segment documents based on their structural layout. Include citations that reference the original source materials.",
            "C. Deploy an Amazon Bedrock agent that has an action group that calls custom AWS Lambda functions to analyze financial documents. Configure the Lambda functions to perform fixed-size chunking when a user submits a query about financial metrics.",
            "D. Create one specialized Amazon Bedrock application that is optimized for structured data. Create a second application that is optimized for unstructured data. Configure each application to use a tailored chunking strategy that is suited to the application's content type. Implement logic to link queries to the appropriate sources.",
        ],
        "answer": "B. Use Amazon Bedrock Knowledge Bases to create a Retrieval Augmented Generation (RAG) application that retrieves relevant information from contextually chunked sections of financial documents. Segment documents based on their structural layout. Include citations that reference the original source materials.",
        "explanation": "Metrics sit next to their **explanatory text**, so segmentation must follow the **document's structure** (sections, tables with their commentary) rather than arbitrary token counts. A **Knowledge Base** with structure-aware chunking provides scalable retrieval, managed grounding and **citations** back to the sources (exam-guide Skills 1.5.1, 1.5.6).\n\n"
                       "**A** sending whole 100-page documents in one prompt hits context limits and isn't scalable. **C** fixed-size chunking splits tables from their explanations, and doing it per query in Lambda is slow. **D** separating structured and unstructured content into two applications breaks the very relationship the question wants to preserve.",
        "reference": f"{_BR}/kb-chunking.html",
        "note": "Answer agrees with the second dump's key (B). High confidence.",
    },
    {
        "id": 145, "category": D3, "task": "3.3", "type": "single",
        "question": "A medical company is creating a generative AI (GenAI) system by using Amazon Bedrock. The system processes data from various sources and must maintain end-to-end data lineage. The system must also use real-time personally identifiable information (PII) filtering and audit trails to automatically report compliance.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use AWS Glue Data Catalog to register all data sources and track lineage. Use Amazon Bedrock Guardrails PII filters. Enable AWS CloudTrail logging for all Amazon Bedrock API calls with Amazon S3 integration. Use Amazon Macie to scan stored data for sensitive information and publish findings to Amazon CloudWatch Logs. Create CloudWatch dashboards to visualize the findings and generate automated compliance reports.",
            "B. Use AWS Config to track data source configurations and changes. Use AWS WAF with custom rules to filter PII at the application layer before Amazon Bedrock processes the data. Configure Amazon EventBridge to capture and route audit events to Amazon S3. Use Amazon Comprehend Medical with scheduled AWS Lambda functions to analyze stored outputs for compliance violations.",
            "C. Use AWS DataSync to replicate data sources to track lineage. Configure Amazon Macie to scan Amazon Bedrock outputs for sensitive information. Use AWS Systems Manager Session Manager to log user interactions. Deploy Amazon Textract with AWS Step Functions workflows to identify and redact PII from generated reports.",
            "D. Configure Amazon Athena to query data sources to analyze and report on data lineage. Use Amazon CloudWatch custom metrics to monitor PII exposure in Amazon Bedrock responses and establish AWS X-Ray tracing to generate an audit trail. Use an Amazon Rekognition Custom Labels model to detect sensitive information in the data that Amazon Bedrock processes.",
        ],
        "answer": "A. Use AWS Glue Data Catalog to register all data sources and track lineage. Use Amazon Bedrock Guardrails PII filters. Enable AWS CloudTrail logging for all Amazon Bedrock API calls with Amazon S3 integration. Use Amazon Macie to scan stored data for sensitive information and publish findings to Amazon CloudWatch Logs. Create CloudWatch dashboards to visualize the findings and generate automated compliance reports.",
        "explanation": "Each need has its purpose-built service: **lineage** → Glue Data Catalog; **real-time PII filtering** → **Bedrock Guardrails** sensitive-information filters; **audit trails** → **CloudTrail**; **stored-data PII discovery** → **Macie**; **automated compliance reporting** → CloudWatch dashboards over the findings (exam-guide Skills 3.2.2, 3.3.1–3.3.4).\n\n"
                       "**B** WAF can't reliably detect PII in prompts. **C** DataSync replicates files, it doesn't track lineage, and Textract extracts text rather than redacting. **D** Athena isn't a lineage tracker and Rekognition Custom Labels is for images.",
        "reference": "https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html",
        "note": "Answer agrees with the second dump's key (A). High confidence — see Q19/Q61 for the same service pairings.",
    },
    {
        "id": 146, "category": D3, "task": "3.4", "type": "single",
        "question": "A healthcare company is building a generative AI (GenAI) application to answer patient questions based on patient medical records and published treatment guidelines. To comply with healthcare regulations, the application must provide transparent citations for all information sources. The application must also maintain an audit trail for all data access and ensure that responses reference only authorized medical information.\n"
                    "Which solution will meet these requirements with the LEAST operational overhead?",
        "options": [
            "A. Deploy an Amazon Bedrock AgentCore agent and Amazon Bedrock Prompt Management to generate patient responses.",
            "B. Use Amazon Bedrock Knowledge Bases to connect the application to authorized data sources. Use Amazon CloudWatch to collect comprehensive logs for all queries and response activities.",
            "C. Configure Amazon Bedrock Guardrails to filter patient information. Create a custom vector database outside of AWS to store medical records. Use AWS Lambda functions to track citations.",
            "D. Use Amazon SageMaker AI to fine-tune Amazon Bedrock models by using medical data. Use a custom attribution mechanism in an Amazon API Gateway layer to cite data sources. Store data lineage records in Amazon DynamoDB.",
        ],
        "answer": "B. Use Amazon Bedrock Knowledge Bases to connect the application to authorized data sources. Use Amazon CloudWatch to collect comprehensive logs for all queries and response activities.",
        "explanation": "**Knowledge Bases + RetrieveAndGenerate** return answers with **citations to the specific source chunks**, restrict retrieval to the **authorised data sources** connected to the knowledge base, and CloudWatch collects the query/response logs for the **audit trail** — all managed, so the least overhead (exam-guide Skill 3.4.1).\n\n"
                       "**A** has no retrieval or citation mechanism. **C** a self-built vector database outside AWS and Lambda citation tracking is the highest overhead. **D** fine-tuning bakes data into the model (no per-answer citations or access control) and needs custom attribution.",
        "reference": f"{_BR}/kb-test-retrieve-generate.html",
        "note": "Answer agrees with the second dump's key (B). High confidence.",
    },
    {
        "id": 147, "category": D4, "task": "4.3", "type": "single",
        "question": "A financial services company deploys a RAG application. The application uses Amazon OpenSearch Service to provide vector storage and Amazon Bedrock to generate text. The application ingests thousands of documents daily and processes hundreds of user queries each hour. Several weeks after the deployment, users report increased response times despite sufficient compute resources.\n"
                    "The company needs a monitoring solution that proactively identifies performance issues across the entire RAG pipeline.\n"
                    "Which solution will meet this requirement?",
        "options": [
            "A. Configure Amazon CloudWatch alarms for the OpenSearchDashboardsHealthyNodes metric and the SearchLatency metric. Manually investigate and restart OpenSearch Service instances whenever query response times exceed predefined thresholds based on historical performance patterns.",
            "B. Use Amazon CloudWatch Container Insights to monitor the OpenSearch Service cluster. Use Amazon EventBridge to invoke AWS Systems Manager Automation to restart the OpenSearch Service instances whenever memory usage exceeds 80%.",
            "C. Create basic Amazon CloudWatch dashboards to track CPU and memory usage for individual services. Configure alarms based on static thresholds for query latency. Set up email notifications when thresholds are exceeded.",
            "D. Use Amazon CloudWatch dashboards to monitor end-to-end RAG metrics including vector search latency, foundation model (FM) response times, and document ingestion rates. Set up anomaly detection for the metrics to proactively identify performance degradation before users are affected.",
        ],
        "answer": "D. Use Amazon CloudWatch dashboards to monitor end-to-end RAG metrics including vector search latency, foundation model (FM) response times, and document ingestion rates. Set up anomaly detection for the metrics to proactively identify performance degradation before users are affected.",
        "explanation": "'**Proactively** … **across the entire RAG pipeline**' means watching **every stage** (vector search latency, FM `InvocationLatency`, ingestion rate) together, with **anomaly detection** so gradual degradation (response times creeping up over weeks despite spare compute) is caught against a learned baseline before users notice (exam-guide Skills 4.3.2, 4.3.5).\n\n"
                       "**A/C** static thresholds and manual investigation are reactive. **B** restarting OpenSearch at 80% memory treats a symptom of one component and could cause outages.",
        "reference": f"{_BR}/monitoring-cw.html",
        "note": "Answer agrees with the second dump's key (D). High confidence.",
    },
    {
        "id": 148, "category": D5, "task": "5.2", "type": "single",
        "question": "A healthcare company uses a multi-agent system on Amazon Bedrock AgentCore. The system uses multiple FMs to process 2,000 medical report documents daily. The documents range from 5 to 50 pages each. The company discovers that the system is not performing complete analysis on documents that exceed 30 pages. Documents over 30 pages miss critical information from later sections. The results are truncated, but there are no explicit errors. The company must resolve this issue while maintaining response times under 10 seconds. The company must keep processing costs low.\n"
                    "Which solution will meet these requirements?",
        "options": [
            "A. Use Amazon CloudWatch Logs Insights queries to analyze Amazon Bedrock agent processing times. Increase the timeout settings for the Lambda functions that host the agents. Implement pagination for larger documents to process in sequential batches.",
            "B. Implement document chunking with semantic overlap between chunks where content from the end of one chunk appears at the beginning of the next chunk. Configure Amazon CloudWatch metrics to monitor InputTokenCount. Set up a CloudWatch dashboard for context utilization percentage. Configure diagnostic logging that identifies truncation points in the processing flow.",
            "C. Configure agent action groups to process documents sequentially by automatically creating separate tasks for each document section. Set up an AWS Step Functions workflow to coordinate processing. Combine the results from individual sections.",
            "D. Deploy the system in a higher memory configuration with a larger compute instance size to accommodate complete documents in memory. Add Amazon Comprehend Medical to identify and prioritize critical medical entities for improved context management.",
        ],
        "answer": "B. Implement document chunking with semantic overlap between chunks where content from the end of one chunk appears at the beginning of the next chunk. Configure Amazon CloudWatch metrics to monitor InputTokenCount. Set up a CloudWatch dashboard for context utilization percentage. Configure diagnostic logging that identifies truncation points in the processing flow.",
        "explanation": "Silent truncation of long inputs with **no errors** is a **context-window overflow** (exam-guide Skill 5.2.1), not a compute or timeout problem. The fix is to **chunk** the documents with **overlap** so no content is dropped at boundaries, and to **instrument** the cause: `InputTokenCount` metrics, a context-utilisation dashboard and logs that show where truncation happens.\n\n"
                       "**A** raising timeouts and paginating sequentially slows responses past the 10-second target. **C** sequential per-section tasks add latency and cost. **D** more memory doesn't enlarge the model's context window.",
        "reference": f"{_BR}/kb-chunking.html",
        "note": "Answer agrees with the second dump's key (B). Moderate-high confidence.",
    },
    {
        "id": 149, "category": D1, "task": "1.6", "type": "multi",
        "question": "A financial services company is using Amazon Bedrock to deploy a GenAI application across multiple business units. The company must ensure that all prompts that are used with the application's FMs follow regulatory compliance standards and maintain consistent formatting. The company must implement a solution that provides version control for prompt templates, requires approval workflows for new prompts, and maintains detailed audit trails of all prompt usage and modifications.\n"
                    "Which combination of solutions will meet these requirements? (Select TWO.)",
        "options": [
            "A. Use Amazon Bedrock Prompt Management to create parameterized prompt templates and enable version control. Configure approval workflows that require approvals from the company's regulatory compliance team before deploying new prompts to production environments.",
            "B. Store all prompt templates in Amazon S3 buckets. Enable versioning on the buckets. Use AWS Lambda functions and Amazon SNS to send approval requests to regulatory compliance reviewers through email notifications.",
            "C. Configure AWS CloudTrail to log all Amazon Bedrock API calls and prompt interactions. Use Amazon CloudWatch Logs to capture detailed access patterns and prompt usage metrics to generate compliance reports.",
            "D. Use AWS Systems Manager Parameter Store to manage prompt templates as secure strings. Use AWS Step Functions to orchestrate a multi-stage approval workflow that has automatic rollback capabilities.",
            "E. Use Amazon API Gateway and AWS WAF rules to filter prompt requests. Use Amazon DynamoDB to store approval status and audit information for all prompt template modifications.",
        ],
        "answer": [
            "A. Use Amazon Bedrock Prompt Management to create parameterized prompt templates and enable version control. Configure approval workflows that require approvals from the company's regulatory compliance team before deploying new prompts to production environments.",
            "C. Configure AWS CloudTrail to log all Amazon Bedrock API calls and prompt interactions. Use Amazon CloudWatch Logs to capture detailed access patterns and prompt usage metrics to generate compliance reports.",
        ],
        "explanation": "This is exam-guide Skill 1.6.3 (prompt governance): **Bedrock Prompt Management** provides **parameterized templates, versions** and a gate before a version is used in production (A), while **CloudTrail** (API activity, including who created or changed prompts) plus **CloudWatch Logs** supply the **audit trail** and usage reporting (C).\n\n"
                       "**B, D, E** rebuild versioning and approvals by hand from S3, Parameter Store, Step Functions or DynamoDB, and the WAF filtering in E does nothing for prompt governance. Compare Q9, which has the same single-answer pattern.",
        "reference": f"{_BR}/prompt-management.html",
        "note": "Answer agrees with the second dump's key (A + C). High confidence.",
    },
]
