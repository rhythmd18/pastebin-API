from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

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

    # whether to display line numbers or not
    linenos = models.BooleanField(default=False)

    # the language field will use the choices from LANGUAGE_CHOICES and default to 'python'
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default="python", max_length=100
    )

    # the style field will use the choices from STYLE_CHOICES and default to 'friendly'
    style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)

    # the owner field is a foreign key to the User model
    owner = models.ForeignKey(
        "auth.User", related_name="snippets", on_delete=models.CASCADE
    )

    # to store the highlighted HTML representation of the code snippet
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        # get the lexer for the specified language
        lexer = get_lexer_by_name(self.language)
        # determine the line numbers option based on the linenos field
        linenos = "table" if self.linenos else False
        # create the formatter with the specified style and line numbers option
        # create the formatter for the highlighted code
        formatter = HtmlFormatter(style=self.style, linenos=linenos)
        # highlight the code and save it to the highlighted field
        self.highlighted = highlight(self.code, lexer, formatter)
        # call the parent class's save method to save the model instance
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta options for the Snippet model.
        Orders the snippets by the created field in ascending order.
        """

        ordering = ["created"]
