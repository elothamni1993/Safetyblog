from flask import render_template, request, Blueprint
from flask_login import current_user  # Import current_user from flask_login
from flaskblog.models import Post
from flaskblog.posts.forms import CommentForm

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        # Display blog posts if user is logged in
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        form = CommentForm()  # Assuming you want to add comments functionality when logged in
        return render_template('home.html', posts=posts, form=form)
    else:
        # Display landing page if user is not logged in
        return render_template('welcome.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')

