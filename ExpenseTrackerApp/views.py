from django.shortcuts import render, redirect
from ExpenseTrackerApp.models import transaction_details, categories
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
from dateutil.relativedelta import *

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('/transaction-history')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                if User.objects.filter(username = username).exists():
                    messages.info(request, 'user already exists')
                    return redirect('/register')
                elif User.objects.filter(email = email).exists():
                    messages.info(request, 'email id already exists')
                    return redirect('/register')
                else:
                    user = User(username= username, email = email)
                    user.set_password(password)
                    user.save()
                    user_login = authenticate(username = username, password=password)
                    login(request, user_login)
                    return redirect('/transaction')
            else:
                messages.info(request, "passwords don't match")  
                return redirect('/register')
        else:
            return render(request,'register.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/transaction-history')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username, password= password)
            if user is not None:
                login(request, user)
                return redirect('/transaction-history')
            else:
                messages.info(request, 'Invalid username and password combination. Please try again.')
                return redirect('/login')
        else:
            return render(request,'login.html')

def login_again(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password= password)
        if user is not None:
            login(request, user)
            return redirect('/transaction-history')
        else:
            messages.info(request, 'Invalid username and password combination. Please try again.')
            return redirect('/login')
    else:
        return render(request,'login_again.html')

def add_transaction(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            date = request.POST.get('date')
            amount = request.POST.get('amount')
            category = request.POST.get('category')
            transaction_type = request.POST.get('type')
            note = request.POST.get('note')
            transaction_detail = transaction_details(user_id  = request.user, date = date, amount = 
            amount, category = category, transaction_type = transaction_type, note = note)
            transaction_detail.save()
            return redirect('/transaction-history')
        else:
            return render(request,'add_transaction.html')
    else:
        return redirect('/login')

def transaction_history(request):
    if request.user.is_authenticated:
        transaction_detail = transaction_details.objects.filter(user_id = request.user).order_by('-date')
        paginator = Paginator(transaction_detail, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        context = {
            'transaction_detail': transaction_detail,
            'page_obj' : page_obj
        }
        return render(request, 'transaction_history.html', context)
    else:
        return redirect('/login')

def load_categories(request):
    type = request.GET.get('type')
    category_list = categories.objects.filter(type = type)
    return render(request, 'add_transaction_category.html', {'category_list': category_list})

def change_password(request):
    if request.method =='POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            if User.objects.filter(email = email).exists():
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return redirect('/login_again')
            else:
                messages.info(request, 'Please enter valid email-id.')
                return redirect('/change-password')
        else:
            messages.info(request, "passwords don't match")  
            return redirect('/change-password')
    else:
        return render(request,'change_password.html')

def report(request):
    if request.user.is_authenticated:
        incomes = transaction_details.objects.filter(user_id = request.user, date__month = datetime.now().strftime('%m'), transaction_type = "Income")
        expenses = transaction_details.objects.filter(user_id = request.user, date__month = datetime.now().strftime('%m'), transaction_type = "Expense")
        income_amount = []
        expense_amount  = []
        for i in incomes:
            income_amount.append(i.amount)

        for i in expenses:
            expense_amount.append(i.amount)

        def total_amount(list):
            total = 0
            for i in range(len(list)):
                total += list[i]
            return total

        total_income = total_amount(income_amount)
        total_expense = total_amount(expense_amount)
        net_balance =  total_income - total_expense
        balance = abs(total_income - total_expense)
        
        return render(request,'report.html', {'total_income': total_income, 'total_expense' : total_expense, 'net_balance' : net_balance, 'balance': balance })
    
    else:
        return redirect('/login')

def current_month_link(request):
    return render(request, 'current_month_link.html')

def previous_month_link(request):
    return render(request, 'previous_month_link.html')

def current_month_amount(request):
    incomes = transaction_details.objects.filter(user_id = request.user, date__month = datetime.now().strftime('%m'), transaction_type = "Income")
    expenses = transaction_details.objects.filter(user_id = request.user, date__month = datetime.now().strftime('%m'), transaction_type = "Expense")
    income_amount = []
    expense_amount  = []
    for i in incomes:
        income_amount.append(i.amount)

    for i in expenses:
        expense_amount.append(i.amount)

    def total_amount(list):
        total = 0
        for i in range(len(list)):
            total += list[i]
        return total

    total_income = total_amount(income_amount)
    total_expense = total_amount(expense_amount)
    net_balance =  total_income - total_expense
    balance = abs(total_income - total_expense)
        
    return render(request,'total_amount.html', {'total_income': total_income, 'total_expense' : total_expense, 'net_balance' : net_balance, 'balance': balance })

def previous_month_amount(request):
    one_month_ago = datetime.now() - relativedelta(months=1)
    previous_month = one_month_ago.strftime("%m")
    incomes = transaction_details.objects.filter(user_id = request.user, date__month = previous_month, transaction_type = "Income")
    expenses = transaction_details.objects.filter(user_id = request.user, date__month = previous_month, transaction_type = "Expense")
    income_amount = []
    expense_amount  = []
    for i in incomes:
        income_amount.append(i.amount)

    for i in expenses:
        expense_amount.append(i.amount)

    def total_amount(list):
        total = 0
        for i in range(len(list)):
            total += list[i]
        return total

    total_income = total_amount(income_amount)
    total_expense = total_amount(expense_amount)
    net_balance =  total_income - total_expense
    balance = abs(total_income - total_expense)
        
    return render(request,'total_amount.html', {'total_income': total_income, 'total_expense' : total_expense, 'net_balance' : net_balance, 'balance': balance })


def current_month_report_display(request):
    expenses = transaction_details.objects.filter(user_id = request.user, date__month = datetime.now().strftime('%m'), transaction_type = "Expense")
    finaldict = {}
            
    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category = category)

        for item in filtered_by_category:
            amount += item.amount
                
        return amount

    for x in category_list:
        finaldict[x] = get_expense_category_amount(x)

    return JsonResponse({'data': finaldict} , safe = False)

def previous_month_report_display(request):
    one_month_ago = datetime.now() - relativedelta(months=1)
    previous_month = one_month_ago.strftime("%m")
    expenses = transaction_details.objects.filter(user_id = request.user, date__month = previous_month, transaction_type = "Expense")
    finaldict = {}
            
    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category = category)

        for item in filtered_by_category:
            amount += item.amount
                
        return amount

    for x in category_list:
        finaldict[x] = get_expense_category_amount(x)

    return JsonResponse({'data': finaldict} , safe = False)

def daywise_current_month_report_display(request):
    expenses = transaction_details.objects.filter(user_id = request.user, date__month = datetime.now().strftime('%m'), transaction_type = "Expense")
    finaldict = {}

    def days_cur_month(m):
        y = datetime.now().year
        ndays = (date(y, m+1, 1) - date(y, m, 1)).days
        print(ndays)
        print(type(m))
        d1 = date(y, m, 1)
        d2 = date(y, m, ndays)
        delta = d2 - d1

        return [(d1 + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

    def get_expense_date_amount(date):
        amount = 0
        filtered_by_date = expenses.filter(date = date)

        if filtered_by_date is None:
            return 0
        else:
            for item in filtered_by_date:
                amount += item.amount
            return amount
    
    current_month_date_list = days_cur_month(datetime.now().month)

    for x in current_month_date_list:
        finaldict[x] = get_expense_date_amount(x)

    return JsonResponse({'data': finaldict} , safe = False)

def daywise_previous_month_report_display(request):
    one_month_ago = datetime.now() - relativedelta(months=1)
    previous_month = one_month_ago.strftime("%m")
    expenses = transaction_details.objects.filter(user_id = request.user, date__month = previous_month, transaction_type = "Expense")
    finaldict = {}

    def days_pre_month(m):
        y = datetime.now().year
        ndays = (date(y, m+1, 1) - date(y, m, 1)).days
        d1 = date(y, m, 1)
        d2 = date(y, m, ndays)
        delta = d2 - d1

        return [(d1 + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

    def get_expense_date_amount(date):
        amount = 0
        filtered_by_date = expenses.filter(date = date)

        if filtered_by_date is None:
            return 0
        else:
            for item in filtered_by_date:
                amount += item.amount
            return amount
    
    current_month_date_list = days_pre_month(one_month_ago.month)

    for x in current_month_date_list:
        finaldict[x] = get_expense_date_amount(x)

    return JsonResponse({'data': finaldict} , safe = False)

def current_month_report(request):
    if request.user.is_authenticated:
        incomes = transaction_details.objects.filter(user_id = request.user, date__month = datetime.now().strftime('%m'), transaction_type = "Income")
        expenses = transaction_details.objects.filter(user_id = request.user, date__month = datetime.now().strftime('%m'), transaction_type = "Expense")
        income_amount = []
        expense_amount  = []
        for i in incomes:
            income_amount.append(i.amount)

        for i in expenses:
            expense_amount.append(i.amount)

        def total_amount(list):
            total = 0
            for i in range(len(list)):
                total += list[i]
            return total

        total_income = total_amount(income_amount)
        total_expense = total_amount(expense_amount)
        net_balance =  total_income - total_expense
        balance = abs(total_income - total_expense)
        
        return render(request,'current_month_report.html', {'total_income': total_income, 'total_expense' : total_expense, 'net_balance' : net_balance, 'balance': balance })

def previous_month_report(request):
    if request.user.is_authenticated:
        one_month_ago = datetime.now() - relativedelta(months=1)
        previous_month = one_month_ago.strftime("%m")
        incomes = transaction_details.objects.filter(user_id = request.user, date__month = previous_month, transaction_type = "Income")
        expenses = transaction_details.objects.filter(user_id = request.user, date__month = previous_month, transaction_type = "Expense")
        income_amount = []
        expense_amount  = []
        for i in incomes:
            income_amount.append(i.amount)

        for i in expenses:
            expense_amount.append(i.amount)

        def total_amount(list):
            total = 0
            for i in range(len(list)):
                total += list[i]
            return total

        total_income = total_amount(income_amount)
        total_expense = total_amount(expense_amount)
        net_balance =  total_income - total_expense
        balance = abs(total_income - total_expense)
        
        return render(request,'previous_month_report.html', {'total_income': total_income, 'total_expense' : total_expense, 'net_balance' : net_balance, 'balance': balance })

def daywise_current_month_report(request):
    if request.user.is_authenticated:
        incomes = transaction_details.objects.filter(user_id = request.user, date__month = datetime.now().strftime('%m'), transaction_type = "Income")
        expenses = transaction_details.objects.filter(user_id = request.user, date__month = datetime.now().strftime('%m'), transaction_type = "Expense")
        income_amount = []
        expense_amount  = []
        for i in incomes:
            income_amount.append(i.amount)

        for i in expenses:
            expense_amount.append(i.amount)

        def total_amount(list):
            total = 0
            for i in range(len(list)):
                total += list[i]
            return total

        total_income = total_amount(income_amount)
        total_expense = total_amount(expense_amount)
        net_balance =  total_income - total_expense
        balance = abs(total_income - total_expense)
        
        return render(request,'daywise_current_month_report.html', {'total_income': total_income, 'total_expense' : total_expense, 'net_balance' : net_balance, 'balance': balance })

def daywise_previous_month_report(request):
    if request.user.is_authenticated:
        one_month_ago = datetime.now() - relativedelta(months=1)
        previous_month = one_month_ago.strftime("%m")
        incomes = transaction_details.objects.filter(user_id = request.user, date__month = previous_month, transaction_type = "Income")
        expenses = transaction_details.objects.filter(user_id = request.user, date__month = previous_month, transaction_type = "Expense")
        income_amount = []
        expense_amount  = []
        for i in incomes:
            income_amount.append(i.amount)

        for i in expenses:
            expense_amount.append(i.amount)

        def total_amount(list):
            total = 0
            for i in range(len(list)):
                total += list[i]
            return total

        total_income = total_amount(income_amount)
        total_expense = total_amount(expense_amount)
        net_balance =  total_income - total_expense
        balance = abs(total_income - total_expense)
        
        return render(request,'daywise_previous_month_report.html', {'total_income': total_income, 'total_expense' : total_expense, 'net_balance' : net_balance, 'balance': balance })

def delete_data(request, id):
    if request.method == 'POST':
        data = transaction_details.objects.get(id = id)
        data.delete()
        return redirect('/transaction-history')

def logout_user(request):
    logout(request)
    return redirect('/login')
    
