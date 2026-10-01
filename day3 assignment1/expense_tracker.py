import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS - SIMPLE LIGHT UI
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0E1117;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Main title */
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #243447;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Cards */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        text-align: center;
    }

    .metric-title {
        color: #6b7280;
        font-size: 14px;
    }

    .metric-value {
        color: #243447;
        font-size: 25px;
        font-weight: 700;
        margin-top: 5px;
    }

    /* Section headings */
    .section-title {
        color: #243447;
        font-size: 22px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        border: none;
        background-color: #4f86c6;
        color: white;
        font-weight: 600;
        padding: 8px 18px;
    }

    .stButton > button:hover {
        background-color: #3d6fa8;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #eef3f8;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "next_id" not in st.session_state:
    st.session_state.next_id = 1


# ---------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------

def create_dataframe():
    """Convert session state expenses into a DataFrame."""

    if len(st.session_state.expenses) == 0:
        return pd.DataFrame(
            columns=[
                "ID",
                "Date",
                "Category",
                "Description",
                "Amount",
                "Payment Method"
            ]
        )

    return pd.DataFrame(st.session_state.expenses)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">💰 Expense Tracker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Track, manage and understand your spending patterns</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------

st.sidebar.title("💰 Expense Tracker")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "➕ Add Expense",
        "📋 View Expenses",
        "✏️ Update Expense",
        "🗑️ Delete Expense",
        "📊 Analytics"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="section-title">📊 Spending Overview</div>',
        unsafe_allow_html=True
    )

    df = create_dataframe()

    # No expenses
    if df.empty:

        st.info("No expenses recorded yet. Add your first expense from the sidebar.")

    else:

        total_expense = df["Amount"].sum()
        number_expenses = len(df)
        average_expense = df["Amount"].mean()
        highest_expense = df["Amount"].max()

        # KPI CARDS
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Total Spending</div>
                    <div class="metric-value">₹{total_expense:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Number of Expenses</div>
                    <div class="metric-value">{number_expenses}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Average Expense</div>
                    <div class="metric-value">₹{average_expense:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Highest Expense</div>
                    <div class="metric-value">₹{highest_expense:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        # Recent expenses
        st.markdown(
            '<div class="section-title">🧾 Recent Expenses</div>',
            unsafe_allow_html=True
        )

        recent_df = df.sort_values("Date", ascending=False).head(5)

        st.dataframe(
            recent_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# ADD EXPENSE
# =========================================================

elif page == "➕ Add Expense":

    st.markdown(
        '<div class="section-title">➕ Add New Expense</div>',
        unsafe_allow_html=True
    )

    with st.form("add_expense_form"):

        col1, col2 = st.columns(2)

        with col1:

            expense_date = st.date_input(
                "Date",
                value=date.today()
            )

            category = st.selectbox(
                "Category",
                [
                    "Food",
                    "Transport",
                    "Shopping",
                    "Education",
                    "Bills",
                    "Health",
                    "Entertainment",
                    "Others"
                ]
            )

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                step=10.0
            )

        with col2:

            description = st.text_input(
                "Description",
                placeholder="Example: Lunch"
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "UPI",
                    "Credit Card",
                    "Debit Card",
                    "Net Banking"
                ]
            )

        submitted = st.form_submit_button(
            "➕ Add Expense"
        )

        if submitted:

            if amount <= 0:

                st.error("Please enter an amount greater than ₹0.")

            elif description.strip() == "":

                st.error("Please enter a description.")

            else:

                new_expense = {
                    "ID": st.session_state.next_id,
                    "Date": expense_date,
                    "Category": category,
                    "Description": description,
                    "Amount": amount,
                    "Payment Method": payment_method
                }

                st.session_state.expenses.append(new_expense)

                st.session_state.next_id += 1

                st.success("✅ Expense added successfully!")


# =========================================================
# VIEW EXPENSES
# =========================================================

elif page == "📋 View Expenses":

    st.markdown(
        '<div class="section-title">📋 All Expenses</div>',
        unsafe_allow_html=True
    )

    df = create_dataframe()

    if df.empty:

        st.info("No expenses available.")

    else:

        # Filters
        col1, col2 = st.columns(2)

        with col1:

            category_filter = st.selectbox(
                "Filter by Category",
                ["All"] + sorted(df["Category"].unique().tolist())
            )

        with col2:

            search = st.text_input(
                "🔍 Search",
                placeholder="Search description or category..."
            )

        filtered_df = df.copy()

        # Category filter
        if category_filter != "All":

            filtered_df = filtered_df[
                filtered_df["Category"] == category_filter
            ]

        # Search
        if search:

            search_lower = search.lower()

            filtered_df = filtered_df[
                filtered_df["Description"].str.lower().str.contains(
                    search_lower,
                    na=False
                )
                |
                filtered_df["Category"].str.lower().str.contains(
                    search_lower,
                    na=False
                )
            ]

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        st.write(
            f"**Showing {len(filtered_df)} expense(s)**"
        )

        # Download
        csv = filtered_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Expenses",
            data=csv,
            file_name="expenses.csv",
            mime="text/csv"
        )


# =========================================================
# UPDATE EXPENSE
# =========================================================

elif page == "✏️ Update Expense":

    st.markdown(
        '<div class="section-title">✏️ Update Expense</div>',
        unsafe_allow_html=True
    )

    df = create_dataframe()

    if df.empty:

        st.info("No expenses available to update.")

    else:

        expense_ids = df["ID"].tolist()

        selected_id = st.selectbox(
            "Select Expense ID",
            expense_ids
        )

        selected_expense = next(
            expense for expense in st.session_state.expenses
            if expense["ID"] == selected_id
        )

        with st.form("update_form"):

            col1, col2 = st.columns(2)

            with col1:

                new_date = st.date_input(
                    "Date",
                    value=selected_expense["Date"]
                )

                categories = [
                    "Food",
                    "Transport",
                    "Shopping",
                    "Education",
                    "Bills",
                    "Health",
                    "Entertainment",
                    "Others"
                ]

                new_category = st.selectbox(
                    "Category",
                    categories,
                    index=categories.index(
                        selected_expense["Category"]
                    )
                )

                new_amount = st.number_input(
                    "Amount (₹)",
                    min_value=0.0,
                    value=float(selected_expense["Amount"]),
                    step=10.0
                )

            with col2:

                new_description = st.text_input(
                    "Description",
                    value=selected_expense["Description"]
                )

                payment_methods = [
                    "Cash",
                    "UPI",
                    "Credit Card",
                    "Debit Card",
                    "Net Banking"
                ]

                new_payment_method = st.selectbox(
                    "Payment Method",
                    payment_methods,
                    index=payment_methods.index(
                        selected_expense["Payment Method"]
                    )
                )

            update_button = st.form_submit_button(
                "✏️ Update Expense"
            )

            if update_button:

                if new_amount <= 0:

                    st.error(
                        "Amount must be greater than ₹0."
                    )

                elif new_description.strip() == "":

                    st.error(
                        "Description cannot be empty."
                    )

                else:

                    for expense in st.session_state.expenses:

                        if expense["ID"] == selected_id:

                            expense["Date"] = new_date
                            expense["Category"] = new_category
                            expense["Description"] = new_description
                            expense["Amount"] = new_amount
                            expense["Payment Method"] = new_payment_method

                            break

                    st.success(
                        "✅ Expense updated successfully!"
                    )


# =========================================================
# DELETE EXPENSE
# =========================================================

elif page == "🗑️ Delete Expense":

    st.markdown(
        '<div class="section-title">🗑️ Delete Expense</div>',
        unsafe_allow_html=True
    )

    df = create_dataframe()

    if df.empty:

        st.info("No expenses available to delete.")

    else:

        expense_ids = df["ID"].tolist()

        selected_id = st.selectbox(
            "Select Expense ID",
            expense_ids
        )

        selected_expense = next(
            expense for expense in st.session_state.expenses
            if expense["ID"] == selected_id
        )

        st.warning(
            f"""
            You are about to delete:

            **{selected_expense["Description"]}**

            Amount: ₹{selected_expense["Amount"]:,.2f}
            """
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this expense."
        )

        if st.button("🗑️ Delete Expense"):

            if not confirm:

                st.error(
                    "Please confirm the deletion first."
                )

            else:

                st.session_state.expenses = [
                    expense
                    for expense in st.session_state.expenses
                    if expense["ID"] != selected_id
                ]

                st.success(
                    "✅ Expense deleted successfully!"
                )


# =========================================================
# ANALYTICS
# =========================================================

elif page == "📊 Analytics":

    st.markdown(
        '<div class="section-title">📊 Spending Analytics</div>',
        unsafe_allow_html=True
    )

    df = create_dataframe()

    if df.empty:

        st.info(
            "Add some expenses to view analytics."
        )

    else:

        # ---------------------------------------------
        # CATEGORY CHART
        # ---------------------------------------------

        category_data = (
            df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        fig_category = px.pie(
            category_data,
            names="Category",
            values="Amount",
            title="💰 Spending by Category",
            hole=0.4
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

        # ---------------------------------------------
        # PAYMENT METHOD CHART
        # ---------------------------------------------

        payment_data = (
            df.groupby("Payment Method")["Amount"]
            .sum()
            .reset_index()
        )

        fig_payment = px.bar(
            payment_data,
            x="Payment Method",
            y="Amount",
            title="💳 Spending by Payment Method",
            text_auto=True
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True
        )

        # ---------------------------------------------
        # DAILY SPENDING TREND
        # ---------------------------------------------

        daily_data = (
            df.groupby("Date")["Amount"]
            .sum()
            .reset_index()
        )

        daily_data["Date"] = pd.to_datetime(
            daily_data["Date"]
        )

        fig_trend = px.line(
            daily_data,
            x="Date",
            y="Amount",
            title="📈 Daily Spending Trend",
            markers=True
        )

        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )

        # ---------------------------------------------
        # INSIGHTS
        # ---------------------------------------------

        st.markdown(
            '<div class="section-title">💡 Spending Insights</div>',
            unsafe_allow_html=True
        )

        highest_category = (
            category_data
            .sort_values("Amount", ascending=False)
            .iloc[0]
        )

        st.info(
            f"💡 Your highest spending category is "
            f"**{highest_category['Category']}** "
            f"with ₹{highest_category['Amount']:,.2f}."
        )

        highest_expense = df.loc[
            df["Amount"].idxmax()
        ]

        st.info(
            f"💡 Your highest individual expense is "
            f"**₹{highest_expense['Amount']:,.2f}** "
            f"for **{highest_expense['Description']}**."
        )