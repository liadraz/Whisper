# Whisper-bot

**Whisper** is a smart chatbot that helps users find and compare laptop and book products in real time. It listens to natural language queries, scrapes live product data from the web, and responds with relevant options — quietly doing the heavy lifting for you.

---

## ✨ Features

- 💬 Conversational interface via Dialogflow  
- 🔍 Real-time web scraping based on user input  
- 📚 Book genre and price-based filtering  
- 💻 Laptop model and brand comparison (coming soon)  
- ⚡ Fast, lightweight backend built with FastAPI  
- 🧠 Intent recognition with webhook and parameters  
- 🐳 Ready for Docker deployment  
- 🌐 Local development supported via **ngrok**

---

## 🛠️ Tech Stack

| Layer         | Tool                      |
|---------------|---------------------------|
| Language      | Python                    |
| Web Framework | FastAPI                   |
| Scraping      | HTTPX + BeautifulSoup     |
| Chatbot       | Dialogflow                |
| Tunneling     | Ngrok (for local webhook) |
| Deployment    | Docker                    |

---

## 🚀 How to Use

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/liadraz/Whisper.git
cd whisper
````

---

### ⚙️ 2. Choose How to Run

#### 🔧 Option A: Run Locally

1. **Set up virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Start FastAPI server:**

```bash
uvicorn main:app --reload
```

3. **Expose local server to Dialogflow using ngrok:**

```bash
ngrok http 8000
```

4. **Copy the HTTPS URL from ngrok** and use it in Dialogflow Webhook config
   (e.g. `https://abcd1234.ngrok.io/webhook/`)

---

#### 🐳 Option B: Run via Docker

1. **Build Docker image:**

```bash
docker build -t whisper-bot .
```

2. **Run container:**

```bash
docker run -p 8000:8000 whisper-bot
```

3. **Expose it with ngrok:**

```bash
ngrok http 8000
```

> 🔗 You still need ngrok unless your container is deployed to a public server.

---

### 🤖 3. Dialogflow Setup

1. **Create Intents:**

* `SearchBooks`: expects `genre` (optional), `price_limit` (optional)
* `SearchLaptops`: expects `brand`, `model`, or `price` (optional)

2. **Webhook Configuration:**

* Go to **Fulfillment** tab → Enable webhook
* Set URL to: `https://your-ngrok-or-cloud-url/webhook/`
* Click **Save**

3. **Example Training Phrases:**

For books:

* “Find me fantasy books under 30 dollars”
* “Show me science books”
* “What are the cheapest books?”

For laptops (planned):

* “Find laptops under 3000 NIS”
* “Compare Dell vs Asus”
* “Show me laptops with 16GB RAM”

---

## 📦 API Example (Dialogflow Payload)

```json
{
  "queryResult": {
    "intent": {
      "displayName": "SearchBooks"
    },
    "parameters": {
      "genre": "fiction",
      "price_limit": "20"
    }
  }
}
```

---

### 📋 Sample Response

```
Here are some books for you:
1. The Time Machine - $18.00 - https://books.toscrape.com/...
2. 1984 - $16.50 - https://books.toscrape.com/...
```

---

## 🧪 Testing (Optional)

To test locally:

```bash
pytest run_tests.py
```

Tests are written for:

* Fetching book pages
* Scraping book info
* URL building and genre mapping
