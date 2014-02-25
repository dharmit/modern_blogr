import math
import calendar
from operator import itemgetter

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.session import check_csrf_token

from .models import (
    DBSession,
    User,
    Entry,
    Tag,
    )

from .pagination import Pagination
from .forms import (
    BlogCreateForm,
    BlogUpdateForm,
    )

PER_PAGE = 5


@view_config(route_name='home', renderer='home.mako')
@view_config(route_name='home:page', renderer='home.mako')
def home_view(request):
    page = int(request.matchdict.get('page', 1))
    count = DBSession.query(Entry).count()
    entries = Entry.get_page(page, PER_PAGE)

    if not entries and page != 1:
        raise HTTPNotFound()

    pagination = Pagination(page, PER_PAGE, count)

    return dict(
        section='home',
        entries=entries,
        pagination=pagination,
        logged_in=authenticated_userid(request),
        )


@view_config(route_name='blog', renderer='view_blog.mako')
def blog_view(request):
    id = int(request.matchdict.get('id', -1))
    entry = Entry.by_id(id)
    if not entry:
        raise HTTPNotFound()
    return dict(
        entry=entry,
        logged_in=authenticated_userid(request),
        )


@view_config(route_name='blog_action',
             match_param='action=create',
             renderer='edit_blog.mako',
             permission='create')
def blog_create(request):
    entry = Entry()
    form = BlogCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        user = User.by_name(authenticated_userid(request))
        entry = Entry(
            title=form.title.data,
            body=form.body.data,
            user_id=user.id,
            tags=form.tags.data,
            )
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return dict(
        form=form,
        action=request.matchdict.get('action'),
        logged_in=authenticated_userid(request),
        )


@view_config(route_name='blog_action',
             match_param='action=edit',
             renderer='edit_blog.mako',
             permission='edit')
def blog_update(request):
    id = int(request.params.get('id', -1))
    entry = Entry.by_id(id)
    if not entry:
        raise HTTPNotFound()
    form = BlogUpdateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        return HTTPFound(location=request.route_url('blog', id=entry.id,
                                                    slug=entry.slug))
    return dict(
        form=form,
        action=request.matchdict.get('action'),
        logged_in=authenticated_userid(request),
        )


@view_config(route_name='archive', renderer='archive.mako')
def archives_view(request):
    year = request.matchdict.get('year')
    month = request.matchdict.get('month')
    try:
        year = int(year)
        month = int(month)
        if month < 1 or month > 12:
            raise ValueError
    except ValueError:
        raise HTTPNotFound()

    fullname = "%s, %s" % (calendar.month_name[month], year)
    entries = Entry.get_month(year, month)

    return dict(
        fullname=fullname,
        entries=entries,
        logged_in=authenticated_userid(request),
        )


@view_config(route_name='tag', renderer='view_tag.mako')
def tag_view(request):
    tag_name = request.matchdict.get('tag_name')
    return dict(
        tag_name=tag_name,
        entries = Entry.by_tag_name(tag_name),
        logged_in=authenticated_userid(request),
        )


@view_config(route_name='tags', renderer='tags.mako')
def tags_view(request):
    totalcounts = []
    for tag in Tag.tag_counts():
        weight = int((math.log(tag[1] or 1) * 4) + 10)
        totalcounts.append((tag[0], tag[1], weight))
    tags = sorted(totalcounts, key=itemgetter(0))

    return dict(
        section='tags',
        tags=tags,
        logged_in=authenticated_userid(request),
        )


@view_config(route_name='about', renderer='about.mako')
def about_view(request):
    return dict(
        section='about',
        logged_in=authenticated_userid(request),
        )


@view_config(route_name='login', renderer='login.mako')
@forbidden_view_config(renderer='login.mako')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        user = User.by_name(login)
        if user and user.verify_password(password):
            headers = remember(request, login)
            return HTTPFound(location=came_from,
                             headers=headers)
        message = 'Failed login'

    return dict(
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(request):
    request.response.status = '404 Not Found'
    return {}
