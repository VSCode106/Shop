from flask import Flask, render_template, redirect, url_for, request
import csv
from datetime import datetime

app = Flask(__name__)

def get_csv_file_path():
    """Generate the CSV file path based on the current date."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"Product_{current_date}.csv"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/take_attendance')
def take_attendance():
    return render_template('index.html')

@app.route('/view_attendance')
def view_attendance():
    csv_file_path = get_csv_file_path()
    try:
        with open(csv_file_path, "r") as f:
            reader = csv.reader(f)
            attendance_data = list(reader)
            print("Attendance Data:", attendance_data)  # Debug print
    except FileNotFoundError:
        attendance_data = []
    return render_template('view_attendance.html', attendance_data=attendance_data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        csv_file_path = get_csv_file_path()
        try:
            with open(csv_file_path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if query.lower() in row[0].lower() or query.lower() in row[1].lower() or query.lower() in row[3].lower():
                        results.append(row)
        except FileNotFoundError:
            pass
    return render_template('search.html', results=results)

@app.route('/add_attendance', methods=['POST'])
def add_attendance():
    S_No = request.form['S_No']
    name = request.form['name']
    locality = request.form['locality']
    phone_no = request.form['phone_no']
    item = request.form['item']
    price = request.form['price']
    pending = request.form['pending']
    time = datetime.now().strftime("%H:%M:%S")
    csv_file_path = get_csv_file_path()
    with open(csv_file_path, "a+", newline="") as csv_file:
        lnwriter = csv.writer(csv_file)
        lnwriter.writerow([S_No, name, locality, phone_no, item, price, pending, time])
        print(f"Manually recorded {name} S_No {S_No} at {time}")  # Debug print
    return redirect(url_for('take_attendance'))

if __name__ == "__main__":
    app.run(debug=True)
