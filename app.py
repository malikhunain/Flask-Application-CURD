from flask import Flask, request, redirect, url_for, render_template
import uuid, json
app = Flask("Flask Application")

# Read operation
@app.route("/")
def get_transactions():
    try:
        with open('transactions.json', 'r') as file:
            dataset = json.load(file)
    except FileNotFoundError:
        dataset = []
    return render_template("transactions.html", transactions=dataset)

# Create operation
def create_new_record(date, amount):
    try:
        with open('transactions.json', 'r') as file:
            dataset = json.load(file)
    except FileNotFoundError:
        dataset = []

    record = {
        "id": str(uuid.uuid1()),
        "date": date,
        "amount": amount
    }
    dataset.append(record)
    with open('transactions.json', 'w') as file:
        json.dump(dataset, file)

@app.route("/create", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        date = request.form["date"]
        amount = request.form["amount"]
        create_new_record(date, amount)
        return redirect(url_for("get_transactions"))
    return render_template("form.html")

# Update operation
def update_record(id, date, amount):
    try:
        with open('transactions.json', 'r') as file:
            dataset = json.load(file)
    except FileNotFoundError:
        dataset = []

    for data in dataset:
        if str(data['id']) == str(id):
            data['date'] = date
            data['amount'] = amount
            break
    
    with open('transactions.json', 'w') as file:
        json.dump(dataset, file)
    

def get_record(id):
    try:
        with open('transactions.json', 'r') as file:
            dataset = json.load(file)
    except FileNotFoundError:
        dataset = []

    for data in dataset:
        if str(data['id']) == str(id):
            return data

    return None

@app.route("/edit/<transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":
        date = request.form["date"]
        amount = request.form["amount"]
        update_record(transaction_id, date, amount)
        return redirect(url_for("get_transactions"))
    record = get_record(transaction_id)
    return render_template("edit.html", transaction=record)

# Delete operation
def delete_record(id):
    try:
        with open('transactions.json', 'r') as file:
            dataset = json.load(file)
    except FileNotFoundError:
        dataset = []

    for data in dataset:
        if str(data['id']) == str(id):
            dataset.remove(data)
            break
    with open('transactions.json', 'w') as file:
        json.dump(dataset, file)

@app.route("/delete/<transaction_id>", methods=["GET"])
def delete_transaction(transaction_id):
    delete_record(transaction_id)
    return redirect(url_for("get_transactions"))

@app.route("/search", methods=["GET", "POST"])
def search_transaction():
    if request.method == "POST":
        min_amount = request.form["min_amount"]
        max_amount = request.form["max_amount"]
        record = []
        try:
            with open('transactions.json', 'r') as file:
                dataset = json.load(file)
        except FileNotFoundError:
            dataset = []
        for data in dataset:
            if int(data["amount"]) > int(min_amount) and int(data["amount"]) < int(max_amount):
                record.append(data)

        return render_template("transactions.html", transactions=record)
    return render_template("search.html")
        

# Run the Flask app
    