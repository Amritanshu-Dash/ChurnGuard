# ChurnGuard

**Customer Churn Prediction System**

A complete end-to-end Machine Learning project to predict which bank customers are likely to churn (leave the bank).

## Project Overview

This project demonstrates a full production-grade ML pipeline including:
- Data Analysis & Visualization
- Feature Engineering
- Model Training & Experiment Tracking
- REST API Development
- Docker Containerization

## Tech Stack

- **Programming Language**: Python
- **ML Libraries**: Pandas, Scikit-learn, XGBoost
- **Experiment Tracking**: MLflow
- **API Framework**: FastAPI
- **Containerization**: Docker

## How to Run the Project

### Option 1: Using Docker (Recommended)

```bash
# Build the Docker image
docker build -t churnguard .

# Run the container
docker run -p 8000:8000 churnguard