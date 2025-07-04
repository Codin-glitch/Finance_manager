import pandas as pd

# Initialize categories
finance_data = {
    'Credit': [],
    'Debit': [],
    'Savings': []
}

category_map = {
    '1': 'Credit',
    '2': 'Debit',
    '3': 'Savings'
}

# Function to add entry
def add_entry(category, amount, description):
    entry = {
        'Amount': amount,
        'Description': description,
        'Running Total': 0
    }
    finance_data[category].append(entry)

# Function to update running totals
def update_totals():
    for category in finance_data:
        total = 0
        for entry in finance_data[category]:
            total += entry['Amount']
            entry['Running Total'] = total

# Take user input
while True:
    print("\nSelect category:\n1. Credit\n2. Debit\n3. Savings\nEnter '0' to exit.")
    choice = input("Your choice: ").strip()
    
    if choice == '0':
        break
    if choice not in category_map:
        print("❌ Invalid choice. Try again.")
        continue
    
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        continue

    description = input("Enter description: ")
    add_entry(category_map[choice], amount, description)

# Update totals before saving
update_totals()

# Save to Excel
with pd.ExcelWriter('finance_tracker.xlsx', engine='openpyxl') as writer:
    for category, entries in finance_data.items():
        df = pd.DataFrame(entries)
        df.to_excel(writer, sheet_name=category, index=False)

print("\n✅ Finance data saved to 'finance_tracker.xlsx'")
