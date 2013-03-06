from django.template import Template, Context
from django.conf import settings
from debug_toolbar.panels import DebugPanel

from subprocess import check_output, CalledProcessError

GIT_COMMIT_COUNT = getattr(settings, 'GIT_COMMIT_COUNT', 20)
GIT_COMMIT_FIELDS = ['id', 'author_name', 'author_email', 'date', 'message']
GIT_LOG_FORMAT = ['%h', '%an', '%ae', '%cd', '%s']
GIT_LOG_FORMAT = '%x1f'.join(GIT_LOG_FORMAT) + '%x1e'

try:
    log = check_output(["git", "log", "-%i" % GIT_COMMIT_COUNT, "--format=%s" % GIT_LOG_FORMAT]).strip("\"\n")
    log = log.strip('\n\x1e').split("\x1e")
    log = [row.strip().split("\x1f") for row in log]
    GIT_LOG = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in log]
except CalledProcessError, e:
    GIT_LOG = []

_TEMPLATE_MARKUP = """<table>
    <thead>
        <th>ID</th>
        <th>Date</th>
        <th>Author</th>
        <th>Message</th>
    </thead>
    <tbody>
        {% for row in log %}
        <tr class="{% cycle 'djDebugOdd' 'djDebugEven' %}">
            <td>
                {% if commit_url %}
                <a href="{{ commit_url }}{{ row.id }}">{{ row.id }}</a>
                {% else %}
                {{ row.id }}
                {% endif %}
            </td>
            <td>{{ row.date }}</td>
            <td>{{ row.author_name }}</td>
            <td>{{ row.message }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
"""


class RecentCommitsDebugPanel(DebugPanel):
    """
    Panel that displays the latest commit date
    """
    name = "Last Commit"
    has_content = True
    template = Template(_TEMPLATE_MARKUP)

    def nav_title(self):
        return "Last Commit"

    def nav_subtitle(self):
        if GIT_LOG:
            return GIT_LOG[0]['date']
        return ""

    def url(self):
        return ''

    def title(self):
        return "Recent Commits"

    def content(self):
        context = self.context.copy()
        context.update({
            'log': GIT_LOG,
            'commit_url': getattr(settings, 'GIT_COMMIT_URL', False)
        })
        return self.template.render(Context(context))
