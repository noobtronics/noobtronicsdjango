from mysite import settings



def webpack_processor(request):
    my_dict = {
        'webpack_js': settings.webpack_js,
        'webpack_css': settings.webpack_css,
    }

    return my_dict
