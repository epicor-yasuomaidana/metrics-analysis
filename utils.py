import pandas as pd

scenarios = [
    "ARInvoiceTracker",
    "BAQ",
    "CopySalesOrder",
    "CustomerTracker",
    "GLJournalTracker",
    "JobTracker",
    "MiscARInvoice",
    "PartMaintenance",
    "PartTracker",
    "POEntry10",
    "POEntry20",
    "ProcessMRP",
    "QuantityOnHandCheck",
    "QuoteEntry",
    "SalesOrderEntry",
    "SalesOrderErrorNO",
    "SalesOrderErrorYES",
    "SalesOrderTracker",
    "SOEntry500ShipTos",
    "SystemMonitor"
]

def load_df_with_time_index(csv_path):
    df = pd.read_csv(csv_path)
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time'] = df['Time'] - df['Time'].min()
    df.set_index('Time', inplace=True)
    return df