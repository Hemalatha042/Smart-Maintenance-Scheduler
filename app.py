import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta

from utils import predict_failures
from email_alert import send_email_alert  # ✅ Working email alert function

st.set_page_config(page_title="Smart Maintenance Scheduler")
st.title("🛠️ Smart Maintenance Scheduler")

st.markdown("Upload your machine log data to predict if maintenance is needed.")

# 📁 Upload CSV
uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Uploaded Data")
    st.dataframe(df)

    # 🔍 Predict failures
    result_df = predict_failures(df)
    st.subheader("🔍 Maintenance Prediction Results")
    st.dataframe(result_df)

    # 📊 Bar chart: Maintenance Needed vs Not Needed
    st.subheader("📊 Maintenance Needed vs Not Needed")
    st.bar_chart(result_df["Maintenance_Required"].value_counts())

    # ⬇️ Excel download
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        result_df.to_excel(writer, index=False, sheet_name="Predictions")

    st.download_button(
        label="⬇️ Download Results as Excel",
        data=excel_buffer.getvalue(),
        file_name="maintenance_predictions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # 🔧 Maintenance alerts
    maintenance_needed = result_df[result_df["Maintenance_Required"] == 1]

    if not maintenance_needed.empty:
        st.warning(f"⚠️ {len(maintenance_needed)} machine(s) need maintenance.")

        # ✅ Feature 1: Show Top Error Codes Causing Failures
        st.subheader("📌 Top Error Codes Causing Failures")
        top_errors = maintenance_needed["Error_Code"].value_counts().head(5)
        st.table(top_errors.reset_index().rename(columns={"index": "Error Code", "Error_Code": "Count"}))

        # ✅ Feature 2: Calculate Average Hours Before Maintenance (MTBF)
        mtbf = maintenance_needed["Hours_Ran"].mean()
        st.metric("⏱️ Avg. Hours Before Maintenance (MTBF)", f"{mtbf:.2f} hours")

        # ✅ Feature 3: Suggested Next Maintenance Dates
        st.subheader("🗓️ Suggested Maintenance Dates")
        today = datetime.today()
        maintenance_needed["Next_Maintenance_Date"] = today + timedelta(days=30)
        st.dataframe(maintenance_needed[["Machine_ID", "Next_Maintenance_Date"]])

        # 📧 Email alert to supervisor
        supervisor_email = st.text_input("Supervisor Email Address")  # Update if needed
        if supervisor_email:
            email_sent = send_email_alert(supervisor_email, len(maintenance_needed))

        if email_sent:
            st.success("✅ Email successfully sent to supervisor.")
        else:
            st.error("❌ Email sending failed. Please check credentials or internet.")

    else:
        st.success("✅ No maintenance required for any machine!")
