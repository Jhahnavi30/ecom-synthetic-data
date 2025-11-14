from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker


def create_users(fake: Faker, count: int) -> pd.DataFrame:
    users = []
    for user_id in range(1, count + 1):
        created_at = fake.date_time_between(start_date="-2y", end_date="now")
        users.append(
            {
                "user_id": user_id,
                "name": fake.name(),
                "email": fake.unique.email(),
                "created_at": created_at.isoformat(),
            }
        )
    return pd.DataFrame(users)


def create_products(fake: Faker, count: int) -> pd.DataFrame:
    categories = [
        "Electronics",
        "Home",
        "Beauty",
        "Books",
        "Sports",
        "Toys",
        "Groceries",
    ]
    products = []
    for product_id in range(1, count + 1):
        base_price = round(random.uniform(5, 500), 2)
        products.append(
            {
                "product_id": product_id,
                "name": fake.catch_phrase(),
                "category": random.choice(categories),
                "price": base_price,
            }
        )
    return pd.DataFrame(products)


def create_orders(fake: Faker, users_df: pd.DataFrame, count: int) -> pd.DataFrame:
    orders = []
    now = datetime.utcnow()
    for order_id in range(1, count + 1):
        user_id = int(random.choice(users_df["user_id"]))
        order_date = fake.date_time_between(start_date="-18mo", end_date="now")
        orders.append(
            {
                "order_id": order_id,
                "user_id": user_id,
                "order_date": order_date.isoformat(),
                "total_amount": 0.0,  # placeholder; filled after order items created
            }
        )
    return pd.DataFrame(orders)


def create_order_items(
    products_df: pd.DataFrame, orders_df: pd.DataFrame, target_rows: int
) -> pd.DataFrame:
    items = []
    order_item_id = 1
    product_prices = products_df.set_index("product_id")["price"].to_dict()

    orders_cycle = list(orders_df["order_id"])
    current_index = 0
    while len(items) < target_rows:
        order_id = orders_cycle[current_index % len(orders_cycle)]
        product_id = random.choice(products_df["product_id"].tolist())
        quantity = random.randint(1, 5)
        base_price = product_prices[product_id]
        price_variation = random.uniform(0.9, 1.1)
        item_price = round(base_price * price_variation, 2)

        items.append(
            {
                "order_item_id": order_item_id,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "item_price": item_price,
            }
        )
        order_item_id += 1
        current_index += 1

    return pd.DataFrame(items)


def reconcile_order_totals(orders_df: pd.DataFrame, order_items_df: pd.DataFrame) -> pd.DataFrame:
    line_totals = order_items_df.assign(
        line_total=order_items_df["quantity"] * order_items_df["item_price"]
    )
    totals = (
        line_totals.groupby("order_id")["line_total"]
        .sum()
        .reindex(orders_df["order_id"], fill_value=0)
    )
    orders_df = orders_df.copy()
    orders_df["total_amount"] = totals.round(2).values
    return orders_df


def create_payments(fake: Faker, orders_df: pd.DataFrame) -> pd.DataFrame:
    methods = ["credit_card", "paypal", "bank_transfer", "gift_card"]
    statuses = ["paid", "pending", "failed"]
    payments = []
    for order in orders_df.to_dict("records"):
        paid_at = datetime.fromisoformat(order["order_date"]) + timedelta(
            hours=random.randint(1, 72)
        )
        status = random.choices(statuses, weights=[0.8, 0.15, 0.05])[0]
        payments.append(
            {
                "payment_id": order["order_id"],
                "order_id": order["order_id"],
                "payment_method": random.choice(methods),
                "status": status,
                "paid_at": paid_at.isoformat(),
            }
        )
    return pd.DataFrame(payments)


def main() -> None:
    random.seed(42)
    fake = Faker()
    fake.seed_instance(42)

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    users_df = create_users(fake, 100)
    products_df = create_products(fake, 50)
    orders_df = create_orders(fake, users_df, 200)
    order_items_df = create_order_items(products_df, orders_df, 400)
    orders_df = reconcile_order_totals(orders_df, order_items_df)
    payments_df = create_payments(fake, orders_df)

    output_files = {
        "users.csv": users_df,
        "products.csv": products_df,
        "orders.csv": orders_df,
        "order_items.csv": order_items_df,
        "payments.csv": payments_df,
    }

    for filename, df in output_files.items():
        df.to_csv(data_dir / filename, index=False)

    print(f"Generated {len(output_files)} datasets in {data_dir.resolve()}")


if __name__ == "__main__":
    main()


