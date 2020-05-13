from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from subtitles.services import process_sub
from mimetypes import guess_type
from flashcards.models import MovieSet, Flashcard


@login_required
def sub_processor(request):
    if request.method == 'POST':
        if 'subtitle' in request.FILES:
            uploaded_sub = request.FILES['subtitle']
            name = uploaded_sub.name
            file_type = name[name.rfind('.'):]
            text = uploaded_sub.read()
            result_words, result_text = process_sub(text, file_type, 3)
            new_words = []
            for word, trans in result_words:
                new_words.append("{0} : {1}".format(word, trans))
            request.session['filename'] = name[:name.rfind('.')] + "_enchanted" + file_type
            request.session['content'] = result_text
            request.session['new_words'] = new_words
            return render(request, 'subtitles/succeed.html', {'count': len(new_words), 'name': name[:name.rfind('.')],
                                                              'title': 'Subtitle Result'})
        elif "movie_name" in request.POST:
            movie_set = MovieSet(movie_name=request.POST['movie_name'], user=request.user)
            movie_set.save()
            for line in request.session['new_words']:
                en, fa = line.split(" : ")
                flashcard = Flashcard(english_word=en, translation=fa, movie=movie_set)
                flashcard.save()
            return render(request, 'subtitles/flash_added.html', {'title': 'Subtitle Result'})

    return render(request, 'subtitles/upload.html', {'title': 'Upload Subtitle'})


def download_sub(request):
    filename = request.session['filename']
    content = request.session['content'].encode('utf-8')
    response = HttpResponse(content, content_type=guess_type(filename))
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def download_words_list(request):
    filename = "New words.txt"
    content = "\n".join(request.session['new_words'])
    content.encode("utf-8")
    response = HttpResponse(content, content_type=guess_type(filename))
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
