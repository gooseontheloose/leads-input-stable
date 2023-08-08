from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLineEdit, QTextEdit, QPushButton, QComboBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFormLayout, QTabWidget, QTableWidget, QTableWidgetItem
import sys
import sqlite3

class InputTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.address1_input = QLineEdit()
        self.address2_input = QLineEdit()
        self.city_input = QLineEdit()
        self.state_input = QLineEdit()
        self.zipcode_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.type_of_work_combo = QComboBox()
        self.type_of_work_combo.addItems(["Residential", "Commercial", "Other"])
        self.referred_by_input = QLineEdit()

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_lead)

        layout = QFormLayout()  # Use QFormLayout here
        layout.addRow("First Name:", self.first_name_input)
        layout.addRow("Last Name:", self.last_name_input)
        layout.addRow("Address Line 1:", self.address1_input)
        layout.addRow("Address Line 2:", self.address2_input)
        layout.addRow("City:", self.city_input)
        layout.addRow("State:", self.state_input)
        layout.addRow("Zipcode:", self.zipcode_input)
        layout.addRow("Notes:", self.notes_input)
        layout.addRow("Type of Work:", self.type_of_work_combo)
        layout.addRow("Referred By:", self.referred_by_input)
        layout.addRow(self.submit_button)

        self.setLayout(layout)

    def submit_lead(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        address1 = self.address1_input.text()
        address2 = self.address2_input.text()
        city = self.city_input.text()
        state = self.state_input.text()
        zipcode = self.zipcode_input.text()
        notes = self.notes_input.toPlainText()
        type_of_work = self.type_of_work_combo.currentText()
        referred_by = self.referred_by_input.text()

        query = "INSERT INTO leads (first_name, last_name, address1, address2, city, state, zipcode, notes, type_of_work, referred_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        params = (first_name, last_name, address1, address2, city, state, zipcode, notes, type_of_work, referred_by)
        self.parent.execute_query(query, params)

        self.parent.view_tab.populate_table()

        self.first_name_input.clear()
        self.last_name_input.clear()
        self.address1_input.clear()
        self.address2_input.clear()
        self.city_input.clear()
        self.state_input.clear()
        self.zipcode_input.clear()
        self.notes_input.clear()
        self.type_of_work_combo.setCurrentIndex(0)
        self.referred_by_input.clear()

class ViewTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.table = QTableWidget()
        self.table.setColumnCount(13)  # Number of columns
        self.table.setHorizontalHeaderLabels([
            "Lead ID", "Lead Status", "First Name", "Last Name", "Address Line 1", "Address Line 2",
            "City", "State", "Zipcode", "Notes", "Type of Work", "Referred By", "Delete"
        ])  # Column names

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_table)

        self.save_changes_button = QPushButton("Save Changes")
        self.save_changes_button.clicked.connect(self.save_changes)

        self.populate_table()

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.save_changes_button)

        self.setLayout(layout)

    def populate_table(self):
        self.table.setRowCount(0)

        query = "SELECT * FROM leads"
        leads = self.parent.execute_query(query)

        for lead in leads:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, row=row_position: self.delete_lead(row))

            self.table.setItem(row_position, 0, QTableWidgetItem(str(lead[0])))  # Lead ID
            self.table.setItem(row_position, 1, QTableWidgetItem("Pending"))
            self.table.setItem(row_position, 2, QTableWidgetItem(lead[1]))  # First Name
            self.table.setItem(row_position, 3, QTableWidgetItem(lead[2]))  # Last Name
            self.table.setItem(row_position, 4, QTableWidgetItem(lead[3]))  # Address Line 1
            self.table.setItem(row_position, 5, QTableWidgetItem(lead[4]))  # Address Line 2
            self.table.setItem(row_position, 6, QTableWidgetItem(lead[5]))  # City
            self.table.setItem(row_position, 7, QTableWidgetItem(lead[6]))  # State
            self.table.setItem(row_position, 8, QTableWidgetItem(lead[7]))  # Zipcode
            self.table.setItem(row_position, 9, QTableWidgetItem(lead[8]))  # Notes
            self.table.setItem(row_position, 10, QTableWidgetItem(lead[9]))  # Type of Work
            self.table.setItem(row_position, 11, QTableWidgetItem(lead[10]))  # Referred By
            self.table.setCellWidget(row_position, 12, delete_button)

    def refresh_table(self):
        self.populate_table()

    def save_changes(self):
        for row in range(self.table.rowCount()):
            lead_id = int(self.table.item(row, 0).text())
            first_name = self.table.item(row, 2).text()
            last_name = self.table.item(row, 3).text()
            address1 = self.table.item(row, 4).text()
            address2 = self.table.item(row, 5).text()
            city = self.table.item(row, 6).text()
            state = self.table.item(row, 7).text()
            zipcode = self.table.item(row, 8).text()
            notes = self.table.item(row, 9).text()
            type_of_work = self.table.item(row, 10).text()
            referred_by = self.table.item(row, 11).text()

            query = "UPDATE leads SET first_name=?, last_name=?, address1=?, address2=?, city=?, state=?, " \
                    "zipcode=?, notes=?, type_of_work=?, referred_by=? WHERE id=?"
            params = (first_name, last_name, address1, address2, city, state, zipcode, notes,
                      type_of_work, referred_by, lead_id)
            self.parent.execute_query(query, params)

        self.populate_table()

    def delete_lead(self, row):
        lead_id = int(self.table.item(row, 0).text())
        query = "DELETE FROM leads WHERE id = ?"
        self.parent.execute_query(query, (lead_id,))
        self.populate_table()

class FormsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()

        self.my_forms_tab = ComingSoonTab("My Forms")
        self.create_form_tab = ComingSoonTab("Create")
        self.embed_form_tab = ComingSoonTab("Embed")

        self.tab_widget.addTab(self.my_forms_tab, "My Forms")
        self.tab_widget.addTab(self.create_form_tab, "Create")
        self.tab_widget.addTab(self.embed_form_tab, "Embed")

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

class IntegrationsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()

        payments_integrations_tab = QTabWidget()
        payments_integrations_tab.addTab(ComingSoonTab("Stripe"), "Stripe")
        payments_integrations_tab.addTab(ComingSoonTab("Square"), "Square")
        payments_integrations_tab.addTab(ComingSoonTab("PayPal"), "PayPal")

        automation_integrations_tab = QTabWidget()
        automation_integrations_tab.addTab(ComingSoonTab("Zapier"), "Zapier")
        automation_integrations_tab.addTab(ComingSoonTab("Other Alternatives"), "Other Alternatives")

        calendar_integrations_tab = QTabWidget()
        calendar_integrations_tab.addTab(ComingSoonTab("Google"), "Google")
        calendar_integrations_tab.addTab(ComingSoonTab("Calendly"), "Calendly")
        calendar_integrations_tab.addTab(ComingSoonTab("GHL"), "GHL")
        calendar_integrations_tab.addTab(ComingSoonTab("Other"), "Other")

        calls_integrations_tab = QTabWidget()
        calls_integrations_tab.addTab(ComingSoonTab("Twilio"), "Twilio")
        calls_integrations_tab.addTab(ComingSoonTab("Callrail"), "Callrail")
        calls_integrations_tab.addTab(ComingSoonTab("Google Voice"), "Google Voice")

        email_integrations_tab = QTabWidget()
        email_integrations_tab.addTab(ComingSoonTab("Gmail"), "Gmail")
        email_integrations_tab.addTab(ComingSoonTab("Yahoo"), "Yahoo")
        email_integrations_tab.addTab(ComingSoonTab("SMTP"), "SMTP")
        email_integrations_tab.addTab(ComingSoonTab("Other Protocols"), "Other Protocols")

        messaging_integrations_tab = QTabWidget()
        messaging_integrations_tab.addTab(ComingSoonTab("Twilio"), "Twilio")
        messaging_integrations_tab.addTab(ComingSoonTab("Facebook"), "Facebook")
        messaging_integrations_tab.addTab(ComingSoonTab("Instagram"), "Instagram")
        messaging_integrations_tab.addTab(ComingSoonTab("Twitter"), "Twitter")

        self.tab_widget.addTab(payments_integrations_tab, "Payments")
        self.tab_widget.addTab(automation_integrations_tab, "Automation")
        self.tab_widget.addTab(calendar_integrations_tab, "Calendar")
        self.tab_widget.addTab(calls_integrations_tab, "Calls")
        self.tab_widget.addTab(email_integrations_tab, "Emails")
        self.tab_widget.addTab(messaging_integrations_tab, "Messaging")

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

class ComingSoonTab(QWidget):
    def __init__(self, tab_name):
        super().__init__()
        self.layout = QVBoxLayout()
        label = QLabel(f"Coming Soon: {tab_name}")
        label.setAlignment(Qt.AlignCenter)  # Use Qt.AlignCenter
        self.layout.addWidget(label)
        self.setLayout(self.layout)

class CustomCRMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom CRM App")
        self.setGeometry(100, 100, 800, 600)

        self.init_database()

        self.tab_widget = QTabWidget(self)
        self.tabs = {
            "Input": InputTab(self),
            "View": ViewTab(self),
            "Calendar": ComingSoonTab("Calendar"),
            "Calls": ComingSoonTab("Calls"),
            "Emails": ComingSoonTab("Emails"),
            "Messaging": ComingSoonTab("Messaging"),
            "Forms": FormsTab(),  
            "Integrations": IntegrationsTab(),
            "Settings": ComingSoonTab("Settings")
        }

        for tab_name, tab_instance in self.tabs.items():
            self.tab_widget.addTab(tab_instance, tab_name)

        self.setCentralWidget(self.tab_widget)

    def init_database(self):
        self.conn = sqlite3.connect("leads.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                address1 TEXT,
                address2 TEXT,
                city TEXT,
                state TEXT,
                zipcode TEXT,
                notes TEXT,
                type_of_work TEXT,
                referred_by TEXT
            )
        """)
        self.conn.commit()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        result = None
        if "SELECT" in query:
            result = self.cursor.fetchall()
        else:
            self.conn.commit()

        return result

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomCRMApp()
    window.show()
    sys.exit(app.exec_())
