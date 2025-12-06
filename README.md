# BPMN Real-Time Collaboration Challenge

Welcome to the SUMM AI take-home assignment.

Your task: build a **minimal, real-time collaborative BPMN diagram editor**.

---

## 🧩 Core Features

- Render BPMN diagrams in the browser using **bpmn.io** (`bpmn-js`).
- Edit the diagram - changes should appear live for all connected users.
- Show a simple “online users” indicator.
- Store the current BPMN diagram in memory (no need for a DB).

**Bonus:** show a lock/marker when another user is editing a BPMN element.

---

## 🛠️ Notes

- Use any frontend framework (React, Vue, etc.).
- Backend would be preferrably in FastAPI (Python) but you can use any other backend framework you're comfortable with.
- No authentication is required.
- Keep it simple.

---

## 🚀 Submission

You have one week from the date of receiving the assignment to submit your solution.
For submission, please send a mail to Nicholas (you should have his email from the interview invitation).

Please include the following:
- A public GitHub repo link or invite me to a private repo (@flowni).
- A concise README on how to run it.
- (Optional) A short Loom/video demo.

---

## 🧭 What We’re Looking For

- Clean, modular code.
- Working real-time sync.
- Clear, minimal UX.
- Bonus creativity or nice touches.

---

Have fun - and all the best from SUMM AI!

## 📦 Installation

### Prerequisites
- **Python 3.11+** (for backend)
- **Node.js 18+** and **npm** (for frontend)
- **UV** (Python package manager - recommended) or **pip**

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies using pip:**
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## 🚀 Running the Application

### Start Backend Server

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Run the FastAPI server:**
   ```bash
   fastapi run
   ```
   
   The backend server will start at: `http://127.0.0.1:8000`

### Start Frontend Application

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Start the React development server:**
   ```bash
   npm start
   ```
   
   The frontend application will start at: `http://localhost:3000`

### Access the Application

- Open your web browser and go to: `http://localhost:3000`
- The BPMN editor will load with real-time collaboration features
- Open multiple browser tabs/windows to test real-time collaboration

## 🔧 API Endpoints

- automatic API documentation at `http://127.0.0.1:8000/docs`
