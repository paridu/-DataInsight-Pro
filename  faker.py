import pandas as pd
import numpy as np
from faker import Faker
import random

# สร้าง instance ของ Faker
fake = Faker()

# สร้างรายการคงที่สำหรับบางคอลัมน์
departments = ['Sales', 'HR', 'IT', 'Finance', 'Marketing']
genders = ['Male', 'Female']
comments = [
    "Excellent performance",
    "Needs improvement",
    "Average performance",
    "Outstanding contribution",
    "Below expectations",
    "Met expectations"
]

# สร้างข้อมูลจำลอง
data = {
    'ID': range(1, 501),
    'Name': [fake.name() for _ in range(500)],
    'Age': [random.randint(18, 65) for _ in range(500)],
    'Gender': [random.choice(genders) for _ in range(500)],
    'Join Date': [fake.date_between(start_date='-8y', end_date='today') for _ in range(500)],
    'Salary': [random.randint(30000, 120000) for _ in range(500)],
    'Department': [random.choice(departments) for _ in range(500)],
    'Performance Score': [random.randint(1, 10) for _ in range(500)],
    'Comments': [random.choice(comments) for _ in range(500)]
}

# สร้าง DataFrame
df = pd.DataFrame(data)

# บันทึกเป็น CSV
df.to_csv('sample_dataset.csv', index=False)

print("DataSet created successfully!")
