# Revenue Forecast Tester AI Agent

An interactive Streamlit application for testing and validating revenue forecasts with AI-powered analysis and visualization tools.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Features

### 📁 Data Upload
- Upload CSV or Excel files
- Automatic data preview and statistics
- Column type detection

### 🤖 AI Chat
- Ask questions about your revenue data
- Get insights on trends, averages, outliers
- Forecast recommendations

### 📈 Chart Bot
- Interactive chart builder (Line, Bar, Area, Scatter)
- Multiple Y-axis support
- Export charts as PNG

### 🧪 Forecast Testing
- Calculate accuracy metrics (MAPE, MAE, RMSE)
- Detect anomalies and outliers
- Residual analysis visualization

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## Expected Data Format

For forecast testing, your data should include:
- Date/Period column
- Actual Revenue column
- Predicted/Forecast column (optional)

Example CSV:
```csv
Date,Revenue,Forecast
2024-01,10000,9500
2024-02,12000,11500
2024-03,11500,12000
```

## Deploy to GitHub

1. Push this project to a GitHub repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy with `app.py` as the main file

## Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib

## License

MIT
