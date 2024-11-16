import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data.csv')

st.sidebar.title("Media Analysis")
st.sidebar.write("Choose an Option")

# Add some widgets to the sidebar
dropdown_value = st.sidebar.selectbox(
    "Analysis based on App:",  # Heading for the dropdown
    ["Overall", "Instagram", "Facebook", "Snapchat", "Pinterest", "TikTok", "LinkedIn", "Twitter"]  # List of values
)


# Function to display summary statistics
def display_summary_statistics(df_app, app_name):
    st.write(f"### Summary for {app_name}")
    st.write(f"**Total Users:** {df_app['User_ID'].nunique()}")
    st.write(f"**Total Posts per Day:** {df_app['Posts_Per_Day'].sum()}")
    st.write(f"**Total Likes per Day:** {df_app['Likes_Per_Day'].sum()}")
    st.write(f"**Total Follows per Day:** {df_app['Follows_Per_Day'].sum()}")
    st.write(f"**Total Daily Minutes Spent:** {df_app['Daily_Minutes_Spent'].sum()} minutes")
    st.write(f"**Average Daily Minutes Spent per User:** {df_app['Daily_Minutes_Spent'].mean():.2f} minutes")


if dropdown_value == "Overall":
    st.title('Social Media Usage Analysis')
    st.write("""
    This app allows you to analyze social media usage data. You can view overall statistics,
    compare activities across different apps, and identify top users based on daily time spent, posts, likes, and follows.
    """)
    st.dataframe(df)

    # Show the scatter plot for each app
    st.subheader("Point Graph for Each App")
    app_colors = {
        "Instagram": "red",
        "Facebook": "blue",
        "Snapchat": "yellow",
        "Pinterest": "purple",
        "TikTok": "orange",
        "LinkedIn": "green",
        "Twitter": "cyan"
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    for app in df['App'].unique():
        app_data = df[df['App'] == app]
        ax.scatter(app_data['User_ID'], app_data['Daily_Minutes_Spent'], label=app, color=app_colors.get(app, 'gray'),
                   alpha=0.6)

    ax.set_title("Posts Per Day vs Likes Per Day for Each App", fontsize=16)
    ax.set_xlabel("Users", fontsize=12)
    ax.set_ylabel("Daily Minutes Spent", fontsize=12)
    ax.legend(title="Apps")
    st.pyplot(fig)

elif dropdown_value in ["Instagram", "Facebook", "Snapchat", "Pinterest", "TikTok", "LinkedIn", "Twitter"]:
    # Filter data for the selected app
    df_app = df[df['App'] == dropdown_value]

    # Display summary statistics
    display_summary_statistics(df_app, dropdown_value)

    # Add user filter: Select a user based on User_ID
    user_filter = st.selectbox("Select a User ID:", df_app['User_ID'].unique())
    df_user = df_app[df_app['User_ID'] == user_filter]
    st.write(f"### Data for User {user_filter}")
    st.dataframe(df_user)

    # Allow users to choose a specific graph
    graph_option = st.selectbox(
        f"Select a Graph to Display for {dropdown_value}:",
        ["Posts Per Day", "Likes Per Day", "Posts vs Likes Per Day", "Daily Time Spent"]
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    # Display the selected graph
    if graph_option == "Posts Per Day":
        st.subheader("Posts Per Day")
        ax.plot(df_app['User_ID'], df_app['Posts_Per_Day'], marker='o', color='red')
        ax.set_title(f"Posts Per Day for {dropdown_value}", fontsize=14)
        ax.set_xlabel("User ID", fontsize=12)
        ax.set_ylabel("Posts Per Day", fontsize=12)
        ax.grid(True)

    elif graph_option == "Likes Per Day":
        st.subheader("Likes Per Day")
        ax.bar(df_app['User_ID'], df_app['Likes_Per_Day'], color='blue')
        ax.set_title(f"Likes Per Day for {dropdown_value}", fontsize=14)
        ax.set_xlabel("User ID", fontsize=12)
        ax.set_ylabel("Likes Per Day", fontsize=12)
        ax.grid(True)

    elif graph_option == "Posts vs Likes Per Day":
        st.subheader("Posts vs Likes Per Day")
        ax.scatter(df_app['Posts_Per_Day'], df_app['Likes_Per_Day'], color='green')
        ax.set_title(f"Posts vs Likes Per Day for {dropdown_value}", fontsize=14)
        ax.set_xlabel("Posts Per Day", fontsize=12)
        ax.set_ylabel("Likes Per Day", fontsize=12)
        ax.grid(True)

    elif graph_option == "Daily Time Spent":
        st.subheader("Daily Time Spent")
        ax.hist(df_app['Daily_Minutes_Spent'], bins=20, color='purple', edgecolor='black')
        ax.set_title(f"Histogram of Daily Minutes Spent on {dropdown_value}", fontsize=14)
        ax.set_xlabel("Minutes", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.grid(True)

    # Adjust layout to make sure plots don't overlap
    fig.tight_layout()
    st.pyplot(fig)

    # Add option to download the filtered data
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=df_user.to_csv(index=False),
        file_name=f"{dropdown_value}_user_{user_filter}_data.csv",
        mime="text/csv"
    )
