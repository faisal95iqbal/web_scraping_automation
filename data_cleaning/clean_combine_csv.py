import pandas as pd

# Load CSV files
products = pd.read_csv("products.csv")
prices = pd.read_csv("prices.csv")
inventory = pd.read_csv("inventory.csv")

# Clean column names
def clean_cols(df):
    df.columns = (df.columns.str.strip()
                            .str.lower()
                            .str.replace(" ", "_")
                            .str.replace("-", "_"))
    return df

products = clean_cols(products)
prices = clean_cols(prices)
inventory = clean_cols(inventory)

# Clean string values (trim spaces)
products = products.applymap(lambda x: x.strip() if isinstance(x, str) else x)
prices = prices.applymap(lambda x: x.strip() if isinstance(x, str) else x)
inventory = inventory.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Merge all on product_id
final = products.merge(prices, on="product_id", how="left") \
                .merge(inventory, on="product_id", how="left")

# Remove duplicates
final = final.drop_duplicates()

# Save output
final.to_csv("cleaned_combined.csv", index=False)

print("\ncleaned_combined.csv created successfully!")
