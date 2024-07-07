import pandas as pd
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from products.models import Product

class Command(BaseCommand):
    help = 'Upload product data from a CSV file to the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            # Check CSV file format before reading
            with open(csv_file, 'r') as f:
                first_line = f.readline().strip()
                required_columns = ['product_name', 'category', 'price', 'quantity_sold', 'rating', 'review_count']
                actual_columns = first_line.split(',')
                if not all(column in actual_columns for column in required_columns):
                    raise ValueError(f"CSV file should contain columns: {', '.join(required_columns)}")

            df = pd.read_csv(csv_file)

            # Clean data
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

            df['price'].fillna(df['price'].median(), inplace=True)
            df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
            df['rating'] = df.groupby('category')['rating'].transform(lambda x: x.fillna(x.mean()))

            for _, row in df.iterrows():
                try:
                    Product.objects.update_or_create(
                        product_name=row['product_name'],
                        category=row['category'],
                        price=row['price'],
                        quantity_sold=row['quantity_sold'],
                        rating=row['rating'],
                        review_count=row['review_count'],
                    )
                except IntegrityError as e:
                    self.stderr.write(f'IntegrityError: {str(e)}')
                    continue  # Skip to the next row if IntegrityError occurs

            self.stdout.write(self.style.SUCCESS('Data uploaded successfully'))

        except FileNotFoundError as e:
            self.stderr.write(f'FileNotFoundError: {str(e)}')

        except pd.errors.ParserError as e:
            self.stderr.write(f'ParserError: {str(e)}')

        except ValueError as e:
            self.stderr.write(f'ValueError: {str(e)}')

        except Exception as e:
            self.stderr.write(f'Error: {str(e)}')
