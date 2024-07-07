import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Upload product data from a CSV file to the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        df = pd.read_csv(csv_file)

        # Clean data
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        df['price'].fillna(df['price'].median(), inplace=True)
        df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
        df['rating'] = df.groupby('category')['rating'].transform(lambda x: x.fillna(x.mean()))

        for _, row in df.iterrows():
            Product.objects.update_or_create(
                product_id=row['product_id'],
                defaults={
                    'product_name': row['product_name'],
                    'category': row['category'],
                    'price': row['price'],
                    'quantity_sold': row['quantity_sold'],
                    'rating': row['rating'],
                    'review_count': row['review_count'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Data uploaded successfully'))
