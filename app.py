from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_wtf import CSRFProtect
from extensions import db, login_manager
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, TaskForm, SignupForm, TimetableEntryForm, ProfileForm
from models import User, Task, TimetableEntry
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = SignupForm()
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
            return redirect(url_for('login'))
        return render_template('signup.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        form = ProfileForm(obj=current_user)
        if form.validate_on_submit():
            current_user.username = form.username.data
            if form.password.data:
                current_user.set_password(form.password.data)
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        return render_template('profile.html', form=form)

    @app.route('/tasks', methods=['GET', 'POST'])
    @login_required
    def tasks():
        form = TaskForm()
        if form.validate_on_submit():
            task = Task(
                description=form.description.data,
                due_date=form.due_date.data,
                time=form.time.data,
                priority=form.priority.data,
                completed=form.completed.data,
                user_id=current_user.id
            )
            db.session.add(task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('tasks'))
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return render_template('tasks.html', form=form, tasks=tasks)

    @app.route('/toggle_task/<int:task_id>', methods=['POST'])
    @login_required
    def toggle_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            flash('You do not have permission to modify this task.', 'danger')
            return redirect(url_for('tasks'))
        task.completed = not task.completed
        db.session.commit()
        flash('Task status updated.', 'success')
        return redirect(url_for('tasks'))

    @app.route('/delete_task/<int:task_id>', methods=['POST'])
    @login_required
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            flash('You do not have permission to delete this task.', 'danger')
            return redirect(url_for('tasks'))
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted.', 'success')
        return redirect(url_for('tasks'))

    @app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
    @login_required
    def edit_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            flash('You do not have permission to edit this task.', 'danger')
            return redirect(url_for('tasks'))
        form = TaskForm(obj=task)
        if form.validate_on_submit():
            task.description = form.description.data
            task.due_date = form.due_date.data
            task.time = form.time.data
            task.priority = form.priority.data
            task.completed = form.completed.data
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('tasks'))
        return render_template('edit_task.html', form=form, task=task)
    
    @app.route('/timetable')
    @login_required
    def timetable():
        entries = TimetableEntry.query.order_by(TimetableEntry.start_time).all()
        return render_template('timetable.html', entries=entries)
    
    @app.route('/timetable/add', methods=['GET', 'POST'])
    @login_required
    def add_timetable_entry():
        form = TimetableEntryForm()
        if form.validate_on_submit():
            entry = TimetableEntry(
                title=form.title.data,
                description=form.description.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data
            )
            db.session.add(entry)
            db.session.commit()
            flash('Timetable entry added successfully!', 'success')
            return redirect(url_for('timetable'))
        return render_template('add_timetable_entry.html', form=form)
    
    @app.route('/timetable/edit/<int:entry_id>', methods=['GET', 'POST'])
    @login_required
    def edit_timetable_entry(entry_id):
        entry = TimetableEntry.query.get_or_404(entry_id)
        form = TimetableEntryForm(obj=entry)
        if form.validate_on_submit():
            entry.title = form.title.data
            entry.description = form.description.data
            entry.start_time = form.start_time.data
            entry.end_time = form.end_time.data
            db.session.commit()
            flash('Timetable entry updated successfully!', 'success')
            return redirect(url_for('timetable'))
        return render_template('edit_timetable_entry.html', form=form, entry=entry)
    
    @app.route('/timetable/delete/<int:entry_id>', methods=['POST'])
    @login_required
    def delete_timetable_entry(entry_id):
        entry = TimetableEntry.query.get_or_404(entry_id)
        db.session.delete(entry)
        db.session.commit()
        flash('Timetable entry deleted successfully!', 'success')
        return redirect(url_for('timetable'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)