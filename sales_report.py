import psycopg2
import csv

def connect_to_database():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="dbpython",
            user="root",
            password="root",
            host="localhost"
        )
        print("Connected to the database")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

def generate_sales_report(conn, start_date=None, end_date=None, product_name=None):
    try:
        cursor = conn.cursor()
        
        # Construct the SQL query using parameters
        query = "SELECT * FROM sales WHERE true"
        params = []

        if start_date:
            query += " AND sale_date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND sale_date <= %s"
            params.append(end_date)
        if product_name:
            query += " AND product_name = %s"
            params.append(product_name)
        
        # Execute the query
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return rows
    except psycopg2.Error as e:
        print("Error executing SQL query:", e)
        return None

def export_to_csv(report_data, filename):
    try:
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([i[0] for i in cursor.description])  # Write header
            for row in report_data:
                csv_writer.writerow(row)
        print(f"Report exported to {filename}")
    except Exception as e:
        print("Error exporting report to CSV:", e)

if __name__ == '__main__':
    conn = connect_to_database()
    if conn:
        start_date = input("Enter start date (YYYY-MM-DD) [Optional, leave blank for no filter]: ")
        end_date = input("Enter end date (YYYY-MM-DD) [Optional, leave blank for no filter]: ")
        product_name = input("Enter product name [Optional, leave blank for no filter]: ")

        report_data = generate_sales_report(conn, start_date, end_date, product_name)

        if report_data:
            filename = 'sales_report.csv'
            export_to_csv(report_data, filename)
        else:
            print("No data found matching the specified criteria.")
        conn.close()
    else:
        print("Exiting script due to database connection error.")

