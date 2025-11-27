from django.http import HttpResponse, JsonResponse
from django.urls import reverse

def index(request):
    """
    Simple landing page / root endpoint for quick developer access.
    Returns an HTML response with links to main endpoints.
    """
    # build simple HTML with links
    html = """
    <!doctype html>
    <html>
      <head><meta charset="utf-8"><title>Credit Risk Backend</title></head>
      <body style="font-family:system-ui,Segoe UI,Roboto,Arial;line-height:1.6;padding:24px">
        <h1>Credit Risk Scoring Backend</h1>
        <p>Available endpoints (development):</p>
        <ul>
          <li><a href="/admin/">Admin</a></li>
          <li><a href="/api/users/">Users API</a></li>
          <li><a href="/api/applications/">Applications API</a></li>
          <li><a href="/api/ml/score">ML Score (POST)</a> (POST with JSON)</li>
        </ul>
        <p>Tip: use <code>/api/applications/</code> to create an application that triggers scoring.</p>
      </body>
    </html>
    """
    return HttpResponse(html)
