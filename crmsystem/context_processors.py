
def marks_processor(request):
    marks = Mark.objects.all()            
    return {'marks': marks}