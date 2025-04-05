# Vote Compass

Vote Compass is a web application that helps users discover their political alignment by comparing their answers on political issues with the stances of different political parties. Built with FastAPI, this tool processes user responses and maps them across ideological dimensions using customizable data.

---

## 🌐 Features

- 🧠 Opinion-to-party match system
- 📊 Ideological dimension scoring
- 📁 Dynamic data loading from JSON (questions, parties, etc.)
- ⚙️ Simple and extensible FastAPI backend
- ✅ Unit-tested matching algorithm

---

## 🏗️ Project Structure

```
vote_compass/
│
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── models/schemas.py    # Pydantic schemas
│   ├── services/matcher.py  # Core matching logic
│   ├── data/                # Static data (questions, parties, etc.)
│   └── utils/helpers.py     # Helper functions (loaders, etc.)
│
├── tests/test_matcher.py    # Unit tests
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/vote-compass.git
cd vote-compass
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

### 4. Access the API docs

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

---

## 📦 JSON Data Format

- `questions.json`: List of statements users respond to
- `parties.json`: Positions of political parties
- `dimensions.json`: Definitions of ideological axes
- `sources.json`: Reference sources for positions

---

## ✅ Testing

Run tests with:

```bash
pytest tests/
```

---

## 📌 Future Improvements

- Frontend with React or Vue
- Admin UI to manage questions and party data
- Advanced scoring algorithm with weights and confidence levels
- User authentication and result history

---

## 📄 License

MIT License. See `LICENSE` for details.
