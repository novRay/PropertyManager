# coding: utf-8
from exts import db
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import Post, Comment

post_bp = Blueprint('post', __name__)


@post_bp.route('/posts')
@login_required
def view_posts():
    # 查询所有帖子并按ID降序排列
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('post/view_posts.html', posts=posts, user=current_user)


@post_bp.route('/post/<int:post_id>')
@login_required
def view_post(post_id):
    post = Post.query.get(post_id)
    # 查询当前帖子下所有评论并按ID降序排列
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.id.desc()).all()
    return render_template('post/view_post.html', post=post, comments=comments, comment_cnt=len(comments),
                           user=current_user)


@post_bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post.view_posts'))
    return render_template('post/new_post.html', user=current_user)


@post_bp.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    content = request.form.get('content')
    new_comment = Comment(content=content, post_id=post_id, user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('post.view_post', post_id=post_id))


@post_bp.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    # 只有管理员可以删帖
    if post and current_user.is_admin:
        # 查询当前帖子下的全部评论
        comments = Comment.query.filter_by(post_id=post.id).all()

        # 删除所有评论，再删除当前帖子
        [db.session.delete(comment) for comment in comments]
        db.session.delete(post)
        db.session.commit()
    else:
        flash('你没有权限删除这个帖子', 'error')
    return redirect(url_for('post.view_posts'))


@post_bp.route('/delete_comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    post_id = comment.post_id
    if comment and current_user.is_admin:
        db.session.delete(comment)
        db.session.commit()
    else:
        flash('你没有权限删除这个评论', 'error')
    return redirect(url_for('post.view_post', post_id=post_id))
