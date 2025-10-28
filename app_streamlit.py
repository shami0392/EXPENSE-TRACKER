import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from db import init_db, add_expense, get_all_expenses

# Init DB
init_db()

st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker with Analytics")

menu = ["Add Expense", "View Expenses", "Analytics"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Expense":
    st.subheader("➕ Add a New Expense")
    amount = st.number_input("Amount (INR)", min_value=0.0, step=10.0)
    category = st.selectbox("Category", ["Food", "Travel", "Bills", "Shopping", "Other"])
    date = st.date_input("Date", datetime.today())
    note = st.text_input("Note (optional)")

    if st.button("Save Expense"):
        add_expense(amount, category, str(date), note)
        st.success("✅ Expense added successfully!")

elif choice == "View Expenses":
    st.subheader("📋 All Expenses")
    data = get_all_expenses()
    if len(data) == 0:
        st.warning("⚠ No expenses found")
    else:
        df = pd.DataFrame(data, columns=["ID", "Amount", "Category", "Date", "Note"])
        st.dataframe(df)

elif choice == "Analytics":
    st.subheader("📊 Expense Analytics")
    data = get_all_expenses()
    if len(data) == 0:
        st.warning("⚠ No expenses found")
    else:
        df = pd.DataFrame(data, columns=["ID", "Amount", "Category", "Date", "Note"])
        df["Date"] = pd.to_datetime(df["Date"])

        total = df["Amount"].sum()
        top_cat = df.groupby("Category")["Amount"].sum().idxmax()

        st.write(f"💵 *Total Expenses:* {total} INR")
        st.write(f"🏆 *Top Category:* {top_cat}")

        # Pie chart
        st.write("### Category-wise Distribution")
        cat_sum = df.groupby("Category")["Amount"].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(cat_sum, labels=cat_sum.index, autopct="%1.1f%%")
        ax1.set_title("Expenses by Category")
        st.pyplot(fig1)

        # Line chart
        st.write("### Monthly Trend")
        monthly_sum = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum()
        fig2, ax2 = plt.subplots()
        monthly_sum.plot(kind="line", marker="o", ax=ax2)
        ax2.set_title("Monthly Expense Trend")
        ax2.set_ylabel("Amount (INR)")
        st.pyplot(fig2)