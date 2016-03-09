from django.http import Http404
from django.shortcuts import render
from django.views import generic

from .models import SearchItems
from .forms import SearchForm

class SearchView(generic.ListView):
    
    template_name = "search_results.html"
    search_query = None
    
    def get_queryset(self):
        
        try:
            q = SearchForm({'search_query':self.request.GET['q']})
            assert q.is_valid()
            self.search_query = q.cleaned_data['search_query']
            queryset = SearchItems.items.search(self.search_query) 
            return queryset
        
        except:
            raise
        
        
    def get_context_data(self,*args,**kwargs):
        
        context = super(SearchView,self).get_context_data(*args,**kwargs)
        context['search_query'] = self.search_query
        return context
        
    