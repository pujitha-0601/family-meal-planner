import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
st.set_page_config(page_title="Family Meal Planner", layout="wide")
st.title("Family Meal Planner - AI Agent (3 Agents)")

api_key = os.getenv("GROQ_API_KEY") 
if not api_key:
    st.error("API Key pettu!")
    st.stop()

client = Groq(api_key=api_key)

# Sidebar
budget = st.sidebar.text_input("Weekly Budget", "Rs 2000")
allergies = st.sidebar.text_input("Allergies", "None")

def call_agent(role, task):
    prompt = f"You are {role}. Task: {task}. Budget: {budget}, Avoid: {allergies}"
    res = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

if st.button("Generate Weekly Meal Plan"):
    
    with st.spinner("Agent 1: Meal Planner working..."):
        st.subheader("🤖 Agent 1: Meal Planner Agent")
        meal_plan = call_agent("Indian Family Meal Planner", "Create 7 days Indian breakfast, lunch, dinner, snack plan")
        st.markdown(meal_plan)
    
    with st.spinner("Agent 2: Nutrition Agent checking..."):
        st.subheader("🤖 Agent 2: Nutrition Agent")
        nutrition = call_agent("Nutritionist", f"Check nutrition for this meal plan and add calories: {meal_plan}")
        st.markdown(nutrition)
    
    with st.spinner("Agent 3: Shopping Agent listing..."):
        st.subheader("🤖 Agent 3: Shopping List Agent")
        shopping = call_agent("Shopping Assistant", f"Create budget shopping list under {budget} for this plan: {meal_plan}. Avoid: {allergies}")
        st.markdown(shopping)
    
    st.success("3 Agents Completed!")

st.caption("CrewAI Concept - 3 Agents - Meal, Nutrition, Shopping")