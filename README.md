# FinTech Investment Recommendation System

## Project Introduction
This repository provides a solution for recommending domains of investment to a user based on their demographics, investment history, and goals. It makes use of machine learning and a well-formed API with custom recommendations.

---

## Project Overview

### Goal
The goal of this project is to eliminate investment decision-making delays by giving users personalized investment recommendations.

### Working
For operation, this scheme makes use of:
1. **Machine Learning Model:** A pre-trained model called `projetML.pkl` predicts the recommendations on the basis of the input from users.
2. **API:** The FastAPI application takes care of fetching user data and fetching recommendations through a RESTful API.

### Use Case Scenario
A user wants to start investing in different assets but does not know where to begin. The user provides inputs such as age, income, and goals through the API, which returns investment domain recommendations such as Cryptocurrencies or Real Estate.

### Features
- Uses a dataset found on Kaggle for testing and training.
- Involves machine learning predictive analytics.
- RESTful API that enables web and mobile applications with relative ease.
- Additions of investment domains or fine-tuning recommendations can be performed with relative ease.

---

## Technologies & Tools

### Languages
- Python: For data processing, machine learning, and API development.

### Libraries & Frameworks
- **FastAPI:** Used to create a RESTful API as the back-end in the application architecture.
- **Pandas, NumPy:** Used for data manipulation and processing.
- **scikit-learn:** Used for training the machine learning model and prediction once trained.

### Tools
- **Pickle:** Used to save and load the ML model.
- **Postman:** Used to test API endpoints.
- **GitHub:** Used for version control and collaboration.

---

## File Structure

1. **`Micro.py`:** The backend based on FastAPI, capable of loading the ML model and serving predictions.
2. **`projetML.pkl`:** A serialized machine-learning model that predicts investment domains.
3. **`enhanced_investment_data1.csv`:** A dataset found on Kaggle used for model training and validation.

---

### Prerequisite
- You must have Python 3.8 or a higher version.
- Install the required packages: `pip install -r requirements.txt`.

### Running the Project
1. Clone this repository.
2. Install its dependencies.
3. Run the `Micro.py` script to start the API server.
4. Type in a terminal window: `uvicorn Micro:app --reload` to run the API.
5. To test out the API, make a POST request to `/predict/`.
