from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import QuoteForm
from .models import Quote
import random


def random_quote(request):
    quotes = list(Quote.objects.all())
    if not quotes:
        return HttpResponse("Цитат пока нет.")

    weights = [q.weight for q in quotes]
    chosen = random.choices(quotes, weights=weights, k=1)[0]

    chosen.views += 1
    chosen.save(update_fields=['views'])

    return render(request, 'random_quote.html', {'quote': chosen})


def like_quote(request, quote_id):
    if request.method == 'POST':
        quote = get_object_or_404(Quote, id=quote_id)
        quote.likes += 1
        quote.save()
    return redirect('random_quote')


def dislike_quote(request, quote_id):
    if request.method == 'POST':
        quote = get_object_or_404(Quote, id=quote_id)
        quote.dislikes += 1
        quote.save()
    return redirect('random_quote')


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Цитата успешно добавлена.")
            return redirect('add_quote')
    else:
        form = QuoteForm()
    return render(request, 'add_quote.html', {'form': form})


def quote_list(request):

    quotes = Quote.objects.all()
    source_filter = request.GET.get('source')
    if source_filter:
        quotes = quotes.filter(source__icontains=source_filter)

    popular_quotes = quotes.order_by('-likes')[:10]

    context = {
        'popular_quotes': popular_quotes,
        'source_filter': source_filter or '',
    }
    return render(request, 'quote_list.html', context)
