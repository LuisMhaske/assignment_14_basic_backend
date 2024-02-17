from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Dummy data for demonstration purposes (replace with database or actual data source)
inventory = {'Piano': {'quantity': 100, 'price_per_unit': 10},
             'Batman': {'quantity': 50, 'price_per_unit': 20}}
account_balance = 1000
history = []

# Function to update inventory
def update_inventory(product_name, quantity):
    global inventory
    if product_name in inventory and inventory[product_name]['quantity'] >= quantity:
        inventory[product_name]['quantity'] -= quantity
        return True
    return False

# Function to update account balance
def update_balance(amount):
    global account_balance
    account_balance += amount

# Function to record transaction history
def record_transaction(transaction_type, product_name, quantity, price_per_unit):
    global history
    timestamp = datetime.now()
    history.append({'timestamp': timestamp, 'transaction_type': transaction_type,
                    'product_name': product_name, 'quantity': quantity,
                    'price_per_unit': price_per_unit})

# Main page route
@app.route('/')
def main_page():
    return render_template('mainpage.html', inventory=inventory, account_balance=account_balance)

# Purchase form submission route
@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = int(request.form['quantity'])
        price_per_unit = int(request.form['price_per_unit'])

        if product_name in inventory:
            # Product exists in inventory
            old_quantity = inventory[product_name]['quantity']
            old_price_per_unit = inventory[product_name]['price_per_unit']
            total_price = quantity * price_per_unit

            if account_balance >= total_price:
                # Sufficient balance to purchase
                if old_price_per_unit != price_per_unit:
                    # Update price_per_unit if new price
                    inventory[product_name]['price_per_unit'] = price_per_unit

                # Increase quantity
                inventory[product_name]['quantity'] += quantity

                update_balance(-total_price)
                record_transaction('Purchase', product_name, quantity, price_per_unit)

                return redirect(url_for('main_page'))
            else:
                return "Error: Insufficient account balance"
        else:
            # Product does not exist in inventory, add new entry
            total_price = quantity * price_per_unit
            if account_balance >= total_price:
                inventory[product_name] = {'quantity': quantity, 'price_per_unit': price_per_unit}

                update_balance(-total_price)
                record_transaction('Purchase', product_name, quantity, price_per_unit)

                return redirect(url_for('main_page'))
            else:
                return "Error: Insufficient account balance"
    else:
        return render_template('purchase.html')


# Sale form submission route
@app.route('/sale', methods=['GET', 'POST'])
def sale():
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = int(request.form['quantity'])
        price_per_unit = int(request.form['price_per_unit'])
        if product_name in inventory and inventory[product_name]['quantity'] >= quantity:
            # price_per_unit = inventory[product_name]['price_per_unit']
            total_price = quantity * price_per_unit
            update_inventory(product_name, quantity)
            update_balance(total_price)
            record_transaction('Sale', product_name, quantity, price_per_unit)
            return redirect(url_for('main_page'))
        else:
            return "Error: Not enough stock for sale"
    else:
        return render_template('sale.html')

# Balance change form submission route
@app.route('/balance', methods=['GET', 'POST'])
def balance():
    if request.method == 'POST':
        amount = int(request.form['amount'])
        update_balance(amount)
        record_transaction('Balance Change', '', 0, amount)
        return redirect(url_for('main_page'))
    else:
        return render_template('balance.html')


# History subpage route
@app.route('/history/')
@app.route('/history/<line_from>/<line_to>/')
def history_page(line_from=None, line_to=None):
    global history
    if line_from and line_to:
        line_from = int(line_from)
        line_to = int(line_to)
        history = history[line_from:line_to]
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
