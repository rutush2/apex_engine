import streamlit as st
import pandas as pd
import altair as alt
from database import engine, SessionLocal, init_db
from apex_queries import ApexAuditor
import models


def main():
    st.set_page_config(page_title="Apex Engine | Command", layout="wide")

    st.markdown("""
        <style>
        /* This hides the header completely to stop the chopping */
        header[data-testid="stHeader"] { visibility: hidden; display: none; }

        /* Forces the entire dashboard down to clear the top bar area */
        .block-container { padding-top: 8rem !important; }

        [data-testid="stMetricValue"] { color: #1f77b4; font-family: 'Courier New', monospace; }
        .stTabs [data-baseweb="tab-list"] { gap: 24px; }
        </style>
    """, unsafe_allow_html=True)

    auditor = ApexAuditor()

    models.Base.metadata.create_all(bind=engine)

    with st.sidebar:
        st.header("⚙️ Apex Control")
        if st.button("🔄 Sync Intelligence", use_container_width=True):
            st.rerun()

    tab_dashboard, tab_entry = st.tabs(["📊 Analytics Dashboard", "📥 Data Ingestion"])

    with tab_dashboard:
        findings = auditor.generate_audit_report()

        if not findings:
            st.info("Engine status: Awaiting data ingestion...")
        else:
            df = pd.DataFrame([{
                "Code": f.ref_code,
                "Subject": f.subject,
                "Impact": f.impact_level,
                "Priority": f.priority,
                "Status": f.status,
                "Age": f.age_in_days,
                "Solutions": len(f.strategies),
                "Age": f.age_in_days,
            } for f in findings])


            with st.container(border=True):
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Findings", len(df), delta="Active")
                m2.metric("Mean Priority", f"{df['Priority'].mean():.2f}")
                m3.metric("Remediation Rate",
                          f"{(len(df[df['Status'] == 'Resolved']) / len(df) * 100 if len(df) > 0 else 0):.1f}%")
                m4.metric("Avg Age", f"{df['Age'].mean():.1f} Days")

            st.divider()

            col_left, col_right = st.columns([2, 1])
            with col_left:
                st.subheader("📊 Risk Velocity Heatmap")
                chart = alt.Chart(df).mark_circle(size=200).encode(
                    x=alt.X('Age:Q', title='Days Since Detection'),
                    y=alt.Y('Priority:Q', title='Priority Score (0-10)'),
                    color=alt.Color('Impact:N', scale=alt.Scale(domain=['Critical', 'High', 'Medium', 'Low'],
                                                                range=['#D32F2F', '#F57C00', '#FBC02D', '#388E3C'])),
                    tooltip=['Code', 'Subject', 'Priority']
                ).interactive()
                st.altair_chart(chart, use_container_width=True)

            with col_right:
                st.subheader("🌐 Status Distribution")
                donut = alt.Chart(df).mark_arc(innerRadius=50).encode(
                    theta=alt.Angle("count():Q"),
                    color=alt.Color("Status:N", scale=alt.Scale(range=['#1f77b4', '#aec7e8', '#ff7f0e'])),
                    tooltip=['Status', 'count()']
                )
                st.altair_chart(donut, use_container_width=True)

            st.divider()

            st.subheader("📋 Intelligence Queue")
            for f in findings:
                with st.expander(f"🔍 {f.ref_code} | {f.subject}"):
                    col_info, col_promote = st.columns([2, 1])

                    with col_info:
                        st.write(f"**Impact:** {f.impact_level} | **Current Status:** {f.status}")

                    with col_promote:
                        new_stat = st.selectbox(
                            "Update Status",
                            ["Identified", "In-Progress", "Resolved"],
                            index=["Identified", "In-Progress", "Resolved"].index(f.status) if f.status in [
                                "Identified", "In-Progress", "Resolved"] else 0,
                            key=f"stat_sel_{f.id}"
                        )
                        if new_stat != f.status:
                            auditor.update_finding_status(f.id, new_stat)
                            st.rerun()

                    st.divider()

                    for s in f.strategies:
                        st.info(f"🛠️ **{s.title}**: {s.methodology}")

                    with st.form(f"strat_form_{f.id}", clear_on_submit=True):
                        s_title = st.text_input("Strategy Title")
                        s_steps = st.text_area("Mitigation Steps")

                        if st.form_submit_button("Add Strategy"):
                            if s_title and s_steps:
                                auditor.add_strategy(f.id, s_title, s_steps)
                                st.rerun()

    with tab_entry:
        st.subheader("🌐 Ingest New Intelligence")
        with st.form("new_finding_form", clear_on_submit=True):
            f_code = st.text_input("Finding Code")
            f_subject = st.text_input("Subject")
            f_impact = st.selectbox("Impact", ["Critical", "High", "Medium", "Low"])
            f_status = st.selectbox("Status", ["Identified", "In-Progress", "Resolved"])
            f_age = st.number_input("Age in Days", min_value=0, step=1)

            if st.form_submit_button("Submit"):
                if f_code and f_subject:
                    auditor.ingest_finding(f_code, f_subject, f_impact, f_status, f_age)
                    st.success("Finding integrated.")
                    st.rerun()


if __name__ == "__main__":
    main()