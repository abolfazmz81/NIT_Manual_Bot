# NIT Manual Chatbot

A specialized chatbot designed to assist **Noshirvani University of Technology (NIT) students** by providing fast and accurate access to university regulations, manuals, and relevant student guidelines.

## 📌 Project Overview

The **NIT Manual Bot** is a chatbot that helps students quickly find information from the university's official manual and other academic resources. It leverages **ChatGPT**, **Elasticsearch**, and **LangChain** to efficiently search and retrieve relevant sections from PDFs and structured documents.

## 🚀 Features

- **Intelligent Search:** Uses **Elasticsearch** and **ChatGPT API** to quickly find relevant sections from the NIT manual.
- **Text Extraction & Processing:** Extracts content from **PDF files** and processes them for structured search.
- **Dynamic Interaction:** Engages with users in a conversational manner to refine queries and provide accurate responses.
- **Multi-Layered Query Processing:** Utilizes **prompt engineering** and **AI-based refinement** for more relevant answers.
- **Integration with Telegram:** Provides a **Telegram chatbot** for direct interaction with students.
- **Custom Query Handling:** Supports **natural language queries** and extracts relevant information from **university regulations**.

## 🛠️ Tech Stack

The project is built using the following technologies:

- **Python** – Core programming language
- **Elasticsearch** – Efficient text indexing and retrieval
- **LangChain** – Orchestrating LLM-based responses
- **ChatGPT API** – AI-powered responses and text analysis
- **Python-Telegram-Bot** – Integration with **Telegram**
- **Docker** – Containerized deployment for easy scalability
- **Regex & NLP Libraries** – For text processing and query refinement

## 📂 Installation

To set up the **NIT Manual Bot** locally, follow these steps:

### **1️⃣ Clone the Repository**
  ```bash
  git clone https://github.com/abolfazmz81/NIT_Manual_Bot.git
  cd NIT_Manual_Bot
  ```

### 2️⃣ Install Dependencies
  Ensure you have Python installed, then install required packages:
  ```bash
  pip install -r requirements.txt
  ```

### 3️⃣ Set Up Configuration
- **Elasticsearch**: Run an instance of Elasticsearch (via Docker or local install).
- **API Keys**: Add your ChatGPT API key and other necessary credentials in a config.
- **Telegram Bot Token**: Obtain a token via **BotFather** and update the configuration.

### 4️⃣ Run the Chatbot
```bash
python bot.py
```
**Note**: You can also use **Docker Compose** to load **Elasticsearch** without any issues.

## 🏆 Usage
Once the bot is running, you can interact with it via **Telegram**. Simply start a conversation and ask questions about NIT regulations, academic guidelines, or specific rules.

**Example Queries**:
- "What are the graduation requirements?"
- "How many credits do I need to complete my degree?"
- "What is the university's attendance policy?"
**Note**: Questions must be asked in **Persian**, as **Persian** is the official language of **Noshirvani University of Technology (NIT)**.

## 🔧 Deployment with Docker
To deploy using Docker:
```bash
docker-compose up --build
```

This sets up **Elasticsearch** and **Kibana** in a scalable environment. it also includes **Weaviate** and **Playground** for future features.

## 📜 License
This project is licensed under the [**MIT License**](./LICENSE)
