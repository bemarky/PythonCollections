import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import random

# Set page config
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS styling
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f9fafb;
    }

    /* Headers */
    h1, h2, h3 {
        color: #1f2937;
    }

    /* Cards */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* Info boxes */
    .info-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #1e293b;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# Function to generate random sales data
@st.cache_data
def generate_sales_data(days=90):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    # Generate product data
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    regions = ['North', 'South', 'East', 'West', 'Central']

    # Create random data
    data = []
    for date in date_range:
        for product in products:
            for region in regions:
                # Create some seasonality and trends
                base_quantity = random.randint(5, 50)
                day_factor = 1 + 0.3 * np.sin(date.day_of_year / 30)

                # Products have different popularity
                product_factor = {
                    'Product A': 1.5,
                    'Product B': 0.7,
                    'Product C': 1.2,
                    'Product D': 0.9,
                    'Product E': 1.1
                }[product]

                # Regions have different sales volumes
                region_factor = {
                    'North': 1.1,
                    'South': 0.9,
                    'East': 1.3,
                    'West': 1.2,
                    'Central': 0.8
                }[region]

                quantity = int(base_quantity * day_factor * product_factor * region_factor)
                price = {
                    'Product A': 50,
                    'Product B': 75,
                    'Product C': 100,
                    'Product D': 120,
                    'Product E': 200
                }[product]

                revenue = quantity * price

                data.append({
                    'date': date,
                    'product': product,
                    'region': region,
                    'quantity': quantity,
                    'price': price,
                    'revenue': revenue
                })

    return pd.DataFrame(data)


# Function to generate random user data
@st.cache_data
def generate_user_data(num_users=1000):
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()

    users = []
    for i in range(num_users):
        # Generate a random join date
        join_date = start_date + timedelta(days=random.randint(0, 365))

        # Generate user activity level
        activity_level = random.choice(['High', 'Medium', 'Low'])

        # Generate login count based on activity level
        if activity_level == 'High':
            login_count = random.randint(50, 200)
        elif activity_level == 'Medium':
            login_count = random.randint(15, 50)
        else:
            login_count = random.randint(1, 15)

        # Generate subscription status
        subscription = random.choice(['Free', 'Basic', 'Premium', 'Enterprise'])

        # Generate user data
        users.append({
            'user_id': f'USER{i + 1000}',
            'join_date': join_date,
            'last_login': join_date + timedelta(days=random.randint(0, (end_date - join_date).days)),
            'name': f'User {i + 1}',
            'email': f'user{i + 1}@example.com',
            'country': random.choice(
                ['USA', 'Canada', 'UK', 'Germany', 'France', 'Australia', 'Japan', 'Brazil', 'India', 'China']),
            'subscription': subscription,
            'activity_level': activity_level,
            'login_count': login_count,
            'completed_profile': random.choice([True, False]),
            'notifications_enabled': random.choice([True, False])
        })

    return pd.DataFrame(users)


# Function to generate issue tickets
@st.cache_data
def generate_tickets(num_tickets=200):
    start_date = datetime.now() - timedelta(days=30)

    tickets = []
    for i in range(num_tickets):
        created_date = start_date + timedelta(days=random.randint(0, 30))

        status = random.choice(['Open', 'In Progress', 'Closed', 'Resolved'])

        if status in ['Closed', 'Resolved']:
            resolved_date = created_date + timedelta(days=random.randint(1, 5))
        else:
            resolved_date = None

        priority = random.choice(['Low', 'Medium', 'High', 'Critical'])

        tickets.append({
            'ticket_id': f'TCK-{i + 1000}',
            'created_date': created_date,
            'resolved_date': resolved_date,
            'status': status,
            'title': f'Issue {i + 1}',
            'category': random.choice(['Bug', 'Feature Request', 'Question', 'Technical Issue', 'Billing']),
            'priority': priority,
            'assigned_to': f'Agent {random.randint(1, 10)}',
            'user_id': f'USER{random.randint(1000, 2000)}'
        })

    return pd.DataFrame(tickets)


# Load data (cached)
sales_df = generate_sales_data()
user_df = generate_user_data()
ticket_df = generate_tickets()


# Authentication (simple demo version)
def check_password():
    # Hard-coded credentials for demo purposes only
    # In a real application, you would use a secure authentication system
    return True  # Bypass authentication for this demo

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username == "admin" and password == "password":
            st.session_state.authenticated = True
            return True
        else:
            st.sidebar.error("Invalid username or password")
            return False
    return False


# Main dashboard function
def dashboard():
    # Sidebar navigation
    st.sidebar.title("Admin Dashboard")

    # User profile picture placeholder
    st.sidebar.image("https://via.placeholder.com/150", width=100)
    st.sidebar.write("Welcome, Admin")

    # Navigation
    page = st.sidebar.radio("Navigation",
                            ["Dashboard", "Sales Analytics", "User Management", "Support Tickets", "Settings"])

    # Sidebar filters that apply to all pages
    st.sidebar.header("Filters")

    # Date range filter
    date_option = st.sidebar.selectbox(
        "Date Range",
        ["Last 7 days", "Last 30 days", "Last 90 days", "All time"]
    )

    # Update dataframes based on date filter
    if date_option == "Last 7 days":
        filter_date = datetime.now() - timedelta(days=7)
    elif date_option == "Last 30 days":
        filter_date = datetime.now() - timedelta(days=30)
    elif date_option == "Last 90 days":
        filter_date = datetime.now() - timedelta(days=90)
    else:
        filter_date = datetime.now() - timedelta(days=365)

    filtered_sales = sales_df[sales_df['date'] >= filter_date]
    filtered_users = user_df[user_df['join_date'] >= filter_date]
    filtered_tickets = ticket_df[ticket_df['created_date'] >= filter_date]

    # Dashboard page
    if page == "Dashboard":
        st.title("📊 Dashboard Overview")

        # KPI metrics in cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Total Revenue", f"${filtered_sales['revenue'].sum():,.2f}",
                      f"{random.randint(5, 15)}% ↑")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("New Users", len(filtered_users),
                      f"{random.randint(3, 10)}% ↑")
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Active Users", int(len(user_df) * 0.7),
                      f"{random.randint(-5, 5)}% ↓")
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            open_tickets = len(filtered_tickets[filtered_tickets['status'].isin(['Open', 'In Progress'])])
            st.metric("Open Tickets", open_tickets,
                      f"{random.randint(-10, 0)}% ↓")
            st.markdown("</div>", unsafe_allow_html=True)

        # Revenue trend chart
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.subheader("Revenue Trend")

        # Aggregate daily revenue
        daily_revenue = filtered_sales.groupby('date')['revenue'].sum().reset_index()

        # Create line chart with Plotly
        fig = px.line(
            daily_revenue,
            x='date',
            y='revenue',
            title='Daily Revenue',
            labels={'date': 'Date', 'revenue': 'Revenue ($)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Second row with user and sales distribution
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("User Distribution by Country")

            country_counts = user_df['country'].value_counts().reset_index()
            country_counts.columns = ['country', 'count']

            fig = px.pie(
                country_counts,
                values='count',
                names='country',
                hole=0.4,
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("Sales by Product")

            product_sales = filtered_sales.groupby('product')['revenue'].sum().reset_index()

            fig = px.bar(
                product_sales,
                x='product',
                y='revenue',
                color='product',
                labels={'product': 'Product', 'revenue': 'Revenue ($)'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Third row with recent activities and ticket status
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("Recent Activities")

            # Create a sample activity log
            activities = [
                {"time": "Today, 10:30 AM", "description": "New user registration: John Doe"},
                {"time": "Today, 09:15 AM", "description": "Support ticket #1245 resolved"},
                {"time": "Yesterday, 4:20 PM", "description": "System update completed"},
                {"time": "Yesterday, 1:30 PM", "description": "Product C price updated"},
                {"time": "Apr 22, 11:00 AM", "description": "New feature deployed"}
            ]

            for activity in activities:
                st.write(f"**{activity['time']}**: {activity['description']}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("Ticket Status Distribution")

            status_counts = filtered_tickets['status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']

            # Custom colors for different statuses
            status_colors = {
                'Open': 'red',
                'In Progress': 'orange',
                'Resolved': 'green',
                'Closed': 'blue'
            }

            fig = px.bar(
                status_counts,
                x='status',
                y='count',
                color='status',
                color_discrete_map=status_colors,
                labels={'status': 'Status', 'count': 'Number of Tickets'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Sales Analytics page
    elif page == "Sales Analytics":
        st.title("📈 Sales Analytics")

        # Filters specific to sales
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_product = st.multiselect(
                "Select Products",
                options=sales_df['product'].unique(),
                default=sales_df['product'].unique()
            )
        with col2:
            selected_region = st.multiselect(
                "Select Regions",
                options=sales_df['region'].unique(),
                default=sales_df['region'].unique()
            )
        with col3:
            group_by = st.selectbox(
                "Group By",
                options=["Day", "Week", "Month"]
            )

        # Filter data based on selections
        filtered_data = filtered_sales[
            (filtered_sales['product'].isin(selected_product)) &
            (filtered_sales['region'].isin(selected_region))
            ]

        # Grouping data based on selection
        if group_by == "Day":
            grouped_data = filtered_data.groupby(['date', 'product'])['revenue'].sum().reset_index()
            time_col = 'date'
        elif group_by == "Week":
            filtered_data['week'] = filtered_data['date'].dt.isocalendar().week
            filtered_data['year'] = filtered_data['date'].dt.isocalendar().year
            filtered_data['week_label'] = filtered_data['year'].astype(str) + '-W' + filtered_data['week'].astype(str)
            grouped_data = filtered_data.groupby(['week_label', 'product'])['revenue'].sum().reset_index()
            time_col = 'week_label'
        else:  # Month
            filtered_data['month'] = filtered_data['date'].dt.strftime('%Y-%m')
            grouped_data = filtered_data.groupby(['month', 'product'])['revenue'].sum().reset_index()
            time_col = 'month'

        # Show total revenue
        total_revenue = filtered_data['revenue'].sum()
        avg_order = filtered_data['revenue'].mean()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Average Order Value", f"${avg_order:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        # Revenue over time chart
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.subheader(f"Revenue Over Time (Grouped by {group_by})")

        # Create line chart with Plotly
        fig = px.line(
            grouped_data,
            x=time_col,
            y='revenue',
            color='product',
            labels={time_col: group_by, 'revenue': 'Revenue ($)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Sales breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("Sales by Product")
            product_revenue = filtered_data.groupby('product')['revenue'].sum().reset_index()

            fig = px.pie(
                product_revenue,
                values='revenue',
                names='product',
                title='Revenue Distribution by Product'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("Sales by Region")
            region_revenue = filtered_data.groupby('region')['revenue'].sum().reset_index()

            fig = px.pie(
                region_revenue,
                values='revenue',
                names='region',
                title='Revenue Distribution by Region'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Sales data table
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.subheader("Detailed Sales Data")

        # Aggregate data
        agg_data = filtered_data.groupby(['product', 'region']).agg({
            'quantity': 'sum',
            'revenue': 'sum'
        }).reset_index()

        # Sort by revenue (descending)
        agg_data = agg_data.sort_values('revenue', ascending=False)

        # Format revenue column
        agg_data['revenue'] = agg_data['revenue'].apply(lambda x: f"${x:,.2f}")

        st.dataframe(agg_data, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # User Management page
    elif page == "User Management":
        st.title("👥 User Management")

        # User metrics
        total_users = len(user_df)
        active_users = len(user_df[user_df['last_login'] >= (datetime.now() - timedelta(days=30))])
        premium_users = len(user_df[user_df['subscription'].isin(['Premium', 'Enterprise'])])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Total Users", total_users)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Active Users (30d)", active_users, f"{int(active_users / total_users * 100)}%")
            st.markdown("</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Premium Users", premium_users, f"{int(premium_users / total_users * 100)}%")
            st.markdown("</div>", unsafe_allow_html=True)

        # User activity chart
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.subheader("User Growth")

        # Group users by join date
        user_df['join_month'] = user_df['join_date'].dt.strftime('%Y-%m')
        monthly_users = user_df.groupby('join_month').size().reset_index(name='count')
        monthly_users['cumulative'] = monthly_users['count'].cumsum()

        # Create dual-axis chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_users['join_month'],
            y=monthly_users['count'],
            name='New Users'
        ))
        fig.add_trace(go.Line(
            x=monthly_users['join_month'],
            y=monthly_users['cumulative'],
            name='Total Users',
            yaxis='y2'
        ))
        fig.update_layout(
            title='Monthly User Growth',
            yaxis=dict(title='New Users'),
            yaxis2=dict(title='Total Users', overlaying='y', side='right')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # User distribution
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("Subscription Distribution")

            sub_counts = user_df['subscription'].value_counts().reset_index()
            sub_counts.columns = ['subscription', 'count']

            fig = px.pie(
                sub_counts,
                values='count',
                names='subscription',
                color='subscription',
                color_discrete_map={
                    'Free': 'lightgray',
                    'Basic': 'skyblue',
                    'Premium': 'royalblue',
                    'Enterprise': 'darkblue'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("User Activity Levels")

            activity_counts = user_df['activity_level'].value_counts().reset_index()
            activity_counts.columns = ['activity_level', 'count']

            fig = px.bar(
                activity_counts,
                x='activity_level',
                y='count',
                color='activity_level',
                color_discrete_map={
                    'Low': 'lightcoral',
                    'Medium': 'orange',
                    'High': 'green'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # User table with search and filters
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.subheader("User Database")

        # Search and filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search Users", "")
        with col2:
            subscription_filter = st.multiselect(
                "Subscription Type",
                options=user_df['subscription'].unique(),
                default=[]
            )
        with col3:
            activity_filter = st.multiselect(
                "Activity Level",
                options=user_df['activity_level'].unique(),
                default=[]
            )

        # Apply filters
        filtered_user_data = user_df.copy()

        if search_term:
            mask = (filtered_user_data['name'].str.contains(search_term, case=False)) | \
                   (filtered_user_data['email'].str.contains(search_term, case=False)) | \
                   (filtered_user_data['user_id'].str.contains(search_term, case=False))
            filtered_user_data = filtered_user_data[mask]

        if subscription_filter:
            filtered_user_data = filtered_user_data[filtered_user_data['subscription'].isin(subscription_filter)]

        if activity_filter:
            filtered_user_data = filtered_user_data[filtered_user_data['activity_level'].isin(activity_filter)]

        # Display paginated results
        user_page_size = 10
        user_page_number = st.number_input("Page", min_value=1, value=1)
        start_idx = (user_page_number - 1) * user_page_size
        end_idx = start_idx + user_page_size

        display_columns = ['user_id', 'name', 'email', 'subscription', 'activity_level', 'join_date', 'last_login']
        st.dataframe(filtered_user_data[display_columns].iloc[start_idx:end_idx], use_container_width=True)

        total_pages = (len(filtered_user_data) - 1) // user_page_size + 1
        st.write(f"Showing page {user_page_number} of {total_pages} ({len(filtered_user_data)} total users)")
        st.markdown("</div>", unsafe_allow_html=True)

    # Support Tickets page
    elif page == "Support Tickets":
        st.title("🎫 Support Tickets")

        # Ticket metrics
        open_tickets = len(ticket_df[ticket_df['status'] == 'Open'])
        in_progress = len(ticket_df[ticket_df['status'] == 'In Progress'])
        resolved = len(ticket_df[ticket_df['status'] == 'Resolved'])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Open Tickets", open_tickets)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("In Progress", in_progress)
            st.markdown("</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Resolved", resolved)
            st.markdown("</div>", unsafe_allow_html=True)

        # Ticket distribution charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("Tickets by Priority")

            priority_counts = ticket_df['priority'].value_counts().reset_index()
            priority_counts.columns = ['priority', 'count']

            # Order priorities
            priority_order = {'Low': 0, 'Medium': 1, 'High': 2, 'Critical': 3}
            priority_counts['order'] = priority_counts['priority'].map(priority_order)
            priority_counts = priority_counts.sort_values('order')

            fig = px.bar(
                priority_counts,
                x='priority',
                y='count',
                color='priority',
                color_discrete_map={
                    'Low': 'green',
                    'Medium': 'blue',
                    'High': 'orange',
                    'Critical': 'red'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("Tickets by Category")

            category_counts = ticket_df['category'].value_counts().reset_index()
            category_counts.columns = ['category', 'count']

            fig = px.pie(
                category_counts,
                values='count',
                names='category'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Ticket resolution time chart
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.subheader("Resolution Time by Priority")

        # Calculate resolution time for resolved tickets
        resolved_tickets = ticket_df[ticket_df['resolved_date'].notna()].copy()
        resolved_tickets['resolution_time'] = (resolved_tickets['resolved_date'] - resolved_tickets[
            'created_date']).dt.total_seconds() / 3600  # in hours

        resolution_by_priority = resolved_tickets.groupby('priority')['resolution_time'].mean().reset_index()

        # Order priorities
        priority_order = {'Low': 0, 'Medium': 1, 'High': 2, 'Critical': 3}
        resolution_by_priority['order'] = resolution_by_priority['priority'].map(priority_order)
        resolution_by_priority = resolution_by_priority.sort_values('order')

        fig = px.bar(
            resolution_by_priority,
            x='priority',
            y='resolution_time',
            color='priority',
            color_discrete_map={

        'Low': 'green',
        'Medium': 'blue',
        'High': 'orange',
        'Critical': 'red'
        },
        labels = {'resolution_time': 'Average Resolution Time (hours)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Ticket table with search and filters
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.subheader("Ticket Management")

        # Search and filters
        col1, col2, col3 = st.columns(3)
        with col1:
            ticket_search = st.text_input("Search Tickets", "")
        with col2:
            status_filter = st.multiselect(
                "Status",
                options=ticket_df['status'].unique(),
                default=[]
            )
        with col3:
            priority_filter = st.multiselect(
                "Priority",
                options=ticket_df['priority'].unique(),
                default=[]
            )

        # Apply filters
        filtered_ticket_data = ticket_df.copy()

        if ticket_search:
            mask = (filtered_ticket_data['ticket_id'].str.contains(ticket_search, case=False)) | \
                   (filtered_ticket_data['title'].str.contains(ticket_search, case=False)) | \
                   (filtered_ticket_data['user_id'].str.contains(ticket_search, case=False))
            filtered_ticket_data = filtered_ticket_data[mask]

        if status_filter:
            filtered_ticket_data = filtered_ticket_data[filtered_ticket_data['status'].isin(status_filter)]

        if priority_filter:
            filtered_ticket_data = filtered_ticket_data[filtered_ticket_data['priority'].isin(priority_filter)]

        # Display paginated results
        ticket_page_size = 10
        ticket_page_number = st.number_input("Page", min_value=1, value=1, key="ticket_page")
        start_idx = (ticket_page_number - 1) * ticket_page_size
        end_idx = start_idx + ticket_page_size

        display_columns = ['ticket_id', 'title', 'status', 'priority', 'category', 'created_date', 'assigned_to']
        st.dataframe(filtered_ticket_data[display_columns].iloc[start_idx:end_idx], use_container_width=True)

        total_pages = (len(filtered_ticket_data) - 1) // ticket_page_size + 1
        st.write(f"Showing page {ticket_page_number} of {total_pages} ({len(filtered_ticket_data)} total tickets)")

        # Ticket detail expansion
        st.write("---")
        ticket_id = st.text_input("Enter Ticket ID to View Details")
        if ticket_id:
            ticket_data = ticket_df[ticket_df['ticket_id'] == ticket_id]
            if not ticket_data.empty:
                ticket = ticket_data.iloc[0]

                st.write(f"### Ticket: {ticket['title']}")
                st.write(f"**ID:** {ticket['ticket_id']}")
                st.write(f"**Status:** {ticket['status']}")
                st.write(f"**Priority:** {ticket['priority']}")
                st.write(f"**Category:** {ticket['category']}")
                st.write(f"**Created:** {ticket['created_date'].strftime('%Y-%m-%d %H:%M')}")
                st.write(f"**Assigned to:** {ticket['assigned_to']}")
                st.write(f"**User:** {ticket['user_id']}")

                if pd.notna(ticket['resolved_date']):
                    st.write(f"**Resolved:** {ticket['resolved_date'].strftime('%Y-%m-%d %H:%M')}")

                st.write("### Ticket Description")
                st.write(
                    "This is a placeholder for the ticket description. In a real application, this would contain the details of the user's issue or request.")

                st.write("### Activity Log")
                activities = [
                    {"time": "2 hours ago", "user": "System", "action": "Ticket priority changed from Medium to High"},
                    {"time": "3 hours ago", "user": ticket['assigned_to'],
                     "action": "Added comment: Working on this issue"},
                    {"time": "1 day ago", "user": "System", "action": f"Assigned ticket to {ticket['assigned_to']}"},
                    {"time": ticket['created_date'].strftime('%Y-%m-%d %H:%M'), "user": "System",
                     "action": "Ticket created"}
                ]

                for activity in activities:
                    st.write(f"**{activity['time']}** - {activity['user']}: {activity['action']}")

                # Status update - demo only
                new_status = st.selectbox("Update Status", options=["Open", "In Progress", "Resolved", "Closed"])
                if st.button("Update Ticket"):
                    st.success(f"Ticket {ticket_id} status updated to {new_status}")
            else:
                st.error("Ticket not found")
        st.markdown("</div>", unsafe_allow_html=True)

        # Settings page
    elif page == "Settings":
        st.title("⚙️ System Settings")

        settings_tab1, settings_tab2, settings_tab3 = st.tabs(
            ["General Settings", "User Settings", "Notification Settings"])

        with settings_tab1:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("System Configuration")

            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("Theme", ["Light", "Dark", "Auto"])
                st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
                st.selectbox("Time Zone", ["UTC", "Eastern Time", "Pacific Time", "Central European Time"])

            with col2:
                st.selectbox("Default Language", ["English", "Spanish", "French", "German"])
                st.number_input("Session Timeout (minutes)", min_value=5, max_value=120, value=30)
                st.checkbox("Enable Analytics", value=True)

            st.write("---")
            st.subheader("Data Management")

            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("Data Retention Period", ["30 days", "90 days", "1 year", "Forever"])
                st.selectbox("Backup Schedule", ["Daily", "Weekly", "Monthly"])

            with col2:
                st.text_input("Backup Location", "/data/backups")
                st.checkbox("Enable Automatic Backups", value=True)

            if st.button("Save General Settings"):
                st.success("Settings saved successfully!")
            st.markdown("</div>", unsafe_allow_html=True)

        with settings_tab2:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("User Account Settings")

            st.selectbox("Default User Role", ["Admin", "Manager", "User", "Viewer"])
            st.checkbox("Require Email Verification", value=True)
            st.checkbox("Allow Self-Registration", value=False)
            st.number_input("Maximum Login Attempts", min_value=1, max_value=10, value=5)
            st.number_input("Password Expiry (days)", min_value=30, max_value=365, value=90)

            st.write("---")
            st.subheader("Password Policy")

            st.checkbox("Require Upper and Lower Case Letters", value=True)
            st.checkbox("Require Numbers", value=True)
            st.checkbox("Require Special Characters", value=True)
            st.number_input("Minimum Password Length", min_value=8, max_value=24, value=12)

            if st.button("Save User Settings"):
                st.success("User settings saved successfully!")
            st.markdown("</div>", unsafe_allow_html=True)

        with settings_tab3:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.subheader("Notification Settings")

            st.checkbox("Email Notifications", value=True)
            st.checkbox("In-App Notifications", value=True)
            st.checkbox("SMS Notifications", value=False)

            st.write("---")
            st.subheader("Notification Events")

            col1, col2 = st.columns(2)
            with col1:
                st.checkbox("New User Registration", value=True)
                st.checkbox("Password Reset", value=True)
                st.checkbox("Failed Login Attempts", value=True)

            with col2:
                st.checkbox("System Updates", value=True)
                st.checkbox("Backup Completion", value=True)
                st.checkbox("High Priority Tickets", value=True)

            st.write("---")
            st.subheader("Email Configuration")

            col1, col2 = st.columns(2)
            with col1:
                st.text_input("SMTP Server", "smtp.example.com")
                st.text_input("SMTP Port", "587")

            with col2:
                st.text_input("Sender Email", "noreply@example.com")
                st.text_input("SMTP Password", type="password", value="password123")

            if st.button("Save Notification Settings"):
                st.success("Notification settings saved successfully!")

            if st.button("Test Email Configuration"):
                with st.spinner("Sending test email..."):
                    time.sleep(2)  # Simulate email sending
                st.success("Test email sent successfully!")
            st.markdown("</div>", unsafe_allow_html=True)

    def main():
        if check_password():
            dashboard()

    if __name__ == "__main__":
        main()