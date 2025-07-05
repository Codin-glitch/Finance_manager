from django.core.management.base import BaseCommand
from tracker.models import Transaction
from users.models import CustomUser
from users.session_utils import get_logged_in_user
from django.db.models import Sum
from django.db.models.functions import ExtractYear
import csv

class Command(BaseCommand):
    help = "Show yearly financial report"

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int, help="Filter report for specific year")
        parser.add_argument('--export', action='store_true', help="Export the report to yearly_report.csv")
    
    
    def handle(self, *args, **options):
        username = get_logged_in_user()
        if not username:
            self.stdout.write(self.style.ERROR("Please login first."))
            return

        user = CustomUser.objects.get(username=username)
        transactions = Transaction.objects.filter(user=user)

        if not transactions.exists():
            self.stdout.write(self.style.WARNING("No transactions found."))
            return

        currency = user.preferred_currency

        if options['year']:
            transactions = transactions.annotate(year=ExtractYear('date')).filter(year=options['year'])

        yearly_summary = transactions.annotate(year=ExtractYear('date')) \
            .values('year', 'type') \
            .annotate(total=Sum('amount')) \
            .order_by('year')

        report = {}

        for entry in yearly_summary:
            year = entry['year']
            if year not in report:
                report[year] = {'income': 0, 'expense': 0}
            report[year][entry['type']] = entry['total']

        if not report:
            self.stdout.write(self.style.WARNING("No data found for the selected year."))
            return

        self.stdout.write(self.style.SUCCESS(f"\nYearly Report for {username}:\n"))

        for year, totals in report.items():
            income = totals.get('income', 0)
            expense = totals.get('expense', 0)
            savings = income - expense
            self.stdout.write(f"{year}")
            self.stdout.write(f"  Income:  {currency}{income}")
            self.stdout.write(f"  Expense: {currency}{expense}")
            self.stdout.write(f"  Savings: {currency}{savings}\n")

        # Export CSV
        if options['export']:
            with open('yearly_report.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Year', 'Income', 'Expense', 'Savings'])
                for year, totals in report.items():
                    income = totals.get('income', 0)
                    expense = totals.get('expense', 0)
                    savings = income - expense
                    writer.writerow([year, income, expense, savings])
            self.stdout.write(self.style.SUCCESS("Report exported to yearly_report.csv"))
