import pandas as pd
import matplotlib.pyplot as plt


# Define data loader class
class visualize:
    def __init__(self, dataframe):
        """
        Initialize the Plot class with a dataframe.
        """
        self.dataframe = dataframe

    def distribution_of_missing_values(self, column_names):
        """
        Plot the distribution of missing values for the specified columns.
        """
        # Check for missing values in the specified columns
        null_columns = self.dataframe[column_names]
        constant_values = (null_columns.isnull().sum())

        # Calculate percentages
        total = constant_values.sum()
        percentages = (constant_values / total) * 100 if total > 0 else [0] * len(constant_values)

        # Bar plot for constant/zero values
        ax = constant_values.plot(kind='barh', figsize=(10, 8), color='orange')

        # Add number and percentage annotations
        for bar, percentage in zip(ax.patches, percentages):
            width = bar.get_width()
            y = bar.get_y() + bar.get_height() / 2
            annotation = f'{int(width)} ({percentage:.2f}%)'
            ax.annotate(annotation, xy=(width, y), xytext=(5, 0),
                        textcoords="offset points", ha='left', va='center')

        # Add labels and title
        plt.title("Distribution of Missing Values Per Column")
        plt.xlabel("Frequency")
        plt.ylabel("Columns")
        plt.xticks(rotation=45)
        plt.show()

    def outlier_detection(self):
        # Select only numeric columns
        numeric_data = self.dataframe.select_dtypes(include=['number'])

        # Check if there are numeric columns
        num_columns = len(numeric_data.columns)
        if num_columns < 10:
            print("The dataset has fewer than 10 numeric columns.")
        else:
            def plot_histograms_in_grid(group, title, cols=3):
                """Plots histograms for a group of columns in a grid layout."""
                rows = (len(group.columns) + cols - 1) // cols  # Calculate number of rows needed
                fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))
                axes = axes.flatten()  # Flatten axes for easier indexing

                for i, column in enumerate(group.columns):
                    group[column].hist(ax=axes[i], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
                    
                    # Add vertical lines for mean and median
                    mean_val = group[column].mean()
                    median_val = group[column].median()
                    
                    axes[i].axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
                    axes[i].axvline(median_val, color='green', linestyle='-.', linewidth=1.5, label=f'Median: {median_val:.2f}')
                    
                    # Add title and legend
                    axes[i].set_title(f'Histogram of {column}', fontsize=12)
                    axes[i].set_xlabel(column, fontsize=10)
                    axes[i].set_ylabel('Frequency', fontsize=10)
                    axes[i].legend(fontsize=9)

                # Hide unused subplots
                for j in range(i + 1, len(axes)):
                    fig.delaxes(axes[j])
                
                fig.suptitle(title, fontsize=16, y=1.02)
                plt.tight_layout()
                plt.show()

            # Group and plot histograms for the first 55 numeric columns in groups of up to 12 columns each
            for start in range(0, min(num_columns, 55), 12):
                end = start + 12
                group = numeric_data.iloc[:, start:end]
                skewness = group.skew()
                print(f"Skewness for columns {start + 1} to {end}:")
                print(skewness)
                plot_histograms_in_grid(group, f"Histograms for Columns {start + 1} to {end}")
