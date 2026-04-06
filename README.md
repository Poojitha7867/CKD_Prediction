# Chronic Kidney Disease Prediction System

## Project Overview

This project is a full-stack web application developed using **Machine Learning and Django** to predict the stage of Chronic Kidney Disease (CKD).

The system allows users to input clinical data and predicts whether the patient is:

* Healthy Kidney
* Mild CKD
* Moderate CKD
* Severe CKD

---

## Features

* User-friendly login system with OTP
* CKD prediction using Machine Learning models
* Comparison of multiple algorithms:

  * Decision Tree
  * Random Forest
  * Logistic Regression
* Displays:

  * Prediction results
  * Accuracy of each model
  * Best performing model
* Clean and responsive UI

---

## 🧠 Machine Learning Models Used

* Decision Tree Classifier
* Random Forest Classifier
* Logistic Regression

---

## Dataset

The model is trained on a clinical dataset containing:

* Age, BMI, Blood Pressure
* Sodium, Potassium, Hemoglobin
* Diabetes, Hypertension, Smoking Status
* And other medical features

---

## Tech Stack

* **Frontend:** HTML, CSS
* **Backend:** Django (Python)
* **Machine Learning:** Scikit-learn, Pandas, NumPy

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Create virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the server:

```bash
python manage.py runserver
```

---

## Output

* Predicts CKD stage
* Shows accuracy of all models
* Displays best model based on accuracy

---

## Future Improvements

* Add real-time OTP via email
* Deploy on cloud (Render / AWS)
* Add patient report download (PDF)
* Improve model accuracy

---

## If you like this project, give it a star!
