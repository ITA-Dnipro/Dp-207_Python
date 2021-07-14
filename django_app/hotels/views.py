from django.shortcuts import render

def first(request):
    return render(request, 'hotels/hotels_list.html')
