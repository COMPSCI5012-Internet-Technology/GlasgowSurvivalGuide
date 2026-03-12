import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GlasgowSurvivalGuide.settings')

django.setup()


from guide.models import Category

def populate():
   
    category_list = [
        "Default",
        "Lifestyle - Resturant",
        "Lifestyle - Park",
        "Lifestyle - Bar",
        "University - Computer Science",
        "University - Human and Art",
        "University - Business",
    ]

    for cat_name in category_list:
        Category.objects.get_or_create(name=cat_name)
if __name__ == '__main__':
    populate()