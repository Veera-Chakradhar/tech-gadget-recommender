import streamlit as st

from app import laptop_agent


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Tech Gadget & Laptop Recommender",
    page_icon="💻",
    layout="wide"
)


# ---------------------------------------------------------
# Custom Styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">💻 Tech Gadget & Laptop Recommender</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered laptop recommendations for students and developers</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("About the Agent")

    st.write(
        """
        This AI agent helps students choose laptops
        based on their budget and requirements.
        """
    )

    st.write("### Technologies")

    st.write(
        """
        • Gemini AI  
        • LangGraph  
        • FAISS  
        • RAG  
        • Python  
        • Streamlit
        """
    )


# ---------------------------------------------------------
# User Input
# ---------------------------------------------------------

st.subheader("Tell us what laptop you need")

question = st.text_area(
    "Enter your requirements",
    placeholder=(
        "Example: I am a B.Tech AI/ML student. "
        "My budget is 80000. I need a laptop for "
        "Python, machine learning, deep learning and college work."
    ),
    height=150
)


# ---------------------------------------------------------
# Recommendation Button
# ---------------------------------------------------------

if st.button(
    "🔍 Find My Laptop",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter your laptop requirements."
        )

    else:

        with st.spinner(
            "Analyzing your requirements..."
        ):

            try:

                result = laptop_agent(
                    question
                )

                # -------------------------------------------------
                # Extract Results
                # -------------------------------------------------

                budget = result.get(
                    "budget",
                    None
                )

                use_case = result.get(
                    "use_case",
                    "Unknown"
                )

                laptops = result.get(
                    "affordable_laptops",
                    []
                )

                recommendation = result.get(
                    "recommendation",
                    "No recommendation available."
                )


                # -------------------------------------------------
                # Requirement Summary
                # -------------------------------------------------

                st.subheader(
                    "📋 Your Requirements"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if budget:

                        st.metric(
                            "Maximum Budget",
                            f"₹{budget:,}"
                        )

                    else:

                        st.metric(
                            "Maximum Budget",
                            "Not specified"
                        )

                with col2:

                    st.write("**Main Use Case**")

                    st.write(
                        use_case
                    )


                # -------------------------------------------------
                # Affordable Laptops
                # -------------------------------------------------

                st.subheader(
                    "💰 Laptops Within Your Budget"
                )

                if laptops:

                    for laptop in laptops:

                        col1, col2 = st.columns(
                            [3, 1]
                        )

                        with col1:

                            st.write(
                                f"💻 **{laptop['name']}**"
                            )

                        with col2:

                            st.write(
                                f"₹{laptop['price']:,}"
                            )

                else:

                    st.info(
                        "No laptops were found within your budget."
                    )


                # -------------------------------------------------
                # Final Recommendation
                # -------------------------------------------------

                st.subheader(
                    "🤖 AI Recommendation"
                )

                st.markdown(
                    '<div class="result-box">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    recommendation
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            except Exception as error:

                st.error(
                    "Something went wrong while generating "
                    "the recommendation."
                )

                st.write(
                    str(error)
                )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Tech Gadget & Laptop Recommender • "
    "Built with Python, LangGraph, FAISS, RAG and Gemini"
)