### Deepkeep API Quickstart - Python

Welcome to the official repository for quick start applications utilizing the Deepkeep's SDK. Our SDK is designed to streamline interactions with ML models like LLMs and Object detection, providing an intuitive Python interface for managing models, datasets, users, and processing pipelines to provied ML security security and trust assessments or provied a firewall for ML Models incrissing trust and security rubustness.
This repository is your starting point to dive into leveraging our advanced AI and machine learning trust and security capabilities across various endpoints, including model management, user authentication, conversational AI, and customized content moderation pipelines.




## Basic request

To send your first API request with the Deepkeep Python SDK, make sure you have the right dependencies installed and then run the following code:

```python
host_id = "DEEPKEEP_HOST_ID"
access_key = "DEEPKEEP_ACCESS_KEY"
secret_key = "DEEPKEEP_SECRET_KEY"
base_url = "DEEPKEEP_BASE_URL"

user_id = access_key
dk_client = Deepkeep(access_key=access_key, secret_key=secret_key, base_url=base_url)

# Create a new conversaion
conversation_id = dk_client.conversation.create(user_id=user_id, host_id=host_id)["id"]

# Convers with the assistant
content = "<MESSAGE>"
assistant_response = dk_client.message.create(host_id=host_id, conversation_id=conversation_id, content=content)
print(assistant_response["content"])

# Converse Debug Mode
content = "<MESSAGE>"
assistant_response = dk_client.message.create(monitor=host_id, conversation_id=conversation_id, content=content, verbose=True)
print(assistant_response["content"])
print(assistant_response["statistics"])

# Note: another optional way to create Deepkeep client is using a token instead of access_key and secret_key
# client = Deepkeep(token="<Access Token>", base_url=base_url)
```

## Setup

1. If you don't have Python installed, install it [from Python.org](https://pypi.org/project/deepkeep/).

2. [Clone](https://github.com/Deepkeepai/deepkeep-quickstart-python) this repository.

3. Navigate into the project directory:

   ```bash
   $ cd deepkeep-quickstart-python
   ```

4. Create a new virtual environment:

   - macOS:

     ```bash
     $ python -m venv venv
     $ . venv/bin/activate
     ```

   - Windows:
     ```cmd
     > python -m venv venv
     > .\venv\Scripts\activate
     ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Run the notebooks:

Install JupyterLab with pip:
```bash
pip install jupyterlab
```

Once installed, launch JupyterLab with:
```bash
jupyter lab
```

You should now be able to access the notebooks from your browser at the following URL: [http://localhost:8888/lab](http://localhost:8888/lab)!