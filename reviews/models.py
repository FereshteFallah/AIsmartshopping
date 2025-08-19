from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from textblob import TextBlob

SENTIMENT_CHOICES = [
    ('positive', 'Positive'),
    ('negative', 'Negative'),
    ('neutral', 'Neutral'),
]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    sentiment = models.CharField(max_length=8, choices=SENTIMENT_CHOICES, blank=True)
    score = models.IntegerField(default=3)  # امتیاز از 1 تا 5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def analyze_sentiment(self, content):
        blob = TextBlob(content)
        polarity = blob.sentiment.polarity

        if polarity > 0:
            sentiment = 'positive'
        elif polarity < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        # امتیاز‌دهی بر اساس polarity
        if polarity > 0.5:
            score = 5
        elif polarity > 0:
            score = 4
        elif polarity == 0:
            score = 3
        elif polarity > -0.5:
            score = 2
        else:
            score = 1

        return sentiment, score

    def save(self, *args, **kwargs):
        self.sentiment, self.score = self.analyze_sentiment(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name} (Sentiment: {self.sentiment}, Score: {self.score})"




    def average_sentiment_score(self):
        comments = self.comments.all()
        if not comments:
            return 0  # اگر نظری نبود 0 برگردان

        positive_count = comments.filter(sentiment='positive').count()
        total_count = comments.count()

            # امتیاز در مقیاس 0 تا 10
        score = (positive_count / total_count) * 10
        return round(score, 1)  # عدد رو با یک رقم اعشار برگردون