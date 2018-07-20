from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command
from django.test import TestCase
# Create your tests here.
from food_and_search.models import Product, Categorie
from django.contrib.auth.models import User
class ProductTestCase(TestCase):
    def setUp(self):
        self.fruit = Categorie.objects.create(name='fruit', id_category='fruit_id')
        self.pomme = Product.objects.create(name="pomme",
                                            id=1,
                                            description="une pomme",
                                            nutrition_grade='a',
                                            saturated_fat_100g='9.9',
                                            carbohydrates_100g='9.9',
                                            energy_100g='9.9',
                                            sugars_100g='9.9',
                                            sodium_100g='9.9')
        self.poire = Product.objects.create(name="poire",
                                            id=2,
                                            description="une poire",
                                            nutrition_grade='a',
                                            saturated_fat_100g='9.9',
                                            carbohydrates_100g='9.9',
                                            energy_100g='9.9',
                                            sugars_100g='9.9',
                                            sodium_100g='9.9')
        self.bananne = Product.objects.create(name="bananne",
                                              id=3,
                                              description="une bananne",
                                              nutrition_grade='a',
                                              saturated_fat_100g='9.9',
                                              carbohydrates_100g='9.9',
                                              energy_100g='9.9',
                                              sugars_100g='9.9',
                                              sodium_100g='9.9')
        self.cerise = Product.objects.create(name="cerise",
                                             id=4,
                                             description="une cerise",
                                             nutrition_grade='a',
                                             saturated_fat_100g='9.9',
                                             carbohydrates_100g='9.9',
                                             energy_100g='9.9',
                                             sugars_100g='9.9',
                                             sodium_100g='9.9')
        self.groseille = Product.objects.create(name="groseille",
                                                id=5,
                                                description="une groseille",
                                                nutrition_grade='a',
                                                saturated_fat_100g='9.9',
                                                carbohydrates_100g='9.9',
                                                energy_100g='9.9',
                                                sugars_100g='9.9',
                                                sodium_100g='9.9')
        self.mangue = Product.objects.create(name="mangue",
                                             id=6,
                                             description="une mangue",
                                             nutrition_grade='a',
                                             saturated_fat_100g='9.9',
                                             carbohydrates_100g='9.9',
                                             energy_100g='9.9',
                                             sugars_100g='9.9',
                                             sodium_100g='9.9')
        self.ananas = Product.objects.create(name="ananas",
                                             id=7,
                                             description="un ananas",
                                             nutrition_grade='a',
                                             saturated_fat_100g='9.9',
                                             carbohydrates_100g='9.9',
                                             energy_100g='9.9',
                                             sugars_100g='9.9',
                                             sodium_100g='9.9')
        self.pomme.categorie.add(self.fruit)
        self.ananas.categorie.add(self.fruit)
        self.bananne.categorie.add(self.fruit)
        self.cerise.categorie.add(self.fruit)
        self.groseille.categorie.add(self.fruit)
        self.mangue.categorie.add(self.fruit)
        self.poire.categorie.add(self.fruit)
        self.client = Client()
        self.user = User.objects.create_user('foo', 'foo@bar.com', 'foo#')


    def test_categorie(self):
        categorie = Categorie.objects.get(id_category='fruit_id')
        self.assertEqual(categorie.id_category, 'fruit_id')
        self.assertEqual(categorie.id, 1)
        self.assertEqual(str(categorie), 'fruit')

    def test_product(self):
        product = Product.objects.get(name="pomme")
        self.assertEqual(product.description, 'une pomme')
        self.assertEqual(product.nutrition_grade, 'a')
        self.assertEqual(product.saturated_fat_100g, 9.9)
        self.assertEqual(product.carbohydrates_100g, 9.9)
        self.assertEqual(product.energy_100g, 9.9)
        self.assertEqual(product.sugars_100g, 9.9)
        self.assertEqual(product.sodium_100g, 9.9)
        self.assertEqual(str(product), 'pomme')

    def test_index(self):
        response = self.client.get(reverse('food_and_search:index'))
        self.assertEqual(response.status_code, 200)

    def test_result(self):
        response = self.client.get('/result/', data={'product': 'pomme'})
        self.assertEqual(response.status_code, 200)

    def test_result_raise_error(self):
        response = self.client.get('/result/', data={'product': 'pommier'})
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/result/')
        self.assertEqual(response.status_code, 404)

    def test_save_result_product(self):
        self.client.login(username='foo', password='foo#')
        response = self.client.post("/result/",{'name_product_search':'pomme','product_form': '1'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.post("/result/", {'name_product_search': 'pomme', 'product_form': '1'})
        self.assertEqual(response.status_code, 302)
    def test_saveproduct(self):
        self.client.login(username='foo', password='foo#')
        response = self.client.get(reverse('food_and_search:save_product'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/saveproduct/", {'product_form': '1'})
        self.assertEqual(response.status_code, 200)
        self.client.logout()
    def test_detailproduct(self):
        response = self.client.get(reverse('food_and_search:detailproduct',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('food_and_search:detailproduct', kwargs={'pk': 18}))
        self.assertEqual(response.status_code, 404)
    def test_user_account(self):
        response = self.client.get(reverse('food_and_search:user'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='foo', password='foo#')
        response = self.client.get(reverse('food_and_search:user'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
    def test_signup_account(self):
        response = self.client.post("/signup/", {'username': 'Foo2', 'password1': 'Foo12345','password2':'Foo12345','email':'foo@baar.com'})
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='Foo2')
        self.assertIsNotNone(user)




