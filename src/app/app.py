import pandas as pd
import plotly.express as px
import streamlit as st
from data_loading.importing import import_data
from data_loading.processing import process_data

from data_loading.data_flow import export_data_sql,get_data_sql


st.markdown('Graphs')
st.sidebar.markdown('Graphs')


st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

age_bins = [0, 18, 25, 35, 45, 55, 65, 120]
age_labels = ['-18','18-25','25-32','32-45','45-55','55-65','65+']
PAllET = px.colors.qualitative.Plotly



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
 
    col1, col2 = st.columns(2)
    col1.metric("💰 Total Revenue", f"$ {total_revenue:,.2f}")
    col2.metric("📦 Sold Products", f"{total_qtd:,.0f}")

    col3,col4,col5 = st.columns(3)
    col3.metric("👥 Unique Clients", f"{unique_clients:,.0f}")
    col4.metric("🧾 Mean Ticket", f"R$ {mean_ticket:,.2f}")
    col5.metric("🏷️ Mean Price", f"R$ {mean_price:,.2f}")


def ghp_revenue_time(df: pd.DataFrame, granunality: str = "date"):

    cat1 = st.selectbox('Color Revenue By: ',['age_range','product_name','category'])

    if st.checkbox(cat1):
        revenue = df.groupby([granunality,cat1], as_index=False)["revenue"].sum()
        fig = px.line(
            revenue,
            x=granunality,
            y="revenue",
            color=cat1,
            markers=True,
            title="Revenue Along the time",
            labels={"revenue": "Revenue ($)", granunality: f"Period: {granunality}"},
            color_discrete_sequence=PAllET,
        )
        fig.update_layout(hovermode="x unified")

    else:
        revenue = df.groupby(granunality, as_index=False)["revenue"].sum()
        fig = px.line(
            revenue,
            x=granunality,
            y="revenue",
            markers=True,
            title="Revenue Along the time",
            labels={"revenue": "Revenue ($)", granunality: f"Period: {granunality}"},
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


def ghp_seazonality(df: pd.DataFrame,time):
    days_dict = {
        "Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday",
        "Thursday": "Thursday", "Friday": "Friday", "Saturday": "Saturday", "Sunday": "Sunday",
    }

    df = df.groupby(['weekday',time])['revenue'].sum().reset_index()

    pivot = df.pivot_table(
        index="weekday", columns=time, values="revenue", aggfunc="sum", fill_value=0
    ).reindex(days_dict)
 
    fig = px.imshow(
        pivot,
        aspect="auto",
        title="Seasonality of Sales by time",
        labels=dict(x=f'{time}', y="Week Day", color="Revenue $"),
        color_continuous_scale="magma",
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
        size_max=15,
        hover_name="client_id",
        opacity=0.65,
        title="Recency x Frequency Per Buy for Client",
        labels={"recency": "Days since last Buy ", "frequency": "Nº Buy"},
        color_continuous_scale="Reds",
    )

    return fig


def ghp_qtd_per_category_time(df: pd.DataFrame, granularity: str = "month"):


    cat2 = st.selectbox('Color Quantity By: ' ,['category','product_name','age_range'])

    if st.checkbox(cat2):

        agg = df.groupby([granularity,cat2], as_index=False)["quantity"].sum()
        fig = px.area(
                agg,
                x=granularity,
                y="quantity",
                color = cat2,
                title="Quantity sold along the time",
                labels={"quantity": "Quantity", granularity: f"Period: {granularity}"},
                color_discrete_sequence=PAllET,
            )
    

    else:

        agg = df.groupby(granularity, as_index=False)["quantity"].sum()

        fig = px.area(
            agg,
            x=granularity,
            y="quantity",
            title="Quantity sold along the time",
            labels={"quantity": "Quantity", granularity: f"Period: {granularity}"},
            color_discrete_sequence=PAllET,
        )


    return fig


def main():
    st.title("📊 Sales Dashboard")

    data_imported = import_data('csv','sales4.csv')
    data_preproccessed = process_data(data_imported)

    data_preproccessed = export_data_sql('csv','sales4.csv')
    data_preproccessed = get_data_sql()

    print(data_preproccessed.head())
    data_preproccessed = load_data(data_preproccessed)
    #process:

    print(data_preproccessed.head())

    df = apply_filters(data_preproccessed)
    
 
    if df.empty:
        st.warning("None Filter for selected data.")
        return
 
    show_kpis(df)
    st.divider()
 
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 General", "🛒 Products", "👥 Clients", "🕒 Seasonality"]
    )
 
    
    with tab1:
        granularity = st.selectbox(
            "Group revenue by:", ["date", "week", "month"]
        )
        st.plotly_chart(ghp_revenue_time(df, granularity), use_container_width=True)


        granularity2 = st.selectbox(
                    "Group quantity by:", ["date", "week", "month"]
                )
        st.plotly_chart(ghp_qtd_per_category_time(df, granularity2), use_container_width=True)
 
    
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
 
        st.plotly_chart(ghp_frequency_sale(df), use_container_width=True)
 
  
    with tab4:
        time = st.selectbox(
                            "Select Period:", ["month", "Year", "hour"]
                        )

        st.plotly_chart(ghp_seazonality(df,time), use_container_width=True)



        data = pd.DataFrame({
                'datetime': df['month'],
                'series': df['revenue']
            })
        data = data.set_index('datetime')

        import matplotlib.pyplot as plt
        from statsmodels.graphics.tsaplots import plot_acf,plot_pacf

        fig1,ax1 = plt.subplots()
        ax1.plot(data,color='red',label='data')
        st.pyplot(fig1)

        #ar,ma,armax
        fig2,ax2 = plt.subplots()
        plot_acf(data,lags=20,alpha=0.05,ax=ax2)
        st.pyplot(fig2)

        fig3,ax3 = plt.subplots()
        plot_pacf(data,lags=20,alpha=0.05,ax=ax3)
        st.pyplot(fig3)
 
if __name__ == "__main__":
    main()