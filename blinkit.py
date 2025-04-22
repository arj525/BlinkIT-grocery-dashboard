# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import seaborn as sns
# import matplotlib.pyplot as plt
# import os

# # Load Excel
# df = pd.read_excel("BlinkIT Grocery Data Excel.xlsx")

# # Prepare output directory
# output_dir = "all_graphs_output"
# os.makedirs(output_dir, exist_ok=True)

# # Rename for consistency
# df = df.rename(columns={
#     "Item Type": "Category",
#     "Total Sales": "Sales",
#     "Rating": "Orders",  # Temporary mapping for demo
#     "Item Identifier": "Product",
#     "Outlet Location Type": "Region"
# })

# # Drop NA
# df = df.dropna()

# # Define color palette
# COLOR_PALETTE = px.colors.qualitative.Set2

# # 1. Bar Chart – Total Sales per Product Category
# fig = px.bar(
#     df.groupby("Category")["Sales"].sum().reset_index(),
#     x="Category", y="Sales", title="Total Sales per Product Category",
#     color_discrete_sequence=COLOR_PALETTE
# )
# fig.update_layout(
#     xaxis_tickangle=-45,
#     title_font=dict(size=20, family="Arial", color="black"),
#     xaxis_title="Category",
#     yaxis_title="Total Sales",
#     paper_bgcolor="#F9F9F9",
#     plot_bgcolor="#F9F9F9"
# )
# fig.write_image(f"{output_dir}/bar_sales_per_category.png")

# # 2. Pie Chart – Order Share by Category
# fig = px.pie(
#     df.groupby("Category")["Orders"].sum().reset_index(),
#     names="Category", values="Orders", title="Order Share by Category",
#     color_discrete_sequence=COLOR_PALETTE
# )
# fig.update_layout(
#     title_font=dict(size=20, family="Arial", color="black"),
#     paper_bgcolor="#F9F9F9"
# )
# fig.write_image(f"{output_dir}/pie_orders_by_category.png")

# # 3. Line Chart – Average Sales Over Category (simulated time trend)
# fig = px.line(
#     df.groupby("Category")["Sales"].mean().reset_index(),
#     x="Category", y="Sales", title="Average Sales by Category",
#     color_discrete_sequence=COLOR_PALETTE
# )
# fig.update_layout(
#     title_font=dict(size=20, family="Arial", color="black"),
#     xaxis_title="Category",
#     yaxis_title="Average Sales",
#     paper_bgcolor="#F9F9F9",
#     plot_bgcolor="#F9F9F9"
# )
# fig.write_image(f"{output_dir}/line_sales_category.png")

# # 4. Scatter Plot – Orders vs. Sales
# fig = px.scatter(
#     df, x="Orders", y="Sales", color="Category",
#     title="Orders vs. Sales", color_discrete_sequence=COLOR_PALETTE,
#     size="Sales", hover_data=["Category"]
# )
# fig.update_layout(
#     title_font=dict(size=20, family="Arial", color="black"),
#     xaxis_title="Orders",
#     yaxis_title="Sales",
#     paper_bgcolor="#F9F9F9",
#     plot_bgcolor="#F9F9F9"
# )
# fig.write_image(f"{output_dir}/scatter_orders_vs_sales.png")

# # 5. Histogram – Sales per Product
# fig = px.histogram(
#     df, x="Sales", nbins=30, title="Distribution of Sales per Product",
#     color_discrete_sequence=COLOR_PALETTE
# )
# fig.update_layout(
#     title_font=dict(size=20, family="Arial", color="black"),
#     xaxis_title="Sales",
#     yaxis_title="Frequency",
#     paper_bgcolor="#F9F9F9",
#     plot_bgcolor="#F9F9F9"
# )
# fig.write_image(f"{output_dir}/histogram_sales.png")

# # 6. Box Plot – Sales by Category
# fig = px.box(
#     df, x="Category", y="Sales", title="Sales Distribution by Category",
#     color="Category", color_discrete_sequence=COLOR_PALETTE
# )
# fig.update_layout(
#     title_font=dict(size=20, family="Arial", color="black"),
#     xaxis_title="Category",
#     yaxis_title="Sales",
#     paper_bgcolor="#F9F9F9",
#     plot_bgcolor="#F9F9F9"
# )
# fig.write_image(f"{output_dir}/boxplot_sales_category.png")

# # 7. Stacked Bar – Orders by Region and Category
# pivot_df = df.groupby(["Region", "Category"])["Orders"].sum().reset_index()
# fig = px.bar(
#     pivot_df, x="Region", y="Orders", color="Category",
#     title="Orders by Region and Category", barmode="stack",
#     color_discrete_sequence=COLOR_PALETTE
# )
# fig.update_layout(
#     title_font=dict(size=20, family="Arial", color="black"),
#     xaxis_title="Region",
#     yaxis_title="Orders",
#     paper_bgcolor="#F9F9F9",
#     plot_bgcolor="#F9F9F9"
# )
# fig.write_image(f"{output_dir}/stackedbar_orders_region_category.png")

# # 8. Heatmap – Correlation
# corr = df[["Sales", "Orders", "Item Weight", "Item Visibility"]].corr()
# sns.heatmap(corr, annot=True, cmap="coolwarm")
# plt.title("Heatmap – Correlation", fontsize=16)
# plt.savefig(f"{output_dir}/heatmap_correlation.png")
# plt.clf()

# # 9. Donut Chart – Top 5 Best-Selling Products
# top_products = df.groupby("Product")["Sales"].sum().nlargest(5).reset_index()
# fig = px.pie(
#     top_products, names="Product", values="Sales", hole=0.4,
#     title="Top 5 Best-Selling Products", color_discrete_sequence=COLOR_PALETTE
# )
# fig.update_layout(
#     title_font=dict(size=20, family="Arial", color="black"),
#     paper_bgcolor="#F9F9F9"
# )
# fig.write_image(f"{output_dir}/donut_top5_products.png")

# # 10. Area Chart – Simulated Time Series using Rating
# fig = px.area(
#     df.sort_values("Orders"), x="Orders", y="Sales",
#     title="Area Chart – Sales over Orders (Simulated)",
#     color_discrete_sequence=COLOR_PALETTE
# )
# fig.update_layout(
#     title_font=dict(size=20, family="Arial", color="black"),
#     xaxis_title="Orders",
#     yaxis_title="Sales",
#     paper_bgcolor="#F9F9F9",
#     plot_bgcolor="#F9F9F9"
# )
# fig.write_image(f"{output_dir}/area_sales_orders.png")

# print("✅ All graphs have been generated and saved in the 'all_graphs_output' folder!")
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load Excel
df = pd.read_excel("BlinkIT Grocery Data Excel.xlsx")

# Prepare output directory
output_dir = "all_graphs_output"
os.makedirs(output_dir, exist_ok=True)

# Rename for consistency
df = df.rename(columns={
    "Item Type": "Category",
    "Total Sales": "Sales",
    "Rating": "Orders",  # Temporary mapping for demo
    "Item Identifier": "Product",
    "Outlet Location Type": "Region"
})

# Drop NA
df = df.dropna()

# Define a dark theme color palette
COLOR_PALETTE = px.colors.qualitative.Dark24

# 1. Bar Chart – Total Sales per Product Category
fig = px.bar(
    df.groupby("Category")["Sales"].sum().reset_index(),
    x="Category", y="Sales", title="Total Sales per Product Category",
    color_discrete_sequence=COLOR_PALETTE
)
fig.update_layout(
    xaxis_tickangle=-45,
    title_font=dict(size=20, family="Arial", color="#FFFFFF"),
    xaxis_title="Category",
    yaxis_title="Total Sales",
    paper_bgcolor="#1E1E2F",
    plot_bgcolor="#2A2A3D",
    font=dict(color="#FFFFFF")
)
fig.write_image(f"{output_dir}/bar_sales_per_category.png")

# 2. Pie Chart – Order Share by Category
fig = px.pie(
    df.groupby("Category")["Orders"].sum().reset_index(),
    names="Category", values="Orders", title="Order Share by Category",
    color_discrete_sequence=COLOR_PALETTE
)
fig.update_layout(
    title_font=dict(size=20, family="Arial", color="#FFFFFF"),
    paper_bgcolor="#1E1E2F",
    font=dict(color="#FFFFFF")
)
fig.write_image(f"{output_dir}/pie_orders_by_category.png")

# 3. Line Chart – Average Sales Over Category (simulated time trend)
fig = px.line(
    df.groupby("Category")["Sales"].mean().reset_index(),
    x="Category", y="Sales", title="Average Sales by Category",
    color_discrete_sequence=COLOR_PALETTE
)
fig.update_layout(
    title_font=dict(size=20, family="Arial", color="#FFFFFF"),
    xaxis_title="Category",
    yaxis_title="Average Sales",
    paper_bgcolor="#1E1E2F",
    plot_bgcolor="#2A2A3D",
    font=dict(color="#FFFFFF")
)
fig.write_image(f"{output_dir}/line_sales_category.png")

# 4. Scatter Plot – Orders vs. Sales
fig = px.scatter(
    df, x="Orders", y="Sales", color="Category",
    title="Orders vs. Sales", color_discrete_sequence=COLOR_PALETTE,
    size="Sales", hover_data=["Category"]
)
fig.update_layout(
    title_font=dict(size=20, family="Arial", color="#FFFFFF"),
    xaxis_title="Orders",
    yaxis_title="Sales",
    paper_bgcolor="#1E1E2F",
    plot_bgcolor="#2A2A3D",
    font=dict(color="#FFFFFF")
)
fig.write_image(f"{output_dir}/scatter_orders_vs_sales.png")

# 5. Histogram – Sales per Product
fig = px.histogram(
    df, x="Sales", nbins=30, title="Distribution of Sales per Product",
    color_discrete_sequence=COLOR_PALETTE
)
fig.update_layout(
    title_font=dict(size=20, family="Arial", color="#FFFFFF"),
    xaxis_title="Sales",
    yaxis_title="Frequency",
    paper_bgcolor="#1E1E2F",
    plot_bgcolor="#2A2A3D",
    font=dict(color="#FFFFFF")
)
fig.write_image(f"{output_dir}/histogram_sales.png")

# 6. Box Plot – Sales by Category
fig = px.box(
    df, x="Category", y="Sales", title="Sales Distribution by Category",
    color="Category", color_discrete_sequence=COLOR_PALETTE
)
fig.update_layout(
    title_font=dict(size=20, family="Arial", color="#FFFFFF"),
    xaxis_title="Category",
    yaxis_title="Sales",
    paper_bgcolor="#1E1E2F",
    plot_bgcolor="#2A2A3D",
    font=dict(color="#FFFFFF")
)
fig.write_image(f"{output_dir}/boxplot_sales_category.png")

# 7. Stacked Bar – Orders by Region and Category
pivot_df = df.groupby(["Region", "Category"])["Orders"].sum().reset_index()
fig = px.bar(
    pivot_df, x="Region", y="Orders", color="Category",
    title="Orders by Region and Category", barmode="stack",
    color_discrete_sequence=COLOR_PALETTE
)
fig.update_layout(
    title_font=dict(size=20, family="Arial", color="#FFFFFF"),
    xaxis_title="Region",
    yaxis_title="Orders",
    paper_bgcolor="#1E1E2F",
    plot_bgcolor="#2A2A3D",
    font=dict(color="#FFFFFF")
)
fig.write_image(f"{output_dir}/stackedbar_orders_region_category.png")

# 8. Heatmap – Correlation
corr = df[["Sales", "Orders"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Heatmap – Correlation", fontsize=16, color="#FFFFFF")
plt.savefig(f"{output_dir}/heatmap_correlation.png", facecolor="#1E1E2F")
plt.clf()

# 9. Donut Chart – Top 5 Best-Selling Products
top_products = df.groupby("Product")["Sales"].sum().nlargest(5).reset_index()
fig = px.pie(
    top_products, names="Product", values="Sales", hole=0.4,
    title="Top 5 Best-Selling Products", color_discrete_sequence=COLOR_PALETTE
)
fig.update_layout(
    title_font=dict(size=20, family="Arial", color="#FFFFFF"),
    paper_bgcolor="#1E1E2F",
    font=dict(color="#FFFFFF")
)
fig.write_image(f"{output_dir}/donut_top5_products.png")

# 10. Area Chart – Simulated Time Series using Rating
fig = px.area(
    df.sort_values("Orders"), x="Orders", y="Sales",
    title="Area Chart – Sales over Orders (Simulated)",
    color_discrete_sequence=COLOR_PALETTE
)
fig.update_layout(
    title_font=dict(size=20, family="Arial", color="#FFFFFF"),
    xaxis_title="Orders",
    yaxis_title="Sales",
    paper_bgcolor="#1E1E2F",
    plot_bgcolor="#2A2A3D",
    font=dict(color="#FFFFFF")
)
fig.write_image(f"{output_dir}/area_sales_orders.png")

print("✅ All graphs have been generated and saved in the 'all_graphs_output' folder!")