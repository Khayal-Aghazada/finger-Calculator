# 🖐️ Finger Math Calculator 🧠➕

A gesture-based calculator using **OpenCV**, **MediaPipe**, and **Python** — do math with just your hands!  
Show numbers with your fingers, choose an operation, and get results — no keyboard needed.

---

## ✨ Features

- 🧮 Detects numbers **1–10** using **both hands**
- ➕➖✖️➗ Supports basic operations: `+`, `-`, `*`, `/`
- 👍 Thumbs-up gesture to calculate (`=`)
- ✊ Fist gesture to **restart**
- ⏱️ All gestures require a **2-second hold** for accuracy

---

## 🛠️ Tech Stack

- **Python 3**
- **OpenCV** — for webcam and image processing
- **MediaPipe** — for real-time hand and finger tracking

---

## 🧩 How It Works

1. Show a number (e.g. `3 fingers`) for 2 seconds ➝ System saves **first number**
2. Show operation:
   - `1` → `+`
   - `2` → `-`
   - `3` → `*`
   - `4` → `/`
3. Show second number (e.g. `5 fingers`) for 2 seconds ➝ System saves **second number**
4. Show 👍 (thumbs up) ➝ System calculates and displays the result
5. Show ✊ (fist = 0 fingers) for 2 seconds ➝ System **resets**

---

## 🚀 Getting Started

### 🔧 Requirements

```bash
pip install -r requirements.txt
