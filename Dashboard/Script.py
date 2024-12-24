import streamlit as st
import os
from Dash_Visualization import Plot

# Set up the data folder
data_folder = os.path.join(os.path.dirname(__file__), "data")
# Instantiate the Plot class
plot = Plot(data_folder)

# # Load and apply the external CSS file
# def load_css():
#     with open("styles.css") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# # Apply the CSS to the app
# load_css()

# Custom header for the app
st.markdown(
    """<div style="background-color: #6F4E37; padding: 10px; border-radius: 5px;">
        <h2 style="color: white;">User Data Analysis</h2>
    </div>""",
    unsafe_allow_html=True
)

# Sidebar menu
menu = st.sidebar.selectbox(
    "Select Analysis",
    ["User Overview Analysis", "User Engagement Analysis", "Experience Analysis", "Satisfaction Analysis"]
)

visualization_menu = st.sidebar.selectbox(
    "Select Visualization Type",
    ["Bar Plot", "Histogram", "Scatter Plot", "Correlation Heatmap", "Pie Chart"]#, 'Line Chart']
)

# Load and visualize data when user clicks the button
if st.sidebar.button("Visualize"):
    # Load data using the Plot class
    data = plot.load_data(menu)
    
    if data is not None:
        st.write("### Top Five Data From Loaded!")
        # Display the dataframe with alternating row colors
        if menu == "User Overview Analysis":
            st.write("")
        else:
            plot.display_dataframe_with_colors(data.head())

        # Visualization logic for each analysis type
        if menu == "User Overview Analysis":
            # plot.create_bar_plot(data, "Bearer Id", "Top 20 User Overview Values")
            top_10, last_10  = plot.first_last_handsets_by_cust(data,"Handset Type", 10)
            top_manufacturers, top_handsets_per_manufacturer = plot.top_handsets_per_top_manufacturers(data,
                manufacturer_column="Handset Manufacturer",
                handset_column="Handset Type",
                top_n_manufacturers=3,
                top_n_handsets=5
                )
            if visualization_menu == "Bar Plot":
                # Streamlit layout with two columns
                col1, col2 = st.columns(2)

                # with col1:
                plot.plot_bar_chart(top_10, "Handset Type", "Count", "Top Handset Type vs Customer Count")  
                # with col2:
                plot.plot_bar_chart(last_10, "Handset Type", "Count", "Bottom Handset Type vs Customer Count")
                # with col1:
                plot.plot_bar_chart(top_manufacturers.head(3), "Handset Manufacturer", "Count", "Top Handset Type vs Customer Count")  
                # with col2:
                plot.plot_bar_chart1(top_handsets_per_manufacturer.head(5), "Handset Type", "Count","Handset Manufacturer", "Bottom Handset Type vs Customer Count")                
            elif visualization_menu == "Histogram":
                st.error("Histogram Plot not applicable for this analysis.")
                # plot.plot_histogram(top_manufacturers, "Handset Manufacturer", "Handset Manufacturer Distribution")
            elif visualization_menu == "Scatter Plot":
                st.error("Scatter Plot not applicable for this analysis.")
            elif visualization_menu == "Correlation Heatmap":
                st.error("Correlation Heatmap not applicable for this analysis.")
            elif visualization_menu == "Pie Chart":
                plot.plot_pie_chart(top_manufacturers.head(10), "Handset Manufacturer", "Proportion of Handset Type")

        elif menu == "User Engagement Analysis":
            if visualization_menu == "Bar Plot":
                plot.create_bar_plot(data, 'Youtube Traffic', "Youtube Traffic Distribution")
            elif visualization_menu == "Histogram":
                plot.create_histogram(data, 'Gaming Traffic', "Gaming Traffic Distribution")
            elif visualization_menu == "Scatter Plot":
                plot.create_scatter_plot(data, 'Youtube Traffic', 'Netflix Traffic', "Youtube vs Netflix Traffic")
            elif visualization_menu == "Correlation Heatmap":
                plot.create_heatmap(data, "Traffic Correlation Heatmap")
            elif visualization_menu == "Pie Chart":
                plot.create_pie_chart(data, 'Youtube Traffic', "Top 10 customer Distribution of Traffic Types")
            elif visualization_menu == "Line Chart":
                plot.create_line_plot(data, 'MSISDN/Number', 'Gaming Traffic', "Gaming Traffic Over MSISDN")

        elif menu == "Experience Analysis":
            if visualization_menu == "Bar Plot":
                # Bar Plot Example
                plot.create_bar_plot(data, 'Most Common Handset Type', "Top 5 Handsets")
                # plot.create_bar_plot_EX(data, "Average UL Throughput", "Top 20 Experience Levels")
            elif visualization_menu == "Histogram":
                plot.create_histogram(data, 'TCP DL Retrans. Vol (Bytes)', "Distribution of TCP DL Retrans. Vol")
                plot.create_histogram(data, 'TCP UL Retrans. Vol (Bytes)', "Distribution of TCP UL Retrans. Vol")
                plot.create_histogram(data, 'Average DL RTT', "Distribution of Average DL RTT")
                plot.create_histogram(data, 'Average UL RTT', "Distribution of Average UL RTTl")
                plot.create_histogram(data, 'Average DL Throughput', "Distribution of Average DL Throughput")
                plot.create_histogram(data, 'Average UL Throughput', "Distribution of Average UL Throughput")
            elif visualization_menu == "Scatter Plot":
                plot.create_scatter_plot(data, 'Average DL RTT', 'Average UL RTT', "DL vs UL RTT")
                plot.create_scatter_plot(data, "TCP UL Retrans. Vol (Bytes)", "TCP DL Retrans. Vol (Bytes)", "UL vs DL Retransmission")
                plot.create_scatter_plot(data, "Average UL Throughput", "Average DL Throughput", "UL vs DL Throughput")
            elif visualization_menu == "Correlation Heatmap":
                plot.create_heatmap(data, "Correlation Heatmap")
            elif visualization_menu == "Pie Chart":
                plot.create_pie_chart(data, 'Most Common Handset Type', "Top 10 Handset Type Distribution")
            elif visualization_menu == "Box Plot":
                plot.create_box_plot(data, 'Average DL RTT', "Average DL RTT by Handset Type")

        elif menu == "Satisfaction Analysis":
            if visualization_menu == "Bar Plot":
                plot.create_bar_plot(data, "cluster", "Segmentation of User base on Satisfaction")
            elif visualization_menu == "Histogram":
                plot.plot_histogram(data, "satisfaction_score", "Satisfaction Score Distribution")
            elif visualization_menu == "Scatter Plot":
                plot.plot_scatter(data, "engagement_score", "satisfaction_score", "Engagement vs Satisfaction Score")
                plot.plot_scatter(data, "experience_score", "satisfaction_score", "Experience vs Satisfaction Score")
            elif visualization_menu == "Correlation Heatmap":
                plot.plot_correlation_heatmap(data, ["engagement_score", "experience_score", "satisfaction_score"], "Correlation Heatmap")
            elif visualization_menu == "Pie Chart":
                plot.plot_pie_chart(data, "cluster", "Proportion of Users by Cluster")