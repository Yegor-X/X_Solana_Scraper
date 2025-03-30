# X (Twitter) Web Scraper

Simple Python scripts that extract recent (within the last 7 days) news or posts about Solana from X (formerly Twitter) and analyze their relevance using a locally hosted large language model (Deepseek-R1).

## Setup

### 1. Install Ollama (if not already installed)
- Go to [Ollama](https://ollama.com/) and click the download button.
- After downloading, open the terminal and input:
```bash
ollama   # Check general info
ollama pull deepseek-r1
```
- For more details, visit: [Ollama GitHub](https://github.com/ollama/ollama)

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your X (Twitter) Credentials
Since X (Twitter) requires login credentials to access content, enter your details in the `config.ini` file:
```ini
[X]
username = @your_username
password = your_password
email = your_email@example.com
```
**Important:** If your account is banned, create a new one and update `config.ini` accordingly.

### 5. Run `save_cookies.py`
If you have just entered new credentials (Step 4), run the following script to store cookies and keep the main script running longer:
```bash
python save_cookies.py
```
After running this script, a `cookies.json` file will be created. **Do not delete `cookies.json`.**

### 5.1 Enable Full Scraping (Optional)
By default, the script analyzes ~12-15 recent posts. If you want to collect **all** relevant posts, modify `scraper.py`:
- Locate **line 62**:
```python
while tweet_count < MINIMUM_TWEETS:
```
- Replace it with:
```python
while True:
```
**Warning:** Full scraping requires **significant time, computing power, and memory**, as there are **millions** of tweets related to Solana.

### 6. Run the Main Script
```bash
python scraper.py
```
Grab a cup of tea and enjoy watching progress in your terminal! 🚀

## Result
After execution, the script generates `data_with_llm_analytics.csv`, which contains relevant information for each post, including **basic analytics from Deepseek-R1 LLM**.

