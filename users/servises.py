import stripe
from stripe import StripeClient
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

client = StripeClient(STRIPE_API_KEY)  # явный клиент


def convert_rub_to_dollars(amount):
    """Конвертирование рубля в долар."""
    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(amount * rate)


def create_stripe_product(product):
    """Конвертирование объект Product на Страйпе."""
    return stripe.Product.create(name=product.title)


def create_stripe_price(payment, product):
    """Создаёт цену на Страйпе."""
    return stripe.Price.create(
        currency="usd",
        unit_amount=payment.amount * 100,
        # recurring={"interval": "month"},
        product_data={"name": product.name},
    )


def create_stripe_session(price):
    """Создаёт сессию на оплату в Страйпе."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )

    return session.id, session.url


def checkout_stripe_payment(session_id):
    return stripe.checkout.Session.retrieve(session_id)
