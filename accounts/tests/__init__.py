import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "CakeTime.settings_test")

print(os.environ.get("DJANGO_SETTINGS_MODULE"))
