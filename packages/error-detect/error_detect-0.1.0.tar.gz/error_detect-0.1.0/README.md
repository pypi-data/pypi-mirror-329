# 🌟 ErrorDetect: AI-Powered Python Error Fixing

[![PyPI version](https://img.shields.io/pypi/v/error_detect.svg)](https://pypi.org/project/error_detect/)
[![Python version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**ErrorDetect** is a Python package that **automatically captures, analyzes, and fixes errors** using a Large Language Model (LLM). It integrates with Ollama LLM APIs to return **only the corrected line of code** for detected errors.

---

## 🚀 Features

✅ **Automatic Error Capture** – Detects exceptions and captures error details.  
✅ **AI-Powered Fixes** – Uses LLMs (like Llama3) to generate **corrected lines of code**.  
✅ **Traceback Extraction** – Captures the **exact line of code** causing the error.  
✅ **Flexible Integration** – Works with or without LLM integration.  

---

## 👥 Installation

You can install `error_detect` directly from PyPI:

```bash
pip install error_detect
```

Or install it from source:

```bash
git clone https://github.com/Rhul27/error_detect.git
cd error_detect
pip install .
```

---

## 🛠️ Usage

### **1️⃣ Basic Usage (Without LLM Integration)**
You can use `ErrorDetect` to capture and display error details:

```python
from error_detect import ErrorDetect

client = ErrorDetect()

try:
    a = 1 / 0
except Exception:
    print(client.error_detect())
```

**Output:**
```
Type: ZeroDivisionError
Line: 10
Error: division by zero
```

---

### **2️⃣ Using an LLM to Automatically Fix Errors**
If you have an Ollama-compatible API running, you can **connect to an AI model** to fix errors automatically:

```python
from error_detect import ErrorDetect

client = ErrorDetect("http://localhost:11434", "llama3.2")

try:
    a = 1 / 0
except Exception:
    output = client.get_error_solution()
    print(output)
```

**Example Output:**
```
Type: ZeroDivisionError
Line: 12
Error: division by zero
Solution : "a = 1.0 / (0.0001)  # Avoid division by zero"
```

---

### **3️⃣ Handling Missing Dictionary Keys (KeyError Example)**

```python
try:
    data = {"name": "Alice"}
    print(data["age"])  # This key does not exist
except Exception:
    output = client.get_error_solution()
    print(output)
```

**Output:**
```
Type: KeyError
Line: 15
Error: 'age'
Solution : "age = data.get('age', 25)  # Provide a default value"
```

---

## ⚙️ **API Reference**

### `ErrorDetect(ollama_url=None, model_name=None)`

**Parameters:**
- `ollama_url` *(str, optional)* – The base URL of the Ollama LLM server.
- `model_name` *(str, optional)* – The name of the LLM model to use.

---

### `error_detect()`

**Returns:**  
Returns a string containing error details:
```
Type: <ExceptionType>
Line: <LineNumber>
Error: <ErrorMessage>
```

---

### `get_error_solution(error_message=None, error_line=None)`

**Automatically detects errors and gets the corrected code line using LLM.**  

**Returns:**  
Formatted output with both the **error details** and the **solution**:
```
Type: <ExceptionType>
Line: <LineNumber>
Error: <ErrorMessage>
Error line : <ErrorLine>
Solution : "<Corrected Line of Code>"
```

If **LLM is not integrated**, returns:
```
LLM integration not configured.
```

---

## 🌍 **Environment Setup**
To use the AI-powered error detection, ensure you have an **Ollama LLM server** running locally:

```bash
ollama serve
```

You can check available models via:

```bash
curl http://localhost:11434/api/tags
```

---

## 🛠️ **Troubleshooting**

**Problem:** I get `LLM integration not configured.`  
👉 **Solution:** Pass a valid `ollama_url` and `model_name` when initializing `ErrorDetect`.

**Problem:** LLM does not return a proper fix.  
👉 **Solution:** Try a different model like `"codellama"` for better code-specific fixes.

---

## 🤝 **Contributing**

We welcome contributions! Follow these steps to contribute:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Added new feature"`).
4. Push to your fork (`git push origin feature-branch`).
5. Open a **Pull Request**.

---

## 📃 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 📞 Contact

📧 Email: 27rg2000@gmail.com 
🔗 GitHub: [Rhul27/error_detect](https://github.com/Rhul27/error_detect)  
```

