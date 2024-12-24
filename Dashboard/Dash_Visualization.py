import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class Plot:
    def __init__(self, folder):
        self.folder = folder
        self.file_mapping = {
            "User Overview Analysis": os.path.join(self.folder, "cleaned_dataset.csv"),
            "User Engagement Analysis": os.path.join(self.folder, "User_Engagment.csv"),
            "Experience Analysis": os.path.join(self.folder, "User_Exprience.csv"),
            #"Satisfaction Analysis": os.path.join(self.folder, "user_satisfaction.csv")
        }
    # User Overview Analysis Visualization
    def first_last_handsets_by_cust(self, data, column_name, n = 10):
        """
        Get the top 10 handsets by the specified group_by_columns.
        """
        self.data = data
        top_handsets = None
        # top_each_customers = None
        
        if not self.data.empty:
            # Group by Handset Type and count occurrences
            top_handsets = (
                self.data.groupby(column_name)
                .size()
                .reset_index(name="Count")
                .sort_values(by="Count", ascending=False)
                .head(n)
            )
            bottom_handsets = (
                self.data.groupby(column_name)
                .size()
                .reset_index(name="Count")
                .sort_values(by="Count", ascending=False)
                .tail(n)
            )

        return  top_handsets, bottom_handsets
    
    def top_handsets_per_top_manufacturers(self,data, manufacturer_column, handset_column, top_n_manufacturers=3, top_n_handsets=5):
        """
        Get the top N handsets for the top N manufacturers.
        """
        top_manufacturers = None
        top_handsets_per_manufacturer = None
        self.df = data
        if not self.df.empty:
            # Identify the top N manufacturers
            top_manufacturers = (
                self.df.groupby(manufacturer_column)
                .size()
                .reset_index(name="Count")
                .sort_values(by="Count", ascending=False)
                # .tolist()
            )
            top_manufacturers1 = (
                self.df.groupby(manufacturer_column)
                .size()
                .reset_index(name="Count")
                .sort_values(by="Count", ascending=False)
                .head(top_n_manufacturers)[manufacturer_column]
                .tolist()
            )

            # Filter data for the top N manufacturers
            filtered_data = self.df[self.df[manufacturer_column].isin(top_manufacturers1)]

            # Identify top N handsets for each manufacturer
            top_handsets_per_manufacturer = (
                filtered_data.groupby([manufacturer_column, handset_column])
                .size()
                .reset_index(name="Count")
                .sort_values([manufacturer_column, "Count"], ascending=[True, False])
                .groupby(manufacturer_column)
            )

        return top_manufacturers, top_handsets_per_manufacturer
    def display_dataframe_with_colors(self, data):
        """Display the dataframe with alternating row colors."""
        colors = ['#D2B48C', '#F4A460', '#FFFAF0', '#D2B48C', '#F4A460', 'teal']
        
        # Creating a custom HTML table to show the data with alternating row colors
        table_html = "<table style='width:100%; border-collapse: collapse;'>"
        table_html += "<thead><tr>"
        
        # Table header
        for col in data.columns:
            table_html += f"<th style='padding: 8px; text-align: left; background-color: teal; border: 1px solid #ddd;'>{col}</th>"
        table_html += "</tr></thead><tbody>"

        # Table body with alternating row colors
        for i, row in data.iterrows():
            row_color = colors[i % len(colors)]  # Alternate colors
            table_html += "<tr style='background-color: " + row_color + ";'>"
            
            for value in row:
                table_html += f"<td style='padding: 8px; border: 1px solid #ddd;'>{value}</td>"
            table_html += "</tr>"

        table_html += "</tbody></table>"

        # Display the table using markdown to render the HTML
        st.markdown(table_html, unsafe_allow_html=True)
        
    def load_data(self, analysis_type):
        """Load data based on the analysis type."""
        file_path = self.file_mapping.get(analysis_type)
        if file_path and os.path.exists(file_path):
            data = pd.read_csv(file_path)
            if not data.empty:
                return data
            else:
                st.error("The selected CSV file is empty.")
        else:
            st.error("CSV file not found. Please ensure the file exists in the 'data' folder.")
        return None

    def create_bar_plot(self, data, column, title):
        """Generate a bar plot for the given data with custom colors and a legend."""
        # Get the value counts of the column
        top_values = data[column].value_counts().nlargest(20)
        
        # Map the cluster values to custom names
        cluster_mapping = {0: 'Satisfied', 1: 'Unsatisfied'}
        labels = [cluster_mapping.get(label, label) for label in top_values.index]

        # Define custom colors (you can adjust these colors as needed)
        custom_colors = ['pink', 'teal']#, '#8B4513', '#A0522D', '#CD853F', '#F5DEB3', '#DEB887', '#D2691E', '#F4A460', '#A52A2A', '#C19A6B', '#B8860B']

        # Create the bar plot with alternating colors for each bar
        fig, ax = plt.subplots()
        bars = ax.bar(top_values.index, top_values.values, color=custom_colors[:len(top_values)])  # Apply custom colors
        
        # Add labels and title
        ax.set_title(title)
        ax.set_ylabel("Count")
        ax.set_xlabel(column)

        # Adding the legend
        ax.legend(bars, labels, title="Cluster", loc="best", fontsize=10)
        
        # Rotate x-axis labels for readability
        plt.xticks(rotation=45)
        
        # Display the bar plot
        st.pyplot(fig)

    def plot_histogram(self, data, column, title):
        """Generate a histogram for the given column."""
        fig, ax = plt.subplots()
        data[column].plot(kind='hist', bins=10, alpha=0.7, color='#D2B48C', ax=ax)
        ax.set_title(title)
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    def plot_scatter(self, data, x_column, y_column, title):
        """Generate a scatter plot between two columns."""
        fig, ax = plt.subplots()
        data.plot.scatter(x=x_column, y=y_column, alpha=0.7, color='orange', ax=ax)
        ax.set_title(title)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        st.pyplot(fig)

    def plot_correlation_heatmap(self, data, columns, title):
        """Generate a correlation heatmap for selected columns."""
        correlation = data[columns].corr()
        fig, ax = plt.subplots()
        sns.heatmap(correlation, annot=True, cmap='RdYlGn', ax=ax)
        ax.set_title(title)
        st.pyplot(fig)

    def plot_pie_chart(self, data, column, title):
        """Generate a pie chart for the given column."""
        # Define custom colors for the pie chart
        """Generate a pie chart for the given data."""
        # Get the value counts of the column
        value_counts = data[column].value_counts()
        labels = value_counts.index
        sizes = value_counts.values

        # Define custom colors for the pie chart
        custom_colors = ['pink', 'teal']

        # Map the cluster values to custom names
        cluster_mapping = {0: 'Satisfied', 1: 'Unsatisfied'}
        labels = [cluster_mapping.get(label, label) for label in labels]  # Apply mapping to the labels

        # Create the pie chart
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=custom_colors,  # Use the custom colors
            wedgeprops={'edgecolor': 'black'}
        )
        

        # Set the title
        ax.set_title(title)
        
        # Display the pie chart
        st.pyplot(fig)
        
    # User Experience Visualization
    @staticmethod
    def create_bar_plot(data, column, title):
        """Generate a bar plot for the given data with custom colors and a legend."""
        top_values = data[column].value_counts().nlargest(5)
        labels = top_values.index
        custom_colors = ['pink', 'teal']

        fig, ax = plt.subplots()
        bars = ax.bar(top_values.index, top_values.values, color=custom_colors[:len(top_values)]) 
        
        ax.set_title(title)
        ax.set_ylabel("Count")
        ax.set_xlabel(column)
        # Map the cluster values to custom names
        cluster_mapping = {'undefined': 'Unknown'}
        labels = [cluster_mapping.get(label, label) for label in labels] 
        
        ax.legend(bars, labels, title="Cluster", loc="best", fontsize=10)
        plt.xticks(rotation=45)

        st.pyplot(fig)

    @staticmethod
    def create_histogram(data, column, title, bins=30):
        """Generate a histogram for a numerical column in the dataset."""
        fig, ax = plt.subplots()
        ax.hist(data[column], bins=bins, color='teal', edgecolor='black')
        ax.set_title(title)
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        
        st.pyplot(fig)

    @staticmethod
    def create_scatter_plot(data, x_column, y_column, title):
        """Generate a scatter plot to compare two numerical columns."""
        fig, ax = plt.subplots()
        ax.scatter(data[x_column], data[y_column], color='skyblue', alpha=0.5)
        ax.set_title(title)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

        st.pyplot(fig)

    @staticmethod
    def create_heatmap(data, title):
        """Generate a heatmap to show correlation between numerical columns."""
        # data = data.drop(columns = ['MSISDN/Number','Most Common Handset Type'])
        # List of columns to drop
        columns_to_drop = ['MSISDN/Number', 'Most Common Handset Type']

        # Drop the columns only if they exist in the DataFrame
        data = data.drop(columns=[col for col in columns_to_drop if col in data.columns])
        correlation_matrix = data.corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='RdYlGn', ax=ax, fmt=".2f")
        ax.set_title(title)

        st.pyplot(fig)

    @staticmethod
    def create_pie_chart(data, column, title):
        """Generate a pie chart for a categorical column."""
        top_values = data[column].value_counts().head(10)
        fig, ax = plt.subplots()
        ax.pie(top_values, labels=top_values.index, autopct='%1.1f%%', startangle=90, colors=['teal', 'pink'])
        ax.set_title(title)

        st.pyplot(fig)

    @staticmethod
    def create_line_plot(data, x_column, y_column, title):
        """Generate a line plot to show trends over time."""
        fig, ax = plt.subplots()
        ax.plot(data[x_column], data[y_column], color='teal')
        ax.set_title(title)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

        st.pyplot(fig)
    
    
    # User Overview Visualization
    def plot_bar_chart(self, data, column_name1, y_column, title):
        """Generate a bar chart for two columns with a specified y-axis column."""
        self.data = data
        fig, ax = plt.subplots(figsize=(13, 10))

        # Assign unique colors for each bar
        colors = plt.cm.tab10(range(len(data)))  # Use a colormap for unique colors
        bars = ax.bar(data[column_name1], data[y_column], color=colors)

        # Annotate each bar with its value
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # Center the text horizontally
                height,  # Position the text at the top of the bar
                f'{height}',  # The value to display
                ha='center',  # Horizontal alignment
                va='bottom',  # Vertical alignment
                rotation=45,  # Rotate the text by 45 degrees
                fontsize=10  # Font size
            )

        # Customize the plot
        ax.set_title(title)
        ax.set_xlabel(column_name1)
        ax.set_ylabel("")  # Remove the y-axis label
        ax.set_yticks([])  # Remove y-axis numbers (tick labels)
        plt.xticks(rotation=45)
        if ax.get_legend() is not None:
            ax.legend().remove()

        # Display the plot in Streamlit
        st.pyplot(fig)
    # User Overview Visualization
    def plot_bar_chart1(self, data, column_name1, y_column, manufacturer_column, title):
        """Generate a bar chart with consistent colors for each manufacturer."""
        self.data = data
        fig, ax = plt.subplots(figsize=(13, 10))

        # Generate a unique color for each manufacturer
        unique_manufacturers = data[manufacturer_column].unique()
        color_map = {manufacturer: plt.cm.tab10(i % 10) for i, manufacturer in enumerate(unique_manufacturers)}

        # Plot each bar with its corresponding manufacturer color
        for idx, row in data.iterrows():
            bar = ax.bar(
                row[column_name1],  # X-value (Handset Type)
                row[y_column],      # Y-value (Count)
                color=color_map[row[manufacturer_column]],  # Consistent color for each manufacturer
                label=row[manufacturer_column]   # Use Manufacturer for the legend
            )

            # Annotate each bar with its value
            ax.text(
                bar[0].get_x() + bar[0].get_width() / 2,  # Center the text horizontally
                bar[0].get_height(),                     # Position the text at the top of the bar
                f'{int(bar[0].get_height())}',           # The value to display
                ha='center',                             # Horizontal alignment
                va='bottom',                             # Vertical alignment
                rotation=45,                             # Rotate the text by 45 degrees
                fontsize=10                              # Font size
            )

        # Customize the plot
        ax.set_title(title)
        ax.set_xlabel(column_name1)
        ax.set_ylabel("")  # Remove the y-axis label
        ax.set_yticks([])  # Remove y-axis numbers (tick labels)
        plt.xticks(rotation=45)

        # Add a legend with unique manufacturers
        handles = [plt.Line2D([0], [0], color=color_map[m], lw=4) for m in unique_manufacturers]
        ax.legend(handles, unique_manufacturers, title="Handset Manufacturer")

        # Display the plot in Streamlit
        st.pyplot(fig)
            
        