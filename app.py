from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load data from CSV
def load_data():
    df = pd.read_csv(r"C:\Users\varun\Downloads\leetcode-website\data\leetcode.csv")
    return df

# Generate Clearbit logo URL based on the company name
def get_clearbit_logo_url(company_name):
    company_domain = f"{company_name.lower().replace(' ', '')}.com"
    return f"https://logo.clearbit.com/{company_domain}"

@app.route('/')
def index():
    # Load LeetCode data
    data = load_data()

    # Get query parameters for sorting and searching
    sort_by = request.args.get('sort_by', 'ID')
    search_query = request.args.get('search', '').lower()
    company_filter = request.args.get('company', '').lower()
    difficulty_filter = request.args.get('difficulty', '').lower()
    acceptance_rate = request.args.get('acceptance_rate', '')

    # Search filter by Title
    if search_query:
        data = data[data['Title'].str.lower().str.contains(search_query)]

    # Filter by Company
    if company_filter:
        data = data[data['Company'].str.lower().str.contains(company_filter)]

    # Filter by Difficulty
    if difficulty_filter:
        data = data[data['Difficulty'].str.lower() == difficulty_filter]

    # Filter by Acceptance Rate (greater or equal)
    if acceptance_rate:
        try:
            acceptance_rate = float(acceptance_rate.strip('%'))
            data = data[data['Acceptance'].str.rstrip('%').astype(float) >= acceptance_rate]
        except ValueError:
            pass  # Ignore if conversion fails

    # Sort data
    if sort_by in ['ID', 'Title', 'Acceptance', 'Difficulty']:
        if sort_by == 'Acceptance':
            data['Acceptance'] = data['Acceptance'].str.rstrip('%').astype(float)
        data = data.sort_values(by=sort_by, ascending=True)

    # Add logo URLs to the data
    data['Logo'] = data['Company'].apply(get_clearbit_logo_url)

    # Get unique companies and difficulties for the dropdowns
    unique_companies = sorted(data['Company'].unique())
    unique_difficulties = sorted(data['Difficulty'].unique())

    return render_template('index.html', data=data.to_dict(orient='records'),
                           unique_companies=unique_companies,
                           unique_difficulties=unique_difficulties)

@app.route('/about')
def about():
    return render_template('about.html')  # Render the about.html template

if __name__ == "__main__":
    app.run(debug=True)
