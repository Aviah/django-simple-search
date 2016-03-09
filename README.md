
# Dajngo Simple Search

A full text search app without installing any other tool. It uses the databases native full text search.

There are probably better solutions for scaled search, but if you need a basic search, up and running, without too much hustle and configs, this app is an easy solution.

*Note: The app was tested on MySQL. For other databases please review and adjust the sql statments on app_settings.py, migrations/0001_initial.py*


## Installation

1. Add the app, the "search" directory. to your django project (the app directory name should be "search").
2. Install sqlparse (for migrations):

		$ sudo pip install sqlparse
		
3. Add the app to the INSTALLED_APPS
4. Edit the initial migration file:

		$ nano search/migrations/0001_initial.py
		mig_sql = MySQL_5_6 # for MySQL versions prior to 5.7
		mig_sql = MySQL_5_7 # for MySQL versions from 5.7
5. If you are not using MySQL, edit and adjust the SQL in 0001_initial.py migration, and app_settings.py
6. Run migrations:

		$ ./manage.py migrate
		
		
## Settings

If you want to change the search defaults, add SEARCH_SETTINGS dictionary to your main project settings.py file. These are the search settings and defaults:

	SEARCH_SETTINGS = {
		'MIN_LENGTH_SEARCH_QUERIES': 4,
		'WILDCARD': "*",
		'AUTO_WILDCARD': True,
		'MAX_ENTRIES': 100,
		'SELECT': sql
		}
		
**MIN_LENGTH_SEARCH_QUERIES**    
Minimum lenghth of the search term. When MIN_LENGTH_SEARCH_QUERIES = 4, search term like "ABC" is ignored

**WILDCARD**    
The wildcard character, adjust to your database. In MySQL it's "*", the default.

**AUTO_WILDCARD**    
Add wildcard to any search query. The default is True, so searching for "books" is actually searching for "books*"

**MAX_ENTRIES**    
The sql LIMIT to the search query.

**SELECT**    
The search query SQL. The default works for MySQL, adjust if required for another database

## Saving an Entry to the Search Index

Entries are saved automatically when you save an object (with a post_save signal).

Just add to every model that you want to index a 'SearchConfig' class, with the fields to be indexed, as follows:


	class Product(models.Model):
	
		class SearchConfig:
			item_name_field = 'product_name'
			search_fields = ['category','description']
						
		product_name = models.CharField(max_length=50)
		price = models.FloatField()
		category = models.CharField(max_length=50)
		description = models.CharField(max_length=50)
		notes =  models.CharField(max_length=200)
		
		
In this example, the search item name, which it the text that will show on the search results, is 'product_name'. The search index will also index the 'category' and 'description' fields. The 'notes' fields will not be indexed.

If you want to index only the item name, use empty list for the seach fields:


	class Polls(models.Model):
	
		class SearchConfig:
			item_name_field = 'question_text'
			search_fields = []			
			
		question_text = models.CharField(max_length=200)
		pub_date = models.DateTimeField('date published)
		
		
## Running Search

Searching is very simple:

	from search.models import SearchItems
	...
	items = SearchItems.search('foobar')
	
This returns a list with search results for 'foobar'.Use "items" in your views and templates.

The results list, 'items', is a list of dictionaries of all found objects.    
Note that 'items' has **mixed objects**, since it pulls objects from  different models.    
The 'items' results will look like:

	[{'name':'product1','object':<django model object>},
	{'name':'product2','object':<django model object>},
	{'name':'contact1','object':<django model object>},…
	]
	

Note that ins this example, results include both a "product" object and "contact" object. This can happen if the search indexed matched both obejcts, say product "foobar Phone" and contact "foobar Smith".


To get a set of the search results **objects**, similar to a queryset:


	search_results_objects = [x[object] for x in items]
	
You can use the "object" attribute in your code and templates, just make sure you use only the attributes and methods that are common to all objects.


A search results template may look like:

	{% for item in items %}
		<p> <a href="{{ item.object.get_absolute_url }}"> {{ item.name }} </a> </p>		
	{% endfor %}
	
	
Since all objects should have a get_absolute_url method, this code will work for the entire search results.

See the example view and template in the app.


## Loading Exsiting Data to the Search Index

The search index is automatically updated when you save an object, so every new entry, or updated entry, will be saved to the search index.

However, if there is already data in the models, before you installed the search app, you can load it in bulk to the search index.    

The search index updates with a post_save signal, so looping through all objects and saving them will create the search index entries for existing data.

A script to load all objects from a model will look like this:

		import os
		# use the same settings as in your manage.py file
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_repo.settings")
		os.environ['DJANGO_SETTINGS_MODULE'] = "site_repo.settings"
		
		import django
		django.setup()
		
		# add SearchConfig to Product before running this script
		from site_repo.products.models import Product 		
		products = Product.objects.all()
		for product in products:
			product.save()
			
Run a similar script for every model you need to load to the search index, after adding **SearchConfig** to the model.

*Note: Such script will trigger the model's validation for each save. You may have to ignore this validation temporarily, e.g. when the validation does not allow to save record from past dates.*
		


## User Specific Search


The search app, by default, searches every entry in the model. 

If you need to limit the search only to the user's records, you will have to add a user field:


1. The SearchItems model: add a user field
2. The SearchResultsManager: add a user criteria to the queryset and the search method
3. Add user_id field to the SQL in  migrations/0001_initial.py and app_settings.py.

For a complete example of user-based search results see the [Example Project](https://github.com/aviah/example_project/master/readme.md)



		
		

		
		
	



		
		

	






	
	
	
