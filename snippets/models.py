from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

# Get the list of all lexers and styles from Pygments and create choices for the language and style fields in the Snippet model
LEXERS = [
    item for item in get_all_lexers() if item[1]
]  # filter out lexers without aliases
LANGUAGE_CHOICES = sorted(
    [(item[1][0], item[0]) for item in LEXERS]
)  # create a list of tuples (alias, name) and sort it
STYLE_CHOICES = sorted(
    [(item, item) for item in get_all_styles()]
)  # create a list of tuples (style, style) and sort it


# Create your models here.
class Snippet(models.Model):
    """A model to represent a code snippet."""

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(
        default=False
    )  # whether to display line numbers or not
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default="python", max_length=100
    )  # the language field will use the choices from LANGUAGE_CHOICES and default to 'python'
    style = models.CharField(
        choices=STYLE_CHOICES, default="friendly", max_length=100
    )  # the style field will use the choices from STYLE_CHOICES and default to 'friendly'

    class Meta:
        """
        Meta options for the Snippet model.
        Orders the snippets by the created field in ascending order.
        """

        ordering = ["created"]
