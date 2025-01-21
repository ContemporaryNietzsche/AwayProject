import pandas as pd

data = {'Name': ['Tom', 'Nick', 'John'],
        'Age': [20, 21, 19],
        'City': ['New York', 'Los Angeles', 'Chicago']}

df = pd.DataFrame(data)

print("DataFrame:\n", df)

average_age = df['Age'].mean()

print ("\nAverage Age:", average_age)