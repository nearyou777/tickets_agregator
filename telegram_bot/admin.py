from flask import Blueprint, render_template, request, redirect, url_for,flash
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
from shared.models import Users, Session, Tickets # Импортируем модели
from datetime import datetime
from math import ceil
# from your_module import session  # Инициализируем сессию для работы с базой данных

# Создаем Blueprint для админской панели
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Главная страница админки
@admin_bp.route('/')
@login_required  # Защищаем админку от неавторизованных пользователей
def index():
    if not current_user.is_superuser:
        return "Access Denied", 403  # Проверяем, является ли текущий пользователь суперпользователем
    return render_template('admin/index.html')

# Страница управления пользователями
@admin_bp.route('/users')
@login_required
def users():
    if not current_user.is_superuser:
        return "Access Denied", 403  # Только суперпользователи могут просматривать пользователей

    # Получаем всех пользователей из базы данных
    with Session() as session:
        users = session.query(Users).all()
    return render_template('admin/users.html', users=users)

# Страница для редактирования пользователя
@admin_bp.route('/users/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_superuser:
        return "Access Denied", 403  # Только суперпользователи могут редактировать пользователей

    with Session() as session:
        user = session.query(Users).get(user_id)  # Находим пользователя по ID
        if user is None:
            return "User not found", 404
        if request.method == 'POST':
            user.Name = request.form['name']
            user.Email = request.form['email']
            subscription_date_str = request.form['subscription_date']  # Строка из формы (формат: 'YYYY-MM-DD')
            print(subscription_date_str)
            try:
                user.SubscriptionDate = datetime.strptime(subscription_date_str, '%Y-%m-%d')
            except ValueError:
                return "Invalid date format", 400 
            
            session.commit()  # Сохраняем изменения в базе данных
            return redirect(url_for('admin.users'))  # Перенаправляем на страницу пользователей

    return render_template('admin/edit_user.html', user=user)

# Страница добавления нового пользователя
@admin_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_superuser:
        return "Access Denied", 403  # Только суперпользователи могут добавлять пользователей

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        with Session() as session:
            new_user = Users(Name=name, Email=email)

            session.add(new_user)
            session.commit()
        return redirect(url_for('admin.users'))  # Перенаправляем на страницу пользователей

    return render_template('admin/add_user.html')


@admin_bp.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    # Количество элементов на странице
    per_page = 10
    # Текущая страница
    page = request.args.get('page', 1, type=int)

    # Получаем параметры сортировки и фильтрации
    sort_by = request.args.get('sort_by', 'date_added')  # Default to sorting by Date Added
    order = request.args.get('order', 'asc')  # Default to ascending order
    start_date = request.args.get('start_date')  # Get the start date from query parameters
    end_date = request.args.get('end_date')  # Get the end date from query parameters

    # Ensure 'order' is either 'asc' or 'desc'
    if order not in ['asc', 'desc']:
        order = 'asc'

    # Открываем сессию
    with Session() as session:
        # Строим запрос для получения тикетов с фильтрацией и сортировкой
        tickets_query = session.query(Tickets)

        # Применяем фильтр по дате, если start_date и end_date предоставлены
        if start_date and end_date:
            # Преобразуем строки в дату
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            tickets_query = tickets_query.filter(Tickets.DateAdded.between(start_date, end_date))

        # Применяем сортировку
        if sort_by == 'date_added':
            if order == 'asc':
                tickets_query = tickets_query.order_by(Tickets.DateAdded.asc())
            else:
                tickets_query = tickets_query.order_by(Tickets.DateAdded.desc())

        # Получаем количество тикетов после фильтрации
        total_tickets = tickets_query.count()

        # Запрашиваем тикеты для текущей страницы с пагинацией
        tickets = tickets_query.offset((page - 1) * per_page).limit(per_page).all()

    # Количество страниц
    total_pages = ceil(total_tickets / per_page)

    return render_template('admin/tickets.html', tickets=tickets, page=page, total_pages=total_pages, sort_by=sort_by, order=order, start_date=start_date, end_date=end_date)


@admin_bp.route('/tickets/edit_ticket/<string:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    with Session() as session:
        ticket = session.query(Tickets).get(ticket_id)
        
        if ticket is None:
            return "Ticket not found", 404
        
        if request.method == 'POST':
            # Обновляем поля билета из формы
            ticket.Title = request.form['title']
            ticket.Type = request.form['type']
            ticket.Cabin = request.form['cabin']
            ticket.Price = request.form['price']
            ticket.OriginalPrice = request.form['original_price']
            ticket.Dates = request.form['dates']
            ticket.Book = request.form['book']
            ticket.DepartureCities = request.form['departure_cities']
            ticket.DepartureAirports = request.form['departure_airports']
            ticket.BookGuide = request.form['book_guide']
            ticket.Summary = request.form['summary']
            ticket.PictureName = request.form['picture_name']
            ticket.DateAdded = datetime.utcnow()
            
            session.commit()  # Сохраняем изменения в базе данных
            return redirect(url_for('admin.tickets'))  # Перенаправляем на страницу билетов
        
    return render_template('admin/edit_ticket.html', ticket=ticket)

@admin_bp.route('/tickets/delete/<ticket_id>', methods=['POST'])
def delete_ticket(ticket_id):
    with Session() as session:
        ticket = session.query(Tickets).get(ticket_id)
        if ticket:
            session.delete(ticket)
            session.commit()
            flash('Ticket deleted successfully!', 'success')
        else:
            flash('Ticket not found!', 'danger')
        
        return redirect(url_for('admin.tickets'))  # Redirect back to the tickets list

@admin_bp.route('/tickets/new_ticket', methods=['GET', 'POST'])
@login_required
def new_ticket():
    if request.method == 'POST':
        # Получаем данные из формы
        new_ticket = Tickets(
            Title=request.form['title'],
            Type=request.form['type'],
            Cabin=request.form['cabin'],
            Price=request.form['price'],
            OriginalPrice=request.form['original_price'],
            Dates=request.form['dates'],
            Book=request.form['book'],
            DepartureCities=request.form['departure_cities'],
            DepartureAirports=request.form['departure_airports'],
            BookGuide=request.form['book_guide'],
            Summary=request.form['summary'],
            PictureName=request.form['picture_name'],
            DateAdded=datetime.utcnow()
        )

        with Session() as session:
            session.add(new_ticket)  # Добавляем новый билет в сессию
            session.commit()  # Сохраняем изменения в базе данных

        return redirect(url_for('admin.tickets'))  # Перенаправляем на страницу билетов

    return render_template('admin/new_ticket.html')