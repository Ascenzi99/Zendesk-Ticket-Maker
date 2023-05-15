import sys
import base64
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QSpinBox
import requests
import json

class TicketCreator(QWidget):
    def __init__(self, parent=None):
        super(TicketCreator, self).__init__(parent)
        self.layout = QVBoxLayout()

        self.email = 'brian.shantz95@gmail.com'
        self.api_token = 'U1OlCIJlUglDdG0TmFljuzR7z6caytDCMX3RwV2o'
        self.auth = base64.b64encode(f'{self.email}/token:{self.api_token}'.encode()).decode()

        self.subject_label = QLabel('Subject:')
        self.subject_input = QLineEdit()

        self.body_label = QLabel('Body:')
        self.body_input = QLineEdit()

        self.ticket_number_label = QLabel('Number of tickets:')
        self.ticket_number_input = QSpinBox()

        self.submit_button = QPushButton('Create Tickets')
        self.submit_button.clicked.connect(self.create_tickets)

        self.layout.addWidget(self.subject_label)
        self.layout.addWidget(self.subject_input)
        self.layout.addWidget(self.body_label)
        self.layout.addWidget(self.body_input)
        self.layout.addWidget(self.ticket_number_label)
        self.layout.addWidget(self.ticket_number_input)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def create_tickets(self):
        tickets = []
        subject_base = self.subject_input.text()
        body = self.body_input.text()

        for i in range(self.ticket_number_input.value()):
            tickets.append({
                "subject": f"{subject_base} {i+1}",
                "comment": {"body": body},
            })

        data = json.dumps({"tickets": tickets})

        response = requests.post(
            'https://d3v-appsforalex.zendesk.com/api/v2/tickets/create_many.json',
            headers={'Content-type': 'application/json', 'Authorization': f'Basic {self.auth}'},
            data=data,
        )

        print(response.status_code)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TicketCreator()
    window.show()

    sys.exit(app.exec_())
