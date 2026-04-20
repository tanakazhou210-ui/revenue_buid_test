import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

st.set_page_config(page_title="Revenue Forecast Tester", page_icon="📊", layout="wide")

COLORS = ["#10B981", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6"]


def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "uploaded_data" not in st.session_state:
        st.session_state.uploaded_data = None


def analyze_data(df):
    insights = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i + 1 :]:
                corr = corr_matrix.loc[col1, col2]
                if abs(corr) > 0.7:
                    insights.append(
                        f"Strong correlation between {col1} and {col2}: {corr:.2f}"
                    )

    for col in numeric_cols:
        insights.append(f"{col}: mean={df[col].mean():.2f}, std={df[col].std():.2f}")

    return insights


def generate_ai_response(df, question):
    question_lower = question.lower()
    insights = analyze_data(df)

    if "trend" in question_lower:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            trend = "upward" if df[col].iloc[-1] > df[col].iloc[0] else "downward"
            return f"The {col} shows an {trend} trend. Starting at {df[col].iloc[0]:.2f} and ending at {df[col].iloc[-1]:.2f}."

    if "average" in question_lower or "mean" in question_lower:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        results = []
        for col in numeric_cols:
            results.append(f"{col}: {df[col].mean():.2f}")
        return "Average values:\n" + "\n".join(results)

    if "forecast" in question_lower or "predict" in question_lower:
        return (
            "For forecasting, I recommend using the Chart Bot to visualize trends and applying time-series models. Key columns detected: "
            + ", ".join(df.columns.tolist())
        )

    if "outlier" in question_lower or "anomaly" in question_lower:
        outliers = []
        for col in df.select_dtypes(include=[np.number]).columns:
            mean, std = df[col].mean(), df[col].std()
            outlier_count = ((df[col] - mean).abs() > 2 * std).sum()
            if outlier_count > 0:
                outliers.append(f"{col}: {outlier_count} outliers detected")
        return "Outlier Analysis:\n" + (
            "\n".join(outliers) if outliers else "No significant outliers detected."
        )

    if "total" in question_lower or "sum" in question_lower:
        results = []
        for col in df.select_dtypes(include=[np.number]).columns:
            results.append(f"{col}: {df[col].sum():.2f}")
        return "Total values:\n" + "\n".join(results)

    return "Here are the key insights from your data:\n" + "\n".join(insights[:5])


def generate_forecast_recommendations(actual, predicted, metrics):
    recommendations = []

    mape = metrics["MAPE"]

    if mape < 10:
        recommendations.append(
            "✅ Excellent forecast accuracy (MAPE < 10%). Your model is performing very well."
        )
    elif mape < 20:
        recommendations.append(
            "✅ Good forecast accuracy (MAPE < 20%). Consider fine-tuning for better results."
        )
    elif mape < 30:
        recommendations.append(
            "⚠️ Moderate forecast accuracy (MAPE < 30%). Review data quality and consider feature engineering."
        )
    else:
        recommendations.append(
            "❌ Poor forecast accuracy (MAPE > 30%). Consider using additional variables or alternative models."
        )

    residuals = np.array(actual) - np.array(predicted)
    mean_res = np.mean(residuals)

    if mean_res > 0:
        recommendations.append(
            "📈 The model consistently under-forecasts. Consider adding a bias correction factor."
        )
    elif mean_res < 0:
        recommendations.append(
            "📉 The model consistently over-forecasts. Consider adjusting the baseline."
        )

    std_res = np.std(residuals)
    if std_res > np.std(actual) * 0.2:
        recommendations.append(
            "⚠️ High variance in residuals. The model may be unstable for some periods."
        )

    positive_residuals = np.sum(residuals > 0)
    negative_residuals = np.sum(residuals < 0)

    if positive_residuals > negative_residuals * 1.5:
        recommendations.append(
            "📊 More under-forecasts detected. Revenue tends to be higher than predicted."
        )
    elif negative_residuals > positive_residuals * 1.5:
        recommendations.append(
            "📊 More over-forecasts detected. Revenue tends to be lower than predicted."
        )

    trend_col = None
    for col in [actual.name, predicted.name]:
        if col and "revenue" in col.lower():
            trend_col = col

    recommendations.append("\n📋 Recommendations:")
    recommendations.append(
        "1. Use the Chart Bot to visualize actual vs predicted trends"
    )
    recommendations.append("2. Consider adding seasonal adjustments to your model")
    recommendations.append("3. Review periods with largest residuals for insights")
    recommendations.append(
        "4. Test alternative forecasting methods (moving average, exponential smoothing)"
    )

    return "\n".join(recommendations)


def calculate_metrics(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)

    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    mae = np.mean(np.abs(actual - predicted))
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))

    return {"MAPE": mape, "MAE": mae, "RMSE": rmse}


def create_chart(df, chart_type, x_col, y_cols):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#1E293B")
    ax.set_facecolor("#1E293B")

    for i, y_col in enumerate(y_cols):
        color = COLORS[i % len(COLORS)]
        if chart_type == "Line":
            ax.plot(
                df[x_col], df[y_col], marker="o", label=y_col, color=color, linewidth=2
            )
        elif chart_type == "Bar":
            ax.bar(df[x_col], df[y_col], label=y_col, color=color, alpha=0.8)
        elif chart_type == "Area":
            ax.fill_between(df[x_col], df[y_col], alpha=0.4, label=y_col, color=color)
        elif chart_type == "Scatter":
            ax.scatter(df[x_col], df[y_col], label=y_col, color=color, s=50)

    ax.set_xlabel(x_col, color="#F8FAFC", fontsize=12)
    ax.set_ylabel("Value", color="#F8FAFC", fontsize=12)
    ax.tick_params(colors="#94A3B8")
    ax.legend(facecolor="#1E293B", edgecolor="#94A3B8", labelcolor="#F8FAFC")
    ax.spines["bottom"].set_color("#94A3B8")
    ax.spines["left"].set_color("#94A3B8")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    return fig


def main():
    init_session_state()

    st.markdown(
        """
        <style>
        .stApp { background-color: #0E1117; }
        .main-title { font-size: 32px; font-weight: bold; color: #10B981; margin-bottom: 8px; }
        .subtitle { font-size: 16px; color: #94A3B8; margin-bottom: 24px; }
        .chat-message { padding: 16px; border-radius: 12px; margin-bottom: 12px; background: #1E293B; }
        .chat-user { background: #10B98120; border-left: 4px solid #10B981; }
        .chat-assistant { border-left: 4px solid #3B82F6; }
        .metric-card { background: #1E293B; padding: 20px; border-radius: 12px; text-align: center; }
        .metric-value { font-size: 28px; font-weight: bold; color: #10B981; }
        .metric-label { font-size: 14px; color: #94A3B8; }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-title">📊 Revenue Forecast Tester AI Agent</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitle">Upload data, analyze with AI, and visualize results</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📁 Data Upload", "🤖 AI Chat", "📈 Chart Bot", "🧪 Forecast Test"]
    )

    with tab1:
        st.subheader("Upload Your Revenue Data")

        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file", type=["csv", "xlsx"]
        )

        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                st.session_state.uploaded_data = df

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(
                        f"<div class='metric-card'><div class='metric-value'>{len(df)}</div><div class='metric-label'>Rows</div></div>",
                        unsafe_allow_html=True,
                    )
                with col2:
                    st.markdown(
                        f"<div class='metric-card'><div class='metric-value'>{len(df.columns)}</div><div class='metric-label'>Columns</div></div>",
                        unsafe_allow_html=True,
                    )
                with col3:
                    st.markdown(
                        f"<div class='metric-card'><div class='metric-value'>{len(df.select_dtypes(include=[np.number]).columns)}</div><div class='metric-label'>Numeric Columns</div></div>",
                        unsafe_allow_html=True,
                    )

                st.subheader("Data Preview")
                st.dataframe(df.head(10), use_container_width=True)

                st.subheader("Column Types")
                col_info = pd.DataFrame(
                    {"Column": df.columns, "Type": df.dtypes.values}
                )
                st.dataframe(col_info, use_container_width=True)

            except Exception as e:
                st.error(f"Error loading file: {e}")
        else:
            st.info("Please upload a CSV or Excel file to get started.")
            st.markdown("""
            **Expected columns for forecast testing:**
            - Date/Period
            - Revenue/Actual
            - Predicted/Forecast (optional)
            """)

    with tab2:
        st.subheader("AI Analysis Chat")

        if st.session_state.uploaded_data is not None:
            df = st.session_state.uploaded_data

            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            if prompt := st.chat_input("Ask about your revenue data..."):
                st.session_state.chat_history.append(
                    {"role": "user", "content": prompt}
                )

                with st.chat_message("user"):
                    st.write(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing..."):
                        response = generate_ai_response(df, prompt)
                        st.write(response)

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": response}
                )

            col1, col2 = st.columns([6, 1])
            with col2:
                if st.button("Clear Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
        else:
            st.info("Please upload data first in the Data Upload tab.")

    with tab3:
        st.subheader("Chart Bot - Build Your Visualizations")

        if st.session_state.uploaded_data is not None:
            df = st.session_state.uploaded_data

            col1, col2 = st.columns([1, 2])

            with col1:
                chart_type = st.selectbox(
                    "Chart Type", ["Line", "Bar", "Area", "Scatter"]
                )
                all_cols = df.columns.tolist()
                x_col = st.selectbox("X-Axis Column", all_cols)
                y_cols = st.multiselect(
                    "Y-Axis Columns", all_cols, default=all_cols[:1] if all_cols else []
                )

            with col2:
                if y_cols:
                    fig = create_chart(df, chart_type, x_col, y_cols)
                    st.pyplot(fig)

                    col_btn1, col_btn2 = st.columns([1, 1])
                    with col_btn1:
                        buf = BytesIO()
                        fig.savefig(buf, format="png", dpi=150, facecolor="#1E293B")
                        b64 = base64.b64encode(buf.getvalue()).decode()
                        href = f'<a href="data:image/png;base64,{b64}" download="chart.png" style="background:#10B981;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;display:inline-block;">📥 Download Chart</a>'
                        st.markdown(href, unsafe_allow_html=True)
                else:
                    st.warning("Please select at least one Y-axis column.")
        else:
            st.info("Please upload data first in the Data Upload tab.")

    with tab4:
        st.subheader("Forecast Accuracy Testing")

        if st.session_state.uploaded_data is not None:
            df = st.session_state.uploaded_data
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

            if len(numeric_cols) >= 2:
                col1, col2, col3 = st.columns(3)

                with col1:
                    actual_col = st.selectbox(
                        "Actual Revenue Column", numeric_cols, key="actual"
                    )
                with col2:
                    pred_col = st.selectbox(
                        "Forecast/Predicted Column", numeric_cols, key="pred"
                    )
                with col3:
                    threshold = st.slider("Anomaly Threshold (std)", 1.0, 4.0, 2.0)

                if st.button("Run Forecast Test"):
                    actual = df[actual_col]
                    predicted = df[pred_col]

                    metrics = calculate_metrics(actual, predicted)

                    st.subheader("Accuracy Metrics")
                    m_col1, m_col2, m_col3 = st.columns(3)
                    with m_col1:
                        st.markdown(
                            f"<div class='metric-card'><div class='metric-value'>{metrics['MAPE']:.2f}%</div><div class='metric-label'>MAPE</div></div>",
                            unsafe_allow_html=True,
                        )
                    with m_col2:
                        st.markdown(
                            f"<div class='metric-card'><div class='metric-value'>{metrics['MAE']:.2f}</div><div class='metric-label'>MAE</div></div>",
                            unsafe_allow_html=True,
                        )
                    with m_col3:
                        st.markdown(
                            f"<div class='metric-card'><div class='metric-value'>{metrics['RMSE']:.2f}</div><div class='metric-label'>RMSE</div></div>",
                            unsafe_allow_html=True,
                        )

                    residuals = actual - predicted
                    mean_res = residuals.mean()
                    std_res = residuals.std()
                    anomalies = df[abs(residuals) > threshold * std_res]

                    if not anomalies.empty:
                        st.subheader("⚠️ Detected Anomalies")
                        st.dataframe(anomalies, use_container_width=True)

                    st.subheader("Residual Analysis")
                    fig_res, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
                    fig_res.patch.set_facecolor("#1E293B")

                    ax1.plot(df.index, residuals, color="#10B981", linewidth=1)
                    ax1.axhline(y=0, color="#EF4444", linestyle="--", alpha=0.5)
                    ax1.axhline(
                        y=threshold * std_res,
                        color="#F59E0B",
                        linestyle="--",
                        alpha=0.5,
                    )
                    ax1.axhline(
                        y=-threshold * std_res,
                        color="#F59E0B",
                        linestyle="--",
                        alpha=0.5,
                    )
                    ax1.set_xlabel("Index", color="#F8FAFC")
                    ax1.set_ylabel("Residual", color="#F8FAFC")
                    ax1.tick_params(colors="#94A3B8")
                    ax1.set_facecolor("#1E293B")
                    ax1.spines["top"].set_visible(False)
                    ax1.spines["right"].set_visible(False)

                    ax2.hist(
                        residuals,
                        bins=20,
                        color="#3B82F6",
                        edgecolor="#1E293B",
                        alpha=0.7,
                    )
                    ax2.set_xlabel("Residual", color="#F8FAFC")
                    ax2.set_ylabel("Frequency", color="#F8FAFC")
                    ax2.tick_params(colors="#94A3B8")
                    ax2.set_facecolor("#1E293B")
                    ax2.spines["top"].set_visible(False)
                    ax2.spines["right"].set_visible(False)

                    st.pyplot(fig_res)

                    st.subheader("🤖 AI Recommendations")
                    recommendations = generate_forecast_recommendations(
                        actual, predicted, metrics
                    )
                    st.markdown(f"```\n{recommendations}\n```")
            else:
                st.warning(
                    "Need at least 2 numeric columns for forecast testing (Actual and Predicted)."
                )
        else:
            st.info("Please upload data first in the Data Upload tab.")


if __name__ == "__main__":
    main()
