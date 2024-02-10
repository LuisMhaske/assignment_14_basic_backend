from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Sample data
stock_data = [
    {'product': 'Piano', 'in_stock': 100},
    {'product': 'Guitar', 'in_stock': 50},
    {'product': 'Drums', 'in_stock': 30}
]
account_balance = 1000

# Route for the main page
@app.route('/')
def main_page():
    return render_template('mainpage.html', account_balance=account_balance)

# Route for the purchase form
@app.route('/purchase', methods=['GET', 'POST'])
def purchase_form():
    if request.method == 'POST':
        # Process form submission here
        return redirect('/')
    return render_template('purchase.html')

# Route for the sale form
@app.route('/sale', methods=['GET', 'POST'])
def sale_form():
    if request.method == 'POST':
        # Process form submission here
        return redirect('/')
    return render_template('sale.html')

# Route for the balance change form
@app.route('/balance', methods=['GET', 'POST'])
def balance_change_form():
    if request.method == 'POST':
        # Process form submission here
        return redirect('/')
    return render_template('balance.html')

# Route for the history subpage
@app.route('/history')
def history():
    # Retrieve and display history data
    return "History page (to be implemented)"

if __name__ == '__main__':
    app.run(debug=True)
