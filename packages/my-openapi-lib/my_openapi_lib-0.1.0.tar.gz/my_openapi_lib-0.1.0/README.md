# discovery-scs

## FastAPI-Ecommerce-API with OpenAPI Spec Generation

This repository contains the FastAPI-based E-commerce API, extended with a script to generate an OpenAPI specification using the `openapi-specgen` library.

---

## **Features**
- Listens for GitHub webhook events for pull requests.
- Dynamically clones or updates the repository to a specified folder.
- Runs a pipeline (`main.py`) to analyze the repository and generate an OpenAPI spec.

---

## **Project Structure**
```
discovery-scs/
├── main.py                 # Pipeline script for OpenAPI generation
├── webhook_listener.py     # Webhook Listener for handling PR events
├── repo_to_scan/           # Folder where repositories are cloned
├── openapi_spec.json       # Generated OpenAPI specification
└── README.md               # Setup guide and documentation
```

---

## **Setup Instructions**

### **1. Prerequisites**
- **Python**: Installed with Conda or a similar package manager.
- **Git**: Installed and available in the system PATH.
- **ngrok**: For local webhook testing.
- **GitHub Repository Access**: To set up webhooks.

---

### **2. Clone This Repository**

Clone this repository and navigate to the project directory:
```bash
# Clone the repository
git clone https://github.com/tope-ai/discovery-scs.git

# Navigate to the project directory
cd discovery-scs
pip install my_openapi_lib

```
4.  Update the folder_to_scan variable in main.py with your project path:
   ```bash
   folder_to_scan = r"C:\your\path\to\discovery-scs\FastAPI-Ecommerce-API-main"

   ```

## Generate OpenAPI Spec
Run the main script:
  ```bash
python main.py
```

The script will:

Scan the FastAPI-Ecommerce-API folder
Find important Python files
Generate OpenAPI specification
Save it as openapi_spec.json
Project Structure
spec_gen_19.1/
└── discovery-scs/
    ├── FastAPI-Ecommerce-API-main/
    ├── openapi-specgen-master/
    ├── main.py
    └── README.md



## Validate the Spec

- Open the `openapi_ecommerce_specgen.json` file in [Swagger Editor](https://editor.swagger.io/) to validate and explore the API.
