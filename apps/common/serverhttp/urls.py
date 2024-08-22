from django.urls import path, re_path

from .views import HttpRequestAttakView

app_name = 'serverhttp'

urlpatterns = [
    re_path(
        r'^.*[Ss][Ee][Tt][Uu][Pp].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Ee][Nn][Vv].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Pp][Hh][Pp][Mm][Yy][Aa][Dd][Mm][Ii][Nn].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Ww][Ee][Pp][Mm][Yy][Aa][Dd][Mm][Ii][Nn].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Hh][Tt][Mm][Ll].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Tt][Xx][Tt].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Ww][Ee][Ll][Ll]-?[Kk][Nn][Oo][Ww][Nn].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Pp][Hh][Pp].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Ww][Oo][Rr][Dd][Pp][Rr][Ee][Ss][Ss].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Oo][Ll][Dd][Ss][Ii][Tt][Ee].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Ww][Pp]-[Oo][Ll][Dd].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Tt][Ee][Ss][Tt].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Bb][Aa][Cc][Kk][Uu][Pp].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Ss][Ii][Tt][Ee].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Oo][Ll][Dd].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Ss][Hh][Oo][Pp].*',
        HttpRequestAttakView.as_view()
    ),
    re_path(
        r'^.*[Ww][Pp].*',
        HttpRequestAttakView.as_view()
    )
]
