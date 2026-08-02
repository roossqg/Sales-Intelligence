import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
import streamlit as st
from data_loading.importing import import_data
from data_loading.processing import process_data

matplotlib.use('QtAgg')


st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
)


age_bins = [0, 18, 25, 35, 45, 55, 65, 120]
age_labels = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
PAllET = px.colors.qualitative.Set2

@st.cache_data
def load_data(data) -> pd.DataFrame:
    df = data
 
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["revenue"] = df["price"] * df["quantity"]
 
    df["date"] = df["datetime"].dt.date
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.to_period("M").astype(str)
    df["week"] = df["datetime"].dt.to_period("W").astype(str)
    df["weekday"] = df["datetime"].dt.day_name()
    df["hour"] = df["datetime"].dt.hour
 
    return df

 
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("🔍 Filters")
 
    data_min, data_max = df["datetime"].min(), df["datetime"].max()
    interval = st.sidebar.date_input(
        "Period",
        value=(data_min.date(), data_max.date()),
        min_value=data_min.date(),
        max_value=data_max.date(),
    )
    if len(interval) == 2:
        start, end = interval
        df = df[(df["date"] >= start) & (df["date"] <= end)]
 
    categories = st.sidebar.multiselect(
        "Category",
        options=sorted(df["category"].dropna().unique()),
        default=None,
    )
    if categories:
        df = df[df["category"].isin(categories)]
 
    products = st.sidebar.multiselect(
        "Product",
        options=sorted(df["product_name"].dropna().unique()),
        default=None,
    )
    if products:
        df = df[df["product_name"].isin(products)]
 
    age_range_sel = st.sidebar.multiselect(
        "age_range",
        options=age_labels,
        default=None,
    )
    if age_range_sel:
        df = df[df["age_range"].isin(age_range_sel)]
 
    return df


def show_kpis(df: pd.DataFrame):
    total_revenue = df["revenue"].sum()
    total_qtd = df["quantity"].sum()
    mean_ticket = df["revenue"].sum() / df["client_id"].nunique() if df["client_id"].nunique() else 0
    unique_clients = df["client_id"].nunique()
    mean_price = df["price"].mean()
 
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("💰 Total Revenue", f"R$ {total_revenue:,.2f}")
    col2.metric("📦 Sold Products", f"{total_qtd:,.0f}")
    col3.metric("👥 Unique Clients", f"{unique_clients:,.0f}")
    col4.metric("🧾 Mean Ticket (ATV)", f"R$ {mean_ticket:,.2f}")
    col5.metric("🏷️ Mean Price", f"R$ {mean_price:,.2f}")


def ghp_revenue_time(df: pd.DataFrame, granunality: str = "date"):
    revenue = df.groupby(granunality, as_index=False)["revenue"].sum()
    fig = px.line(
        revenue,
        x=granunality,
        y="revenue",
        markers=True,
        title="Revenue Along the time",
        labels={"revenue": "Revenue ($)", granunality: "Period"},
        color_discrete_sequence=PAllET,
    )
    fig.update_layout(hovermode="x unified")
    return fig


def ghp_top_products(df: pd.DataFrame, top_n: int = 10):
    top = (
        df.groupby("product_name", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(top_n)
    )
    fig = px.bar(
        top,
        x="revenue",
        y="product_name",
        orientation="h",
        title=f"Top {top_n} Products per Revenue",
        labels={"revenue": "Revenue $", "product_name": "Product"},
        color="revenue",
        color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def ghp_participation_per_category(df: pd.DataFrame):
    cat = df.groupby("category", as_index=False)["revenue"].sum()
    fig = px.pie(
        cat,
        names="category",
        values="revenue",
        title="Paticipation per category",
        hole=0.4,
        color_discrete_sequence=PAllET,
    )
    fig.update_traces(textinfo="percent+label")
    return fig


def ghp_dist_clients_by_age(df: pd.DataFrame):
    dist = df.drop_duplicates("client_id").groupby("age_range", as_index=False).size()
    fig = px.bar(
        dist,
        x="age_range",
        y="size",
        title="Distribuition of clients by age",
        labels={"size": "N clients", "age_range": "Age Range"},
        color_discrete_sequence=PAllET,
        )
    return fig


def ghp_seazonality(df: pd.DataFrame):
    days_dict = {
        "Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday",
        "Thursday": "Thursday", "Friday": "Friday", "Saturday": "Saturday", "Sunday": "Sunday",
    }
    pivot = df.pivot_table(
        index="weekday", columns="hour", values="revenue", aggfunc="sum", fill_value=0
    ).reindex(days_dict)
 
    fig = px.imshow(
        pivot,
        aspect="auto",
        title="Seasonality of Sales by time",
        labels=dict(x="Hour", y="Week Day", color="Revenue $"),
        color_continuous_scale="Sunsetdark",
    )
    return fig


def ghp_top_clients(df: pd.DataFrame, top_n: int = 10):
    top = (
        df.groupby("client_id", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(top_n)
    )
    top["client_id"] = top["client_id"].astype(str)
    fig = px.bar(
        top,
        x="client_id",
        y="revenue",
        title=f"Top {top_n} clients revenue",
        labels={"revenue": "Revenue $", "client_id": "Client"},
        color="revenue",
        color_continuous_scale="Greens",
    )
    return fig


def ghp_frequency_sale(df: pd.DataFrame):
   
    data_ref = df["datetime"].max()
    rfm = df.groupby("client_id").agg(
        recency=("datetime", lambda x: (data_ref - x.max()).days),
        frequency=("datetime", "count"),
        monetary=("revenue", "sum"),
    ).reset_index()
 
    fig = px.scatter(
        rfm,
        x="recency",
        y="frequency",
        size="monetary",
        color="monetary",
        hover_name="client_id",
        title="Recency x Frequency Per Buy for Client",
        labels={"recency": "Days since last Buy ", "frequency": "Nº Buy"},
        color_continuous_scale="Purples",
    )

    return fig
# -> prb of sales in month (poisson)

def ghp_qtd_per_category_time(df: pd.DataFrame, granularity: str = "month"):
    agg = df.groupby(granularity, as_index=False)["quantity"].sum()
    fig = px.line(
        agg,
        x=granularity,
        y="quantity",
        title="Quantity sold along the time",
        labels={"quantity": "Quantity", granularity: "Period"},
        color_discrete_sequence=PAllET,
    )
    return fig


def main():
    st.title("📊 Sales Dashboard")

    data_imported = import_data('csv','sales.csv')
    data_preproccessed = process_data(data_imported)
    print(data_preproccessed.columns)
    data_datetime = load_data(data_preproccessed)
    
    df = apply_filters(data_datetime)
    
 
    if df.empty:
        st.warning("None Filter for selected data.")
        return
 
    show_kpis(df)
    st.divider()
 
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 General", "🛒 Products & Categories", "👥 Clients", "🕒 Seazonality"]
    )
 
    
    with tab1:
        granularity = st.radio(
            "Group revenue by:", ["date", "week", "month"], horizontal=True, index=2
        )
        st.plotly_chart(ghp_revenue_time(df, granularity), use_container_width=True)
        st.plotly_chart(ghp_qtd_per_category_time(df, "month"), use_container_width=True)
 
    
    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            top_n = st.slider("How products show?", 5, 20, 10)
            st.plotly_chart(ghp_top_products(df, top_n), use_container_width=True)
        with col_b:
            st.plotly_chart(ghp_participation_per_category(df), use_container_width=True)
 
    
    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(ghp_dist_clients_by_age(df), use_container_width=True)
 
        top_n_clientes = st.slider("How clients show?", 5, 20, 10)
        st.plotly_chart(ghp_top_clients(df, top_n_clientes), use_container_width=True)
        st.plotly_chart(ghp_frequency_sale(df), use_container_width=True)
 
  
    with tab4:
        st.plotly_chart(ghp_seazonality(df), use_container_width=True)
 
 
if __name__ == "__main__":
    main()