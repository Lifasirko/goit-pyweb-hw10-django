import requests
from bs4 import BeautifulSoup
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import AuthorForm, QuoteForm, SignUpForm
from .models import Quote, Author


def home(request):
    quotes_list = Quote.objects.all()
    for quote in quotes_list:
        quote.tags_list = quote.tags.split(',') if quote.tags else []

    paginator = Paginator(quotes_list, 10)  # Кількість цитат на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    top_tags = get_top_tags()  # Отримуємо топ-теги

    context = {
        'page_obj': page_obj,
        'top_tags': top_tags,
    }
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Перенаправлення на головну сторінку з урахуванням простору імен
            return redirect('quotes:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            # Перенаправлення на головну сторінку з урахуванням простору імен
            return redirect('quotes:home')
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            # Перенаправлення на головну сторінку з урахуванням простору імен
            return redirect('quotes:home')
    else:
        form = QuoteForm()
    return render(request, 'add_quote.html', {'form': form})


def quotes_by_tag(request, tag):
    quotes_list = Quote.objects.filter(tags__icontains=tag)
    for quote in quotes_list:
        quote.tags_list = quote.tags.split(',') if quote.tags else []

    paginator = Paginator(quotes_list, 10)  # Кількість цитат на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_tags = set()
    for quote in Quote.objects.all():
        if quote.tags:
            all_tags.update(quote.tags.split(','))

    context = {
        'tag': tag,
        'page_obj': page_obj,
        'all_tags': sorted(all_tags),
    }
    return render(request, 'quotes_by_tag.html', context)


def get_top_tags():
    tags = Quote.objects.values_list('tags', flat=True)  # Отримати всі теги
    tag_count = {}
    for tag_list in tags:
        for tag in tag_list.split(','):
            if tag.strip():  # Перевіряємо, щоб тег не був пустим
                tag_count[tag] = tag_count.get(tag, 0) + 1

    # Сортування тегів за кількістю появ і відбір топ-10
    top_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_tags


def scrap_quotes(request):
    url = 'http://quotes.toscrape.com'
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.select('div.quote')
        for quote in quotes:
            text = quote.select_one('span.text').get_text(strip=True).strip('“”')
            author_name = quote.select_one('small.author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.select('div.tags a.tag')]

            author, created = Author.objects.get_or_create(name=author_name)
            Quote.objects.get_or_create(
                text=text,
                author=author,
                defaults={'tags': ','.join(tags)}
            )

        next_button = soup.select_one('li.next a')
        url = next_button['href'] if next_button else None
        if url:
            url = 'http://quotes.toscrape.com' + url

    return redirect('quotes:home')
