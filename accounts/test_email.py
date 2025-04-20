from django.core.mail import send_mail

# em8088.example.com

send_mail(
    "Тестовое письмо",
    "Привет! Это тестовое письмо из Django через SendGrid.",
    "caketime.store@gmail.com",
    ["arsen.test.mess@gmail.com"],  # Замени на реальный email получателя
    fail_silently=False,
)
