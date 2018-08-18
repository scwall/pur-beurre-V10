from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from django.core.management.base import BaseCommand

import os
import sys
import time
import requests
from food_and_search.models import Categorie, Product
import setproctitle
import time




class Command(BaseCommand):
    help = 'Use the command --chargedatabase, to load the database'

    def add_arguments(self, parser):
        # for arg for load database
        parser.add_argument(
            '--chargedatabase',
            action='store_true',
            dest='charge_database',
            help='To load the database or use',
        )

    def handle(self, *args, **options):
        if options['charge_database']:
            setproctitle.setproctitle('saluttoi')
            self.stdout.write("charge database\n")
            #function to clear screen and calculate the progression percentage
            def clr():
                os.system('clr' if os.name == 'nt' else 'clear')

            def percentage_calculation(count, total_count):
                return int(100 * (count / total_count))

            #Recovery the categories of openfoodfacts
            count = 0
            self.stdout.write("Login to openfoodfact website\n")
            categories_json = requests.get("https://fr.openfoodfacts.org/categories.json")
            self.stdout.write("Successful login to the openfoodfact website\n")
            clr()
            categories_dic = categories_json.json()
            total_count = categories_dic['count']
            for categories in categories_dic['tags']:
                if int(categories['products']) > 10 and len(categories['name']) < 150 and str(
                        categories['name']).lower() != str(categories['id']).lower():
                    categorie_add = Categorie.objects.get_or_create(name=categories['name'],
                                              id_category=categories['id'])
                    count += 1

                else:
                    count += 1

                self.stdout.write("\rCategory Recovery, " + str(percentage_calculation(count, total_count)) + "%" +
                                  " d'effectué(s)\r")
                sys.stdout.flush()
            self.stdout.write("\rRecovering successful categories\r")
            time.sleep(2)

            # recovery products of the openfoodfacts
            self.stdout.write("\rProduct recovery\r")
            sys.stdout.flush()
            count = 0
            total_count = 0
            final_page = False
            range_list = [0, 20]

            while final_page is False:
                list_page_for_pool = []
                for link_page_add_list in range(*range_list):
                    link = ((lambda url, number_pages: str(url) + "/" + str(number_pages) + ".json")(
                        "https://fr.openfoodfacts.org", link_page_add_list + 1))

                    list_page_for_pool.append(link)

                # Function call in multiprocessing
                def function_recovery_and_push(link_page):
                    count_and_end_page_return_all = {}
                    count_f = 0
                    total_count_f = 0
                    try:
                        products_dic = requests.get(link_page).json()
                        if products_dic['count']:
                            count_f = products_dic['page_size']
                        if products_dic['count']:
                            total_count_f = products_dic['count']
                        if not products_dic['products']:
                            count_and_end_page_return_all['count'] = False
                            count_and_end_page_return_all['total_count'] = False
                            count_and_end_page_return_all['final_page'] = True
                        else:
                            count_and_end_page_return_all['final_page'] = False
                        for product in products_dic["products"]:
                            if 'nutrition_grades' in product.keys() \
                                    and 'product_name_fr' in product.keys() \
                                    and 'categories_tags' in product.keys() \
                                    and 1 <= len(product['product_name_fr']) <= 100:
                                try:
                                    add_product, created = Product.objects.get_or_create(id_singularity=int(product['code']),name=product['product_name_fr'],
                                                          description=product['ingredients_text_fr'],
                                                          nutrition_grade=product['nutrition_grades'],
                                                          link_http=product['url'],
                                                          link_picture=product['image_front_small_url'],
                                                          saturated_fat_100g=product['nutriments'][
                                                              'saturated-fat_100g'],
                                                          carbohydrates_100g=product['nutriments'][
                                                              'carbohydrates_100g'],
                                                          energy_100g=product['nutriments']['energy_100g'],
                                                          sugars_100g=product['nutriments']['sugars_100g'],
                                                          sodium_100g=product['nutriments']['sodium_100g'],

                                                          )
                                    if created :
                                        for categorie in product['categories_tags']:
                                            try:
                                                add_categorie = Categorie.objects.get(id_category=str(categorie))
                                                add_product.categorie.add(add_categorie)
                                            except:
                                                add_product.delete()


                                except KeyError:
                                    continue

                            count_and_end_page_return_all['count'] = count_f
                            count_and_end_page_return_all['total_count'] = total_count_f
                    except:
                        count_and_end_page_return_all['count'] = False
                        count_and_end_page_return_all['total_count'] = False
                        count_and_end_page_return_all['final_page'] = True

                    return count_and_end_page_return_all

                p = Pool(cpu_count())
                articles_list_all_pool = p.map(function_recovery_and_push, list_page_for_pool)
                p.close()

                # Browse list all articles recovery for count
                for article in articles_list_all_pool:
                    if article['count'] != False and article['total_count'] != False:
                        count += article['count']
                        total_count = article['total_count']

                        if article['final_page'] is True:
                            final_page = article['final_page']

                self.stdout.write(
                    "\rProduct recovery, " + str(percentage_calculation(count, total_count)) + "%" + " done \r")
                sys.stdout.flush()
                range_list[0] += 20
                range_list[1] += 20
                self.stdout.write(
                    "\rProduct recovery, " + str(percentage_calculation(count, total_count)) + "%" + " done \r")
                sys.stdout.flush()

        if options['update_database']:
            self.stdout.write('update database')
