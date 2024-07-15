import pandera as pa
from pandera.typing import Series
import pandas as pd

# Define the schema using pa.SchemaModel
class MySchema(pa.SchemaModel):
    col1: Series[int]
    col2: Series[float]
    col3: Series[str]

    class Config:
        strict = True

# Create a DataFrame to validate
df = pd.DataFrame({
    "col1": [1, 2, 3],
    "col2": [4.0, 5.1, 6.2],
    "col3": ["a", "b", "c"]
})

# Validate the DataFrame
validated_df = MySchema.validate(df)
print(validated_df)
