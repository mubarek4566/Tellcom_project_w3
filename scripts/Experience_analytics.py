import pandas as pd

class Experience():
    def __init__(self, dataframe):
        self.df = dataframe
        #self.preprocess_column = None
        self.calculate_avg_tcp_retrans =None
        self.calculate_avg_rtt = None

    # Function to handle missing values and outliers
    def preprocess_column(self, dataframe):
        # Replace missing values with the column mean
        self.df[dataframe].fillna(self.df[dataframe].mean(), inplace=True)
        
        # Treat outliers using the IQR method
        Q1 = self.df[dataframe].quantile(0.25)
        Q3 = self.df[dataframe].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        self.df[dataframe] = self.df[dataframe].clip(lower=lower_bound, upper=upper_bound)
        
        return self.df
    
    def Analytics(self):
        # Handle missing values by replacing them with the column mean
        self.df['TCP DL Retrans. Vol (Bytes)'].fillna(self.df['TCP DL Retrans. Vol (Bytes)'].mean(), inplace=True)
        self.df['TCP UL Retrans. Vol (Bytes)'].fillna(self.df['TCP UL Retrans. Vol (Bytes)'].mean(), inplace=True)

        # Treat outliers using the IQR method
        def treat_outliers(column):
            Q1 = column.quantile(0.25)
            Q3 = column.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return column.clip(lower=lower_bound, upper=upper_bound)

        self.df['TCP DL Retrans. Vol (Bytes)'] = treat_outliers(self.df['TCP DL Retrans. Vol (Bytes)'])
        self.df['TCP UL Retrans. Vol (Bytes)'] = treat_outliers(self.df['TCP UL Retrans. Vol (Bytes)'])

        # Aggregate average TCP retransmission per customer
        customer_aggregated_data = self.df.groupby('IMSI')[
            ['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)']
        ].mean().rename(columns={
            'TCP DL Retrans. Vol (Bytes)': 'Avg TCP DL Retrans Vol (Bytes)',
            'TCP UL Retrans. Vol (Bytes)': 'Avg TCP UL Retrans Vol (Bytes)'
        }).reset_index()

        return customer_aggregated_data
    
    def Average_RTT(self):
        # Handle missing values by replacing them with the column mean
        columns_to_fill = ['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 
                        'Avg RTT DL (ms)', 'Avg RTT UL (ms)']
        for col in columns_to_fill:
            self.df[col].fillna(self.df[col].mean(), inplace=True)

        # Step 2: Treat outliers using the IQR method
        def treat_outliers(column):
            Q1 = column.quantile(0.25)
            Q3 = column.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return column.clip(lower=lower_bound, upper=upper_bound)

        columns_to_treat = ['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 
                            'Avg RTT DL (ms)', 'Avg RTT UL (ms)']
        for col in columns_to_treat:
            self.df[col] = treat_outliers(self.df[col])

        # Step 3: Aggregate average TCP retransmission and RTT per customer
        customer_aggregated_data = self.df.groupby('IMSI')[
            ['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 
            'Avg RTT DL (ms)', 'Avg RTT UL (ms)']
        ].mean().rename(columns={
            'TCP DL Retrans. Vol (Bytes)': 'Avg TCP DL Retrans Vol (Bytes)',
            'TCP UL Retrans. Vol (Bytes)': 'Avg TCP UL Retrans Vol (Bytes)',
            'Avg RTT DL (ms)': 'Avg RTT DL (ms)',
            'Avg RTT UL (ms)': 'Avg RTT UL (ms)'
        }).reset_index()

        return customer_aggregated_data

