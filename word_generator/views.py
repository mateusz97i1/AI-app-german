from django.shortcuts import render
import json
from pathlib import Path
from django.http import JsonResponse
import random
from dotenv import load_dotenv
import os
import openai
from .models import Words_db
import string
from django.db.models import Q
import markdown2
load_dotenv()

MODEL_GPT = 'gpt-4o-mini'
api_key=os.getenv('OPENAI_API_KEY')

def home(request):
    list_german_words = list(Words_db.objects.all())
    random_word = None
    result = "Waiting for Your move Boss!"
    rendered_result_html = "" # Initialize an empty string for the HTML result

    if request.method == "POST":
        random_word = random.choice(list_german_words)
        word_text = random_word.german_word

        system_prompt = "You are a german teacher from poland, each word you get in german you have explain them in polish language."
        system_prompt += " Please answer in short markdowns like max 150 words."
        system_prompt += " Create one sentence using this word. Write in markdowns."

        response = openai.chat.completions.create(
            model=MODEL_GPT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": word_text}
            ],
        )

        raw_result_markdown = response.choices[0].message.content
        # Convert markdown to HTML
        rendered_result_html = markdown2.markdown(raw_result_markdown)
        result = raw_result_markdown # You might still want the raw markdown for debugging or other purposes

    return render(request, "home.html", {
        "list_german_words": list_german_words,
        "random_word": random_word,
        "result": result, # This will be the raw markdown
        "rendered_result_html": rendered_result_html # This will be the HTML version
    })


# Create your views here.

def learn_words(request):
    # Get all words from database
    list_german_words = list(Words_db.objects.all())
    
    # Initialize variables
    result = "Press 'Get New Word' to see the first definition"
    result_word = "Read The Hint Below"
    current_word = None
    user_guess = None

    if request.method == "POST":
        # Handle word drawing
        if 'draw' in request.POST:
            if list_german_words:
                current_word = random.choice(list_german_words)
                word_text = current_word.german_word
                
                # Generate hint using OpenAI
                system_prompt = (
                    "You are a German teacher from Poland. Explain this German word in Polish "
                    "without using the word itself. Keep it short (max 80 words)."
                )
                
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": word_text}
                    ],
                )
                
                result = response.choices[0].message.content
                request.session['current_word'] = word_text
                request.session['current_hint'] = result
            else:
                result = "No words available in database"
        
        # Handle guess submission
        elif 'input' in request.POST:
            user_guess = request.POST.get('input', '').strip()
            current_word = request.session.get('current_word')
            result = request.session.get('current_hint', result)
            
            if not current_word:
                result_word = "Please get a word first"
            elif not user_guess:
                result_word = "Please enter a guess"
            else:
                if user_guess.lower() == current_word.lower():
                    result_word = "That's right!"
                    # Clear current word to allow new word drawing
                    request.session.pop('current_word', None)
                else:
                    result_word = f"Correct word is {current_word} !"

    return render(request, "learn.html", {
        "result": result,
        "result_word": result_word,

    })

def dictionary_view(request):
    query = request.GET.get('q', '')
    words = Words_db.objects.all()
    if query:
        words = words.filter(
            Q(german_word__icontains=query) |
            Q(polish_translation__icontains=query)
        )
    context = {'words': words}
    return render(request, 'dictionary.html', context)

def autocomplete_api(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        # Zwracamy listę słowników (z dwoma polami) - można wyświetlać np. "german_word - polish_translation"
        results = list(
            Words_db.objects.filter(
                Q(german_word__icontains=query) |
                Q(polish_translation__icontains=query)
            )
            .values('german_word', 'polish_translation')
            .distinct()[:10]
        )
    return JsonResponse(results, safe=False)