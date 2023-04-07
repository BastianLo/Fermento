from django.shortcuts import redirect

def set_language(request):
    language_code = request.POST.get('language')
    next_url = request.POST.get('next')
    if language_code and check_for_language(language_code):
        response = redirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
        return response
    return redirect('home')
