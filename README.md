📂 Classifier Agent
The Classifier Agent is a modular AI-powered Flask-based system designed to classify various document formats (PDFs, JSON, emails) by intent (e.g., Complaint, RFQ, Invoice, Regulation, Fraud Risk) and optionally analyze tone. It uses both rule-based logic and a transformer-based zero-shot classifier (facebook/bart-large-mnli).

📌 Features
✅ Uploads and classifies files (PDF, JSON, Email)

✅ Detects document format via MIME types

✅ Uses keyword-based rule classification

✅ Optionally performs zero-shot classification (requires internet)

✅ Routes tasks to the appropriate agent

✅ Detects tone from textual content

✅ Stores memory logs for future context

🧠 Architecture
ASCII Overview
pgsql
Copy
Edit
+------------+         +-----------------+          +------------------+
|  Upload UI | ----->  | route_input()   |  ----->  | classify_input() |
+------------+         +-----------------+          +--------+---------+
                                                             |
                                                             v
                                                 +------------------------+
                                                 | Format Detection Logic |
                                                 +-----------+------------+
                                                             |
                          +----------+-----------+-----------+-----------+
                          |          |           |           |           |
                          v          v           v           v           v
                       PDF Agent  Email Agent  JSON Agent  Tone Agent  Memory Logger
Mermaid (for GitHub render)
<details> <summary>Mermaid Diagram</summary>
mermaid
Copy
Edit
graph TD
    A[File Upload] --> B(route_input)
    B --> C{detect_format}
    C --> D[PDF Agent]
    C --> E[Email Agent]
    C --> F[JSON Agent]
    B --> G[classify_input]
    G --> H{Keyword Match}
    H --> I[RFQ/Invoice/Complaint/etc.]
    B --> J[detect_tone]
    B --> K[write_to_memory]
</details>
🛠️ Setup Instructions
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/your-username/classifier-agent.git
cd classifier-agent
2. Create a virtual environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # On Windows
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
📌 You need internet access to download the transformer model the first time.

4. Run the app
bash
Copy
Edit
python main.py
Visit http://127.0.0.1:5000

📤 Upload Flow
User uploads a file via the UI.

route_input(filepath) is called.

Format is detected.

Content is extracted (text for PDFs using PyMuPDF).

Intent is classified (rule-based or transformer).

Tone is optionally detected.

Results are routed to the relevant agent.

Logged into memory.

🧩 Modules
Module	Purpose
classifier_module	Classifies intent using keyword rules or zero-shot model
tone_agent	Analyzes text to detect tone using simple sentiment logic
memory_store	Logs classification result and metadata
main.py	Flask app handling upload and routing

🔍 Sample Classification Rules
Keyword(s)	Classified As
invoice	Invoice
complain, disappointed	Complaint
gdpr, fda	Regulation
fraud	Fraud Risk
quote, price	RFQ

🧪 Testing
Test files are provided in the /test_files/ folder. You can upload .pdf, .json, or .eml (email) files to see how classification and routing behaves.

📝 Notes
For PDFs, make sure PyMuPDF (fitz) is installed.

If offline, avoid initializing HuggingFace model on the fly.

You can expand tone detection by integrating sentiment models (e.g., Vader or transformers).

