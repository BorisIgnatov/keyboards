from keyboard.models import Review

def review(request, keyboard):
        review = Review(user=request.user,keyboard=keyboard,
                        rating=request.POST.get('rating'),
                        content=request.POST.get('content'),
                        is_positive=request.POST.get('is_positive') == 'True')

        review.save()
        
        keyboard.save()
